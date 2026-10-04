---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 12
translated_chapter: "chapter-12-contain-activity.md"
canonical_rag_boundary:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0244:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0299:c01"
source_pdf_page_range: "244-299"
qa_status: "ACCEPTED"
qa_contract: "DYNAMIC-IR-RU-TRANSLATION-QA v1.0"
---

# QA — Chapter 12

## Boundary and completeness

- PASS — Chapter 12 begins at PDF page 244 / chunk `p0244:c01`.
- PASS — Chapter 12 ends at PDF page 299 / chunk `p0299:c01`.
- PASS — PDF page 300 / chunk `p0300:c01` begins Chapter 13 (`Eradicate Activity`) and is excluded.
- PASS — Figures 74–90 represented as captions/references.
- PASS — Listings 48–61 represented.
- PASS — Tables 16–25 represented.
- PASS — standalone DoH curl example represented.
- PASS — Contain: Step-by-Step represented with all eight steps.
- PASS — references [1]–[5] represented.

## Semantic fidelity

- PASS — containment dual objective preserved: stop attacker activity while preserving evidence.
- PASS — passive, active, adaptive, and deceptive containment strategies preserved with their trade-offs.
- PASS — timing/coordination logic preserved, including immediate containment triggers and simultaneous isolation rationale.
- PASS — Stryker/Intune case preserved as a remote-management-plane containment lesson.
- PASS — technical containment layers preserved:
  - network;
  - host;
  - application;
  - identity/access.
- PASS — DNS sinkhole and DoH limitations preserved.
- PASS — AI-agent/MCP containment considerations preserved.
- PASS — identity containment sequence preserved:
  - credential revocation;
  - session termination;
  - refresh/persistent token revocation;
  - conditional access;
  - SSO/MFA coordination.
- PASS — back-channel logout / authorization-sprawl discussion preserved.
- PASS — evidence collection model preserved, including DAIR's all-activities-as-data-collection principle and isolate-vs-collect trade-off.
- PASS — cloud shared-responsibility/security-demarcation discussion preserved.
- PASS — cloud identity-first containment, network isolation, resource tagging, termination protection, SaaS and serverless containment preserved.
- PASS — multi-cloud coordination, encrypted communications, remote-worker/BYOD/home-network containment preserved.
- PASS — BEC, supply-chain/MOVEit, and partner-ecosystem containment models preserved.
- PASS — containment validation channels preserved: network, process, log analysis.
- PASS — multi-tenant Kubernetes/AWS case preserved.
- PASS — ransomware rapid-response case preserved, including sub-10-minute coordinated EDR + identity containment.
- PASS — all eight containment Step-by-Step actions preserved.

## Technical integrity

- PASS — Listings 48–51 preserve RDP/SSH/SIEM session-management commands.
- PASS — Listing 52 preserves Get-NetTCPConnection output.
- PASS — Listings 53–57 preserve cloud protection, OAuth enumeration, Azure quarantine, Lambda deny-and-log code/deployment.
- PASS — Listings 58–61 preserve AWS/Kubernetes containment commands.
- PASS — Tables 16–25 preserve strategy, regulatory, token, tagging, multi-cloud, remote-worker, validation, and action-summary mappings.
- PASS — identifiers preserved where present: EDR, RDP, SSH, RMM, OAuth, SAML, JWT, IdP, SSO, MFA, FIDO2, TOTP, WAF, MCP, IAM, IaaS, PaaS, SaaS, VPC, NSG, EBS, CI/CD, BEC, BYOD, MDM, MAM, NDR, C2, KRBTGT, HIPAA, PCI DSS, GDPR, NIS2, DORA, CRA, PSD2.
- PASS — source commands, IP addresses, object/resource IDs, filenames, timestamps, account identifiers, and technical literals retained where relevant.

## Glossary consistency

- PASS — `passive containment` locked as `пассивное сдерживание`.
- PASS — `active containment` locked as `активное сдерживание`.
- PASS — `adaptive containment` locked as `адаптивное сдерживание`.
- PASS — `deceptive containment` locked as `обманное сдерживание`.
- PASS — `cloud security demarcation` locked.
- PASS — `identity-first containment` locked.
- PASS — `termination protection` locked.
- PASS — `containment validation` locked.

Glossary commit:
`61e45db934dc94e665c96d4fcd00de95f4b5684e`

## Licensing / fail-closed handling

- PASS — unofficial translation/adaptation notice present.
- PASS — Figures 74–90 are not reproduced; captions/cross-references retained.
- PASS — third-party/product screenshots and Stryker facility notice remain fail-closed.
- PASS — external references are cited without reproducing protected third-party prose.
- PASS — source-authored technical examples/listings are retained under the translation workflow.

## Result

`ACCEPTED`
