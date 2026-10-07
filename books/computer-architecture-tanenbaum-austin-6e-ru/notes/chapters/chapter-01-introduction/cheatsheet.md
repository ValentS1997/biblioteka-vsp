# Cheatsheet — глава 1 «Введение»

**Provenance:** RAG `p0020:c01`–`p0075:c01`, PDF pages 20–75. Policy: **rag_only**.

## Symptom / problem framing

Типичная проблема этой главы — смешение уровней абстракции:

- «компьютер выполняет Python/C/ассемблер напрямую»;
- «ISA и микроархитектура — одно и то же»;
- «операционная система исполняет вообще все команды программы»;
- «hardware и software имеют жестко заданную границу»;
- «более высокая частота автоматически означает пропорционально большую производительность»;
- «все компьютеры отличаются только мощностью».

Глава предлагает лечить это не запоминанием отдельных моделей, а определением **уровня, языка, способа реализации и trade-off**.

## Baseline / context

Перед анализом архитектурного утверждения зафиксировать:

1. **Какой уровень обсуждается?**
   - digital logic;
   - microarchitecture;
   - ISA;
   - operating-system level;
   - assembly;
   - high-level language.

2. **Что видит пользователь этого уровня?**
   - типы данных;
   - операции/команды;
   - доступные характеристики.

3. **Как поддерживается уровень?**
   - hardware;
   - interpreter;
   - translator;
   - hybrid path.

4. **Какой класс машины обсуждается?**
   - embedded/microcontroller;
   - mobile/game;
   - PC;
   - server;
   - cluster/data center;
   - mainframe.

5. **Какой критерий решения?**
   - cost;
   - speed;
   - reliability;
   - power/heat;
   - compatibility;
   - expected rate of change.

## Read-only checks

Глава не содержит shell/CLI-команд. Read-only checks здесь — концептуальные.

### Check 1 — level ownership

Спросить:

- «Эта характеристика видима пользователю уровня?»
- «Или это деталь реализации нижнего уровня?»

Если свойство относится к видимому интерфейсу уровня — это architectural concern. Если речь о способе реализации памяти/тракта/логики — implementation concern.

### Check 2 — translation vs interpretation

- **Translation:** вся программа верхнего языка превращается в программу нижнего языка, затем исполняется.
- **Interpretation:** команда верхнего языка обрабатывается и сразу исполняется через нижний язык.

### Check 3 — OS level is hybrid

Часть команд уровня ОС совпадает с ISA и может идти в нижнюю реализацию напрямую; дополнительные возможности уровня ОС интерпретируются операционной системой.

### Check 4 — performance claim

Если утверждение основано только на clock rate, проверить, не упускаются ли:

- количество выполняемых одновременно операций;
- организация памяти;
- ширина/объем передачи;
- I/O;
- parallelism;
- architecture/microarchitecture.

### Check 5 — units

Уточнить, что измеряется:

- memory/storage capacity → в главе используются двоичные степени для Кбайт/Мбайт/Гбайт/Тбайт;
- bit-rate → десятичные 10³/10⁶/10⁹/10¹².

## Interpretation

### Уровни

| Уровень/область | Роль в главе |
|---|---|
| Physical devices | Ниже рассматриваемого digital-logic уровня; транзисторы как примитивы |
| Digital logic | Вентили, биты, регистры и базовые цифровые функции |
| Microarchitecture | Registers + ALU + datapath; может контролироваться hardware/microprogram |
| ISA | Опубликованный машинный интерфейс команд |
| OS level | Гибрид: часть ISA-команд + дополнительные виртуальные возможности |
| Assembly | Символическая форма нижележащего языка; обычно транслируется ассемблером |
| High-level language | Языки прикладного программиста; обычно компилируются/иногда интерпретируются |

### Hardware vs software

Не спрашивать «где проходит вечная граница». Спрашивать:

- что дешевле;
- что быстрее;
- что надежнее;
- что чаще придется менять.

Источник рассматривает функциональность как логически переносимую между hardware и software.

### История

Ключевые сдвиги главы:

```text
mechanical
→ vacuum tubes
→ transistors
→ integrated circuits
→ VLSI / personal computers
→ small / embedded / invisible computers
```

Параллельно меняются архитектурные идеи:

```text
wired control
→ microprogramming
→ OS virtual operations
→ compatible families
→ RISC / superscalar / FPGA
→ multicore / parallelism
```

### Спектр систем

Чем ближе к embedded/mobile:
- сильнее ограничения size/power/cost;
- меньше универсальность/расширяемость.

Чем ближе к server/cluster/mainframe:
- выше требования к capacity, I/O, networking, transaction load and continuity.

## Next action

Для любого нового понятия из следующих глав применять один и тот же порядок:

1. Найти его уровень.
2. Назвать видимый интерфейс уровня.
3. Определить, кто реализует этот интерфейс ниже.
4. Отделить architectural property от implementation detail.
5. Зафиксировать trade-off: cost/speed/power/reliability/compatibility.
6. Сравнить минимум две архитектуры/класса машин вместо принятия одной реализации за норму.

## Modifying action

**[Not applicable].**

Глава 1 не задает операционных state-changing действий для реальной системы. Она не содержит команд конфигурации, прошивки, BIOS/UEFI, assembler invocation или изменения ОС.

Не добавлять такие действия из модельной памяти.

## Verification / acceptance checks

После изучения главы читатель должен уметь без внешних источников:

- объяснить разницу translation / interpretation;
- объяснить связь language ↔ virtual machine;
- расположить digital logic, microarchitecture, ISA, OS, assembly и HLL по уровням;
- объяснить, почему OS level назван hybrid;
- различить architecture и implementation;
- объяснить логическую эквивалентность hardware/software и назвать факторы выбора;
- назвать ключевые поколения развития;
- объяснить, почему совместимое семейство машин — отдельная архитектурная ценность;
- различить PC/server/cluster/mainframe/microcontroller contexts;
- объяснить, зачем книге три примера x86/ARM/AVR;
- не путать binary capacity units и decimal bit-rate units.

## Rollback

**[Not applicable].**

Глава не предписывает изменений системы, следовательно rollback procedure отсутствует.

## Короткая формула главы

```text
abstraction level
+ visible architecture
+ lower-level implementation
+ translation/interpretation path
+ engineering trade-off
= useful model of a computer system
```
