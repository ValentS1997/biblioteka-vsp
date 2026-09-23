# Команды главы 32

Этот раздел исторический. Он перечисляет ранние UNIX utilities, но почти не обучает их современному использованию.

Не добавлять syntax/options из model memory или других глав.

## Source-supported command inventory

| command | purpose | what_to_check | type |
|---|---|---|---|
| `cal` | простая утилита-календарь | глава лишь фиксирует наличие команды в UNIX 1971 | read-only |
| `cat` | конкатенация и вывод | точные options/syntax здесь не описаны | read-only |
| `chdir` | изменение рабочего каталога | exact verification/rollback syntax в главе отсутствуют | state-changing |
| `chmod` | изменение режима | исходный mode и rollback syntax: [Needs confirmation] | state-changing |
| `chown` | изменение владельца | исходный owner и rollback syntax: [Needs confirmation] | state-changing |
| `cmp` | сравнение двух файлов | exact output/exit semantics в этой главе не описаны | read-only |
| `cp` | копирование файла | destination semantics и rollback в этой главе не описаны | state-changing |
| `dc` | калькулятор | syntax не приводится | read-only |
| `du` | отчет об использовании дискового пространства | exact options/units не приводятся | read-only |
| `ed` | редактор | exact editing/verification/rollback workflow не приводится | state-changing |

## Commands named without enough local semantics

Глава также называет:
- `as` — assembler;
- `date`;
- `grep`;
- `who`.

Для `grep` и `who` они используются в историческом обсуждении pipeline composition.

Не добавляем:
- modern options;
- flags;
- exact examples;
- exit codes;
- package-specific behavior;

поскольку эта глава их не дает.

## Pipeline concept

Source-supported concept:

~~~text
program output
→ standard channel
→ next program input
~~~

Глава объясняет pipe как generalized mechanism for connecting programs.

Из этого выводятся три UNIX principles:
- one program does one task well;
- programs work together;
- text streams act as a common interface.

OCR точного символа pipe в историческом примере поврежден, поэтому exact command line не нормализуется.

## State-changing command boundary

### chdir

Effect:
- chapter states that it changes the working directory.

Verification:
- [Needs confirmation].

Rollback:
- [Needs confirmation].

### chmod

Effect:
- chapter states that it changes mode.

Precondition:
- исходный mode: [Needs confirmation].

Verification:
- [Needs confirmation].

Rollback:
- restore previous mode;
- exact syntax: [Needs confirmation].

### chown

Effect:
- chapter states that it changes owner.

Precondition:
- исходный owner: [Needs confirmation].

Verification:
- [Needs confirmation].

Rollback:
- restore previous owner;
- exact syntax: [Needs confirmation].

### cp

Effect:
- chapter identifies it as file copy.

Verification:
- [Needs confirmation].

Rollback:
- [Needs confirmation].

### ed

Effect:
- chapter identifies it as editor.

Verification:
- [Needs confirmation].

Rollback:
- [Needs confirmation].

## Workload-generating commands

The chapter does not provide enough local detail to classify a specific named historical utility as workload-generating in the operational sense used by this repository.

Do not invent such a classification merely to populate the category.

## Historical, not operational CLI chapter

The chapter's CLI value is architectural/history context:

~~~text
small utilities
+ standard streams
+ composition
→ UNIX operating style
~~~

For modern command usage, use the dedicated technical chapters rather than inferring syntax here.
