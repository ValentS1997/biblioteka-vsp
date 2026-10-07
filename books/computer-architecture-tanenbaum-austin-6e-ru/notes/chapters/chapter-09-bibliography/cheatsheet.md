# Cheatsheet — глава 9 «Библиография»

**Provenance:** RAG `p0699:c01`–`p0707:c01`. Policy: **rag_only**.

## Symptom / problem framing

Нужно перейти от объяснения в учебнике к первоисточнику, на который ссылаются авторы.

Глава 9 — не учебный материал, а алфавитный индекс **153** книг и статей.

## Baseline / context

```text
chapter 1–8 claim
→ in-text citation / author
→ chapter 9 bibliography
→ external source
```

Библиография охватывает архитектуру процессоров, ОС, память, параллелизм, сети, I/O, storage, security и исторические работы.

## Read-only checks

1. Найти фамилию/ссылку в RAG изучаемой главы.
2. Найти соответствующую запись в `p0699:c01`–`p0707:c01`.
3. Проверить:
   - авторов;
   - название;
   - venue/publisher;
   - год;
   - volume/pages/edition, если они присутствуют.
4. Если metadata выглядит повреждённой extraction-ом, не нормализовать её молча.

## Interpretation

Библиографическая запись подтверждает только то, **какой источник указан авторами книги**.

Она сама по себе не подтверждает:

- содержание внешней публикации;
- актуальность публикации;
- доступность URL/DOI;
- отсутствие ошибок в библиографической записи.

## Next action

Если требуется deeper research:

```text
identify bibliography entry
→ create external-research task
→ retrieve current authoritative copy/metadata
→ compare with textbook claim
```

Это отдельный workflow; глава 9 остаётся `rag_only`.

## Modifying action

[Not applicable]

В самой главе нет команд, конфигураций или процедур изменения системы.

Допустимое изменение в репозитории — только создание/обновление chapter artifacts на основе canonical RAG.

## Verification / acceptance checks

- Boundary = PDF 699–707.
- RAG range = `p0699:c01`–`p0707:c01`.
- First entry = 1.
- Last entry = 153.
- `p0708:c01` = Appendix A.
- No summary/review section is invented.
- No external metadata is injected into source-grounded artifacts.

## Rollback

Для технической системы: [Not applicable].

Для repository change: rollback = revert the chapter-artifact commit/PR if acceptance checks fail.
