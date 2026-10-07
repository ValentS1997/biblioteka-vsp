# Source findings — глава 7

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 215–241; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основной строкой, formula or caption.

**Решение:** footer не считается содержанием книги и не переносится в artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions in acronyms and formulas

Встречаются искажения/смешение кириллицы и латиницы в `NRZ`, `NRZI`, `AMI`, `HDB3`, `QAM`, `TDM`, формулах спектров, I/Q notation and trigonometric expressions.

**Решение:** однозначно распознаваемые standard acronyms нормализуются; повреждённые formula glyphs не реконструируются посимвольно из model memory.

## F-03 — [Source extraction issue] Constellations, spectra and timing diagrams lose spatial semantics

Figures 7.2–7.14 contain signal waveforms, spectra, QAM constellation, codec/TDM diagrams and switching-memory layout. Text RAG preserves captions/labels only partially.

**Решение:** Mermaid/SVG artifacts are new source-grounded conceptual diagrams, not exact reconstructions of original figures.

## F-04 — [Needs confirmation] Numeric rates/frequencies are textbook examples and source snapshots

Source uses examples such as 4B/5B at 125 MHz, telephone channel 300–3400 Hz, modem rates, PCM 8 kHz / 56–64 Kbit/s, FDM guard bands, TDM slot sizes and WDM wavelength/rate examples.

**Решение:** do not treat these as current universal operational limits/defaults without checking the exact physical standard/device.

## F-05 — [Source-model boundary] “Asynchronous TDM” terminology is preserved as authored

The chapter explicitly calls packet-network time sharing an asynchronous TDM variant and reserves unqualified `TDM` for synchronous TDM.

**Решение:** artifact wording preserves this source taxonomy; it is not silently replaced with another terminology scheme.

## F-06 — [Needs confirmation] Error-code capabilities depend on exact code/model

Source states generic Hamming-distance detection/correction relationships and CRC capabilities for its described scheme.

**Решение:** production guarantees for a specific CRC polynomial/FEC scheme, burst length or BER require exact code parameters and standard-specific verification.
