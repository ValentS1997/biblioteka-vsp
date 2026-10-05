# Translation / editorial findings — Chapter 17

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0546:c01`–`p0583:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-17-incident-response-for-ransomware.md`.

## Итог проверки

- Semantic coverage: strong and extensive.
- Listing 140 preserved.
- Tables 50–54 preserved.
- Figures 178–184 represented.
- Main debt: very high English-heading density and mixed terminology across technical, legal, communications and recovery topics.

## High-priority heading cleanup

Representative examples:

- `RANSOMWARE INTRODUCTION`
- `Ransomware Attack Trends`
- `Initial Access Trends`
- `THE UNTRACEABLE CREDENTIAL PROBLEM`
- `Legitimate RMM as Attacker Infrastructure`
- `Initial Access Brokers`
- `Infrastructure Targets`
- `Attack Differentiation`
- `Human-Operated Ransomware (HumOR)`
- `Automated or Mass-Distributed Ransomware`
- `Encryptionless Extortion`
- `Pseudo-Ransomware and Wipers`
- `Multi-Vector Extortion Campaigns`
- `PREPARE`
- `Crisis Communications and Public Relations`
- `CTI for Ransomware`
- `Employee Training and Awareness`
- `Identity, Access, and Tier-0 Protection`
- `Ransomware-Resistant Backup Strategies`
- `The 3-2-1-1-0 Backup Rule`
- `VERIFY/TRIAGE`
- `Ransomware Verification Indicators`
- `The Incident Commander Role`
- `Framework for Ransomware Scoping`
- `Data Exfiltration Detection Strategies`
- `Decryption Possibilities`
- `Recovery Planning and Prioritization`
- `Decrypted Does Not Mean Clean`
- `Watching for Attacker Return`
- `Communication During Recovery`
- `Ransomware-Specific Debrief Questions`
- `Ransomware-Specific Metrics`
- `FINAL CONSIDERATIONS`
- `Recovery Is Not the End`
- `Prevention Remains Essential`

## Canonical terminology proposal

- Ransomware → программа-вымогатель / ransomware, first use
- Human-Operated Ransomware (HumOR) → управляемая человеком ransomware-атака (HumOR)
- RaaS → ransomware-as-a-service (RaaS)
- Encryptionless Extortion → вымогательство без шифрования
- Pseudo-Ransomware / Wiper → псевдо-вымогатель / вайпер
- Multi-Vector Extortion → многовекторное вымогательство
- Holding Statement → предварительное публичное заявление
- Tier-0 Protection → защита Tier 0
- Immutable Backup → неизменяемая резервная копия
- Air-Gapped Backup → изолированная/offline резервная копия
- Backup Survival Rate → доля уцелевших резервных копий
- Data Exfiltration Confidence → степень уверенности в оценке эксфильтрации
- Dwell Time → время присутствия атакующего
- Incident Commander → руководитель реагирования / Incident Commander, first use

Acronyms and proper names (EDR, NDR, SIEM, RTO, RPO, CTI, TTP, IOC, RMM, ESXi, Blackbaud, Kadokawa, LockBit) should remain.

## Structural findings

1. DAIR mapping is present but visually buried among long sections; v2 should make Prepare → Verify/Triage → Scope → Eradicate → Recover → Debrief explicit.
2. Ransomware type differentiation deserves a comparison table.
3. Backup architecture and 3-2-1-1-0 deserve a dedicated visual callout.
4. Decryption workflow should be separated from eradication to avoid implying decrypt = clean.
5. Incident Commander and responder-sustainability sections deserve distinct operational callouts.
6. Legal/regulatory and case-study sections must preserve source dates and framing; do not silently update.
7. Tables 50–54 require A4 QA.
8. Figure captions and long sidebars need visual hierarchy cleanup.
9. Payment-related language must keep source framing: payment buys a promise, not proof of deletion.
10. AI threat-development section is time-sensitive and should retain source timing rather than be silently refreshed.

## Visual debt

Figures 178–184.

Priority:
- Figure 178 — trend context: MEDIUM
- Figures 180–182 — RaaS/extortion structure: HIGH
- Figure 183 — ransom note victim identifier: HIGH
- Figure 184 — egress spike/exfiltration: HIGH

## Priority

`CRITICAL`

Reason: Chapter 17 combines high-impact response operations with business continuity, identity, backups, communications, legal/regulatory exposure and long-duration recovery. RU v2 must make those workstreams distinct but connected.
