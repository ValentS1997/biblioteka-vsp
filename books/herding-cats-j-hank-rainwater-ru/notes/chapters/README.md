# Главы — «Как пасти котов»

Book ID: `herding-cats-j-hank-rainwater-ru` · Inventory: `0021`

## Публикация и последовательность
- **10 глав** по RAG-плану [plan.yaml](plan.yaml), источник `p0005-c01` и читаемое введение `p0020-c01`–`p0022-c01`.
- **Готовые индивидуальные наборы в этой ветке: 5/10 (50%)**, главы 1–5. На момент подготовки ветки `main` содержал 4/10: 1, 2, 3 и 5; после merge проверять актуальное состояние `main`.
- [Глава 1 — Как привыкнуть к роли руководителя](chapter-01-kak-privyknut-k-roli-rukovoditelya/README.md) — PR #490 merged.
- [Глава 2 — Как руководить собой](chapter-02-kak-rukovodit-soboy/README.md) — PR #546 merged.
- [Глава 3 — Как вести стаю за собой](chapter-03-kak-vesti-stayu-za-soboy/README.md) — PR #550 merged.
- [Глава 4 — Как организовать успех](chapter-04-kak-organizovat-uspekh/README.md) — индивидуальные RAG-артефакты дополнены в текущей ветке; окончательное признание публикации требует CI и merge.
- [Глава 5 — Как вести совещания](chapter-05-kak-vesti-soveshchaniya/README.md) — PR #554 merged.
- **Следующая неизданная глава после публикации главы 4:** 6 — «Философия и методы технического лидера», PDF p. 124–146.

## Источник и контракты
Глава 4: PDF p. 81–106; RAG `p0081-c01`–`p0106-c01` (каталог `p0001-p0100` до p. 100, затем `p0101-p0200`). Глава 5 начинается на p. 107. Канонический source SHA-256: `5f11cf93711c9489b25218c701e1027f5ca0354523e2faeb1bb7041ed3b62795`; book RAG acceptance `ACCEPTED`.

Canonical templates: `process-compliance-router-v1.2`, `session-recovery-v1.0`, `chapter-analysis-request-v1.4`, `chapter-artifact-collection-v1.8`, `chapter-publication-v1.0`.

Шесть обязательных и четыре обусловленных источником файла главы 4 размещены непосредственно в Git. Вопросы на p. 93 и 102 исходно не нумерованы; summary на p. 105–106. Извлечение заголовков и таблиц повреждено кодировкой, визуальные данные рис. 4.1–4.3 отдельно не доступны — см. `chapter-04-kak-organizovat-uspekh/source-findings.md`.

Статус чтения, PDF и RAG при публикации не изменяются. Файлы checkpoint — временные и удаляются из итогового дерева до PR merge.
