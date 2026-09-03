# Planning governance log

How the release scheduler is *meant* to behave -- the recovery of the truncated gauge series, what a
reading the basin office has marked suspect contributes, in what order the appropriations are
served, where the environmental minimum sits against them, how a flood release is sized and what
the curtailment record carries -- was settled incrementally by the basin board, and those decisions
live in the review entries below, not in any single summary. Several stages deliberately depart from the intuitive reading, and which ones they are is settled in the entries below rather than here. The February draft proposals were
An on-call engineer signed off a routine observation. A batch retried once after a transient timeout and completed on the second pass. Nothing here bears on engine behaviour.
A reviewer on shift logged a routine observation. Two accounts showed a same-day transfer the export had not yet picked up.
A weekly review carried forward a routine observation. Late inputs arrived from one feed and were loaded before the cut. No action was carried forward.


- 2026-02-20: The platform team recorded a routine observation. Late inputs arrived from one feed and were loaded before the cut. No action was carried forward.

- 2026-02-06: The platform team spot-checked a routine observation. One record appeared twice in the export after a mid-cycle correction.

> **Recovery draft proposal (2026-02-06 - #BAS-8020)** Rosa: rebuild the truncated gauge series by concatenating the pre-migration snapshot with the telemetry journal and keeping the last row seen for each reading; a restored reading is re-read from the snapshot *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-13: A shift handover opened a query on a routine observation. The downstream vendor confirmed receipt inside the agreed window. Nothing here bears on engine behaviour.

> **Recovery draft proposal (2026-02-13 - #BAS-8026)** Anders: the sensor's datum offset is SUBTRACTED from the raw stage, the offset being the amount by which the family reads high *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-26: The platform team logged a routine observation. One record appeared twice in the export after a mid-cycle correction. No action was carried forward.

- 2026-02-10: A stand-up note recorded a routine observation. The count sat a little above the running mean, entirely from estimated inputs. Filed for the record.

> **Recovery draft proposal (2026-02-19 - #BAS-8032)** Marek: a reading the basin office has marked suspect is dropped, and the day it covers drops out of the schedule with it *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-26: The audit lead spot-checked a routine observation. A duplicate order was cancelled at source and never reached the run. No action was carried forward.

- 2026-02-16: The exceptions queue owner raised and closed a routine observation. The overnight window ran long behind an unrelated platform patch.

- 2026-02-06: The reconciliation desk logged a routine observation. A query about a prior-period entry was answered from the published schedule.

- 2026-02-27: The reconciliation desk filed a routine observation. One record appeared twice in the export after a mid-cycle correction.

- 2026-02-19: An on-call engineer recorded a routine observation. A query about a prior-period entry was answered from the published schedule. Closed with no parameter change.

- 2026-02-01: A reviewer on shift noted a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. Referred to the dated decisions and closed.

- 2026-02-03: The reconciliation desk carried forward a routine observation. Two accounts showed a same-day transfer the export had not yet picked up.

- 2026-02-05: A weekly review recorded a routine observation. Storage on the staging host was extended after the export outgrew its allocation.

- 2026-02-21: The audit lead spot-checked a routine observation. The variance sat inside tolerance and no adjustment was raised. The desk confirmed no downstream impact.

- 2026-02-25: The audit lead recorded a routine observation. The downstream vendor confirmed receipt inside the agreed window. The thread was archived after review.

- 2026-02-02: An on-call engineer filed a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. The desk confirmed no downstream impact.

- 2026-02-14: The audit lead carried forward a routine observation. Dashboard tiles lagged the refresh; traced to cache staleness rather than the engine. Filed for the record.

- 2026-02-17: The controls team signed off a routine observation. Two accounts showed a same-day transfer the export had not yet picked up.

- 2026-02-24: The platform team reviewed a routine observation. A typo in a reference record was corrected before the run started. The desk confirmed no downstream impact.

> **Interim decision (2026-03-05 - #BAS-8038)** Priya: where the day cannot meet the appropriations in full, the shortage is prorated across every right on the reservoir in proportion to its entitlement *(Revised -- see the 2026-05 operations review.)*

- 2026-03-01: The operations desk reviewed a routine observation. A duplicate order was cancelled at source and never reached the run. Referred to the dated decisions and closed.

- 2026-03-24: A stand-up note spot-checked a routine observation. A query about a prior-period entry was answered from the published schedule. Filed for the record.

- 2026-03-10: A shift handover noted a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-03-11: An on-call engineer signed off a routine observation. A batch retried once after a transient timeout and completed on the second pass. The desk confirmed no downstream impact.

- 2026-03-09: A reviewer on shift logged a routine observation. One record appeared twice in the export after a mid-cycle correction. The thread was archived after review.

- 2026-03-13: The duty analyst opened a query on a routine observation. A typo in a reference record was corrected before the run started.

- 2026-03-04: The audit lead signed off a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-03-17: A stand-up note signed off a routine observation. The downstream vendor confirmed receipt inside the agreed window.

- 2026-03-12: A shift handover logged a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-03-09: A shift handover filed a routine observation. A question raised on the floor was withdrawn once the entry was reread.

- 2026-03-14: The operations desk opened a query on a routine observation. A duplicate order was cancelled at source and never reached the run. Nothing here bears on engine behaviour.

- 2026-03-15: The audit lead opened a query on a routine observation. The variance sat inside tolerance and no adjustment was raised. Nothing here bears on engine behaviour.

> **Interim decision (2026-03-11 - #BAS-8044)** Anders: the environmental minimum is served out of whatever remains once the appropriations have been met, the rights having the senior claim on the outlet *(Revised -- see the 2026-05 operations review.)*

- 2026-03-21: The controls team filed a routine observation. The count sat a little above the running mean, entirely from estimated inputs. Referred to the dated decisions and closed.

- 2026-03-22: The operations desk signed off a routine observation. One record appeared twice in the export after a mid-cycle correction. No follow-up was requested.

- 2026-03-23: The controls team signed off a routine observation. A question raised on the floor was withdrawn once the entry was reread.

- 2026-03-04: The operations desk recorded a routine observation. A duplicate order was cancelled at source and never reached the run.

- 2026-03-06: An on-call engineer noted a routine observation. A duplicate order was cancelled at source and never reached the run. No action was carried forward.

- 2026-03-13: The duty analyst logged a routine observation. One record appeared twice in the export after a mid-cycle correction. Filed for the record.

- 2026-03-13: The controls team recorded a routine observation. A batch retried once after a transient timeout and completed on the second pass. The thread was archived after review.

- 2026-03-23: An on-call engineer recorded a routine observation. A typo in a reference record was corrected before the run started.

- 2026-03-26: The exceptions queue owner reviewed a routine observation. A query about a prior-period entry was answered from the published schedule. Nothing here bears on engine behaviour.

- 2026-03-25: The audit lead noted a routine observation. Nightly reconciliation matched exactly and the file was released without comment.

- 2026-03-19: A reviewer on shift signed off a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. Closed with no parameter change.

- 2026-03-19: The audit lead reviewed a routine observation. Late inputs arrived from one feed and were loaded before the cut. Nothing here bears on engine behaviour.

- 2026-03-18: The reconciliation desk spot-checked a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. No action was carried forward.

- 2026-03-20: The platform team reviewed a routine observation. A batch retried once after a transient timeout and completed on the second pass. No action was carried forward.

- 2026-04-17: The audit lead raised and closed a routine observation. Storage on the staging host was extended after the export outgrew its allocation. Referred to the dated decisions and closed.

- 2026-04-20: A weekly review opened a query on a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-04-25: A weekly review filed a routine observation. Nightly reconciliation matched exactly and the file was released without comment.

- 2026-04-17: The controls team reviewed a routine observation. Late inputs arrived from one feed and were loaded before the cut. Nothing here bears on engine behaviour.

- 2026-04-12: The duty analyst raised and closed a routine observation. The downstream vendor confirmed receipt inside the agreed window. The desk confirmed no downstream impact.

- 2026-04-13: The audit lead raised and closed a routine observation. One record appeared twice in the export after a mid-cycle correction.

- 2026-04-18: A reviewer on shift opened a query on a routine observation. Nightly reconciliation matched exactly and the file was released without comment.

- 2026-04-25: The duty analyst reviewed a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. Nothing here bears on engine behaviour.

- 2026-04-03: The exceptions queue owner logged a routine observation. One record appeared twice in the export after a mid-cycle correction. No follow-up was requested.

- 2026-04-09: A reviewer on shift recorded a routine observation. Dashboard tiles lagged the refresh; traced to cache staleness rather than the engine.

- 2026-04-23: The operations desk signed off a routine observation. Dashboard tiles lagged the refresh; traced to cache staleness rather than the engine. The thread was archived after review.

- 2026-04-27: The duty analyst recorded a routine observation. The overnight window ran long behind an unrelated platform patch.

- 2026-04-06: The reconciliation desk opened a query on a routine observation. The overnight window ran long behind an unrelated platform patch.

- 2026-04-10: The audit lead opened a query on a routine observation. The count sat a little above the running mean, entirely from estimated inputs. No follow-up was requested.

- 2026-04-23: The platform team logged a routine observation. Dashboard tiles lagged the refresh; traced to cache staleness rather than the engine.

- 2026-04-03: The platform team noted a routine observation. The variance sat inside tolerance and no adjustment was raised. Closed with no parameter change.

- 2026-04-08: The controls team reviewed a routine observation. Two accounts showed a same-day transfer the export had not yet picked up. Nothing here bears on engine behaviour.

- 2026-04-06: A shift handover spot-checked a routine observation. The overnight window ran long behind an unrelated platform patch.

- 2026-04-19: The reconciliation desk logged a routine observation. Storage on the staging host was extended after the export outgrew its allocation. The thread was archived after review.

- 2026-04-09: The duty analyst raised and closed a routine observation. A query about a prior-period entry was answered from the published schedule.

- 2026-04-02: The operations desk reviewed a routine observation. The overnight window ran long behind an unrelated platform patch. No action was carried forward.

- 2026-04-06: A stand-up note reviewed a routine observation. A question raised on the floor was withdrawn once the entry was reread.

- 2026-05-27: A shift handover raised and closed a routine observation. The downstream vendor confirmed receipt inside the agreed window.

> **Governance decision (2026-05-05 - #BAS-8150)** Priya: Input paths, final. The reservoir register, the rights register and the operating policy are always read from their fixed absolute paths under /app/data; `--input` selects the gauge series only. Both `--input` and `--output-dir` keep their documented defaults.

> **Governance decision (2026-05-07 - #BAS-8170)** Yusuf: Gauge recovery, final (supersedes #BAS-8020). Start from the pre-migration snapshot and replay the telemetry journal in ascending `seq`, never in file order, keying each change on the reading it names. An `amend` overwrites the named field in place. A `retract` takes the reading out, but the basin office keeps it as it stood at that moment. A `restore` returns a retracted reading EXACTLY as it then stood: an amendment posted before the retraction survives, and one posted while it was out is lost. A change naming a reading the snapshot never carried is ignored.

> **Governance decision (2026-05-08 - #BAS-8174)** Yusuf: Datum correction, final (supersedes #BAS-8026; deviates from the subtractive reading). The sensor family's datum offset is ADDED to the raw stage to bring the reading onto the basin datum, the offset being signed for that purpose. A sensor the datum table does not carry keeps its raw stage. A corrected inflow never falls below zero.

> **Governance decision (2026-05-09 - #BAS-8178)** Yusuf: Recovered shape, final. The rebuilt series is a JSON array ascending by reservoir id, then day, then reading id, and each row carries the seven reading fields -- the migrator's bookkeeping (`seq`, `kind`, `posted_by`) never survives the replay.

> **Governance decision (2026-05-12 - #BAS-8182)** Lena: Suspect readings, final (supersedes #BAS-8032; deviates from the dropped-day reading). A reading the basin office has marked suspect carries no water: it contributes ZERO inflow for its reservoir-day. The day itself is still scheduled, and the reservoir still owes its environmental minimum on it out of storage.

> **Governance decision (2026-05-15 - #BAS-8186)** Marek: Allocation order, final (revises #BAS-8038; deviates from the prorated interim). The appropriations are served in strict priority order, the oldest appropriation year first and a tie going to the lower right id, each taken in full before the next is considered. The basin never prorates: a junior right goes short, or goes without entirely, before a senior right gives up an acre-foot.

> **Governance decision (2026-05-18 - #BAS-8190)** Marek: Environmental minimum, final (revises #BAS-8044; deviates from the remainder reading). The reservoir's minimum environmental flow is served BEFORE any appropriation, out of whatever the outlet and the live pool allow, and it is never curtailed in favour of a right. Where the live pool cannot meet it in full the reservoir releases what it has, and no curtailment record is raised for the shortfall.

> **Governance decision (2026-05-21 - #BAS-8194)** Priya: Flood operation, final. A flood release is sized on the storage as it stands AFTER the day's inflow and after the environmental minimum has been set aside, taking the policy's flood_release_fraction_pct of whatever sits above the reservoir's flood pool, floored to whole acre-feet. It takes precedence over the appropriations for whatever outlet capacity remains.

> **Governance decision (2026-05-24 - #BAS-8196)** Yusuf: Curtailment record, final. A right served less than its entitlement raises one curtailment record for the day carrying the acre-feet it went short. Where the day carried a flood release and the right is junior to the policy's curtail_below_year, the reason is `flood_operation`; otherwise it is `supply_short`.

> **Governance decision (2026-05-27 - #BAS-8198)** Lena: Release accounting, final. No reservoir releases more than its outlet limit on a day, nor draws its storage below the dead pool, and inflow above capacity spills unrecorded before any release is set. The schedule is emitted by reservoir and then day; the curtailment queue by day, then reservoir, then right id, and everything past the policy's max_curtailments is dropped from the record though it still counts in the totals.

- 2026-05-09: The duty analyst noted a routine observation. The downstream vendor confirmed receipt inside the agreed window.

- 2026-05-07: The duty analyst carried forward a routine observation. A duplicate order was cancelled at source and never reached the run. The thread was archived after review.

- 2026-05-21: A stand-up note reviewed a routine observation. The downstream vendor confirmed receipt inside the agreed window. No follow-up was requested.

- 2026-05-17: The platform team carried forward a routine observation. One record appeared twice in the export after a mid-cycle correction. The desk confirmed no downstream impact.

- 2026-05-17: A weekly review raised and closed a routine observation. Late inputs arrived from one feed and were loaded before the cut. Filed for the record.

- 2026-05-08: The platform team reviewed a routine observation. Late inputs arrived from one feed and were loaded before the cut. No follow-up was requested.

- 2026-05-23: An on-call engineer carried forward a routine observation. The downstream vendor confirmed receipt inside the agreed window. Referred to the dated decisions and closed.

- 2026-05-14: An on-call engineer raised and closed a routine observation. A question raised on the floor was withdrawn once the entry was reread. No follow-up was requested.

- 2026-05-23: The controls team recorded a routine observation. The count sat a little above the running mean, entirely from estimated inputs. Closed with no parameter change.

- 2026-05-20: The exceptions queue owner raised and closed a routine observation. A duplicate order was cancelled at source and never reached the run.

- 2026-05-19: A reviewer on shift noted a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-05-03: The duty analyst carried forward a routine observation. A question raised on the floor was withdrawn once the entry was reread. The desk confirmed no downstream impact.

- 2026-05-21: An on-call engineer noted a routine observation. A question raised on the floor was withdrawn once the entry was reread. The desk confirmed no downstream impact.

- 2026-05-20: The exceptions queue owner raised and closed a routine observation. A question raised on the floor was withdrawn once the entry was reread.

- 2026-05-14: The exceptions queue owner raised and closed a routine observation. One record appeared twice in the export after a mid-cycle correction. Nothing here bears on engine behaviour.

- 2026-05-16: A reviewer on shift carried forward a routine observation. A question raised on the floor was withdrawn once the entry was reread. The desk confirmed no downstream impact.

- 2026-05-04: The reconciliation desk carried forward a routine observation. Late inputs arrived from one feed and were loaded before the cut.

- 2026-05-21: The exceptions queue owner carried forward a routine observation. A question raised on the floor was withdrawn once the entry was reread.

- 2026-06-09: An on-call engineer signed off a routine observation. Dashboard tiles lagged the refresh; traced to cache staleness rather than the engine. No follow-up was requested.

> **Governance decision (2026-06-03 - #BAS-8210)** Priya: Operating policy baseline, read from /app/data/operating_policy.json at that fixed absolute path. Any field the policy file omits keeps its baseline: horizon_days = 180; curtail_below_year = 1960; flood_release_fraction_pct = 35; max_curtailments = 2400.

- 2026-06-13: An on-call engineer raised and closed a routine observation. The downstream vendor confirmed receipt inside the agreed window.

- 2026-06-08: The audit lead filed a routine observation. A query about a prior-period entry was answered from the published schedule. Referred to the dated decisions and closed.

- 2026-06-25: The exceptions queue owner recorded a routine observation. A query about a prior-period entry was answered from the published schedule. Nothing here bears on engine behaviour.

- 2026-06-09: The audit lead filed a routine observation. The downstream vendor confirmed receipt inside the agreed window.

- 2026-06-07: A weekly review raised and closed a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-06-13: An on-call engineer raised and closed a routine observation. Storage on the staging host was extended after the export outgrew its allocation. The thread was archived after review.

- 2026-06-19: The operations desk spot-checked a routine observation. The count sat a little above the running mean, entirely from estimated inputs. Closed with no parameter change.

- 2026-06-25: The controls team raised and closed a routine observation. A batch retried once after a transient timeout and completed on the second pass.

- 2026-06-07: An on-call engineer reviewed a routine observation. Two accounts showed a same-day transfer the export had not yet picked up. Referred to the dated decisions and closed.

- 2026-06-25: A reviewer on shift logged a routine observation. Storage on the staging host was extended after the export outgrew its allocation. The thread was archived after review.

- 2026-06-10: The duty analyst spot-checked a routine observation. The count sat a little above the running mean, entirely from estimated inputs. No follow-up was requested.

- 2026-06-26: The platform team spot-checked a routine observation. A question raised on the floor was withdrawn once the entry was reread. Filed for the record.

- 2026-06-24: The operations desk raised and closed a routine observation. Storage on the staging host was extended after the export outgrew its allocation. No action was carried forward.

- 2026-06-11: A shift handover spot-checked a routine observation. Late inputs arrived from one feed and were loaded before the cut. Nothing here bears on engine behaviour.

- 2026-06-27: The exceptions queue owner carried forward a routine observation. A typo in a reference record was corrected before the run started. No follow-up was requested.

- 2026-06-20: The reconciliation desk opened a query on a routine observation. The downstream vendor confirmed receipt inside the agreed window. Referred to the dated decisions and closed.

- 2026-06-05: The exceptions queue owner spot-checked a routine observation. One record appeared twice in the export after a mid-cycle correction. Referred to the dated decisions and closed.

- 2026-06-07: A stand-up note opened a query on a routine observation. The count sat a little above the running mean, entirely from estimated inputs. Closed with no parameter change.

- 2026-06-03: The exceptions queue owner filed a routine observation. An operator asked whether a credit had posted; it had, in the preceding period. Nothing here bears on engine behaviour.

- 2026-06-02: A stand-up note filed a routine observation. Late inputs arrived from one feed and were loaded before the cut.

- 2026-06-09: The audit lead reviewed a routine observation. Two accounts showed a same-day transfer the export had not yet picked up.

- 2026-06-04: The platform team signed off a routine observation. A typo in a reference record was corrected before the run started.

- 2026-06-24: A reviewer on shift spot-checked a routine observation. Storage on the staging host was extended after the export outgrew its allocation. Filed for the record.

- 2026-06-01: The reconciliation desk logged a routine observation. A duplicate order was cancelled at source and never reached the run.
