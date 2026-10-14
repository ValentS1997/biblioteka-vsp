# Source findings — Глава 4

**Source policy:** `rag_only`; PDF 143–180. Эти записи сохраняют спорные формулировки книги и границы применимости, **не** объявляя их исправленными с помощью внешней документации или модельной памяти. Вердикты: [Needs confirmation].

## F-01 — [Source wording/code mismatch]: kubectl apply для существующего Pod

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0151:c01`, `…:p0153:c01`.
- **Вариант 1:** в p0151–p0153 `kubectl apply -f` служит декларативному применению YAML.
- **Вариант 2:** p0153 утверждает, что существующий `nginx-pod` обязательно приведёт к ошибке `kubectl apply -f nginx-pod.yaml`, и предлагает изменить имя.
- **Uncertainty:** нет наблюдения конкретного ранее существовавшего ресурса и его полей. Не объявлять этот исход универсальным, не корректировать source silently. **[Needs confirmation]**.

## F-02 — [Needs confirmation]: restartPolicy Never vs Job retries

- **RAG:** `…:p0167:c01`, `…:p0168:c01`.
- **Source:** `OnFailure` описан через перезапуск контейнера/пода; для `Never` p0168 утверждает, что «объект Job не будет перезапускать поды» при сбое.
- **Boundary:** текст не разделяет полностью контейнерный restart policy и логику контроллера Job и не дает проверенного поведения всех failure modes. Нельзя считать `Never` гарантией отсутствия новых Pod. **[Needs confirmation]**.

## F-03 — [Source wording/code mismatch]: parallelism без completions

- **RAG:** `…:p0169:c01`, `…:p0170:c01`, `…:p0171:c01`.
- **Вариант 1:** `completions: 10` описывается как десять последовательных выполнений.
- **Вариант 2:** p0170 говорит, что при `parallelism: 5` параметр `completions` «становится ненужным»; манифест p0170 его не содержит, p0171 сообщает о пяти одновременно создаваемых Pod.
- **Boundary:** дефолтное число завершений, фактическая конкуррентность и итоговые retries конкретного кластера не подтверждены. Не подменять исходный пример новым манифестом. **[Needs confirmation]**.

## F-04 — [Needs confirmation]: activeDeadlineSeconds и короткие задачи

- **RAG:** `…:p0171:c01`.
- **Source:** `activeDeadlineSeconds: 60` интерпретирован как «выполнение задания завершится через 60 секунд независимо от обстоятельств».
- **Boundary:** в тексте недостаточно данных, чтобы считать заданную продолжительность фактическим временем работы независимо от успешного более раннего завершения. **[Needs confirmation]**.

## F-05 — [Source wording/code mismatch]: Job delete --cascade=false

- **RAG:** `…:p0172:c01`, `…:p0173:c01`.
- **Вариант 1:** p0172 описывает `kubectl delete jobs hello-world-job` как удаление Job и Pod; `kubectl delete jobs hello-world-job --cascade=false` — как удаление Job с сохранением Pod.
- **Вариант 2:** p0173 начинает с «Эта команда позволяет вам избавляться от всех завершенных заданий…», что может быть прочитано как расширенная область удаления.
- **Action:** не объявлять удаление всех Job эффектом команды, проверять конкретное имя и Pod; **[Needs confirmation]**.

## F-06 — [Source contradiction]: «все процессы приложения в одном Pod» и разделение слоев

- **RAG:** `…:p0145:c01`, `…:p0149:c01`.
- **Source A:** p0145 формулирует правило объединения всех контейнеров и процессов приложения в одном Pod, пример Nginx/PHP-FPM.
- **Source B:** p0149 рекомендует запуск СУБД и WordPress в разных Pod.
- **Scope:** разные границы понятия «приложение» и его слоев; в notes сохранены обе позиции без вывода, что всю систему следует поместить в один Pod. **[Needs confirmation]**.

## F-07 — [Needs confirmation]: image digest и runtime версия

- **RAG:** `…:p0151:c01`, `…:p0152:c01`.
- **Source:** `nginx:latest` противопоставлен `nginx@sha256:1445eb9c6dc5e9619346c836ef6fbd6a95092e4663f27dcfce116f051cdbd232`, для просмотра показан `podman manifest inspect nginx:latest`.
- **Boundary:** актуальные registry, digest, платформа и доверенность образа не проверены. **[Needs confirmation]**.

## F-08 — [Needs confirmation]: история CronJob и Pod

- **RAG:** `…:p0177:c01`, `…:p0178:c01`.
- **Source:** `successfulJobsHistoryLimit: 5` и утверждение о видимости «только последних пяти заданий или запущенных подов»; в примере по `get pods` показаны пять.
- **Boundary:** точная судьба дочерних Pod и других параллельных Job из данного примера не выводится, источник не дает универсальных гарантий их очистки. **[Needs confirmation]**.

**Operational risk:** `delete`, `replace`, `label`, `exec`, `port-forward` и периодический `CronJob` описаны как учебные действия; реальная цель, права, rollback и последствия не проверены.
