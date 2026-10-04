---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 4
source_title: "Getting Started"
source_pdf_page_range: "61-75"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0061:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0075:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_flags:
  - "Figure 12 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 13 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 14 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 15 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "CrowdStrike direct quotation in IOA sidebar: THIRD_PARTY_REVIEW_REQUIRED"\n  - "FortiGuard advisory excerpt preceding Listing 26: THIRD_PARTY_REVIEW_REQUIRED"
rag_gaps:
  - "MTTD equation is not present in extracted canonical RAG text layer: RAG_MISS"
  - "MTTR equation is not present in extracted canonical RAG text layer: RAG_MISS"
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Commands, queries, log records, rule syntax, paths, URLs, identifiers and acronyms are preserved verbatim where present."
  - "Third-party direct quotation is not translated until separate rights are verified."
  - "Missing equations are not reconstructed from model memory."
---

# Глава 4. С чего начать

На протяжении книги мы будем рассматривать несколько важных аспектов, которые следует учитывать при анализе и оценке процесса реагирования на инциденты. Некоторые из них связаны с терминологией и позволяют всем участникам команды общаться эффективно и однозначно. Другие представляют собой стратегии, дающие понятный способ измерять результативность реагирования.

В этой главе мы рассмотрим ряд распространённых терминов incident response, а также важные базовые концепции реагирования на инциденты.

## ИНЦИДЕНТ

Инцидент — это неблагоприятное событие в информационной системе и/или сети либо угроза возникновения такого события.[1] Инцидент подразумевает причинение вреда или попытку его причинить.

Это классическое определение инцидента, однако на практике существует множество нюансов. Не все инциденты выглядят одинаково: одни возникают в результате преднамеренной атаки, другие — из-за человеческой ошибки, третьи — вследствие внешних обстоятельств, не зависящих от людей. Разделение инцидентов на злонамеренные, случайные и вызванные внешней средой помогает точнее определить их природу и формирует подход response team.

### Злонамеренные инциденты

Такие инциденты являются результатом преднамеренных действий threat actor или adversary. Эксплуатация уязвимости, злоупотребление украденными credentials или развёртывание вредоносного кода для компрометации системы — всё это относится к злонамеренным инцидентам.

> Основное внимание в этой книге уделяется злонамеренным инцидентам. Практики incident response, описанные здесь, применимы также к случайным и environmental incidents, однако рассматриваемые техники и стратегии прежде всего рассчитаны на случаи, когда атакующий активно пытается скомпрометировать системы и данные.

### Случайные инциденты

Такие инциденты возникают из-за непреднамеренных действий, причиняющих вред системам или данным. Пользователь может удалить чувствительные данные; неверная конфигурация firewall может открыть внутренние сервисы в интернет; разработчик может закоммитить API credentials в публичный репозиторий; партнёр может случайно раскрыть клиентские данные в Google Cloud bucket — все эти ситуации требуют incident response.[2]

На ранних этапах расследования случайные и злонамеренные инциденты нередко выглядят одинаково, поскольку первоначальные признаки — например, раскрытые данные или несанкционированный доступ — могут совпадать, пока не установлена root cause. После установления root cause усилия incident response смещаются в сторону remediation и prevention, а анализ действий threat actor становится менее значимым.

### Инциденты, вызванные внешней средой

Такие инциденты вызваны природными событиями или отказами инфраструктуры, а не действиями человека. Примеры: отключение питания, которое приводит к некорректному завершению работы систем и повреждению данных; затопление data center; сбой cloud provider, нарушающий работу критических сервисов. Хотя environmental incidents находятся за пределами основной темы этой книги, организациям следует иметь планы реагирования и на них наряду с cybersecurity incidents.

На практике не каждая организация немедленно объявляет событие инцидентом. В регулируемых отраслях само присвоение статуса incident может запускать обязательства по уведомлению и нормативные сроки, поэтому многие организации сознательно работают в прединцидентном режиме расследования, пока не накопят достаточно информации. На этой стадии response team собирает данные и определяет масштаб, не классифицируя событие формально как incident. Такой подход распространён и практичен, но означает, что действия реагирования, рассматриваемые далее в книге, могут начаться ещё до официального объявления инцидента.

## СОБЫТИЕ

Событие — это любое наблюдаемое происшествие в системе и/или сети. Определение кажется простым, но само понятие события и методы его оценки могут усложняться, особенно при работе с коммерческими продуктами и поставщиками, которые адаптируют терминологию под свои решения.

Независимо от того, работает ли аналитик в incident response team или security operations center (SOC), применяет ли digital forensics techniques в рамках расследования или обслуживает системы как системный администратор, он постоянно работает с событиями. События образуют непрерывный поток информации, описывающий и фиксирующий деятельность систем и сетей.

Примеры событий:

- запись firewall Fortinet:
  `msg="Unregistered device localhost add succeeded" device="localhost" adom="FortiManager"`
- ошибка Apache web server:
  `PHP Fatal error: Uncaught Error: Call to undefined function add_action() in public_html/wp-content/plugins/hello.php:69`
- ticket службы поддержки №12345: пользователь сообщает о низкой производительности рабочей станции;
- Windows Event ID 104: `The System event log was cleared.`
- запись Linux auth log:
  `systemd: pam_unix(systemd-user:session): session opened for user httpd by (uid=0)`
- запись сетевого устройства:
  `Administrator accessed UniFi OS via unifi.ui.com. Source IP: 95.181.86.2`
- OPS engineer сообщает о ранее неизвестном локальном пользователе `badmin` на сервере доступа к камерам.

Многие аналитики воспринимают события исключительно как данные из logging sources. Однако события могут поступать и из недигитальных источников: например, системный администратор сообщает об отказе системы или пользователь обращается за помощью, потому что его рабочая станция внезапно стала работать медленно.

При обсуждении потока событий в совокупности систем книга использует аналогию с водопадом. Поток событий можно представить как воду, падающую с вершины скального уступа, как показано на рисунке 12. Аналитики могут наблюдать события по мере движения этого потока или анализировать их после накопления в нижней точке.

### Рисунок 12. Водопад событий

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Аналитики извлекают полезные сведения из потоков событий, выявляя шаблоны и аномалии, которые могут указывать на incident. Событием может быть запись в log file, наблюдаемая сетевая активность, сообщение пользователя о необычном поведении системы или любое другое наблюдаемое явление. Большинство событий не свидетельствуют об атаке или инциденте. Однако некоторые требуют дальнейшего расследования. Такие события называются Events of Interest (EOI).

## СОБЫТИЕ, ПРЕДСТАВЛЯЮЩЕЕ ИНТЕРЕС

Event of Interest (EOI) — событие, которое требует дальнейшего расследования. Рассматривая непрерывный поток событий во всех системах, аналитики быстро понимают, что обработать их все невозможно. Необходима фильтрация, позволяющая определить, какие события являются интересующими. Определение «интересующего» события различается от организации к организации.

Рассмотрим события, показанные на рисунке 13. На иллюстрации отмечены несколько примеров:

- **Неизвестная browser session.** Web application server фиксирует начало новой сессии пользователя, который ранее не входил в систему.
- **Доступ с source IP 95.181.86.2.** Web Application Firewall (WAF) регистрирует запрос с адреса `95.181.86.2`, который Cyber Threat Intelligence (CTI) sources связывают со злонамеренной активностью.
- **Необычное время доступа.** Система обращается к приложению в 3:00 ночи, хотя обычно в это время не используется.
- **Попытка входа с неверным username.** Пользователь пытается войти с именем `admin`, которое не является допустимым username в этой системе.

### Рисунок 13. Водопад событий с Events of Interest

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Каждое из этих событий может указывать на incident, а может оказаться безобидным. Однако одно событие само по себе обычно даёт ограниченный контекст. Лучше рассматривать события совместно: по времени, источнику, reporting system и другим факторам. Хотя отдельное событие иногда прямо указывает на incident, аналитикам часто требуется оценить поток событий целиком.

### Организационное определение EOI

Событие не обязательно является инцидентом, хотя оно может дать сведения о наличии инцидента; несколько событий также могут быть скоррелированы и привести к выявлению incident. При этом то, что считается EOI в одной организации, может не считаться им в другой.

Например, рассмотрим MySQL query из листинга 25, который показывает неудачные попытки входа на WordPress server за последние 24 часа.

### Листинг 25. MySQL query для анализа неудачных входов WordPress за последние 24 часа

```
mysql> SELECT event_type, DATE_FORMAT(FROM_UNIXTIME(MIN(created_on)), '%Y-%m-%d %H:%i:%s')
AS first_observed_failure, client_ip, COUNT() AS failure_count FROM wp_wsal_occurrences
WHERE alert_id = 1002 AND FROM_UNIXTIME(created_on) >= NOW() - INTERVAL 1 DAY GROUP BY
event_type, client_ip ORDER BY first_observed_failure ASC;*
+--------------+------------------------+-----------------+---------------+
| event_type   | first_observed_failure | client_ip       | failure_count |
+--------------+------------------------+-----------------+---------------+
| failed-login | 2024-12-30 12:44:36    | 13.214.39.195   |             9 |
| failed-login | 2024-12-30 12:59:02    | 185.196.220.113 |         40592 | ①
| failed-login | 2024-12-30 13:10:18    | 13.214.202.144  |             3 |
| failed-login | 2024-12-30 22:11:25    | 3.101.81.132    |             8 |
| failed-login | 2024-12-30 22:18:20    | 54.151.17.204   |            10 |
| failed-login | 2024-12-31 10:44:19    | 35.72.8.125     |             3 |
| failed-login | 2024-12-31 11:51:57    | 18.183.180.112  |             1 |
+--------------+------------------------+-----------------+---------------+
7 rows in set (8.59 sec)
mysql> select object, event_type, user_agent from wp_wsal_occurrences WHERE alert_id =
1000 AND client_ip = '185.196.220.113';
Empty set (3.75 sec) ②
```

① 40 592 неудачных попыток входа с `185.196.220.113`.  
② Успешных входов с `185.196.220.113` не зарегистрировано.

Первый SQL query обращается к таблице WordPress Security Audit Log (WSAL), выбирая события неудачного входа, группируя их по event type и client IP и сортируя по времени первой наблюдаемой неудачи. Каждая строка представляет одну или несколько неудачных попыток входа, и каждую из них можно рассматривать как EOI для расследования.

Второй query обращается к той же таблице и пытается найти успешные входы для IP-адреса с наибольшим числом неудачных попыток. Отсутствие таких записей — `Empty set` — показывает, что многочисленные неудачные попытки не привели к успешному входу.

Одна организация может классифицировать эти данные как атаку и начать расследование. Другая может также признать это атакой, но не считать EOI, поскольку она не привела к успеху.

Решение о том, должны ли одно или несколько событий привести к классификации incident, должно учитывать политики и приоритеты организации. Сами события объективны, но их интерпретация субъективна и может различаться между организациями.

В обновлённой иллюстрации на рисунке 14 несколько предыдущих EOI объединены в агрегированное представление: многочисленные неудачные попытки входа и успешный вход, после которого последовала ошибка MFA, показаны как aggregate EOI. Даже такое представление не обязательно означает incident — это зависит от политики организации. Однако aggregate EOI даёт более полную картину событий, которые могут указывать на инцидент и требовать расследования.

### Рисунок 14. Водопад событий с агрегированными Events of Interest

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

Для incident response team события являются важным источником данных о потенциальных инцидентах. В идеале организация должна собирать и хранить полезные события в течение разумного retention period с учётом типа события и собственных потребностей. Такой накопленный пул событий обеспечивает исторический контекст и ценные данные для аналитиков и часто хранится в Security Information and Event Management (SIEM) или другой log management platform.

## ИНДИКАТОР КОМПРОМЕТАЦИИ

Indicator of Compromise (IOC) — свидетельство успешной компрометации. Хотя некоторые события также могут использоваться как IOC, обычно IOC являются более конкретными datapoints. IOC связываются с источником intelligence — например, threat intelligence feed, — чтобы получить контекст, позволяющий определить наблюдаемое свидетельство как результат компрометации. IOC могут быть atomic, computed или behavioral.[3]

Наиболее распространённый тип — atomic IOC. Слово atomic означает, что IOC представляет собой один конкретный datapoint, который нельзя дополнительно разложить. Atomic IOC полезны для анализа, потому что редко дают false positives. Их также легко применять в автоматизированных detection systems: для обнаружения такого IOC не требуется дополнительное вычисление или анализ. Типичные примеры atomic IOC — имена файлов, registry keys, URLs и IP addresses.

Computed IOC выводится из наблюдаемых в системе данных после некоторого вычисления или анализа. Например, атакующий может рандомизировать имя файла, используемого для persistence на скомпрометированной Windows workstation, что мешает обнаружению по atomic IOC имени файла. Однако hash содержимого файла позволяет получить IOC, не зависящий от имени. Другой пример computed IOC — regular expression match в command-line expression: правило может сработать, если длина command line превышает заданный предел или содержимое соответствует известному attack pattern. Как и atomic IOC, computed IOC удобно применять в автоматизированных detection systems, хотя для них требуется немного больше обработки.

Behavioral IOC представляет собой datapoint, полученный в результате совокупного анализа поведения атакующего, событий, atomic IOC и computed IOC. Такие IOC сложнее обнаруживать: требуется анализировать данные и понимать Tactics, Techniques, and Procedures (TTPs) атакующего. Также нужен baseline нормального поведения системы. Behavioral IOC являются ценным средством обнаружения инцидентов, поскольку позволяют выявлять attackers, использующих новые или неизвестные техники, через anomaly analysis или pattern matching.

Аналитики используют IOC для выявления присутствия атакующего в системе, сети, logging data и forensic analysis. Threat intelligence feeds предоставляют ценный источник IOC, позволяя обнаруживать известные угрозы и применять соответствующие indicators к своим системам.

Например, ниже приведён IOC, описывающий log entries при эксплуатации уязвимости Fortinet FortiGate `CVE-2024-55591`:

```
Following admin creation log with seemingly randomly generated user name and source IP: type="event"
subtype="system"   level="information"   vd="root"   logdesc="Object   attribute   configured"
user="admin"  ui="jsconsole(127.0.0.1)"  action="Add"  cfgtid=1411317760  cfgpath="system.admin"
cfgobj="vOcep"   cfgattr="password[*]accprofile[super_admin]vdom[root]"   msg="Add   system.admin
vOcep [4]
```

Используя эти threat intelligence data, аналитики могут анализировать журналы Fortinet и выявлять успешную эксплуатацию Fortinet FortiOS vulnerability, описанной в `CVE-2024-55591`. Построив detection capability для автоматической оценки Fortinet device logs, можно использовать IOC для поиска скомпрометированных устройств Fortinet.

В данном случае log entry можно сопоставлять как atomic IOC, опираясь на статические элементы записи. Используя синтаксис Sigma detection format, можно также сформировать computed IOC через pattern matching с regular expression syntax. Пример Sigma rule приведён в листинге 26.

### Листинг 26. Sigma rule для обнаружения IOC Fortinet FortiOS

```yaml
title: Fortinet FortiOS Exploit Attempt - FG-IR-24-535
id: 8c67a5b8-9e6b-4f34-a90f-7b728f02856e
status: experimental
description: Detects exploitation of CVE-2024-55591 against Fortinet FortiOS devices where an
attacker creates a new admin user.
references:
- https://www.fortiguard.com/psirt/FG-IR-24-535
author: Joshua Wright
date: 2025-03-12
logsource:
  category: firewall
  product: fortinet
  service: fortios
detection:
  keywords: ①
    - 'type="event"'
    - 'subtype="system"'
    - 'logdesc="Object attribute configured"'
    - 'action="Add"'
    - 'cfgpath="system.admin"'
    - 'cfgattr="password[*]accprofile[super_admin]vdom[root]"'
  condition: keywords
falsepositives:
  - Unknown
level: high
tags:
  - attack.persistence
  - cve.2024.55591
  - cve.2024.24472
  - fortios
  - fortinet
```

① Ключевые слова Sigma rule, используемые для обнаружения FortiOS exploit, соответствующего IOC intelligence из advisory Fortinet.

IOC — это intelligence, который аналитики могут превратить в практическое действие. Независимо от того, применяется ли он через Sigma rules для log detection, Endpoint Detection and Response (EDR), Network Detection and Response (NDR) или другой инструмент, IOC представляет actionable insight, необходимый для выявления инцидентов.

### Что насчёт Indicators of Attack (IOA)?

Indicator of Attack (IOA) — термин, популяризированный CrowdStrike для описания detection capabilities, основанных на поведении атакующего. Источник книги приводит прямую цитату CrowdStrike, объясняющую IOA.

`THIRD_PARTY_REVIEW_REQUIRED` — прямая цитата CrowdStrike не переводится и не воспроизводится в производном тексте до отдельной проверки прав.[5]

CrowdStrike использует IOA для выявления присутствия атакующего в системе на основании его поведения, а не конкретных инструментов или техник. Наряду с advanced threat detection capabilities CrowdStrike использует цепочки связанных событий, классифицированных как suspicious или malicious, для обнаружения угроз.

На практике различие между IOA и behavioral IOC невелико. Более простые механизмы detection — atomic IOC и computed IOC — остаются полезными для выявления известных угроз, тогда как IOA и behavioral IOC дают более развитые возможности обнаружения как известных, так и неизвестных угроз. Независимо от того, использует аналитик термин IOA или behavioral IOC, базовая идея одна: обнаруживать присутствие атакующего по его поведению, а не ограничиваться конкретными atomic или computed IOC.

## MEAN TIME TO DETECT

Mean Time to Detect (MTTD) — метрика, измеряющая среднее время, необходимое для обнаружения security incident. Она используется для оценки работы SOC и incident response team.

Источник книги указывает, что MTTD рассчитывается как общее время обнаружения всех инцидентов за заданный период, делённое на число обнаруженных инцидентов.

`RAG_MISS` — сама формула MTTD отсутствует в извлечённом canonical RAG text layer и не реконструируется по памяти модели.

Как performance metric MTTD показывает задержку между возникновением инцидента и его обнаружением. Если атакующий скомпрометировал систему и остаётся незамеченным несколько дней, MTTD будет высоким, что указывает на необходимость улучшать detection capabilities. Низкий MTTD, напротив, означает, что организация способна быстро выявлять инциденты и переходить к реагированию.

### Проблемы измерения MTTD

MTTD — широкая метрика, которая сильно зависит от типа incident, размера и сложности организации и зрелости её security operations. По данным различных security reports, средний MTTD может варьироваться от дней до месяцев. IBM *Cost of a Data Breach Report* указывает среднее значение 204 дня для выявления breach.[6] Verizon *Data Breach Investigations Report* показывает значительный разброс между attack vectors: одни инциденты обнаруживаются за минуты, другие остаются незамеченными месяцами.[7] Организации со зрелыми SOC и robust detection capabilities часто измеряют MTTD часами или даже минутами для критичных инцидентов. Industry leaders с advanced threat detection и automated monitoring systems сообщают MTTD менее 24 часов для большинства типов инцидентов.[8][9]

Ещё одна проблема MTTD — определение момента возникновения incident. Во многих случаях точное время компрометации неизвестно, и организация вынуждена оценивать его по самому раннему наблюдаемому IOC. По мере появления новых доказательств occurrence time может изменяться. Нередко точное время становится известно только после полного расследования и remediation, поэтому MTTD по своей природе часто является retrospective metric.

Чтобы MTTD был полезен, его следует отслеживать во времени и определять единообразно для всей организации. Необходимо установить ясные критерии того, что считается incident, и обеспечивать точные timestamps возникновения и обнаружения каждого инцидента. Наблюдая MTTD в динамике, организация может выявлять тенденции, оценивать эффективность detection capabilities и принимать решения об инвестициях в улучшение security posture.

## MEAN TIME TO RESPOND

Mean Time to Respond (MTTR) — метрика, измеряющая среднее время между обнаружением security incident и выполнением реагирования с его разрешением. Если MTTD отражает эффективность detection processes, то MTTR показывает эффективность incident response capabilities.

Источник книги указывает, что MTTR рассчитывается как суммарное время реагирования и разрешения всех инцидентов за заданный период, делённое на число разрешённых инцидентов.

`RAG_MISS` — сама формула MTTR отсутствует в извлечённом canonical RAG text layer и не реконструируется по памяти модели.

Как performance metric MTTR помогает отслеживать, насколько быстро организация может сдержать, разрешить инцидент и восстановиться после него. Например, если среднее реагирование и разрешение занимает 48 часов, это даёт baseline для оценки улучшений. Более низкий MTTR может указывать на эффективные incident response processes, достаточный staffing и подходящие tools. Высокий MTTR, напротив, может свидетельствовать о недостатках процедур, ограничениях ресурсов или технических проблемах, замедляющих resolution.

MTTR часто используют вместе с MTTD, чтобы получить более полное представление о security posture. MTTD показывает, насколько быстро угрозы обнаруживаются, MTTR — насколько быстро они устраняются. Вместе эти метрики описывают lifecycle от первоначальной компрометации до resolution.

Источник также отмечает общее время от возникновения incident до его разрешения.

`RAG_MISS` — соответствующее математическое выражение отсутствует в canonical RAG text layer и не реконструируется.

### Проблемы измерения MTTR

Чтобы MTTR был полезной метрикой, организация должна чётко определить, что означает «resolution» для каждого типа incident. Это может включать сдерживание угрозы, устранение присутствия атакующего, восстановление затронутых систем и подтверждение того, что угроза полностью устранена. Единообразие критично: разные команды и подразделения могут по-разному понимать, что означает «разрешить» инцидент.

Как и MTTD, MTTR значительно зависит от типа incident, размера и сложности организации и зрелости incident response processes. Простой phishing incident, где пользователь перешёл по malicious link, может быть разрешён за несколько часов. Сложная ransomware attack с восстановлением из backups может занимать недели или месяцы. Поэтому MTTR целесообразно отслеживать по категориям:

- **Тип incident.** Malware infection, data breach, insider threat и другие категории имеют существенно разные MTTR.
- **Severity level.** Инциденты можно разделять по приоритету и severity — например, P0/Critical, P1/High, P2/Medium, P3/Low — и отслеживать MTTR отдельно.
- **Percentiles.** Вместо одного среднего значения можно отслеживать median и percentile MTTR, например P90. MTTR P50/median показывает типичное время реагирования, а P90 — длинный хвост инцидентов, требующих существенно больше времени.
- **Time to containment и time to resolution.** MTTR можно разделять по этапам: время до containment — прекращения непосредственной угрозы — и время до полного resolution — восстановления и validation. Это позволяет отдельно измерять критические milestones процесса.

MTTR чувствителен к внешним зависимостям, которые incident response team не контролирует. Инциденты часто требуют действий от IT operations, legal, human resources, external vendors или law enforcement, и ожидание этих сторон увеличивает MTTR. Например, если response team создаёт ticket для IT с просьбой сбросить скомпрометированную учётную запись, время выполнения зависит уже от SLA IT, а не только от incident response capability.

> Ticketing systems обычно позволяют приостанавливать отсчёт времени на период внешнего ожидания, но на практике команды нередко забывают это делать, из-за чего метрика постепенно перестаёт отражать реальность.

Организациям следует понимать, какие факторы влияют на MTTR. Тогда improvement efforts будут направлены на то, на что response team действительно может воздействовать, а внешние зависимости станут видимыми вместо того, чтобы растворяться в агрегированном числе.

MTTR измеряет скорость реагирования, но не его качество. Команда может быстро закрывать tickets, не проводя полноценного расследования, и получить низкий MTTR, при этом пропуская persistence, связанные системы или root causes. Вознаграждение только за низкий MTTR создаёт давление на скорость закрытия, а не на качество расследования. Поэтому MTTR следует дополнять quality-oriented measures.

Incident response teams должны совместно с decision makers определить наиболее полезные категории MTTR для отслеживания и отчётности. Основное внимание следует уделять метрикам, которые дают actionable insight и позволяют оценивать эффект инвестиций в tools, training и process improvements.

### С чего начать с метриками incident response

В *SANS SOC Survey 2025* Chris Crowley отмечает, что половина опрошенных организаций не отслеживает MTTD или MTTR. Из тех, кто отслеживает, 69% используют ручные или преимущественно ручные методы — spreadsheets или ticketing systems — вместо автоматизированных tools.[10] Это объяснимо: многим организациям сложно определить эти метрики и измерять их последовательно, либо не хватает систем и человеческих ресурсов для tracking and analysis.

Даже с этими ограничениями MTTD и MTTR дают полезные данные для измерения incident response effectiveness и обоснования ресурсов, необходимых для улучшения security operations. Если команда может показать конкретные detection и response times, ей проще аргументировать необходимость дополнительного staff, tools, training и process improvements. Executive leadership и budget decision makers обычно лучше реагируют на количественные данные, которые показывают текущее состояние, выявляют gaps и позволяют оценить эффект предлагаемых инвестиций.

Три подхода для начала:

1. **Начать с простого manual tracking.** Фиксировать несколько ключевых datapoints в spreadsheet или ticketing system: предполагаемое время возникновения incident, время обнаружения и время resolution. Даже простая ручная история создаёт baseline и позволяет видеть тенденции.
2. **Определить ясные категории incident и критерии resolution.** Совместно с response team установить определения detection и resolution для каждого типа incident, документировать их и применять одинаково. Начать можно с 3–5 широких категорий — например, malware, unauthorized access, data loss и denial-of-service — и уточнять модель со временем.
3. **Использовать существующие tools для автоматизации сбора данных.** Ticketing systems вроде ServiceNow и Jira, SIEM и incident response platforms часто автоматически фиксируют timestamps создания incident, смены статуса и resolution. Дополнительные поля могут хранить occurrence time и detection time, а простые reports и dashboards — визуализировать MTTD и MTTR trends.

При построении программы метрик важнее последовательность и точность, чем стремление сразу получить идеальную модель. Последовательно собираемые несовершенные данные полезнее полного отсутствия данных. По мере накопления опыта организация сможет уточнять подход.

### Дополнение MTTR оценкой качества

MTTR показывает, насколько быстро команда закрывает инциденты, но быстрое resolution ничего не говорит о полноте реагирования. Tickets можно закрывать быстрее, если пропускать log review, принимать первоначальный triage без validation или объявлять систему чистой после поверхностного scan. Это улучшает MTTR и ухудшает фактический результат.

Чтобы сбалансировать скорость, организация может дополнить MTTR quality score для каждого incident ticket. Для начала достаточно простой шкалы от 1 до 10. Reviewer может оценивать вопросы:

- Был ли первоначальный анализ достаточно глубоким или analyst слишком быстро прошёл мимо evidence?
- Оставался ли ticket длительное время без движения?
- Были ли выявлены и исследованы связанные системы или incident ошибочно рассматривался как изолированный?
- Была ли задокументирована root cause или response остановился на устранении симптомов?
- Был ли ticket закрыт преждевременно, что позже привело к reopen или escalation?

Quality score позволяет увидеть закономерности, которые MTTR не показывает: сотрудник может держать tickets без движения несколько дней; analysts могут закрывать P1 быстрее P3, что иногда говорит не о лучших возможностях, а о давлении на скорость; отдельные категории инцидентов могут системно исследоваться поверхностно.

Совместное отслеживание quality score и MTTR даёт более полную картину response effectiveness. Если quality scores улучшаются при стабильном MTTR, команда действительно становится лучше. Если MTTR снижается одновременно с ухудшением quality scores, скорость достигается за счёт глубины.

## INCIDENT MANAGEMENT И INCIDENT RESPONSE

Термины incident management и incident response часто используются как взаимозаменяемые, однако означают разные вещи. Понимание различий помогает командам определить роли и ответственность в общем процессе работы с security incidents. Рисунок 15 показывает их отдельные и пересекающиеся области ответственности.

### Рисунок 15. Ответственность incident response и incident management

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект требует отдельной проверки прав и не включается в производный перевод автоматически.

### Incident Response

Incident response — техническая работа по обнаружению, анализу, сдерживанию, искоренению и восстановлению после security incident. Analysts и responders выполняют validation и triage alerts, собирают forensic artifacts, изолируют скомпрометированные hosts и восстанавливают services. По своей сути incident response — техническая дисциплина, сосредоточенная непосредственно на инциденте: понять, что произошло, остановить дальнейший ущерб и вернуть системы в known-good state.

Эффективный incident response требует как широты, так и глубины технических навыков. Responders нужны знания network analysis, host forensics, log interpretation, нескольких operating systems и cloud platforms, хотя один человек редко является экспертом во всех областях. Поэтому команды объединяют специалистов с дополняющими друг друга компетенциями.

Одних технических навыков недостаточно. Analysts также должны применять critical thinking, problem solving и ясную коммуникацию, чтобы работать со сложностью incident и координироваться с другими командами и stakeholders.

### Incident Management

Incident management — более широкий организационный framework, окружающий техническую работу. Он включает coordination, communication, decision-making и governance, которые поддерживают и направляют response effort.

К этим функциям относятся:

- коммуникация со stakeholders — executives, legal, public relations, regulators и customers;
- resource allocation и escalation;
- cross-functional coordination — подключение legal counsel, human resources, insurance и law enforcement при необходимости;
- tracking timeline и documentation для compliance или litigation;
- ownership post-incident review и tracking remediation.

Если incident response сфокусирован на техническом разрешении инцидента, incident management обеспечивает координированное, документированное и обоснованное реагирование всей организации. Обе функции необходимы и на практике идут параллельно: responders расследуют и сдерживают угрозу, а managers координируют организационную сторону response.

Отношение между incident response и incident management не является строго иерархическим. В небольшой организации обе функции может выполнять одна команда или даже один человек. В крупной dedicated incident managers координируют работу нескольких response teams, business units и external parties. Независимо от масштаба организации разделение терминов помогает зафиксировать ожидания: responders сосредоточены на техническом разрешении incident, managers — на том, чтобы эта работа была обеспечена ресурсами, правильно коммуницировалась и соответствовала organizational objectives.

> Основная тема книги — incident response как техническая дисциплина обнаружения, расследования и разрешения security incidents. Однако responders должны понимать функции incident management, поскольку эффективное реагирование зависит от поддержки и координации, которую он обеспечивает. В Part 2: *A Dynamic Approach to Incident Response* представлена модель, охватывающая как технические, так и организационные аспекты incident handling.

В этой главе мы ввели базовую терминологию incident response: incidents, events, Events of Interest и Indicators of Compromise. Также были рассмотрены метрики, используемые для измерения detection и response effectiveness, и различие между incident response и incident management.

Далее мы рассмотрим модели incident response, которые организации используют для структурирования работы, а также ограничения, проявившиеся по мере роста сложности и масштаба инцидентов.

## Сноски и источники

[1] *Incident Response Recommendations and Considerations for Cyber Risk Management*, retrieved from `nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf`.

[2] Twingate, *Mr. Cooper Data Breach: What & How It Happened?* `www.twingate.com/blog/tips/Mr.%20Cooper-data-breach`

[3] Hutchins, E. M., Cloppert, M. J., Amin, R. M., Ph. D., & Lockheed Martin Corporation. *Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains*. `www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/cyber/LM-White-Paper-Intel-Driven-Defense.pdf`

[4] FortiGuard Labs. (2025, January 1). *Authentication bypass in Node.js websocket module and CSF requests*. `www.fortinet.com/blog/threat-research/fortiguard-labs-discovers-multiple-critical-vulnerabilities-in-adobe-reader`

[5] CrowdStrike. (2022, October 4). *IOA VS IOC*. `www.crowdstrike.com/en-us/cybersecurity-101/threat-intelligence/ioa-vs-ioc/`

[6] IBM Security, *Cost of a Data Breach Report 2024*. `www.ibm.com/reports/data-breach`

[7] Verizon, *2024 Data Breach Investigations Report*. `www.verizon.com/business/resources/reports/dbir/`

[8] Ponemon Institute, *The Cost of Cybercrime Study*, sponsored by Accenture, 2023.

[9] SANS Institute, *2025 SOC Survey*. `www.sans.org/white-papers/sans-2025-soc-survey`

[10] SANS Institute, *2025 SOC Survey*. `www.sans.org/white-papers/sans-2025-soc-survey`
