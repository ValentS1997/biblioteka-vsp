# Source findings — Глава 3

**Policy:** `rag_only`. Это журнал несоответствий текста/кода и непроверенных учебных инструкций. **Никаких молчаливых исправлений оригинальной книги, PDF, RAG или команд из внешних источников.** Наличие записи не означает, что исходник заведомо неверен.

## F-01 — [Source wording/code mismatch] — диагностика kind

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0134:c01`, PDF 134.
- **Формулировка книги:** «Для дополнительной отладки и диагностики проблем в кластере используйте команду `kubectl cluster-info dump`».
- **Непосредственно приведенная после нее команда:** `kubectl get --raw='/readyz?verbose'`, с примером вывода `readyz check passed`.
- **Расхождение:** текст и код называют разные CLI-операции; в RAG нет основания объявлять их равнозначными.
- **Действие:** оставить обе записи с точным происхождением, в командах для read-only проверки показывать только фактически приведенный пример для readiness. **Adjudication:** [Needs confirmation].

## F-02 — [Needs confirmation] — команда `kind stop`

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0134:c01`, раздел «Остановка и удаление локального кластера kind».
- **Формулировка книги:** `kind stop` описана как команда остановки кластера с сохранением состояния.
- **Проблема:** в рамках этой главы отсутствует успешный воспроизводимый пример вызова или проверка результата; гарантировать работоспособность команды на текущей установке нельзя.
- **Действие:** не предлагать `kind stop` как подтвержденную исполняемую операцию; оставить исходное написание и пометить [Needs confirmation] без самостоятельной замены.

## F-03 — [Source code mismatch] — имя кластера kind при удалении

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0131:c01` и `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0132:c01`.
- **Вариант создания:** `kind create cluster --name test-kind`, пример сообщает о создании `test-kind` (p0131).
- **Вариант удаления:** `kind delete cluster` без параметра имени, пример выводит `Deleting cluster "kind"` (p0132).
- **Риск:** по фрагментам нельзя подтвердить, что удаление воздействует на ранее созданный **именованный** кластер; нельзя считать команду безопасным соответствующим rollback.
- **Действие:** явно сохранять несоответствие; корректное удаление нужного кластера и его идентификация [Needs confirmation].

## F-04 — [Needs confirmation] — deprecated health API

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0125:c01` и `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0126:c01`.
- **Команда:** `kubectl get componentstatuses`.
- **Предупреждение в примере книги:** `Warning: v1 ComponentStatus is deprecated in v1.19+`.
- **Действие:** фиксировать предупреждение и не использовать вывод как универсальную проверку работоспособности современных установок; альтернативный production monitoring [Needs confirmation].

## F-05 — [Source extraction issue] — переносы CLI-фрагментов minikube

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0128:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0129:c01`.
- **Источник:** команды запуска с `--profile=cluster-vbox` / `--profile=clusterdocker` разбиты строками PDF так, что не всюду однозначно видно shell-продолжение.
- **Действие:** воспроизводить опции отдельно, не изобретать готовый вызов из неоднозначно разбитых строк; подтвержденная read-only команда `minikube profile list` приводится полностью.

## F-06 — [Needs confirmation] — версии, платформа, установка

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0118:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0120:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0121:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0130:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0131:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0133:c01`.
- **Источник:** примеры содержат конкретные сочетания `minikube v1.32.0`, Kubernetes `1.29.0/1.30.0`, `kind v0.20.0/v0.23.0`, образы с конкретными digest и загрузки `latest`.
- **Граница:** эти сочетания — исторические данные учебного примера; текущая совместимость, архитектура ЦП, права и целостность бинарников **не проверены**.
- **Действие:** не обновлять значения молча и не объявлять команды безопасным способом текущей установки без отдельной проверки/полномочий.

## F-07 — [Needs confirmation] — необратимое удаление учебной среды

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0127:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0134:c01`.
- **Источник:** `minikube delete` и `kind delete cluster` описаны как уничтожение кластера и его состояния без восстановления.
- **Действие:** удаление — отдельная потенциально разрушительная операция; **rollback отсутствует в главе** и должен оставаться [Needs confirmation]. Не использовать удаление как безрисковую операцию после `config set`.
