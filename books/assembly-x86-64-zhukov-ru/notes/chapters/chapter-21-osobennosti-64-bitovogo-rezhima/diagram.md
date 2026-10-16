# Глава 21 — концептуальные схемы

**Provenance:** canonical RAG PDF 341–372. Схемы авторские аналитические, не изображения рис. 21.1–21.3. Не являются исполняемыми инструкциями.

```mermaid
flowchart TD
  A["64-bit data: RAX, R8–R15"] --> B{"Width of write?"}
  B -->|"32 bits EAX/R8D"| C["Upper 32 bits become 0"]
  B -->|"8 or 16 bits"| D["Upper bits preserved"]
  C --> E["Use 64-bit register or combine halves"]
  D --> E
  E --> F["Consider sign-extended immediates"]
```

```mermaid
flowchart TD
  A["Code+data located at 0x300"] --> B["Copy block +0x100"]
  B --> C["Copy backwards to handle overlap"]
  C --> D{"Memory reference form"}
  D -->|"RIP-relative"| E["Same relative distances after relocation"]
  D -->|"Absolute"| F["References original address"]
  E --> G["Program and its data relocate together"]
  F --> H["Unexpected old data and corrupted output"]
```

```mermaid
flowchart TD
  A["Caller: compatibility or 64-bit mode"] --> B["SYSCALL"]
  B --> C["Select entry from CSTAR or LSTAR"]
  C --> D["STAR-derived selectors, CPL 0"]
  D --> E["Return RIP in RCX, FLAGS in R11"]
  E --> F["System procedure"]
  F --> G["SYSRET: compatibility; SYSRETQ: 64-bit"]
  G --> H["CPL 3, selectors must have matching DPL"]
```

```mermaid
flowchart TD
  A["64-bit IDT gate: 16 bytes"] --> B{"IST field"}
  B -->|"IST = 0"| C["Stack selected on CPL change"]
  B -->|"IST = 1..7"| D["RSP from corresponding TSS IST"]
  C --> E["64-bit interrupt entry"]
  D --> E
  E --> F["Save return SS and RSP even when CPL unchanged"]
  F --> G["Handler; IRETQ"]
  G --> H{"Environment"}
  H -->|"Bochs"| I["Author reports expected counts"]
  H -->|"PC"| J["Author observes GP13, cause unresolved"]
```

**Ограничения:** рисунки и аппаратные журналы не доступны в RAG как самостоятельные мультимодальные объекты. Отличия Bochs/PC на PDF 365–369 — наблюдения автора, не общие гарантии. В примечании 26 (p. 371) указано, что для программных прерываний поле, прочитанное как код ошибки, может быть частью адреса возврата; не интерпретировать его как достоверный selector.
