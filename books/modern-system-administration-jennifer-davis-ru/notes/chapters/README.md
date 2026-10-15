# Артефакты глав — Современное системное администрирование

Инвентарный номер: `0011`. Book ID: `modern-system-administration-jennifer-davis-ru`.

План: [plan.yaml](plan.yaml). Источник: canonical PDF RAG (оглавление на PDF-страницах 5–11; всего 21 нумерованная глава).

## Git publication progress

- Полных наборов артефактов в книжной ветке: **9 / 21 (42.9%)**; подтверждённая исходная база `main`: **8 / 21 (38.1%)**.
- Глава 4 слита из `chapters/0011-modern-system-administration-chapter-04` через [PR #508](https://github.com/vsp-corp/biblioteka-vsp/pull/508), merge commit [`aa87563`](https://github.com/vsp-corp/biblioteka-vsp/commit/aa875633f8b32b96af5a5b5342e9de8b7ca96350).
- Осталось в книжной ветке: **12**.
- Следующая неопубликованная глава: **10 — Презентации**.
- Учёт публикации: только отдельные committed Git files; ZIP и подготовленные вне Git тексты не учитываются.
- Recovery evidence: [chapter 3 checkpoint](../../../../.workflow/checkpoints/0011-modern-system-administration-chapter-03.yaml) — `COMPLETE`; слияние PR #503 и #504, финальные CI PASS.
- Публикация в `main`: PR [#489](https://github.com/vsp-corp/biblioteka-vsp/pull/489) слит; merge commit [`781200b`](https://github.com/vsp-corp/biblioteka-vsp/commit/781200b791f0ce111a6659b330d537adb49289be).
- **Проверенный прогресс книжной ветки: 9 / 21 (42.9%); исходный `main`: 8 / 21 (38.1%).** Глава 8 через [PR #523](https://github.com/vsp-corp/biblioteka-vsp/pull/523), merge commit [`99f6755`](https://github.com/vsp-corp/biblioteka-vsp/commit/99f6755d0a4237dd32fc645fc9a637d2c4425772). Глава 7 через [PR #519](https://github.com/vsp-corp/biblioteka-vsp/pull/519), merge commit [`b48f0ec`](https://github.com/vsp-corp/biblioteka-vsp/commit/b48f0ec569a2ca280f38392aa416572c9daaf722). Глава 3 через [PR #503](https://github.com/vsp-corp/biblioteka-vsp/pull/503), глава 4 через [PR #508](https://github.com/vsp-corp/biblioteka-vsp/pull/508), глава 5 через [PR #512](https://github.com/vsp-corp/biblioteka-vsp/pull/512), merge commit [`a153eed`](https://github.com/vsp-corp/biblioteka-vsp/commit/a153eed050e88f65c9462052ba7378cd90fcc317).

## Реестр глав

| № | Название | Публикация |
|---:|---|---|
| 1 | [Закономерности и взаимосвязи](chapter-01-patterns-and-interconnections/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 2 | [Вычислительные среды](chapter-02-computing-environments/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 3 | [Хранилище](chapter-03-storage/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 4 | [Сеть](chapter-04-network/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #508, CI PASS |
| 5 | [Набор инструментов сисадмина](chapter-05-sysadmin-toolkit/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #512, CI PASS |
| 6 | [Контроль версий](chapter-06-version-control/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #515, CI PASS |
| 7 | [Тестирование](chapter-07-testing/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #519, CI PASS |
| 8 | [Безопасность инфраструктуры](chapter-08-infrastructure-security/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #523, CI PASS |
| 9 | [Документация](chapter-09-documentation/README.md) | Полный набор в книжной ветке: 6 обязательных + 2 условных Git-файла; read-back выполнен |
| 10 | Презентации | Не опубликована |
| 11 | Разработка сценариев инфраструктуры | Не опубликована |
| 12 | Управление инфраструктурой | Не опубликована |
| 13 | Обеспечение безопасности инфраструктуры | Не опубликована |
| 14 | Теоретические аспекты мониторинга | Не опубликована |
| 15 | Мониторинг вычислительной инфраструктуры и программного обеспечения на практике | Не опубликована |
| 16 | Управление данными мониторинга | Не опубликована |
| 17 | Мониторинг вашей работы | Не опубликована |
| 18 | Управление мощностями | Не опубликована |
| 19 | Создание надежной дежурной службы | Не опубликована |
| 20 | Управление инцидентами | Не опубликована |
| 21 | Руководство устойчивыми командами | Не опубликована |

Глава считается опубликованной только при наличии и read-back всех шести файлов: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`. Условные артефакты добавляются по RAG chapter content.

Печатные начальные страницы сохранены в `plan.yaml` только как данные оглавления; реальные границы PDF должны быть проверены перед анализом каждой главы.

Статус чтения при подготовке этого индекса не менялся.

## Свидетельство публикации главы 2

В ветке `chapters/0011-modern-system-administration` созданы и независимо прочитаны из Git восемь отдельных файлов `chapter-02-computing-environments/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Границы: PDF 37–47; глава 3 начинается на PDF 48. Статус чтения не менялся. PR #489 слит в `main`; восемь файлов главы доступны в canonical branch.

## Свидетельство публикации главы 1

В ветке `chapters/0011-modern-system-administration` созданы и прочитаны из Git отдельно файлы `chapter-01-patterns-and-interconnections/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Границы: PDF 28–36; режим RAG-only. PR #489 слит в `main`; все восемь файлов главы доступны в canonical branch. Статус чтения не затронут.

## Свидетельство публикации главы 3 (`main`)

В ветке `chapters/0011-modern-system-administration-chapter-03` восемь отдельных Git-файлов `chapter-03-storage/` прочитаны обратно после коммитов: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Границы подтверждены RAG PDF **48–62** (печатные 51–65), PDF 63 начинает главу 4. Историческая таблица Amazon EBS и проблемы извлечения обозначены отдельно. **Глава 3 слита в `main` через PR #503; всего опубликовано 3/21.** Статус чтения не менялся.

## Свидетельство публикации главы 4 (`main`)

Глава 4 «Сеть»: RAG PDF **63–71**, печатные с. **66–74**; PDF 72 — титул части II, PDF 73 — начало главы 5. В ветке `chapters/0011-modern-system-administration-chapter-04` независимо записаны и прочитаны из Git: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Источник и RAG не изменялись. Условные обзорные вопросы отсутствуют. Глава 4 **слита в `main` через PR #508**; merge commit `aa875633f8b32b96af5a5b5342e9de8b7ca96350`; PR CI `Validate chapter notes and SVG`: PASS ([run 38702483089](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38702483089)). Все 8 путей независимо проверены в `main`. Статус чтения не менялся.

## Свидетельство публикации главы 5 (`main`)

Глава 5 «Набор инструментов сисадмина»: RAG PDF **73–82** (печатные с. **77–86**); PDF 83 — начало главы 6. В ветке `chapters/0011-modern-system-administration-chapter-05` созданы и отдельно прочитаны из Git восемь путей `chapter-05-sysadmin-toolkit/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Пример Bash из текстового слоя PDF 75–76 содержит [Source extraction issue] и не выдаётся за рабочую команду. Глава 5 **слита в `main` через PR #512**, merge commit `a153eed050e88f65c9462052ba7378cd90fcc317`; PR CI `Validate chapter notes and SVG` PASS ([run 38706997942](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38706997942)). Все восемь отдельных файлов проверены в `main`. Git-публикация: **5/21 (23,8%)**. Статус чтения не менялся.

## Свидетельство публикации главы 6 (`main`)

Глава 6 «Контроль версий»: RAG PDF **83–88**, печатные **87–92**; на PDF 89 начинается глава 7 «Тестирование». В ветке `chapters/0011-modern-system-administration-chapter-06` по отдельности созданы и прочитаны из Git восемь файлов `chapter-06-version-control/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Детали CLI отсутствуют в RAG — они не добавлены из модельной памяти. Зафиксированы проблемы извлечения терминов mono/multi и колонтитулов без переписывания источника. **Глава 6 слита в `main` через [PR #515](https://github.com/vsp-corp/biblioteka-vsp/pull/515)**; merge commit [`536e9b6`](https://github.com/vsp-corp/biblioteka-vsp/commit/536e9b68b7a1ded03463a6afb8fc564aef787166); PR CI `Validate chapter notes and SVG` — PASS ([run 38710519610](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38710519610)). Все восемь путей сверены в `main`. **Прогресс: 6/21 (28,6%)**. Статус чтения не менялся.

## Свидетельство публикации главы 7 (`main`)

Глава 7 «Тестирование»: подтверждённый RAG **PDF 89–99**, печатные страницы **93–103**; на PDF 100 начинается глава 8. В книжной ветке `chapters/0011-modern-system-administration-chapter-07` созданы и по отдельности прочитаны из Git восемь файлов `chapter-07-testing/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Исходный RuboCop-пример с неоднозначной YAML-структурой и рисунки пирамиды зафиксированы в `source-findings.md`; неподтверждённые команды не добавлялись. **Глава 7 слита в `main` через PR #519**; merge commit `b48f0ec569a2ca280f38392aa416572c9daaf722`; PR CI `Validate chapter notes and SVG` PASS ([run 38718086347](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38718086347)). Все восемь отдельных путей сверены в `main`. **Глобальный прогресс: 7/21 (33,3%)**. Статус чтения не изменён.

## Свидетельство публикации главы 8 (`main`)

Глава 8 «Безопасность инфраструктуры»: RAG PDF **100–108** (печатные **104–112**); начало главы 9 — PDF 109. На `chapters/0011-modern-system-administration-chapter-08` индивидуально закоммичены и прочитаны из Git восемь файлов `chapter-08-infrastructure-security/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Искажение рис. 8.1 и моделей размещения зафиксировано отдельно; команды изменения конфигураций не добавлялись из модели. **Глава 8 слита в `main` через PR #523**; merge commit `99f6755d0a4237dd32fc645fc9a637d2c4425772`. PR CI `Validate chapter notes and SVG`: PASS ([run 38721037869](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38721037869)). Все восемь индивидуальных файлов проверены в `main`. **Глобальный прогресс: 8/21 (38,1%)**. Статус чтения не изменялся.

## Свидетельство публикации главы 9 (книжная ветка)

Глава 9 «Документация»: RAG **PDF 109–115** (печатные **113–119**); глава 10 начинается на PDF 116. В ветке `chapters/0011-modern-system-administration-chapter-09` отдельно записаны и прочитаны из Git восемь файлов `chapter-09-documentation/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Замечания о недоступных графических деталях рис. 9.1–9.3 сохранены без восстановления из внешних знаний. **Прогресс ветки: 9/21 (42,9%)**. Доступность в `main` считается подтверждённой только после CI PASS, слияния PR и Git read-back; статус чтения не изменялся.
