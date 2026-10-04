---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 7
source_title: "Prepare Activity"
source_pdf_page_range: "94-165"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0094:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0165:c01"
translation_status: "DRAFT_IN_PROGRESS"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Chapter translated incrementally by canonical chunk ranges."
---

# Глава 7. Подготовка

Действие **prepare — подготовка** в incident response готовит организацию к возможности возникновения инцидента. Оно включает создание плана реагирования на инциденты, обучение персонала и обеспечение наличия необходимых инструментов и ресурсов, готовых к использованию при возникновении incident. Подготовка явно присутствует в моделях DAIR, PICERL и NIST SP 800-61 и является важным элементом incident response capability любой организации.

### Рисунок 29. Опорная точка Prepare Activity

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается автоматически.

Значительная часть времени incident response team должна быть посвящена подготовке. Когда команда не реагирует на активный incident, она должна готовиться к возможному incident и одновременно искать угрозы в среде организации — выполнять detect activity.

Объём подготовительной работы легко может казаться чрезмерным, однако чем лучше подготовлена команда, тем эффективнее она сможет реагировать. Подготовка — самостоятельный процесс, который можно последовательно развивать и улучшать.

Эта глава рассматривает цели подготовки, стратегии формирования организационной и командной готовности и сложности, затрудняющие подготовительные усилия. Также рассматриваются практические методы разработки policies, обучения teams и создания proactive detection capabilities.

## ЦЕЛИ ПОДГОТОВКИ

Prepare activity имеет три цели:

1. сформировать организационную готовность к incident response;
2. развить возможности incident response team;
3. создать proactive prevention and detection measures.

Если другие действия DAIR направлены на реагирование на активные угрозы, подготовка создаёт фундамент для эффективного response.

Первая цель — организационная готовность: policies, plans и playbooks для принятия решений, communication channels, reporting procedures и management support. Организации, заранее инвестирующие в эти элементы, эффективнее реагируют, поскольку решения о приоритетах, полномочиях и координации уже приняты.

Вторая цель — развитие возможностей incident response team. Технические навыки, отношения с важными сотрудниками, документированные playbooks и доступ к tools/systems повышают effectiveness. Команды, которые тренируются вместе, проводят exercises и поддерживают toolsets, действуют быстрее и увереннее.

Третья цель — proactive prevention and detection. Vulnerability management, security monitoring и интеграция Cyber Threat Intelligence (CTI) снижают вероятность и impact успешных атак и улучшают detection capabilities.

### Парадокс подготовки

Подготовка incident response сталкивается с внутренним парадоксом: её ценность наиболее заметна именно тогда, когда она требуется меньше всего. Инвестиции сложнее всего оправдать, когда они работают. Организация может серьёзно вложиться в preparation и не столкнуться с крупным incident; напротив, после серьёзного incident организации часто жалеют, что не инвестировали заранее.

Security teams могут обосновывать preparation через снижение риска, а не обещание полного предотвращения incidents. Полезные metrics: снижение Mean Time to Detect (MTTD), более быстрое containment на training exercises и улучшенная координация в tabletop scenarios.

## СТРАТЕГИИ ПОДГОТОВКИ

Подготовительные действия объединяются в три области:

- **Подготовка организации:** policies, plans, playbooks, management support, communication и coordination.
- **Подготовка incident response team:** technical skills, playbooks, relationships и tooling.
- **Proactive prevention and detection:** monitoring, threat intelligence и hardening measures.

### Policies, plans и playbooks

**Policies — политики:** высокоуровневые директивы руководства, задающие границы принятия решений. Они отвечают: **«Что решила организация?»**

**Plans — планы:** incident response plan переводит policy в operational structure: roles, responsibilities, delegated authority, escalation paths и communication workflows. Он отвечает: **«Кто что делает и когда?»**

**Playbooks — плейбуки:** пошаговые инструкции для конкретных incident types и tools. Они отвечают: **«Как мы реагируем?»**

Policies задают границы, plan — структуру и полномочия, playbooks — tactical guidance.


## ПОДГОТОВКА ОРГАНИЗАЦИИ

Подготовка организации к incident включает разработку policies, plans и playbooks, определяющих подход к реагированию. Эта область охватывает более широкие приоритеты incident response, участие management teams и вопросы того, будет ли и каким образом организация взаимодействовать и координироваться с attackers.

Эти действия формируют people/process foundation incident response: кто участвует, какими полномочиями располагает и как организация коммуницирует и принимает решения во время incident.

### Получение поддержки руководства для разработки policies

Многие подготовительные действия требуют management support, поскольку именно руководство помогает определить policy decisions, соответствующие потребностям организации. Technical leads и incident responders должны работать совместно с management.

Один из лучших способов получить management support — показать ценность incident response для организации и одновременно минимизировать объём времени, который management должно потратить на разработку policies.

Уважение к их времени и expertise — например, подготовка draft policy для review and feedback до утверждения — помогает формировать сильные рабочие отношения.

При разработке policy о подключении legal team возможны два подхода.

**Открытый вопрос:** попросить management сформулировать policy с нуля.

**Подготовленный вариант:** представить draft policy, который management может оценить, например предложив подключать legal при подтверждённых incidents, связанных с возможным public disclosure, cyber insurance claims или law enforcement coordination.

Предложение заранее продуманных вариантов показывает, что incident response lead оценил последствия вопроса и ценит время decision maker. Это снижает трудозатраты management на разработку обязательных элементов incident response.

## РАЗРАБОТКА ОРГАНИЗАЦИОННЫХ POLICIES

Организационные policies — важный инструмент управления подходом к incident response. Во время incident technical analysts и managers часто должны принимать решения с существенными последствиями. Policies и guidance должны быть разработаны заранее.

Policies наиболее полезны, когда они ясны, кратки и легко понимаются. Их следует разрабатывать совместно с relevant stakeholders и утверждать руководством, чтобы incident response team имела необходимые полномочия.

Некоторые организации предпочитают одну policy, покрывающую все аспекты incident response; другие используют отдельные policies по разным областям. Единый документ иногда проще сопровождать и он снижает риск противоречий. Раздельные policies позволяют подробнее регулировать отдельные вопросы и независимо обновлять их.

Policies необходимо регулярно пересматривать.

При разработке incident response policies следует рассмотреть:

- mission компании применительно к incident response;
- цели incident response program;
- приоритеты организации до, во время и после incident;
- policy по подключению management teams, включая GRC, legal и public relations;
- policy по оплате ransom или extortion;
- policy по коммуникации с attackers;
- policy по data retention и preservation of evidence;
- policy по reporting incidents в law enforcement, government или industry partners;
- policy по public disclosure incidents;
- policy по привлечению third-party incident response providers;
- containment authorization policy — кто вправе разрешать отключение systems.

Incident response plan должен также учитывать Recovery Time Objectives (RTO), Recovery Point Objectives (RPO), evidence retention, chain of custody и распределение ролей между teams.

### Полномочия на containment

Во время активных incidents responders часто колеблются: имеют ли они право выключить server или изолировать network segment. Такая задержка, иногда называемая **escalation paralysis**, откладывает containment.

Полезно заранее определить authorization tiers:

- **Tier 1 — SOC/IRT-authorized:** изоляция отдельных endpoints/user workstations, отключение compromised user accounts, блокировка malicious IP addresses.
- **Tier 2 — Service owner-authorized:** изоляция servers/services, отключение service accounts, firewall rules, влияющие на конкретные business functions, активация IR retainer или cyber insurance IR provider.
- **Tier 3 — Executive-authorized:** остановка production systems, изоляция network segments, действия в regulated/public-facing systems, привлечение law enforcement или regulators.

Главное различие между tiers — impact, а не seniority. Tier 1 имеет ограниченный business disruption; Tier 2 затрагивает services и требует оценки service owner; Tier 3 несёт organization-wide или regulatory consequences.

Организации, подпадающие под NIS2 или DORA, должны учитывать соответствующие обязательства: containment actions в regulated systems/services могут запускать notification и impact-assessment requirements.[1][2]

### Шаблоны policy и plan

Canonical source перечисляет сторонние templates:

- FRSecure Incident Response Plan Template;
- ICIMS Incident Response Policy Template;
- GovRAMP Incident Response Plan Template;
- Prima Incident Response Plan Template;
- CIS Incident Response Policy Template;
- CRF Resilience Management Policy Template.

`THIRD_PARTY_REVIEW_REQUIRED` — сами сторонние templates не воспроизводятся и не переводятся; сохраняются их названия и роль как starting point.

Многие templates используют линейный incident response approach, а не DAIR, однако остаются полезной отправной точкой. Chapter 16 отдельно рассматривает применение AI для подготовки incident response documentation.

## РАЗВИТИЕ MANAGEMENT SUPPORT

DAIR подчёркивает важность management support. На протяжении incident команда зависит от management при decision-making, resource allocation и communication с external stakeholders.

Для формирования support incident response leads могут:

- объяснять ценность incident response;
- информировать management об industry events, regulatory changes и threats;
- получать insight и expertise management во время preparation;
- разработать communication plan для взаимодействия с management во время incident;
- предлагать ясные и краткие decision options;
- закреплять за management actionable responsibilities — tabletop exercises, breach simulations или on-call rotations — согласуя это с frameworks вроде ISO 27001.[3]

Так формируется доверие и вероятность того, что incident response team получит необходимые ресурсы и полномочия.

## ПРОЦЕССЫ ОЦЕНКИ И КЛАССИФИКАЦИИ РИСКА

Эффективный incident response требует ясных criteria оценки risk и классификации incidents. Без predefined risk thresholds responders тратят время на определение severity и appropriate response.

Risk tolerance thresholds задают acceptable risk levels и escalation triggers. Совместно с decision makers следует определить low/medium/high/critical criteria с учётом data sensitivity, system criticality, regulatory implications и potential business impact.

Некоторые организации используют level-0/1/2; другие — color-based scheme вроде CISA green/yellow/orange/red/black.[4]

Incident classification matrix может учитывать:

- число затронутых systems/users;
- тип потенциально compromised data;
- impact на business operations;
- regulatory notification requirements;
- потенциал lateral movement/escalation.

Risk assessment processes следует регулярно пересматривать; annual review можно согласовывать с broader risk management activities.

### Broad vs. specific risk criteria

Broad criteria дают быстрый at-a-glance guidance. Canonical source приводит пример InvGate Incident Prioritization Matrix.[5]

### Рисунок 30. InvGate Incident Prioritization Matrix

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект и сторонняя матрица требуют отдельной проверки прав.

Более specific criteria удобно оформлять как decision tree/flowchart, аналогично CISA Incident Scoring rubric.

### Рисунок 31. CISA Incident Scoring Rubric

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав.

Менее опытным responders могут быть полезны detailed criteria; более опытные teams могут предпочитать broad criteria с большей flexibility.

## ПЛАН КОММУНИКАЦИИ ПРИ INCIDENT

Incident communications охватывают несколько audiences, channels и timelines: от real-time coordination responders до regulatory notifications спустя несколько дней.

Без единого плана communication распадается под давлением: teams используют разные channels, contact lists устаревают, public messaging расходится с internal updates.

Единый governed incident communications plan объединяет coordination channels, stakeholder contacts, leadership reporting procedures и emergency communication plan. Документ следует пересматривать как минимум ежегодно и тестировать на tabletop exercises.

### C4 как модель для incident communications

Canonical source адаптирует идеи C4 software architecture model Саймона Брауна к incident communications:

- **Coherent:** все сообщения основаны на едином точном понимании incident.
- **Consistent:** сообщения по channels и во времени не противоречат друг другу; нужен single source of truth и approval workflow.
- **Concise:** status updates должны сразу сообщать, что изменилось, каков impact и какое действие требуется.
- **Converted:** сообщение адаптируется к аудитории; board, SOC и customers получают одинаковые факты в разной форме.
