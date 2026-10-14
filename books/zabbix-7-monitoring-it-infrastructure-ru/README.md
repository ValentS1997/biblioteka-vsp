# Zabbix 7: мониторинг ИТ-инфраструктуры

Book ID: `zabbix-7-monitoring-it-infrastructure-ru` · Inventory: `0020`.

## Издание (подтверждено PDF, стр. 4)
- Авторы: Натан Лифтинг, Брайан ван Бэкел
- Третье обновлённое издание; русский перевод А. Ларина; научный редактор Ф. Осьминин
- Издательство «Спринт Бук» (Астана), 2025; ISBN 978-601-08-4700-2
- Английский оригинал: *Zabbix 7 IT Infrastructure Monitoring Cookbook – Third Edition*, Packt Publishing, 2024, ISBN 9781801078320
- PDF: 512 страниц; оглавление содержит 13 глав

## Canonical source
- `source/book.pdf` — исходный PDF, Git LFS; git blob pointer в точности переиспользован из vault
- SHA-256 PDF: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`
- Size: `19047049` bytes
- Vault: `source-vault/2026-10-13-found-books-14`
- Upload commit: `3482c94a29445074dc60fbd967e68871cafb80f2`
- Реальный LFS-объект проверен во время GitHub Actions checkout/build; хеш бинарного файла совпал.

## RAG
- Scope: full book, 512/512 PDF pages processed
- 509 source pages with extractable text, 3 empty extraction units: 2, 3, 511
- Chunks: 509, deterministic lexical shards: 2371
- `rag/acceptance.yaml`: `ACCEPTED` (13/13 checks PASS)
- Generation: `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`
- Workflow: https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38373632055
- Limitations documented in `rag/manifest.yaml` (no independent multimodal extraction; lexical, not semantic index).

## Главы и публикация
- [RAG-подтверждённый план 13 глав](notes/chapters/plan.yaml) (стартовые страницы и chunk IDs).
- [Индекс и прогресс публикации](notes/chapters/README.md): учитываются только отдельные Git-файлы, прошедшие проверку.
- Текущие canonical contracts: `process-compliance-router-v1.2`, `session-recovery-v1.0`, `chapter-publication-v1.0`, `chapter-analysis-request-v1.4`, `chapter-artifact-collection-v1.8`.
- Анализ главы запускается только командой `Анализ главы N`; чтение и публикация независимы.

## Reading
No reading status has been changed or inferred. Reading state remains `[Needs confirmation]`.

## Verification
`python scripts/check_book_readiness.py --book-id zabbix-7-monitoring-it-infrastructure-ru --capability chapter-analysis`

## Provenance note
The inventory previously described this title as an original Russian publication.
The PDF imprint on page 4 explicitly credits an English original and Russian translation.
The inventory translator/editor description is corrected on that source evidence.
