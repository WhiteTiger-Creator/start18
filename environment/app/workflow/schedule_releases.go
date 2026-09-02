// Reservoir release scheduler shipped before the basin board's operations review.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
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
	ReservoirID string `json:"reservoir_id"`
	Day         int    `json:"day"`
	InflowAF    int64  `json:"inflow_af"`
	EnvFlowAF   int64  `json:"env_flow_af"`
	RightsAF    int64  `json:"rights_af"`
	FloodAF     int64  `json:"flood_af"`
	TotalAF     int64  `json:"total_release_af"`
	ClosingAF   int64  `json:"closing_storage_af"`
	OutletBound bool   `json:"outlet_bound"`
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

func main() {
	input := flag.String("input", "/app/data/gauge_readings.json", "recovered gauge series")
	outputDir := flag.String("output-dir", "/app/output", "output directory")
	flag.Parse()

	var readings []reading
	var reservoirs []reservoir
	var rights []right
	var pol policy
	readJSON("/app/data/reservoir_register.json", &reservoirs)
	readJSON("/app/data/rights_register.json", &rights)
	readJSON("/app/data/operating_policy.json", &pol)
	readJSON(*input, &readings)

	horizon := int(pol.Default["horizon_days"])
	curtailBelow := int(pol.Default["curtail_below_year"])
	floodPct := pol.Default["flood_release_fraction_pct"]
	maxCurtail := int(pol.Default["max_curtailments"])

	// Inflow per reservoir-day, and the days this run passes over.
	inflow := map[string]map[int]int64{}
	skip := map[string]map[int]bool{}
	for _, r := range readings {
		if inflow[r.ReservoirID] == nil {
			inflow[r.ReservoirID] = map[int]int64{}
			skip[r.ReservoirID] = map[int]bool{}
		}
		if r.Quality == "suspect" {
			skip[r.ReservoirID][r.Day] = true
			continue
		}
		inflow[r.ReservoirID][r.Day] += r.CorrectedAF
	}

	byRes := map[string][]right{}
	for _, w := range rights {
		byRes[w.ReservoirID] = append(byRes[w.ReservoirID], w)
	}
	for id := range byRes {
		list := byRes[id]
		sort.Slice(list, func(i, j int) bool { return list[i].RightID < list[j].RightID })
		byRes[id] = list
	}

	sort.Slice(reservoirs, func(i, j int) bool { return reservoirs[i].ReservoirID < reservoirs[j].ReservoirID })

	schedule := make([]releaseRow, 0)
	curtailments := make([]curtailRow, 0)
	var totalRelease, totalShort int64
	outletBoundDays := 0

	for _, res := range reservoirs {
		storage := res.OpeningStorage
		for day := 0; day < horizon; day++ {
			if skip[res.ReservoirID][day] {
				continue
			}
			opening := storage
			storage += inflow[res.ReservoirID][day]
			if storage > res.CapacityAF {
				storage = res.CapacityAF
			}
			available := storage - res.DeadStorageAF
			if available < 0 {
				available = 0
			}
			room := res.OutletLimitAF

			// Flood release for the day.
			var flood int64
			if opening > res.FloodPoolAF {
				flood = ((opening - res.FloodPoolAF) * floodPct) / 100
				if flood > room {
					flood = room
				}
				if flood > available {
					flood = available
				}
				available -= flood
				room -= flood
			}

			// Allocation of the day's water across the outlet's claims.
			var demand int64
			for _, w := range byRes[res.ReservoirID] {
				demand += w.DailyAF
			}
			pool := available
			if pool > room {
				pool = room
			}
			var served int64
			for _, w := range byRes[res.ReservoirID] {
				give := w.DailyAF
				if demand > pool && demand > 0 {
					give = (w.DailyAF * pool) / demand
				}
				served += give
				if give < w.DailyAF {
					reason := "supply_short"
					if w.PriorityYear >= curtailBelow {
						reason = "flood_operation"
					}
					curtailments = append(curtailments, curtailRow{
						Day: day, ReservoirID: res.ReservoirID, RightID: w.RightID,
						ShortfallAF: w.DailyAF - give, Reason: reason,
					})
					totalShort += w.DailyAF - give
				}
			}
			available -= served
			room -= served

			env := res.MinEnvFlowAF
			if env > room {
				env = room
			}
			if env > available {
				env = available
			}
			if env < 0 {
				env = 0
			}
			available -= env
			room -= env

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

	sort.Slice(curtailments, func(i, j int) bool {
		a, b := curtailments[i], curtailments[j]
		if a.ReservoirID != b.ReservoirID {
			return a.ReservoirID < b.ReservoirID
		}
		if a.Day != b.Day {
			return a.Day < b.Day
		}
		return a.RightID < b.RightID
	})
	recorded := curtailments
	if maxCurtail > 0 && len(recorded) > maxCurtail {
		recorded = recorded[:maxCurtail]
	}

	if err := os.MkdirAll(*outputDir, 0o755); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
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
