---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 7
source_title: "Prepare Activity"
source_pdf_page_range: "94-165"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0094:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0165:c01"
translation_status: "DRAFT_FOR_QA"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Inline THIRD_PARTY_REVIEW_REQUIRED markers are fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled only from full-fidelity source-range segments; condensed draft excluded."
  - "Commands, code, URLs, identifiers and technical literals are preserved unless an explicit third-party boundary applies."
---

# Глава 7. Подготовка

Действие **prepare — подготовка** в incident response предназначено для подготовки организации к возможности возникновения инцидента. Оно включает создание плана реагирования на инциденты, обучение персонала и обеспечение того, чтобы необходимые инструменты и ресурсы были подготовлены и доступны на случай возникновения incident. Подготовка явно выделяется в моделях DAIR, PICERL и NIST SP 800-61 и является важным элементом incident response capability любой организации.

### Рисунок 29. Опорная точка Prepare Activity

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически; сохраняются подпись и cross-reference.

Значительная часть времени incident response team должна уходить на подготовку. Когда команда не занята активным реагированием на incident, она должна готовиться к его возможному возникновению и одновременно активно искать угрозы в среде организации — выполнять detect activity. Объём подготовительной работы легко может показаться подавляющим, однако чем лучше подготовлена команда, тем лучше она сможет реагировать, когда incident действительно произойдёт. Подготовка — это отдельный процесс, который можно развивать и совершенствовать со временем.

Эта глава рассматривает цели подготовки, стратегии формирования готовности организации и команды, а также проблемы, осложняющие подготовительные усилия. Кроме того, в ней рассматриваются практические техники разработки policies, обучения teams и создания proactive detection capabilities, после чего приводятся примеры prepare activity.

## ЦЕЛИ ПОДГОТОВКИ

Prepare activity преследует три цели: сформировать организационную готовность к incident response, развить возможности incident response team и создать proactive prevention and detection measures. Если другие действия DAIR направлены на реагирование на активные угрозы, подготовка закладывает фундамент эффективного response.

Первая цель связана с готовностью организации. Сюда относятся разработка policies, plans и playbooks, регулирующих принятие решений во время incidents; создание communication channels и reporting procedures; получение management support для incident response capability. Организации, которые вкладываются в эти базовые элементы, реагируют эффективнее, потому что критически важные решения о приоритетах, полномочиях и координации уже были приняты заранее.

Вторая цель сосредоточена на развитии возможностей incident response team. Технические навыки, налаженные отношения с важными сотрудниками, документированные playbooks и доступ к необходимым tools и systems — всё это повышает эффективность реагирования. Teams, которые тренируются вместе, проводят exercises и поддерживают свой набор инструментов, реагируют быстрее и увереннее, чем teams, вынужденные импровизировать во время активного incident.

Третья цель — proactive prevention and detection. Ни одна организация не может предотвратить все incidents, но такие preparation activities, как vulnerability management, security monitoring и интеграция Cyber Threat Intelligence (CTI), снижают вероятность и impact успешных атак. Эти меры также улучшают detection capabilities, позволяя раньше выявлять угрозы, прежде чем они причинят значительный ущерб.

### ПАРАДОКС ПОДГОТОВКИ

У подготовки к incident response есть внутренне присущая проблема: её ценность наиболее очевидна тогда, когда она меньше всего нужна. Иными словами, инвестиции в preparation труднее всего обосновывать, когда они действительно работают. Организация, много вкладывающая в подготовку, может вообще не пережить крупного incident, и тогда кто-то начнёт задаваться вопросом, стоили ли эти затраты того. Напротив, организации, пережившие серьёзные incidents, часто хотели бы, чтобы до них они вложили в подготовку больше.

Этот парадокс может создавать напряжение при распределении ресурсов. Security teams могут уменьшить это напряжение, представляя preparation investments как снижение риска, а не как предотвращение incident. Метрики, демонстрирующие ценность подготовки, дают осязаемые доказательства: сокращение Mean Time to Detect (MTTD), более быстрое containment во время training exercises и лучшая координация в tabletop scenarios. Эти измерения позволяют доказать эффективность подготовки, не дожидаясь реального incident.

## СТРАТЕГИИ ПОДГОТОВКИ

Preparation activities делятся на три основные области:

- **Подготовка организации:** разработка policies, plans и playbooks, регулирующих принятие решений; получение management support; определение того, как организация коммуницирует и координируется во время incident.
- **Подготовка incident response team:** развитие technical skills, playbooks, рабочих relationships и tooling, позволяющих responders уверенно действовать при возникновении incident.
- **Proactive prevention and detection:** развёртывание monitoring, threat intelligence и hardening measures, снижающих частоту incidents и улучшающих способность team выявлять threats на ранней стадии.

Далее каждая из этих областей рассматривается подробнее.

### РАЗНЫЕ, НО СВЯЗАННЫЕ: POLICIES, PLANS И PLAYBOOKS

В этой главе используются термины, которые иногда смешивают: policies, plans и playbooks. Хотя их нередко применяют как взаимозаменяемые, полезно уточнить, кто отвечает за каждый из этих элементов и как они влияют на incident response team.

**Policies.** Высокоуровневые директивы, устанавливаемые руководством организации, часто CISO или executive team. Они задают границы для принятия решений: платить ли ransom, когда подключать legal counsel, при каких условиях делать public disclosure. Policies отвечают на вопрос: **«Что решила организация?»**

**Plans.** Incident response plan переводит policy в operational structure. Он определяет роли и responsibilities — часто с помощью RACI matrix (см. раздел о распределении ролей через RACI), delegated authority, escalation paths и communication workflows. Plan отвечает на вопрос: **«Кто что делает и когда?»**

**Playbooks.** Они дают пошаговые instructions для реагирования на конкретные типы incident и использования конкретных tools. Например, ransomware playbook проводит responder через containment, evidence collection и recovery actions, адаптированные к этому сценарию. Playbooks отвечают на вопрос: **«Как мы реагируем?»**

Эти три элемента работают совместно: policies задают границы, plan устанавливает structure и authority, а playbooks дают tactical guidance для выполнения действий.

## ПОДГОТОВКА ОРГАНИЗАЦИИ

Подготовка организации к incident включает разработку policies, plans и playbooks, описывающих, как организация будет реагировать. Эта область рассматривает более широкие приоритеты incident response, участие management teams, а также вопрос о том, будет ли организация взаимодействовать и координироваться с attackers и каким образом.

Эти activities охватывают people/process foundation incident response: кто участвует, какими полномочиями обладает и как организация коммуницирует и принимает решения во время incident.

### ПОЛУЧЕНИЕ MANAGEMENT SUPPORT ДЛЯ РАЗРАБОТКИ POLICY

Для многих preparation activities требуется management support, поскольку policy decisions должны соответствовать потребностям организации. Technical leads и incident responders должны работать с management, чтобы организация была готова к incident.

Один из лучших способов получить management support — показать ценность incident response для организации, одновременно сводя к минимуму время, которое management приходится вкладывать в разработку policies.

Уважение к их времени и expertise — например, предварительная подготовка outline или draft policy для review и feedback до approval — помогает выстроить сильные рабочие отношения.

Рассмотрим два подхода при совместной с management разработке policy о том, когда подключать legal team к incident.

Открытый вариант просит management определить policy с нуля:

> «Нам нужна policy, определяющая, когда подключать legal team к incident. Когда вы хотите подключать legal team при возникновении incident?»

Подход с подготовленным вариантом предлагает draft, на который management может отреагировать:

> «Я хотел бы подготовить для вашего утверждения policy по подключению legal team во время incidents. Предлагаю подключать legal при подтверждённых incidents, связанных с потенциальным public disclosure, cyber insurance claims или coordination с law enforcement. Соответствует ли это вашим ожиданиям, или есть другие сценарии, которые нужно включить?»

Предоставление management заранее продуманных вариантов показывает, что incident response lead проанализировал последствия вопроса и ценит время и expertise руководства. Разработка policy может быть сложной и требовать значительного времени и усилий. Предоставляя decision maker продуманные варианты, incident response lead помогает уменьшить время и effort, необходимые для создания policies — обязательного элемента эффективного incident response.

## РАЗРАБОТКА ОРГАНИЗАЦИОННЫХ POLICIES

Организационные policies являются важным инструментом, направляющим подход организации к incident response. Во время incident technical analysts и managers часто приходится принимать решения со значительными последствиями. Policies и guidance о том, как реагировать на incidents, следует разрабатывать заранее, чтобы организация была готова действовать эффективно.

Policies наиболее эффективны, когда они ясны, кратки и понятны. Их следует разрабатывать совместно с relevant stakeholders и утверждать руководством организации, чтобы incident response team получила необходимые полномочия для принятия решений и действий в соответствии с policy.

> Policies создаются для того, чтобы задавать ожидания относительно того, как responders должны действовать во время incident. Ясную policy, которая хорошо доведена до team и понята ею, проще всего соблюдать, когда responders работают под давлением.

Некоторые организации могут предпочесть одну policy, охватывающую все аспекты incident response; другие — отдельные policies по различным областям. Единой policy иногда проще управлять и поддерживать, при этом она помогает избегать противоречащих друг другу statements. Отдельные policies могут давать более подробное guidance по конкретным topics и их проще обновлять независимо друг от друга. Независимо от подхода, policies следует регулярно review, чтобы они оставались актуальными и соответствовали потребностям организации.

При разработке organizational policies для incident response следует рассмотреть включение следующих элементов:

- mission компании применительно к incident response;
- цели incident response program;
- приоритеты организации до, во время и после incident;
- policy по подключению management teams, включая GRC, legal и public relations;
- policy по выплате ransom или extortion;
- policy по коммуникации с attackers;
- policy по data retention и preservation of evidence;
- policy по reporting incidents в law enforcement agencies, government или industry partners;
- policy по public disclosure incidents;
- policy по привлечению third-party incident response providers или дополнительных ресурсов при необходимости;
- containment authorization policies, определяющие, кто может разрешать вывод systems offline.

Incident response plan должен также охватывать operational elements, переводящие эти policies в практику: Recovery Time Objectives (RTO) и Recovery Point Objectives (RPO) для critical systems, требования по evidence retention и chain-of-custody procedures, а также role assignments для coordination между teams.

Этот список не является исчерпывающим. Организации должны разрабатывать policies и plans, адаптированные к своим уникальным потребностям и risk profile.

Среди этих policy elements особого внимания заслуживает containment authorization. Во время active incidents responders часто колеблются из-за вопросов вроде: «Разрешено ли мне выключить этот server?» или «Могу ли я изолировать этот network segment?» Такая нерешительность, которую иногда называют **escalation paralysis**, задерживает containment, пока responders ищут approval через ad hoc channels. Документирование authorization levels заранее уменьшает задержку, устанавливая ясные decision rights для типовых containment actions.

Можно определить authorization tiers, сопоставляющие actions и approval requirements:

- **Tier 1 (SOC/IRT-authorized):** изоляция отдельных endpoints и user workstations, disabling compromised user accounts, blocking known malicious IP addresses.
- **Tier 2 (Service owner-authorized):** изоляция servers или services, disabling service accounts, внедрение более широких firewall rules, влияющих на конкретные business functions, активация IR retainer или cyber insurance IR provider.
- **Tier 3 (Executive-authorized):** shutdown production systems, изоляция network segments, действия, влияющие на regulated systems или public-facing services, а также engagement внешних parties вроде law enforcement или regulators.

Эти tiers должны отражать risk tolerance и operational requirements организации. Важнейшее различие между уровнями — impact, а не seniority: Tier 1 затрагивает отдельных users/endpoints и создаёт ограниченное business disruption; Tier 2 влияет на services и требует от service owner оценки operational impact; Tier 3 имеет organization-wide или regulatory consequences, требующие executive approval.

В зависимости от культуры организации и уровня подготовки incident response конкретные actions в каждом tier могут отличаться. Цель — дать responders уверенность быстро выполнять low-impact containment actions и одновременно обеспечить appropriate authorization для решений с существенными business/regulatory consequences.

Организации, подпадающие под regulatory frameworks вроде Network and Information Security Directive (NIS2) или Digital Operational Resilience Act (DORA), должны учитывать эти obligations при определении authorization tiers, потому что containment actions, затрагивающие regulated systems или services, могут запускать notification и impact-assessment requirements.[1][2]

### ПРИМЕРЫ INCIDENT RESPONSE POLICY И PLAN TEMPLATES

Canonical source перечисляет несколько сторонних template documents с permissive licenses, которые организации могут использовать как starting point:

- FRSecure Incident Response Plan Template;
- ICIMS Incident Response Policy Template;
- GovRAMP Incident Response Plan Template;
- Prima Incident Response Plan Template;
- CIS Incident Response Policy Template;
- CRF Resilience Management Policy Template.

`THIRD_PARTY_REVIEW_REQUIRED` — содержимое сторонних templates не воспроизводится; сохраняется факт ссылки и названия ресурсов.

Многие из этих templates сохраняют линейный подход к incident response, а не модель DAIR, предписанную в книге, но всё равно представляют ценную отправную точку для разработки organizational incident response policies и plans.

Организации также могут использовать AI platforms для помощи при drafting incident response policies и plans. Chapter 16 рассматривает применение AI для incident response tasks, включая подготовку documentation.

## РАЗВИТИЕ MANAGEMENT SUPPORT

DAIR подчёркивает важность management support для incident response. На протяжении incident incident response team будет опираться на management при принятии решений, распределении ресурсов и communication с external stakeholders. Развитие management support необходимо для успеха incident response effort.

Один из лучших способов обеспечить поддержку management во время incident — заранее выстроить сильные отношения. Все организации различаются, и у разных managers разные приоритеты и working styles. То, что помогает выстроить relationship с одним manager, может не работать с другим. Тем не менее incident response leads могут использовать несколько общих элементов:

- сообщать management о ценности incident response для организации, используя примеры из других industries или organizations;
- держать management в курсе industry events, влияющих на организацию, включая regulatory changes или новые threats, и объяснять их relevance;
- получать insight и expertise management на протяжении preparation activity;
- разработать communication plan, определяющий, как management будет информироваться во время incident и как будет направлять incident response team;
- демонстрировать уважение к их времени и expertise, предлагая clear, concise и well-considered decision options;
- назначать management actionable responsibilities, например participation в tabletop exercises, breach simulations или on-call rotations во время incidents, согласуя это с frameworks вроде ISO 27001, определяющими specific management requirements для information security.[3]

Формируя роль источника expertise и insight, incident response leads могут выстроить доверие и поддерживающие working relationships с management. Это помогает обеспечить вовлечённость management во время incident и наличие у incident response team ресурсов и authority, необходимых для эффективного response.

## ПРОЦЕССЫ ОЦЕНКИ И КЛАССИФИКАЦИИ РИСКА

Эффективный incident response требует ясных критериев оценки риска и классификации incidents. Без заранее определённых risk assessment thresholds responders теряют ценное время, определяя severity level и подходящий response. Создание risk assessment processes во время preparation обеспечивает последовательное и быстрое принятие решений при возникновении incidents.

> Во время incident responders часто ощущают давление и необходимость быстро классифицировать его и определить appropriate response. Заранее определённые risk assessment criteria позволяют принимать такие решения уверенно и последовательно, уменьшая uncertainty и delays.

Risk tolerance thresholds определяют допустимые уровни риска и escalation triggers для организации. Совместно с decision makers необходимо установить ясные критерии того, что относится к low, medium, high и critical risk events. Эти thresholds должны учитывать data sensitivity, system criticality, regulatory implications и potential business impact. Thresholds следует документировать в форме, которую responders могут быстро использовать во время incident.

> Некоторые организации считают полезным severity level-label — например, level-0, level-1, level-2 — для быстрого сообщения уровня риска вместо descriptive terms, которые могут быть более субъективны. Другие используют color-based scheme, например CISA green, yellow, orange, red, black.[4] Вместе с decision makers следует определить, какой подход лучше всего подходит для передачи risk в конкретной организации.

Incident classification criteria дают framework для категоризации incidents на основе их характеристик и потенциального impact. При разработке classification matrix следует учитывать такие factors, как:

- число затронутых systems или users;
- тип данных, которые потенциально были compromised — public, internal, confidential, regulated;
- impact на business operations — none, degraded, disrupted, halted;
- triggered regulatory notification requirements;
- потенциальная возможность lateral movement или escalation.

Risk assessment processes следует регулярно пересматривать и обновлять по мере изменения environment, threat landscape и risk tolerance организации. Annual reviews, согласованные с более широкими risk management activities, помогают сохранять classification criteria актуальными.

### BROAD VS. SPECIFIC RISK ASSESSMENT CRITERIA

Некоторым организациям полезны broad risk assessment criteria, которые дают responder быстрый at-a-glance guidance. В качестве примера canonical source приводит Incident Prioritization Matrix, опубликованную InvGate.[5] Эта matrix представляет простой framework для определения incident priority на основе impact и urgency с учётом scope impact и organizational urgency.

### Рисунок 30. InvGate Incident Prioritization Matrix

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний визуальный объект не воспроизводится автоматически.

Другим организациям могут быть полезнее более specific risk assessment criteria, дающие responders детальное guidance. Такой risk-criticality assessment лучше представлять как decision tree или flowchart, проводящий responders через последовательность вопросов к risk classification, подобно CISA Incident Scoring rubric.

### Рисунок 31. CISA Incident Scoring Rubric

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний визуальный объект не воспроизводится автоматически.

Организации должны определить, какой подход лучше отвечает их потребностям, учитывая experience команды, complexity incidents и organizational culture. Организации с менее опытными responders могут выиграть от более specific criteria с детальным guidance, тогда как organizations с опытными responders могут предпочесть broad criteria, оставляющие больше flexibility в assessment.

## РАЗРАБОТКА INCIDENT COMMUNICATIONS PLAN

Incident communications охватывают множество audiences, channels и timelines — от real-time coordination между responders до regulatory notifications через несколько дней после discovery. Без unified plan эти элементы под давлением распадаются: technical teams используют один channel, executives — другой, contact lists устаревают, а public messaging начинает противоречить internal updates.

Единый governed incident communications plan объединяет эти элементы. Следующие sections рассматривают его components: channels для coordination, contact information для stakeholders, reporting procedures для информирования leadership и emergency communication plan, управляющий public и regulatory messaging. В совокупности эти components должны поддерживаться как развивающийся документ, review не реже одного раза в год и test во время tabletop exercises.

### C4: МОДЕЛЬ ИЗ SOFTWARE DEVELOPMENT

C4 model — широко применяемый framework для visualizing и documenting software architecture. Созданная Simon Brown модель предназначена для того, чтобы придать architectural diagrams structure, clarity и consistency. Она использует hierarchical approach, помогающий teams не теряться в technical details, сохраняя при этом достаточную детализацию для effective communication.

Во время incident responders сталкиваются с той же проблемой, что software architects при работе с documentation: нескольким audiences нужно понимать одну и ту же ситуацию, но на разных уровнях detail и с разными priorities. Применение C4 thinking к incident communications означает оценивать каждое message, update и notification по четырём характеристикам:

- **Coherent — согласованность:** все сообщения основаны на едином accurate understanding incident. Technical updates, executive briefings и external statements должны рассказывать одну и ту же историю с разной детализацией, а не разные истории.
- **Consistent — непротиворечивость:** сообщения по разным channels и во времени не должны противоречить друг другу. Необходимо установить single source of truth для incident details и направлять все outbound communications через определённый approval workflow.
- **Concise — краткость:** recipients, работающим под давлением, нужна actionable information, а не длинные narratives. Status updates должны начинаться с того, что изменилось, каков impact и какое action требуется.
- **Converted — адаптация:** communication должна быть адаптирована к каждой audience. Board briefing требует другой framing, чем technical update в SOC, а customer notification — другой language, чем internal all-hands message. Каждая audience получает одни и те же facts в форме, которая позволяет ей действовать.

Эти четыре характеристики применимы к каждому компоненту incident communications plan. При review или exercise плана каждый component следует оценивать по этим критериям.

Canonical source приводит пример update в incident channel во время ransomware event:

> «Мы нашли ransomware на нескольких servers. IT с этим работает. Кажется, backups в порядке, но мы пока не уверены. Наверное, кому-то стоит сообщить CEO.»

Такое сообщение не coherent: выражение «несколько servers» оставляет scope открытым для трактовки. Оно не consistent: фраза «кажется, backups в порядке» вводит неподтверждённое утверждение, которому могут противоречить последующие updates. Оно не concise: отсутствуют containment status и next steps. И оно не converted: сообщение не адресовано конкретной audience и не определяет ownership executive notification.

C4-aligned вариант для incident channel в source выглядит следующим образом:

> «Подтверждено шифрование семи servers в finance segment вариантом LockBit. Все семь изолированы от network в 09:15 UTC. Проверка backup integrity продолжается. Incident commander готовит executive briefing к распространению в 10:00 UTC. Следующий technical update — в 10:30 UTC.»

Эффективное применение C4 во всей организации требует, чтобы каждый участник incident понимал communication expectations и важность этих характеристик. Дополнительная информация по C4 доступна на `c4model.com`.

## СОЗДАНИЕ COMMUNICATION CHANNELS

Во время incident response team должна взаимодействовать с множеством stakeholders: другими team members, management, legal, public relations, system stakeholders и, возможно, external partners. Secure и reliable communication channels важны для эффективной coordination и collaboration.

При создании channels следует учитывать характеристики platform, важные для incident response: confidentiality, authentication, mobility, rich information sharing и другие. Canonical source суммирует ключевые factors в Table 3.

### Таблица 3. Требования к communication channel

| Factor | Description |
|---|---|
| Authentication | Validation identities участников с помощью strong authentication, включая MFA. |
| Confidentiality | Encryption messages, access-controlled channels и controls, предотвращающие unauthorized access к conversations. |
| Mobility | Доступ с desktops и mobile devices при consistent security across platforms; notification controls для mobile devices. |
| Data Retention | Сохранение conversation history для documentation, stakeholder awareness и потенциальных legal/regulatory inquiries. |
| Resilience and Availability | High availability и защита от outages и denial-of-service attacks во время incidents. |
| Access Logging | Recording participant identities и platform access для audit и accountability. |
| Communication Clarity | Threaded messaging и channel organization, позволяющие сохранять discussions сфокусированными при параллельных investigations. |
| Data Provenance | Возможность установить, кто опубликовал information, когда она была опубликована и редактировалась ли она. |
| Rich Information Sharing | Support files, images, code snippets и collaboration features, включая text, voice, video и screen sharing. |

Многие организации используют уже существующие communication platforms вроде Slack или Microsoft Teams вместе с дополнительными security controls, например private channels. Это может быть разумным подходом, если определена secondary communication platform на случай, когда primary platform считается compromised или unsafe. Canonical source называет Signal и Element как возможные alternative platforms.

> Backup communication channels следует создать и test до того, как они понадобятся. Если primary communication platform compromised или unavailable во время incident, team должна уметь перейти на backup platform без задержки.

При planning backup channels необходимо учитывать сценарии, когда собственные containment actions организации нарушают communication. Network isolation, блокирующая external traffic, может отрезать cloud-based platforms вроде Slack или Microsoft Teams, оставив response team без primary coordination tool в ходе active response.

Backup platform должна использовать independent authentication, отдельную от primary directory организации — например, Active Directory или Entra ID. Если domain administrator accounts compromised, attacker, контролирующий directory, может получить доступ и к любой platform, аутентифицирующейся через неё, включая backup communications channel.

## ДОКУМЕНТИРОВАНИЕ CONTACT INFORMATION

В рамках prepare activity необходимо документировать contact information людей, участвующих в incident response process. Canonical source предлагает заполнять contact information template для каждого stakeholder и приводит пример в Table 4.

### Таблица 4. Пример Contact Information Template

| Поле | Пример из source |
|---|---|
| Incident Response Role | UNIX specialist |
| Name | Joshua Wright |
| Title | Senior Systems Administrator |
| Organization | Falsimentis Corporation |
| Department | IT |
| Email | jwright@falsimentis.com |
| Alternate Email | jwright@hasborg.com |
| Phone (office, mobile) | +1-401-555-1212 (office), +1-401-555-1213 (mobile) |
| Messaging Platform ID | @jwright (Slack) |
| Alternate Messaging Platform ID | @joswr1ght.44 (Signal) |
| Timezone | US Eastern (UTC-5) |
| Skills/Specializations | UNIX systems, cloud infrastructure, scripting |
| Last Updated | 2026-08-02 |

Contact information document должен быть доступен response team и другим stakeholders и поддерживаться в актуальном состоянии. Source рекомендует иметь его как в digital, так и в paper format, доступном team.

Помимо внутренних contacts необходимо поддерживать информацию о внешних parties, которые могут участвовать в incident response:

- law enforcement contacts — FBI, state/local law enforcement и relevant national agencies;
- regulatory bodies, относящиеся к industry организации;
- cyber insurance carrier и claims contacts;
- incident response retainer providers;
- legal counsel с cybersecurity expertise;
- public relations или crisis communications support;
- industry Information Sharing and Analysis Centers (ISACs);
- important vendor и cloud provider security contacts.

Актуальность external contacts так же важна, как и внутренних: задержки при попытке связаться с law enforcement или legal counsel во время incident могут иметь серьёзные последствия.

## EXTERNAL REPORTING CHANNELS

Внутренняя contact information поддерживает outbound communication во время incidents, но организациям также нужно подготовиться к inbound disclosures от security researchers, customers и partners, обнаруживших compromise или vulnerability. Исследователи, нашедшие проблему, часто не могут определить, с кем внутри организации нужно связаться. Без ясного reporting channel они могут прекратить попытки, опубликовать findings публично или обратиться не в тот department.

RFC 9116 решает эту проблему, определяя machine-readable file, размещаемый на web servers для публикации security contact information и vulnerability disclosure policies.[6]

Организации публикуют файл `security.txt` по пути:

`/.well-known/security.txt`

Файл содержит contact information — email, phone или URL, expiration date и optional fields для encryption keys, disclosure policies, acknowledgment pages и preferred languages.

### Listing 27. Microsoft security.txt Example

`THIRD_PARTY_REVIEW_REQUIRED` — canonical source воспроизводит verbatim содержимое Microsoft `security.txt`. Этот сторонний текст не переносится в производный перевод без отдельной проверки прав. Команда/URL назначения listing сохранены как provenance: `curl -q https://www.microsoft.com/.well-known/security.txt`.

Публикация `security.txt` — лишь половина работы. Указанный contact должен вести в security team, а не в generic help desk queue или unmonitored inbox. Организации должны документировать internal routing, чтобы external disclosures быстро доходили до analysts, способных их оценить. Затраты на создание и сопровождение файла окупаются, когда он помогает disclosure efforts и становится ранним источником уведомления internal cybersecurity team о возможной compromise.

## REPORTING PROCEDURES

На протяжении incident incident response team должна сообщать status множеству stakeholders. Если reporting procedures определены заранее, необходимая information передаётся эффективнее.

Canonical source рекомендует включать в IR plan reporting guidelines со следующими элементами:

- purpose statement;
- scope of reporting — какие incidents охватываются и кто отвечает за reporting;
- reporting requirements — какую information включать и кому её передавать;
- Service Level Agreement (SLA) для reporting.

Большинство организаций устанавливают более частые reporting requirements при более высоком perceived impact. Например, high-impact incident может требовать initial report в течение одного часа после identification и daily updates, тогда как low-impact incident — только weekly или bi-weekly updates.

### Таблица 5. Пример Incident Reporting SLA

| Impact level | Description | Initial report SLA | Full report SLA |
|---|---|---:|---:|
| Critical | Severe business disruption, data breach affecting sensitive data или regulatory impact | Within 1 hour | Within 24 hours |
| High | Significant operational disruption, targeted attack или compromise critical infrastructure | Within 2 hours | Within 48 hours |
| Medium | Limited operational impact, detected malware или unauthorized access attempt | Within 4 hours | Within 72 hours |
| Low | Minimal/no operational impact, routine security event или false positive | Within 2 days | Within 5 business days |

Impact labels следует адаптировать к потребностям организации — например, low→critical, level 0→4, green→black.

## EMERGENCY COMMUNICATION PLAN

Emergency Communication Plan (ECP) даёт guidance организации по sharing internal или public information об incident. Не каждый incident требует broad messaging, но наличие plan позволяет своевременно сообщать incident details appropriate audience и уменьшает риск misinformation.

ECP должен охватывать несколько элементов internal/public messaging:

- **Notification triggers:** какие incident types требуют communication за пределами incident response team. Следует учитывать regulatory requirements, contractual obligations и organizational policy.
- **Approval workflows:** кто должен approve communications перед distribution. Разные communication types могут требовать разных уровней approval; external communications обычно требуют executive или legal approval.
- **Message templates:** templates для первых 24 часов common incident types — периода, когда ошибки messaging особенно дорого исправлять. Templates следует заранее review legal counsel и communications professionals.
- **Constituent audiences:** customers, partners, regulators, internal employees и другие audiences, зависящие от nature incident и data involved.
- **Distribution channels:** каким способом communication доставляется каждой audience. Employees могут получать email/intranet notifications, external parties — другие channels.
- **Spokesperson designation:** кто authorized говорить от имени организации во время incidents. Назначенным spokespersons нужен media training, соответствующий их role.

Большинство incidents укладываются в пять communication categories. Template set для каждой категории даёт более быстрый starting point в первые 24 часа:

- **Ransomware:** encryption events, включая extortion-aware messaging.
- **Denial-of-service (DoS):** availability impact и customer-facing service disruption.
- **Cyber attack (generic):** intrusions, account compromise или data theft, не покрытые ransomware/DoS templates.
- **On-premises IT outage:** infrastructure failure, где cybersecurity cause подозревается, но не подтверждена.
- **Third-party issue:** cloud provider, data center или vendor incident, влияющий на организацию.

Templates можно комбинировать для hybrid cases, например third-party ransomware incident. Source подчёркивает, что это example list, а не exhaustive taxonomy; организации могут добавить categories с учётом industry, regulatory environment и risk profile.

### REGULATORY NOTIFICATION REQUIREMENTS

Многие regulatory frameworks устанавливают specific notification requirements после security incidents. Требования зависят от jurisdiction, industry и nature of data. Их следует документировать во время preparation и включать в ECP.

Canonical source перечисляет:

- **GDPR:** notification supervisory authorities within 72 hours of awareness personal data breach; notification affected individuals, если breach вероятно создаёт high risk для их rights/freedoms.
- **HIPAA:** covered entities должны notify affected individuals, HHS и в некоторых случаях media после breaches unsecured protected health information.
- **State Breach Notification Laws:** большинство U.S. states имеют собственные laws с различающимися timing/content/recipient requirements.
- **SEC Cybersecurity Rules:** public companies disclose material cybersecurity incidents within four business days after materiality determination.
- **PCI DSS:** organizations, processing/storing/transmitting cardholder data, report suspected/confirmed breaches acquiring bank и payment card brands; forensic investigation PCI Forensic Investigator (PFI) обычно required; non-compliance может привести к penalties или потере способности process card payments.[7]
- **NIS2:** essential/important entities в EU должны notify relevant national authority significant incidents within 24 hours of awareness; full incident report due within 72 hours.[8]
- **DORA:** financial entities в EU classify/report major ICT-related incidents competent authority, включая initial notification, intermediate reports и final report с root cause analysis.[9]
- **CRA:** Cyber Resilience Act применяется к manufacturers, importers и distributors products with digital elements на EU market. Manufacturers report actively exploited vulnerabilities и severe product-security incidents двум external entities: ENISA и designated coordinating CSIRT. Source указывает staged deadlines: early warning within 24 hours, detailed notification within 72 hours, final vulnerability report within 14 days или final incident report within one month. Reporting obligations — from September 2026, full CRA requirements — from December 2027.[10]

Список не exhaustive. Organizations в нескольких jurisdictions или regulated industries могут иметь дополнительные obligations; legal counsel должен review applicable requirements.

## ПРИМЕР: POWERSCHOOL BREACH 2025

ECP напрямую влияет на reputation и stakeholder confidence после incident. Source рассматривает breach PowerSchool.

PowerSchool — student information system platform, управляющая sensitive data миллионов students и educators в США и Канаде. В December 2024 attacker использовал compromised credential customer support portal PowerSchool для exfiltration personal data приблизительно **62 million students** и **9.5 million educators** в **6,505 U.S. school districts**.

Source сообщает, что PowerSchool сделал incomplete notification спустя десять дней после detection, а некоторые districts узнали о breach из news coverage до formal communication. PowerSchool не раскрыл details specific compromised data, из-за чего тысячи school administrators самостоятельно готовили parent notifications на основе incomplete/inconsistent information.

### Таблица 6. PowerSchool Breach Communication Timeline

| Date | Event |
|---|---|
| Dec 19, 2024 | Attacker начинает exfiltration student/educator data из customer support portal. |
| Dec 28, 2024 | PowerSchool detects breach — 9 days after exfiltration began. |
| Late Dec 2024 | PowerSchool pays approximately **$2.85 million** ransom и получает video, purportedly showing data deletion. |
| Jan 7, 2025 | PowerSchool делает incomplete disclosure — 10 days after detection. |
| Jan 13, 2025 | PowerSchool публикует public incident page. |
| Late Jan 2025 | Начинаются notification emails affected individuals. |
| Mar 10, 2025 | CrowdStrike investigation reveals earlier unauthorized access dating back to August 2024 — over 100 days before main exfiltration. |
| May 7, 2025 | Attackers начинают extort school districts напрямую, используя samples stolen data, что показывает ложность deletion assurance. |

Breach exposed sensitive records, включая special education status, mental health information, custody alerts и medication schedules. В некоторых districts выяснилось, что compromised были decades historical student data.

Source связывает communication failures с отсутствием pre-built notification для downstream organizations, coordinated communication toolkits для districts/parents и protocol прозрачного сообщения ransom decisions. Такая неподготовленность привела не только к ransom payment, но и к потере trust и reputational damage; несколько customers после breach перешли на competitor platforms.[11]

`THIRD_PARTY_REVIEW_REQUIRED` — canonical source содержит прямую цитату North Carolina Superintendent Maurice Green о переходе штата с PowerSchool на Infinite Campus. Цитата не воспроизводится и не переводится без отдельной проверки прав.

Организации, управляющие данными от имени других, должны разрабатывать communication plans, учитывающие regulatory disclosure requirements и потребности downstream stakeholders: comprehensive notification, coordinated messaging и accurate scoping compromised data. Инвестиции в такие plans заранее обходятся значительно дешевле, чем восстановление trust после плохо управляемого disclosure.

Все компоненты — communication channels, contact information, external reporting channels, reporting procedures и ECP — вместе образуют incident communications plan. Их следует поддерживать в едином governed document, чтобы изменение одного component отражалось рядом с остальными. Plan должен иметь конкретного owner, review как минимум ежегодно и validation во время tabletop exercises на coherent, consistent, concise и audience-appropriate communication.

## СОЗДАНИЕ INCIDENT RESPONSE TEAM

Incident Response Team (IRT) служит основным ресурсом организации для detection, analysis и response security incidents. Определение structure, roles и responsibilities во время preparation создаёт ясную accountability при возникновении incidents.

Организации могут строить incident response capability различными способами в зависимости от size, resources и risk profile. Small organizations могут назначить incident response дополнительной responsibility существующего IT/security staff. Larger organizations могут содержать dedicated incident response teams со specialized roles. Некоторые дополняют internal capabilities через MSSPs или incident response retainer agreements, дающие доступ к external expertise при необходимости.

Нужно документировать team structure, включая primary и backup personnel; поддерживать contacts актуальными и доступными через multiple channels; определять escalation paths для ситуаций, где нужны дополнительные resources или management decisions.

### VIRTUAL VS DEDICATED INCIDENT RESPONSE TEAMS

Многие организации используют **virtual/soft IRT**, где incident response — secondary responsibility участников наряду с primary roles. **Dedicated/hard IRT** назначает members incident response как primary function. Возможен hybrid approach: небольшая dedicated on-call group, которую при необходимости усиливает wider virtual team.

Virtual teams максимизируют resource efficiency, но создают проблемы во время active incidents, когда members должны балансировать competing priorities.

Для virtual teams полезны clear activation procedures, временно освобождающие team members от normal duties во время significant incidents. Эти temporary reassignments следует pre-approve с management, чтобы activation происходила без delay. Нужно документировать trigger conditions и expected reassignment duration для разных severity levels.

## INCIDENT TRACKING PLATFORM

Во время incident response team должна отслеживать progress, фиксировать decisions и document collected evidence. Хотя это можно делать вручную, большинство организаций выигрывают от centralized collaborative incident-tracking platform.

Incident tracking platform позволяет record/track incident от initial detection до resolution. Частые features:

- incident categorization/prioritization;
- analyst assignment/activity tracking;
- status reporting;
- playbook execution tracking;
- response documentation/evidence collection.

Эти capabilities помогают сохранять situational awareness и accountability на протяжении response effort.

Многие организации переиспользуют existing ticketing systems. Это разумно, если system настроена под incident response process и доступна team во время incident. Source называет JIRA, ServiceNow и Zendesk как примеры.

Alternative — purpose-built incident management platforms; дальнейший текст продолжает их рассмотрение в следующем source segment.

Purpose-built platforms специально рассчитаны на incident response и часто включают automated incident categorization, integration with threat intelligence feeds и сбор/reporting incident metrics. Canonical source называет коммерческие options: **DFIR-IRIS, Incident.io и SmartSOAR**.

> Для некоторых организаций shared document или spreadsheet может быть достаточным для incident tracking, особенно при небольшом числе incidents или ограниченных resources. Можно создать spreadsheet template с fields для incident details, status, assigned personnel и notes, а затем копировать его как starting point для каждого нового incident.

### STANDARDIZED VOCABULARY WITH MITRE ATT&CK

Ясность incident documentation важна и для effective communication во время incident, и для post-incident analysis. Inconsistent terminology и разные definitions — распространённая проблема cybersecurity: разные teams могут использовать разные названия одного attacker behavior. Отсутствие стандартизации приводит к confusion и miscommunication, особенно при coordination между internal teams или с external partners.

MITRE ATT&CK framework предоставляет широко принятую taxonomy adversary tactics, techniques and procedures и служит common language cybersecurity community.[12] Хотя MITRE ATT&CK имеет широкий спектр применений для threat modeling, detection engineering и adversary simulation, один из наиболее практичных benefits для incident tracking — стандартизация vocabulary.

Когда analysts описывают attacker activity через ATT&CK technique identifiers — например, **T1059 Command and Scripting Interpreter** или **T1078 Valid Accounts** — terminology становится однозначной и consistent независимо от автора report.

### Рисунок 32. MITRE ATT&CK Framework Website Technique Identifier

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Применение ATT&CK terminology в incident tracking platform улучшает documentation quality и позволяет structured analysis. Incident records, tagged ATT&CK techniques, можно search, correlate и compare между incidents, выявляя patterns attacker behavior и измеряя detection coverage со временем. При оценке incident-tracking platforms следует учитывать возможность categorization incidents через ATT&CK tactics/techniques.

## УЧЁТ ТРЕБОВАНИЙ CYBER INSURANCE

Многие организации имеют cyber insurance policies, но их часто приобретают risk management или finance teams без прямого участия cybersecurity group. В результате incident response team оказывается связана contractual requirements, в формировании которых не участвовала, и узнаёт ограничения policy только тогда, когда incident заставляет обратиться к carrier/insurer.

Во время incidents требования carrier могут существенно влиять на response decisions: какие IR firms можно привлекать, когда уведомлять law enforcement и как определять scope breach notification.

Financial interest carrier в минимизации claim costs может конфликтовать с необходимостью организации провести thorough investigation и complete remediation. Многие policies включают **breach coach** — назначенного carrier attorney — в response chain, чтобы направлять engagement, выбирать vendors и контролировать flow decisions.

Некоторые policies уменьшают или отказывают в coverage, если организация привлекает non-panel IR vendors; другие требуют notify carrier до обращения в law enforcement или external IR teams. Неправильная последовательность response actions может поставить reimbursement под угрозу в самые критические первые часы incident.

### Рисунок 33. Travelers Insurance Cyber Coach Promotional Article [13]

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний визуальный/промоматериал не воспроизводится.

> Финансовый интерес insurance carrier в минимизации claim costs может конфликтовать с потребностью организации в thorough investigation и complete remediation.

Чтобы избежать конфликтов во время active incident, cyber insurance необходимо заранее интегрировать в incident response planning:

- **Получить и review policy.** Запросить copy cyber insurance policy у risk management/finance и review совместно с IR team. Убедиться, что incident response plan соответствует notification timelines, pre-approval requirements, vendor restrictions и coverage exclusions — например, social engineering, acts of war или failure to maintain security controls.
- **Заранее согласовать vendor preferences.** Если у организации уже есть relationship с IR firms, договориться о включении этих firms в approved vendor panel carrier при оформлении или renewal policy, а не во время active incident.
- **Включить policy owner в IRT.** Person, responsible за cyber insurance policy, должен быть в contact list incident response team и участвовать в tabletop exercises.
- **Обеспечить offline access.** Копия cyber insurance policy, contacts carrier и claims procedures должна существовать вне primary network. Incidents, ограничивающие network access, могут сделать policy details недоступными именно тогда, когда они нужны. Offline documentation должна содержать claims phone, policy number и authorization details для activation coverage.
- **Защитить policy от disclosure.** Не хранить cyber insurance policy на systems, доступных attackers, и не раскрывать details policy во время ransom negotiations. Attackers, узнав coverage limits, могут подстроить demands; unauthorized disclosure policy также может void coverage.
- **Привлекать independent legal counsel.** Breach coach carrier представляет интересы carrier. Организация должна использовать собственный legal counsel при decisions о regulatory notification и disclosure scope, когда интерес carrier по минимизации costs может не совпадать с legal obligations организации.

Risk incomplete investigation может значительно превышать short-term cost savings, приоритетные для carrier-directed response. Организации, интегрировавшие cyber insurance в preparation, могут эффективно координироваться с carriers и одновременно отстаивать thorough investigation/remediation.

> Многие cyber insurance policies включают pre-breach services, которые policyholders редко используют: tabletop exercises, vulnerability assessments и reviews incident response plans. Следует спросить carrier/broker о доступных services и использовать carrier-facilitated tabletop exercises для выстраивания отношений с panel providers до реального incident.

### CYBER SAFE HARBOR LEGISLATION

Всё больше U.S. states принимают cyber safe harbor laws, предоставляющие организациям affirmative legal defense против некоторых claims после data breach при условии, что организация демонстрирует compliance с признанным cybersecurity framework.[14]

Source указывает: Ohio первым принял такой law в 2018 году; затем Utah, Connecticut, Iowa, Oregon, Tennessee и Texas. В Florida и West Virginia legislators приняли cyber safe harbor bills в 2024 году, но governors наложили veto.

### Рисунок 34. Cybersecurity Safe Harbor Laws in the United States

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Эти laws признают frameworks, включая NIST Cybersecurity Framework, CIS Critical Security Controls, ISO 27001 и другие, как evidence reasonable cybersecurity practices. Например, Texas Cybersecurity Safe Harbor Law (SB 2610), effective September 2025, предоставляет small/mid-sized businesses, внедрившим и поддерживающим qualifying cybersecurity program, protection от punitive damages — monetary penalties сверх actual losses, назначаемых судом для punishment negligent behavior.

Для incident response teams safe harbor legislation даёт дополнительное обоснование investments в preparation. Compliance с recognized framework не только укрепляет security posture, но может давать legal protection и снижать exposure после incident. Организациям следует совместно с legal counsel определить применимые safe harbor provisions и убедиться, что cybersecurity programs соответствуют qualifying criteria.

## SECURITY AWARENESS TRAINING

Security awareness training превращает employees из потенциальных vulnerabilities в активных участников security posture организации. Хорошо обученные employees становятся ранним detection layer, замечая и сообщая suspicious activities, которые technical controls могут пропустить.

Effective programs должны охватывать несколько objectives, важных для incident response:

- **Incident recognition:** employees должны понимать, что считается security incident, и распознавать common indicators: phishing attempts, unusual system behavior, unauthorized access requests.
- **Reporting procedures:** каждый employee должен знать, как сообщить suspected security incident, кому обращаться и какую information предоставить. Clear accessible channels стимулируют prompt notification.
- **Social engineering resistance:** training должен включать phishing, pretexting и baiting. Понимание tactics снижает вероятность successful deception.
- **Data handling:** employees должны понимать data classification requirements и proper handling sensitive information, снижая риск accidental exposure.

Training становится эффективнее, когда включает practical exercises, а не только passive content. Simulated phishing campaigns дают measurable feedback по awareness и выявляют сотрудников, которым нужна дополнительная training.

> Security awareness training следует координировать с incident response team. Когда employees сообщают suspected incidents — даже если они оказываются false alarms — их vigilance следует acknowledge и благодарить. Positive reinforcement поддерживает дальнейшее reporting и показывает, что reports действительно ценятся.

## ПОДГОТОВКА INCIDENT RESPONSE TEAM

Подготовка IRT включает развитие skills, tools, relationships и processes, позволяющих эффективно реагировать. Она должна обеспечить способность members решительно действовать под pressure, сотрудничать с другими departments и уверенно выполнять response activities.

Если предыдущий раздел был сосредоточен на organizational structure/policy, здесь соединяются people, process и technology: team training, playbook development, tools и access для response operations.

### ОБУЧЕНИЕ INCIDENT RESPONSE TEAM

Technical competence — фундамент эффективного incident response. Members должны иметь skills для detection threats, collection evidence, analysis attacker activity и выполнения containment/eradication actions. Training programs должны включать foundational skills и advanced techniques, соответствующие roles.

Core technical training areas:

- **SOAR:** familiarity Security Orchestration, Automation, and Response platforms для automation repetitive tasks, workflow orchestration и management incident response processes.
- **Digital forensics:** collection, preservation и analysis evidence в Windows, Linux и cloud environments; file systems, registry analysis, memory forensics, timeline construction.
- **Network analysis:** packet capture analysis, network flow interpretation, identification command-and-control communications; tools like Wireshark, Zeek и network detection platforms.
- **Malware analysis:** basic static/dynamic analysis malicious code behavior и safe handling malware samples.
- **Log analysis:** proficiency SIEM, parsing/correlation techniques, common log formats и investigative value.
- **Scripting and automation:** automation repetitive analysis tasks и custom tools; особенно полезны Python, PowerShell и UNIX shell scripting.
- **Leadership and negotiation:** способность вести cross-functional response effort и communicate с executives/stakeholders без одинакового technical background.

Вместе эти области дают responders широту skills для investigations в diverse environments.

Помимо technical skills responders полезно обучаться communication, documentation и decision-making under pressure. Эти soft skills часто отличают effective responders от тех, кому сложно действовать при high-stress incidents.

> Training должна быть ongoing, а не one-time event. Threats постоянно меняются, responders должны регулярно обновлять skills. Следует budget annual training и conference attendance.

## BACKUP И RECOVERY PROCEDURES

Backup/recovery capabilities напрямую определяют способность организации восстанавливаться после incidents, особенно ransomware, где data encrypted/destroyed, а также после non-malicious failures или accidental deletions. Preparation должна подтвердить, что backups существуют, защищены от compromise и могут быть restored в acceptable timeframes.

Сначала необходимо document current backup architecture и organizational requirements:

- какие systems/data backed up;
- frequency и retention periods;
- storage locations: on-premises, cloud, off-site;
- access controls/authentication;
- RTO и RPO для critical systems.

Нужно оценить resilience backup против common attack scenarios. Современные ransomware operators целенаправленно атакуют backup infrastructure, чтобы увеличить leverage. Следует проверить, останутся ли backups intact, если attacker получит privileged access.

Source рекомендует:

- **Immutable backups:** storage не допускает modification/deletion заданный retention period даже administrators.
- **Air-gapped copies:** offline copies, недоступные через network connectivity.
- **Separate authentication:** credentials backup systems отделены от production identity environment.
- **Backup integrity monitoring:** detection unauthorized access/modification attempts.
- **Notifications for backup failures:** failures вызывают alerts ответственным personnel.

Комбинация controls создаёт layered defense для backup infrastructure.

> Во многих ransomware incidents attackers отключают backup systems и ждут, пока старые backups age out, а затем требуют ransom. Failure notifications должны идти нескольким recipients и escalated, если проблема не устраняется prompt.

Regular restoration testing проверяет, что investment в backup действительно даёт recovery capability. Необходимо schedule periodic restoration tests, measure actual recovery times against RTO и verify data completeness against RPO; results следует document, а gaps — устранить.

### ПРАВИЛО BACKUP 3-2-1-1

Traditional 3-2-1 rule: три copies data, два разных media types, одна copy off-site. Для ransomware resilience source расширяет его до **3-2-1-1**: добавить ещё одну immutable или air-gapped copy, которую нельзя удалить/manipulate через network connectivity или compromised credentials.

### Рисунок 35. Backup System with Immutable Copy

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Эта дополнительная copy — last line of defense, когда attackers compromise и backup infrastructure, и production systems. Без immutable backups организации могут оказаться перед выбором между ransom и total data loss.

## RELATIONSHIPS С ESSENTIAL PERSONNEL

Incident response редко происходит изолированно. Effective response требует collaboration departments, каждый из которых даёт specialized expertise. Relationships следует строить до incident.

Important contacts:

- business unit leaders;
- essential stakeholders — system owners/application managers;
- SOC;
- IT Operations — sysadmins, network engineers, DBAs;
- help desk;
- legal counsel;
- HR;
- public relations.

Relationships нужно строить через regular interaction, а не ждать incident. Key contacts следует привлекать к tabletop exercises, делиться relevant threat intelligence и получать их input во время preparation. Тогда при incident established relationships ускоряют coordination и уменьшают friction.

### CLARIFYING ROLES WITH A RACI MATRIX

RACI matrix уточняет ответственность при incident response и снижает confusion при collaboration нескольких teams.

- **Responsible:** person/team, выполняющие работу.
- **Accountable:** единственный individual с final authority и ответственностью за outcome.
- **Consulted:** те, чей input запрашивается до decisions — two-way communication.
- **Informed:** те, кого держат в курсе progress/decisions — one-way communication.

### Таблица 7. Пример RACI Matrix для Incident Response Activities

| Activity | IR Lead | SOC | IT Ops | Legal | HR | Comms |
|---|---|---|---|---|---|---|
| Initial detection and triage | A | R | C | I | I | I |
| Containment decisions | R/A | C | R | C | I | I |
| Evidence preservation | R/A | R | C | C | I | I |
| System recovery | A | I | R | I | I | I |
| External communications | C | I | I | C | I | R/A |
| Employee-related actions | C | I | I | C | R/A | C |

Это simplified example. Organizations должны расширять RACI relevant groups: executive leadership, regulators, affected business units, cyber insurance contacts, third-party IR providers.

Organizations, создающие RACI во время preparation и validating его through tabletop exercises, получают более clear role definitions. При реальном incident participants уже знают responsibilities и могут focus on execution, а не negotiate roles.

Matrix следует review/update annually или при organizational changes.

## DOCUMENT INCIDENT RESPONSE DECISION AUTHORITY

RACI показывает, кто участвует в activities, но не определяет, кто authorized принимать наиболее consequential decisions. **Incident response authority matrix** дополняет RACI: указывает authority для major decision, delegate на случай unavailable primary authority и documentation, которую должно породить решение.

RACI охватывает staffing/coordination; authority matrix — decision rights и evidence решения.

Authority matrices особенно полезны под high pressure, когда decisions по containment, scope expansion или external notification должны приниматься быстро. Они также дают compliance evidence для CSF 2.0 Govern function, где assessors ожидают named decision authorities.

### Таблица 8. Пример Incident Response Authority Matrix

| Decision | Authority | Delegate | Documentation Required |
|---|---|---|---|
| Incident declaration | Incident Commander | Senior analyst on duty | Incident ticket с declaration timestamp и rationale |
| Containment action with material business impact | Incident Commander + business unit head concurrence | CISO if Incident Commander unavailable | Containment decision record + business impact assessment |
| Scope expansion to additional business units | Incident Commander with notification to CISO | None | Scope expansion log entry + trigger rationale |
| Response Actions Loop exit, technical closure | Incident Commander based on eradication validation | Senior analyst with written Incident Commander approval | Signed loop exit checklist |
| Response Actions Loop exit, residual risk acceptance | CISO or designated risk owner | Board-level executive for significant incidents | Signed risk acceptance record + residual risk description |
| Regulatory notification, decision to notify | Legal counsel with CISO | General Counsel | Notification decision log + timeline/regulator |
| Post-incident improvement ownership | Incident Commander from declaration through debrief closure, then Security Program Manager | None | Improvement register + named owners/milestone dates |
| Media/public communications | Communications lead with Legal sign-off | CEO for material incidents | Approved statement with version control/distribution record |

Role names следует адаптировать к фактической structure организации. Value matrix — убрать ambiguity authority и определить documentation каждого decision для audit review и post-incident debrief.

Matrix следует review/update при изменениях authority и validate tabletop exercises.

## PLAYBOOKS ДЛЯ COMMON INCIDENTS

Playbooks — essential tool IRT. Incident часто сопровождается high stress, chaotic/initially misunderstood details и множеством tasks за короткое время. Playbook даёт structured approach и steps для specific incident type.

Effective playbooks имеют:

- **Actionable steps:** sufficiently specific для trained responder без дополнительного research.
- **Decision points:** decision trees common scenarios.
- **Tool references:** tools и command-line syntax where applicable.
- **Communication triggers:** когда notify stakeholders, escalate management или involve external parties.
- **Documentation requirements:** какое evidence collect и как document actions.

Playbook development — ongoing iterative process; документы должны evolve из lessons learned и threat landscape changes.

Разрабатывать следует playbooks для incident types, наиболее вероятных для организации, начиная с IOC, который даёт responder clear investigation starting point.

Canonical source перечисляет publicly available resources:

- CERT Societe Generale Incident Response Methodologies;
- Sudhakara Raju’s Playbooks;
- CISA Cybersecurity Incident and Vulnerability Response Playbooks.

Перечень продолжается в следующем canonical segment.

Canonical source продолжает список publicly available playbooks:

- **Mike Lamb’s Playbooks:** collection playbooks для Amazon Elastic Kubernetes Service, Amazon Elastic Container Service, Citrix и VMware ESXi.
- **Jai Minton’s DFIR Cheat Sheet:** collection scripts и manual investigation steps для расследования compromise Microsoft Windows systems.

Раздел 16.4.1 рассматривает использование AI для помощи при generation playbooks для specific IOCs.

### Рисунок 36. Sample Incident Response Playbook

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Playbooks следует review/update после каждого incident, где они использовались, и после каждого exercise, где они тестировались. Нужно document, что сработало хорошо, чего не хватало и что можно улучшить. Такой continuous improvement сохраняет playbooks relevant и effective.

## ПОДГОТОВКА RESOURCES ДЛЯ RESPONSE ACTIONS

Incident response team нужен доступ к range tools/resources для эффективного response. Они обеспечивают technical capabilities для containment systems, collection data, investigation threats, eradication и recovery.

### Forensic Workstations

Dedicated analysis systems с investigation tools, изолированные от production networks. Forensic workstations должны иметь достаточные processing power и storage для large evidence files, memory dumps и disk images.

Следует поддерживать Windows и Linux analysis environments для investigations разных system types. Там, где это соответствует environment, нужны и дополнительные platforms — macOS, другие UNIX systems, cloud instances и т. п.

Организации с существенной cloud infrastructure могут использовать cloud-based forensic workstations, размещая analysis capability ближе к data и уменьшая время transfer больших evidence sets.

### Evidence Collection Tools

Software для acquisition forensic images и volatile data с compromised systems. Source приводит memory acquisition tools **WinPMEM** и **LiME**, disk imaging tools и endpoint collection agents. Tools должны быть tested и readily accessible до incident.

### Analysis Tools

Software для examination collected evidence, включая:

- timeline analysis: Plaso, log2timeline;
- memory analysis: Volatility, MemProcFS;
- disk/artifact forensics: Autopsy, X-Ways, FTK, Magnet AXIOM;
- log analysis и SIEM platforms;
- network traffic analysis: Wireshark, Zeek;
- EDR, XDR и EPP consoles для host telemetry и response actions;
- Cloud Security Posture Management (CSPM) platforms для visibility cloud configuration changes/policy violations.

Кроме dedicated forensic tools необходимо определить существующие security/operational tools, полезные для investigation. Например, Data Loss Prevention (DLP) platforms часто содержат detailed records file movements и data transfers, ценные при scoping и evidence analysis.

Analysts должны быть знакомы с tools до incident: обучение новому tool во время active response замедляет investigation.

### Evidence Storage

Secure storage для forensic images/artifacts с appropriate access controls, integrity verification и retention management. Доступная ёмкость должна учитывать worst-case data volume и retention duration.

### Jump Bag / Go Kit

Portable incident response equipment для on-site investigations: bootable USB drives с forensic tools, write blockers, portable storage, network cables и documentation templates.

### COMMERCIAL VS. OPEN-SOURCE FORENSIC TOOLS

Организации должны решить, инвестировать ли в commercial forensic tools или использовать open-source alternatives.

Commercial tools вроде **EnCase, FTK и X-Ways** предлагают polished interfaces, vendor support и established credibility в legal proceedings. Недостатки — значительные licensing costs и возможная меньшая flexibility.

Open-source tools **Autopsy, Volatility и Plaso** дают мощные capabilities без licensing costs и позволяют customization. Но часто требуют большей expertise и не имеют formal support channels.

Многие организации используют hybrid approach: commercial tools для primary investigations, open-source — для specific analysis и automation. Независимо от выбора analysts должны быть trained/proficient заранее.

## ПОДГОТОВКА ACCESS К SYSTEMS

Responders нужен быстрый access к systems для investigation, containment и eradication. Ожидание approvals во время active incident тратит critical time и позволяет attacker укреплять foothold. Preparation должна заранее создать access mechanisms и возможность быстро получить necessary privileges.

Первый шаг — **break-glass accounts** для emergency access. Они дают elevated privileges, если normal access methods unavailable или compromised. Credentials необходимо защищать hardware tokens или secured credential vault и выдавать только с appropriate organizational approval. Любое использование должно вызывать alert; accounts следует periodically test.

> Access preparation должна балансировать response speed и security. Break-glass accounts/elevated privileges создают significant risk при misuse. Нужны monitoring, multi-person authorization для sensitive actions и regular access reviews.

Далее следует документировать access procedures:

- кто authorizes investigative access к production systems;
- как request access after hours/emergency;
- как работать с systems разных business units;
- как получать access cloud environments/third-party services.

Procedures должны быть доступны team до incident.

Наконец, нужно document procedures получения support у cloud providers и critical vendors: security contacts, escalation paths и prerequisites — account numbers, support contracts, verification procedures. Эти paths следует периодически test.

## TABLETOP EXERCISES И INCIDENT RESPONSE DRILLS

Exercises/drills проверяют preparation и находят gaps до того, как их выявит реальный incident. Teams, тренировавшиеся вместе, эффективнее действуют под pressure, потому что уже проходили decision points, communication challenges и coordination issues в low-stakes environment. Реалистичные и даже увлекательные drills также укрепляют collaboration и confidence.

**Tabletop exercises** — discussion-based sessions, где participants обсуждают response к hypothetical scenario. Они требуют сравнительно небольших организационных затрат и могут включать разные departments/management levels. Tabletop особенно полезен для testing communication procedures, decision-making и team coordination.

Для exercise следует:

- разработать realistic scenario на основе relevant threats;
- включить participants всех departments, involved в incident response;
- назначить facilitator, который ведёт discussion и вводит scenario developments;
- назначить note-taker для observations/improvement opportunities;
- выделить достаточно времени — source рекомендует обычно **2–4 hours**;
- провести debrief сразу после exercise, пока lessons learned свежи.

При выборе scenario source рекомендует использовать publicly reported incidents, затронувшие похожие organizations, либо AI platform для review recent industry news и generation scenarios по real-world incidents.

Tabletop должен test не только technical procedures, но и **authorization levels**. Scenario injects должны заставлять participants принимать containment decisions — например, изолировать ли compromised server, hosting customer portal, немедленно или ждать management approval. Такие моменты показывают, достаточно ли clear authorization policies и уверены ли responders в пределах approved authority.

**Technical drills** идут дальше: responders hands-on отрабатывают skills в simulated/isolated environments. Они проверяют, способны ли members реально выполнить documented playbooks. Примеры:

- evidence collection на test systems;
- malware analysis controlled samples;
- log analysis scenarios с planted indicators;
- containment procedure walkthroughs в lab environment.

**Full-scale exercises** объединяют tabletop discussion и technical execution и являются наиболее realistic test incident response capability. Они требуют значительного planning/resources, поэтому большинство organizations проводят их annually для critical scenarios. Инвестиция окупается при реальном incident.

Раздел 16.4.3 рассматривает применение AI для generation tabletop scenarios на основе specific IOC или attack techniques.

### TABLETOP EXERCISE GAME PLAY: BACKDOORS & BREACHES

Card game **Backdoors & Breaches**, published by Black Hills Information Security, предлагает engaging способ practice incident response. Activity-based cards используются для exploration attack paths и practice decision-making.

Source описывает использование twenty-sided die для randomness; cards представляют initial compromise, pivoting, privilege escalation, persistence, command and control и data exfiltration. Игра collaborative: participants выигрывают/проигрывают вместе в зависимости от collective incident response decisions.

### Рисунок 37. Backdoors & Breaches: Compromised Web Server Card

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний card visual не воспроизводится автоматически.

Game подходит разным skill levels. Cards доступны на English/Spanish, включая core set и expansion packs; source также указывает free download для printing/digital use.

### NCSC EXERCISE TOOLKIT

Ещё один resource — **NCSC Exercise Toolkit** от UK National Cyber Security Centre. Он включает pre-planned micro exercises и full tabletop exercises по scenarios: ransomware, Wi-Fi breach, remote work compromise, insider data breach и др.

### Рисунок 38. NCSC Insider Threat Tabletop Exercise

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний visual не воспроизводится автоматически.

Каждый NCSC exercise-in-a-box scenario включает:

- facilitator guide;
- collection injects — updates, вводимые по мере развития scenario;
- desirable/optional attendee roles — senior incident leader, cybersecurity engineer, HR advisor, PR officer и др.;
- short briefing каждому participant с role/responsibilities.

Source оценивает NCSC tabletop-in-a-box как простой способ начать practice incident response с минимальной setup effort. Sessions рассчитаны примерно на **30–60 minutes** и подходят in-person/remote teams.

## PROACTIVE PREVENTION AND DETECTION

Proactive prevention/detection measures снижают likelihood successful attacks и улучшают раннее threat identification. Хотя эти activities выходят за традиционные boundaries incident response, они напрямую улучшают response effectiveness, уменьшая frequency/severity incidents.

Основной focus здесь — technology: monitoring/detection capabilities, system hardening, logging и infrastructure, необходимые investigation/response.

## CYBER THREAT INTELLIGENCE (CTI) CAPABILITIES

Cyber threat intelligence добавляет context, превращающий security data в actionable insight. Понимание threats против organization/industry позволяет IRT prioritise defenses, распознавать attack patterns и эффективнее respond.

CTI поддерживает incident response через proactive defense, detection enhancement, investigation context и prioritization.

### Таблица 9. CTI Capabilities for Incident Response

| Capability | Description |
|---|---|
| Proactive Defense | Intelligence emerging threats позволяет внедрять protections до materialization attack; при новой campaign targeting industry teams могут deploy detections и harden systems заранее. |
| Detection Enhancement | IOC из threat feeds интегрируются в detection systems для known malicious infrastructure, file hashes и behavioral patterns. |
| Investigation Context | Во время incidents threat intelligence помогает понять attacker motivations/tactics и определить, что искать при scoping; attribution может inform decisions и help predict behavior. |
| Prioritization | Threat intelligence помогает prioritise remediation по active exploitation и relevance environment. |

Threat intelligence можно получать из:

- commercial providers;
- industry ISACs;
- government sources, включая CISA/sector agencies;
- OSINT feeds/communities;
- internal intelligence из past incidents.

Разные sources дают разную coverage, поэтому useful комбинировать multiple feeds.

> Threat intelligence имеет ценность только если operationalized для organization и IRT. Нужны processes review incoming intelligence, assess relevance и take action. Intelligence, которую никто не читает, не даёт actionable security benefit.

### STANDARDIZED THREAT INTELLIGENCE WITH STIX

**Structured Threat Information eXpression (STIX)** — open standard для machine-readable cyber threat intelligence. Он позволяет consistent sharing/consumption threat data across platforms/tools. Если ISAC распространяет IOC или commercial feed отдаёт intelligence, STIX задаёт common data structure для automated ingestion/correlation.

STIX определяется OASIS Cyber Threat Intelligence Technical Committee (CTI TC); source указывает current version **STIX 2.1**, serialization JSON.[15]

Canonical source приводит пример STIX indicator malicious URL в spear-phishing campaign. Технический объект сохраняется verbatim:

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
  "created": "2025-12-31T14:30:00.000Z",
  "modified": "2025-12-31T14:30:00.000Z",
  "name": "Credential phishing URL",
  "description": "Malicious URL mimicking corporate login page",
  "indicator_types": ["malicious-activity"],
  "pattern": "[url:value = 'https://login-secure-verify.com/auth']",
  "pattern_type": "stix",
  "valid_from": "2025-12-31T14:30:00.000Z"
}
```

① `pattern` matches malicious URL.

Поле `pattern` использует **STIX Patterning Language**. Security tools с STIX support могут автоматически parse structure и создавать detection rules/blocklist entries. Это превращает raw intelligence в operational defense без manual intervention.

STIX 2.1 определяет множество object types. Domain objects включают threat actor identifiers, campaigns, intrusion sets, malware definitions, attack patterns, vulnerabilities и courses of action. Observable objects представляют artifacts investigations: IP addresses, domains, file hashes, email messages, network traffic, registry keys. Relationship objects связывают elements — например, threat actor с campaigns, malware и vulnerabilities.

Такая interconnected structure позволяет intelligence рассказывать целостную историю activity, а не давать isolated data points. STIX bundle новой ransomware campaign может дать analysts не только IOC, но и attacker tactics, targeted vulnerabilities и recommended defensive actions.

### CTI PLATFORMS

Без dedicated platform управление multiple feeds, correlation indicators и context over time усложняются. CTI platform даёт centralized environment для ingest, enrichment, analysis и sharing intelligence.

Она может aggregate commercial feeds, ISAC, government sources и internal investigations в единый repository, автоматически поддерживая relationships между threat actors, campaigns, indicators и vulnerabilities.

Во время active incident analysts могут:

- search intelligence по newly identified indicators;
- находить связи с known campaigns/threat actors;
- выявлять additional indicators для scoping.

Это превращает CTI из preparation activity в active investigation resource.

Platforms также дают trend visibility: какие threat actors наиболее active против sector, какие techniques растут в recent campaigns, какие infrastructure patterns повторяются. При новом incident analysts могут использовать накопленный intelligence, чтобы anticipate attacker next steps, prioritise systems для scoping и recommend containment, не начиная analysis с нуля.

Один из вариантов — **OpenCTI**. Community Edition — open-source/free, поддерживает STIX 2.1 ingestion, entity correlation и integration detection tools через connectors. Enterprise Edition добавляет collaborative workspaces, advanced analytics и role-based access controls.

### Рисунок 39. OpenCTI Platform Dashboard

`THIRD_PARTY_REVIEW_REQUIRED` — product screenshot не воспроизводится автоматически.

### Рисунок 40. OpenCTI Indicator Drill-Down

`THIRD_PARTY_REVIEW_REQUIRED` — product screenshot не воспроизводится автоматически.

CTI platforms вроде OpenCTI становятся особенно полезны по мере роста intelligence volume и потребности в correlation/context. Продолжение этой мысли следует в следующем canonical segment.

CTI platforms вроде OpenCTI дают valuable capabilities для management и operationalization threat intelligence. Smaller teams могут эффективно работать через spreadsheets или SIEM integrations, однако CTI platform становится всё ценнее по мере роста intelligence volume и важности correlation/context для incident response.

## SOFTWARE MANAGEMENT PROCESSES И PROCEDURES

Эффективное software management уменьшает attack surface. Особого внимания требуют пять областей: patch management, configuration management, software inventory, software supply-chain security и end-of-life management.

### PATCH, CONFIGURATION И INVENTORY

**Patch management** создаёт processes identification, testing и deployment security patches. Vulnerabilities выявляются через vendor advisories, scanning tools и threat intelligence feeds. Remediation следует prioritise по exploitability/asset criticality, ускоряя vulnerabilities under active exploitation. Patches нужно test до broad deployment и иметь exception handling для systems, которые нельзя patch сразу.

**Configuration management** поддерживает documented, version-controlled configurations. Во время incidents baselines помогают обнаружить unauthorized changes. При recovery documented configurations ускоряют restore known-good state, фиксируют dependencies/integration points для scoping и поддерживают rollback.

**Software inventory** отслеживает installed software и versions. Software Bill of Materials (SBOM) помогает выявить systems, затронутые vulnerability third-party component. Accurate inventory позволяет быстро найти affected systems при новой vulnerability.

> Formal inventory часто пропускает shadow IT: SaaS, cloud services и licenses, приобретённые вне approved procurement. Практический discovery method — review recurring billing statements и expense reports. Shadow services расширяют attack surface и создают gaps при scoping, особенно когда monitoring/hardening отсутствуют.

### SUPPLY CHAIN SECURITY И END-OF-LIFE

Modern software собирается из множества open-source libraries, third-party SDKs и developer packages. Каждая upstream dependency — дополнительная organization/maintainer/project, compromise которой может стать путём к downstream targets.

Source перечисляет vectors: compromise package repositories вроде NPM/PyPI, dependency confusion, typosquatting, compromise trusted maintainer accounts.[16] Один compromised component может распространяться через transitive dependencies по portfolio и затронуть systems, не использовавшие malicious package напрямую.

Supply-chain risk следует включать в software management. SBOM должен охватывать vendor-supplied applications. Для internal development source рекомендует pin known-good dependency versions через lock files/hash verification, использовать private registries/repository proxies и включать dependency scanning в build pipelines. Для vendor software следует оценивать их upstream dependency vetting и communication supply-chain incidents.

End-of-life management отслеживает software около или после vendor support date. Software без security updates создаёт ongoing risk. Нужны migration/replacement/compensating controls. Во время incidents EOL systems особенно вероятны как attack vector из-за permanently unpatched known vulnerabilities.

### PATCH MANAGEMENT AND PRIORITIZATION EFFORTS

Основной challenge patch management для многих organizations — prioritization. Monthly patch volume велик, а отставание накапливается: чем больше delay, тем сложнее catch up.

Canonical source приводит пример **CVE-2025-14847 “MongoBleed”**. В December 2025 vulnerability активно обсуждалась из-за exploitation in the wild. Source описывает её как unauthenticated vulnerability MongoDB, affecting releases вплоть до **MongoDB 3.6.0 (2017)**, позволяющую получить memory chunks через vulnerability в используемой MongoDB zlib library. На момент написания source указывает более **213,000 internet-exposed MongoDB instances** по данным Shodan.

### Рисунок 41. Shodan Results for Internet-Exposed MongoDB Instances

`THIRD_PARTY_REVIEW_REQUIRED` — screenshot/results visual не воспроизводится автоматически.

Source отмечает, что между vulnerability disclosure и availability public exploit **December 25, 2025** прошло лишь несколько дней.

### Рисунок 42. X Release of MongoBleed Exploit

`THIRD_PARTY_REVIEW_REQUIRED` — third-party social-media visual не воспроизводится автоматически.

Limited resources часто приводят к updates только при critical vulnerability. Старые MongoDB versions могут быть locally provisioned или embedded в third-party turnkey applications. При emergency значительные version jumps сложнее incremental updates.

Отложенное software management повышает цену critical vulnerabilities. Regular patch cycles, accurate inventory и established testing уменьшают cost/chaos emergency response; patch debt имеет compounding effect.

## SYSTEM HARDENING

System hardening уменьшает attack surface через removal unnecessary features, secure configuration и least privilege. Hardened systems сложнее compromise и они ограничивают attacker options после initial access.

Следует disable unnecessary services, удалить ненужные features и change/remove default accounts/credentials.

Нужно deploy endpoint controls для monitoring/alerting/blocking unauthorized access и forward logs central collection server. Logs hardened systems полезны при investigation.

Следует применять vendor security benchmarks, например CIS Benchmarks или DISA STIGs. Где возможно — application allowlisting для prevention execution unauthorized software.

### Рисунок 43. CIS Benchmark Checklist for HPE Aruba Networks Device

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний visual не воспроизводится автоматически.

> Hardened systems дают threat-hunting opportunity: attacker после compromise может disable controls. Отклонение system от hardened baseline может стать IOC.

Hardening configurations нужно document и automate where possible. Infrastructure-as-code обеспечивает consistency и упрощает rebuild during recovery. Для existing systems могут использоваться PowerShell или другие shell scripts. Baselines следует регулярно review/update.

## ENDPOINT-BASED SECURITY MONITORING И THREAT DETECTION

Endpoint Detection and Response (EDR) tools дают essential visibility host-based activities. EDR поддерживает proactive threat detection и incident investigation.

Product-specific labels различаются: Endpoint Detection and Response (EDR), Extended Detection and Response (XDR), Next-Generation Antivirus (NGAV), Endpoint Protection Platform (EPP). Далее source использует EDR как обобщённое обозначение.

EDR platforms собирают telemetry: process execution, file-system changes, registry modifications и network connections. Это позволяет behavioral detection suspicious patterns, включая process injection, credential dumping, anomalous usage и persistent-access tool deployment. Analysts могут query telemetry для hunting indicators по managed endpoints, а responders — remote isolate systems, terminate processes или collect evidence.

> Gaps EDR coverage создают visibility gaps. Third-party systems, legacy devices и cloud instances часто исключены из deployment. Coverage должна охватывать servers, workstations и cloud instances.

EDR effectiveness зависит от proper configuration и alert tuning. Detection rules нужно адаптировать к environment, снижая false positives без потери sensitivity. EDR alerts должны prompt review/investigation; delay даёт attacker дополнительное время.

### EDR AS A SUCCESS STORY

Автор пишет с позиции professional penetration tester: основная challenge — не initial access, а сохранение доступа достаточно долго для достижения objectives без detection/removal endpoint protection.

Common initial foothold techniques, например exploitation public-facing web apps или manipulation users, хорошо известны. Но persistence и lateral movement без detection стали существенно сложнее; даже novel internally developed techniques часто detect хорошо настроенные EDR solutions.

Source рассматривает это как genuine success: mature EDR deployments изменили economics attacks, сделав post-compromise activity expensive и risky. Organizations регулярно detect/disrupt intrusions, которые несколько лет назад были бы successful.

Attackers адаптировались: supply-chain compromises, cloud token theft и social engineering techniques, bypass endpoint protection, стали заметнее. Это evidence эффективности EDR, но одновременно reminder, что defense не должна быть static.

## SYSMON ДЛЯ ENHANCED WINDOWS TELEMETRY

System Monitor (Sysmon) — free tool Microsoft Sysinternals, расширяющий default Windows event logging high-fidelity telemetry.[17] Sysmon фиксирует process creation с full command line и parent process, network connections, file creation timestamps, registry modifications, driver/DLL loading.

Во время incidents Sysmon logs дают investigation-grade detail в Windows Event Log. Analysts могут reconstruct process chains, identify lateral movement через remote service activity и trace attacker tooling на compromised hosts.

Sysmon особенно полезен там, где EDR coverage incomplete: legacy systems, third-party-managed hosts, lab/dev environments. При наличии EDR он остаётся complementary independent telemetry source, доступным даже если attacker disable/evade EDR agent.

> Для organizations с существенной Windows environment и EDR gaps Sysmon — high-value preparation resource. Небольшие затраты на deployment/configuration могут значительно помочь IRT.

Sysmon value сильно зависит от configuration. Default config без filtering создаёт significant noise. **SwiftOnSecurity Sysmon configuration** source предлагает как curated community starting point, балансирующий noise reduction и detection coverage. Organization должна tune config: exclusions known-good activity и additional rules для org-specific needs. Events следует forward в central log collection для correlation/long-term retention.

Sysmon deployment хорошо сочетается с adversary simulation: после deployment/tuning следует run atomic tests против ATT&CK techniques relevant threat profile и verify expected telemetry в logs.

## NETWORK SECURITY MONITORING И THREAT DETECTION

Network monitoring даёт visibility communications между systems и external networks. Endpoint monitoring ограничен single host, тогда как network monitoring показывает traffic across environment. Это помогает detect C2, lateral movement traffic patterns и data exfiltration, которые host-based monitoring может пропустить.

Есть несколько complementary approaches с tradeoffs visibility, storage и analytical capability. Выбор зависит от needs, budget и technical capacity.

### FULL PACKET CAPTURE

Full Packet Capture (FPC) много лет считался gold standard. Organizations инвестировали в capture/storage complete traffic для retrospective analysis, threat hunting и incident investigation.

Но investment дорог: volume data перегружает analysts, transport encryption ограничивает value без decryption, а storage/processing cost растёт с bandwidth, device count и cloud/SaaS traffic.

### STRATEGIC PACKET CAPTURE

Для organizations, сохраняющих packet capture, source приводит practical guidance Phil Hagen по optimization.

После cost/resources основная проблема — encryption. Даже store-now-decrypt-later с acquired private key material осложняется Perfect Forward Secrecy (PFS) и emerging post-quantum cryptography. Поэтому strategy должна смещаться от capture-everything к traffic с immediate analytical value.

Source рекомендует:

- определить traffic, доступный через TLS-decrypting proxies;
- использовать Zero Trust platforms вроде Zscaler/Netskope для visibility на proxy-interception layer;
- deprioritize commonly encrypted traffic на ports **22 (SSH), 443 (HTTP over TLS), 993 (IMAP over TLS)**, где payload inspection мало полезен;
- для encrypted traffic, которое всё же сохраняется, рассмотреть truncation до **20–30 packets per socket**, сохраняя TLS negotiation metadata: certificates, cipher suites и ClientHello fingerprints, включая JA4+;
- при tighter constraints исключить encrypted traffic и обеспечить comprehensive NetFlow coverage.

Эти approaches могут откладываться из-за cost, complexity, sensitivity или legal reasons, но остаются valuable для limited use или targeted visibility во время active incident.

### NETWORK FLOW MONITORING

Network flow monitoring даёт summary network communications без storage burden FPC и подходит для long-term retention/broad deployment. Если FPC отвечает «что именно было передано», flow data отвечает «кто с кем говорил, когда и сколько» — часто этого достаточно для detection и initial investigation.

Flow record — unidirectional sequence packets с common attributes source, destination и protocol.

### Таблица 10. Common NetFlow Fields

| Field | Description |
|---|---|
| Source/Destination IP | IP addresses communicating hosts |
| Source/Destination Port | TCP/UDP ports identifying services |
| Protocol | TCP, UDP, ICMP и др. |
| Timestamps | Flow start/end для timeline analysis |
| Byte Count | Total bytes; полезно для detecting data exfiltration |
| Packet Count | Number packets; broad traffic patterns |
| TCP Flags | SYN, ACK, RST и др. |
| Interface/Direction | ingress/egress direction |

Metadata помогает identify anomalous communication, quantify transfer volumes, detect beaconing и trace lateral movement.

Source перечисляет Cisco NetFlow, IPFIX и sFlow.

> Flow data с routers/switches часто sampled — source приводит ratios **1:1000 packets or higher**, что пропускает часть traffic. Security-focused flow с firewalls обычно unsampled. Для router-generated flow необходимо verify sampling config и учитывать coverage gaps.

Cloud environments предлагают AWS VPC Flow Logs, Azure NSG Flow Logs и Google Cloud VPC Flow Logs. Несмотря на различие formats, core value — lightweight metadata без full packet capture cost.

### EXTENDED BERKELEY PACKET FILTER (eBPF)

eBPF развивается из original BPF, introduced early 1990s для packet filtering. eBPF превращает этот подход в general-purpose programmable framework для безопасного execution custom code внутри OS kernel.

eBPF programs работают в sandboxed virtual machine kernel; built-in verifier проверяет safety до execution. Это даёт deep visibility network connections, system calls, file operations и process execution без custom kernel modules или reboot. Low overhead полезен для continuous production monitoring.

Для incident response preparation eBPF-based tools могут generate flow data, capture connection metadata, inspect packet headers и наблюдать process behavior, file access patterns и privilege changes.

Open-source projects **Cilium, Falco и Tetragon** используют eBPF для network policy enforcement, runtime threat detection и security observability traditional/containerized environments.

Microsoft развивает **eBPF for Windows**.[18], расширяя framework за пределы Linux. Cross-platform adoption может дать unified observability network/host/container workloads.

### NETWORK DETECTION AND RESPONSE (NDR)

NDR platforms анализируют network traffic через behavioral analysis, signature detection и threat intelligence integration. Near-real-time processing и ML помогают выявлять anomalous patterns и known threat signatures, уменьшая manual burden и MTTD.

CTI integration позволяет использовать IOC commercial/free feeds, ISACs и government sources для detection communications with known malicious infrastructure, known C2 patterns и file transfers matching malware signatures.

Многие NDR поддерживают event correlation, объединяя host telemetry и network data для richer context.

Monitoring следует размещать на critical points: internet egress, network segment boundaries, connections to sensitive systems, а также North-South и East-West traffic, где может происходить lateral movement.

## INVEST IN DETECTION ENGINEERING

Развёртывание security monitoring tools — необходимый первый шаг, но сами tools дают value только при sustained detection engineering practice. Detection engineering — discipline проектирования, создания, testing и maintenance detection rules/logic, которые превращают raw telemetry в actionable insight. Без постоянной investment организации накапливают monitoring tools, генерирующие noise вместо insight.

> Monitoring tool без хорошо поддерживаемых detection rules — это дорогой log collector.

Detection engineering связывает endpoint, network и log monitoring capabilities. EDR даёт telemetry, но detection engineer пишет rules, обнаруживающие suspicious process relationships или unapproved credential access. SIEM ingests logs, но engineers создают correlation logic для lateral movement между sources. NDR анализирует traffic, но engineers определяют behavioral patterns, требующие analyst attention.

Effective detection engineering включает ongoing activities:

- **Rule development:** detection rules, tied specific attacker techniques, informed threat intelligence и mapped MITRE ATT&CK.
- **Testing and validation:** verification rule firing через adversary simulation tools, например Atomic Red Team.
- **Tuning:** снижение false positives через refinement logic и removal/revision rules без investigative value.
- **Coverage tracking:** mapping rules к ATT&CK matrix для coverage/gaps.
- **Lifecycle management:** retirement outdated rules, updates при environment changes, documentation intent/logic для maintainability.

Organizations, рассматривающие detection как one-time configuration, неизбежно отстают по мере adaptation attackers.

## THREAT HUNTING PROGRAM

Threat hunting дополняет automated detection: analysts proactively ищут threats, пропущенные rules/signatures. Вместо ожидания alerts analysts формулируют hypotheses о возможной attacker activity и исследуют telemetry.

Документированная program вместо ad hoc effort обеспечивает coverage по relevant threats и evidence diligence для regulator review.

Program обычно включает:

- **Hypothesis catalog:** maintained list hypotheses, tied MITRE ATT&CK tactics/techniques — например C2 beaconing, lateral movement via WMI, data staging unusual directories.
- **Target data sources:** logs/telemetry для каждой hypothesis — proxy logs, DNS queries, process creation events.
- **Cadence:** frequency review каждой hypothesis по risk/data freshness.
- **Audit trail:** data set с hypothesis, source, cadence, last-run date, analyst, findings для internal reviews/regulator inquiries.
- **Feedback loop:** promotion hunt findings в automated detection rules.

Начать можно с небольшого high-priority hypothesis set и расширять catalog по мере роста expertise. Documentation защищает investment от staff turnover: следующий analyst получает history/catalog и может продолжить работу.

## CATALOG ALL CRITICAL DATA, SYSTEMS, AND INFRASTRUCTURE

Comprehensive asset inventory ускоряет scoping и помогает обеспечивать appropriate protection critical systems. Если responders быстро знают, какие systems существуют, кто owner и как они связаны, scoping становится быстрее и точнее. Без inventory team тратит время и может пропустить unknown/forgotten assets.

### Таблица 11. Asset Inventory Categories

| Category | Elements to Document |
|---|---|
| Hardware Assets | Servers, workstations, network devices, mobile devices, IoT systems; location, owner, criticality |
| Software Assets | Applications, OS, middleware; versions, licensing, support status |
| Data Assets | Sensitive repositories, locations, classification, regulatory requirements |
| Cloud Resources | VMs, containers, storage, databases, cloud services |
| Network Architecture | Diagrams, IP schemes, VLAN assignments, firewall rules |
| Third-Party Connections | VPN, API integrations, data-sharing relationships |
| Critical Assets | Systems/services essential objectives: revenue, customer-facing, compliance |

В многих organizations эти categories принадлежат разным teams/systems: network engineering — diagrams/firewall; server/cloud teams — infrastructure inventory; business units — data assets/third-party relationships.

IRT должна иметь local copies для offline access во время incidents и relationships с authoritative source owners для current data. Local copy обеспечивает availability при compromised primary systems; authoritative source — актуальность при scoping/containment.

Systems имеют разную priority. Classification по business criticality помогает decision makers. Critical Assets должны быть identified заранее для priority scoping, containment, recovery.

Inventory должен поддерживать rapid querying. Spreadsheets подходят smaller environments; larger organizations — CMDB/asset management platforms с search/filter/integration. Inventory должен оставаться available даже если primary systems compromised.

> Asset inventory полезен только если accurate. Нужны automated discovery, change-management integration и periodic audits. Stale data может mislead responders.

## MONITOR THE ATTACK SURFACE

Asset inventory показывает то, что organization знает о своей environment; attackers target то, что organization exposes, и это не всегда совпадает. Attack Surface Monitoring (ASM) continuously discovers/evaluates accessible assets: internet-facing services, cloud resources, domains, certificates, distributed endpoints, exposed APIs и др.

Inventory отвечает: **what do we have?** ASM: **what can an attacker see?**

### THE MODERN ATTACK SURFACE

Canonical source приводит две прямые цитаты Ron Eddings и MJ Kaufmann из *Attack Surface Management*.[19]

`THIRD_PARTY_REVIEW_REQUIRED` — цитаты не переводятся и не воспроизводятся без отдельной проверки прав.

В окружающем авторском тексте source отмечает, что modern attack surface включает cloud environments, SaaS applications, APIs, mobile devices, IoT, AI infrastructure и third-party dependencies. Internal inventory может учитывать traditional IT и при этом пропускать cloud resources, SaaS integrations и vendor connections.

ASM tools помогают discover/monitor broad attack surface. Для IRT это особенно важно: assets, неизвестные в preparation, вероятно, будут пропущены и при scoping.

ASM обнаруживает externally accessible assets, которых нет internal inventory: forgotten dev servers, test environments с production data, acquired infrastructure, не integrated после acquisition, cloud resources outside standard change management.

> Assets, которых нет internal inventory, с высокой вероятностью не попадут в incident scope. ASM закрывает gap, обнаруживая exposures до attacker.

Для incident response preparation ASM даёт два benefits:

1. уменьшает likelihood incidents через discovery exposures до exploitation — например, newly exposed admin interface или expiring certificate customer-facing service;
2. улучшает scoping accuracy, давая current view accessible attack surface, который может отличаться от internal documentation.

Smaller teams могут начать с periodic external scanning open-source tools и compare inventory. Larger organizations — dedicated ASM platforms continuous monitoring/change alerting/vulnerability workflow integration. Results должны feed back в asset inventory/hardening, замыкая discovery→remediation loop.

## ASSESS SECURITY POSTURE THROUGH ADVERSARY SIMULATION

Security posture нельзя оценить только known vulnerabilities. Vulnerability scanning выявляет missing patches/misconfigurations, но не показывает, работают ли detection/response после initial access. Post-exploitation gaps — undetected lateral movement, missed credential harvesting, silent persistence — в scan results не появляются.

Adversary simulation тестирует full defensive chain from initial access through post-compromise activity.

### Рисунок 44. Adversary Simulation Risk Assessment Coverage

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Simulation проверяет, detect ли tools attack techniques на практике и способны ли response processes contain/remediate incident.

Формы и maturity:

- vulnerability scanning + configuration assessment security benchmarks;
- penetration testing для проверки exploitability;
- application security testing: static/dynamic/code review;
- adversary simulation и purple teaming для detection coverage known techniques;
- MITRE ATT&CK как structured catalog tactics/techniques.[20]
- Atomic Red Team как repeatable granular test cases individual ATT&CK techniques.[21]

Mature red team не обязателен: небольшой set atomic tests по relevant ATT&CK techniques уже показывает, даёт ли investment в detection tools результат.

Для continuous validation существуют Breach and Attack Simulation (BAS) platforms, scheduled automated attack scenarios production/near-production. BAS mimics threat actor behavior и проверяет detection/blocking каждого шага. Results map к actual control failures и формируют prioritized remediation.

> BAS меняет вопрос с «может ли эта attack succeed?» на «обнаружили и заблокировали ли её наши controls?». Это помогает prioritise demonstrated gaps вместо hypothetical risk.

BAS дополняет manual simulation/penetration testing, а не заменяет. Manual exercises дают human creativity/adaptability; BAS — continuous coverage между assessments. Detection engineering teams могут использовать BAS для validation rules и measure improvement.

Все findings должны feed back в patch/hardening; remediation progress track, persistent vulnerabilities escalate above acceptable risk.

### CVSS FOR VULNERABILITY PRIORITIZATION

Common Vulnerability Scoring System (CVSS), maintained FIRST, standardizes severity scoring **0–10**. Higher scores обычно используются для remediation prioritization.

CVSS 3.1 base score использует восемь metrics exploitability/impact. Source иллюстрирует их **CVE-2025-61882**, Oracle E-Business Suite vulnerability, base score **9.8**.

### Таблица 12. CVSS 3.1 Base Metrics for CVE-2025-61882

| Metric | Value | Meaning |
|---|---|---|
| Attack Vector | Network | Exploitable remotely over network |
| Attack Complexity | Low | No special conditions |
| Privileges Required | None | No prior access/credentials |
| User Interaction | None | No victim action |
| Scope | Unchanged | Impact limited vulnerable component |
| Confidentiality Impact | High | Complete loss confidentiality |
| Integrity Impact | High | Complete loss integrity |
| Availability Impact | High | Complete denial of service possible |

Комбинация network exploitation без privileges/user interaction и high impact по трём dimensions даёт critical **9.8**.

Но CVSS нельзя использовать как единственный basis prioritization. Critical vulnerability internet-facing system требует immediate attention; та же vulnerability isolated test environment может иметь lower priority. CVSS не учитывает deployed status, compensating controls или business criticality.

CVSS следует комбинировать с asset criticality, exposure и threat intelligence active exploitation.

**Exploit Prediction and Scoring (EPSS)** от FIRST оценивает probability exploitation in the wild. Если CVSS фокусируется на difficulty/impact, EPSS добавляет likelihood и дополняет vulnerability prioritization.

## COLLECT AND RETAIN LOGGING INFORMATION

Comprehensive logging — data foundation threat detection и incident investigation. Без adequate logs detection ограничена, а post-incident analysis может быть impossible.

Сначала нужно определить sources для central collection. Priority:

- authentication systems;
- security tools;
- critical servers;
- network devices;
- cloud platforms.

Systems должны capture security-relevant events: process creation with command-line Windows, successful/failed authentication, network connections и DNS queries where feasible.

### FEAR THE DARK: WHEN LOGS GO MISSING

Canonical source пересказывает guidance Heather Barnhart, SANS Institute Head of Faculty, о **dark periods** — временных gaps без reliable digital evidence.[22]

Причины, перечисленные source:

- misconfigured logging;
- default logging insufficient forensic detail;
- retention policies, deleting evidence too early;
- infrastructure changes creating coverage gaps;
- deliberate attacker log manipulation/destruction.

Source приводит examples 2022 Idaho murders investigation и 2025 Bybit cryptocurrency breach (с attribution APT38 и заявленным loss **$1.5 billion**) как иллюстрации evidence gaps.

`THIRD_PARTY_REVIEW_REQUIRED` — две прямые цитаты Heather Barnhart, включая формулировку о logging normal activity и “fear the dark”, не переводятся и не воспроизводятся.

Organizations должны establish baselines expected activity и обеспечивать logging sufficient context для distinction legitimate/malicious operations. Без complete logs даже skilled IRT сталкивается с preventable gaps.

Retention periods зависят от investigation needs, compliance и storage. Source указывает common range **90 days–1 year**, с возможностью longer retention для compliance/APT investigation.

Нужно разделять logs:

- **compliance retention:** regulatory/audit, можно хранить lower-cost archive/log management;
- **active detection/investigation:** требуют query/correlation performance SIEM.

Это позволяет reserve SIEM capacity для sources с active use cases.

> Logs следует защищать от tampering/deletion. Forward central collection promptly и применять access controls. Attackers часто пытаются delete/modify logs, чтобы скрыть activity.

### SIEM OR SINK?

SIEM aggregates logs, normalizes data и enables correlation. Properly operated SIEM valuable для detection/investigation.

Но без ongoing effort SIEM становится expensive log sink: logs ingest, но не review; alerts никто не investigates.

Effective SIEM требует:

- dedicated analysts;
- continuous tuning;
- regular coverage review;
- removal log sources без detection/investigation use cases;
- custom detections org-specific threats;
- integration incident response escalation.

До investment organization должна реалистично оценить willingness поддерживать ongoing resources. Хорошо managed log aggregation может быть полезнее underutilized SIEM.

## PREPARATION CHALLENGES

Effective preparation требует sustained effort в периоды без active incidents. Это создаёт challenges даже там, где важность preparation признаётся.

### Таблица 13. Preparation Challenges Summary

| Challenge | Impact |
|---|---|
| Resource Constraints | Operational demands оставляют мало времени preparation |
| Readiness Erosion | Skills atrophy/complacency during quiet periods |
| Documentation Drift | Plans/playbooks outdated as environment changes |
| Knowledge Loss | Institutional knowledge уходит с staff |
| Value Demonstration | Benefits трудно quantify |

Понимание challenges позволяет заранее создавать countermeasures.

### RESOURCE CONSTRAINTS

Preparation конкурирует с operational demands. Security teams обрабатывают alerts, manage tools, поддерживают business initiatives; update IR plan естественно уступает urgent vulnerability или suspicious alert.

Budget constraints — отдельный related challenge: training, forensic tools и exercises требуют funding и конкурируют с visible projects; ROI preparation трудно quantify.

> При management support preparation следует framing как risk reduction, а не optional enhancement. Где возможно, сравнивать estimated incident costs из industry data с относительно modest preparation investment.

Source начинает список подходов к resource constraints; продолжение находится в следующем canonical segment.

## ПРОДОЛЖЕНИЕ: RESOURCE CONSTRAINTS

Команды могут работать с resource constraints несколькими способами:

- **Приоритизировать high-impact activities.** Сосредоточиться на наиболее вероятных incident scenarios, самых critical systems и наиболее значимых capability gaps.
- **Использовать существующие meetings.** Проводить пятнадцатиминутные tabletop discussions или playbook reviews в рамках регулярных team meetings вместо отдельных preparation sessions.

### TURNING INCIDENTS INTO PREPARATION FUNDING

Для incident response team особенно неприятна ситуация, когда missing capability или underfunded tool были отмечены заранее, request месяцами лежал в backlog, а затем именно этот gap замедлил active response. Когда такое происходит, delay и его impact на incident timeline необходимо документировать.

После этого сам incident можно использовать, чтобы получить approval на исправление. Leadership следует сообщить, что team намерена закрыть gap во время response или сразу после него, и получить approval, пока стоимость отсутствующей capability ещё очевидна.

Decision makers, только что увидевшие, как missing tool/process замедлил реагирование, гораздо охотнее финансируют исправление, чем во время routine budget discussions. Incident budgets нередко покрывают remediation costs, которые в обычных условиях месяцами проходили бы procurement review; urgency active incident помогает преодолеть inertia, ранее блокировавшую request.

Даже modest preparation investments накапливаются со временем. Если организация выделяет только **два часа в неделю** на preparation activities, за год это составляет более **100 hours** подготовки и постепенно создаёт capabilities, которые становятся крайне ценными при incident.

## ПОДДЕРЖАНИЕ ГОТОВНОСТИ В СПОКОЙНЫЕ ПЕРИОДЫ

Длительные периоды без significant incidents создают парадокс: отсутствие incidents может означать, что cybersecurity controls и preparation работают, но одновременно уменьшает urgency, поддерживающую дальнейшие investment. Team members могут становиться complacent, если месяцами или годами не сталкиваются с incidents, требующими серьёзного response. Даже лучшие analysts теряют часть навыков без регулярной practice, особенно когда organizational attention переключается на более visible priorities.

Для снижения этого риска source рекомендует регулярную practice:

- **Monthly tabletop discussions:** короткие scenario walkthroughs для проверки decision-making и communication.
- **Quarterly technical drills:** hands-on exercises с forensic tools и evidence collection procedures.
- **Annual full-scale exercises:** comprehensive simulations с участием всех stakeholders.

Следует rotating team members между различными roles, чтобы развивать depth и избегать single points of failure. Analyst, который всегда выполняет evidence collection в drills, должен периодически отрабатывать coordination или communication roles. Team leads также следует иногда выполнять technical procedures, чтобы сохранять hands-on familiarity.

### INCIDENT RESPONSE INVESTIGATION CHALLENGES

Один из способов сохранять incident response skills — выделять время на continued professional development. Обычно это training courses или on-the-job work, но полезной альтернативой являются Capture the Flag (CTF) competitions. Они имитируют real-world incident scenarios и требуют анализировать logs, reverse-engineer malware и reconstruct attack timelines.

Competitive aspect привлекает многих participants, но может быть drawback для людей с imposter syndrome. Source рекомендует рассмотреть участие team members в CTF как group activity с focus на learning/collaboration вместо competition. Это развивает teamwork, knowledge sharing и confidence в investigative skills, напрямую применимых к incident response.

Source выделяет **SANS Skills Quest (SSQ)** как low-cost self-paced training с realistic scenarios для practical skills. Автор отдельно отмечает свой first-hand experience как contributor команды, разработавшей SSQ.

Другой вариант — бесплатные resources **Splunk Boss of the SOC**. Platform предлагает incident response и forensic investigation challenges. Хотя scenarios преимущественно ориентированы на Splunk users, они дают valuable practice general investigative skills, а предоставленное evidence часто можно анализировать и другими forensic tools.

### Рисунок 45. Splunk Boss of the SOC Platform

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний product/platform visual не воспроизводится автоматически.

## ПОДДЕРЖАНИЕ PLANS И PLAYBOOKS В АКТУАЛЬНОМ СОСТОЯНИИ

Organizational changes, technology updates и evolving threats могут быстро сделать preparation documents устаревшими. Incident response plan, завершённый шесть месяцев назад, может ссылаться на decommissioned systems, contacts с изменившимися roles и procedures, которые больше не соответствуют current tool capabilities.

Outdated documentation создаёт false confidence: responders считают, что у них есть guidance, хотя оно уже неверно.

Playbooks подвержены тому же drift. Ransomware playbook, созданный до adoption cloud infrastructure, может не содержать критичных containment steps. Procedures, предполагающие наличие external consulting contracts, становятся проблемой, если budget cuts или renegotiation уменьшили доступные resources.

Для борьбы с outdated documents организации должны устанавливать regular review cycles и назначать owner каждого preparation document:

- **Contact lists:** quarterly review с verification current information.
- **Playbooks:** каждый playbook exercise минимум один раз в год и отдельный review по смещённому schedule. Source рекомендует разнести exercise и review примерно на **шесть месяцев**, чтобы playbooks оставались validated/current в течение года. После каждого exercise или incident, где playbook использовался, его нужно update.
- **Policy documents:** annual reviews, aligned broader governance cycles.

Полезно создать annual exercise plan, mapping каждый playbook на scheduled exercise date. Такой plan помогает validate все playbooks в течение года и даёт auditors evidence structured review program.

Следует назначить конкретных людей responsible за current state документов и включить document review в performance expectations. Организации, рассматривающие documentation maintenance как ongoing discipline, а не periodic project, имеют более accurate/useful preparation materials. При incident responders могут доверять guidance.

## ORGANIZATIONAL CHANGE И TURNOVER

Personnel changes могут ослабить preparation, когда institutional knowledge уходит вместе с сотрудниками. Senior analyst, прошедший десятки incidents, знает не только documented procedures, но и реальное поведение systems, особенности stakeholders и разницу между тем, что works in theory и работает на практике. Replacement получает documents, но не весь nuanced context.

Turnover влияет и на relationships: legal counsel, HR partners и business unit leaders должны заново научиться доверять новым team members. Меняется response dynamics, communication patterns и role assignments.

### TABLETOP INJECT: SARAH’S DEPARTURE

Автор описывает tabletop exercise в крупной media company. Team демонстрировала strong decision-making и communication, но заметно зависела от IRT leader Sarah, обладавшей глубоким institutional knowledge.

Sarah работала в компании более десяти лет и провела её через несколько high-profile public incidents. Она знала key stakeholders, особенности systems и unwritten rules organizational incident response. Team сильно полагалась на её knowledge и relationships.

Через час двухчасового exercise автор ввёл следующий inject:

> «Sarah отправили выполнять обязанности присяжного, и до конца exercise она будет недоступна.»

Team отреагировала профессионально: Sarah отошла от участия и наблюдала. Secondary members попытались взять ответственность, но exercise быстро начал рассыпаться без её guidance. Decisions замедлились, communication ухудшилась, team потеряла cohesion, начала спорить и не смогла выполнить objectives.

CISO компании позже поблагодарил автора за наблюдение и признал риск over-reliance на одного человека. Sarah также назвала experience eye-opening: она знала, что хранит значительный institutional knowledge, но только наблюдение за struggle team сделало риск tangible.

После этого Sarah стала advocate cross-training, начала активно mentoring teammates по leadership skills и документировать unwritten knowledge, накопленное за годы.

Cross-training создаёт foundation turnover resilience:

- **Rotate responsibilities:** несколько team members должны уметь выполнять каждую critical function.
- **Document reasoning:** объяснять не только steps, но и почему определённые approaches работают.
- **Pair experienced and new responders:** во время exercises и, где возможно, actual incidents.

> Knowledge transfer следует начинать до departures. Exit interviews для undocumented knowledge и transition periods с job shadowing помогают сохранить institutional knowledge.

Полезно создавать knowledge repositories с lessons learned, incident post-mortems и informal guidance, иначе существующими только в памяти experienced responders. Такие repositories особенно ценны после changes team composition или при incident types, давно не встречавшихся.

## ДЕМОНСТРАЦИЯ ЦЕННОСТИ БЕЗ INCIDENTS

У preparation investments фундаментальная measurement problem: success означает incidents, которые не произошли, или impact, который не materialized.

Cybersecurity leaders сложно обосновывать preparation budget, когда основной benefit — avoided hypothetical future losses. Executives обоснованно спрашивают, что организация получила за investment, и ответ «у нас не было major incident» недостаточен.

Проблема усиливается в budget discussions, где preparation конкурирует с projects с tangible returns. Customer-facing feature может дать measurable revenue; updated incident response plan обещает risk reduction, которую сложно quantify.

Для демонстрации value независимо от actual incidents source предлагает track:

- **Exercise performance:** response times в drills и improvement trends между exercises.
- **Capability gaps addressed:** issues, identified exercises и затем remediated.
- **Detection improvements:** new detection rules, reduced false positives, MTTD в simulated scenarios.
- **Documentation currency:** percentage documents reviewed on schedule.

Tracking этих metrics со временем даёт tangible evidence progress и поддерживает budget/resource allocation decisions.

### BENCHMARKING PREPARATION INVESTMENTS

External reference points помогают обосновывать investment levels.

Canonical source приводит два industry data points:

- **SANS Institute 2025 SOC Survey:** **62%** SOC professionals считают, что их organization делает недостаточно для retention top staff, что подчёркивает importance training/development investments.[23]
- **Ponemon Institute 2025 Cybersecurity Threat and Risk Management Report:** **71%** organizations увеличивают cybersecurity budgets, а **51%** теперь consistently применяют incident response plans across enterprise.[24]

### Рисунок 46. SANS 2025 SOC Survey Key Findings

`THIRD_PARTY_REVIEW_REQUIRED` — сторонний survey visual не воспроизводится автоматически.

Кроме industry surveys source рекомендует использовать public incident case studies: когда breaches peer organizations попадают в news, показывать, какие controls отсутствовали и как existing preparation activities закрывают подобные gaps.

Value preparation трудно выразить точно, но organizations, consistently investing in readiness, реагируют эффективнее. Challenge не в отсутствии value, а в её communication stakeholders, принимающим resource decisions.

## ПРИМЕРЫ PREPARE ACTIVITY

Следующие examples иллюстрируют значение preparation.

### BUILDING THE BRIDGE BEFORE THE FLOOD

Dana присоединилась к **Meridian Financial** как incident response team lead восемь месяцев назад. Её predecessor сосредоточился на technical capabilities: впечатляющей forensic lab и advanced detection tools. Но в первый месяц Dana заметила тревожный gap: когда требовалась coordination с другими departments, она впервые представлялась людям, которые должны были быть близкими partners.

Dana начала системно строить relationships. Она организовала monthly meetings с Ron из IT operations, Rachel из Legal и Vincent из Human Resources. Каждый разговор обнаруживал coordination gaps:

- Ron сообщил, что team недавно мигрировала applications в cloud infrastructure, не уведомив security.
- Rachel рассматривала vendor breach notification как contract matter, не подключая incident response.
- Vincent сначала не понимал, зачем HR coordination с security, пока Dana не объяснила, что premature technical actions при insider investigation могут создать wrongful termination claims.

### Рисунок 47. Meridian Financial Incident Response Team Coordination

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Dana включила этих contacts в quarterly tabletop exercises по cross-functional coordination. Во время ransomware simulation:

- Ron обнаружил outdated vendor contact list;
- Rachel выяснила, что cyber insurance policy требует **24-hour breach notification**;
- Vincent понял, что termination procedures конфликтуют с evidence preservation requirements.

Каждый exercise выявлял gaps до того, как они могли negatively impact organization.

Через семь месяцев preparation доказала свою ценность. Security analyst обнаружил unusual data-access patterns пользователя **Thomas**, senior accountant с двенадцатилетним стажем. Pattern указывал на data staging для возможной exfiltration customer financial records.

Dana позвонила Vincent в течение нескольких минут. Благодаря established relationship ей не нужно было объяснять, кто она и почему HR должен участвовать.

Vincent сказал:

> «Нам нужно действовать осторожно. Thomas пользуется большим уважением. Если мы ошибаемся, это может повредить его репутации. Но если мы правы, нужно действовать до того, как уйдёт ещё больше данных.»

Vincent сообщил Dana, что Thomas недавно подал resignation notice с уходом через **две недели** — information, существенно изменившая risk calculation. Следующим звонком Dana связалась с Rachel, которая сразу увидела regulatory implications и дала guidance по evidence preservation для возможного law enforcement referral.

### Рисунок 48. Meridian Financial Coordinated Response Timeline

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

В течение **двух часов** Dana сформировала coordinated response plan. Team Ron незаметно отключила remote access Thomas, объяснив это «routine security update». Legal подготовил data hold notice. HR подготовил administrative leave documentation для немедленного применения, если investigation подтвердит malicious activity.

Investment Dana в relationships превратил potential crisis в coordinated action. Эти relationships были не просто professional courtesy — они стали foundation effective response, столь же важным, как forensic tools и detection systems.

### INTELLIGENCE-DRIVEN DETECTION

Isaac Morgan получил три недели на завершение integration threat intelligence feeds в NDR platform **Warren Health**. Healthcare organization была подписана на healthcare-specific ISAC feed; Isaac настроил NDR correlation network traffic с known IOC. Manager сомневался в оправданности времени, но Isaac понимал: detection без context — просто noise.

Integration была straightforward, но требовала careful tuning. Isaac mapped STIX indicators на NDR detection engine, focusing infrastructure threat actors, known targeting healthcare. Он настроил alerting thresholds, балансируя sensitivity и false positives, и test исторический traffic до production alerts.

### Listing 28. ISAC STIX Indicator for Velvet Tempest C2 Infrastructure

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--8f43b2e1-6d9a-4c5b-b8e7-3f2a1d9c4e6b",
  "created": "2026-01-13T08:15:00.000Z",
  "modified": "2026-01-13T08:15:00.000Z",
  "name": "Velvet Tempest C2 Infrastructure",
  "description": "IP address hosting C2 for ransomware targeting healthcare",
  "indicator_types": ["malicious-activity"],
  "pattern": "[ipv4-addr:value = '165.227.88.15']",
  "pattern_type": "stix",
  "valid_from": "2026-01-13T08:15:00.000Z"
}
```

Через три недели после completion integration Isaac получил alert, оправдавший effort.

NDR обнаружил outbound connections с workstation billing department на IP, связанный с **Velvet Tempest**, threat actor group, известной ransomware attacks against healthcare. ISAC опубликовал indicator только **36 hours** ранее на основе activity другого healthcare provider.

Isaac открыл alert в **AC-Hunter**, network threat detection platform. Connections происходили периодически — каждые **four hours**, что соответствовало C2 beaconing. Без CTI integration traffic выглядел бы как routine HTTPS к uncategorized external host. Threat intelligence context сразу показал severity.

### Рисунок 49. Velvet Tempest C2 Detection Alert

`THIRD_PARTY_REVIEW_REQUIRED` — visual alert/platform screenshot не воспроизводится автоматически.

В течение **одного часа** IRT изолировала workstation и начала forensic analysis. Investigation показала, что billing specialist два дня назад открыла malicious attachment phishing email. Malware создал persistence, но ещё не успел move laterally или получить access patient data.

Early detection благодаря CTI integration превратил потенциальный ransomware incident в contained compromise. Preparation Isaac окупилась в avoided downtime, preserved patient data и incident costs, которые не materialized.

## PREPARE: STEP-BY-STEP

Следующие steps представляют condensed reference preparation activities. Каждый step соответствует темам, рассмотренным ранее в этой главе.

## PREPARE: STEP-BY-STEP

Этот step-by-step guide суммирует темы, рассмотренные ранее в Chapter 7, и предназначен для использования при создании organizational readiness, обучении incident response team и усилении proactive defenses.

Source указывает, что guide доступен для download в PDF и Markdown formats на companion website `dynamicincidentresponse.com`.

### Step 1. Prepare the Organization

1. Разработать organizational policies, описывающие подход организации к incident response, включая:
   - mission компании и цели incident response program;
   - priorities до, во время и после incident;
   - policy по вовлечению management teams, включая GRC, legal и public relations;
   - policy по ransom/extortion payment;
   - policy по communication with attackers;
   - policy по data retention и evidence preservation;
   - policy по reporting incidents law enforcement, government или industry partners;
   - policy по public disclosure;
   - policy по engaging third-party incident response providers;
   - containment authorization policies с tiered authorization levels:
     - SOC/IRT-authorized actions вроде endpoint isolation;
     - service-owner-authorized actions вроде server/service isolation;
     - executive-authorized actions вроде shutdown production systems или действий, затрагивающих regulated services;
   - Recovery Time Objectives (RTO) и Recovery Point Objectives (RPO) critical systems;
   - evidence retention requirements и chain-of-custody procedures.

2. Развить management support для incident handling capability:
   - сформировать relationships с decision makers до incidents;
   - показывать value incident response через industry examples и metrics;
   - получать management input при разработке policies;
   - определить communication expectations during incidents;
   - назначать management actionable responsibilities — например, tabletop exercises или breach simulations.

3. Определить critical assets и risk assessment processes:
   - выявить systems/services, essential для survival organization, включая revenue-generating operations, customer-facing services и regulatory compliance systems;
   - определить risk tolerance thresholds для low/medium/high/critical events;
   - разработать incident classification criteria на основе systems affected, data sensitivity, business impact и regulatory implications;
   - документировать classification matrix для rapid reference;
   - пересматривать criteria ежегодно.

4. Разработать incident communications plan, включающий channels, contacts, reporting и emergency messaging:
   - создать secure/reliable primary communication platform;
   - определить backup communication channel на случай compromise primary;
   - периодически test communication channels;
   - документировать platform access procedures;
   - документировать internal/external/vendor/cloud contacts;
   - пересматривать contacts quarterly;
   - определить reporting requirements по incident severity;
   - создать report templates для разных audiences;
   - установить SLA initial/ongoing reports;
   - документировать distribution lists;
   - определить notification triggers;
   - установить approval workflows internal/external communications;
   - создать message templates common scenarios;
   - определить constituent audiences;
   - определить distribution channels;
   - назначить и обучить spokespersons;
   - документировать applicable notification requirements, включая GDPR, HIPAA, SEC, PCI DSS, NIS2, DORA и applicable breach-notification laws;
   - опубликовать `security.txt` по RFC 9116 с contact/encryption/disclosure-policy information;
   - документировать internal routing external security disclosures к security team.

5. Создать incident response team:
   - определить team structure и roles;
   - назначить primary/backup personnel;
   - документировать escalation paths и decision authority;
   - определить team activation procedures.

6. Выбрать incident tracking platform:
   - подобрать platform по size/needs;
   - настроить incident categorization/prioritization;
   - определить access controls/retention policies;
   - обучить team работе с platform.

7. Учесть cyber insurance requirements:
   - получить и review policy вместе с IR team;
   - определить notification timelines, pre-approval requirements, vendor restrictions;
   - попытаться включить preferred IR firms в approved vendor panel;
   - добавить policy owner в IRT contacts и tabletop exercises;
   - обеспечить offline access к policy, carrier contacts, claims phone, policy number и procedures engagement approved IR providers;
   - защитить policy от disclosure attacker-accessible systems и ransom negotiations;
   - определить independent legal counsel отдельно от carrier breach coach.

8. Реализовать security awareness training:
   - создать content по incident recognition/reporting;
   - определить training frequency и completion tracking;
   - использовать practical exercises, включая simulated phishing;
   - создать ясные reporting channels suspicious activity.

### Step 2. Prepare the Incident Response Team

1. Обучить IRT:
   - technical skills: SOAR, digital forensics, network analysis, malware analysis, log analysis, scripting, automation;
   - soft skills: communication, documentation, decision-making under pressure, leadership, negotiation;
   - incident response procedures/playbook execution;
   - company policies/escalation procedures;
   - ongoing training.

2. Разработать и validate backup/recovery procedures:
   - документировать backup architecture/coverage;
   - проверить ransomware resilience: immutable, air-gapped, separate authentication;
   - реализовать backup integrity monitoring/failure notifications;
   - test restoration procedures against RTO/RPO;
   - документировать backup access procedures для incident response.

3. Развивать relationships с essential personnel:
   - определить contacts в IT operations, SOC, help desk, legal, HR, public relations, business units;
   - при необходимости создать RACI matrix;
   - привлекать essential contacts к exercises/preparation;
   - определить communication preferences/escalation;
   - поддерживать relationships через regular interaction.

4. Разрабатывать playbooks common incidents:
   - определить наиболее вероятные incident types;
   - создавать detailed actionable procedures;
   - включать decision points, tool references, communication triggers;
   - review/update после exercise или incident.

5. Подготовить resources:
   - forensic workstations, включая cloud-based там, где relevant;
   - evidence collection tools;
   - secure evidence storage достаточной capacity;
   - jump bag для on-site response.

6. Подготовить access:
   - break-glass accounts с hardware tokens/credential vault, alerting и periodic testing;
   - access request procedures;
   - pre-authorize access where possible;
   - vendor/cloud provider support procedures.

7. Проводить tabletop exercises и drills:
   - monthly tabletop discussions;
   - quarterly technical drills;
   - annual full-scale exercises combining tabletop + technical execution;
   - realistic scenarios;
   - participants from all relevant departments;
   - test authorization levels/containment decisions;
   - rotate roles;
   - document findings и track improvements.

8. Поддерживать preparation documentation:
   - quarterly contact reviews;
   - каждый playbook exercise минимум раз в год + отдельный review по offset schedule;
   - annual policy review;
   - annual exercise plan mapping playbooks to dates;
   - назначить owners и включить document review в performance expectations.

### Step 3. Proactive Prevention and Detection

1. Реализовать CTI capabilities:
   - commercial, ISAC, government, OSINT sources;
   - process review/operationalization intelligence;
   - integrate IOC в detection systems через STIX 2.1;
   - использовать intelligence для prioritization;
   - оценить CTI platforms для centralized management/correlation/investigation pivots.

2. Разработать software management:
   - risk-based patch management;
   - configuration management/version control;
   - software inventory/version tracking;
   - SBOM;
   - shadow IT discovery через billing/expense review;
   - EOL tracking и migration/compensating controls;
   - exception handling для systems, которые нельзя patch.

3. Применять system hardening:
   - disable unnecessary services/default credentials;
   - CIS/DISA STIG benchmarks;
   - endpoint controls + central log forwarding;
   - application allowlisting where feasible;
   - automate через IaC/scripts;
   - review/update baselines;
   - monitor configuration drift;
   - document exceptions/compensating controls.

4. Реализовать endpoint monitoring:
   - deploy EDR across servers/workstations/cloud instances;
   - tune detection rules;
   - alert review/investigation processes;
   - enable isolation/evidence-collection response capabilities.

5. Deploy enhanced endpoint telemetry там, где EDR coverage insufficient:
   - supplemental telemetry agent;
   - community-maintained baseline config + tuning;
   - forward telemetry centrally;
   - validate capture через adversary simulation.

6. Реализовать network security monitoring:
   - monitoring at egress/segment boundaries;
   - detection rules;
   - north-south и east-west visibility;
   - alert review/investigation.

7. Инвестировать в detection engineering:
   - rules tied attacker techniques и mapped MITRE ATT&CK;
   - test/validate через adversary simulation;
   - tune false positives;
   - track coverage ATT&CK matrix;
   - lifecycle management rules.

8. Создать threat hunting program:
   - hypothesis catalog tied ATT&CK;
   - data sources;
   - cadence;
   - audit table с last-run/analyst/findings;
   - promote findings to automated detections.

9. Каталогизировать critical data/systems/infrastructure:
   - hardware/software/data/cloud/third-party connections;
   - identify critical assets;
   - business criticality classification;
   - network architecture/dependencies;
   - local offline copies + authoritative sources;
   - inventory-accuracy processes.

10. Monitor attack surface:
    - continuous discovery internet-facing services/cloud/domains/certificates/APIs;
    - compare against internal inventory;
    - feed ASM findings into hardening/vulnerability management;
    - evaluate ASM tools.

11. Assess security posture через adversary simulation:
    - vulnerability scanning/config assessment;
    - penetration/application security testing;
    - adversary simulation/purple teaming with MITRE ATT&CK и Atomic Red Team;
    - prioritize remediation using CVSS + EPSS + asset criticality + exposure + active exploitation intelligence;
    - evaluate BAS platforms;
    - track remediation и escalate persistent vulnerabilities above risk thresholds.

12. Collect and retain logging information:
    - identify critical log sources;
    - capture security-relevant events;
    - define retention periods для investigation/compliance;
    - separate active-detection logs и compliance archive;
    - reserve SIEM capacity для active use cases;
    - remove log sources without detection/investigation use cases;
    - protect logs от tampering и centralize collection.

## Сноски и источники

[1] European Union, "Directive (EU) 2022/2555 on Measures for a High Common Level of Cybersecurity Across the Union (NIS2)," December 2022, `www.nis-2-directive.com/`

[2] European Union, "Regulation (EU) 2022/2554 on Digital Operational Resilience for the Financial Sector (DORA)," January 2023, `www.digital-operational-resilience-act.com/`

[3] ISO/IEC 27001:2022, "Information security, cybersecurity and privacy protection — Information security management systems — Requirements," International Organization for Standardization, `www.iso.org/standard/27001`

[4] CISA, "National Cyber Incident Scoring System," `www.cisa.gov/sites/default/files/2023-01/cisa_national_cyber_incident_scoring_system_s508c.pdf`

[5] InvGate, "ITIL Priority Matrix: How to Use it for Incident, Problem, Service Request, and Change Management," `blog.invgate.com/itil-priority-matrix`

[6] Security.txt Project, `securitytxt.org/`

[7] PCI Security Standards Council, "Responding to a Cardholder Data Breach," `listings.pcisecuritystandards.org/documents/Responding_to_a_Cardholder_Data_Breach.pdf`

[8] European Union, NIS2, December 2022, `www.nis-2-directive.com/`

[9] European Union, DORA, January 2023, `www.digital-operational-resilience-act.com/`

[10] European Union, "Regulation (EU) 2024/2847 ... (Cyber Resilience Act)," October 2024, `eur-lex.europa.eu/eli/reg/2024/2847/oj`

[11] Keierleber, Mark, "PowerSchool Paid Off Hackers After Huge Breach — Now They’re Extorting Districts," The 74 Million, May 2025, `www.the74million.org/article/powerschool-paid-off-hackers-after-huge-breach-now-theyre-extorting-districts/`

[12] MITRE ATT&CK, `attack.mitre.org/`

[13] Travelers, "What Is a Data Breach Coach?" `www.travelers.com/resources/business-topics/cyber-security/what-is-a-data-breach-coach`

[14] Wilson Elser, "States Enact Safe Harbor Laws that Provide Affirmative Defenses in Data Breach Litigation," `www.wilsonelser.com/publications/states-enact-safe-harbor-laws-that-provide-affirmative-defenses-in-data-breach-litigation`

[15] OASIS Cyber Threat Intelligence Technical Committee, "Introduction to STIX," `oasis-open.github.io/cti-documentation/stix/intro`

[16] GitLab, "GitLab discovers widespread npm supply chain attack," `about.gitlab.com/blog/gitlab-discovers-widespread-npm-supply-chain-attack/`

[17] Sysinternals Suite, `learn.microsoft.com/en-us/sysinternals/`

[18] Microsoft, "eBPF for Windows," `github.com/microsoft/ebpf-for-windows`

[19] Eddings, Ron and Kaufmann, MJ, *Attack Surface Management: Strategies and Techniques for Safeguarding Your Digital Assets*, Function, 2024.

[20] MITRE ATT&CK, `attack.mitre.org/`

[21] Atomic Red Team - Library of Tests Mapped to the MITRE ATT&CK Framework, `github.com/redcanaryco/atomic-red-team`

[22] Barnhart, Heather, "Fear the Dark: How Dark Periods Are Threatening Forensic Investigations," SANS Institute White Paper, 2025, `www.rsaconference.com/-/media/project/rsac/rsac-website/reports/white-paper_rsac_sans_fear-the-dark.pdf`

[23] SANS Institute, "2025 SOC Survey," `www.sans.org/white-papers/sans-2025-soc-survey`

[24] Ponemon Institute and Optiv, "2025 Cybersecurity Threat and Risk Management Report," `www.optiv.com/insights/discover/downloads/2025-cybersecurity-threat-and-risk-management-report`
