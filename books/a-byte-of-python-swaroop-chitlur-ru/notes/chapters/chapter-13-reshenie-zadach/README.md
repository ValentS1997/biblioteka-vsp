# Глава 13. Решение задач

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 13 — «Решение задач». Она объединяет предыдущие части языка в небольшой
практический проект: сценарий резервного копирования. Источник проходит от анализа
задачи и первой реализации к последовательным улучшениям, намеренной ошибке,
отладке и формулировке общего software-development cycle.

Разделы, подтверждённые RAG:

- 13.1 Задача
- 13.2 Решение
- 13.3 Вторая версия
- 13.4 Третья версия
- 13.5 Четвёртая версия
- 13.6 Дополнительные усовершенствования
- 13.7 Процесс разработки программного обеспечения
- 13.8 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0099:c01` — `p0108:c01`
- PDF pages: 99–108
- printed pages visible in chapter: 91–100
- chapter start: PDF page 99, heading «Решение задач»
- chapter end: PDF page 108, section 13.8 «Резюме»
- next chapter boundary: PDF page 109 begins «Объектно-ориентированное программирование»
- boundary verified: yes

## Main principle

Глава демонстрирует iterative problem-solving workflow:

1. определить задачу;
2. собрать недостающие требования;
3. спроектировать простейший алгоритм;
4. реализовать первую working version;
5. протестировать и локализовать ошибки;
6. использовать программу;
7. улучшать её последовательными версиями.

Source formula в 13.7:

`Что → Как → Создание → Тестирование → Использование → Поддержка`.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 13.1 | Backup problem analysis: source list, target directory, ZIP archive, timestamp naming, external archiver. |
| 13.2 | `backup_ver1.py`: `os`, `time`, `os.sep`, `strftime`, command-string construction, `os.system`, debugging by printing/running `zip_command`. |
| 13.3 | `backup_ver2.py`: date subdirectory + shorter time-based archive names; `os.path.exists` and `os.mkdir`. |
| 13.4 | `backup_ver3.py`: user comment added to archive name; intentionally broken logical line produces `SyntaxError`. |
| 13.5 | `backup_ver4.py`: fixes continuation with `\`; comment spaces replaced with underscores. |
| 13.6 | Suggested improvements: verbosity `-v`, command-line sources via `sys.argv` + `list.extend`, replace external `zip`/`os.system` with `zipfile` or `tarfile`. |
| 13.7 | Development lifecycle distilled into analysis, design, implementation, testing/debugging, deployment/operation, maintenance. |
| 13.8 | Reader is encouraged to build a program using the same recipe. |

## Source implementation skeleton

```python
import os
import time

source = ['"C:\\My Documents"', 'C:\\Code']
target_dir = 'E:\\Backup'

target = target_dir + os.sep + time.strftime('%Y%m%d%H%M%S') + '.zip'
zip_command = "zip -qr {0} {1}".format(target, ' '.join(source))

if os.system(zip_command) == 0:
    print('Резервная копия успешно создана в', target)
else:
    print('Создание резервной копии НЕ УДАЛОСЬ')
```

## Operational acceptance

Для каждой working version source принимает успех, когда:

- script завершается без syntax/runtime failure;
- `os.system(zip_command)` возвращает source-success condition;
- target ZIP archive создаётся по вычисленному пути;
- программа печатает success message.

Для version 3 expected result, наоборот, — показанный `SyntaxError: invalid syntax`,
который используется как debugging lesson.

## Safety boundary

Эта глава содержит реальные state-changing actions:

- `os.mkdir(today)` создаёт directory;
- external `zip -qr ...` создаёт/перезаписывает archive path в зависимости от target;
- `os.system(zip_command)` выполняет shell command;
- versions 1/2/4 intended to create backup archives;
- Windows source path/PATH instructions and external GnuWin32 dependency are historical.

Перед использованием на реальной системе source-specific paths
`C:\My Documents`, `C:\Code`, `E:\Backup` требуют **[Needs confirmation]**.

Source не предоставляет rollback procedure для созданных directories/archives.

## Conditional artifacts

Раздел 13.8 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
