# Команды, операции и интерфейсы главы 1

Глава 1 почти полностью концептуальная. Ниже перечислены только элементы, явно подтверждённые RAG главы. Полный shell-синтаксис Docker-команд из внешнего знания не добавляется.

| Элемент | Роль в главе | Тип | Effect / риск | Verification | Rollback |
|---|---|---|---|---|---|
| Docker CLI | Интерфейс командной строки для взаимодействия с Docker daemon | interface | Сам по себе не определяет изменение; эффект зависит от операции | В главе отдельная проверка CLI не приводится | `[Not applicable]` |
| Docker REST API | Интерфейс взаимодействия приложений/клиента с Docker daemon | interface | Позволяет управлять объектами Docker через демон | В главе отдельная проверка API не приводится | `[Not applicable]` |
| `push` | Отправка образа в registry | state-changing | Публикует/загружает образ в registry; точный синтаксис в главе отсутствует | `[Needs confirmation]` | `[Needs confirmation]` |
| `pull` | Получение образа из registry | state-changing | Загружает образ из registry в локальное окружение; точный синтаксис в главе отсутствует | `[Needs confirmation]` | `[Needs confirmation]` |

## Docker Engine: интерфейс взаимодействия

```text
client / CLI
    │
    ├─ REST API
    ├─ Unix socket
    └─ network interface
           ↓
       Docker daemon
           ↓
 containers / images / networks / storage / volumes
```

Глава прямо указывает, что Docker daemon выполняет работу по созданию, администрированию и контролю объектов Docker.

## Registry operations

Источник описывает две операции:

```text
local image -- push --> Registry
local host  <-- pull -- Registry image
```

Полные команды `docker push ...` и `docker pull ...` в границе главы 1 не показаны, поэтому они намеренно не представлены как готовые copy-paste команды.

## Operational boundary

- Явных read-only shell-команд в главе 1 нет.
- Завершённых state-changing административных процедур нет.
- Проверки результата и rollback для `push`/`pull` глава 1 не задаёт: `[Needs confirmation]`.
- Практическое выполнение Docker-команд начинается в следующей главе.
