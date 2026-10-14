# Source findings — Глава 5

**Policy:** `rag_only`; PDF 181–217. Записи сохраняют противоречия/неоднозначности исходника. Они **не** являются исправлением книги по памяти модели или внешним источникам. Для интерпретации/исполнения при расхождении ставится **[Needs confirmation]**.

## F-01 — [Source code mismatch] — имя диагностического Pod

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0186:c01`, `…:p0187:c01`.
- **YAML:** имя файла `failed-multi-container-pod.yaml`, однако `metadata.name: multi-container-pod`.
- **CLI/result:** `kubectl apply -f failed-multi-container-pod.yaml` сопровождается результатом `pod/failed-multi-container-pod created`; последующие `get` и `describe` используют `failed-multi-container-pod`.
- **Resolution:** не превращать это в рабочую воспроизводимую лабораторию и не менять исходное `metadata.name` без отдельной проверки. **[Needs confirmation]**.

## F-02 — [Source wording/code mismatch] — удаление именованного Pod названо императивным

- **RAG:** `…:p0188:c01`.
- **Текст:** говорит об «императивном способе, без указания пути к YAML-файлу».
- **Непосредственный пример:** `kubectl delete -f failed-multi-container-pod.yaml` — команда **с** путем к манифесту.
- **Resolution:** фиксировать обе формулировки, не смешивать способ удаления по имени (`kubectl delete pods/multi-container-pod`) с применением `-f`.

## F-03 — [Source contradiction] — обязателен ли --container

- **RAG:** `…:p0191:c01`, `…:p0192:c01`, `…:p0198:c01`.
- **Вариант A:** p0191 утверждает, что `--container` при нескольких контейнерах «обязателен, иначе Kubernetes не будет знать, к какому контейнеру подключиться».
- **Вариант B:** p0192 объясняет выбор первого контейнера при пропуске имени; p0198 допускает контейнер по умолчанию для логов.
- **Resolution:** в runbook явно задавать `-c` для определённости; без проверки целевого Pod не выдавать один вариант за универсальное техническое правило. **[Needs confirmation]**.

## F-04 — [Source wording/code mismatch] — путь hostPath и место узла minikube

- **RAG:** `…:p0204:c01`, `…:p0205:c01`, `…:p0206:c01`.
- **Вариант A:** текст p0204 описывает локальный компьютер как host в одноузловом minikube и обещает смонтировать файл `worker-node/nginx.conf` по пути `/var/config/nginx.conf`.
- **Вариант B:** YAML p0205 фактически монтирует `hostPath.path: /tmp` в `mountPath: /foo` у Nginx; p0205 затем создаёт файл через `minikube ssh` **внутри виртуальной машины**.
- **Resolution:** нельзя полагаться на файлы произвольного физического ноутбука при запуске с VM-драйвером; фактическая файловая система узла и источник пути **[Needs confirmation]**. Отмечено как пример, а не безопасная инструкция production.

## F-05 — [Source code mismatch] — имя файла Adapter

- **RAG:** `…:p0214:c01`, `…:p0215:c01`.
- **Manifest heading:** `# alpine-with-adapter.yaml`, `metadata.name: pod-with-adapter`.
- **Команда:** `kubectl apply -f nginx-with-adapter.yaml`, вывод `pod/pod-with-adapter created`.
- **Resolution:** нельзя гарантировать наличие `nginx-with-adapter.yaml` или подменить имя исходного YAML. Без отдельного подтверждения файлы не считаются согласованным скриптом.

## F-06 — [Needs confirmation] — Sidecar и Job, жизненный цикл

- **RAG:** `…:p0210:c01`, `…:p0211:c01`, `…:p0215:c01`, `…:p0216:c01`.
- **Source:** p0210 заявляет, что отказ классического Sidecar не влияет на основной контейнер. p0211 утверждает, что Sidecar в Job «не препятствуют успешному завершению задания» без дополнительной настройки. p0215 одновременно описывает проблему традиционного Sidecar, способного работать после завершения основного приложения; p0216 показывает нативный sidecar в `initContainers` с `restartPolicy: Always`.
- **Boundary:** книга использует слово Sidecar как для обычного контейнера, так и для специального варианта lifecycle; фактическое поведение и readiness/завершение Job **[Needs confirmation]**. Не использовать общие обещания как критерии приёмки.

## F-07 — [Needs confirmation] — демонстрационный Fluentd и SQL Ambassador

- **RAG:** `…:p0208:c01`, `…:p0211:c01`, `…:p0212:c01`.
- **Ambassador:** демонстрационный `mysql-proxy:latest` с `DB_HOST` (RDS) не сопровождается подтверждённым развернутым SQL-прокси или реальной БД; сам источник отмечает потребность в подготовленной среде.
- **Sidecar:** `nginx-with-fluentd-sidecar.yaml` содержит `emptyDir` для логов и `fluent/fluentd:v1.17`; текст даёт отдельный ConfigMap `fluentd.conf`, но в показанном Pod **нет явного volumeMount/config wiring этого ConfigMap**.
- **Boundary:** завершённая работающая конфигурация Fluentd/RDS без настройки вне источника **[Needs confirmation]**. Демонстрационные адреса не считать реальными целями.

## F-08 — [Needs confirmation] — нативные sidecar и поддержка версии

- **RAG:** `…:p0215:c01`, `…:p0216:c01`.
- **Source:** утверждение о добавлении native sidecars в Kubernetes v1.28; далее приводится **фрагмент**, а не целый Deployment, с `initContainers[*].restartPolicy: Always`.
- **Boundary:** текущее состояние поддержки конкретного Kubernetes/feature gate и полный применимый manifest **[Needs confirmation]**. Не конструировать отсутствующие поля из памяти.

## F-09 — [Needs confirmation] — абсолютные утверждения о Pod volumes

- **RAG:** `…:p0199:c01`, `…:p0200:c01`, `…:p0203:c01`.
- **Source:** p0199 сначала обобщает, что все volumes существуют ровно столько, сколько Pod, а при его удалении удаляются все связанные тома; p0200 тут же отмечает исключения и упоминает внешние хранилища/PVC.
- **Boundary:** подтверждённая потеря данных относится к `emptyDir` из p0203; этот вывод нельзя автоматически распространять на `hostPath`/NFS/PV/PVC. **[Needs confirmation]**.

**Operational risk:** `kubectl delete --grace-period=0 --force` прямо предупреждает о возможной продолжающейся работе (p0189). External init-контент, NodePort, hostPath и runtime privileged shell требуют отдельного разрешения. PDF/RAG остаются неизменными.
