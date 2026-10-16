# Команды, код и инструменты — глава 3

Canonical source: `designing-machine-learning-systems-chip-huyen-ru`; SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`; chapter 3 PDF pages **68–98** (printed **67–97**). TOC `p0007-c01` (PDF p. 7); chapter opens at `p0068-c01`, next chapter opens at `p0099-c01`. Chapter-specific RAG chunks under `books/designing-machine-learning-systems-chip-huyen-ru/rag/chunks/p0001-p0100/p####-c01.md`.

## Командная дисциплина

Глава обзорная и не задаёт готовый CLI-runbook для базы данных, ETL или брокеров. **Не добавлять из памяти** команды `psql`, `kubectl`, `kafka-*`, `curl`, SQL-запросы, параметры конфигурации, адреса серверов и команды изменения схемы: RAG не содержит нужных исполнимых аргументов. Названия SQL, POST/GET, REST/RPC, Spark, Kafka, Kinesis, Flink, KSQL и Spark Streaming выступают как концепции/технологии. [p0079-c01; p0090-c01; p0096-c01]

## Демонстрация H20 AutoML — workload-generating

В `p0080-c01` автор показывает Python-подобный пример подготовки предикторов/отклика и обучения группы моделей H20 AutoML. **Извлечение повреждено. Фрагмент ниже приведён как evidence, НЕ ЗАПУСКАТЬ:**

```text
х = train.columns
у = "response"
х.remove (у)
train[у] = train[у].asfactor()
test[y] = test[у].asfactor()
ami = H20AutoML(max_models=20, seed=l)
ami.train(x=x, y=y, training_frame=train)
lb = ami.leaderboard
ami.leader
```

Названия и символы из RAG не исправлены (в том числе `х`, `у`, `y`, `ami`, `H20`, `seed=l`). Синтаксис и источник окружения не подтверждены; обозначения могут быть визуально похожими латинскими/кириллическими знаками. Исполнение `train` создаёт вычислительную нагрузку и обучает модели в рамках описанной демонстрации. **Требование ресурсов, выходные артефакты, rollback:** [Needs confirmation]. [p0080-c01]

## Классификация source-grounded действий

| Класс | Источник | Что известно / не подтверждено |
| --- | --- | --- |
| Read-only | `ami.leaderboard` и `ami.leader` из примера | Получение результатов/лидера после обучения; корректность идентификатора [Needs confirmation], p0080-c01 |
| Workload-generating | `ami.train(...)`, `H20AutoML(max_models=20, seed=l)` | Запускает подбор/обучение моделей; текст не исполняем без проверки исходного кода, p0080-c01 |
| State-changing | [Not applicable] как подтверждённая операция production | В главе нет готовой команды записи в рабочую БД или деплоя; эффект/риск/верификация/откат [Needs confirmation] |

## Примеры формата, не команды

`p0081-c01`–`p0082-c01` содержат примеры документов о книгах в JSON, в RAG видны несовпадающие кавычки и неполные скобки. Это **не готовый JSON** для импорта. [Source extraction issue] описана в `source-findings.md`. В `p0073-c01` есть иллюстрация JSON-содержимого с адресом, также без готового интерфейса исполнения.

## Перед действием

Если требуется реальная миграция/экспорт/запрос/запуск AutoML, необходимо получить проверенный исходный листинг, параметры, права, тестовое окружение, метрики наблюдения и процедуру восстановления. RAG главы не предоставляет эти подробности: **[Needs confirmation]**.
