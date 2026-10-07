# Source findings — глава 12

Canonical source: PDF pp. 324–349, SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`. Policy: `rag_only`.

## F-01 — [Historical/current-state caveat] OWASP Top 10 is explicitly 2021

- `p0325:c01`–`p0326:c01` use OWASP Top 10:2021 categories.
- This is source-correct for the book but not silently treated as a future/current standards snapshot.
- Current OWASP guidance after the book date: **[Needs confirmation]** unless externally verified.

## F-02 — [Source/version mismatch] Legacy CRS tag vs OWASP 2021 category

- `p0326:c01` identifies Injection as `A03:2021`.
- `p0335:c01` shows ModSecurity CRS `3.2.0` rule metadata containing `OWASP_TOP_10/A1`.
- This is consistent with historical/legacy rule tagging rather than a single normalized taxonomy.
- Disposition: preserve both source facts; do not rewrite the rule tag to A03.

## F-03 — [High-risk boundary] Injection examples

- pp. 328–333 contain directly adaptable XSS, SQL injection, command-injection and traversal techniques.
- These can enable data access, code execution or unauthorized file access.
- Artifact policy: retain mechanism/mitigation/evidence only; no runnable payload sequence is reproduced.

## F-04 — [Historical attack data] Smurf / amplification / SlowHTTP

- `p0336:c01` explicitly says the cited Smurf-amplifier registry stopped checking in 2017.
- pp. 337–339 include historical amplification/DDoS and SlowHTTP tool examples.
- These are source-era demonstrations, not current capacity/tool-status facts.

## F-05 — [Interpretation caveat] Crash or mitigation presence ≠ fixed bug

- pp. 340–344 discuss buffer overflow, ASLR, stack canaries and non-executable memory.
- ASLR/canaries/NX can reduce exploitability but do not remove the underlying memory-safety defect.
- Likewise, application crash behavior alone does not prove arbitrary-code execution.

## F-06 — [High-risk boundary] Heap spraying / shellcode

- pp. 342–344 discuss heap spraying and injected shellcode concepts.
- These concepts can directly support exploit development.
- They are retained only at conceptual/defensive level.

## F-07 — [High-risk boundary] Lateral movement / credential access

- pp. 344–346 describe lateral movement, further reconnaissance and credential gathering after compromise.
- These operations can expand unauthorized access across systems.
- No runnable lateral-movement or credential-reuse workflow is reproduced.

## F-08 — [Architecture terminology] Defense-in-depth, defense-in-breadth, defensible network architecture

- pp. 346–349 use source-specific framing around “глубокоэшелонированная”, “широкая” and “защищаемая/защищенная” network architecture.
- Artifacts preserve the source terminology and do not silently relabel it as Zero Trust or another external framework.

## F-09 — [Broad source claim] DMZ usefulness and cloud outsourcing

- `p0347:c01` says DMZ design becomes less useful as internet services move to cloud providers.
- Applicability depends on architecture, trust boundaries and control plane; the chapter does not prove this as a universal rule.
- Disposition: preserve as source commentary, not a general infrastructure law.

## F-10 — [Strategic assumption] “Systems will be compromised”

- `p0348:c01` uses compromise as a design assumption to motivate visibility and containment.
- This is best interpreted as a resilience/architecture assumption, not a claim that every specific system is inevitably compromised.

## Defensive takeaway

Secure coding/root-cause remediation, tested WAF rules, memory-safety mitigations, segmentation, centralized telemetry/SIEM and endpoint/network containment are complementary controls. None should be treated as a standalone guarantee.
