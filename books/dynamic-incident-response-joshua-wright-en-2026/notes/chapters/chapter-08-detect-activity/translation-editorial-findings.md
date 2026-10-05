# Translation / editorial findings — Chapter 8

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0166:c01`–`p0189:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-08-detect-activity.md`.

## Итог проверки

- Semantic coverage: good.
- Listings 29–33 preserved.
- Figures 50–56 represented.
- Main debt: headings remain heavily English and prose uses dense hybrid terminology.

## High-priority heading cleanup

Current headings requiring normalization:

- `Signature-Based Detection`
- `Behavioral Detection`
- `SCOPING BASELINES TO BUSINESS UNITS`
- `Machine Learning Detection`
- `Hybrid Detection Approaches`
- `ACTIVE VS. PASSIVE DETECTION`
- `THE TYRANNY OF INFINITE CHOICE`
- `DETECTION DATA SOURCES`
- `Technical Detection Sources`
- `OPENOBSERVE: OPEN SOURCE LOG ANALYSIS`
- `RITA: OPEN SOURCE NETWORK THREAT ANALYSIS`
- `HUMAN DETECTION SOURCES`
- `CLOUD-NATIVE DETECTION SOURCES`
- `Container and Kubernetes Detection`
- `Serverless and Microservices Detection`
- `Hybrid Cloud`
- `CHALLENGES IN DETECTION`
- `Data Volume and Velocity`
- `DETECTION-DRIVEN COLLECTION: AZURE STORAGE LOGGING`
- `Encrypted Traffic`
- `ENCRYPTED TRAFFIC DETECTION TECHNIQUES`
- `Adversary Evasion`
- `THE PRE-ATTACK LAB`
- `Skills Gap`
- `DETECT ACTIVITY EXAMPLES`
- `The External Breach Hunter`
- `The SIEM Wizard`
- `DETECT: STEP-BY-STEP`

## Terminology normalization

Candidate policy:

- signature-based detection → сигнатурное обнаружение
- behavioral detection → поведенческое обнаружение
- machine learning detection → обнаружение на основе машинного обучения
- hybrid detection → гибридное обнаружение
- baseline → базовый профиль / baseline (first use)
- active detection → активное обнаружение
- passive detection → пассивное обнаружение
- threat hunting → поиск угроз (threat hunting)
- data source → источник данных
- endpoint telemetry → телеметрия конечных устройств
- beaconing → периодические C2-обращения / beaconing
- encrypted traffic → зашифрованный трафик
- detection-driven collection → сбор данных, ориентированный на задачи обнаружения
- adversary evasion → уклонение атакующего от обнаружения
- skills gap → дефицит компетенций
- human-in-the-loop → человек в контуре принятия решения

Acronyms/tool names (EDR/NDR/SIEM/SOAR/ML/JA4/RITA/Zeek) should remain.

## Structural findings

1. Chapter 8 has a clean source structure but current translation reads unevenly because many headings remain English.
2. Listings 29–33 need monospace/A4 QA in v2.
3. Tool/product names must not be translated.
4. The transition Detect → Verify/Triage should be visually emphasized in v2.
5. Human reporting culture deserves a distinct visual/sidebar treatment because it is easy to lose among technical sections.

## Visual debt

Figures 50–56:
- 50 — Detect waypoint
- 51 — baseline by business unit
- 52 — Pyramid of Pain
- 53 — SentinelOne EDR dashboard
- 54 — OpenObserve dashboard
- 55 — RITA results
- 56 — reporting-awareness poster

Highest educational priority:
- Figure 50
- Figure 51
- Figure 52
- Figure 55

## Priority

`HIGH`

Chapter 8 is operationally important and tool-dense. The translation is technically useful already, but consistent Russian headings and terminology will make v2 substantially smoother.
