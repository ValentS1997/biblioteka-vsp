# Команды и инструменты главы 2

Таблица включает только команды и механизмы, явно подтверждённые RAG главы 2. Опасные варианты помечены отдельно.

## v1.6 command contract normalization

Для всех строк с типом `state-changing` применяется следующий контракт:

- **Effect** — действие, явно указанное в колонке «Назначение» или в самой строке.
- **Risk** — только source-supported ограничение/риск из строки или safety notes; если отдельный риск не дан, `[Needs confirmation]`.
- **Verification** — только явно указанный source-supported check; если check не дан, `[Needs confirmation]`.
- **Rollback** — только явно указанный обратный путь; если источник его не даёт, `[Needs confirmation]`.

Этот блок является нормативной интерпретацией таблицы ниже для `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6`; недостающие поля не достраиваются из model knowledge.

| Команда / инструмент | Назначение | Тип | Verification / risk / rollback |
|---|---|---|---|
| <code>echo ...</code> | Вывести аргументы в stdout | read-only | Проверить вывод |
| <code>cat file...</code> | Вывести/конкатенировать содержимое | read-only | Ctrl+D завершает stdin при чтении из терминала |
| <code>ls</code>, <code>ls -l</code>, <code>ls -F</code>, <code>ls -a</code> | Просмотр файлов, типов и metadata | read-only | Базовый verification для файловых изменений |
| <code>cp file1 file2</code> | Копирование | state-changing | Проверить <code>ls</code>; rollback зависит от контекста |
| <code>mv file1 file2</code> | Переименование/перемещение | state-changing | Проверить <code>ls</code>; rollback <code>[Needs confirmation]</code> |
| <code>touch file</code> | Создать файл или обновить timestamp | state-changing | <code>ls -l file</code>; rollback timestamp не дан |
| <code>rm file</code> | Удалить файл | state-changing | Destructive; rollback <code>[Needs confirmation]</code> |
| <code>cd dir</code> | Изменить cwd shell | state-changing | <code>pwd</code> |
| <code>mkdir dir</code> | Создать каталог | state-changing | <code>ls</code> |
| <code>rmdir dir</code> | Удалить пустой каталог | state-changing | Каталог должен быть пуст; rollback <code>[Needs confirmation]</code> |
| recursive removal variant of <code>rm</code> | Удалить каталог вместе с содержимым | state-changing | Источник прямо предупреждает о серьёзном ущербе и запрещает небрежное сочетание с wildcard; rollback <code>[Needs confirmation]</code> |
| <code>echo *</code> | Показать shell glob expansion | read-only | Shell расширяет wildcard до запуска команды |
| <code>grep root /etc/passwd</code> | Фильтрация строк | read-only | <code>-i</code>, <code>-v</code>, <code>-E</code> также описаны |
| <code>less file</code> | Просмотр длинного файла | read-only | Space/b/q; поиск внутри less |
| <code>pwd</code>, <code>pwd -P</code> | Показать cwd; физический путь | read-only | <code>-P</code> помогает при symlink |
| <code>diff file1 file2</code> | Сравнить два текстовых файла | read-only | <code>diff -u</code> упомянут как удобный формат |
| <code>file file</code> | Определить тип файла | read-only | Проверить распознанный формат |
| <code>find dir -name file -print</code> | Поиск в реальном времени | read-only | Wildcards для find следует quote-ить от shell expansion |
| <code>locate pattern</code> | Быстрый поиск по индексу | read-only | Индекс может быть устаревшим |
| <code>head</code>, <code>tail</code> | Просмотр начала/конца данных | read-only | Поддерживаются варианты количества строк |
| <code>sort</code> | Сортировать строки | read-only | <code>-n</code> numeric, <code>-r</code> reverse |
| <code>passwd</code> | Изменить пароль | state-changing | Rollback <code>[Needs confirmation]</code> |
| <code>chsh</code> | Изменить login shell | state-changing | В книге дальше используется bash; rollback <code>[Needs confirmation]</code> |
| <code>STUFF=blah</code> | Shell variable | state-changing | Проверить через expansion |
| <code>export STUFF</code> | Передать variable в environment дочерних процессов | state-changing | Проверить дочерним процессом; rollback <code>[Needs confirmation]</code> |
| <code>echo $PATH</code> | Показать PATH | read-only | Перед изменением PATH |
| <code>PATH=dir:$PATH</code> / <code>PATH=$PATH:dir</code> | Изменить порядок поиска команд | state-changing | Источник: при ошибке временного PATH можно открыть новую shell |
| <code>man ls</code> | Man page команды | read-only | Локальная документация |
| <code>man -k keyword</code> | Поиск man pages | read-only | Выводит page/section/description |
| <code>man 5 passwd</code> | Выбрать конкретный раздел man | read-only | Отличает file format от одноимённой команды |
| <code>info command</code> | GNU info | read-only | Можно передать вывод в less |
| <code>command &gt; file</code> | Redirect stdout с перезаписью | state-changing | Риск: существующий файл затирается |
| <code>command &gt;&gt; file</code> | Append stdout | state-changing | Проверить содержимое файла |
| <code>command 2&gt; file</code> | Redirect stderr | state-changing | Проверить diagnostic file |
| <code>command &gt; file 2&gt;&amp;1</code> | stdout+stderr в один файл | state-changing | Проверить файл |
| <code>head &lt; /proc/cpuinfo</code> | Redirect stdin | read-only | Эквивалентный смысл показан в источнике |
| pipe <code>|</code> | stdout → stdin следующей команды | workload-generating | Пример: <code>head /proc/cpuinfo | tr a-z A-Z</code> |
| <code>ps</code> | Список процессов | read-only | PID/TTY/STAT/TIME/COMMAND |
| <code>ps x</code>, <code>ps ax</code>, <code>ps u</code>, <code>ps w</code>, combinations | Расширенный просмотр процессов | read-only | Перед отправкой signal |
| <code>ps $$</code> | Проверить текущую shell по PID | read-only | <code>$$</code> содержит PID shell |
| <code>kill PID</code> | Отправить TERM | state-changing | Повторить <code>ps</code>; процесс может обработать/игнорировать сигнал |
| <code>kill -STOP PID</code> | Остановить процесс | state-changing | Rollback: <code>kill -CONT PID</code> |
| <code>kill -CONT PID</code> | Продолжить остановленный процесс | state-changing | Повторить <code>ps</code> |
| KILL signal variant | Принудительно завершить процесс | state-changing | Источник: только крайний случай; rollback невозможен в рамках главы |
| <code>kill -l</code> | Таблица сигналов | read-only | До выбора numeric signal |
| <code>jobs</code> | Показать jobs текущей shell | read-only | Найти случайно приостановленные jobs |
| <code>fg</code>, <code>bg</code> | Foreground/background job control | state-changing | Проверить через <code>jobs</code> |
| trailing <code>&amp;</code> | Запустить command в background | workload-generating | Shell возвращает PID; stdin/stdout требуют внимания |
| <code>nohup</code> | Упомянут для работы после logout | workload-generating | Детали — man page; глава не даёт полный workflow |
| <code>chmod g+r file</code>, <code>chmod go+r file</code>, <code>chmod go-r file</code> | Изменить mode bits | state-changing | Проверить <code>ls -l</code>; сохранить прежний mode для rollback |
| <code>chmod 644 file</code> | Абсолютно задать mode | state-changing | Проверить <code>ls -l</code>; риск случайно убрать directory execute |
| <code>umask 022</code>, <code>umask 077</code> | Default permissions для новых объектов | state-changing | Эффект на новые файлы/каталоги; rollback <code>[Needs confirmation]</code> |
| <code>ln -s target linkname</code> | Создать symbolic link | state-changing | Проверить order args и <code>ls -l</code>; без <code>-s</code> создаётся hard link |
| <code>gzip file</code> / <code>gunzip file.gz</code> | Сжатие / распаковка gzip | state-changing | Проверить ожидаемое имя файла |
| <code>tar cvf archive.tar ...</code> | Создать tar archive | state-changing | Listing mode перед extraction |
| tar mode <code>t</code> | Проверить содержимое archive | read-only | Источник рекомендует перед extraction |
| <code>tar xvf archive.tar</code> | Extract archive | state-changing | Проверить структуру путей заранее |
| <code>zcat file.tar.gz | tar xvf -</code> | Streaming decompression+extraction | state-changing | Проверка archive до extraction предпочтительна |
| <code>tar ztvf file.tar.gz</code> | Проверить compressed tar | read-only | Показывает содержимое |
| <code>sudo vipw</code> | Пример privileged command | state-changing | sudo логирует действие; rollback <code>[Needs confirmation]</code> |
| <code>visudo</code> | Редактировать <code>/etc/sudoers</code> с syntax check | state-changing | Проверка синтаксиса встроена в workflow |
| <code>journalctl SYSLOG_IDENTIFIER=sudo</code> | Посмотреть sudo log | read-only | Audit после privileged action |

## Keyboard / shell control

- Ctrl+D — EOF для stdin терминала;
- Ctrl+C — обычно interrupt текущей программы;
- Ctrl+Z — suspend job;
- Ctrl+B/F/P/N/A/E/W/U/K/Y — редактирование командной строки;
- Ctrl+L — refresh terminal;
- Ctrl+R в bash — reverse incremental search, а в некоторых input contexts может иметь другое поведение.

## Safety notes из главы

1. Сначала исправлять первую ошибку.
2. Не завершать процессы без понимания их назначения.
3. KILL — крайняя мера.
4. Не делать файлы доступными для записи всем без необходимости.
5. Перед созданием symlink перепроверять порядок аргументов.
6. Перед extraction tar-архива сначала проверить listing.
7. Для <code>/etc/sudoers</code> использовать <code>visudo</code>.
8. Для привилегированных действий предпочитать <code>sudo</code> постоянной root-shell.
