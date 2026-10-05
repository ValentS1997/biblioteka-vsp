# Итог главы 3

## Заключение

Глава 3 разделяет хранение данных в Docker на container writable layer и внешнее persistent/temporary storage.

Storage driver записывает изменения на thin read-write layer контейнера. Этот путь предназначен главным образом для небольшого объёма данных и не считается оптимальным для write-intensive persistent workloads. Выбор driver зависит от kernel/backing filesystem, производительности и стабильности.

В контексте книги предпочтительным driver является `overlay2`. OverlayFS объединяет lower read-only layers и upper writable layer через union mount. `lowerdir` представляет нижние слои, `upperdir` — изменения, `diff` хранит layer differences, `work` используется OverlayFS, а merged view формирует файловую систему container.

Глава показывает, как проверить kernel module и текущий storage driver, а также демонстрирует смену driver через `daemon.json`. Перед этим Docker останавливается, а `/var/lib/docker` копируется в backup. Это state-changing и disruptive операция.

Для persistence используются volumes и bind mounts. Bind mount связывает произвольный host directory с directory container. Docker volume использует Docker-managed storage area; volume может быть anonymous или named. Named volume упрощает управление и может быть подключён к нескольким containers.

tmpfs отличается от volumes/bind mounts тем, что использует host RAM и не сохраняет данные после остановки container.

## Основные тезисы источника

- Данные container по умолчанию записываются на thin read-write layer.
- Writable layer подходит для относительно небольших объёмов данных.
- Storage driver управляет записью данных на этот layer.
- Driver нужно выбирать с учётом kernel и backing filesystem.
- В контексте книги предпочтительный driver — overlay2.
- Overlay2 использует lowerdir/upperdir и union mount.
- Верхние layers хранят differences, а не полные копии.
- Для persistence используются volumes и bind mounts.
- Volume хранится в Docker-managed area host.
- Bind mount использует произвольный host path.
- Named volume можно разделять между несколькими containers.
- tmpfs размещает данные в памяти host и не обеспечивает persistence после stop.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| Storage driver | Механизм записи данных на container read-write layer |
| Backing filesystem | Host filesystem, на которой хранится Docker data root |
| OverlayFS | Union filesystem, лежащая в основе overlay/overlay2 |
| lowerdir | Нижние read-only layers |
| upperdir | Верхний writable layer с изменениями |
| union mount | Объединённое представление lower + upper |
| diff | Отличия, сохранённые в layer |
| Volume | Docker-managed persistent host storage, mapped into container |
| Volume driver | Дополнительный механизм хранения/переноса/шифрования volume data |
| Bind mount | Mount произвольного host path в container |
| Anonymous volume | Volume без user-friendly name, source выбирает Docker |
| Named volume | Volume с заданным именем и Docker-managed mountpoint |
| tmpfs | Temporary filesystem в host RAM |

## Provenance

- Chapter RAG: `p0059:c01`–`p0075:c01`
- PDF pages: 59–75
- Printed pages: 63–79
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
