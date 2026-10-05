# Translation / editorial findings — Chapter 18

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0584:c01`–`p0612:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-18-incident-response-for-cloud-systems.md`.

## Итог проверки

- Semantic coverage: strong.
- Listings 141–151 preserved.
- Tables 55–56 preserved.
- Figures 185–192 represented.
- Main debt: dense hybrid cloud terminology and inconsistent RU/EN heading style.

## High-priority heading cleanup

Representative examples:

- `Cloud-Native Detection Tooling`
- `Detection Tooling for AWS`
- `Detection Tooling for Azure`
- `Detection Tooling for Google Cloud`
- `Cloud-Specific Debrief Questions`
- `Identity and Access`
- `Remediation Storage Account и Bucket`
- `Identity and Access Management`
- `Compute и Workloads`
- `Automated Response Capabilities`
- `Cloud Infrastructure for Forensic Workstations`
- `Secure, Read-Only Log Storage`
- `Network Logging with VPC Flow Logs`
- `Containers and Serverless for Forensic Tooling`
- `Multi-Cloud Environments`
- `AI-driven SOC operations`
- `Runtime visibility для Serverless и Containers`
- `Token-based attacks`
- `Cloud-native forensics`

## Canonical terminology proposal

- Cloud Incident Response → реагирование на инциденты в облачной среде
- Control Plane → плоскость управления (control plane)
- Data Plane → плоскость данных (data plane)
- Cloud-Native Detection → встроенные облачные средства обнаружения
- Resource Group → группа ресурсов
- Subscription → подписка
- Project → проект
- Effective Permissions → эффективные разрешения
- Service Principal → сервисный принципал / service principal
- Session Token → токен сессии
- Access Key → ключ доступа
- Cloud Persistence → закрепление в облачной среде
- Resource Isolation → изоляция ресурса
- Forensic Workstation → форензик-станция
- Immutable Storage → неизменяемое хранилище
- Runtime Visibility → наблюдаемость времени выполнения
- Multi-Cloud Visibility → сквозная видимость multi-cloud среды

Acronyms/proper names (AWS, Azure, GCP, GuardDuty, Defender for Cloud, Security Command Center, NSG, VPC, ECS, Lambda, Velociraptor, CSPM) should remain.

## Structural findings

1. Identity/permissions should visually precede resource investigation.
2. Control plane vs data plane needs a dedicated comparison callout.
3. Four common cloud IR mistakes deserve a high-visibility sidebar.
4. Read-only enumeration must be visually separated from state-changing isolation/remediation.
5. Listings 141–151 need monospace/A4 QA.
6. Tables 55–56 require A4 QA.
7. AWS/Azure/GCP examples should use a consistent visual pattern.
8. Multi-region enumeration should be emphasized in both Scope and Eradicate.
9. Session/token revocation must remain distinct from credential rotation.
10. Serverless/container evidence limitations deserve a dedicated forensic callout.
11. Product/tool capability claims should retain source timing and not be silently updated.

## Visual debt

Figures 185–192.

Priority:
- Figure 185 — MEDIUM
- Figures 186–187 — HIGH
- Figures 188–190 — CRITICAL
- Figures 191–192 — HIGH

## Priority

`CRITICAL`

Reason: cloud incidents are identity-heavy, API-driven and often ephemeral. Incorrect assumptions can destroy evidence or leave active access behind.
