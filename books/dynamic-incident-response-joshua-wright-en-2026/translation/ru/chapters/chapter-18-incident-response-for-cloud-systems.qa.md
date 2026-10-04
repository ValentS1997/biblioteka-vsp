---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 18
translated_chapter: "chapter-18-incident-response-for-cloud-systems.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0584:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0612:c01"
source_pdf_page_range: "584-612"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 18

## Boundary and completeness

- PASS — Chapter 18 begins at PDF page 584 / chunk `p0584:c01`.
- PASS — Chapter 18 ends at PDF page 612 / chunk `p0612:c01`.
- PASS — PDF page 613 / chunk `p0613:c01` begins Chapter 19 (`Incident Response for Operational Technology`) and is excluded.
- PASS — Figures 185–190 represented.
- PASS — Listings 141–151 represented.
- PASS — Tables 55–56 represented.
- PASS — references [1]–[9] preserved.
- PASS — cloud-specific source sections preserved: introduction, common attacks, Prepare, Detect, Response Actions, Debrief, Leveraging the Cloud for Incident Response, Final Considerations.

## Semantic fidelity

- PASS — initial-access discussion preserved across weak/absent credentials, misconfigurations, and API/UI compromise.
- PASS — attacker-impact discussion preserved across data theft/extortion, ransomware, cryptomining, and workload-to-management-plane escalation.
- PASS — logging guidance preserved across control-plane/data-plane distinction, lag time, retention time, SIEM centralization, and data-plane evidence gaps.
- PASS — permissions guidance preserved across global read-only access, dedicated forensic environments, JIT elevation, service-account automation, and break-glass access.
- PASS — provider-native detection coverage preserved for AWS GuardDuty, Microsoft Defender for Cloud, and Google Security Command Center.
- PASS — limitations of cloud-native detection preserved: known-pattern bias, control-plane focus, and lack of organizational context.
- PASS — billing anomaly detection pattern preserved.
- PASS — scoping preserved across compromised identities, inherited permissions, AWS policy evaluation, affected resources, metadata-service risk, connected environments, and token-based compromise.
- PASS — CircleCI session-token supply-chain case preserved.
- PASS — control-plane/data-plane forensic distinction preserved with regulatory/breach-assessment implications.
- PASS — VM isolation and storage/bucket remediation preserved across Azure, AWS, and Google Cloud.
- PASS — IAM, compute, container, serverless, and network persistence mechanisms preserved.
- PASS — active-session revocation requirement preserved in addition to credential rotation.
- PASS — common cloud-IR mistakes preserved, including snapshot-before-termination and all-region enumeration.
- PASS — automated GuardDuty/Lambda isolation-and-snapshot workflow preserved.
- PASS — cloud-specific debrief questions preserved across identity, resources, networking, and data exfiltration.
- PASS — cloud-forensics infrastructure preserved: on-demand workstations, immutable evidence storage, VPC flow logs, containers, serverless tooling, and Velociraptor on ECS.
- PASS — multi-cloud scoping and cross-cloud federation expansion preserved.
- PASS — evolution topics preserved: CSPM, AI-driven SOC operations, runtime visibility, token-based attacks, and cloud-native forensics.

## Technical integrity

- PASS — provider identifiers and product names preserved: AWS, Azure, Google Cloud, GuardDuty, Defender for Cloud, Security Command Center, Entra ID, CloudTrail, S3, ECS, Fargate, EFS, Object Lock, Terraform, Velociraptor.
- PASS — CLI commands preserved for Azure CLI, AWS CLI, gcloud, and gsutil.
- PASS — IAM/security terminology preserved: SecurityAudit, Security Reader, Security Reviewer, PIM, SCP, permission boundaries, OAuth consent grants, service-account keys.
- PASS — logging terminology preserved: SIEM, control plane, data plane, VPC flow logs, CloudTrail data events.
- PASS — WORM/immutability and 365-day Object Lock example preserved.
- PASS — references [1]–[9] retained without invented bibliography metadata.

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — third-party report quotations, charts, and screenshots are not reproduced beyond source-safe textual representation.
- PASS — canonical English RAG remains source of truth.

## Glossary consistency

- PASS — `control plane` → `плоскость управления`.
- PASS — `data plane` → `плоскость данных`.
- PASS — `shared responsibility model` → `модель совместной ответственности`.
- PASS — `break-glass account` → `аварийная учётная запись (break-glass)`.
- PASS — `session token` → `токен сессии`.
- PASS — `cloud-native detection` → `облачное нативное обнаружение`.
- PASS — `Object Lock` preserved.
- PASS — `Cloud Security Posture Management` → `Cloud Security Posture Management (CSPM)`.

Glossary commit:
`21a61a07d1adf211b126cd1cc6de0b1426696dee`

## Result

`ACCEPTED`
