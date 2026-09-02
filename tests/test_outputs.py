"""Verifier tests for this task.

Every test below corresponds to something instruction.md states is graded.
Shared machinery lives in harness.py.
"""

from harness import *  # noqa: F401,F403

@pytest.fixture(scope="session")
def primary_outputs():
    return _run_pipeline()


@pytest.fixture(scope="session")
def alternate_outputs():
    return _run_pipeline(input_path=ALT_INPUT)


# --------------------------------------------------------------------------
# Step one: the truncated gauge series must be rebuilt before anything is scheduled
# --------------------------------------------------------------------------
def test_recovery_sources_are_intact():
    """Every rule source is read, not rewritten."""
    live = {n: hashlib.sha256(Path(p).read_bytes()).hexdigest() for n, p in (
        ("snapshot", SNAPSHOT_PATH), ("journal", JOURNAL_PATH), ("datum", DATUM_PATH),
        ("reservoirs", RESERVOIR_PATH), ("rights", RIGHTS_PATH),
        ("policy", POLICY_PATH), ("log", LOG_PATH))}
    assert _digest(live) == FIXTURE["rule_sources_digest"]


def test_gauge_series_was_recovered():
    """The rebuilt series matches the governed replay exactly."""
    recovered = _load_json(SERIES_PATH)
    assert len(recovered) == FIXTURE["recovered_reading_count"]
    assert _digest(recovered) == FIXTURE["recovered_series_digest"]


def test_recovered_readings_carry_only_the_declared_fields():
    """Migrator bookkeeping never survives the replay."""
    for row in _load_json(SERIES_PATH):
        assert set(row) == READING_KEYS


def test_recovered_series_is_sorted():
    """The series ascends by reservoir, then day, then reading id."""
    rows = _load_json(SERIES_PATH)
    keys = [(r["reservoir_id"], r["day"], r["reading_id"]) for r in rows]
    assert keys == sorted(keys)


def test_corrected_stage_is_the_raw_stage_plus_the_datum_offset():
    """The datum correction is additive and floored at zero, never subtractive."""
    offsets = {d["sensor"]: d["datum_offset_af"] for d in _load_json(DATUM_PATH)}
    for r in _load_json(SERIES_PATH):
        expected = max(0, r["raw_inflow_af"] + offsets.get(r["sensor"], 0))
        assert r["corrected_inflow_af"] == expected, r["reading_id"]


def test_wrong_replays_differ_from_the_governed_series():
    """Four plausible misreadings of the recovery each give a different series."""
    expected = FIXTURE["recovered_series_digest"]
    assert FIXTURE["shipped_truncated_digest"] != expected
    snapshot = {r["reading_id"]: r for r in _load_json(SNAPSHOT_PATH)}
    journal = _load_json(JOURNAL_PATH)
    offsets = {d["sensor"]: d["datum_offset_af"] for d in _load_json(DATUM_PATH)}

    def replay(by_seq: bool, restore_from_snapshot: bool, subtract: bool):
        live = {k: dict(v) for k, v in snapshot.items()}
        held = {}
        for c in (sorted(journal, key=lambda x: x["seq"]) if by_seq else journal):
            k, kind = c["reading_id"], c["kind"]
            if kind == "amend" and k in live:
                live[k][c["field"]] = c["value"]
            elif kind == "retract" and k in live:
                held[k] = dict(live.pop(k))
            elif kind == "restore":
                if restore_from_snapshot:
                    if k in snapshot and k not in live:
                        live[k] = dict(snapshot[k])
                elif k in held:
                    live[k] = held.pop(k)
        rows = []
        for r in live.values():
            row = dict(r)
            off = offsets.get(row["sensor"], 0)
            row["corrected_inflow_af"] = max(
                0, row["raw_inflow_af"] - off if subtract else row["raw_inflow_af"] + off)
            rows.append(row)
        rows.sort(key=lambda r: (r["reservoir_id"], r["day"], r["reading_id"]))
        return _digest(rows)

    assert replay(False, False, False) != expected   # replayed in file order
    assert replay(True, True, False) != expected     # restore re-reads the snapshot
    assert replay(True, False, True) != expected     # datum offset subtracted
    assert replay(True, True, True) != expected


# --------------------------------------------------------------------------
# Step two: the release schedule itself
# --------------------------------------------------------------------------
def test_primary_summary_matches_fixture(primary_outputs):
    """Every summary field matches the sealed reference run."""
    _, summary, _, _ = primary_outputs
    assert summary == FIXTURE["primary"]["summary"]


def test_primary_artifacts_match_fixture(primary_outputs):
    """The schedule and the curtailment queue match the sealed digests."""
    _, _, schedule, queue = primary_outputs
    assert _digest(schedule) == FIXTURE["primary"]["schedule_digest"]
    assert _digest(queue) == FIXTURE["primary"]["queue_digest"]


def test_alternate_series_matches_fixture(alternate_outputs):
    """A held-out gauge series the agent never sees produces the sealed result."""
    _, summary, schedule, queue = alternate_outputs
    assert summary == FIXTURE["alternate"]["summary"]
    assert _digest(schedule) == FIXTURE["alternate"]["schedule_digest"]
    assert _digest(queue) == FIXTURE["alternate"]["queue_digest"]


def test_output_dir_contains_exactly_three_files(primary_outputs):
    """A run writes the three contracted artifacts and nothing else."""
    out_dir, _, _, _ = primary_outputs
    assert sorted(p.name for p in out_dir.iterdir()) == [
        "curtailment_queue.jsonl", "release_schedule.json", "summary.json"]


def test_summary_schema_and_types(primary_outputs):
    """The summary carries exactly the contracted fields at the contracted types."""
    _, summary, _, _ = primary_outputs
    assert set(summary) == SUMMARY_KEYS
    for field, kind in SPEC["outputs"]["summary"]["field_types"].items():
        value = summary[field]
        if kind == "integer":
            assert isinstance(value, int) and not isinstance(value, bool), field
        else:
            assert isinstance(value, str), field


def test_schedule_schema_and_ordering(primary_outputs):
    """Schedule rows carry the contracted fields and the contracted order."""
    _, _, schedule, _ = primary_outputs
    keys = [(r["reservoir_id"], r["day"]) for r in schedule]
    assert keys == sorted(keys)
    for r in schedule:
        assert set(r) == SCHEDULE_KEYS
        assert isinstance(r["outlet_bound"], bool)


def test_queue_schema_and_ordering(primary_outputs):
    """Curtailment rows carry the contracted fields and the contracted order."""
    _, _, _, queue = primary_outputs
    keys = [(r["day"], r["reservoir_id"], r["right_id"]) for r in queue]
    assert keys == sorted(keys)
    for r in queue:
        assert set(r) == CURTAIL_KEYS
        assert r["reason"] in CURTAIL_REASONS
        assert r["shortfall_af"] > 0


def test_every_day_of_the_horizon_is_scheduled(primary_outputs):
    """A suspect reading never removes its day from the schedule."""
    _, summary, schedule, _ = primary_outputs
    horizon = summary["effective_horizon_days"]
    reservoirs = [r["reservoir_id"] for r in _load_json(RESERVOIR_PATH)]
    assert summary["scheduled_day_count"] == len(schedule) == horizon * len(reservoirs)
    for rid in reservoirs:
        days = sorted(r["day"] for r in schedule if r["reservoir_id"] == rid)
        assert days == list(range(horizon))


def test_suspect_readings_are_excluded_from_inflow(primary_outputs):
    """Each scheduled day's inflow is the sum of its good readings only."""
    _, _, schedule, _ = primary_outputs
    good: dict[tuple[str, int], int] = {}
    for r in _load_json(SERIES_PATH):
        if r["quality"] != "suspect":
            key = (r["reservoir_id"], r["day"])
            good[key] = good.get(key, 0) + r["corrected_inflow_af"]
    for row in schedule:
        assert row["inflow_af"] == good.get((row["reservoir_id"], row["day"]), 0)


def test_releases_respect_the_outlet_limit_and_the_dead_pool(primary_outputs):
    """No day releases past the outlet, and no reservoir is drawn below its dead pool."""
    _, _, schedule, _ = primary_outputs
    register = {r["reservoir_id"]: r for r in _load_json(RESERVOIR_PATH)}
    for row in schedule:
        res = register[row["reservoir_id"]]
        assert row["total_release_af"] <= res["outlet_limit_af_day"]
        assert row["total_release_af"] == row["env_flow_af"] + row["rights_af"] + row["flood_af"]
        assert row["closing_storage_af"] >= 0
        assert row["closing_storage_af"] <= res["capacity_af"]
        assert row["outlet_bound"] == (row["total_release_af"] == res["outlet_limit_af_day"])


def test_summary_counts_track_the_artifacts(primary_outputs):
    """The summary's own totals agree with the artifacts beside it."""
    _, summary, schedule, queue = primary_outputs
    assert summary["reading_count"] == len(_load_json(SERIES_PATH))
    assert summary["reservoir_count"] == len(_load_json(RESERVOIR_PATH))
    assert summary["right_count"] == len(_load_json(RIGHTS_PATH))
    assert summary["recorded_curtailment_count"] == len(queue)
    assert summary["total_release_af"] == sum(r["total_release_af"] for r in schedule)
    assert summary["outlet_bound_day_count"] == sum(1 for r in schedule if r["outlet_bound"])


def test_both_curtailment_reasons_occur(primary_outputs):
    """The graded run exercises every documented curtailment reason."""
    _, _, _, queue = primary_outputs
    assert {r["reason"] for r in queue} == CURTAIL_REASONS


def test_the_curtailment_cap_actually_binds(primary_outputs):
    """More curtailments occur than the record admits, so the cap is load-bearing."""
    _, summary, _, _ = primary_outputs
    assert summary["recorded_curtailment_count"] == summary["effective_max_curtailments"]
    assert summary["curtailment_count"] > summary["effective_max_curtailments"]


def test_the_flood_operation_actually_occurs(primary_outputs):
    """The graded run carries real flood releases, so the flood rule is load-bearing."""
    _, _, schedule, _ = primary_outputs
    assert sum(1 for r in schedule if r["flood_af"] > 0) > 0


# --------------------------------------------------------------------------
# Each reversed rule, pinned on a crafted basin where the drafts disagree
# --------------------------------------------------------------------------
def _reservoir(rid="RES-01", *, capacity=100_000, flood_pool=90_000, dead=0,
               outlet=1_000, env=0, opening=50_000):
    return {"reservoir_id": rid, "capacity_af": capacity, "flood_pool_af": flood_pool,
            "dead_storage_af": dead, "outlet_limit_af_day": outlet,
            "min_env_flow_af_day": env, "opening_storage_af": opening}


def _right(wid, *, year=1900, daily=100, rid="RES-01"):
    return {"right_id": wid, "reservoir_id": rid, "holder": "holder-001",
            "priority_year": year, "daily_entitlement_af": daily,
            "beneficial_use": "irrigation"}


def _reading(rdg_id, *, rid="RES-01", day=0, sensor="acoustic", corrected=0, quality="good"):
    return {"reading_id": rdg_id, "reservoir_id": rid, "day": day, "sensor": sensor,
            "raw_inflow_af": corrected, "corrected_inflow_af": corrected, "quality": quality}


def _probe(readings, reservoirs, rights, *, horizon=1, curtail_year=1960,
           flood_pct=35, max_curtail=1000):
    """Run the submitted scheduler over a crafted basin and return its artifacts."""
    saved = {p: p.read_text(encoding="utf-8") for p in (RESERVOIR_PATH, RIGHTS_PATH, POLICY_PATH)}
    staged = _CWORK / f"probe-{next(_run_ctr)}.json"
    try:
        _write_json(RESERVOIR_PATH, reservoirs)
        _write_json(RIGHTS_PATH, rights)
        _write_json(POLICY_PATH, {"default": {
            "horizon_days": horizon, "curtail_below_year": curtail_year,
            "flood_release_fraction_pct": flood_pct, "max_curtailments": max_curtail}})
        _write_json(staged, readings)
        os.chmod(staged, 0o644)
        return _run_pipeline(input_path=staged)
    finally:
        for path, text in saved.items():
            path.write_text(text, encoding="utf-8")


def test_a_suspect_reading_carries_no_water_but_its_day_is_still_scheduled():
    """The suspect inflow contributes nothing, and the day still owes its minimum.

    The dropped-day draft would emit no row at all for day 0; the governed rule
    schedules it with zero inflow and still releases the environmental minimum
    out of storage.
    """
    _, summary, schedule, _ = _probe(
        [_reading("GR-1", corrected=5_000, quality="suspect")],
        [_reservoir(env=300, opening=50_000)], [])
    assert summary["scheduled_day_count"] == 1
    assert [(r["day"], r["inflow_af"], r["env_flow_af"]) for r in schedule] == [(0, 0, 300)]
    assert schedule[0]["closing_storage_af"] == 49_700


def test_the_senior_right_is_served_in_full_before_the_junior_gets_anything():
    """Priority order, not proration: 100 acre-feet go entirely to the senior right.

    Two rights of 100 each face a 100 acre-foot outlet. The prorated interim would
    give each 50; the governed rule serves 1900 in full and leaves 1955 with
    nothing, raising a single curtailment of 100.
    """
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=10_000)],
        [_reservoir(outlet=100, opening=50_000)],
        [_right("WR-0001", year=1900, daily=100), _right("WR-0002", year=1955, daily=100)])
    assert schedule[0]["rights_af"] == 100
    assert [(r["right_id"], r["shortfall_af"], r["reason"]) for r in queue] == [
        ("WR-0002", 100, "supply_short")]


def test_a_priority_tie_is_broken_by_the_lower_right_id():
    """Two rights of the same year: the lower id is served and the higher goes short."""
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=10_000)],
        [_reservoir(outlet=100, opening=50_000)],
        [_right("WR-0002", year=1900, daily=100), _right("WR-0001", year=1900, daily=100)])
    assert schedule[0]["rights_af"] == 100
    assert [r["right_id"] for r in queue] == ["WR-0002"]


def test_the_environmental_minimum_is_served_ahead_of_every_right():
    """The minimum takes its 400 acre-feet first even though a senior right wants the lot.

    The remainder draft would give the whole 1000 acre-foot outlet to the right
    and leave the minimum at zero; the governed rule takes the minimum first and
    curtails the right by 400.
    """
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=10_000)],
        [_reservoir(outlet=1_000, env=400, opening=50_000)],
        [_right("WR-0001", year=1900, daily=1_000)])
    assert [(r["env_flow_af"], r["rights_af"]) for r in schedule] == [(400, 600)]
    assert [(r["right_id"], r["shortfall_af"]) for r in queue] == [("WR-0001", 400)]


def test_the_environmental_shortfall_raises_no_curtailment_record():
    """Where the live pool cannot meet the minimum, no right is recorded as short."""
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=0)],
        [_reservoir(capacity=100_000, dead=9_000, outlet=5_000, env=2_000, opening=9_500)],
        [])
    assert schedule[0]["env_flow_af"] == 500
    assert queue == []


def test_the_flood_release_is_sized_on_the_storage_after_the_inflow():
    """The freshet lands first, then the flood cut is taken off what stands above the pool.

    Storage opens at 89,000 -- below the 90,000 flood pool, so the opening-storage
    draft would release nothing. The day's 5,000 acre-foot inflow lifts it to
    94,000, and 35 per cent of the 4,000 above the pool is 1,400.
    """
    _, _, schedule, _ = _probe(
        [_reading("GR-1", corrected=5_000)],
        [_reservoir(capacity=200_000, flood_pool=90_000, outlet=50_000, opening=89_000)],
        [])
    assert [(r["inflow_af"], r["flood_af"]) for r in schedule] == [(5_000, 1_400)]


def test_the_flood_release_is_taken_after_the_environmental_minimum():
    """The minimum comes off the storage the flood fraction is measured against.

    94,000 less the 1,000 acre-foot minimum leaves 93,000, so the cut is 35 per
    cent of 3,000 rather than of 4,000.
    """
    _, _, schedule, _ = _probe(
        [_reading("GR-1", corrected=5_000)],
        [_reservoir(capacity=200_000, flood_pool=90_000, outlet=50_000, env=1_000,
                    opening=89_000)],
        [])
    assert [(r["env_flow_af"], r["flood_af"]) for r in schedule] == [(1_000, 1_050)]


def test_the_flood_release_takes_the_outlet_ahead_of_the_appropriations():
    """With 1,500 of outlet left, the 1,400 flood cut is served and the right gets 100."""
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=5_000)],
        [_reservoir(capacity=200_000, flood_pool=90_000, outlet=1_500, opening=89_000)],
        [_right("WR-0001", year=1900, daily=900)])
    assert [(r["flood_af"], r["rights_af"]) for r in schedule] == [(1_400, 100)]
    assert [(r["right_id"], r["shortfall_af"]) for r in queue] == [("WR-0001", 800)]


def test_a_junior_right_short_on_a_flood_day_is_reasoned_flood_operation():
    """The reason follows the flood release and the policy's curtailment year.

    Both rights go short on the same flood day; the 1970 right is junior to the
    1960 policy year and is recorded as flood_operation, the 1950 right as
    supply_short.
    """
    _, _, _, queue = _probe(
        [_reading("GR-1", corrected=5_000)],
        [_reservoir(capacity=200_000, flood_pool=90_000, outlet=1_500, opening=89_000)],
        [_right("WR-0001", year=1950, daily=900), _right("WR-0002", year=1970, daily=900)],
        curtail_year=1960)
    assert [(r["right_id"], r["reason"]) for r in queue] == [
        ("WR-0001", "supply_short"), ("WR-0002", "flood_operation")]


def test_a_junior_right_short_without_a_flood_is_reasoned_supply_short():
    """The same junior right is supply_short on a day that carries no flood release."""
    _, _, schedule, queue = _probe(
        [_reading("GR-1", corrected=1_000)],
        [_reservoir(capacity=200_000, flood_pool=190_000, outlet=500, opening=50_000)],
        [_right("WR-0002", year=1970, daily=900)],
        curtail_year=1960)
    assert schedule[0]["flood_af"] == 0
    assert [(r["right_id"], r["reason"]) for r in queue] == [("WR-0002", "supply_short")]


def test_inflow_above_capacity_spills_before_any_release_is_set():
    """A reservoir never carries more than its capacity into the day's allocation."""
    _, _, schedule, _ = _probe(
        [_reading("GR-1", corrected=500_000)],
        [_reservoir(capacity=100_000, flood_pool=99_000, outlet=200, opening=99_000)],
        [])
    assert schedule[0]["closing_storage_af"] == 100_000 - 200


def test_the_curtailment_cap_truncates_the_record_but_not_the_totals():
    """Everything past the cap leaves the record while still counting in the totals."""
    _, summary, _, queue = _probe(
        [_reading("GR-1", corrected=0)],
        [_reservoir(outlet=0, opening=50_000)],
        [_right(f"WR-{i:04d}", year=1900 + i, daily=100) for i in range(1, 6)],
        max_curtail=2)
    assert summary["curtailment_count"] == 5
    assert summary["recorded_curtailment_count"] == 2 and len(queue) == 2
    assert [r["right_id"] for r in queue] == ["WR-0001", "WR-0002"]
    assert summary["total_shortfall_af"] == 500


# --------------------------------------------------------------------------
# Contract, budget, determinism and isolation
# --------------------------------------------------------------------------
def test_the_artifacts_are_serialised_exactly_as_the_contract_states(primary_outputs):
    """Read off the raw bytes, which every other check throws away by parsing.

    The contract fixes a form for all four documents and nothing here looked at
    one, so a run emitting the summary compactly, or the queue with an indent,
    matched every sealed digest.
    """
    out_dir = primary_outputs[0]
    spec = SPEC["outputs"]
    for name, section in (("summary.json", "summary"),
                          ("release_schedule.json", "release_schedule")):
        raw = (out_dir / name).read_text(encoding="utf-8")
        stated = spec[section]["serialisation"]
        assert "two-space indent" in stated and "trailing newline" in stated, stated
        assert raw.endswith("\n") and not raw.endswith("\n\n"), name
        assert raw == json.dumps(json.loads(raw), indent=2) + "\n", (
            f"{name} is not the contract's two-space indent")

    raw = (out_dir / "curtailment_queue.jsonl").read_text(encoding="utf-8")
    assert "compact JSON object per line" in spec["curtailment_queue"]["serialisation"]
    assert raw == "" or raw.endswith("\n")
    for line in raw.splitlines():
        assert line.strip(), "the queue carries a blank line"
        assert line == json.dumps(json.loads(line), separators=(",", ":")), (
            "a queue line is not compact JSON")

    # the rebuilt series is a graded artifact too, and carries its own rule
    raw = SERIES_PATH.read_text(encoding="utf-8")
    stated = SPEC["reconciled_inputs"]["gauge_readings"]["serialisation"]
    assert "two-space indent" in stated and "trailing newline" in stated, stated
    assert raw.endswith("\n") and not raw.endswith("\n\n")
    assert raw == json.dumps(json.loads(raw), indent=2) + "\n", (
        "the rebuilt gauge series is not the contract's two-space indent")


def test_each_policy_field_changes_the_behaviour_it_governs():
    """Not just the figure the summary echoes back.

    The probe beside this one reads the four effective_* fields, which an engine
    could echo from the file while still allocating on hardcoded constants. Each
    field is moved here on its own and checked against what the change implies
    for the schedule itself.
    """
    saved = POLICY_PATH.read_text(encoding="utf-8")
    shipped = json.loads(saved)["default"]
    try:
        # horizon: the schedule covers exactly the days the policy allows
        _write_json(POLICY_PATH, {"default": dict(shipped, horizon_days=12)})
        _, summary, schedule, _ = _run_pipeline()
        days = {row["day"] for row in schedule}
        assert days and max(days) < 12, (
            f"the schedule runs to day {max(days)} under a 12-day horizon")
        assert summary["effective_horizon_days"] == 12

        # flood fraction: doubling it cannot release less on any day
        _write_json(POLICY_PATH, {"default": dict(shipped, flood_release_fraction_pct=0)})
        _, _, none_flood, _ = _run_pipeline()
        _write_json(POLICY_PATH, {"default": dict(
            shipped, flood_release_fraction_pct=min(100, shipped["flood_release_fraction_pct"] * 2))})
        _, _, more_flood, _ = _run_pipeline()
        zero = {(r["reservoir_id"], r["day"]): r["flood_af"] for r in none_flood}
        assert set(zero.values()) == {0}, (
            "a zero flood fraction still released flood water, so the fraction is a constant")
        raised = [r for r in more_flood if r["flood_af"] > 0]
        assert raised, "doubling the flood fraction released no flood water anywhere"

        # curtailment cap: it binds on the queue
        _write_json(POLICY_PATH, {"default": dict(shipped, max_curtailments=3)})
        _, summary, _, queue = _run_pipeline()
        assert len(queue) <= 3, f"the cap of 3 admitted {len(queue)} curtailments"
        assert summary["effective_max_curtailments"] == 3

        # priority year: #BAS-8196 uses it to choose the reason a curtailment
        # carries, so moving it either side of every right on the register has to
        # move the labels rather than the records
        # a right counts as junior where its priority year is at or after the
        # policy's, so a year before every right on the register makes them all
        # junior and one after it makes them all senior
        _write_json(POLICY_PATH, {"default": dict(shipped, curtail_below_year=1800)})
        _, _, _, junior = _run_pipeline()
        _write_json(POLICY_PATH, {"default": dict(shipped, curtail_below_year=2100)})
        _, _, _, senior = _run_pipeline()
        assert senior and junior, "no curtailment is raised either way"
        assert {r["reason"] for r in senior} == {"supply_short"}, (
            "with every right senior to the policy year a curtailment still read "
            "flood_operation, so the year is not being read from the policy")
        assert "flood_operation" in {r["reason"] for r in junior}, (
            "with every right junior to the policy year no curtailment read "
            "flood_operation")
        assert {(r["day"], r["reservoir_id"], r["right_id"]) for r in senior} == \
            {(r["day"], r["reservoir_id"], r["right_id"]) for r in junior}, (
            "the priority year changed which rights were curtailed, not just the "
            "reason each one carries")
    finally:
        POLICY_PATH.write_text(saved, encoding="utf-8")


def test_policy_path_actually_influences_the_output():
    """The policy is resolved from its fixed path, not inlined as constants."""
    saved = POLICY_PATH.read_text(encoding="utf-8")
    try:
        _write_json(POLICY_PATH, {"default": {
            "horizon_days": 40, "curtail_below_year": 1930,
            "flood_release_fraction_pct": 60, "max_curtailments": 25}})
        _, summary, _, _ = _run_pipeline()
        assert summary["effective_horizon_days"] == 40
        assert summary["effective_curtail_year"] == 1930
        assert summary["effective_flood_fraction"] == 60
        assert summary["effective_max_curtailments"] == 25
        assert summary != FIXTURE["primary"]["summary"]
    finally:
        POLICY_PATH.write_text(saved, encoding="utf-8")


def test_reservoir_register_actually_influences_the_output():
    """The reservoir register is resolved from its fixed path too."""
    saved = RESERVOIR_PATH.read_text(encoding="utf-8")
    try:
        register = _load_json(RESERVOIR_PATH)
        for r in register:
            r["outlet_limit_af_day"] = 0
        _write_json(RESERVOIR_PATH, register)
        _, summary, schedule, _ = _run_pipeline()
        assert summary["total_release_af"] == 0
        assert all(r["total_release_af"] == 0 for r in schedule)
    finally:
        RESERVOIR_PATH.write_text(saved, encoding="utf-8")


def test_run_is_idempotent(primary_outputs):
    """Re-running over the same series reproduces the same artifacts."""
    _, summary, schedule, queue = primary_outputs
    _, s2, sc2, q2 = _run_pipeline()
    assert s2 == summary and _digest(sc2) == _digest(schedule) and _digest(q2) == _digest(queue)


def test_no_argument_run_writes_to_the_documented_defaults(primary_outputs):
    """With no flags at all the program reads and writes its documented defaults.

    The previous form still passed --output-dir, so it only exercised the --input
    default; a changed default output directory went unnoticed.
    """
    binary = _build(WORKFLOW_PATH)
    _publish_inputs()
    # /app is root-owned, so the run cannot replace this directory -- only empty
    # it, which is what the instruction and the contract ask for. The contents
    # are cleared here for the same reason.
    default_out = Path("/app/output")
    default_out.mkdir(parents=True, exist_ok=True)
    for stale in sorted(default_out.iterdir()):
        stale.unlink() if stale.is_file() or stale.is_symlink() else shutil.rmtree(stale)
    os.chmod(default_out, 0o777)
    # something for the run to clear, so the rule is exercised and not assumed
    (default_out / "left_behind.json").write_text("{}\n", encoding="utf-8")
    os.chmod(default_out / "left_behind.json", 0o666)
    (default_out / "scratch").mkdir()
    os.chmod(default_out / "scratch", 0o777)
    result = _run_agent([binary], cwd=_candidate_dir())
    assert result.returncode == 0, result.stderr
    assert sorted(q.name for q in default_out.iterdir()) == ['curtailment_queue.jsonl', 'release_schedule.json', 'summary.json']
    _, summary, doc, queue = primary_outputs
    assert _load_json(default_out / "summary.json") == summary
    assert _digest(_load_json(default_out / "release_schedule.json")) == _digest(doc)
    assert _digest(_load_jsonl(default_out / "curtailment_queue.jsonl")) == _digest(queue)


def test_submitted_program_runs_unprivileged_and_cannot_write_reward(tmp_path):
    """The graded program runs as nobody and cannot touch the reward path."""
    probe = tmp_path / "main.go"
    probe.write_text(
        'package main\n\nimport ("fmt"; "os")\n\n'
        'func main() {\n\tfmt.Println(os.Getuid())\n'
        '\terr := os.WriteFile("/logs/verifier/reward.txt", []byte("1"), 0o644)\n'
        '\tfmt.Println(err != nil)\n}\n', encoding="utf-8")
    binary = _build(probe)
    result = _run_agent([binary], cwd=_candidate_dir())
    assert result.returncode == 0, result.stderr
    parts = result.stdout.split()
    assert parts[0] == str(CANDIDATE_UID) and parts[1] == "true"


def test_frozen_snapshot_preserved():
    """The migration's scheduler must still be on disk, unmodified."""
    assert ORIGINAL_WORKFLOW_PATH.exists()
    assert hashlib.sha256(ORIGINAL_WORKFLOW_PATH.read_bytes()).hexdigest() == \
        FIXTURE["broken_scheduler_sha256"]


def test_frozen_snapshot_is_wrong(primary_outputs):
    """The shipped scheduler does not already produce the governed schedule."""
    _, summary, _, _ = primary_outputs
    _, broken, _, _ = _run_pipeline(script_path=ORIGINAL_WORKFLOW_PATH)
    assert broken != summary


def test_governance_log_present():
    """The minute book the rules are reconstructed from is in the environment."""
    assert LOG_PATH.exists() and LOG_PATH.stat().st_size > 0


def test_rights_register_actually_influences_the_output():
    """The rights register is resolved from its fixed path, not inlined."""
    saved = RIGHTS_PATH.read_text(encoding="utf-8")
    try:
        _write_json(RIGHTS_PATH, [])
        _, summary, schedule, queue = _run_pipeline()
        assert summary["right_count"] == 0
        assert all(row["rights_af"] == 0 for row in schedule)
        assert queue == []
    finally:
        RIGHTS_PATH.write_text(saved, encoding="utf-8")


def test_shipped_contract_matches_the_golden_copy():
    """The output contract in the environment is unmodified.

    Field lists, container shapes and sort orders are golden metadata and are read
    from the verifier's own image; this proves the agent's copy still agrees with
    it, so the contract cannot be trimmed to weaken a schema check.
    """
    shipped = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert shipped == json.loads(GOLDEN_CONTRACT_PATH.read_text(encoding="utf-8"))
