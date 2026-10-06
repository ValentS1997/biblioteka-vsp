# Глава 5. Установка

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 5 — «Установка». Она описывает проверку наличия Python и способы установки/
настройки Python 3 для GNU/Linux/BSD, Windows и Mac OS X в историческом контексте
этой редакции книги.

Разделы, подтверждённые RAG:

- 5.1 Установка в GNU/Linux и BSD
- 5.2 Установка в Windows
  - 5.2.1 Командная строка DOS
  - 5.2.2 Запуск командной строки Python в Windows
- 5.3 Для пользователей Mac OS X
- 5.4 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0031:c01` — `p0034:c01`
- PDF pages: 31–34
- printed pages visible in chapter: 23–26
- chapter start: PDF page 31, heading «Установка»
- chapter end: PDF page 34, section 5.4 «Резюме»
- next chapter boundary: PDF page 35 begins «Первые шаги»
- boundary verified: yes

## Main principle

Логика главы: сначала проверить, установлен ли Python, и только при отсутствии
подходящей версии переходить к установке или настройке PATH. После изменений снова
проверить доступность интерпретатора командой версии.

## Chapter map

| Section | Source-grounded purpose |
|---|---|
| Intro | Python 2.x не требуется удалять для установки Python 3.0; обе версии могут сосуществовать. |
| 5.1 | Проверка Python в GNU/Linux/BSD; при отсутствии — компиляция из исходников либо бинарные пакеты через системный пакетный менеджер. |
| 5.2 | Установка Windows через скачанный installer; источник предупреждает не отключать optional components, особенно IDLE. |
| 5.2.1 | Настройка системной переменной PATH для старых версий Windows, Vista и Windows 7. |
| 5.2.2 | Запуск Windows command prompt и проверка `python3 -V`. |
| 5.3 | Для Mac OS X: проверка наличия Python; если отсутствует — source instructs установить Homebrew, затем Python 3 и проверить версию. |
| 5.4 | Резюме: после установки книга предполагает наличие Python 3 и переходит к первой программе. |

## Read-only checks

Source-confirmed commands:

- `python -V`
- `python3 -V`

Они используются для проверки наличия/версии Python и не должны изменять систему.

## State-changing actions

- установка Python из исходных текстов;
- установка бинарных пакетов системным package manager;
- установка Python через Windows installer;
- изменение `PATH`;
- изменение `C:\AUTOEXEC.BAT` / использование `AUTOEXEC.NT` в исторических Windows instructions;
- установка Homebrew через remote script;
- `brew install python3`;
- перезагрузка системы там, где её требует source procedure.

Подробная классификация — в `commands.md`.

## Acceptance check

После выбранного installation/configuration path источник использует вывод команды
версии как основной признак того, что Python доступен из командной строки:

- `python -V` либо
- `python3 -V`

## Safety boundary

- Команда установки Homebrew в источнике загружает удалённый код и немедленно
  выполняет его через Ruby. Это state-changing действие; источник не задаёт отдельной
  проверки целостности скачанного кода.
- Конкретные package-manager команды установки в GNU/Linux/BSD источник не приводит;
  нельзя достраивать их из общих знаний.
- Пути, версии Windows, Python 3.0/3.3 и Homebrew-команда относятся к историческому
  содержанию книги; текущая применимость не проверялась в `rag_only` режиме.

## Conditional artifacts

Раздел 5.4 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
