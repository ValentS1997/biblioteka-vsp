---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 20
source_title: "Integrating DAIR with NIST CSF 2.0"
source_pdf_page_range: "637-648"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0637:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0648:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Third-party figures, quoted report text, screenshots, and external materials remain fail-closed where marked."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "CSF 2.0 and NIST SP 800-61 Revision 3 identifiers preserved."
  - "DAIR-to-CSF mappings and compliance artifact structure preserved."
---

# Глава 20. Интеграция DAIR с NIST CSF 2.0

Организации, работающие в условиях regulatory requirements, government contracts или industry mandates, сталкиваются с двойной задачей: необходимо одновременно демонстрировать compliance с established frameworks и эффективно реагировать на реальные incidents.

Для многих организаций, особенно US federal agencies и critical infrastructure operators, NIST SP 800-61 Revision 3 и Cybersecurity Framework (CSF) 2.0 определяют требования к incident response.[1]

Dynamic Approach to Incident Response (DAIR) предоставляет tactical methodology, необходимую для operationalization требований CSF 2.0 при сохранении practical effectiveness incident response.

Эта глава показывает, как DAIR activities сопоставляются с CSF 2.0 functions. Compliance и operational effectiveness не являются взаимоисключающими целями.

Организации могут:

- выполнять audit requirements;
- формировать необходимую documentation;
- демонстрировать control effectiveness;
- при этом использовать dynamic подход DAIR для более полного handling incidents, чем позволяют linear models.

Интеграция DAIR и CSF 2.0 создает practical framework, где compliance достигается через effective response activities, а не существует как отдельная administrative burden.

# Понимание NIST SP 800-61 R3 и CSF 2.0

NIST SP 800-61 Revision 3 существенно меняет место incident response внутри cybersecurity program.

Revision 2 предоставлял specific incident-handling procedures и four-phase lifecycle.

Revision 3 рассматривает incident response как integrated component enterprise cybersecurity risk management.

Это отражает важный сдвиг: effective incident response не может существовать как isolated function.

Response capabilities зависят от и одновременно влияют на:

- governance decisions;
- asset identification;
- protective controls;
- detection mechanisms;
- recovery planning.

CSF 2.0 описывает эти взаимозависимости через шесть core functions.

# Шесть функций CSF

## Govern (GV)

Govern задает organizational context для cybersecurity activities.

Включает:

- cybersecurity risk management strategy;
- expectations;
- policy;
- communication и monitoring этих элементов across organization.

Для incident response Govern определяет:

- severity thresholds;
- escalation procedures;
- allocation response resources;
- integration incident handling с enterprise risk management.

Compliance демонстрируется через documentation того, как response decisions соответствуют organizational risk tolerance и strategic objectives.

## Identify (ID)

Identify требует понимания текущих cybersecurity risks.

Включает awareness:

- assets;
- vulnerabilities;
- threats;
- potential business impacts.

Effective incident response зависит от знания:

- какие systems critical;
- какие data требуют protection;
- как systems interconnect.

Identify также включает threat intelligence, влияющий на detection strategy и response priorities.

## Protect (PR)

Protect охватывает safeguards, управляющие cybersecurity risks до incidents.

Хотя функция в основном preventive, protective controls напрямую влияют на response через:

- attack surface;
- available evidence sources;
- recovery options.

Полезные controls для IR:

- network segmentation;
- access management;
- data protection mechanisms.

Они ограничивают incident scope и помогают сохранять forensic artifacts.

## Detect (DE)

Detect охватывает capabilities для поиска и анализа cyber attacks и compromises.

Функция соответствует ранним stages incident response:

- monitoring;
- alerting;
- initial analysis.

Она превращает security events в actionable incident reports.

Detection capabilities определяют:

- насколько быстро incident обнаружен;
- сколько context доступно responders на старте.

## Respond (RS)

Respond охватывает actions после обнаружения incident.

Основные activities:

- analysis;
- containment;
- eradication;
- communication.

CSF 2.0 прямо признает необходимость iterative response, который адаптируется к новой информации.

## Recover (RC)

Recover фокусируется на restoration assets и operations.

Включает:

- restoring system availability;
- rebuilding stakeholder trust;
- implementing improvements для предотвращения recurrence;
- post-incident lessons learned;
- resilience improvement.

Эти шесть functions формируют структуру, через которую организации демонстрируют maturity и compliance incident response capability.

# Что требует Compliance

## Таблица 60. Требования CSF 2.0 к Incident Response Compliance

| Requirement | Description |
|---|---|
| Documented Capabilities | Организация документирует IR capabilities по relevant CSF functions: detection methods, response procedures, decision authority, external coordination |
| Demonstrated Effectiveness | Организация показывает, что capabilities реально работают через exercises, tabletop scenarios или actual incidents |
| Metrics and Measurement | Устанавливаются baselines для detection time, response time, containment effectiveness, recovery duration |
| Continuous Improvement | Lessons learned, procedure updates и root-cause remediation должны приводить к улучшениям |

Основная проблема — bridge между compliance requirements и practical incident response operations.

CSF 2.0 дает strategic framework, но требуется tactical methodology.

# DAIR как Implementation CSF 2.0

DAIR предоставляет tactical methodology для выполнения требований CSF 2.0.

DAIR activities напрямую сопоставляются с CSF functions, формируя practical implementation path.

Когда организации внедряют effective IR practices, compliance часто становится естественным результатом. CSF 2.0 codifies то, что experienced practitioners уже делают, а DAIR formalizes эти practices и облегчает demonstration compliance.

# Mapping DAIR Activities to CSF Functions

Figure 200 показывает alignment шести CSF functions с DAIR structure.

### Рисунок 200. DAIR Model Mapped to NIST CSF 2.0 Functions

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

## Таблица 61. DAIR Activities Mapped to CSF 2.0 Functions

| CSF Function | DAIR Activities | How DAIR satisfies requirements |
|---|---|---|
| Govern (GV) / Identify (ID) | Decision Maker coordination throughout all activities | Координация с Decision Maker связывает response с organizational risk tolerance и critical asset/business context |
| Protect (PR) | Prepare | Prepare включает proactive controls, response readiness, detection capability deployment, forensic readiness, training |
| Detect (DE) | Detect, Verify, Triage | Detect обнаруживает events; Verify подтверждает incidents; Triage prioritizes по organizational impact |
| Respond (RS) | Response Actions Loop: Scope, Contain, Eradicate, Recover | Iterative loop адаптирует response к новым findings и формирует evidence comprehensive handling |
| Recover (RC) | Recover, Debrief | Recover восстанавливает systems; Debrief фиксирует lessons learned и improvement opportunities |

Эта mapping показывает, что организации, уже использующие DAIR, выполняют activities, соответствующие требованиям CSF 2.0.

Остается документировать их так, чтобы compliance была видима assessor/auditor.

# Value of Iterative Response for Compliance

Iterative Response Actions Loop особенно полезен для CSF 2.0 compliance.

Linear models могут создавать впечатление process failure, если:

- remediation приходится повторять;
- после containment обнаруживается новый scope;
- нужно возвращаться к предыдущим фазам.

DAIR рассматривает iteration как expected и appropriate behavior.

Каждый loop:

- увеличивает thoroughness;
- добавляет remediation effort;
- генерирует новые evidence artifacts.

Iteration count можно показывать как positive metric, а не признак failure.

При documentation iterations необходимо записывать:

- какая new information запустила следующий cycle;
- какое дополнительное remediation было выполнено.

Это превращает iteration в evidence adaptive и considered response.

Для audit это важно: extended response periods и multiple remediation attempts могут быть объяснены как intentional DAIR behavior.

Каждый cycle:

- incorporates new information;
- appropriately expands scope;
- improves overall response effectiveness.

# Decision Maker Integration и Govern Function

DAIR emphasis на Decision Maker coordination соответствует Govern function на протяжении всего lifecycle.

Assessors ожидают evidence, что IR decisions отражают enterprise risk management strategy на практике.

Decision Makers участвуют не только в начале или конце incident.

Они дают ongoing guidance по:

- scope expansion;
- containment approach;
- acceptable operational impacts;
- recovery priorities.

Эта continuous coordination формирует records, напрямую относящиеся к CSF Govern categories.

## Таблица 62. DAIR Activities Mapped to CSF 2.0 Govern Categories

### GV.OC — Organizational Context

Assessor ожидает documentation того, что response decisions учитывают:

- regulatory obligations;
- stakeholder expectations;
- risk appetite;
- business environment.

DAIR artifacts:

- risk classification framework;
- triage decision records;
- regulatory notification trigger log.

### GV.RM — Risk Management Strategy

Нужно evidence, что residual risk при closure:

- formally assessed;
- accepted authorized individual;
- возвращается в enterprise risk register.

DAIR artifacts:

- signed loop-exit risk acceptance;
- debrief report с risk register recommendations;
- recovery metrics/trend data.

## Продолжение таблицы 62. Govern Categories

### GV.RR — Roles, Responsibilities, and Authorities

Assessor ожидает defined authority matrix для incident response, включая:

- incident declaration;
- command authority;
- business-impact decisions;
- loop exit;
- ownership post-incident improvements.

Нужны named roles, а не generic titles.

DAIR activities:

- Prepare;
- incident response team structure;
- RACI matrix;
- escalation thresholds;
- documented decision authority.

Artifacts:

- incident response authority matrix;
- escalation procedure documentation;
- named role assignments по incident type или severity tier.

### GV.PO — Policy

Нужны documented cybersecurity policies, отражающие organizational context.

Incident response documentation должна различать:

- policy — что должно происходить;
- procedure — как это происходит;
- playbook — как это происходит для specific scenario.

DAIR activities:

- incident response plan;
- playbooks;
- communication plan;
- contact lists;
- callout rosters.

Artifacts:

- incident response policy;
- procedure documents по DAIR phase;
- scenario-specific playbooks;
- communication plan с last-reviewed timestamp.

### GV.SC — Supply Chain Risk Management

Assessor ожидает evidence, что:

- third-party/supplier IR obligations определены;
- contractual notification requirements mapped;
- supplier access revocation включен в procedures.

DAIR activities:

- Prepare: supplier incident obligations, data processing agreement review, third-party access inventory;
- Scope/Contain: third-party access revocation;
- Debrief: supplier-related root cause и remediation tracking.

Artifacts:

- supplier IR obligations register;
- DPA/contract review records;
- third-party access revocation log;
- post-incident supplier remediation tracking.

Организация может демонстрировать Govern compliance через artifacts из таблицы и связывать их с конкретными incident records.

Такой category-level documentation показывает, что incident response встроен в enterprise risk management framework.

# Meeting Compliance Through DAIR Activities

Effective incident response естественным образом генерирует значительный объем documentation.

При использовании DAIR эту documentation можно структурировать под compliance requirements без создания отдельного administrative process.

Главная задача:

- распознать compliance artifacts, уже возникающие в DAIR operations;
- оформить их в ожидаемом assessment format.

# Compliance Artifacts from DAIR Activities

Assessors требуют tangible evidence того, что IR capabilities:

- существуют;
- работают как задумано;
- улучшаются со временем.

Если evidence не представлено, возможны compliance gaps даже при фактически сильной operational capability.

Каждый DAIR waypoint генерирует documentation, пригодную для compliance.

## Таблица 63. Compliance Artifacts by DAIR Phase

| DAIR Phase | Artifacts Generated | CSF Function |
|---|---|---|
| Prepare | Incident response plans, playbooks, contact lists, training records, CSF cross-references | Protect (PR) |
| Detect / Verify / Triage | Alert logs, monitoring dashboards, threat intelligence reports, triage decisions, false-positive records, incident declaration | Detect (DE) |
| Response Actions Loop | Scoping analysis, containment decisions, eradication records, recovery verification; artifacts accumulate across iterations | Respond (RS) |
| Debrief | Lessons learned, root cause analysis, improvement recommendations, implementation tracking | Recover (RC) |
| Decision Maker coordination | Stakeholder consultation records, guidance, business impact assessments, risk-aligned decision rationale | Govern (GV) / Identify (ID) |

Artifacts накапливаются естественно.

Каждая iteration Response Actions Loop увеличивает evidence base.

Tracking implementation of debrief recommendations дополнительно показывает program maturation.

Важно документировать не только actions, но и rationale decision-making.

# Demonstrating Control Effectiveness

CSF 2.0 требует показать, что controls работают, а не просто существуют.

DAIR дает возможность продемонстрировать effectiveness через actual incident handling.

## Таблица 64. Control Effectiveness Evidence by CSF Function

| CSF Function | Evidence of Effectiveness | DAIR Source Activities |
|---|---|---|
| Detect (DE) | Incidents обнаруживаются monitoring/alerting, а не external notification; MTTD дает quantitative evidence | Detect, Verify, Triage |
| Respond (RS) | Containment ограничил scope, eradication удалил attacker presence, iteration обработала дополнительные findings | Response Actions Loop |
| Recover (RC) | Systems успешно restored, integrity validated, improvements implemented | Recover, Debrief |

Каждая iteration Response Actions Loop усиливает evidence эффективности, поскольку показывает adaptation к новым findings.

# Satisfying Audit Requirements

Audit/assessment обычно включает:

- document review;
- interviews;
- evidence examination.

Организациям с DAIR следует:

1. поддерживать organized documentation;
2. обучить response personnel объяснять DAIR concepts в CSF 2.0 terminology.

Incident documentation следует организовать в alignment с CSF functions.

Auditors часто строят assessment по CSF categories/subcategories, поэтому такой же structure уменьшает assessment friction.

DAIR activities должны быть cross-referenced с CSF functions в plans и procedures.

Personnel должны уметь объяснять:

- Detect + Verify/Triage как detection capability;
- Response Actions Loop как response procedure.

Incident records следует хранить в standardized formats, удобных для evidence review.

Auditors обычно запрашивают:

- incident reports;
- timeline reconstructions;
- lessons learned summaries.

Если эти документы доступны в standardized format, это демонстрирует program maturity.

Интеграция compliance в routine DAIR operations устраняет необходимость собирать evidence постфактум.

# Incident Tracking Platform Configuration

Incident tracking tooling можно настроить одновременно для:

- effective operations;
- compliance requirements.

Хорошая configuration уменьшает manual effort и обеспечивает consistent generation artifacts.

# Ticketing and Case Management

Primary documentation platform может быть:

- JIRA;
- Remedy;
- specialty IR tracking system.

Для DAIR + CSF 2.0 tracking system должен capture operational coordination и compliance evidence.

Status fields могут использовать vocabulary вроде:

- Detection Complete;
- Verification Pending;
- Containment Active;
- Eradication in Progress;
- Recovery Underway.

Эти statuses напрямую mapping на CSF functions и DAIR activities.

Workflow должен позволять incidents многократно проходить Response Actions Loop без интерпретации iteration как undesirable backtracking.

По возможности нужно фиксировать Decision Maker involvement:

- какие stakeholders consulted;
- какую guidance дали;
- как input повлиял на response.

Это поддерживает Govern function requirements по risk-aligned decision-making.

Evidence artifacts следует связывать с конкретными incident records и сохранять согласно retention policies.

# Communication Templates

Communication templates должны быть разработаны during Prepare в рамках Emergency Communication Plan.

Для major incident categories полезны шаблоны, обеспечивающие consistent messaging в первые 24 часа.

Интеграция с CSF 2.0 состоит в tagging/adaptation templates для compliance reporting.

Status updates можно маркировать:

- CSF function;
- DAIR activity.

Пример:

- initial scoping update → CSF Respond / DAIR Scope;
- recovery validation → CSF Recover.

Consistent vocabulary демонстрирует organizational fluency и создает audit-ready records.

Нужны variants для разных audiences:

## Executive

- impact;
- progress;
- concise decision-relevant information.

## Technical

- detailed activities;
- DAIR waypoint terminology.

Оба variants должны поддерживать compliance documentation.

Инвестиции в tool configuration окупаются долгосрочно.

Clear expectations к note-taking уменьшают manual effort и повышают consistency.

Tooling нужно регулярно review, чтобы оно продолжало поддерживать operational и compliance needs.

# Integrating DAIR with NIST CSF 2.0

Интеграция DAIR и CSF 2.0 показывает, что compliance и operational effectiveness усиливают друг друга.

DAIR дает tactical methodology для реализации strategic vision CSF 2.0.

Key relationships:

- DAIR activities map ко всем шести CSF functions;
- Response Actions Loop operationalizes adaptive iterative response;
- Decision Maker coordination удовлетворяет Govern requirements.

Каждый DAIR waypoint естественно генерирует compliance artifacts:

- preparation documentation;
- detection records;
- response action logs;
- post-incident debrief reports.

Эти artifacts демонстрируют control effectiveness across:

- detection;
- response;
- recovery.

Если организация документирует decision rationale вместе с actions, evidence становится сильнее, потому что показывает alignment с enterprise risk management.

Настройка incident-tracking platforms и communication templates под DAIR + CSF vocabulary снижает manual effort при compliance preparation.

Когда compliance встроен в routine DAIR operations, организация не собирает evidence в спешке после incident.

Результат — incident response capability, которая одновременно:

- demonstrably compliant;
- genuinely effective.

# Ссылка

[1] NIST, "Incident Response Recommendations and Considerations for Cyber Risk Management," NIST SP 800-61 Revision 3, nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf.
