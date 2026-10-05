# Диаграмма — глава 2: decomposition, dependencies and testing

~~~mermaid
flowchart TD
    A["Repeated / monolithic code"] --> B["Extract functions"]
    B --> B1["Arguments"]
    B --> B2["Returns"]
    B --> B3["Function values"]
    B1 --> C["Value vs pointer"]
    B2 --> C1["single / multi / named"]
    B3 --> C2["anonymous / higher-order / closure"]
    C2 --> D["Advanced control"]
    D --> D1["recursion"]
    D --> D2["generator via goroutine + channel"]
    D --> D3["defer / LIFO cleanup"]
    C --> E["Organize into packages"]
    C1 --> E
    D --> E
    E --> E1["main = executable package"]
    E --> E2["utility package"]
    E2 --> E3["Uppercase = exported"]
    E --> F["Module"]
    F --> F1["go.mod / go.sum"]
    F --> F2["external dependency"]
    F --> F3["local module via replace"]
    F2 --> F4["tidy / vendor / semver"]
    F --> G["Testing"]
    G --> G1["unit: Test + testing.T"]
    G --> G2["table-driven"]
    G2 --> G3["subtests: t.Run"]
    G --> G4["coverage"]
    G --> G5["benchmark: Benchmark + testing.B"]
    G --> G6["fake data: Faker"]
    G --> H["Tic-tac-toe v.1"]
    H --> H1["package game"]
    H --> H2["InitBoard / Play"]
    H --> H3["private helpers"]
    H --> H4["procedural decomposition"]
~~~

## Core flow

~~~text
one large function
→ separate responsibilities
→ define package boundaries
→ manage dependencies
→ verify behavior with tests
→ measure coverage/performance
→ refactor project without changing core game behavior
~~~

## Decision map

~~~text
Need to change caller value?
├─ no  → pass value
└─ yes → pointer may be appropriate

Need reusable namespace?
→ package

Need dependency boundary?
→ module + go.mod

Need many input combinations?
→ table-driven test

Need per-case visibility?
→ t.Run

Need coverage visibility?
→ coverage profile

Need performance comparison?
→ benchmark
~~~

## Provenance

- functions: `p0101:c01–p0116:c01`
- packages/modules: `p0117:c01–p0131:c01`
- testing: `p0132:c01–p0143:c01`
- project v.1: `p0144:c01–p0149:c01`
