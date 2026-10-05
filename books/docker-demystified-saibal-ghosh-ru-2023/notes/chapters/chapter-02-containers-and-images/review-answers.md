# Ответы к контрольным материалам — глава 2

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | C |
| 2 | D |
| 3 | A |
| 4 | B |
| 5 | C |
| 6 | B |
| 7 | B |
| 8 | A |
| 9 | D |
| 10 | C |

Ключ `1-C, 2-D, 3-A, 4-B, 5-C, 6-B, 7-B, 8-A, 9-D, 10-C` прямо приведён в `p0058:c01`.

## Ответы на открытые вопросы

### 1. Что такое контейнер?

Container — динамический экземпляр image. Он создаётся из read-only image и получает собственный thin read-write layer, куда попадают изменения конкретного container.

### 2. Что такое images и как они связаны с containers?

Image — read-only template filesystem, состоящий из упорядоченных immutable layers. Из одного image можно создать множество containers; каждый использует общие read-only layers image и собственный writable layer.

### 3. В каких состояниях может находиться container?

Глава перечисляет: Running, Paused, Exited, Restarting, Dead, Stopped и Created.

### 4. Что означает immutable применительно к images?

После создания image layers не модифицируются. Если container изменяет данные из image layer, Docker применяет Copy-On-Write: данные копируются в writable layer container, а исходный layer остаётся неизменным.

### 5. Как наиболее эффективно управлять logs?

Источник подчёркивает, что локальное накопление logs потребляет много места, особенно при большом числе containers. Нужна продуманная стратегия: logging driver + централизованный aggregator/data pipeline, который собирает, анализирует/нормализует и отправляет logs в центральное расположение.

### 6. Что такое Dockerfile?

Dockerfile — текстовый файл без расширения с инструкциями для build Docker image. Docker читает его сверху вниз; инструкции формируют configuration/layers итогового image.

### 7. Что такое configuration object в image?

Это объект конфигурации с упорядоченным списком SHA digest-значений layers и другими элементами configuration. Docker Engine использует его для формирования filesystem container на основе image.

### 8. Что такое build cache?

Build cache — механизм повторного использования уже существующих подходящих промежуточных результатов вместо повторной сборки одинаковых layers. Docker сопоставляет текущую инструкцию с existing intermediate images/cache state.

### 9. Что такое multi-stage build?

Это Dockerfile с несколькими `FROM`. Каждый `FROM` начинает отдельный stage/base; нужные artifacts можно переносить между stages, исключая ненужное из final image и сокращая его размер.

### 10. Что такое intermediate image?

Intermediate image создаётся при фиксации layer во время build. Он имеет configuration object и используется для cache matching; в изложении главы intermediate image также содержит ссылку на parent image для сопоставления с build cache.

## Operational map

```text
Dockerfile → build/cache → immutable image layers
                         ↓
                   docker run
                         ↓
image layers + writable layer → container
```

Диагностика:

```text
state → docker ps / docker container ls -a
metadata → docker inspect
logs → docker logs
image structure → docker image inspect / history
```

## Provenance

Ответы сформированы только по RAG главы `p0027:c01`–`p0058:c01` (+ `p0036:c02`). Внешняя документация и model-memory не использовались.
