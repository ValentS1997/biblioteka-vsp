# Команды, инструменты и интерфейсы главы 1

## Source-confirmed CLI commands

В проверенной границе главы 1 нет явных строк команд Docker или Kubernetes.

Поэтому команды вроде `docker ...` или `kubectl ...` здесь намеренно не реконструируются из памяти. Практический CLI начинается в следующей главе.

## Инструменты и компоненты, явно поддержанные главой

| Инструмент / компонент | Роль по главе | Классификация |
|---|---|---|
| Docker | Упаковка, распространение и запуск контейнеризированных приложений | workload-generating / state-changing как платформа; CLI syntax отсутствует |
| rkt | Альтернативная container runtime/platform, упомянутая рядом с Docker | workload-generating; CLI syntax отсутствует |
| OCI | Открытые отраслевые стандарты для форматов и runtime контейнеров | interface/standard, не команда |
| Image | Упакованное приложение, файловая система и метаданные запуска | artifact |
| Registry | Хранилище и распространение images | stateful service |
| Container | Изолированный процесс, создаваемый из image | workload |
| Linux namespaces | Изоляция представления ресурсов для процесса | kernel mechanism |
| cgroups | Ограничение ресурсов процесса/группы процессов | kernel mechanism |
| Kubernetes API server | Точка взаимодействия пользователей и компонентов control plane; принимает описание приложения | state-changing interface |
| Scheduler | Назначает компоненты приложения рабочим узлам | control-plane component |
| Controller Manager | Выполняет кластерные функции, включая репликацию и обработку отказов | control-plane component |
| etcd | Надёжно хранит конфигурацию/состояние кластера | state store |
| Kubelet | Агент рабочего узла, взаимодействует с API server и управляет контейнерами на узле | node agent |
| kube-proxy | Балансирует сетевой трафик между компонентами приложения | network component |
| Container runtime | Получает images и запускает containers | workload-generating component |
| DNS | Один из способов обнаружения службы приложением | read-only discovery interface |
| Environment variables | Один из способов передачи приложению информации для обнаружения службы | read-only discovery interface |
| HTTP / RESTful API | Синхронное взаимодействие между микросервисами | application protocol/interface |
| AMQP | Асинхронное взаимодействие между микросервисами | application protocol/interface |

## Поддержанный workflow развертывания

Глава описывает последовательность без командного синтаксиса:

```text
Application
  ↓ package
Container image
  ↓ push/store
Image registry
  ↓ reference from application description
Kubernetes API server
  ↓
Scheduler
  ↓ assigns workload
Worker node
  ↓
Kubelet
  ↓
Container runtime
  ↓ pull image + start container
Running application
```

## Read-only

Явные CLI read-only команды: `[Not applicable in chapter 1]`.

Read-only механизмы, упомянутые на уровне приложений:

- DNS lookup для обнаружения службы;
- чтение определённых environment variables для обнаружения службы;
- запрос Kubernetes API для получения информации — сам факт запроса описан, конкретный endpoint/command не приводится.

## Workload-generating

Поддержанные концептуальные действия:

- запуск container из image;
- запуск требуемого количества реплик;
- получение image из registry на worker node.

CLI syntax: `[Needs confirmation from later chapter]`.

## State-changing

Поддержанные концептуальные действия:

- публикация описания приложения на API server;
- изменение требуемого количества копий;
- автоматическое переразмещение workload при отказе узла;
- изменение размера кластера в облачной среде — описано как возможная автоматизация.

Конкретные команды, параметры и API payload: `[Needs confirmation]`.

## Verification

Глава задаёт только поведенческие критерии:

- фактическое число экземпляров соответствует описанному;
- отказавший экземпляр заменяется;
- workload переносится при отказе узла;
- служба остаётся доступной через стабильный IP;
- kube-proxy распределяет подключения между контейнерами службы.

Команды проверки: `[Needs confirmation from later chapters]`.

## Rollback

`[Needs confirmation]`

В главе упоминается возможность обнаружить плохую новую версию и остановить её выкладку, но конкретный механизм и команды rollback не приведены.
