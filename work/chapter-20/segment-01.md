# Chapter 20 — Segment 01

Source RAG: `p0637:c01`–`p0642:c01`

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

