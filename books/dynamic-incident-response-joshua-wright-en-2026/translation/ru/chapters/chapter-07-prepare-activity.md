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
