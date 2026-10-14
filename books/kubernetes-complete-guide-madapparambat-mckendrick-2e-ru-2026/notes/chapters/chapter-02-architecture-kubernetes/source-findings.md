# Source findings — Глава 2

**Policy:** RAG-only, без внешней проверки и исправления оригинального PDF/RAG. Эти записи фиксируют исходные формулировки и границы их применимости, а **не** объявляют утверждения книги доказанно ошибочными.

## F-01 — [Needs confirmation] / defaults kubelet

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0094:c01`; таблица `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0113:c01`.
- **Источник:** `kubelet` описывается как HTTP GET-polling каждые 20 секунд, с конфигурацией `/etc/kubernetes/kubelet.conf`, которая в тексте представлена как содержащая и API endpoint, и Unix socket runtime.
- **Вопрос:** конкретный интервал и источник эффективной конфигурации не проверены для версии или дистрибутива кластера; в той же главе используются «watch mechanisms» (p0094). Без исходного реального запуска не делать диагностику на основе обещанного интервала.
- **Решение:** сохранить обе исходные формулировки, отметить как version/distribution dependent; внешняя адъюдикация [Needs confirmation].

## F-02 — [Needs confirmation] / etcd access boundary

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0084:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0085:c01`.
- **Источник:** заявлено, что исключительно `kube-apiserver` может читать/писать данные в etcd, и что `etcd` «реализован как REST API» на порту 2379.
- **Вопрос:** эти формулировки приведены как общие технические утверждения без версии/конфигурации и проверяемого CLI-примера. Запрещать/допускать прямое подключение в конкретной инфраструктуре по одному этому тексту нельзя.
- **Решение:** описывать **архитектурный рекомендуемый путь Kubernetes-компонентов через API**, а не заявлять универсальную невозможность любого иного клиента; не менять источник. Проверка [Needs confirmation].

## F-03 — [Source wording/code mismatch] / kubectl get pods scope

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0103:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0104:c01`.
- **Источник:** `kubectl get pods` описан как получение подов «в вашем кластере», при этом соседний пример использует явный `-n my-namespace` для доступа к ReplicaSet.
- **Неопределенность:** формулировка не устанавливает точную namespace-область для `kubectl get pods`. При переносе в runbook не считать вывод исчерпывающим списком всех namespace без проверки.
- **Решение:** сохранить команду без изменения и отметить область результатов [Needs confirmation].

## F-04 — [Needs confirmation] / installed-version examples

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0096:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0097:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0098:c01`.
- **Источник:** примеры загрузки `kubectl` версии v1.30.0, используются прямой `curl`, `chmod`, `sudo mv` и путь `/usr/local/bin/kubectl`.
- **Граница:** текущая версия кластера, нужная архитектура CPU, проверка скачанного бинарника и последствия замены установленного клиента в главе не подтверждены.
- **Решение:** только учебная фиксация команд; не превращать в unattended production installation.

## F-05 — [Needs confirmation] / CRI socket and node deployment

- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0092:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0094:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0095:c01`.
- **Источник:** перечислены стандартные Unix-socket пути для `containerd`, `CRI-O`, `cri-dockerd` и описана модель `kubelet ↔ runtime`.
- **Граница:** действительный socket endpoint, kubelet flags и root privileges конкретного узла отсутствуют. Авторский запрет монтирования runtime-socket в контейнеры (p0095) должен оставаться явным security boundary.
- **Решение:** не подменять извлеченные пути и не выполнять обращения к socket без проверки.

**Conflicting source variants:** не замещать модельной памятью. Классификация F-03 касается несоответствия буквальной широкой формулировки области действия конкретной команде; требуется подтверждение в реальном окружении.
