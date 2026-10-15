# Артефакты глав — Современное системное администрирование

Инвентарный номер: `0011`. Book ID: `modern-system-administration-jennifer-davis-ru`.

План: [plan.yaml](plan.yaml). Источник: canonical PDF RAG (оглавление на PDF-страницах 5–11; всего 21 нумерованная глава).

## Git publication progress

- Полных наборов артефактов в этой книжной ветке: **5 / 21 (23.8%)**. В `main` на исходном commit `75dd777` было **4 / 21 (19.0%)**.
- Глава 4 слита из `chapters/0011-modern-system-administration-chapter-04` через [PR #508](https://github.com/vsp-corp/biblioteka-vsp/pull/508), merge commit [`aa87563`](https://github.com/vsp-corp/biblioteka-vsp/commit/aa875633f8b32b96af5a5b5342e9de8b7ca96350).
- Осталось в рабочей ветке: **16**.
- Следующая неопубликованная глава: **6 — Контроль версий**.
- Учёт публикации: только отдельные committed Git files; ZIP и подготовленные вне Git тексты не учитываются.
- Recovery evidence: [chapter 3 checkpoint](../../../../.workflow/checkpoints/0011-modern-system-administration-chapter-03.yaml) — `COMPLETE`; слияние PR #503 и #504, финальные CI PASS.
- Публикация в `main`: PR [#489](https://github.com/vsp-corp/biblioteka-vsp/pull/489) слит; merge commit [`781200b`](https://github.com/vsp-corp/biblioteka-vsp/commit/781200b791f0ce111a6659b330d537adb49289be).
- **Зафиксированное исходное состояние `main`: 4 / 21 (19.0%).** В этой ветке завершена также глава 5; статус слияния проверяется отдельно. Глава 3 через [PR #503](https://github.com/vsp-corp/biblioteka-vsp/pull/503), глава 4 через [PR #508](https://github.com/vsp-corp/biblioteka-vsp/pull/508).

## Реестр глав

| № | Название | Публикация |
|---:|---|---|
| 1 | [Закономерности и взаимосвязи](chapter-01-patterns-and-interconnections/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 2 | [Вычислительные среды](chapter-02-computing-environments/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 3 | [Хранилище](chapter-03-storage/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла |
| 4 | [Сеть](chapter-04-network/README.md) | Опубликована в `main`: 6 обязательных + 2 условных Git-файла; PR #508, CI PASS |
| 5 | [Набор инструментов сисадмина](chapter-05-sysadmin-toolkit/README.md) | 6 обязательных + 2 условных отдельных Git-файла в книжной ветке; опубликованы после Git read-back |
| 6 | Контроль версий | Не опубликована |
| 7 | Тестирование | Не опубликована |
| 8 | Безопасность инфраструктуры | Не опубликована |
| 9 | Документация | Не опубликована |
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

## Свидетельство публикации главы 5 (ветка)

Глава 5 «Набор инструментов сисадмина»: RAG PDF **73–82** (печатные с. **77–86**); PDF 83 — начало главы 6. В ветке `chapters/0011-modern-system-administration-chapter-05` созданы и отдельно прочитаны из Git восемь путей `chapter-05-sysadmin-toolkit/`: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`, `summary.md`, `source-findings.md`. Пример Bash из текстового слоя PDF 75–76 содержит [Source extraction issue] и не выдаётся за рабочую команду. Доля полной Git-публикации в этой ветке — **5/21 (23,8%)**; перенос в main определяется фактическим PR/merge. Статус чтения не менялся.
