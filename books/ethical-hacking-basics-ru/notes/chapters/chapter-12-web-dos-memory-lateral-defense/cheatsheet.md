# Cheatsheet — глава 12: web / availability / memory / lateral defense

## Symptom / problem framing

Нужно понять, **где untrusted input or post-compromise access crosses a trust boundary without sufficient validation/control**, и как подтвердить риск с минимальным impact. Source связывает application flaws, memory corruption and lateral movement with the need for layered detection/containment.

## Baseline / context

| Область | Source framing |
| --- | --- |
| Web input | validation, encoding, parameterization and access-control assumptions |
| OWASP | Top 10 2021 categories |
| WAF | additional HTTP inspection/rule layer, not replacement for secure code |
| Availability | amplification/distributed/slow-request exhaustion |
| Memory | stack/heap, ASLR, stack canary, non-executable memory |
| Lateral movement | recon + credentials + access to additional systems |
| Architecture | segmentation, DMZ, honeypot, SIEM, endpoint isolation |

## Read-only checks

1. What exact application/endpoint/function is authorized for testing? [Needs confirmation].
2. Is there a non-production clone or staging environment?
3. Are expected input formats and access-control rules documented?
4. What baseline latency/error rate/service capacity exists before availability testing? [Needs confirmation].
5. Are memory protections/build flags known from build metadata rather than guessed from behavior?
6. What identity/credential handling is permitted during post-compromise validation? [Needs confirmation].
7. Are logs, SIEM and endpoint telemetry available to correlate tests?

## Interpretation

- A changed response to unusual input is a **signal**, not automatic exploit proof.
- WAF detection/blocking does not prove the underlying application is fixed.
- A DoS tool producing load is not a valid production test without rate/impact constraints.
- Crash ≠ arbitrary code execution.
- ASLR/canaries/NX reduce exploitability; their presence does not prove absence of memory bugs.
- Network segmentation without enforcement/identity controls may not stop lateral movement.
- Detection and containment remain necessary even with preventive controls.

## Next action

For legitimate assessment: **define trust boundary → use least-invasive validation → collect application/log evidence → remediate root cause → verify controls → correlate with monitoring**. Move to load, exploitation or lateral-movement validation only under separate explicit scope.

## Modifying action

DoS/load generation, exploit execution, memory corruption and credential/lateral-movement tests can change service/security state and are not operationalized here. WAF/firewall/segmentation changes are production modifications and require environment-specific change/rollback plans.

## Verification / acceptance checks

- Input validation/access control verified at the application boundary.
- WAF findings are correlated with app behavior/logs.
- Availability baseline remains within approved limits.
- Memory-safety mitigations verified from build/runtime evidence where available.
- Segmentation/control points actually enforce intended paths.
- SIEM/EDR/logging can observe the tested behavior.
- Actual environment/test output: **[Needs confirmation]**.

## Rollback

Application/WAF/network changes require versioned config and tested rollback. DoS/exploit side effects cannot be universally “undone”; recovery path, service restart/failover, snapshot/redeploy and owner escalation are **[Needs confirmation]**.
