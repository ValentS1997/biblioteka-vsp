# RAG-grounded ответы — глава 1 «Введение»

**Provenance:** вопросы `p0073:c01`–`p0075:c01`; ответы основаны только на chapter RAG `p0020:c01`–`p0075:c01`. Это не official answer key.

## 1

- **Translator:** преобразует программу верхнего языка целиком в эквивалентную программу нижнего языка.
- **Interpreter:** получает верхнеуровневую программу как input и исполняет ее команды поочередно через lower-level operations.
- **Virtual machine:** логическая машина, машинным языком которой является язык данного уровня; programmer может рассуждать так, будто она существует непосредственно.

## 2

**В принципе — да**, если microarchitecture exposes a stable target language/interface and compiler can generate it. Но chapter model дает сильные доводы против такого design:

- microarchitecture is an implementation layer, not the normal published programmer interface;
- ISA provides a stable architecture boundary between software and lower implementation;
- bypassing ISA couples compiler output to one microarchitecture;
- changing implementation could invalidate generated code and compatibility.

Следовательно, direct target is conceptually possible but defeats much of the abstraction/compatibility value of ISA.

## 3

Да. Глава уже указывает physical-device level below digital logic, а transistor internals относятся к solid-state physics. Можно продолжать decomposition further into lower physical abstractions. Для книги это просто выходит за scope computer architecture.

## 4

Пусть level-1 program содержит некоторый объем работы и занимает `k` seconds.

На каждом более высоком уровне число semantic commands уменьшается в `m` раз, но интерпретация каждой требует `n` lower-level commands.

Тогда:

- level 2: `k · n/m`;
- level 3: `k · (n/m)^2`;
- level 4: `k · (n/m)^3`.

Это вывод при условии, что остальные overheads игнорируются, как предполагает абстрактная модель задачи.

## 5

Чтобы не платить interpreter overhead там, где операция уже существует на ISA level. Если команда OS level идентична ISA command, ее можно отдать microprogram/hardware directly; otherwise unnecessary interpretation multiplies lower-level work.

## 6

Если одна level-1 command занимает `k` ns, а каждый interpreter требует `n` lower-level service commands:

- level 2: `n·k`;
- level 3: `n²·k`;
- level 4: `n³·k`.

## 7

**Эквивалентны логически:** операция, реализованная software, может быть перенесена в hardware; hardware operation может быть simulated in software.

**Не эквивалентны инженерно:** реализации различаются по cost, speed, reliability and expected change frequency. Поэтому выбор placement — trade-off, а не логическая необходимость.

## 8

RAG-grounded comparison:

- similarity: и fixed mechanical program, и read-only recorded content обладают ограниченной изменяемостью после создания;
- difference: Difference Engine embodies computation in machine mechanism, а compact disc в chapter context — storage medium, на котором могут находиться program/data.

Полная аналогия поэтому некорректна: medium and executing machine are different abstraction roles.

## 9

**RAG-grounded inference from the exercise hint:** program could alter an instruction/address used for a repeated array operation so the next iteration applies the same arithmetic action to the next array element.

Глава подтверждает stored-program principle and modifiable programs, но не дает конкретного code example; exact implementation remains **[Needs confirmation]**.

## 10

Cycle time is only one factor. Chapter material on System/360 and later architectures shows other contributors:

- wider/more data transferred per memory cycle;
- more I/O channels;
- greater memory capacity/bandwidth;
- parallel internal functional work;
- architectural/microarchitectural organization.

Therefore performance ratio can greatly exceed clock/cycle-time ratio.

## 11

**[Needs confirmation] for a complete answer.**

RAG text states:

- fig. 1.4 is the von-Neumann/IAS organization with memory, ALU, control and I/O;
- fig. 1.5 is PDP-8 with a single `omnibus` interconnecting components.

But figure arrows and full graphical I/O routing are not independently encoded in text RAG. Current contract forbids direct PDF-image fallback, so exact path comparison cannot be reconstructed safely.

## 12

Source numbers permit the arithmetic:

- people: `300,000,000`;
- packages/day/person: `2`;
- days/year: `365`.

Annual chips:

`300,000,000 × 2 × 365 = 219,000,000,000` chips.

At $0.01/chip:

`$2,190,000,000` per year.

Comparison with GDP requires current/external economic data and is therefore **[Needs confirmation]** under RAG-only policy.

## 13

Any three examples explicitly named in the microcontroller section are valid, e.g.:

- washing machine;
- microwave oven;
- alarm/security system.

Other source examples include printers, scanners, cameras, automotive systems and medical equipment.

## 14

The chapter uses a common formulation of Moore's trend: transistor count per chip grows by about 60% per year.

If chip area is treated as fixed and transistor area scales inversely with count, linear dimension scales as:

`1 / sqrt(1.6) ≈ 0.79`.

So a 1-micron diameter becomes approximately **0.79 micron** after one year.

This answer depends on the geometric scaling assumption implicit in treating density increase as area scaling.

## 15

Using the source's doubling-every-18-months interpretation:

- 3 years = 2 doublings = `4×` performance → `4 h / 4 = 1 h`;
- 6 years = 4 doublings = `16×` → `4 h / 16 = 0.25 h = 15 min`.

For a job that would take 5 years today:

- start now → finish in 5 years;
- wait 3 years → ~4× faster machine → runtime `5/4 = 1.25` years;
- total from today: `3 + 1.25 = 4.25` years.

Thus, under the model, waiting 3 years finishes about 0.75 year earlier.

## 16

The source provides the 1959 baseline, but a numeric comparison requires choosing a **modern computer's** speed, memory and price. Those values are not in chapter RAG.

Formula once those values are supplied:

`improvement = (memory_ratio × speed_ratio) / price_ratio`.

The analogous Boeing calculation likewise depends on the resulting external-data-derived factor.

Status: **[Needs confirmation]**.

## 17

One cycle is explicitly supported:

`centralized mainframe + terminals → decentralized PC → data-center/cloud recentralization`.

A second plausible source-grounded pattern is **[inference]**:

`fixed/specialized hardware → more programmable implementation → reconfigurable FPGA hardware`.

The chapter discusses these stages, but does not explicitly label this second sequence a cycle; treat it as an interpretation, not a quoted conclusion.

## 18

The chapter itself states only the high-level result: the patent claim was invalidated because prior digital-computer work was attributed to Atanasoff, who had not patented it.

The exercise explicitly requires detailed Internet/court-record research to determine exactly what Eckert/Mauchly patented and why the court reached its decision.

External research is forbidden in current RAG-only chapter workflow. Therefore the full report is **[Needs confirmation]**.

## 19

One defensible RAG-grounded trio:

1. **Charles Babbage** — mechanical computing designs and programmable-machine concepts.
2. **John von Neumann** — stored-program organization that became the basis of most later digital computers.
3. **Robert Noyce** — co-invention of the silicon integrated circuit, enabling the integrated-circuit generations and later microprocessor industry.

This is a reasoned selection from chapter history, not an objective ranking.

## 20

**[Needs confirmation].**

The chapter does not provide a sufficiently complete comparative history of software people to justify a top-three ranking without model memory or external sources. It discusses microprogramming, operating systems, compilers and Microsoft-era software, but not enough to make a rigorous three-person selection.

## 21

**[Needs confirmation].**

The chapter does not provide a history of modern high-traffic websites or enough evidence to rank three people. Answering would require external/current information, which is outside the RAG-only contract.
