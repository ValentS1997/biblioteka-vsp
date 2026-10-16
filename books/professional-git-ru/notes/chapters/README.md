# Профессиональная работа с Git — главы

Книга: `professional-git-ru`, инвентарный № `0019`.

## Проверенный план и прогресс

- Всего глав по [RAG-оглавлению](../../rag/text.md) (PDF pages 4–9): **61**; нумерация: 1–61.
- [Git-backed план глав](plan.yaml) содержит заголовки и PDF-локаторы начала всех 61 главы.
- Опубликовано полных глав в этой рабочей ветке: **1/61 (1.64%)**.
- Опубликовано полных глав в `main` при создании плана: **0/61 (0%)**.
- Осталось: **60**; следующая неопубликованная глава: **2 — «Просмотр истории версий»**.
- Завершена в рабочей ветке: **[глава 1 — «Начало работы с Git»](chapter-01-nachalo-raboty-s-git/README.md)**. Шесть обязательных файлов и `source-findings.md` зафиксированы отдельными Git-путями и проверены обратным чтением.

Прогресс рассчитывается по зафиксированным Git-файлам, а не по тексту этого README: `python scripts/chapter_publication_status.py --book-id professional-git-ru`. Перед каждой публикацией и после неё требуется повторно вычислить фактический прогресс по выбранной ветке/HEAD.

## Правила публикации

Применять `templates/process-compliance-router-v1.2.yaml`, `templates/chapter-publication-v1.0.yaml`, `templates/chapter-analysis-request-v1.4.yaml`, `templates/chapter-artifact-collection-v1.8.yaml` `templates/git-execution-policy-v1.0.yaml` и `templates/session-recovery-v1.0.yaml`.

Одна глава считается опубликованной только после Git-коммита и обратной проверки всех шести файлов: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`. Условные артефакты — по главе и шаблону v1.8. Список ссылок на завершённые главы: [глава 1](chapter-01-nachalo-raboty-s-git/README.md). До слияния связанных PR это опубликовано только в рабочей ветке, не в `main`. ZIP/архив не заменяет Git-публикацию. Статус чтения не изменять.
