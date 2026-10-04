---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 10
source_title: "Response Actions Loop"
source_pdf_page_range: "213-223"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0213:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0223:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures remain fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
---

# Глава 10. Цикл действий реагирования

**Response Actions Loop — цикл действий реагирования** представляет собой core operational cycle Dynamic Approach to Incident Response и отражает iterative nature эффективного incident handling.

В отличие от traditional linear models, где containment, eradication и recovery выполняются последовательно, Response Actions Loop рассматривает incident response как learning process: каждая iteration раскрывает new information, требующую additional action.

Этот cyclic approach состоит из activities **scope, contain, eradicate и recover** и может выполняться multiple times до полного resolution incident.

### Рисунок 66. Response Actions Loop Activities

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически; сохраняются подпись и cross-reference.

## ON THE ITERATIVE NATURE OF INCIDENT RESPONSE

Response Actions Loop принципиально меняет подход к incident response, признавая, что complete understanding редко достигается за один pass through response activities.

Каждая iteration даёт new insights, которые влияют на subsequent cycles, создавая continuous learning process, адаптирующийся к evolving understanding incident.

По своей loop structure Response Actions Loop напоминает **OODA loop (Observe, Orient, Decide, Act)** Colonel John Boyd.[1] Однако models оптимизируют разные things.

OODA разработан для military combat operations и оптимизирует individual decision speed under pressure. Response Actions Loop работает на process level и оптимизирует team-wide thoroughness investigation, а не cognitive-cycle speed отдельного responder.

Обе models уходят от single decision cycle к continuous adaptation/learning. Каждый pass through Response Actions Loop уточняет understanding и повышает response effectiveness.

Single-pass incident response часто fails по следующим причинам:

- **Incomplete understanding:** initial view неполон, remediation получается partial, attacker footholds сохраняются.
- **Insufficient insight:** discoveries during eradication reveal additional compromised systems, requiring scoping.
- **Incomplete evidence:** evidence analysis reveals previously unknown attack vectors или persistence mechanisms через iterative scoping.
- **Limited scope:** continued review breadth incident раскрывает related IOC, связанных с initial compromise.

Iterative approach считает эти discoveries не failures/setbacks, а expected part response process и заранее включает multiple learning cycles.

## THE FOUR RESPONSE ACTIONS LOOP ACTIVITIES

Каждая activity внутри loop имеет отдельную цель и одновременно участвует в overall learning process.

### Scope: Understanding Breadth

Scoping определяет extent compromise и помогает понять, какие other systems могут участвовать в incident.

Initial scoping может выявить несколько compromised systems, но subsequent iterations часто раскрывают:

- additional systems с теми же malware variants;
- new IOC, найденные during analysis;
- previously overlooked lateral-movement paths;
- data repositories, к которым attacker получил access.

Каждая iteration уточняет scope understanding, потенциально expanding или contracting incident boundaries по new evidence.

### Contain: Stopping the Bleeding

Containment предотвращает further damage, одновременно preserving evidence для analysis.

Early iterations могут включать:

- isolation obviously compromised systems;
- blocking known malicious IP addresses;
- disabling compromised accounts.

Later iterations могут использовать более sophisticated containment после улучшения understanding:

- careful network segmentation по lateral-movement patterns;
- application-specific restrictions targeting attacker tools;
- deceptive containment, misleading attackers while preserving visibility.

### Eradicate: Removing the Threat

Eradication устраняет attacker presence, но редко полностью succeeds за один attempt.

Initial eradication может удалить:

- obvious malware installations;
- known malicious accounts;
- identified persistence mechanisms.

Subsequent iterations addressing более sophisticated persistence могут включать:

- persistence discovered through deeper analysis;
- backdoors revealed behavioral monitoring;
- supply-chain compromises, requiring vendor coordination;
- living-off-the-land techniques using legitimate tools.

### Recover: Restoring Operations

Recovery возвращает systems к normal operation и одновременно addressing root causes incident.

Early recovery iterations могут:

- restore critical systems from backups;
- reset compromised credentials;
- patch exploited vulnerabilities.

Later iterations могут внедрять systemic improvements на основе root-cause analysis:

- enhanced monitoring for specific attack patterns;
- policy changes для process failures;
- architectural modifications, preventing recurrence.

## ITERATION TRIGGERS

На практике multiple iterations — normal state, driven by new discoveries и evolving understanding.

Response Actions Loop следует продолжать до тех пор, пока new information перестанет появляться и incident не будет resolved к satisfaction organization.

Iteration triggers указывают, что необходим ещё один pass через loop. Их важно замечать рано, потому что cost missed trigger растёт: attacker footholds сохраняются, evidence aging, stakeholder confidence снижается, когда те же systems снова появляются в findings.

Analysts должны рассматривать каждую новую information, полученную от tooling, analysis или business conversations, как potential trigger и задавать вопрос: меняет ли она current understanding **scope, containment, eradication или recovery**?

Source группирует triggers в пять categories:

1. new IOC, surfaced through analysis;
2. scope expansion существующих indicators;
3. evidence incomplete eradication;
4. revelations from deeper forensic work;
5. changing business priorities или external obligations.

### New Indicators of Compromise

Если analysis выявляет previously unknown IOC, team должна вернуться к scoping и искать indicators по environment.

Примеры:

- PowerShell script, найденный в registry одной system, запускает search similar registry modifications elsewhere;
- network analysis выявляет communication с additional C2 infrastructure и требует search других systems communicating those servers.

### Scope Expansion

Scope expansion близок к new IOC, но отличается: новый indicator не появляется; выясняется, что existing indicator имеет более широкий organizational reach.

Например:

- compromised service account, первоначально найденный в marketing application, также active в finance systems hosting regulated data;
- malware sample, initially contained в одном network segment, обнаруживается на hosts другой subsidiary, acquired during recent merger.

Это triggers another scoping pass, часто с другими stakeholders, regulatory considerations и containment requirements.

### Incomplete Eradication

Failed eradication может раскрыть sophisticated persistence и потребовать новой iteration.

Systems, считавшиеся clean, могут показать reinfection, indicating missed persistence или ongoing attacker access через unidentified vectors.

Каждый failed eradication attempt даёт intelligence attacker techniques и помогает сделать subsequent attempts более complete.

### Evidence Analysis Revelations

Detailed analysis collected evidence часто раскрывает information, triggering additional iterations.

Examples:

- memory forensics reveals additional malware families;
- timeline reconstruction shows earlier compromise date;
- log analysis reveals previously unknown affected systems;
- malware reverse engineering exposes hidden capabilities.

### Changing Business Priorities and Obligations

Business priorities могут меняться during incident и вызывать new iterations.

Examples:

- newly identified critical system требует immediate containment/eradication;
- regulatory requirements требуют additional scoping;
- new business objectives заставляют revisit recovery plans;
- cyber-insurance conditions требуют additional response work.

External obligations from law enforcement/regulators тоже могут изменить response mid-incident.

Investigators могут потребовать:

- preserve specific systems;
- defer containment to maintain attacker observation;
- coordinate public-disclosure timing.

Regulators могут требовать:

- notification deadlines;
- evidence handover;
- mandated scope expansion.

Такие requirements могут вызвать new loop iterations независимо от текущего phase.

Triggers не являются failures — это expected elements learning process. Каждая iteration builds on prior knowledge и постепенно улучшает understanding/response effectiveness.

## Stakeholder Communication

Stakeholder communication поддерживает leadership и affected parties informed через regular updates, adapted to audience/authority.

Для senior leadership следует готовить executive summaries, focusing:

- business impact;
- risk reduction;
- resource requirements;

без excessive technical detail.

Для IT/security teams нужны technical briefings с:

- implementation details;
- monitoring requirements;
- validation procedures.

Affected users следует информировать о:

- service disruptions;
- workarounds;
- expected resolution timelines.

Communication frequency/detail нужно adjust по incident severity и stakeholder needs: during critical phases cadence может возрастать, после stabilization — уменьшаться.

Documentation requirements различаются между organizations и могут быть as simple or complex as business requires.

Effective documentation/communication создают foundation informed decision-making across Response Actions Loop.

Documentation требует time/effort, но обеспечивает transparency, defensibility и alignment with organizational objectives.

Records каждой iteration поддерживают не только current incident, но и future responses через lessons learned и institutional knowledge. По мере cycles они складываются в comprehensive incident narrative.

## DOCUMENTATION AND COMMUNICATION

Каждая activity Response Actions Loop требует thorough documentation для:

- legal requirements;
- organizational learning;
- effective stakeholder communication.

Scoping decisions, containment actions, eradication procedures и recovery steps должны capture systematically across incident lifecycle.

Documentation служит нескольким purposes:

- defensible record response decisions;
- knowledge transfer между team members/shifts/iterations;
- support post-incident analysis и future improvements.

Documentation должна быть controlled, но accessible authorized IR personnel.

Все response actions следует record в centralized incident tracking system или case-management platform.

Для многих organizations security labels/access controls в existing ticket systems могут ограничить sensitive incident information и одновременно позволять responders update/review actions.

Необходимо maintain documentation continuity across iterations и link related findings/actions, чтобы incident narrative оставался coherent при evolving understanding.

Минимально source рекомендует three documentation classes:

- decision documentation;
- impact assessment;
- stakeholder communication logs.

### Decision Documentation

Decision documentation фиксирует:

- какие actions taken;
- когда executed;
- кто authorized;
- rationale.

Для scoping следует document systems examined, indicators searched и findings каждой iteration.

Для containment — isolation measures, alternatives considered и rationale selected approach.

Для eradication — artifacts removed, verification removal и encountered challenges.

Для recovery — systems restored, validation steps и security improvements implemented.

Эти records важны для post-incident analysis, legal proceedings и regulatory inquiries.

### Impact Assessment

Impact assessment tracks operational effect response actions на:

- business processes;
- user productivity;
- system availability.

Analysts должны record:

- affected business functions;
- approximate number users affected;
- revenue impact downtime;
- workarounds used to maintain critical operations.

Эти data помогают identify response approaches, обеспечившие effective security при minimal business disruption.

Impact нужно track across all four activities:

- scoping может требовать system access, affecting performance;
- containment disrupts normal operations;
- eradication может требовать service outages;
- recovery содержит transition periods с reduced functionality.

Impact data всё чаще попадает в regulator submissions after incident closure.

Source приводит **DORA** как example: financial-sector organizations могут быть обязаны report impact и associated costs significant incidents, включая direct remediation expenses, lost revenue и follow-on business disruption.[2]

Impact details нужно capture в форме, удобной для person responsible for regulatory notifications, с clear attribution:

- какие business functions affected;
- how long;
- under which response action.

Record during incident проще и надёжнее, чем reconstruction after closure, когда memory fades и log-retention windows expire.

## KNOWING WHEN TO STOP

Exit Response Actions Loop требует judgment по technical indicators, business considerations и input decision makers.

Technical indicators resolution могут включать:

- no new IOC during scoping;
- monitoring shows no attacker activity;
- eradication verification confirms threat removal;
- systems operate normally after recovery.

Business indicators также critical:

- operational objectives met;
- acceptable risk level achieved;
- cost-benefit analysis supports stopping active response;
- resource constraints may force prioritization even with residual uncertainty.

Decision to exit loop часто требует leadership input по acceptable risk и operational priorities.

Leadership balance:

- residual uncertainties;
- pressure return to normal operations;
- regulatory closure requirements;
- ongoing-monitoring strategy.

Некоторые organizations требуют formal sign-off; другие use stakeholder consensus. Это отражает organizational culture/risk tolerance, не обязательно maturity.

Независимо от model, loop-exit decision должен быть captured **in writing** как explicit, attributed decision, а не implied agreement.

Record должен include:

- decision maker name;
- supporting technical/business indicators;
- accepted residual risks;
- date/time.

Такой record делает rationale defensible, если incident reopened или reviewed regulators.

> Сам факт того, что имя decision maker будет записано рядом с exit decision, может повысить quality решения.

Source отмечает, что decision makers иногда reconsider loop-exit decision, когда понимают, что их имя будет явно связано с ним в formal record.

## PRACTICAL CONSIDERATIONS

По опыту автора при работе с разными teams Response Actions Loop действительно увеличивает effort и complexity. Iterative approach требует больше time/resources upfront, но это необходимо для comprehensive handling sophisticated incidents, где linear response может пропустить связанные threats.

Source сравнивает два approaches.

В Figure 67 team получает initial threat report, responds, но не выявляет additional related threats.

### Рисунок 67. Linear Response Threat Processing

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически.

В Figure 68 iterative model позволяет uncover multiple related threats через successive passes Response Actions Loop.

### Рисунок 68. Iterative Response Threat Processing

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически.

Чтобы успешно использовать loop, teams должны учитывать несколько practical constraints.

### Resource Management

Organizational resources нужно manage across multiple iterations.

Проблемы:

- team fatigue;
- необходимость rotation/rest;
- budget constraints;
- tool limitations;
- manual forensic/evidence-collection bottlenecks.

Decision makers должны balance thorough response и resource realities:

- избегать burnout;
- сохранять sufficient effort для resolution;
- prioritise critical scoping/remediation при ограниченном budget.

### Documentation Burden

Каждая iteration создаёт substantial documentation, которую нужно maintain coherently across lifecycle.

Legal/compliance requirements могут требовать specific standards/retention periods.

Knowledge transfer между shifts требует coordination, чтобы incoming responders понимали current state и не создавали duplication/gaps.

Decision makers не должны требовать excessive documentation, мешающую active response.

Нужен balance между:

- thorough records;
- pace/dynamics active incident.

### Stakeholder Patience

По мере iterations patience stakeholders может снижаться.

Leadership может воспринимать repeated cycles как poor planning/execution, а не natural progression understanding incident.

Business units могут давить на faster restoration normal operations до complete remediation.

IRT должна manage expectations через communication:

- объяснять value iterative learning;
- демонстрировать progress каждой cycle;
- признавать legitimate business pressure на resolution.

Response Actions Loop превращает incident response из linear checklist в dynamic learning process.

Success определяется не perfect execution одного pass, а количеством iterations, необходимым для true resolution.

Хотя iterative response может требовать больше initial time, он даёт:

- более complete remediation;
- organizational learning;
- lower risk recurrence.

## RESPONSE ACTIONS LOOP: STEP-BY-STEP

Следующие steps дают condensed reference для управления iterative cycle scope → contain → eradicate → recover.

Individual activity chapters владеют per-activity procedures; этот guide описывает то, что unique именно для выполнения activities как loop.

Source указывает, что guide доступен в PDF/Markdown на `dynamicincidentresponse.com`.

### Step 1. Run the Loop Expecting Each Activity to Deepen Across Iterations

Principles:

- scope, contain, eradicate, recover имеют собственные chapter step-by-step guides;
- loop guide focuses on orchestration/cycling;
- sequence зависит от incident state, а не fixed order;
- scope usually first, но contain может идти earlier/parallel при active threat;
- каждая subsequent iteration должна давать более sophisticated/complete results.

### Step 2. Identify Iteration Triggers Requiring Additional Response Cycles

Representative triggers:

- new IOC discovered;
- incomplete eradication/reinfection;
- forensic revelations requiring expanded scoping;
- changing business priorities;
- changing regulatory requirements.

### Step 3. Maintain Cross-Phase Documentation and Communication

Loop owns cross-phase communication cadence; per-activity documentation feeds into it.

Representative activities:

- record decision documentation: what, when, who, rationale;
- track impact of response actions on business/system availability;
- provide audience-specific stakeholder communication:
  - executive summaries;
  - technical briefings;
  - user notifications;
- maintain documentation continuity across iterations;
- adjust communication frequency/detail by severity/stakeholder needs.

### Step 4. Build Cumulative Understanding Across Iterations

Representative activities:

- document findings each iteration;
- link new discoveries to prior cycles;
- ensure knowledge transfer between shifts.

### Step 5. Monitor for Technical Indicators of Resolution

Representative indicators:

- no new IOC during scoping;
- monitoring shows no attacker activity;
- eradication verification confirms threat removal;
- systems operate normally after recovery.

### Step 6. Assess Business Indicators for Loop Conclusion

Representative indicators:

- operational objectives met;
- acceptable risk level achieved;
- cost-benefit analysis supports conclusion active response;
- resource constraints require prioritization.

### Step 7. Engage Decision-Makers for Loop Exit Determination

Representative activities:

- present technical/business indicators to leadership;
- discuss risk acceptance for residual uncertainties;
- confirm regulatory closure requirements;
- establish ongoing monitoring plans.

### Step 8. Address Practical Considerations Throughout Iterations

Representative considerations:

- manage fatigue with rotations/rest periods;
- account for budget/tool limitations affecting iteration speed;
- balance documentation burden with active response;
- manage stakeholder patience;
- explain why repeated cycles reflect evolving incident understanding, not necessarily poor execution;
- communicate progress and business tradeoffs.

## Сноски и источники

[1] Boyd, John, "A Discourse on Winning and Losing," www.airuniversity.af.edu/Portals/10/AUPress/Books/B_0151_Boyd_Discourse_Winning_Losing.pdf

[2] European Union, "Regulation (EU) 2022/2554 on Digital Operational Resilience for the Financial Sector (DORA)," January 2023, www.digital-operational-resilience-act.com/
