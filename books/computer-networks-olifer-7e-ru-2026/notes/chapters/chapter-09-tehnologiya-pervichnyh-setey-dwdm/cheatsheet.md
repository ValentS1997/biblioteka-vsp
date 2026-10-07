# Cheatsheet — глава 9: технология первичных сетей DWDM

## Symptom / problem framing

**Проблема:** optical path может быть физически целым, но spectral channel недоступен или деградирован из-за неверного wavelength/grid assignment, excessive loss, dispersion, amplifier chain, OADM/ROADM mapping or wavelength collision. DWDM troubleshooting начинается с optical channel/resource state, а не с packet forwarding. `p0268:c01`–`p0281:c01`.

## Baseline / context

| Сущность | Source role | RAG |
| --- | --- | --- |
| Spectral channel / wavelength | Independent optical channel in shared fiber | `p0268:c01`–`p0270:c01` |
| Fixed/flexible frequency plan | Defines spectral slot center/width | `p0271:c01`–`p0272:c01` |
| Transponder | Client optics ↔ DWDM wavelength; O-E-O | `p0273:c01` |
| Optical M/D | Combine/split wavelengths | `p0273:c01`–`p0275:c01` |
| OADM | Fixed add/drop of configured wavelength | `p0275:c01`–`p0276:c01` |
| EDFA / Raman amplifier | Optical-domain power amplification | `p0276:c01` |
| Dispersion compensation | Reduce chromatic/PMD impact | `p0277:c01` |
| OXC | Cross-connect spectral channels in mesh | `p0277:c01`–`p0278:c01` |
| ROADM | Remotely reconfigurable optical cross-connect | `p0278:c01`–`p0281:c01` |
| WSS | Select/switch wavelengths according to table | `p0279:c01`–`p0280:c01` |

## Read-only checks

1. Какой exact spectral channel/wavelength должен существовать end-to-end? **[Needs confirmation]**.
2. Grid fixed или flexible? Slot center/width and non-overlap verified?
3. Client signal terminates on which transponder and which wavelength does it generate?
4. Path topology: T-MUX → OADM → amplifier/compensator → OXC/ROADM → destination?
5. Does the same wavelength already occupy the target spectral resource? OADM/WSS cannot create a forbidden same-output collision.
6. Optical power before/after each amplifier/section and receiver threshold: **[Needs confirmation]**.
7. Which amplifier type and gain band apply? Source examples are not universal device specifications.
8. Dispersion compensation is optical-module based or handled by coherent receiver/DSP?
9. ROADM route: ingress direction + wavelength → egress direction/client bank.
10. Is device merely reconfigurable, or also colorless and directionless?
11. Actual alarms, OSNR, BER/FEC and optical power counters: **[Needs confirmation]** because chapter provides no production system state.

## Interpretation

- **Wavelength is an address-like transport resource, not a packet address.** It identifies a spectral channel provisioned through the optical path. `p0268:c01`–`p0270:c01`.
- **A narrower grid is not automatically “better”.** More channels fit, but spectral overlap/tolerance becomes harder and can require more advanced modulation/equipment. `p0271:c01`–`p0272:c01`.
- **Transponder conversion and optical switching are different domains.** The client/wavelength conversion may be O-E-O, while optical mux/demux/amplification/switching can remain all-optical. `p0270:c01`, `p0273:c01`.
- **Amplifier does not reset the digital signal.** It boosts optical signal power; regeneration is a different function. `p0276:c01`.
- **OADM is physically wavelength-specific in the described basic architecture.** Changing add/drop channel may require module/patching changes. `p0275:c01`–`p0276:c01`.
- **ROADM exists to remove much of that manual reconfiguration.** Its value is remote switching-table changes over more dynamic optical topologies. `p0278:c01`.
- **WSS performs selection, not arbitrary duplication.** The same wavelength from different inputs cannot simultaneously occupy one output spectral slot. `p0280:c01`.
- **Colorless/directionless describes flexibility beyond the ROADM label itself.** Older/basic ROADM can remain wavelength/port or direction constrained. `p0281:c01`.

## Next action

Для optical transport troubleshooting использовать порядок:

**identify client/transponder → identify wavelength + grid slot → trace optical path → verify add/drop/switch table → verify amplifier/power chain → assess dispersion/receiver state → validate destination transponder/client → re-check end-to-end spectral continuity**.

Exact commands, alarm names, optical budgets and thresholds are vendor/system specific.

## Modifying action

**[Not applicable].** Глава не содержит executable configuration commands. Repatching an OADM, changing ROADM/WSS mapping, frequency slot or amplifier configuration are state-changing operations requiring platform-specific precheck/rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- объяснить spectral channel vs colloquial “wavelength”;
- explain why DWDM is a form of FDM;
- distinguish fixed and flexible grids;
- explain T-MUX/transponder/mux-demux roles;
- distinguish OADM vs OXC/ROADM;
- distinguish amplifier vs regenerator;
- explain why dispersion still matters;
- describe WSS switching logic;
- explain reconfigurable vs colorless/directionless;
- trace a client signal through transponder → mux → optical path → ROADM/WSS → demux → destination.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для production optical changes rollback must restore prior wavelength/slot mapping, WSS/ROADM cross-connect and physical patching; exact procedure: **[Needs confirmation]**.
