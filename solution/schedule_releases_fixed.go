// Stage two of the reference: the corrected release scheduler.
//
// Every governing value is traced to its final dated entry in
// /app/incident/basin_governance_log.md; release_contract.json supplies the
// output contract only and no derivation rule.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"sort"
)

type reading struct {
	ReadingID   string `json:"reading_id"`
	ReservoirID string `json:"reservoir_id"`
	Day         int    `json:"day"`
	Sensor      string `json:"sensor"`
	RawInflowAF int64  `json:"raw_inflow_af"`
	CorrectedAF int64  `json:"corrected_inflow_af"`
	Quality     string `json:"quality"`
}

type reservoir struct {
	ReservoirID    string `json:"reservoir_id"`
	CapacityAF     int64  `json:"capacity_af"`
	FloodPoolAF    int64  `json:"flood_pool_af"`
	DeadStorageAF  int64  `json:"dead_storage_af"`
	OutletLimitAF  int64  `json:"outlet_limit_af_day"`
	MinEnvFlowAF   int64  `json:"min_env_flow_af_day"`
	OpeningStorage int64  `json:"opening_storage_af"`
}

type right struct {
	RightID      string `json:"right_id"`
	ReservoirID  string `json:"reservoir_id"`
	Holder       string `json:"holder"`
	PriorityYear int    `json:"priority_year"`
	DailyAF      int64  `json:"daily_entitlement_af"`
	Use          string `json:"beneficial_use"`
}

type policy struct {
	Default map[string]int64 `json:"default"`
}

type releaseRow struct {
	ReservoirID  string `json:"reservoir_id"`
	Day          int    `json:"day"`
	InflowAF     int64  `json:"inflow_af"`
	EnvFlowAF    int64  `json:"env_flow_af"`
	RightsAF     int64  `json:"rights_af"`
	FloodAF      int64  `json:"flood_af"`
	TotalAF      int64  `json:"total_release_af"`
	ClosingAF    int64  `json:"closing_storage_af"`
	OutletBound  bool   `json:"outlet_bound"`
}

type curtailRow struct {
	Day         int    `json:"day"`
	ReservoirID string `json:"reservoir_id"`
	RightID     string `json:"right_id"`
	ShortfallAF int64  `json:"shortfall_af"`
	Reason      string `json:"reason"`
}

func readJSON(path string, into any) {
	raw, err := os.ReadFile(path)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.Unmarshal(raw, into); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func writeJSON(path string, value any) {
	encoded, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := os.WriteFile(path, append(encoded, '\n'), 0o644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

// The policy is read from its fixed absolute path, and any field the file omits
// keeps its governed baseline. A missing Go map key is zero, not the baseline,
// so the fallback has to be explicit.
func policyValue(pol policy, field string, baseline int64) int64 {
	if value, ok := pol.Default[field]; ok {
		return value
	}
	return baseline
}

func main() {
	input := flag.String("input", "/app/data/gauge_readings.json", "recovered gauge series")
	outputDir := flag.String("output-dir", "/app/output", "output directory")
	flag.Parse()

	var readings []reading
	var reservoirs []reservoir
	var rights []right
	var pol policy
	// #BAS-8150: the reservoir register, the rights register and the operating
	// policy are always read from their fixed absolute paths; --input selects the
	// gauge series only.
	readJSON("/app/data/reservoir_register.json", &reservoirs)
	readJSON("/app/data/rights_register.json", &rights)
	readJSON("/app/data/operating_policy.json", &pol)
	readJSON(*input, &readings)

	horizon := int(policyValue(pol, "horizon_days", 180))
	curtailBelow := int(policyValue(pol, "curtail_below_year", 1960))
	floodPct := policyValue(pol, "flood_release_fraction_pct", 35)
	maxCurtail := int(policyValue(pol, "max_curtailments", 2400))

	// #BAS-8182: a reading the basin office has marked suspect carries no water; it
	// is treated as zero inflow for the day rather than dropped, so the day is still
	// scheduled.
	inflow := map[string]map[int]int64{}
	for _, r := range readings {
		if inflow[r.ReservoirID] == nil {
			inflow[r.ReservoirID] = map[int]int64{}
		}
		if r.Quality == "suspect" {
			continue
		}
		inflow[r.ReservoirID][r.Day] += r.CorrectedAF
	}

	byRes := map[string][]right{}
	for _, w := range rights {
		byRes[w.ReservoirID] = append(byRes[w.ReservoirID], w)
	}
	// #BAS-8186: rights are served in priority order, the oldest appropriation
	// first, and a tie goes to the lower right id. Junior rights go short before
	// senior ones -- the basin never prorates across the whole set.
	for id := range byRes {
		list := byRes[id]
		sort.Slice(list, func(i, j int) bool {
			if list[i].PriorityYear != list[j].PriorityYear {
				return list[i].PriorityYear < list[j].PriorityYear
			}
			return list[i].RightID < list[j].RightID
		})
		byRes[id] = list
	}

	sort.Slice(reservoirs, func(i, j int) bool { return reservoirs[i].ReservoirID < reservoirs[j].ReservoirID })

	schedule := make([]releaseRow, 0)
	curtailments := make([]curtailRow, 0)
	var totalRelease, totalShort int64
	outletBoundDays, deficitLedDays := 0, 0

	for _, res := range reservoirs {
		storage := res.OpeningStorage
		// #BAS-8214: the rights carrying a deficit against this reservoir. A
		// deficit is a place in the queue and never a quantity, so the set of
		// rights carrying one is all that has to be kept.
		carrying := map[string]bool{}
		for day := 0; day < horizon; day++ {
			storage += inflow[res.ReservoirID][day]
			if storage > res.CapacityAF {
				storage = res.CapacityAF
			}
			available := storage - res.DeadStorageAF
			if available < 0 {
				available = 0
			}
			room := res.OutletLimitAF

			// #BAS-8190: the environmental minimum is served BEFORE any appropriation,
			// out of whatever the outlet and the live pool allow. It is never curtailed
			// in favour of a right.
			env := res.MinEnvFlowAF
			if env > room {
				env = room
			}
			if env > available {
				env = available
			}
			available -= env
			room -= env

			// #BAS-8194: a flood release is set on the storage as it stands AFTER the
			// day's inflow and after the environmental minimum, taking the stated
			// fraction of whatever sits above the flood pool, and it takes precedence
			// over the appropriations for the outlet that remains.
			var flood int64
			if storage-env > res.FloodPoolAF {
				flood = ((storage - env - res.FloodPoolAF) * floodPct) / 100
				if flood > room {
					flood = room
				}
				if flood > available {
					flood = available
				}
				available -= flood
				room -= flood
			}

			// #BAS-8214: rights carrying a deficit lead, keeping the ordinary
			// priority order among themselves; the rest follow in theirs. byRes is
			// already in priority order, so one pass over it preserves both.
			leading := make([]right, 0, len(byRes[res.ReservoirID]))
			following := make([]right, 0, len(byRes[res.ReservoirID]))
			for _, w := range byRes[res.ReservoirID] {
				if carrying[w.RightID] {
					leading = append(leading, w)
				} else {
					following = append(following, w)
				}
			}
			if len(leading) > 0 {
				deficitLedDays++
			}
			order := append(leading, following...)

			var served int64
			for _, w := range order {
				want := w.DailyAF
				give := want
				if give > room {
					give = room
				}
				if give > available {
					give = available
				}
				if give < 0 {
					give = 0
				}
				served += give
				available -= give
				room -= give
				if give < want {
					reason := "supply_short"
					// #BAS-8196: a right junior to the policy's curtailment year that
					// goes short in a flood window is recorded as curtailed by the
					// flood operation rather than by shortage.
					if flood > 0 && w.PriorityYear >= curtailBelow {
						reason = "flood_operation"
					}
					curtailments = append(curtailments, curtailRow{
						Day: day, ReservoirID: res.ReservoirID, RightID: w.RightID,
						ShortfallAF: want - give, Reason: reason,
					})
					totalShort += want - give
					// A flood day raises no deficit: the shortage is the flood
					// operation's doing. The curtailment is recorded either way.
					if flood == 0 {
						carrying[w.RightID] = true
					}
				} else {
					// served in full, so the deficit it was carrying is cleared
					delete(carrying, w.RightID)
				}
			}

			total := env + flood + served
			storage -= total
			if storage < 0 {
				storage = 0
			}
			totalRelease += total
			bound := total == res.OutletLimitAF
			if bound {
				outletBoundDays++
			}
			schedule = append(schedule, releaseRow{
				ReservoirID: res.ReservoirID, Day: day,
				InflowAF: inflow[res.ReservoirID][day], EnvFlowAF: env,
				RightsAF: served, FloodAF: flood, TotalAF: total,
				ClosingAF: storage, OutletBound: bound,
			})
		}
	}

	// #BAS-8198: the schedule is emitted by reservoir then day; the curtailment
	// queue by day, then reservoir, then right id, and is capped by policy.
	sort.Slice(curtailments, func(i, j int) bool {
		a, b := curtailments[i], curtailments[j]
		if a.Day != b.Day {
			return a.Day < b.Day
		}
		if a.ReservoirID != b.ReservoirID {
			return a.ReservoirID < b.ReservoirID
		}
		return a.RightID < b.RightID
	})
	// #BAS-8198: everything past the cap is dropped from the record though it
	// still counts in the totals. The cap applies at every value it can take,
	// zero included -- guarding on maxCurtail > 0 made a cap of zero mean "no
	// limit", which is the opposite of what the decision says.
	recorded := curtailments
	limit := maxCurtail
	if limit < 0 {
		limit = 0
	}
	if len(recorded) > limit {
		recorded = recorded[:limit]
	}

	if err := os.MkdirAll(*outputDir, 0o755); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	// Anything an earlier run left here is cleared before this run writes, so no
	// stale artifact is passed off as part of this output. The directory itself
	// stays: the run does not own the path it writes into.
	if entries, err := os.ReadDir(*outputDir); err == nil {
		for _, e := range entries {
			os.RemoveAll(filepath.Join(*outputDir, e.Name()))
		}
	}
	summary := map[string]any{
		"schema_version":             "basin-release-v1",
		"reading_count":              len(readings),
		"reservoir_count":            len(reservoirs),
		"right_count":                len(rights),
		"scheduled_day_count":        len(schedule),
		"total_release_af":           totalRelease,
		"total_shortfall_af":         totalShort,
		"curtailment_count":          len(curtailments),
		"recorded_curtailment_count": len(recorded),
		"outlet_bound_day_count":     outletBoundDays,
		"effective_horizon_days":     horizon,
		"effective_curtail_year":     curtailBelow,
		"effective_flood_fraction":   floodPct,
		"effective_max_curtailments": maxCurtail,
		"deficit_led_service_count":  deficitLedDays,
	}
	writeJSON(*outputDir+"/summary.json", summary)
	writeJSON(*outputDir+"/release_schedule.json", schedule)

	handle, err := os.Create(*outputDir + "/curtailment_queue.jsonl")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer handle.Close()
	enc := json.NewEncoder(handle)
	for _, row := range recorded {
		if err := enc.Encode(row); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	fmt.Fprintf(os.Stderr, "scheduled %d reservoir-days, %d curtailments\n",
		len(schedule), len(curtailments))
}
