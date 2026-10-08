# Команды, технологии и проверки — глава 32

**Source:** PDF 1023–1049, RAG p1023:c01–p1049:c01, strict `rag_only`.

## Исполнимый CLI

**В каноническом тексте главы 32 не обнаружены конкретные проверенные CLI-команды** для выполнения аудита, настройки web/mail/cloud, обезвреживания вредоносного ПО либо проверки сертификатов. Имена HTTP/HTTPS, SMTP AUTH, S/MIME, DNSBL, VM, SaaS, PaaS, IaaS и sandbox — **названия технологий**, не готовые команды. Исполнимые команды из памяти модели не добавлялись.

## Source-confirmed technologies и режим работы

| Технология / действие | Смысл в тексте | Класс и граница | RAG |
|---|---|---|---|
| Проверка недоверенных данных | Контроль входа по ожидаемому формату и допустимым значениям | read-only: code review; изменение валидатора **state-changing** | p1023–p1025 |
| Non-executable stack / память процесса | Ограничение исполнения при повреждении стека | чтение security properties read-only; изменение OS mitigation **state-changing** | p1023–p1024 |
| Signature matching / AV updates | Сопоставление с библиотекой и обновление баз | проверка состояния read-only; update **state-changing** | p1030–p1031 |
| Heuristic static/dynamic / VM sandbox | Анализ структуры/поведения подозрительной программы | dynamic execution **workload-generating**, isolate; sandbox не 100% гарантия | p1031 |
| Quarantine / removal | Изоляция обнаруженного образца | **state-changing**, возможны false positive и disruption | p1031 |
| Cookie SID / domain / expiry | Привязка запросов к сеансу браузера | проверка политики read-only, выдача/отзыв cookies state-changing; не раскрывать SID | p1033–p1034 |
| HTTPS and server certificates | Защищённый обмен, проверка подлинности сервера | наблюдать config metadata read-only, изменение trust **state-changing** | p1034–p1036 |
| ActiveX / Java/JavaScript components | Пример динамического кода в веб-приложении | historical browser context, features/version [Needs confirmation] | p1036–p1037 |
| SMTP AUTH | Проверка отправителя при передаче на сервер провайдера | login/access session, секреты; не эквивалент end-to-end author identity | p1038–p1039 |
| S/MIME, PKCS-7, PGP | Цифровая подпись и шифрование почтового содержимого | crypto action; нельзя создавать действительные keys from source | p1039–p1041 |
| Protected mail relay channel | Защита на отдельном участке почтового маршрута | настройка **state-changing**, end-to-end не гарантирована | p1041 |
| DNSBL | Blacklist based mail filtering | read-only inspection / updates **state-changing**, false positive possible | p1043 |
| Attachment/macro inspection | Защита от вредоносных вложений | scan **workload-generating**; quarantine state-changing | p1043–p1044 |
| Cloud SLA/security audit | Доступ к журналам провайдера и договорные обязанности | read-only review; contract/policy updates state-changing | p1044–p1045 |
| Cloud federation / identities | Локальная справочная служба и взаимодействие с провайдером | sensitive state, SSO implementation details [Needs confirmation] | p1046 |
| Cloud replicas, anycast, DDoS filtering | Положительные свойства распределённого провайдера | архитектура и monitoring, не существующий service guarantee | p1047–p1049 |

## Source examples — не шаблоны внедрения

- `HTTPS` связан с защищённым HTTP, но source использует обозначение `TSL` и утверждает, будто у каждой стороны обязательно есть CA-сертификат. Это отмечено в source-findings; нельзя выводить готовую конфигурацию TLS/client authentication.
- `S/MIME`, `PKCS-7`, `PGP` обозначают разные способы подписи/шифрования. Raw MIME пример Microsoft Windows Mail/Apple Mail с `SHA1` — исторический, не сертификация соответствия современной crypto policy.
- `SaaS / PaaS / IaaS` — разные границы управления; в текстовом RAG нет действующей матрицы ответственности какого-либо провайдера.

## Preconditions / verify / rollback

**Read-only:** просмотр разрешённой документации, опубликованных vendor/security policies и минимизированных audit summaries без секретов. **Workload:** загрузка образцов в sandbox, активные сканирования и packet inspection — только с разрешением и изоляцией. **State-changing:** quarantine, trust store, cookies, mail filtering, cloud IAM и backup. Источник не предоставляет версии продуктов, доступа, rehearsal, post-change acceptance или проверенного rollback. Все такие поля — **[Needs confirmation]**. Никакие команды/изменения не выполнялись.
