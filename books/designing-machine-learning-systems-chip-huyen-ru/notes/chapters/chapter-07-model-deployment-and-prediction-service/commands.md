# Commands / tools — глава 7

Источник: канонический RAG, PDF p.202–232, SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`. Кодовые примеры в текстовом слое **не подтверждены как исполнимые**. Их нельзя запускать без отдельной проверки оригинального контекста, API и target environment.

## HTTP prediction endpoint

В `p0203-c01` представлен обработчик POST `/predict`, читающий JSON с полем `X` и возвращающий прогноз `MODEL.predict`. Источник называет FastAPI, но использует декоратор, напоминающий Flask route, с неоднозначными Unicode-символами, кавычками и отступами. Это описание поведения, **не скрипт**. Класс: **state-changing**, если действительно создавать внешний сервис. Версии библиотек, импорты, аутентификация, схема, размещение и rollback — **[Needs confirmation]**.

## Экспорт

`p0204-c01` упоминает TensorFlow SavedModel и PyTorch ONNX export. В исходном тексте идентификаторы сохранены с повреждениями (`tf.keras. Model, save о` и `torch. onnx. export ()`). Результат реального экспорта — новый или перезаписанный артефакт, класс **state-changing**. Точные вызовы, аргументы и форматы — **[Needs confirmation]**.

## cuDNN autotuning

`p0227-c01` содержит повреждённый путь настройки backend cuDNN, связывает его с перебором реализаций свёртки. 

```text
torch, backends, cudnn. benchmarks rue
```

Это не рабочая команда. Класс при фактическом бенчмаркинге — **workload-generating**. Точную настройку и влияние на детерминизм нельзя установить из данного фрагмента. autoTVM упоминается как механизм более широкого поиска исполнения подграфов [p0227-c01–p0228-c01].

## Инструменты по источнику

| Режим | Подтверждённое название | Ограничение |
| --- | --- | --- |
| State-changing | Flask, FastAPI, AWS, GCP, SageMaker, Google App Engine | Концептуальный endpoint/deployment; доступов, инструкций или конфигурации нет [p0203-c01; p0211-c01] |
| Workload-generating | Apache Flink, feature stores | Объединение batch/stream обработки; нет исполняемого SQL [p0213-c01] |
| State-changing / workload | TensorFlow Lite, PyTorch Mobile, TensorRT, QAT и post-training quantization | Варианты сжатия и edge serving; нет runtime settings [p0218-c01] |
| Workload-generating | TVM, autoTVM, cuDNN | Аппаратная компиляция и поиск исполнений [p0227-c01; p0228-c01] |
| State-changing / workload | TensorFlow.js, Synaptic, brain.js, WebAssembly | Браузерный target, нет build-рецепта [p0229-c01] |
| Read-only evaluation | Latency, throughput, memory, power, качество после сжатия | Показатели обсуждаются, но измерительный набор не задан [p0218-c01–p0221-c01] |

## Safety boundary

Ни один пример не является разрешением на публикацию API, выгрузку данных, установку ПО или изменение production. Для всех модифицирующих действий нужны подтверждённые effects, validation, permissions, версия окружения и rollback. Не использовать догадки для исправления исходного листинга. Подробнее: `source-findings.md`.
