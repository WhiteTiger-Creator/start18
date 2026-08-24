// Stage one of the reference: rebuild the gauge series the telemetry migration
// truncated at /app/data/gauge_readings.json.
//
// Governed by #BAS-8170 (replay semantics), #BAS-8174 (datum correction) and
// #BAS-8178 (shape and ordering of the result).
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"
)

type reading struct {
	ReadingID    string `json:"reading_id"`
	ReservoirID  string `json:"reservoir_id"`
	Day          int    `json:"day"`
	Sensor       string `json:"sensor"`
	RawInflowAF  int64  `json:"raw_inflow_af"`
	CorrectedAF  int64  `json:"corrected_inflow_af"`
	Quality      string `json:"quality"`
}

type change struct {
	Seq       int    `json:"seq"`
	ReadingID string `json:"reading_id"`
	Kind      string `json:"kind"`
	Field     string `json:"field"`
	Value     any    `json:"value"`
}

type datumRow struct {
	Sensor        string `json:"sensor"`
	DatumOffsetAF int64  `json:"datum_offset_af"`
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

func setField(r *reading, field string, value any) {
	switch field {
	case "quality":
		if s, ok := value.(string); ok {
			r.Quality = s
		}
	case "sensor":
		if s, ok := value.(string); ok {
			r.Sensor = s
		}
	case "raw_inflow_af":
		switch v := value.(type) {
		case float64:
			r.RawInflowAF = int64(v)
		case string:
			if n, err := strconv.ParseInt(v, 10, 64); err == nil {
				r.RawInflowAF = n
			}
		}
	}
}

func main() {
	var snapshot []reading
	var journal []change
	var data []datumRow
	readJSON("/app/data/gauge_snapshot_pre_migration.json", &snapshot)
	readJSON("/app/data/telemetry_journal.json", &journal)
	readJSON("/app/data/sensor_datum.json", &data)

	offset := make(map[string]int64, len(data))
	for _, d := range data {
		offset[d.Sensor] = d.DatumOffsetAF
	}

	live := make(map[string]*reading, len(snapshot))
	for i := range snapshot {
		r := snapshot[i]
		live[r.ReadingID] = &r
	}
	// #BAS-8170: a retraction takes the reading out but the basin office keeps it,
	// so a later restore returns it exactly as it then stood -- an amendment posted
	// before survives, one posted while it was out is lost.
	held := map[string]reading{}

	sort.Slice(journal, func(i, j int) bool { return journal[i].Seq < journal[j].Seq })
	for _, c := range journal {
		switch c.Kind {
		case "amend":
			if r, ok := live[c.ReadingID]; ok {
				setField(r, c.Field, c.Value)
			}
		case "retract":
			if r, ok := live[c.ReadingID]; ok {
				held[c.ReadingID] = *r
				delete(live, c.ReadingID)
			}
		case "restore":
			if r, ok := held[c.ReadingID]; ok {
				restored := r
				live[c.ReadingID] = &restored
				delete(held, c.ReadingID)
			}
		}
	}

	out := make([]reading, 0, len(live))
	for _, r := range live {
		// #BAS-8174: the sensor's datum offset is ADDED to the raw stage to bring the
		// reading onto the basin datum. A sensor the table does not carry is left as
		// read. A corrected inflow never falls below zero.
		v := r.RawInflowAF + offset[r.Sensor]
		if v < 0 {
			v = 0
		}
		r.CorrectedAF = v
		out = append(out, *r)
	}
	// #BAS-8178: ascending reservoir, then day, then reading id.
	sort.Slice(out, func(i, j int) bool {
		a, b := out[i], out[j]
		if a.ReservoirID != b.ReservoirID {
			return a.ReservoirID < b.ReservoirID
		}
		if a.Day != b.Day {
			return a.Day < b.Day
		}
		return a.ReadingID < b.ReadingID
	})

	encoded, err := json.MarshalIndent(out, "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := os.WriteFile("/app/data/gauge_readings.json", append(encoded, '\n'), 0o644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Fprintf(os.Stderr, "recovered %d readings\n", len(out))
}
