# Source findings — глава 8

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 242–267; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основной строкой, таблицей или caption.

**Решение:** footer не считается содержанием книги и не переносится в artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions

Встречаются смешанные кириллические/латинские glyphs и искажённые acronyms around `OTN`, `SDH`, `PDH`, `ODU`, `OPU`, `OTU`, `GFP`, `TDM`, `Ethernet`, `DWDM`; некоторые числа/units в tables извлечены неоднозначно.

**Решение:** однозначно распознаваемые standard terms нормализуются; спорные literal values не восстанавливаются молча.

## F-03 — [Source extraction issue] Frame/multiplexing diagrams lose spatial semantics

Figures 8.1–8.14 contain topologies, frame matrices, byte positions, tributary-slot interleaving and OTN/DWDM architecture. Text RAG preserves many labels, but spatial structure is incomplete.

**Решение:** Mermaid/SVG are new RAG-grounded conceptual diagrams, not exact reproductions.

## F-04 — [Source snapshot] Rates, standards and technology-status claims are edition-specific

The chapter names ITU-T G.872/G.709, SDH/OTN hierarchy rates, Ethernet mappings, PM-QPSK/PM-QAM examples, restoration times and historical deployment status.

**Решение:** preserve these as statements of the source. Current standard revision, vendor support and modern deployment practice require external verification and are not asserted here.

## F-05 — [Source claim] FEC numerical gain is not treated as a universal guarantee

`p0258:c01` states RS(255,239) correction capability and gives signal/noise, BER and reach benefits.

**Решение:** keep the code/mechanism as source-grounded; treat exact gain, BER improvement and distance extension as source example/claim dependent on system assumptions.

## F-06 — [Semantic trap] OTN frame behavior differs from SDH

Source explicitly states:
- OTN: **fixed frame size, variable transmission time** by hierarchy rate;
- SDH: **frame size grows with hierarchy, transmission period remains 125 μs**.

**Решение:** preserve this distinction explicitly because importing SDH intuition into OTN would produce a conceptual error.

## F-07 — [Needs confirmation] Real transport provisioning state is absent

RAG contains no real OTN vendor inventory, client/container mapping, alarms, FEC counters, slot map, wavelength path or cross-connect configuration.

**Решение:** any production OTN diagnosis/configuration remains **[Needs confirmation]** until real device/topology evidence is supplied.
