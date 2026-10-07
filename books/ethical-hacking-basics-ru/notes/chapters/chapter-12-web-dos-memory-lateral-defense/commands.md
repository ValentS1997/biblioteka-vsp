# Commands and tools — глава 12 (defensive classification)

Source: PDF pp. 324–349. No injection exploit, DoS/load attack, memory exploit or lateral-movement action was executed.

## Safe / defensive operations

The chapter is dominated by attack examples, so only non-offensive operations are retained operationally:

- review application input schemas and validation logic;
- inspect web/application/security logs;
- review WAF/ModSecurity CRS rule matches and anomaly scores;
- inspect build/runtime metadata for memory protections;
- review network segmentation/firewall policy and SIEM/EDR visibility;
- reproduce suspicious requests only in an explicitly authorized non-production lab using benign validation strings.

## State-changing defensive controls

Source discusses:
- input validation and secure application design;
- WAF/ModSecurity/CRS;
- segmentation/firewalls/UTM/DMZ;
- logging/SIEM;
- endpoint isolation/containment.

These controls are environment-specific. Exact configuration changes are not copied as generic production commands because rollback, false-positive impact and application dependencies are unknown.

## High-risk source material — intentionally not operationalized

The source contains executable or directly adaptable examples for:
- XSS, SQL injection, command injection and path traversal;
- SlowHTTP/availability exhaustion and amplification concepts;
- buffer-overflow / heap-spraying / shellcode concepts;
- lateral movement and credential collection.

These can enable unauthorized code/data access, service disruption or movement across systems. Artifact policy: preserve concepts, detection signals and mitigations without a runnable attack recipe.

## Effects / risks / verification

**Risks:** data access/modification, application compromise, outage, credential exposure, lateral spread.  
**Verification:** approved target/staging environment, test identity/data, rate/impact ceiling, logging and recovery — **[Needs confirmation]**.  
**Rollback:** restore versioned app/WAF/network configuration or redeploy/recover affected service according to environment-specific plan — **[Needs confirmation]**.
