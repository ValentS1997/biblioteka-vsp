# Commands and tools — глава 10 (defensive classification)

Source: PDF pp. 274–297. No phishing campaign, credential collection, rogue AP or payload operation was executed.

## Safe / defensive operations

В source мало CLI, пригодного для безопасного operational runbook: основная тема — люди, доверие и campaign tooling.

Safe analysis activities derived from the chapter:
- inspect the **actual destination** of a link before opening it;
- compare sender/display identity with the real address/domain;
- inspect attachment type and business context;
- verify a request using a known independent helpdesk/manager contact;
- review a reported message or webpage artifact without interacting with untrusted content where possible.

## Workload-generating but not inherently malicious

Source discusses website mirroring utilities in the context of site cloning. Recursive mirroring can create significant HTTP workload and, in a phishing context, can facilitate impersonation. Exact mirror commands from the source are therefore **not reproduced as a ready campaign step**. Use website-copy tools only for explicitly authorized archival/testing purposes.

## High-risk source material — intentionally not operationalized

Section 10.2 includes:
- phishing campaign management;
- cloned login/web pages;
- credential-collection flows;
- rogue/imitated wireless access points;
- wireless social-engineering automation;
- Social-Engineer Toolkit payload/campaign menus;
- malicious file-format/payload delivery.

These can facilitate phishing, credential theft, malware delivery or unauthorized network interception. Artifact policy: preserve tool names/concepts/provenance and defensive implications, but do not reproduce runnable campaign/payload sequences.

## Effects / risks / verification

**Risks:** identity deception, credential compromise, malware execution, privacy exposure, unauthorized email/SMS traffic, rogue AP interception, reputational/legal impact.  
**Verification:** approved campaign charter, target list, legal/HR approval, safe landing page/data handling, stop conditions and deconfliction — **[Needs confirmation]**.  
**Rollback:** revoke campaign infrastructure, remove test artifacts/accounts/APs, rotate any intentionally exposed test secrets — exact procedure **[Needs confirmation]**.
