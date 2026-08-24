# Planning governance log

How the release scheduler is *meant* to behave -- the recovery of the truncated gauge series, what a
reading the basin office has marked suspect contributes, in what order the appropriations are
served, where the environmental minimum sits against them, how a flood release is sized and what
the curtailment record carries -- was settled incrementally by the basin board, and those decisions
live in the review entries below, not in any single summary. Several stages deliberately DEVIATE
from the intuitive reading: a suspect reading is carried as zero inflow rather than dropping its
day, the appropriations are served strictly by priority rather than prorated, the environmental
minimum is served ahead of every right rather than out of the remainder, and the flood release is
sized on the storage as it stands after the day's inflow. The February draft proposals were
revisited during the 2026-05 operations review and several were reversed; where a draft or interim
conflicts with a later decision, the later dated decision governs. `/app/docs/release_contract.json`
is the output contract only.


- 2026-02-20: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1009. Stage drift reviewed; no operating change requested.

- 2026-02-06: Watermaster on duty logged a routine observation for the telemetry relay during review window 1007. Stage drift reviewed; no operating change requested.

> **Recovery draft proposal (2026-02-06 - #BAS-8020)** Rosa: rebuild the truncated gauge series by concatenating the pre-migration snapshot with the telemetry journal and keeping the last row seen for each reading; a restored reading is re-read from the snapshot *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-13: Operations review of the canal headworks in window 1012 closed with no action; the standing thresholds were reconfirmed as they are.

> **Recovery draft proposal (2026-02-13 - #BAS-8026)** Anders: the sensor's datum offset is SUBTRACTED from the raw stage, the offset being the amount by which the family reads high *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-26: Basin engineer noted rejected telemetry frames from the canal headworks in window 1019. Raised with the district operator; the release parameters were not touched.

- 2026-02-10: Operations review of the snowpack model feed in window 1018 closed with no action; the standing thresholds were reconfirmed as they are.

> **Recovery draft proposal (2026-02-19 - #BAS-8032)** Marek: a reading the basin office has marked suspect is dropped, and the day it covers drops out of the schedule with it *(Superseded -- reversed in the 2026-05 operations review.)*

- 2026-02-26: Operations review of the canal headworks in window 1038 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-16: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1027. Stage drift reviewed; no operating change requested.

- 2026-02-06: Basin engineer noted rejected telemetry frames from the watermaster's accounting service in window 1030. Raised with the district operator; the release parameters were not touched.

- 2026-02-27: Watermaster on duty logged a routine observation for the telemetry relay during review window 1027. Stage drift reviewed; no operating change requested.

- 2026-02-19: Basin engineer noted rejected telemetry frames from the telemetry relay in window 1023. Raised with the district operator; the release parameters were not touched.

- 2026-02-01: Operations review of the watermaster's accounting service in window 1027 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-03: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1031. Stage drift reviewed; no operating change requested.

- 2026-02-05: Operations stand-up recorded a routine note against the snowpack model feed for window 1027. The diversion backlog was cleared with no order raised.

- 2026-02-21: Operations review of the telemetry relay in window 1025 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-02-25: Watermaster on duty logged a routine observation for the watermaster's accounting service during review window 1033. Stage drift reviewed; no operating change requested.

- 2026-02-02: Watermaster on duty logged a routine observation for the telemetry relay during review window 1039. Stage drift reviewed; no operating change requested.

- 2026-02-14: Watermaster on duty logged a routine observation for the canal headworks during review window 1031. Stage drift reviewed; no operating change requested.

- 2026-02-17: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1037. Stage drift reviewed; no operating change requested.

- 2026-02-24: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1036. Raised with the district operator; the release parameters were not touched.

> **Interim decision (2026-03-05 - #BAS-8038)** Priya: where the day cannot meet the appropriations in full, the shortage is prorated across every right on the reservoir in proportion to its entitlement *(Revised -- see the 2026-05 operations review.)*

- 2026-03-01: Basin engineer noted rejected telemetry frames from the watermaster's accounting service in window 1054. Raised with the district operator; the release parameters were not touched.

- 2026-03-24: Operations stand-up recorded a routine note against the watermaster's accounting service for window 1051. The diversion backlog was cleared with no order raised.

- 2026-03-10: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1048. Raised with the district operator; the release parameters were not touched.

- 2026-03-11: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1058. Raised with the district operator; the release parameters were not touched.

- 2026-03-09: Watermaster on duty logged a routine observation for the telemetry relay during review window 1044. Stage drift reviewed; no operating change requested.

- 2026-03-13: Watermaster on duty logged a routine observation for the watermaster's accounting service during review window 1053. Stage drift reviewed; no operating change requested.

- 2026-03-04: Operations review of the spillway gate controller in window 1057 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-17: Operations review of the spillway gate controller in window 1054 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-12: Operations review of the canal headworks in window 1049 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-09: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1052. Stage drift reviewed; no operating change requested.

- 2026-03-14: Basin engineer noted rejected telemetry frames from the watermaster's accounting service in window 1055. Raised with the district operator; the release parameters were not touched.

- 2026-03-15: Operations review of the snowpack model feed in window 1043 closed with no action; the standing thresholds were reconfirmed as they are.

> **Interim decision (2026-03-11 - #BAS-8044)** Anders: the environmental minimum is served out of whatever remains once the appropriations have been met, the rights having the senior claim on the outlet *(Revised -- see the 2026-05 operations review.)*

- 2026-03-21: Operations review of the watermaster's accounting service in window 1072 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-22: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1068. Stage drift reviewed; no operating change requested.

- 2026-03-23: Operations review of the watermaster's accounting service in window 1073 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-04: Operations review of the canal headworks in window 1077 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-06: Operations stand-up recorded a routine note against the watermaster's accounting service for window 1071. The diversion backlog was cleared with no order raised.

- 2026-03-13: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1063. Raised with the district operator; the release parameters were not touched.

- 2026-03-13: Watermaster on duty logged a routine observation for the spillway gate controller during review window 1060. Stage drift reviewed; no operating change requested.

- 2026-03-23: Operations stand-up recorded a routine note against the canal headworks for window 1068. The diversion backlog was cleared with no order raised.

- 2026-03-26: Operations stand-up recorded a routine note against the spillway gate controller for window 1076. The diversion backlog was cleared with no order raised.

- 2026-03-25: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1060. Raised with the district operator; the release parameters were not touched.

- 2026-03-19: Watermaster on duty logged a routine observation for the telemetry relay during review window 1072. Stage drift reviewed; no operating change requested.

- 2026-03-19: Operations review of the spillway gate controller in window 1074 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-03-18: Operations stand-up recorded a routine note against the canal headworks for window 1075. The diversion backlog was cleared with no order raised.

- 2026-03-20: Operations stand-up recorded a routine note against the watermaster's accounting service for window 1071. The diversion backlog was cleared with no order raised.

- 2026-04-17: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1097. Raised with the district operator; the release parameters were not touched.

- 2026-04-20: Operations stand-up recorded a routine note against the snowpack model feed for window 1085. The diversion backlog was cleared with no order raised.

- 2026-04-25: Watermaster on duty logged a routine observation for the canal headworks during review window 1115. Stage drift reviewed; no operating change requested.

- 2026-04-17: Operations review of the telemetry relay in window 1103 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-12: Operations stand-up recorded a routine note against the canal headworks for window 1113. The diversion backlog was cleared with no order raised.

- 2026-04-13: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1110. Raised with the district operator; the release parameters were not touched.

- 2026-04-18: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1097. Raised with the district operator; the release parameters were not touched.

- 2026-04-25: Operations stand-up recorded a routine note against the watermaster's accounting service for window 1115. The diversion backlog was cleared with no order raised.

- 2026-04-03: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1096. Stage drift reviewed; no operating change requested.

- 2026-04-09: Operations stand-up recorded a routine note against the snowpack model feed for window 1086. The diversion backlog was cleared with no order raised.

- 2026-04-23: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1106. Raised with the district operator; the release parameters were not touched.

- 2026-04-27: Operations review of the snowpack model feed in window 1120 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-06: Operations review of the telemetry relay in window 1107 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-04-10: Operations stand-up recorded a routine note against the telemetry relay for window 1089. The diversion backlog was cleared with no order raised.

- 2026-04-23: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1113. Raised with the district operator; the release parameters were not touched.

- 2026-04-03: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1116. Raised with the district operator; the release parameters were not touched.

- 2026-04-08: Operations stand-up recorded a routine note against the snowpack model feed for window 1119. The diversion backlog was cleared with no order raised.

- 2026-04-06: Operations stand-up recorded a routine note against the spillway gate controller for window 1120. The diversion backlog was cleared with no order raised.

- 2026-04-19: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1110. Stage drift reviewed; no operating change requested.

- 2026-04-09: Basin engineer noted rejected telemetry frames from the telemetry relay in window 1102. Raised with the district operator; the release parameters were not touched.

- 2026-04-02: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1109. Stage drift reviewed; no operating change requested.

- 2026-04-06: Basin engineer noted rejected telemetry frames from the telemetry relay in window 1106. Raised with the district operator; the release parameters were not touched.

- 2026-05-27: Operations review of the telemetry relay in window 1124 closed with no action; the standing thresholds were reconfirmed as they are.

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

- 2026-05-09: Operations stand-up recorded a routine note against the telemetry relay for window 1151. The diversion backlog was cleared with no order raised.

- 2026-05-07: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1150. Raised with the district operator; the release parameters were not touched.

- 2026-05-21: Operations stand-up recorded a routine note against the canal headworks for window 1140. The diversion backlog was cleared with no order raised.

- 2026-05-17: Operations review of the spillway gate controller in window 1130 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-17: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1142. Raised with the district operator; the release parameters were not touched.

- 2026-05-08: Basin engineer noted rejected telemetry frames from the watermaster's accounting service in window 1139. Raised with the district operator; the release parameters were not touched.

- 2026-05-23: Operations review of the telemetry relay in window 1136 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-14: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1145. Raised with the district operator; the release parameters were not touched.

- 2026-05-23: Operations review of the snowpack model feed in window 1135 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-20: Operations stand-up recorded a routine note against the canal headworks for window 1130. The diversion backlog was cleared with no order raised.

- 2026-05-19: Operations review of the spillway gate controller in window 1159 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-05-03: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1158. Raised with the district operator; the release parameters were not touched.

- 2026-05-21: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1136. Stage drift reviewed; no operating change requested.

- 2026-05-20: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1158. Raised with the district operator; the release parameters were not touched.

- 2026-05-14: Operations stand-up recorded a routine note against the snowpack model feed for window 1153. The diversion backlog was cleared with no order raised.

- 2026-05-16: Basin engineer noted rejected telemetry frames from the canal headworks in window 1130. Raised with the district operator; the release parameters were not touched.

- 2026-05-04: Basin engineer noted rejected telemetry frames from the spillway gate controller in window 1142. Raised with the district operator; the release parameters were not touched.

- 2026-05-21: Basin engineer noted rejected telemetry frames from the watermaster's accounting service in window 1129. Raised with the district operator; the release parameters were not touched.

- 2026-06-09: Basin engineer noted rejected telemetry frames from the telemetry relay in window 1164. Raised with the district operator; the release parameters were not touched.

> **Governance decision (2026-06-03 - #BAS-8210)** Priya: Operating policy baseline, read from /app/data/operating_policy.json at that fixed absolute path. Any field the policy file omits keeps its baseline: horizon_days = 180; curtail_below_year = 1960; flood_release_fraction_pct = 35; max_curtailments = 2400.

- 2026-06-13: Operations review of the spillway gate controller in window 1178 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-08: Watermaster on duty logged a routine observation for the telemetry relay during review window 1180. Stage drift reviewed; no operating change requested.

- 2026-06-25: Operations stand-up recorded a routine note against the watermaster's accounting service for window 1200. The diversion backlog was cleared with no order raised.

- 2026-06-09: Operations review of the spillway gate controller in window 1202 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-07: Basin engineer noted rejected telemetry frames from the snowpack model feed in window 1201. Raised with the district operator; the release parameters were not touched.

- 2026-06-13: Operations review of the telemetry relay in window 1173 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-19: Operations review of the spillway gate controller in window 1199 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-25: Operations stand-up recorded a routine note against the canal headworks for window 1190. The diversion backlog was cleared with no order raised.

- 2026-06-07: Operations review of the watermaster's accounting service in window 1203 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-25: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1177. Stage drift reviewed; no operating change requested.

- 2026-06-10: Operations review of the telemetry relay in window 1182 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-26: Operations review of the spillway gate controller in window 1187 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-24: Watermaster on duty logged a routine observation for the spillway gate controller during review window 1181. Stage drift reviewed; no operating change requested.

- 2026-06-11: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1167. Stage drift reviewed; no operating change requested.

- 2026-06-27: Operations review of the snowpack model feed in window 1170 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-20: Operations review of the telemetry relay in window 1199 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-05: Watermaster on duty logged a routine observation for the spillway gate controller during review window 1193. Stage drift reviewed; no operating change requested.

- 2026-06-07: Operations review of the watermaster's accounting service in window 1183 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-03: Operations review of the telemetry relay in window 1166 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-02: Operations review of the spillway gate controller in window 1179 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-09: Operations review of the snowpack model feed in window 1201 closed with no action; the standing thresholds were reconfirmed as they are.

- 2026-06-04: Basin engineer noted rejected telemetry frames from the telemetry relay in window 1175. Raised with the district operator; the release parameters were not touched.

- 2026-06-24: Operations stand-up recorded a routine note against the telemetry relay for window 1185. The diversion backlog was cleared with no order raised.

- 2026-06-01: Watermaster on duty logged a routine observation for the snowpack model feed during review window 1183. Stage drift reviewed; no operating change requested.
