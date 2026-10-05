# Translation / editorial findings — Chapter 7

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0094:c01`–`p0165:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-07-prepare-activity.md`.

## Итог проверки

- Semantic coverage: extensive and largely complete.
- Tables 3–13 preserved.
- Listings 27–28 preserved.
- Figures 29–49 represented.
- Chapter structure is very large and information-rich.
- Main v2 problem: extremely high mixed-language density in headings and prose.

## High-priority heading cleanup

Current headings that should be normalized in v2 include:

- `РАЗНЫЕ, НО СВЯЗАННЫЕ: POLICIES, PLANS И PLAYBOOKS`
- `ПОЛУЧЕНИЕ MANAGEMENT SUPPORT ДЛЯ РАЗРАБОТКИ POLICY`
- `РАЗРАБОТКА ОРГАНИЗАЦИОННЫХ POLICIES`
- `ПРИМЕРЫ INCIDENT RESPONSE POLICY И PLAN TEMPLATES`
- `РАЗВИТИЕ MANAGEMENT SUPPORT`
- `BROAD VS. SPECIFIC RISK ASSESSMENT CRITERIA`
- `РАЗРАБОТКА INCIDENT COMMUNICATIONS PLAN`
- `СОЗДАНИЕ COMMUNICATION CHANNELS`
- `ДОКУМЕНТИРОВАНИЕ CONTACT INFORMATION`
- `EXTERNAL REPORTING CHANNELS`
- `REPORTING PROCEDURES`
- `EMERGENCY COMMUNICATION PLAN`
- `СОЗДАНИЕ INCIDENT RESPONSE TEAM`
- `VIRTUAL VS DEDICATED INCIDENT RESPONSE TEAMS`
- `INCIDENT TRACKING PLATFORM`
- `УЧЁТ ТРЕБОВАНИЙ CYBER INSURANCE`
- `SECURITY AWARENESS TRAINING`
- `ПОДГОТОВКА INCIDENT RESPONSE TEAM`
- `BACKUP И RECOVERY PROCEDURES`
- `RELATIONSHIPS С ESSENTIAL PERSONNEL`
- `DOCUMENT INCIDENT RESPONSE DECISION AUTHORITY`
- `PLAYBOOKS ДЛЯ COMMON INCIDENTS`
- `ПОДГОТОВКА RESOURCES ДЛЯ RESPONSE ACTIONS`
- `ПОДГОТОВКА ACCESS К SYSTEMS`
- `TABLETOP EXERCISES И INCIDENT RESPONSE DRILLS`
- `PROACTIVE PREVENTION AND DETECTION`
- `CYBER THREAT INTELLIGENCE (CTI) CAPABILITIES`
- `SOFTWARE MANAGEMENT PROCESSES И PROCEDURES`
- `PATCH, CONFIGURATION И INVENTORY`
- `SYSTEM HARDENING`
- `ENDPOINT-BASED SECURITY MONITORING И THREAT DETECTION`
- `NETWORK SECURITY MONITORING И THREAT DETECTION`
- `INVEST IN DETECTION ENGINEERING`
- `THREAT HUNTING PROGRAM`
- `MONITOR THE ATTACK SURFACE`
- `COLLECT AND RETAIN LOGGING INFORMATION`
- `PREPARATION CHALLENGES`
- `RESOURCE CONSTRAINTS`
- `ORGANIZATIONAL CHANGE И TURNOVER`
- `ДЕМОНСТРАЦИЯ ЦЕННОСТИ БЕЗ INCIDENTS`
- `ПРИМЕРЫ PREPARE ACTIVITY`

These headings are one of the strongest contributors to the "дерганый" reading experience noted in v1.

## Terminology anchors for v2

Use Chapter 6 terminology policy and normalize Chapter 7 prose around it:

- Prepare → Подготовка
- Incident Response Team → команда реагирования на инциденты
- Decision Makers → лица, принимающие решения
- management → руководство
- policy → политика
- plan → план
- playbook → плейбук / сценарий реагирования (book-level decision needed)
- risk assessment → оценка риска
- severity → уровень критичности
- communication channel → канал связи
- backup communication → резервный канал связи
- incident tracking platform → платформа учёта инцидентов
- cyber insurance → киберстрахование
- security awareness training → обучение осведомлённости о безопасности
- break-glass account → аварийная учётная запись
- tabletop exercise → настольное учение
- threat intelligence → разведданные об угрозах
- system hardening → усиление защищённости системы
- detection engineering → инженерия обнаружения
- threat hunting → поиск угроз
- attack surface management → управление поверхностью атаки
- logging/retention → журналирование/хранение журналов

## Structural findings

1. Chapter is extremely long; v2 should visually segment it more aggressively with consistent subheadings and spacing.
2. Step-by-Step appears duplicated in current translation headings; verify and remove accidental duplicate heading if source does not intentionally repeat it.
3. Long tables need A4 layout QA.
4. Multiple third-party figures and quoted materials require per-item rights/provenance decisions.
5. Regulatory references are time-sensitive; v2 should preserve source wording and dates, not silently "update" them.

## Visual debt

Figures 29–49.

Highest educational priority:
- 29 — Prepare waypoint;
- 35 — immutable backup;
- 36 — sample playbook;
- 37/38 — exercise examples;
- 39/40 — OpenCTI views;
- 44 — adversary simulation coverage;
- 47/48 — coordination and response timeline.

## Priority

`CRITICAL`

Reasons:
- longest operational chapter so far;
- heavy terminology drift;
- dense tables/figures;
- defines practical readiness architecture used throughout the rest of the book.

This chapter should be one of the main editorial targets in RU v2.
