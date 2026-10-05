# Translation / editorial findings — Chapter 11

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0224:c01`–`p0243:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-11-scope-activity.md`.

## Итог проверки

- Semantic coverage: strong.
- Listings 41–47 preserved.
- Tables 14–15 preserved.
- Figures 69–73 represented.
- Main debt: English-heavy headings and hybrid terminology.

## High-priority heading cleanup

Current headings requiring normalization:

- `THE PURPOSE OF SCOPING`
- `INDICATORS OF COMPROMISE IN SCOPING`
- `Technical IOCs`
- `Behavioral IOCs`
- `SCOPING METHODOLOGIES`
- `Enterprise-Wide Hunting`
- `Progressive Scoping`
- `TIMELINE RECONSTRUCTION`
- `SCOPING CHALLENGES`
- `Visibility Gaps`
- `Cloud and Hybrid Environments`
- `Anti-Forensic Techniques`
- duplicate `Anti-Forensic Techniques` heading
- `Log Deletion and Modification`
- `Timestomping`
- `Encryption and Obfuscation`
- `Living off the Land`
- `Scale and Complexity`
- `Dynamic / Cloud Environments`
- `INTEGRATION WITH RESPONSE ACTIVITIES`
- `SCOPE ACTIVITY EXAMPLES`
- `The LinkedIn Attachment`
- `The Cloud Storage Exfiltration`
- `SCOPE: STEP-BY-STEP`

## Terminology normalization

Recommended canonical RU v2 terms:

- Scope / Scoping → Определение масштаба / определение границ инцидента
- IOC → индикатор компрометации (IOC)
- technical IOC → технический IOC
- behavioral IOC → поведенческий IOC
- enterprise-wide hunting → поиск по всей инфраструктуре
- progressive scoping → поэтапное расширение границ расследования
- timeline reconstruction → реконструкция временной шкалы атаки
- visibility gap → пробел видимости
- anti-forensics → антифорензика / противодействие расследованию
- timestomping → подмена временных меток
- living off the land → использование штатных средств системы
- environmental sweep → обследование всей среды
- lateral expansion → боковое расширение поиска
- critical asset prioritization → приоритизация критичных активов

## Structural findings

1. Duplicate `Anti-Forensic Techniques` heading appears in current translation; verify against source and remove duplicate in v2.
2. This chapter is best read as a process flow; v2 should visually emphasize IOC → search → timeline → handoff.
3. Table 14 and Table 15 need A4 QA because command cells are long.
4. Listings 42–47 need monospace QA.
5. LinkedIn Attachment and Cloud Exfiltration examples should be visually separated from core theory.

## Visual debt

Figures 69–73:

- Figure 69 — Scope Activity Waypoint
- Figure 70 — Sample Network Activity Timeline
- Figure 71 — Siemens S7-1200
- Figure 72 — Windows Event Log indicating deletion
- Figure 73 — Event Record ID field

Priority:
- Figure 69 — CRITICAL
- Figure 70 — HIGH
- Figures 72–73 — HIGH
- Figure 71 — MEDIUM

## Priority

`CRITICAL`

Reason: Scope is one of the main differentiators of DAIR versus classic response models. Terminology, timeline ownership and visual flow must be exceptionally clear in RU v2.
