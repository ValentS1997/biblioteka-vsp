# Главы — «Как пасти котов»

Book ID: `herding-cats-j-hank-rainwater-ru` · Inventory: `0021`.

## Подтверждённый Git-прогресс
- По RAG-плану [plan.yaml](plan.yaml): **10 пронумерованных глав** (оглавление p0005-c01, читаемое введение p0020-c01…p0022-c01).
- В ветке `chapter/herding-cats-j-hank-rainwater-ru-0021-ch10`: комплект индивидуальных Git-файлов есть для **10/10 глав (100%)**, 1–10. Публикация в `main` требует отдельного PR merge и post-merge read-back.
- На момент запуска ветки `main` подтверждал **9/10 (90%)** — главы 1–9; актуальный прогресс `main` перепроверять после merge.
- [Глава 1 — Как привыкнуть к роли руководителя](chapter-01-kak-privyknut-k-roli-rukovoditelya/README.md) — PR #490 merged.
- [Глава 2 — Как руководить собой](chapter-02-kak-rukovodit-soboy/README.md) — PR #546 merged.
- [Глава 3 — Как вести стаю за собой](chapter-03-kak-vesti-stayu-za-soboy/README.md) — PR #550 merged.
- [Глава 4 — Как организовать успех](chapter-04-kak-organizovat-uspekh/README.md) — PR #561 merged.
- [Глава 5 — Как вести совещания](chapter-05-kak-vesti-soveshchaniya/README.md) — PR #554 merged.
- [Глава 6 — Философия и методы технического лидера](chapter-06-filosofiya-i-metody-tekhnicheskogo-lidera/README.md) — PR #564 merged.
- [Глава 7 — Закат лидера](chapter-07-zakat-lidera/README.md) — PR #569 merged.
- [Глава 8 — Восход лидера](chapter-08-voskhod-lidera/README.md) — PR #579 merged.
- [Глава 9 — Как ужиться с начальством](chapter-09-kak-uzhitsya-s-nachalstvom/README.md) — PR #582 merged.
- [Глава 10 — Слова без песни](chapter-10-slova-bez-pesni/README.md) — десять файлов в текущей ветке; публикацию подтвердить после PR/CI.
- **Нумерованные главы завершены в ветке** — 10 из 10. За p. 227 следует отдельное послесловие, p. 228; его анализ не входит в коллекцию главы 10.

## RAG provenance
Глава 10: PDF p. 205–227, RAG `p0205-c01`–`p0227-c01` в `rag/chunks/p0201-p0300/`; p. 228 — послесловие. Извлечение и ограничения: `chapter-10-slova-bez-pesni/source-findings.md`.
Глава 9: PDF p. 193–204, RAG `p0193-c01`–`p0204-c01`; p. 193–200 — `rag/chunks/p0101-p0200/`, p. 201–204 — `rag/chunks/p0201-p0300/`; глава 10 начинается `p0205-c01`. Extraction findings: `chapter-09-kak-uzhitsya-s-nachalstvom/source-findings.md`.
Глава 8: PDF p. 167–192, RAG `p0167-c01`–`p0192-c01` в `rag/chunks/p0101-p0200/`; глава 9 начинается `p0193-c01`. Ограничения исходных изображений и таблицы 8.1 — `chapter-08-voskhod-lidera/source-findings.md`.
Глава 7: `p0147-c01`–`p0166-c01`, PDF p. 147–166; source findings: `chapter-07-zakat-lidera/source-findings.md`.
Глава 6: `p0124-c01`…`p0146-c01` в `rag/chunks/p0101-p0200/`; следующая начинается `p0147-c01`. Канонический source SHA-256: `5f11cf93711c9489b25218c701e1027f5ca0354523e2faeb1bb7041ed3b62795`; RAG acceptance `ACCEPTED`. Проблемы кодировки и ограничения примеров — `chapter-06-filosofiya-i-metody-tekhnicheskogo-lidera/source-findings.md`.

Canonical: `process-compliance-router-v1.2`, `session-recovery-v1.0`, `chapter-analysis-request-v1.4`, `chapter-artifact-collection-v1.8`, `chapter-publication-v1.0`. Отдельные Git-файлы, без ZIP. Читательский статус не меняется.
