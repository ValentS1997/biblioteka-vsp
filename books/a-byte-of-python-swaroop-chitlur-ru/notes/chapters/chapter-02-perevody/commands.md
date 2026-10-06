# Commands and tools — глава 2 «Переводы»

## Result

Исполняемых shell-, Python-, Git- или иных CLI-команд в RAG главы 2 нет.

## Source-confirmed procedure: e-mail deobfuscation

В конце главы дана текстовая инструкция для адресов e-mail:

| Source token | Replace with |
|---|---|
| `-at-` | `@` |
| `-dot-` | `.` |
| `-underscore-` | `_` |

Остальные дефисы в адресе источник предписывает оставить без изменений.

Classification: **read-only text transformation**.

Это правило не является shell-командой и не должно автоматически превращаться в
скрипт/regex из общих знаний.

## Source-referenced tools/projects

В тексте упоминаются как контекст, а не как команды:

- Python
- Python Numeric
- TurboGears
- zhpy
- DocBook
- Ubuntu
- Gentoo/Linux
- C#, .NET, Ruby, Java, C++

## Workload-generating commands

[Not applicable]

## State-changing commands

[Not applicable]

## Verification

Для e-mail transformation проверить, что заменены только три явно указанных токена,
а прочие дефисы оставлены без изменений.

## Rollback

Для текстовой подстановки: вернуть исходное замаскированное представление. Конкретная
автоматизированная процедура rollback в источнике не задана.
