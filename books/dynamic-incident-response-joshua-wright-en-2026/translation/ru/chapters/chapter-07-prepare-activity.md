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


Canonical source приводит пример неудачного сообщения во время ransomware incident: расплывчатое описание нескольких серверов, неподтверждённое утверждение о backups, отсутствие containment status, next steps и владельца executive notification. Такой update не соответствует C4.

В C4-aligned варианте сообщение содержит точное число затронутых systems, подтверждённый status containment, явно помеченную незавершённую проверку backup integrity, владельца executive briefing и время следующего technical update.

Эффективное применение C4 требует, чтобы все участники incident понимали требования к communication и значение четырёх характеристик.

## КАНАЛЫ КОММУНИКАЦИИ

Во время incident response team взаимодействует с team members, management, legal, public relations, system stakeholders и возможными external partners. Каналы должны быть secure и reliable.

При выборе communication platform canonical source предлагает учитывать характеристики из Table 3.

### Таблица 3. Требования к communication channel

| Фактор | Требование |
|---|---|
| Authentication | Проверка identity участников с strong authentication, включая MFA. |
| Confidentiality | Encryption, access-controlled channels и controls против unauthorized access. |
| Mobility | Доступ с desktops/mobile devices при согласованной security posture и notification controls. |
| Data Retention | Сохранение history для documentation, stakeholder awareness и legal/regulatory inquiries. |
| Resilience and Availability | High availability и защита от outages/DoS во время incident. |
| Access Logging | Запись identities и доступа для audit/accountability. |
| Communication Clarity | Threaded messaging/channel organization для параллельных investigations. |
| Data Provenance | Возможность установить, кто, когда и что опубликовал и редактировалось ли сообщение. |
| Rich Information Sharing | Files, images, code snippets, text/voice/video/screen sharing. |

Организация может использовать Slack или Microsoft Teams с дополнительными controls, например private channels. Однако должен существовать **secondary communication platform**, если primary platform скомпрометирована или недоступна. Возможные alternatives в source: Signal или Element.

Backup communication channel нужно создать и протестировать заранее. Следует учитывать сценарий, в котором собственные containment actions нарушают communication: network isolation может отрезать cloud-based Slack/Teams.

Backup platform должна использовать независимую authentication, отдельную от primary directory вроде Active Directory или Entra ID. Если attacker контролирует directory, он потенциально получает доступ и к любому communication platform, который аутентифицируется через неё.

## КОНТАКТНАЯ ИНФОРМАЦИЯ

В рамках preparation необходимо документировать контакты людей, участвующих в incident response. Canonical source приводит пример IRT Contact Information Template со следующими полями:

- Incident Response Role;
- Name;
- Title;
- Organization;
- Department;
- Email;
- Alternate Email;
- office/mobile phone;
- Messaging Platform ID;
- Alternate Messaging Platform ID;
- Timezone;
- Skills/Specializations;
- Last Updated.

Контактный документ должен быть доступен response team и stakeholders, поддерживаться актуальным и существовать как минимум в digital и paper formats.

Помимо внутренних контактов, нужно поддерживать внешние:

- law enforcement;
- relevant regulatory bodies;
- cyber insurance carrier/claims contacts;
- incident response retainer providers;
- legal counsel с cybersecurity expertise;
- PR/crisis communications support;
- industry ISACs;
- vendor и cloud provider security contacts.

Задержка с поиском law enforcement или legal counsel во время incident может иметь существенные последствия.

## ВНЕШНИЕ КАНАЛЫ REPORTING

Организация должна планировать не только outbound communication, но и inbound disclosures от security researchers, customers и partners. Исследователю должно быть понятно, куда сообщить о vulnerability или compromise.

RFC 9116 решает эту задачу через machine-readable файл **security.txt**.[6]

Организация публикует его по пути:

`/.well-known/security.txt`

Файл может содержать contact information, expiration date, encryption keys, disclosure policies, acknowledgement pages и preferred languages.

### Listing 27. Microsoft security.txt Example

`THIRD_PARTY_REVIEW_REQUIRED` — canonical source воспроизводит содержимое Microsoft `security.txt`; этот сторонний verbatim-фрагмент не переносится в производный перевод до отдельной проверки прав.

Публикации `security.txt` недостаточно: указанный contact должен маршрутизироваться непосредственно в security team, а не в generic help desk или unmonitored inbox. Нужно документировать внутренний routing внешних disclosures к analysts.

## REPORTING PROCEDURES

Во время incident команда должна сообщать status разным stakeholders. Reporting procedures следует определить заранее.

IR plan должен задавать:

- purpose statement;
- scope of reporting;
- reporting requirements;
- Service Level Agreement (SLA) для reporting.

Частота зависит от impact. High-impact incident может требовать initial report в течение часа и daily updates; low-impact — weekly или bi-weekly.

### Таблица 5. Пример Incident Reporting SLA

| Impact | Описание | Initial report | Full report |
|---|---|---:|---:|
| Critical | Severe business disruption, data breach sensitive data или regulatory impact | ≤1 hour | ≤24 hours |
| High | Significant operational disruption, targeted attack или critical infrastructure compromise | ≤2 hours | ≤48 hours |
| Medium | Limited operational impact, detected malware или unauthorized access attempt | ≤4 hours | ≤72 hours |
| Low | Minimal/no operational impact, routine security event или false positive | ≤2 days | ≤5 business days |

Labels необходимо адаптировать к организации: low→critical, level 0→4, green→black и т. п.

## EMERGENCY COMMUNICATION PLAN

Emergency Communication Plan (ECP) регулирует внутреннее и публичное распространение информации об incident. Даже если broad messaging нужен не всегда, готовый plan помогает своевременно информировать правильную аудиторию и снижать риск misinformation.

ECP должен включать:

- **Notification triggers:** какие incident types требуют communication за пределы IRT.
- **Approval workflows:** кто утверждает разные типы messages; external communication обычно требует executive/legal approval.
- **Message templates:** templates для первых 24 часов common incident types, заранее reviewed legal/communications teams.
- **Constituent audiences:** customers, partners, regulators, employees и другие группы.
- **Distribution channels:** как messages доставляются каждой аудитории.
- **Spokesperson designation:** кто имеет право говорить от имени организации и должен иметь media training.

Source выделяет пять типовых communication categories:

- ransomware;
- denial-of-service (DoS);
- generic cyber attack;
- on-premises IT outage с неподтверждённой cybersecurity cause;
- third-party issue.

Templates можно комбинировать для hybrid cases. Это пример, а не исчерпывающая taxonomy.

### Regulatory notification requirements

Canonical source перечисляет common frameworks:

- **GDPR:** notification supervisory authority within 72 hours of awareness of personal data breach; affected individuals — при high risk.
- **HIPAA:** notification affected individuals, HHS и иногда media для breaches unsecured PHI.
- **U.S. State Breach Notification Laws:** требования различаются по timing/content/recipients.
- **SEC Cybersecurity Rules:** public companies disclose material cybersecurity incidents within four business days after materiality determination.
- **PCI DSS:** suspected/confirmed breaches сообщаются acquiring bank и payment card brands; обычно требуется PCI Forensic Investigator (PFI).[7]
- **NIS2:** significant incidents — early notification within 24 hours и full incident report within 72 hours.[8]
- **DORA:** major ICT-related incidents — initial notification, intermediate reports и final report including root cause analysis.[9]
- **CRA:** manufacturers digital products report actively exploited vulnerabilities и severe product-security incidents в ENISA и coordinating CSIRT; source описывает staged deadlines 24h, 72h, 14 days / one month; reporting obligations from September 2026 and full requirements from December 2027.[10]

Список не исчерпывающий; applicable notification requirements должны быть reviewed legal counsel.

### PowerSchool breach как communication example

Canonical source рассматривает PowerSchool breach как пример последствий слабой ECP. В source указано:

- attacker начал exfiltration 19 Dec 2024;
- breach обнаружен 28 Dec 2024;
- в late Dec PowerSchool выплатил приблизительно **$2.85 million** ransom и получил видео, предположительно подтверждающее deletion;
- incomplete disclosure опубликовано 7 Jan 2025 — через 10 дней после detection;
- public incident page — 13 Jan 2025;
- notification emails affected individuals — late Jan;
- CrowdStrike investigation 10 Mar 2025 выявило earlier unauthorized access ещё с Aug 2024;
- 7 May 2025 attackers начали напрямую extort school districts, используя stolen data samples.

Source указывает приблизительно **62 million students**, **9.5 million educators** и **6,505 U.S. school districts** как масштаб данных в основном breach.

В данных присутствовали sensitive records, включая special education status, mental health information, custody alerts и medication schedules. Source связывает communication failures с отсутствием pre-built downstream notifications, coordinated messaging toolkits и прозрачного protocol для ransom decisions.[11]

`THIRD_PARTY_REVIEW_REQUIRED` — прямая цитата North Carolina Superintendent Maurice Green о переходе штата на competitor Infinite Campus не воспроизводится и не переводится до отдельной проверки прав.

Для организаций, управляющих данными от имени других, communication plan должен учитывать regulatory disclosure и потребности downstream stakeholders: comprehensive notification, coordinated messaging и accurate scoping compromised data.

Все components — channels, contacts, external reporting, reporting procedures и ECP — должны существовать как единый governed incident communications plan с назначенным owner, annual review и validation на tabletop exercises.

## СОЗДАНИЕ INCIDENT RESPONSE TEAM

Incident Response Team (IRT) — основной организационный ресурс для detection, analysis и response security incidents. Team structure, roles и responsibilities следует определить в preparation.

Варианты зависят от размера, ресурсов и risk profile:

- incident response как дополнительная responsibility существующего IT/security staff;
- dedicated IRT со specialized roles;
- internal team + MSSP;
- incident response retainer для external expertise.

Нужно документировать primary/backup personnel, поддерживать contacts и escalation paths.

### Virtual vs. dedicated teams

**Virtual/soft IRT:** incident response — secondary responsibility участников.

**Dedicated/hard IRT:** incident response — primary function.

Возможна hybrid model: небольшая dedicated on-call group + wider virtual team.

Virtual teams лучше используют ресурсы, но создают конфликт priorities. Поэтому нужны clear activation procedures, временно освобождающие members от normal duties при significant incidents. Такие reassignments следует pre-approve с management и документировать activation conditions/duration по severity.

## ПЛАТФОРМА INCIDENT TRACKING

Во время incident команда должна отслеживать progress, decisions и collected evidence. Centralized collaborative incident-tracking platform обычно эффективнее manual tracking.

Платформа может поддерживать:

- incident categorization/prioritization;
- analyst assignment/activity tracking;
- status reporting;
- playbook execution tracking;
- response documentation/evidence collection.

Можно адаптировать существующие ticketing systems — JIRA, ServiceNow, Zendesk — если они поддерживают incident response process и доступны во время incident. Также возможны purpose-built incident management platforms.
