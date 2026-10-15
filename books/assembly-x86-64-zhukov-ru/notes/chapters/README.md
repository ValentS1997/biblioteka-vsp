# Главы: «Ассемблер и программная модель процессоров x86/64»

Book ID: `assembly-x86-64-zhukov-ru`. Canonical RAG source SHA-256: `f65a7ec88148cb29d7e75d1ce34ef14c3a7ddf8af264ec7abcf9b8a0437220c2`.

## План и прогресс публикации

- [RAG-verified план: 21 глава](plan.yaml). Основание: оглавление (RAG PDF p. 4–8), самостоятельные заголовки глав в RAG-чанках и предисловие PDF p. 11.
- **В текущей chapter-ветке:** 5/21 (23,8%); осталось 16, следующая — №6 «Программирование циклов».
- **В `main` на начало работы над главой 5:** 4/21. До merge главы 5 в `main` опубликованы первые четыре главы; сверять HEAD независимо.

## Опубликованные главы (отдельные Git-файлы)

1. [Глава 1. Установка программ](chapter-01-ustanovka-programm/README.md) — [шпаргалка](chapter-01-ustanovka-programm/cheatsheet.md), [команды](chapter-01-ustanovka-programm/commands.md), [схема](chapter-01-ustanovka-programm/diagram.md), [краткая SVG](chapter-01-ustanovka-programm/visual-cheatsheet.svg), [подробная SVG](chapter-01-ustanovka-programm/visual-cheatsheet-detailed.svg).

2. [Глава 2. Программирование данных](chapter-02-programmirovanie-dannyh/README.md) — [шпаргалка](chapter-02-programmirovanie-dannyh/cheatsheet.md), [команды](chapter-02-programmirovanie-dannyh/commands.md), [схема](chapter-02-programmirovanie-dannyh/diagram.md), [краткая SVG](chapter-02-programmirovanie-dannyh/visual-cheatsheet.svg), [подробная SVG](chapter-02-programmirovanie-dannyh/visual-cheatsheet-detailed.svg), [задания](chapter-02-programmirovanie-dannyh/review-questions.md), [разбор заданий](chapter-02-programmirovanie-dannyh/review-answers.md), [расхождение источника](chapter-02-programmirovanie-dannyh/source-findings.md).

3. [Глава 3. Данные, имена и типы](chapter-03-dannye-imena-i-tipy/README.md) — [шпаргалка](chapter-03-dannye-imena-i-tipy/cheatsheet.md), [команды](chapter-03-dannye-imena-i-tipy/commands.md), [схема](chapter-03-dannye-imena-i-tipy/diagram.md), [компактная SVG](chapter-03-dannye-imena-i-tipy/visual-cheatsheet.svg), [подробная SVG](chapter-03-dannye-imena-i-tipy/visual-cheatsheet-detailed.svg), [задания](chapter-03-dannye-imena-i-tipy/review-questions.md), [разборы](chapter-03-dannye-imena-i-tipy/review-answers.md), [находки в источнике](chapter-03-dannye-imena-i-tipy/source-findings.md).

4. [Глава 4. Способы адресации](chapter-04-sposoby-adresatsii/README.md) — [шпаргалка](chapter-04-sposoby-adresatsii/cheatsheet.md), [команды](chapter-04-sposoby-adresatsii/commands.md), [диаграмма](chapter-04-sposoby-adresatsii/diagram.md), [компактная SVG](chapter-04-sposoby-adresatsii/visual-cheatsheet.svg), [подробная SVG](chapter-04-sposoby-adresatsii/visual-cheatsheet-detailed.svg), [задания](chapter-04-sposoby-adresatsii/review-questions.md), [ответы](chapter-04-sposoby-adresatsii/review-answers.md), [source findings](chapter-04-sposoby-adresatsii/source-findings.md).

5. [Глава 5. Система команд i8086](chapter-05-sistema-komand-i8086/README.md) — [шпаргалка](chapter-05-sistema-komand-i8086/cheatsheet.md), [команды](chapter-05-sistema-komand-i8086/commands.md), [диаграмма](chapter-05-sistema-komand-i8086/diagram.md), [компактная SVG](chapter-05-sistema-komand-i8086/visual-cheatsheet.svg), [подробная SVG](chapter-05-sistema-komand-i8086/visual-cheatsheet-detailed.svg), [задания](chapter-05-sistema-komand-i8086/review-questions.md), [разбор](chapter-05-sistema-komand-i8086/review-answers.md), [расхождения](chapter-05-sistema-komand-i8086/source-findings.md).

## Политика

`rag_only` · `chapter-artifact-collection v1.8` · `chapter-publication v1.0` · `session-recovery v1.0`. Статус чтения независим от публикации и не изменяется. Полнота публикации определяется наличием шести отдельных обязательных файлов в Git, а не архивами или черновиками. Отсутствие merge означает отсутствие новой главы в `main`.
