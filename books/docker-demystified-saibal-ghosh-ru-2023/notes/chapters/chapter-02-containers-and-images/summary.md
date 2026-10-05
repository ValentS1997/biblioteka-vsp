# Итог главы 2

## Заключение

Глава 2 даёт базовую operational-модель containers и images Docker. Container создаётся из image и получает собственный thin read-write layer. Image остаётся immutable и может служить основой для любого количества containers.

Lifecycle container описывается состояниями Created, Running, Paused, Exited, Restarting, Dead и Stopped. Для observation используются `docker ps` / `docker container ls -a`; управление показано через run, pause, unpause, stop и create.

Для работы внутри container используется `docker exec`, а для детальной информации — `docker inspect`. Inspect возвращает JSON с состоянием, образом, PID, ExitCode, storage/network fields и служебными путями.

Logs связаны со stdout/stderr и logging driver. В примере default driver — `json-file`, а локальные записи располагаются под `/var/lib/docker/containers/<id>`. Для диагностики используются `docker logs`, follow, tail, timestamps и grep. Для больших сред источник подчёркивает необходимость централизованной стратегии log aggregation.

Архитектура Docker раскрывается цепочкой CLI/REST API → dockerd → containerd → runC. runC соответствует OCI и опирается на Linux mechanisms, включая namespaces и cgroups.

Image состоит из immutable layers. Каждый layer имеет SHA-256 digest; configuration object содержит упорядоченный набор digest-значений. Container меняет данные через Copy-On-Write: нужный файл копируется в upper writable layer, где и модифицируется.

Dockerfile — текстовый файл без расширения, описывающий build image. Глава рассматривает `FROM`, `LABEL`, `ENV`, `RUN`, `CMD`, `ENTRYPOINT`, `ADD`, `EXPOSE`, `WORKDIR`, `USER`, `VOLUME`, build cache, intermediate images и multi-stage build.

## Основные тезисы источника

- Images — templates для создания containers.
- Из одного image можно создать любое количество containers.
- Container = image + thin read-write layer.
- Containers эфемерны и быстро запускаются.
- Containers могут находиться в разных states.
- Внутри container можно выполнять приложения и команды.
- Log management критичен для troubleshooting.
- Images immutable и состоят из layers.
- Каждый layer имеет SHA digest.
- Image ID связан с SHA-256 configuration object.
- Build cache использует intermediate images.
- Image можно сохранить как tar.
- Container можно сохранить как image через commit.
- Images можно pull из registry или build из Dockerfile.
- Dockerfile — текстовый build-файл без расширения.
- Layer ordering/cache влияют на эффективность сборки.
- Multi-stage build позволяет уменьшать final image.

## Ключевые термины

| Термин | Смысл по главе |
|---|---|
| Container | Динамический экземпляр image с thin read-write layer |
| Image | Read-only template из immutable layers |
| Copy-On-Write | Копирование изменяемых данных в writable layer при записи |
| Thin read-write layer | Верхний изменяемый слой конкретного container |
| Container logs | stdout/stderr records, обрабатываемые logging driver |
| Inspect | JSON-описание container/image metadata и state |
| Image ID | Идентификатор image, связанный с SHA-256 configuration object |
| Digest | SHA-256 checksum содержимого layer/image data |
| Configuration object | Упорядоченный список digest-значений слоёв + image configuration |
| Dockerfile | Текстовый файл инструкций для build image |
| Build cache | Повторное использование подходящих предыдущих build results |
| Intermediate image | Промежуточный build result для cache matching |
| Multi-stage build | Несколько `FROM`/stages с переносом нужных artifacts |

## Provenance

- Chapter RAG: `p0027:c01`–`p0058:c01` + `p0036:c02`
- PDF pages: 27–58
- Printed pages: 31–62
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
