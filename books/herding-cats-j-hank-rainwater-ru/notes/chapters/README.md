# Главы — «Как пасти котов»

Book ID: `herding-cats-j-hank-rainwater-ru` · Inventory: `0021`

## Git-публикация глав
- План подтверждён RAG-оглавлением: **10 пронумерованных глав**, [plan.yaml](plan.yaml).
- В текущей ветке `chapter/herding-cats-j-hank-rainwater-ru-0021-ch05` полный комплект индивидуальных Git-артефактов есть в **4 из 10 каталогов**: главы 1, 2, 3 и 5 (**40%**, **не подряд**). Завершённость новой главы требует read-back и CI.
- В исходном `main` при старте работы — **3/10 (30%)**: главы 1, 2 и 3. Обновлённый статус `main` подтверждается после merge.
- **Глава 4 не опубликована** в `main`: её отдельная ветка `chapter/herding-cats-j-hank-rainwater-ru-0021-ch04` осталась незавершённой. Не включать её в процент готовности.
- [Глава 1 — Как привыкнуть к роли руководителя](chapter-01-kak-privyknut-k-roli-rukovoditelya/README.md) — PR #490 merged.
- [Глава 2 — Как руководить собой](chapter-02-kak-rukovodit-soboy/README.md) — PR #546 merged.
- [Глава 3 — Как вести стаю за собой](chapter-03-kak-vesti-stayu-za-soboy/README.md) — PR #550 merged.
- [Глава 5 — Как вести совещания](chapter-05-kak-vesti-soveshchaniya/README.md) — комплект отдельных файлов в текущей ветке; PR/merge/CI требуют отдельного подтверждения.
- **Первая неопубликованная глава по номеру:** 4 — «Как организовать успех» (p. 81–106). Следующая после главы 5 по содержанию: **6 — «Философия и методы технического лидера»**, p. 124–146.

## RAG provenance и ограничения
Глава 5: `p0107-c01`…`p0123-c01`, PDF 107–123. Source SHA-256: `5f11cf93711c9489b25218c701e1027f5ca0354523e2faeb1bb7041ed3b62795`. Найденные дефекты текстовой кодировки и ограничения по рисункам 5.1–5.2 зафиксированы в `chapter-05-kak-vesti-soveshchaniya/source-findings.md`.

Canonical contracts: `process-compliance-router-v1.2`, `session-recovery-v1.0`, `chapter-analysis-request-v1.4`, `chapter-artifact-collection-v1.8`, `chapter-publication-v1.0`. Нет архивной замены individual Git files. Статус чтения не меняется.
