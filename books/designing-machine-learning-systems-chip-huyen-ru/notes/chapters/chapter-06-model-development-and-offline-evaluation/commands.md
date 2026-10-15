# Команды, API и вычислительные операции — глава 6

Canonical RAG only: `designing-machine-learning-systems-chip-huyen-ru`, source SHA-256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`; chapter 06 PDF **162–201** (printed **161–200**). TOC: `p0008-c02`; chapter opening `p0162-c01`, chapter 07 opens at `p0202-c01`. Addressable canonical chunks `books/designing-machine-learning-systems-chip-huyen-ru/rag/chunks/p0101-p0200/p0162-c01.md` through `p0200-c01.md` and bibliography `rag/chunks/p0201-p0300/p0201-c01.md`.

## Границы подтверждения

Глава **не содержит готового CLI-runbook или полного исполнимого скрипта** настройки/обучения/развёртывания модели. Имена методов и технологий из канонического RAG перечислены для ориентира, **не являются подтверждёнными командами** для инфраструктуры пользователя. Запуск с неуказанными параметрами, средой, credentials, data source или target **не допускается**.

| Классификация | Упоминание в RAG | Известный эффект / ограничение |
| --- | --- | --- |
| Read-only / interpretive | Изучение curves, метрик, CPU/GPU, throughput и predictions/labels | Анализ логов/артефактов без готового URL/API; p0174-c01–p0175-c01 |
| Workload-generating | Overfit одного маленького train-batch для отладки | Обучение на малом наборе, контроль минимальной ошибки; p0179-c01 |
| Workload-generating | `random.seed` (дословное обозначение без параметров) | Инициализация состояния генератора; не обещает детерминизма всего железа; p0179-c01–p0180-c01 |
| Workload-generating | Data/model/pipeline parallelism, synchronous/asynchronous SGD | Распределённое обучение; требует контроль градиентов, batch и ресурсов; p0180-c01–p0183-c01 |
| Workload-generating | Random search, grid search, Bayesian optimization, Auto-skleam, Keras Tuner, Ray Tune | Hyperparameter search только по validation, не по test. Конкретные версии/API отсутствуют; p0184-c01–p0186-c01 |
| Read-only / measurement | `sklearn. calibration. calibration_curve` (разорвано переносом в RAG) | Назван метод построения калибровочных кривых; запись не подтверждена для запуска; p0194-c01–p0195-c01 |
| State-changing / workload | `skiearn.calibration.calibratedciassifiercv` (как извлечено) и Platt scaling | Калибровка прогнозных вероятностей; повреждённое написание API не исправлять; p0195-c01 |
| State-changing | Возмущение тестовой копии, настройка порога достоверности, retraining / deployment | Может влиять на тестовые артефакты, решения/доступ пользователей или production; параметры, откат: [Needs confirmation]; p0192-c01–p0196-c01 |

## Названия инструментов — НЕ инструкции установки

В главе указаны **MLflow**, **Weights & Biases**, **DVC** для tracking/versioning [p0174-c01; p0175-c01; p0176-c01]; **XGBoost** и **LightGBM** в ансамблях [p0173-c01]; **Scikit-learn**, **Auto-skleam**, **TensorFlow**, **Keras Tuner**, **Ray Tune**, **Milano** в AutoML [p0185-c01]; **CUDA** в обсуждении недетерминированности [p0177-c01]. Названий команд `mlflow ...`, `dvc ...`, `ray ...`, `python train.py`, путей или внешних хостов RAG не подтверждает.

## Проверка до запуска

Подтвердить dataset и его право использования; разделение train/validation/test; versioning кода, данных, оборудования и random seeds; experiment budget; ограничение ресурсов, измеримые показатели, мониторинг и rollback. Для каждого модифицирующего действия **[Needs confirmation]**. Автор отдельно предостерегает против настройки гиперпараметров на test [p0185-c01–p0186-c01].

## Source issues

Имена API калибровки в p0195-c01, типографика `Auto-skleam` и некоторые единицы batch приведены в [source-findings.md](source-findings.md). Не выдавать их за корректный код.
