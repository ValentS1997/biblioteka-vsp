# Профессиональная работа с Git — главы

Книга: `professional-git-ru`, инвентарный № `0019`.

## Проверенный план и прогресс

- Число глав по [RAG-оглавлению](../../rag/text.md) (PDF 4–9): **61**; нумерация 1–61.
- [Канонический план](plan.yaml) содержит заголовки и точные PDF-локаторы глав и привязан к source SHA-256.
- Завершено в текущей Git-ревизии: **2/61 (3.28%)**.
- Базовая ветка `main` на старте главы 2: **1/61 (1.64%)**. Число в `main` становится **2/61** только после merge соответствующего PR и обратной проверки.
- Осталось по текущей ревизии: **59**.
- Следующая неопубликованная глава: **3 — «Работа с удаленными репозиториями»**.

## Завершённые главы

1. [Глава 1 — «Начало работы с Git»](chapter-01-nachalo-raboty-s-git/README.md) — PDF 10–16, полный комплект индивидуальных Git-файлов.
2. [Глава 2 — «Просмотр истории версий»](chapter-02-prosmotr-istorii-versiy/README.md) — PDF 16–23, шесть обязательных файлов и `source-findings.md`, индивидуальная проверка Git read-back.

Прогресс определяется **фактическими Git-файлами на выбранной ветке**, а не только этим текстом; рабочая команда репозитория: `python scripts/chapter_publication_status.py --book-id professional-git-ru`. Прогресс `main` и рабочей ветки нельзя объединять до слияния PR.

## Правила публикации

Применяются `templates/process-compliance-router-v1.2.yaml`, `templates/session-recovery-v1.0.yaml`, `templates/chapter-publication-v1.0.yaml`, `templates/chapter-analysis-request-v1.4.yaml`, `templates/chapter-artifact-collection-v1.8.yaml`, `templates/git-execution-policy-v1.0.yaml`.

Каждая глава считается опубликованной только при наличии индивидуально зафиксированных `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`; условные артефакты обязательны при наличии соответствующих разделов/проблем. Требуются Git read-back и CI. ZIP/архивы не принимаются. **Статус чтения не изменять**.
