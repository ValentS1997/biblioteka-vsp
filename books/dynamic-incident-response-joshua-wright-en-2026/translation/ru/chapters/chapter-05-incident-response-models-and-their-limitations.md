---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 5
source_title: "Incident Response Models and Their Limitations"
source_pdf_page_range: "76-84"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0076:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0084:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_flags:
  - "Figure 16 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 17 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 18 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 19 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 20 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 21 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Applied Risk direct quotation: THIRD_PARTY_REVIEW_REQUIRED"
  - "NIST SP 800-61r2 direct quotation: THIRD_PARTY_REVIEW_REQUIRED"
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Third-party direct quotations are not translated or reproduced until separate rights are verified."
  - "Figure captions and cross-references are preserved; visual assets are not reproduced."
---

# Глава 5. Модели реагирования на инциденты и их ограничения

Модели incident response дают структурированный подход к управлению киберинцидентами и реагированию на них. Они описывают важные фазы и шаги процесса, помогая организациям эффективно готовиться к инцидентам, обнаруживать их, реагировать и восстанавливаться. В разных организациях по всему миру используются разные модели incident response, каждая со своими особенностями и акцентами.

## КЛАССИЧЕСКАЯ МОДЕЛЬ: PICERL

Классической моделью incident response является PICERL (произносится как *Pick Earl*), разработанная доктором Eugene Schultz в 1990 году.[1] В последующие годы модель совершенствовали US Navy, Carnegie Mellon University Software Engineering Institute и SANS Institute. Она задаёт системный framework реагирования на инциденты.

PICERL — это аббревиатура следующих этапов:

- Preparation;
- Identification;
- Containment;
- Eradication;
- Recovery;
- Lessons Learned.

Каждый этап опирается на предыдущий, формируя логичное движение от готовности к разрешению инцидента.

Эту модель часто изображают как линейную последовательность или как ступенчатый процесс, как показано на рисунках 16 и 17. В обоих вариантах процесс начинается с подготовки организации к инциденту и выполнения действий по identification для обнаружения инцидентов — например, threat hunting, анализа журналов и incident reporting.

Когда incident обнаружен, incident response team ограничивает его влияние посредством containment и одновременно собирает evidence для анализа. На основе этих данных команда оценивает детали инцидента и выполняет eradication угрозы. После искоренения угрозы организация переходит к recovery, а затем проводит lessons learned analysis, чтобы улучшить дальнейшее реагирование.

### Рисунок 16. Модель PICERL — линейное представление

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

### Рисунок 17. Модель PICERL — ступенчатое представление

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

PICERL даёт организациям понятный framework реагирования и широко применяется в индустрии. Модель задаёт практическую последовательность действий и подчёркивает необходимость шагов, которыми иногда пренебрегают: например, ограничения возможностей атакующего посредством containment и использования lessons learned для улучшения будущего response.

## МОДЕЛЬ NIST: SP 800-61

В 2012 году National Institute of Standards and Technology (NIST) опубликовал Special Publication 800-61 Revision 2. NIST SP 800-61r2 содержит рекомендации по подготовке к инцидентам, их обнаружению, анализу и реагированию. Документ описывает процесс Incident Response Life Cycle, показанный на рисунке 18, и выделяет четыре основные фазы:

- Phase 1: Preparation;
- Phase 2: Detection and Analysis;
- Phase 3: Containment, Eradication, and Recovery;
- Phase 4: Post-Incident Activity.

Эти фазы подчёркивают циклическую природу incident response: lessons learned используются для улучшения последующей подготовки.

### Рисунок 18. NIST Incident Response Life Cycle

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Модель NIST похожа на PICERL, но задаёт более гибкий подход к действиям после обнаружения incident, объединяя containment, eradication и recovery из PICERL в одну фазу. SP 800-61r2 подробнее рассматривает detection и analysis, а post-incident activity включает не только lessons learned, но и сбор и анализ metrics для будущего распределения ресурсов, а также обмен incident information с более широким сообществом. Вместе с тем Revision 2 значительно сокращает уровень детализации по сравнению с более ранними руководствами и содержит заметно меньше конкретных рекомендаций о том, как организациям следует выполнять recovery после инцидента.

## NIST SP 800-61 REVISION 3 И CYBERSECURITY FRAMEWORK

Переход от NIST SP 800-61 Revision 2 к Revision 3 отражает структурное изменение в том, как NIST размещает incident response внутри организационной cybersecurity program. Revision 2 содержал тактическое руководство по incident handling, тогда как Revision 3 рассматривает incident response как интегрированную часть более широкой системы cybersecurity risk management и отказывается от прежней четырёхфазной модели Incident Response Life Cycle.

Новая редакция получила название *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* и согласует incident response с NIST Cybersecurity Framework 2.0, отходя от отдельной incident-handling methodology предыдущей версии.

Такое изменение меняет подход к планированию и реализации incident response capabilities. Revision 3 требует учитывать incident response во всех основных функциях CSF:

- **Govern (GV):** стратегия, ожидания и политика управления cybersecurity risk устанавливаются, доводятся до заинтересованных сторон и контролируются.
- **Identify (ID):** организация понимает свои текущие cybersecurity risks.
- **Protect (PR):** применяются safeguards для управления cybersecurity risks организации.
- **Detect (DE):** возможные кибератаки и компрометации обнаруживаются и анализируются.
- **Respond (RS):** выполняются действия в отношении обнаруженного cybersecurity incident.
- **Recover (RC):** восстанавливаются assets и operations, затронутые cybersecurity incident.

Вместе эти функции рассматривают incident response как один компонент комплексной cybersecurity program, а не как отдельную capability.[2]

Теперь документ выступает как CSF 2.0 community profile. Это означает, что организации, использующие Cybersecurity Framework, должны интегрировать incident response considerations в общие процессы risk management и реализацию controls. Прежняя круговая модель incident response заменена flow, согласованным с функциями CSF, как показано на рисунке 19.

### Рисунок 19. Функции NIST SP 800-61 Revision 3, согласованные с Cybersecurity Framework

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Revision 3 переходит от предписывающих incident-handling procedures Revision 2 к framework-oriented подходу, где основное внимание уделяется организационной интеграции. Revision 2 предлагал incident response teams конкретные methodologies и workflows, тогда как Revision 3 сосредоточен на том, как incident response activities должны влиять на общеорганизационные cybersecurity decisions и, в свою очередь, учитывать их.

Как высокоуровневая стратегия Revision 3 способствует более целостному пониманию incident response, встраивая его в общую cybersecurity posture вместо выделения в самостоятельную функцию. Это важное развитие: оно отражает понимание того, что эффективный incident response требует координации между несколькими организационными областями, включая IT, legal, communications и executive leadership.

Однако вместе с этим из документа исчезает детальное step-by-step guidance, на которое многие incident response teams опирались в технической части реагирования.

## ВАРИАЦИИ КЛАССИЧЕСКОЙ МОДЕЛИ

Многие поставщики продуктов и consulting services публикуют собственные модели incident response. Обычно это небольшие модификации PICERL с дополнительными акцентами, отражающими практики и опыт конкретной организации.

Например, некоторые организации предлагают семишаговую модель, добавляя повторное тестирование после lessons learned.

`THIRD_PARTY_REVIEW_REQUIRED` — в canonical source здесь приведена прямая цитата Applied Risk, описывающая семишаговый процесс с дополнительным повторным тестированием. Цитата не переводится и не воспроизводится до отдельной проверки прав.

### Рисунок 20. Семишаговая модель incident response, Applied Risk BV (a DNV Company)

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Другие варианты добавляют communication или documentation после eradication. По существу они не отличаются от PICERL, но могут давать дополнительное руководство или сильнее подчёркивать отдельные аспекты incident response, важные для организации, публикующей модель.

Существуют и circular models. Один из примеров — *Virginia Tech Guide for Cyber Security Incident Response*. В нём предлагается процесс, включающий preparation, identification/detection/analysis, containment, eradication, recovery и incident closure с последующим возвратом к preparation.

### Рисунок 21. Virginia Tech Incident Response Process Model

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Каждая из этих моделей стремится предоставить структурированную, организованную methodology incident response, с небольшими различиями, отражающими опыт и приоритеты разработавшей её организации. Однако даже такие расширения классической модели в целом не устраняют важные недостатки подходов к современным cybersecurity incidents.

## НЕДОСТАТКИ СУЩЕСТВУЮЩИХ МОДЕЛЕЙ

Несмотря на полезные рекомендации, основанные на опыте авторов этих моделей, у них сохраняется ряд общих недостатков:

- недостаточный акцент на scoping;
- акцент на линейных моделях;
- недостаточное руководство по resource prioritization;
- отсутствие явного требования verification инцидента;
- отсутствие root cause analysis.

Понимание этих ограничений помогает организациям адаптировать существующие модели под свои operational needs.

### Недостаточный акцент на scoping

Scoping в incident response — это процесс определения широты инцидента. Ни NIST SP 800-61, ни PICERL не выделяют этот важный этап явно, что может привести к неполному пониманию incident.

Например, аналитик может обнаружить, что в локальную систему добавлен несанкционированный пользователь. Без правильного scoping он может не понять, что тот же пользователь добавлен и в несколько других систем. Результатом станет неполное реагирование. Scoping побуждает responders использовать доступную информацию, чтобы в рамках response effort лучше понимать фактический масштаб инцидента.

### Акцент на линейных моделях

В большинстве представлений PICERL incident response выглядит как линейная последовательность: от preparation до lessons learned. Некоторые адаптации допускают итеративность, используя формулировки вроде *may* или *could* для обозначения возможного возврата к предыдущим шагам.

NIST SP 800-61 подчёркивает нелинейность подхода: Detection and Analysis следует повторять по мере обнаружения новых затронутых hosts.

`THIRD_PARTY_REVIEW_REQUIRED` — canonical source здесь содержит прямую цитату из NIST SP 800-61r2 Table 3-5, Incident Handling Checklist. Цитата не переводится и не воспроизводится до отдельной проверки прав.

Однако необходимость итеративного цикла во время containment, eradication и recovery больше нигде явно не подчёркивается в NIST SP 800-61r2 и также отсутствует в 800-61r3. Эффективный incident response требует повторяющегося analysis process, чтобы все затронутые системы были выявлены и обработаны. Линейные модели не дают достаточного руководства по этому важному аспекту.

### Недостаточное руководство по приоритизации ресурсов

Лишь немногие организации располагают неограниченными ресурсами для incident response. Во время инцидента необходимо распределять доступные ресурсы в соответствии с business imperatives.

Ни NIST SP 800-61, ни PICERL явно не требуют resource prioritization, что может приводить к неэффективному использованию ресурсов. Особенно сильно это проявляется, когда incident затрагивает множество систем, а организация не может работать со всеми одновременно. Согласование business needs с response effort является важным условием эффективного реагирования.

### Отсутствие требования verification инцидента

Иногда наличие incident очевидно. Например, defaced website однозначно требует реагирования. Однако не каждое событие настолько явно является incident, требующим участия incident response team.

Предположим, пользователи массово сообщают, что application server медленно работает или периодически не отвечает. Systems team обнаруживает несколько неожиданных процессов, потребляющих значительные CPU и memory. Это может быть event, требующий incident response, но может оказаться misconfiguration или performance issue, не требующим отдельного response effort.

Verification неявно присутствует в Detection and Analysis NIST SP 800-61 и Identification PICERL, однако ни одна модель явно не требует подтверждать, что наблюдаемое event действительно является incident, требующим реагирования. Это может приводить к неэффективному расходованию ресурсов и дорогостоящему response на события, которые отвлекают команду от другой важной работы.

### Отсутствие root cause analysis

Понимание root cause инцидента важно для эффективного устранения будущих vulnerabilities. Без root cause организация может многократно реагировать на один и тот же тип incident или не устранить уязвимость, которая к нему привела.

Например, если компрометация произошла из-за слабого пароля на критической системе, простая смена пароля устраняет непосредственно использованную vulnerability. Однако root cause analysis показывает необходимость рассмотреть и другие меры: password complexity policy, password auditing с использованием cracking tools, remote access controls для системы и другие связанные элементы.

NIST SP 800-61 и PICERL предусматривают lessons learned analysis и post-incident activities, но ни одна модель явно не выделяет root cause analysis. Между тем это важный элемент понимания vulnerabilities, приведших к incident. Без него команды часто получают неполное представление о произошедшем и, как следствие, недостаточно эффективный response effort.

## НЕОБХОДИМОСТЬ СОВРЕМЕННОГО ПОДХОДА

Недостатки, описанные в этой главе, не являются провалом самих моделей. Они отражают то, насколько incident response изменился со времени их появления. Современные инциденты сложнее, затрагивают множество систем в разнообразных environments, а организации испытывают всё большее давление, требующее быстро реагировать при ограниченных ресурсах.

Эффективная incident response model должна прямо учитывать эти gaps. Она должна поддерживать итеративный process, соответствующий нелинейной природе реальных инцидентов. Она должна помогать responders определять масштаб incident, подтверждать, что event действительно требует реагирования, и приоритизировать ресурсы в соответствии с business objectives. Кроме того, root cause analysis должен быть стандартной частью response effort.

Следующая глава вводит такую модель — рассчитанную на реалии современного incident response и при этом опирающуюся на foundational concepts существующих моделей.

## Сноски и источники

[1] *Responding to Computer Security Incidents: Guidelines for Incident Handling*, `UCRL-MA-106650`.

[2] *Incident Response Recommendations and Considerations for Cyber Risk Management*, retrieved from `nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf`.
