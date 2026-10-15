# Chapter 11 — инструменты и source-supported операции

Канонический RAG PDF p.335–358, source SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`. **Глава не предоставляет исполнимый CLI-runbook или полный API для реализации human-in-the-loop, privacy opt-in, fairness audits или model cards.** Перечислены задачи/инструменты без неподтверждённых команд запуска.

## Provenance и классификация операций

| Класс | Указанная в книге практика / инструмент | Эффект / предел |
| --- | --- | --- |
| Read-only / evaluation | Проверка консистентности рекомендаций при неизменном контексте, сравнение исходов в Booking.com | UX/accuracy trade-off, конкретные правила и dataset неизвестны [p0336-c01] |
| State-changing | Показ нескольких вариантов пользователю и HITL исправление ответа человеком | Меняет интерфейс, пользовательские решения и канал обратной связи; SDK/триггеры неизвестны [p0337-c01–p0338-c01] |
| State-changing | Fast fallback (эвристики, простая модель, cache) после порога latency | Изменение inference routing, quality/latency trade-off; конкретный latency threshold: [Needs confirmation] [p0338-c01] |
| Read-only / work practice | Доменный аудит SME: цели, признаки, анализ ошибок, UX | Источник не требует от SMEs умения использовать Git; нужны доступные способы участия [p0339-c01] |
| State-changing / process | Разделённые команды и end-to-end ownership, platform abstraction | Организационное изменение, не готовый технический скрипт [p0340-c01–p0342-c01] |
| Read-only / workload | `AI Fairness 360 (AIF360)`, `DisparateImpactRemover`, H2O infogram | Названия методов из текста (там повреждено `Al Fairness 360`), версия, параметры и валидированный API неизвестны [p0351-c01; p0356-c01] |
| Read-only / documentation | Model cards: intended use, developer, version, model type, risk, eval sets/slices, training data, ethics, caveats | Источник предлагает поддерживать карточки при обновлении модели; готовой схемы JSON нет [p0354-c01–p0355-c01] |
| State-changing / workload | Генерация model cards при помощи TensorFlow, Metaflow, scikit-learn или собственных инструментов | Создаёт/меняет метаданные артефакта, требует схемы/версии; команды отсутствуют [p0355-c01] |
| Read-only / reference | NIST SP 1270, ACM FAccT, Responsible AI research communities, incidentdatabase.ai | В книге — исторические ресурсы для исследования, не текущие требования compliance [p0344-c01; p0356-c01] |

## Safe-readonly checks

Проверить, какой вариант прежней рекомендации ожидается при повторном запросе; сможет ли получатель исправить «почти верный» результат; существует ли fallback; какие люди уполномочены оценивать ошибки, fairness и privacy; поддерживается ли карточка конкретной версии; нет ли зависимости aggregate accuracy от недопредставленных групп. Документировать provenance evidence `p0336-c01`–`p0356-c01`.

## No executable transformation

Никаких выдуманных вызовов `aif360.*`, `pip install`, cloud CLI, production endpoint или маршрутов данных не добавлено. Реальное действие требует подтверждённого user consent, прав доступа, тестового набора, допустимых ошибок, security/legal review, ответственного владельца и rollback: **[Needs confirmation]**.

## Source issues

Разночтения `Al/AI`, `YALM`, `Kubemetes` и другие extraction artifacts, смешение исторических кейсов/оценок и неполнота figure assets задокументированы в [source-findings.md](source-findings.md).