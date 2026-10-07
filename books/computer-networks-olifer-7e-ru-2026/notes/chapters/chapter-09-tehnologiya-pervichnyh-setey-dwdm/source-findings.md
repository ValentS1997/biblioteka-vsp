# Source findings — глава 9

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 268–281; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основным текстом или caption.

**Решение:** footer не считается содержанием книги и не переносится в canonical artifacts.

## F-02 — [Source extraction issue] OCR/glyph and unit degradation

Встречаются смешанные glyphs в `DWDM`, `CWDM`, `ROADM`, `OADM`, `WSS`, lambda symbols and frequency units. Например, на странице frequency-plan text extraction у диапазона/единиц есть подозрительные substitutions.

**Решение:** standard acronyms and clearly supported units are normalized; questionable literal values are not silently repaired.

## F-03 — [Source extraction issue] Optical figures lose spatial semantics

Figures 9.1–9.9 represent rays, gratings, wavelength paths, add/drop modules, mesh topology, WSS and MEMS mirrors. Text RAG retains captions/labels but not full geometry.

**Решение:** Mermaid/SVG are new source-grounded conceptual diagrams, not exact figure reproductions.

## F-04 — [Source snapshot] Grid and component capabilities are edition-specific

The chapter names fixed DWDM spacings, flexible-grid rules, CWDM spacing, EDFA/Raman bands/reach, transponder reach and generation-specific ROADM capabilities.

**Решение:** preserve as source context only. Current G.694.1 revision, vendor grid support, coherent modulation and amplifier specifications require external/current verification.

## F-05 — [Semantic trap] “Wave” vs spectral channel

Source explicitly notes that the transported signal occupies a frequency spectrum; “wavelength” refers colloquially to the central wavelength of a spectral channel.

**Решение:** artifacts prefer `spectral channel / wavelength` and avoid treating it as an infinitely narrow monochromatic carrier.

## F-06 — [Semantic trap] All-optical DWDM does not mean every component avoids O-E-O

Source emphasizes optical-domain multiplexing/switching/amplification, but the terminal transponder described at `p0273:c01` performs O-E-O wavelength conversion.

**Решение:** distinguish client adaptation/transponding from all-optical line processing rather than making the blanket claim “DWDM never converts to electrical”.

## F-07 — [Boundary finding] Questions are part-level, not chapter-level

`p0282:c01` begins «Вопросы к части II» and includes material spanning chapters 6–9.

**Решение:** questions are outside chapter-9 boundary and are not converted into chapter-specific review artifacts.
