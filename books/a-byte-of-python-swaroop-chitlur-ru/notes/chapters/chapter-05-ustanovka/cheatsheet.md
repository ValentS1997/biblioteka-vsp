# Chapter 5 cheatsheet — «Установка»

## Symptom / problem framing

Нужно определить, доступен ли Python 3 в системе и, если нет, установить/настроить его
по platform-specific ветке источника.

## Baseline / context

- Python 2.x и Python 3.0, согласно источнику, могут быть установлены одновременно.
- GNU/Linux/BSD: Python, вероятно, уже установлен.
- Windows: источник описывает installer + PATH.
- Mac OS X: источник предполагает наличие Python; при отсутствии приводит Homebrew path.
- Материал отражает историческую редакцию книги и не является проверкой современных OS/package procedures.

## Read-only checks

### GNU/Linux / BSD

```text
python -V
```

Если используется Python 3.x, источник также предлагает:

```text
python3 -V
```

Interpretation:
- получена строка версии → Python доступен;
- получено `command not found` → переход к installation path.

### Windows / Mac OS X

После настройки/установки источник проверяет:

```text
python3 -V
```

## Interpretation

- Сначала verification, затем изменение — это основной operational pattern главы.
- В GNU/Linux/BSD источник даёт два пути установки: compile from source или binary
  packages через package manager.
- Для Windows важны две отдельные задачи: установить Python и обеспечить доступ через PATH.
- Для Mac OS X источник приводит цепочку Homebrew → Python 3 → version check.
- Наличие Python 2.x не является причиной для удаления перед Python 3.0.

## Next action

Если version check успешен, installation branch завершён. Раздел 5.4 говорит, что дальше
книга считает Python 3 установленным и переходит к первой программе.

Если version check неуспешен, выбрать только source-supported platform path; конкретные
недостающие package-manager команды остаются [Needs confirmation].

## Modifying action

### Windows PATH

Effect: добавляется каталог Python к системному `PATH`.

Source examples:
- добавить `;C:\Python33`;
- для старых Windows — строка `PATH=%PATH%;C:\Python33` в `C:\AUTOEXEC.BAT`.

Risk: изменение системного PATH может повлиять на разрешение executable paths.

Verification: `python3 -V`.

Rollback: [Needs confirmation] — source не задаёт отдельную процедуру отката.

### Homebrew installation command

```text
ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"
```

Effect: по source context устанавливает Homebrew.

Risk: команда получает удалённый контент и передаёт его на выполнение Ruby; отдельная
проверка содержимого/целостности в главе не описана.

Verification: [Needs confirmation] для Homebrew как такового.

Rollback: [Needs confirmation].

### Python 3 via Homebrew

```text
brew install python3
```

Effect: устанавливает Python 3 через Homebrew.

Verification:

```text
python3 -V
```

Rollback: [Needs confirmation].

## Verification / acceptance checks

Installation/configuration path принимается как успешный, когда source version check
возвращает информацию о версии Python без ошибки.

## Rollback

Для state-changing installation/PATH operations source-specific rollback procedures
не приведены: **[Needs confirmation]**.
