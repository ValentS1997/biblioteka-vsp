# Шпаргалка: Chapter 19 — OT Incident Response

## Core rule

```text
Do not optimize only for cyber containment.
Optimize for:
safety + process stability + visibility + threat reduction
```

## IT vs OT

| IT | OT |
|---|---|
| isolate fast | validate operational impact first |
| reboot/reimage common | reboot may be unsafe |
| endpoint telemetry rich | many assets have no agents |
| digital impact | physical/safety impact |
| IT team can act alone | engineering/operations required |

## OT response gate

Before disruptive action ask:
- what process does this asset support?
- will operator visibility be lost?
- can safety/protective functions be affected?
- is threat active?
- can attacker reach control layer?
- is engineering approval required?

## Asset classes

Embedded:
- PLC;
- RTU;
- DCS;
- relay;
- VFD;
- SIS.

OS-based:
- HMI;
- engineering workstation;
- historian;
- supervisory server.

## Scope question

```text
did attacker activity reach
systems capable of influencing
control logic / safety / process?
```

## Best evidence in OT

- network traffic;
- industrial protocol analysis;
- firewall logs;
- flow logs;
- HMI/SCADA/historian;
- engineering workstation;
- controller logic;
- project repositories;
- operator observations.

## Containment

Prefer:
- selective restrictions;
- engineering coordination;
- preserve operator visibility;
- preserve protective functions.

Avoid blind:
- full isolation;
- reboot;
- rebuild;
- automated blocking.

## Island mode

```text
disconnect external paths
→ continue local/manual operations
→ investigate safely
→ restore deliberately
```

Must be pre-planned and exercised.

## Recovery acceptance

- trusted controller logic;
- validated firmware/config;
- HMI visibility restored;
- historian/supervisory comms restored;
- protective systems validated;
- physical walkthrough complete;
- controlled startup complete.

## Five critical controls

1. OT-specific IR
2. Defensible architecture
3. OT network visibility
4. Secure remote access
5. Risk-based vulnerability management

## Main takeaway

```text
safe process control
comes before
fast cyber action
```
