# Шпаргалка: контейнеризация и Docker

Цель: удерживать модель главы 1 — зачем нужны контейнеры, какую роль играет Docker и где находятся основные границы архитектуры и безопасности.

## Symptom / problem framing

Глава связывает контейнеризацию с несколькими исходными проблемами:

- физические серверы часто приобретались с большим запасом мощности и использовались неэффективно;
- виртуальные машины улучшают утилизацию оборудования, но каждая ВМ требует отдельной ОС;
- различия между development/test/production приводят к отказам после развёртывания;
- монолитные приложения трудно изменять, развёртывать и масштабировать частями;
- доступ к Docker daemon и общим каталогам хоста создаёт значимую security boundary.

## Baseline / context

### VM и контейнер

```text
Virtual machine
application
guest OS
hypervisor
host / hardware

Container
application + runtime + dependencies
container isolation
shared host OS / kernel
hardware
```

В логике главы контейнер легче ВМ, потому что ему не нужна отдельная ОС. Несколько контейнеров используют ядро хоста.

### Docker Engine

```text
Docker CLI / API client
        ↓
      REST API
        ↓
   Docker daemon
        ↓
containers / images / networks / storage / volumes
```

Docker Engine представлен как клиент-серверное приложение.

### Registry

Docker Registry хранит и доставляет образы, различая их по тегам. Registry может быть публичным или закрытым. Docker Hub описан как облачный репозиторий для образов.

## Read-only checks

В главе 1 нет полноценного набора диагностических shell-команд.

Явно названы:

- Docker CLI как интерфейс;
- Docker REST API;
- операции `push` и `pull` для отправки и получения образов из registry.

Полный shell-синтаксис этих операций в главе не приводится, поэтому команды вида `docker ...` здесь не реконструируются.

Operational checks: `[Not applicable in chapter 1]`.

## Interpretation

### Если проблема — избыточные накладные расходы ВМ

Модель главы указывает на контейнеры как на более лёгкую единицу изоляции: отдельная гостевая ОС для каждого контейнера не требуется.

### Если приложение работает по-разному в разных средах

Глава связывает контейнеризацию с упаковкой приложения вместе с конфигурацией, библиотеками и зависимостями. Это уменьшает различия runtime-сред.

### Если нужна независимая доставка компонентов

Микросервисы имеют чёткие границы и могут развертываться, обновляться и масштабироваться независимо. Контейнеры дают им изолированную среду.

### Если вопрос о том, кто выполняет Docker-операции

Клиент Docker взаимодействует с Docker daemon через REST API, Unix socket или сетевой интерфейс. Демон выполняет основную работу с объектами Docker.

### Если вопрос о доставке образов

Registry — слой хранения и доставки образов по тегам. `push` отправляет образ в registry, `pull` получает его.

### Если вопрос о безопасности

Проверить концептуальную границу:

1. namespaces — изоляция процессов;
2. cgroups — ограничения ресурсов;
3. отдельная сетевой инфраструктура контейнера;
4. доступ к Docker daemon — только доверенным пользователям;
5. capabilities — оставлять только необходимые права;
6. Docker Content Trust — запуск подписанных образов;
7. общие каталоги контейнера и хоста — потенциальный риск.

## Next action

После определения категории перейти к более детальному слою:

```text
container basics / images
        → chapter 2

storage / volumes
        → chapter 3

Swarm / orchestration
        → later chapters

security
        → chapters 7–8
```

В рамках главы 1 не добавлять эксплуатационные команды из внешнего знания.

## Modifying action

`[Not applicable]`

Глава не задаёт законченного административного workflow с командами изменения состояния.

Операции `push` и `pull` упомянуты как операции с registry, но точный shell-синтаксис и rollback в главе не определены.

## Verification / acceptance checks

Понимание главы можно считать достаточным, если можно объяснить:

- почему контейнер легче ВМ;
- что именно упаковывается в контейнер;
- почему контейнеры уменьшают расхождения между средами;
- из каких трёх компонентов состоит Docker Engine;
- зачем нужен Docker Registry;
- почему контейнеры хорошо сочетаются с микросервисами;
- какие security boundaries перечислены в главе.

Командные acceptance checks: `[Not applicable in chapter 1]`.

## Rollback

`[Not applicable]`

Глава не содержит законченных state-changing процедур с определённым rollback.

## Минимальная карта памяти

```text
Containerization
├─ app + runtime + dependencies
├─ shared host kernel
├─ fast / lightweight
├─ portable runtime
└─ isolated execution

Docker
├─ CLI
├─ REST API
├─ daemon
├─ Registry / Hub
└─ orchestration: Swarm

Microservices
└─ independent deploy / update / scale

Security
├─ namespaces
├─ cgroups
├─ network isolation
├─ daemon access
├─ capabilities
└─ Docker Content Trust
```
