# Команды и инструменты — глава 1 «Введение»

**Provenance:** RAG `p0020:c01`–`p0075:c01`, PDF pages 20–75.

## Source-confirmed operational commands

**[Not applicable].**

В chapter RAG нет shell-команд, команд конфигурации ОС, firmware-команд, assembler/compiler invocation или иной операторской процедуры, которую можно безопасно вынести в operational command sheet.

По контракту v1.7 знакомые команды не добавляются из model memory.

## Source-confirmed conceptual tools

Ниже — не CLI-команды, а механизмы/программы, явно определенные главой.

| Tool / mechanism | Source role | Operational class |
|---|---|---|
| Translator | Преобразует программу верхнего языка в программу нижнего языка целиком | Conceptual, not a shell command |
| Interpreter | Получает программу верхнего языка как input и исполняет команды поочередно через нижний язык | Conceptual, not a shell command |
| Assembler | Транслятор символического языка уровня 4 в более низкий уровень | Conceptual, not invoked by a source command |
| Compiler | Транслятор high-level programs; глава отмечает, что возможна и интерпретация | Conceptual, not invoked by a source command |
| Operating system | Интерпретирует дополнительные возможности уровня 3; часть ISA-identical commands идет ниже напрямую | Conceptual/system component |
| Microprogram | На некоторых машинах интерпретирует ISA-level commands через datapath | Conceptual/implementation mechanism |

## Machine-command examples

Во вводном фрагменте как примеры простых машинных операций названы:

- сложение двух чисел;
- проверка числа на ноль;
- копирование блока данных между областями памяти.

Это **семантические примеры**, а не синтаксис конкретной ISA. Нельзя превращать их в x86/ARM/AVR instructions без дополнительного RAG evidence.

## Named platforms/interfaces

Глава использует как сравнительные примеры:

- x86;
- ARM;
- AVR / ATmega168;
- Arduino.

Она прямо предупреждает, что книга не является руководством по программированию этих архитектур. Поэтому operational syntax здесь **[Not applicable]**.

## State-changing actions

**[Not applicable].**

Источник не предписывает никаких изменений рабочей системы.

## Verification

Проверка данного файла проста: если команда отсутствует в chapter RAG, она не должна появляться здесь.

## Rollback

**[Not applicable]** — state-changing commands отсутствуют.
