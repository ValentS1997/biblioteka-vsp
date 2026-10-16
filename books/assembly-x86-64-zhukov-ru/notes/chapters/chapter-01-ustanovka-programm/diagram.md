# Глава 1 — логика подготовки среды

**Источник:** `rag/chunks/p0001-p0100/p0015-c01.md`–`p0019-c01.md` (PDF p. 15–19). Схема отражает последовательность книги, не является универсальным troubleshooting playbook.

```mermaid
flowchart TD
  A["Стартовый каталог: arch/01, bochsrc, BAT"] --> B["Добавить BIOS/VGA BIOS, bochs.exe, bochsdbg.exe"]
  B --> C["Запуск __work.bat"]
  C --> D{"disk_c.img доступен?"}
  D -- "Нет: сообщение об отсутствии образа" --> E["Подготовить образ FreeDOS как disk_c.img"]
  E --> F["Запуск __work.bat: проверка C:/>"]
  D -- "Да" --> F
  F --> G["Резервная копия disk_c.img"]
  G --> H["Добавить tools, work, autoexec.bat в образ"]
  H --> I["Повторная загрузка FreeDOS; должен открыться VC"]
  I --> J["Проверка a86, nasm, bitmap"]
  J --> K{"Нет Bad command or filename?"}
  K -- "Нет" --> L["Проверить наполнение образа и пути"]
  K -- "Да" --> M["Сохранить копию рабочего образа"]
  M --> N["Запуск __debug.bat"]
  N --> O["GUI debugger: Continue и загрузка FreeDOS"]
  L --> H
```

**Boundary:** `gui_debug` добавляется только к конфигурации `bochsdbg.exe` через `debug_on.txt`; не делать его постоянной опцией общего `bochsrc` (p. 18).

**Риски:** операции удаления каталога и форматирование USB из p. 16–18 не автоматизированы на схеме. Процедуры возврата для них в RAG не расписаны: [Needs confirmation].
