# Диаграмма — глава 1: от окружения к первой программе

~~~mermaid
flowchart TD
    A["Установить Go<br/>и проверить go version"] --> B["Создать module<br/>go mod init"]
    B --> C["package main + func main()"]
    C --> D["Переменные<br/>var / := / ="]
    D --> E["Типы данных"]

    E --> E1["Numbers<br/>int / float / complex"]
    E --> E2["Text/logic<br/>byte / rune / string / bool"]
    E --> E3["Collections<br/>array / slice / map"]
    E --> E4["Pointers<br/>& / * / nil / new"]

    E3 --> F["Constants<br/>const / iota"]
    E4 --> F

    F --> G["Operators<br/>precedence"]
    G --> H["Control flow"]

    H --> H1["if / else"]
    H --> H2["switch / case"]
    H --> H3["for / range"]
    H3 --> H4["break / continue"]
    H --> H5["goto<br/>discouraged"]

    H1 --> I["Explicit conversions<br/>numeric / strconv"]
    H2 --> I
    H4 --> I

    I --> J["I/O + formatting<br/>fmt / bufio / os.Stdin"]
    J --> K["Standard library helpers"]

    K --> K1["strings"]
    K --> K2["slices"]
    K --> K3["maps"]

    K1 --> L["Tic-tac-toe v.0"]
    K2 --> L
    K3 --> L

    L --> L1["Board size 3..9"]
    L --> L2["Validate moves"]
    L --> L3["Rows / columns / diagonals"]
    L --> L4["win / draw / quit"]

    L --> M["Summary + 36 review questions"]
~~~

## Chapter logic

Глава движется от минимально необходимого execution environment к языковым примитивам, затем к структурам данных и control flow, после чего добавляет ввод/вывод и функции стандартной библиотеки. Финальный проект собирает эти элементы в одну работающую программу.

## Important branch points

~~~text
same-looking data?
→ verify type
→ convert explicitly if required

string indexing?
→ ASCII/bytes acceptable?
   ├─ yes → byte indexing
   └─ no  → range / []rune

copy collection?
→ array → assignment copies
→ slice → allocate + copy when independence is required

repeated control?
→ for
   ├─ finite condition
   ├─ range
   └─ infinite for {} + explicit break
~~~

## Provenance

- environment: `p0018:c01–p0022:c01`
- variables/syntax: `p0023:c01–p0026:c01`
- types/collections: `p0027:c01–p0044:c01`
- constants/operators/control: `p0045:c01–p0063:c01`
- conversions/I/O: `p0064:c01–p0078:c01`
- standard library: `p0079:c01–p0092:c01`
- project: `p0092:c01–p0098:c01`
