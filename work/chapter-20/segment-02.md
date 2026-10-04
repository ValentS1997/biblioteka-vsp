# Chapter 20 — Segment 02

Source RAG: `p0643:c01`–`p0648:c01`

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
