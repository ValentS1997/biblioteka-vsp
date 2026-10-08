# Cheatsheet — глава 32. Code, web, mail, cloud security

Источник: `computer-networks-olifer-7e-ru-2026`; PDF 1023–1049, RAG p1023:c01–p1049:c01 (27 chunks), **rag_only**. Нет наблюдений реальных хостов, веб-сервисов, писем и облачных систем.

## Symptom / problem framing

Сначала уточнить **где нарушается безопасность**: некорректная обработка входа/памяти, сомнительная программа или вложение, недостатки защиты браузера и cookie-session, недоверенный HTTPS endpoint, почтовое происхождение/содержимое/метаданные, неправильная граница cloud provider ↔ client. Разделять **security ресурсов**, **confidentiality/privacy**, **identity**, **availability** и **ответственность**.

## Baseline / context

| Подсистема | Важные объекты RAG | Страницы |
|---|---|---|
| Код/память | stack, input validation, permissions, undesired execution | 1023–1025 |
| Malware | trojan, worm, virus, software implant, botnet | 1025–1032 |
| Detection | signatures, heuristics, sandbox, quarantine, updates | 1030–1031 |
| Web/privacy | browser history, cookies, domain/scope/lifetime | 1032–1034 |
| HTTPS | authentication, server certificate/trust, protected HTTP | 1034–1036 |
| Dynamic pages | components, plugins, ActiveX/Java/JavaScript in textbook | 1036–1037 |
| Email | SMTP AUTH, S/MIME, certificates, PKCS-7/PGP | 1037–1041 |
| Metadata/spam | email metadata, DNSBL, attachments, scripts | 1041–1044 |
| Cloud | SaaS/PaaS/IaaS, tenancy, IAM/federation, jurisdiction, audit | 1044–1046 |
| Cloud benefits | replicas, distributed capacity/anycast, specialists | 1047–1049 |

## Read-only checks

1. **Code trust boundary:** по согласованной архитектуре определить источники недоверенных данных и, если есть разрешённая документация, как приложение проверяет тип/длину/диапазон значений. Отсутствие подтверждённой проверки — **[Needs confirmation]**, не доказанная exploitability. [p1023–p1025]
2. **Execution surface:** инвентаризованы ли исполняемые компоненты, приложения, расширения, macros, подписанный/неизвестный код? Разделены software owner и trust decision? [p1025–p1030, p1036–p1037]
3. **Detection:** имеются ли политика обновления сигнатур, отдельные heuristic/sandbox механизмы, процесс расследования карантина и защита самой антивирусной системы? Нельзя объявить endpoint safe по одному scan. [p1030–p1031]
4. **Botnet risk:** какие легитимно доступные журналы поддерживают вывод о нарушении, а какие лишь показывают обычный сетевой обмен? Исторический Citadel не означает текущего инцидента. [p1031–p1032]
5. **Browser privacy/session:** как используются history, cookie SID, cookie scope/lifetime, режимы сторонних cookies? Не собирать чужие SID и полные токены. [p1033–p1034]
6. **HTTPS trust:** существует ли HTTPS и подтверждена ли идентичность сервера, корректность домена и trust chain; отличать пользовательскую аутентификацию от аутентификации веб-сервера. Формулировки книги о client certificate/«TSL» — source caveats. [p1034–p1036]
7. **Email origin:** нужно ли проверить SMTP-provider authentication или end-to-end подпись конкретного отправителя? Почтовые подпись, шифрование и доставка между relay — разные механизмы. [p1037–p1041]
8. **Email privacy:** как отделены encrypted body, SMTP hop, exposed metadata и stored messages; имеются ли разрешённые правила retention/audit? Историческое утверждение книги о законности сбора метаданных **не** переносить в текущую юрисдикцию. [p1041–p1043]
9. **Mail filtering:** какая область DNSBL, сканирования attachments и политики работы со скриптами/макросами? False positives и условия блокировки требуют согласования. [p1043–p1044]
10. **Cloud responsibility:** кто владеет security приложений/OS/контрольных точек в SaaS/PaaS/IaaS; есть ли договорный доступ к security logs, provider attestations, backup and escalation? [p1044–p1045]
11. **Cloud identity/residency:** как защищены cloud accounts/administrative connections, tenant isolation и персональные данные; где они хранятся, обрабатываются, откуда доступны? [p1045–p1046]
12. **Cloud resilience:** основана ли требуемая доступность на проверенных replicas, fault domains, routing и capacity, а не на самом названии «облако»? [p1047–p1049]

## Interpretation

- Класс malware и техническая уязвимость — не одно и то же; сигнатура фиксирует известный признак, heuristic может дать ложное срабатывание.
- История браузера и email metadata являются предметом privacy review, даже если body зашифрован.
- Cookie — не исполнимый код, но SID может быть чувствительным идентификатором сеанса.
- HTTPS transport protection не заменяет проверку авторизации приложения или политики хранения данных.
- SMTP AUTH/подпись письма/S/MIME encryption охватывают разные threat surfaces.
- SaaS/PaaS/IaaS различаются распределением обязанностей; обязанность клиента не исчезает при аутсорсинге.
- Избыточность облака может повысить availability, но не доказывает безусловной защищённости каждого провайдера.

## Next action

Создать **read-only accountability map**: trusted/untrusted input → execution boundary → web session/certificates → mail origin/body/metadata → cloud provider/client obligations. Связать её с уже доступными SLA, security policies, audit rights и данными согласованной среды. Не собирать персональные данные или секреты сверх необходимого. Недостающая фактура **[Needs confirmation]**.

## Modifying action

Правки browser cookie policy, authentication, certificate trust, AV quarantine, attachment rules, mail relay, SPF-like policies (не описаны в главе), cloud tenancy, federated authentication или backup могут остановить доступ, утратить данные либо нарушить privacy. Никакая из них **не следует** как обязательная процедура из RAG; каждое изменение требует approved scope, environment, test and owner.

## Verification / acceptance checks

- Отделены факты исходника, наблюдения среды и допущения.
- Проверены границы execution/session/encryption/identity/provider.
- Legacy ActiveX, TSL, PGP/PKCS-7 и AV заявления не считаются текущей нормативной реализацией.
- Для заявленной безопасности есть версия/owner/evidence; без них статус **[Needs confirmation]**.
- В материалах нет эксплойт-процедур, неподтверждённых CLI, live credentials или выдачи чужих данных.

## Rollback

Read-only review — **[Not applicable]**. Реальный rollback настроек web/mail/cloud требует backup исходных конфигураций, восстановление прав доступа, validation данных, критерии приемки и процедуры инцидентного восстановления: **[Needs confirmation]**. Изменений не проводилось.
