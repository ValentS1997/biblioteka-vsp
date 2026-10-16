# Глава 15 — диаграммы IDT, fault и внешних IRQ

**Источник:** canonical RAG PDF 253–268, листинги 15.1–15.7. Эти диаграммы аналитические, не снимки Bochs и не аппаратная спецификация вне книги.

```mermaid
flowchart TD
    A["Событие: INT, fault или IRQ"] --> B["Номер события n"]
    B --> C["IDTR: база и предел IDT"]
    C --> D{"Gate n: 8*n в пределах limit?"}
    D -->|"Нет"| E["General Protection Fault #13"]
    D -->|"Да"| F["Gate хранит selector:offset ISR"]
    F --> G{"Тип Gate"}
    G -->|"Trap: 1111b"| H["IF сохраняется"]
    G -->|"Interrupt: 1110b"| I["IF очищается"]
    H --> J["ISR и кадр возврата"]
    I --> J
    J --> K["IRET; для #GP учитывать DWORD кода ошибки"]
```

```mermaid
flowchart TD
    A["max_int = 39"] --> B["40 Gate по 8 байт = 320"]
    B --> C["IDTR.limit = 319 = 0x13f"]
    C --> D{"Номер вектора"}
    D -->|"0..39"| E["Запись IDT доступна"]
    D -->|"40"| F["Offset 0x140: за пределом"]
    F --> G["#GP 13; error code 0x142"]
    G --> H["IDT bit = 1; индекс 0x140/8 = 40"]
```

```mermaid
flowchart TD
    A["Источник в обычной настройке PIC"] --> B["IRQ0: vector 8"]
    B --> C["Protected mode: 8 = Double Fault"]
    C --> D["Коллизия назначений"]
    D --> E["Авторский опыт 15.5: remap PIC"]
    E --> F["IRQ0..7 → vector 32..39"]
    F --> G["8 Interrupt Gate"]
    H["Исключения CPU 0..31"] --> I["32 Trap Gate"]
    G --> J["IRQ device handler → EOI → IRET"]
    I --> K["Fault/trap handler → IRET, error-code-aware"]
```

```mermaid
flowchart LR
    A["EFLAGS IF=1 перед событиями"] --> B["Trap Gate"]
    A --> C["Interrupt Gate"]
    B --> D["В ISR IF остаётся 1"]
    C --> E["В ISR IF становится 0"]
    F["CPL=0 в примере"] --> G["Изменение IOPL не меняет доступ портов"]
```

В диаграммах «EOI» относится к внешним аппаратным прерываниям, а дополнительный DWORD ошибки — только к соответствующим fault-исключениям, например #GP, не ко всем `int`. Сценарии переполнения IDT, #GP и перенастройки PIC не исполнялись. Точные сообщения Bochs и значения регистров — [Needs confirmation].
