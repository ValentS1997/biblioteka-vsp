# Глава 7. Развертывание модели и совершенствование ее сервиса прогнозирования

Книга: Чип Хьюен, «Проектирование систем машинного обучения», inventory 0031.

Источник: канонический RAG, PDF pp.202–232, source SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`.

Главная идея: развёртывание ML-модели подразумевает доступный, своевременный, воспроизводимый и сопровождаемый сервис прогнозирования, а не только экспорт весов и создание HTTP endpoint. [p0202-c01; p0203-c01; p0230-c01]

Разделы: мифы о деплое [p0204-c01–p0207-c01]; batch, online и streaming prediction [p0207-c01–p0212-c01]; согласование train и serving feature pipelines [p0212-c01–p0213-c01]; low-rank factorization, distillation, pruning, quantization [p0214-c01–p0219-c01]; cloud vs edge [p0219-c01–p0221-c01]; IR, model compilers и runtime optimisation [p0221-c01–p0228-c01]; browser/WebAssembly [p0229-c01]; авторские «Итоги» [p0229-c01–p0230-c01].

В RAG повреждены исходные Python-демонстрации HTTP endpoint, экспорта TensorFlow/PyTorch и настройки cuDNN; исполняемость не подтверждена. Конкретные SLA, версии runtime, инфраструктура и rollback: [Needs confirmation]. Статус чтения не изменять.
