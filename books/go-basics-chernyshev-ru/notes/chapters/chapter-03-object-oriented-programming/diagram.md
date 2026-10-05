# Диаграмма — глава 3: struct → methods → interfaces → generics

~~~mermaid
flowchart TD
    A["Domain state"] --> B["struct"]
    B --> B1["fields"]
    B --> B2["pointer / nested / anonymous fields"]
    B --> C["methods"]
    C --> C1["value receiver"]
    C --> C2["pointer receiver"]
    C2 --> D["constructor function New..."]
    D --> E["package boundary"]
    E --> E1["Uppercase = exported"]
    E --> E2["lowercase = hidden/internal"]
    E2 --> E3["protect invariants"]
    E --> F["composition"]
    F --> F1["embedded struct"]
    F1 --> F2["promoted methods / same-name outer method"]
    F --> G["interfaces"]
    G --> G1["implicit satisfaction"]
    G --> G2["argument / return / slice"]
    G --> G3["interface as struct field"]
    G --> H["runtime polymorphism"]
    H --> H1["type assertion"]
    H --> H2["type switch"]
    H --> H3["nested interfaces"]
    H --> I["generics"]
    I --> I1["any"]
    I --> I2["comparable"]
    I --> I3["union constraints"]
    I --> I4["~ underlying type"]
    I --> J["Tic-tac-toe v.2"]
    J --> J1["Board"]
    J --> J2["Player"]
    J --> J3["Game"]
~~~

## Project transformation

~~~text
v.1 procedural package state
→ identify domain responsibilities
→ Board owns board behavior
→ Player owns current-player behavior
→ Game coordinates state + input + loop
→ v.2 object-oriented organization
~~~

## Interface decision flow

~~~text
Need shared behavior across different concrete types?
→ define small method set
→ concrete type implements methods
→ accept interface in function/field
→ swap concrete implementation without changing caller logic
~~~

## Provenance

- structs: `p0153:c01–p0160:c01`
- methods/constructor/encapsulation/composition: `p0161:c01–p0168:c01`
- interfaces: `p0168:c01–p0183:c01`
- generics: `p0184:c01–p0189:c01`
- project v.2: `p0190:c01–p0196:c01`
