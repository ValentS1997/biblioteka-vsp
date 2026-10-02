# Шпаргалка: базовый operational workflow по главе 2

Цель: сначала получить наблюдаемое состояние, затем выполнить минимальное изменение и проверить результат.

## Symptom / problem framing

Типовые задачи главы:

- найти файл, каталог или команду;
- понять текущий рабочий каталог;
- посмотреть содержимое файла или длинный вывод;
- локализовать первую ошибку;
- найти и при необходимости остановить процесс;
- проверить права доступа;
- проверить symbolic link;
- проверить архив перед распаковкой;
- выполнить привилегированную команду через sudo.

## Baseline / context

### Shell и пути

- абсолютный путь начинается с <code>/</code>;
- относительный путь — нет;
- <code>.</code> — текущий каталог;
- <code>..</code> — родительский каталог;
- <code>~</code> часто обозначает home directory;
- shell выполняет wildcard expansion до запуска команды.

### Стандартные потоки

- stdin — стандартный ввод;
- stdout — стандартный вывод;
- stderr — диагностический поток;
- pipe <code>|</code> передаёт stdout одной команды в stdin другой.

### Базовая иерархия

<code>/bin</code> — основные исполняемые файлы;  
<code>/dev</code> — файлы устройств;  
<code>/etc</code> — системная конфигурация;  
<code>/home</code> — home обычных пользователей;  
<code>/lib</code> — библиотеки;  
<code>/proc</code> — процессы и параметры ядра через файловый интерфейс;  
<code>/run</code> — runtime state;  
<code>/sys</code> — интерфейс к устройствам и системе;  
<code>/sbin</code> — системные исполняемые файлы;  
<code>/tmp</code> — временные данные;  
<code>/usr</code> — основная масса пользовательских программ и данных системы;  
<code>/var</code> — изменяемые данные, логи и кэши.

## Read-only checks

### Где я и что здесь есть

~~~bash
pwd
pwd -P
ls
ls -l
ls -F
ls -a
~~~

### Найти и посмотреть данные

~~~bash
grep root /etc/passwd
find dir -name file -print
locate pattern
file file
less file
head /etc/passwd
tail /etc/passwd
diff file1 file2
sort file
~~~

Для длинного вывода:

~~~bash
grep ie /usr/share/dict/words | less
~~~

<code>locate</code> работает по периодически создаваемому индексу, поэтому новый файл может не найтись.

### Документация

~~~bash
man ls
man -k keyword
man 5 passwd
info command
~~~

Также глава указывает на <code>--help</code>/<code>-h</code> и каталог <code>/usr/share/doc</code>.

### Процессы

~~~bash
ps
ps x
ps ax
ps u
ps w
ps aux
ps auxw
ps $$
jobs
kill -l
~~~

Сначала определить PID и состояние процесса, затем решать, нужен ли сигнал.

### sudo audit

~~~bash
journalctl SYSLOG_IDENTIFIER=sudo
~~~

В старых системах журнал может находиться в <code>/var/log</code>, например <code>/var/log/auth.log</code>.

## Interpretation

### Ошибка команды

Сначала читать первую ошибку и разложить её на программу, объект/путь и конкретную причину.

Частые категории главы:

- <code>No such file or directory</code> / ENOENT;
- <code>File exists</code>;
- <code>Not a directory</code> / <code>Is a directory</code>;
- <code>No space left on device</code>;
- <code>Permission denied</code>;
- <code>Operation not permitted</code>;
- <code>Segmentation fault</code> / <code>Bus error</code>.

### Процесс

Обычное завершение выполняется сигналом TERM. STOP временно останавливает процесс, CONT продолжает его. Неигнорируемый KILL в источнике прямо обозначен как крайняя мера.

### Права доступа

<code>ls -l</code> показывает тип файла и три набора прав: user, group, other.

Биты:

- <code>r</code> — read;
- <code>w</code> — write;
- <code>x</code> — execute;
- <code>-</code> — право отсутствует.

Для каталога read позволяет перечислить содержимое, а execute нужен для доступа к объектам внутри.

### Архив

Перед extraction источник рекомендует сначала проверить содержимое tar-архива в режиме <code>t</code>. Это снижает риск распаковать множество файлов прямо в неподходящий текущий каталог.

## Next action

1. Получить read-only baseline.
2. Если есть ошибка — сначала исправлять первую.
3. Если требуется изменение — выбрать минимальную операцию.
4. Для destructive/privileged действия перепроверить аргументы и путь.
5. После изменения повторить подходящий read-only check.

## Modifying action

Глава подтверждает операции копирования, перемещения, создания и удаления файлов/каталогов; изменение shell/environment variables; перенаправление вывода; отправку сигналов процессам; изменение прав; создание symbolic links; архивирование/распаковку; изменение пароля/shell и выполнение команд через sudo.

Опасные варианты, которые источник отдельно сопровождает предупреждениями, не вынесены здесь в copy-paste блоки. Точный перечень и classification приведены в [commands.md](commands.md).

## Verification / acceptance checks

| Изменение | Проверка из главы |
|---|---|
| copy/move/create | <code>ls</code> / <code>ls -l</code> |
| working directory | <code>pwd</code> / <code>pwd -P</code> |
| permissions | <code>ls -l</code> |
| process signal | повторный <code>ps</code> для нужного PID |
| background job | <code>jobs</code> |
| symbolic link | длинный listing показывает <code>link -> target</code> |
| tar archive | режим <code>t</code> до extraction |
| sudo activity | <code>journalctl SYSLOG_IDENTIFIER=sudo</code> |

## Rollback

- ошибочный временный <code>PATH</code>: источник рекомендует запустить новую shell;
- STOP: продолжить процесс сигналом CONT;
- ошибочная symbolic link: источник рекомендует найти ошибочную ссылку и удалить её;
- остальные destructive/state-changing операции: <code>[Needs confirmation]</code>, если глава не даёт гарантированного обратного действия.

## Минимальный workflow

~~~text
задача
  ↓
pwd / ls / man / grep / find / ps
  ↓
понятно текущее состояние?
  ├─ нет → собрать ещё read-only evidence
  └─ да
       ↓
нужно изменение?
  ├─ нет → завершить
  └─ да
       ↓
проверить path / PID / permissions / target
       ↓
минимальное изменение
       ↓
повторный read-only check
~~~
