# Cheatsheet — глава 8: технология первичных сетей OTN

## Symptom / problem framing

**Проблема:** transport network может не иметь packet loss/queueing symptoms в привычном смысле, но circuit не поднимется или будет transport-degraded, если неправильно provisioned path, slot mapping, client mapping, synchronization/alignment или FEC/optical transport state. `p0242:c01`–`p0267:c01`.

## Baseline / context

| Уровень / сущность | Source role | RAG |
| --- | --- | --- |
| Primary/transport network | Static point-to-point channels for overlay clients | `p0242:c01`–`p0243:c01` |
| TM / ADM / DXC | Terminate, add/drop, cross-connect channels | `p0244:c01`–`p0246:c01` |
| OPU | Map/align client payload | `p0256:c01`–`p0260:c01` |
| ODU | End-to-end transport/monitoring + multiplexing | `p0256:c01`–`p0263:c01` |
| OTU | Adjacent OTN nodes + FEC + photonic handoff | `p0256:c01`–`p0258:c01` |
| GFP-F / GFP-T | Generic client framing for asynchronous/frame or transparent synchronous traffic | `p0259:c01`–`p0260:c01` |
| Tributary Slot / PSI | Multiplexing placement and payload-structure description | `p0261:c01`–`p0263:c01` |
| ODUFlex / GMP | Arbitrary-rate client mapping | `p0265:c01` |
| Transponder / muxponder / cross-connect | OTN/DWDM evolution from point-to-point wrapper to switching fabric | `p0265:c01`–`p0267:c01` |

## Read-only checks

1. Это packet network symptom или **transport circuit** symptom?
2. Какой client signal: SDH, Ethernet, Fibre Channel, other? Exact client type/rate: **[Needs confirmation]**.
3. Какой OTN container/block: OPUk / ODUk / OTUk / ODUFlex / ODUCn?
4. Client mapping synchronous or asynchronous? GFP-F/GFP-T or another source-described mapping?
5. Какой tributary slot map и PSI association between slot, ODU level and tributary port?
6. Circuit path проходит через TM/ADM/DXC/OTN switch? Какие segments/regenerators/DWDM channels участвуют?
7. Есть ли free capacity on every aggregate segment? В OTN lack of provisioned capacity can block the circuit entirely.
8. FEC state/error counters and OTU section condition: **[Needs confirmation]** on real equipment.
9. Is frame/rate model interpreted correctly: **fixed OTN frame size, variable transmission time** by hierarchy level?
10. Underlying photonic/DWDM wavelength/channel state: **[Needs confirmation]**.

## Interpretation

- **OTN is provisioned, not routed per packet.** Absence of routing protocols is a feature of the source model, not a missing configuration. `p0246:c01`–`p0247:c01`.
- **Unused time slots are normal reserved capacity.** Static transport can carry “empty” slots by design. `p0247:c01`.
- **An OTN frame is not an Ethernet/IP frame.** It is a repeating transport structure carrying mapped client data and overhead. `p0248:c01`–`p0250:c01`.
- **OPU/ODU/OTU are not interchangeable labels.** OPU solves client adaptation, ODU end-to-end transport/multiplexing, OTU section transport/FEC. `p0256:c01`–`p0258:c01`.
- **Rate alignment matters even when client protocol is valid.** Burstiness or small clock differences must be absorbed by mapping/alignment procedures. `p0259:c01`–`p0260:c01`.
- **GFP makes client handling protocol-neutral at the OTN transport layer.** It is an envelope, not the user application protocol itself. `p0260:c01`.
- **Tributary slots are multiplexing resources, not physical ports.** PSI explicitly maps TS → ODU type → tributary-port ownership. `p0262:c01`–`p0263:c01`.
- **OTN switching appears only in later architecture.** Early transponder/muxponder OTN still provided point-to-point channels without OTN-native transit switching. `p0265:c01`–`p0267:c01`.

## Next action

Для transport troubleshooting использовать порядок:

**identify client signal/rate → identify OPU/ODU/OTU mapping → verify slot/PSI provisioning → trace provisioned circuit across OTN nodes → check OTU/FEC section state → check underlying DWDM path → verify client receive rate/data integrity end-to-end**.

Это source-grounded sequence. Exact vendor commands, alarms, thresholds and provisioning workflow require platform documentation.

## Modifying action

**[Not applicable].** Глава описывает provisioning tables, multiplexing, mapping and cross-connect functions, но не приводит executable CLI/configuration syntax.

Изменения circuit/slot/cross-connect/FEC/DWDM mapping требуют before-state capture, maintenance plan and rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- объяснить primary/transport network vs overlay packet network;
- различить TM / ADM / DXC / regenerator;
- объяснить static load and capacity planning;
- различить PDH bit stuffing and SDH pointer mechanism;
- объяснить OPU / ODU / OTU roles;
- объяснить fixed-size OTN frame vs SDH fixed-period frame;
- объяснить purpose of FEC in OTU;
- различить synchronous/asynchronous client mapping and GFP-F/GFP-T;
- объяснить tributary slots + PSI;
- объяснить why ODU0/ODU2e/ODU4/ODUCn/ODUFlex appeared;
- описать evolution transponder → muxponder → OTN switching.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для production transport changes rollback должен восстанавливать предыдущие circuit mappings, tributary-slot allocation and cross-connect state; конкретная процедура: **[Needs confirmation]**.
