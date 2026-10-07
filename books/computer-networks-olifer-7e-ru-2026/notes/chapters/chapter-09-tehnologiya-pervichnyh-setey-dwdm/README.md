# Глава 9 — Технология первичных сетей DWDM

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0268:c01` … `p0281:c01`.
- PDF pages: **268–281**, включительно; **15** адресуемых RAG chunks.
- Печатные страницы книги: **267–280**.
- На `p0268:c01` явно начинается «Глава 9. Технология первичных сетей DWDM».
- На `p0282:c01` явно начинается «Вопросы к части II»; этот блок не входит в scope главы 9.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Принцип работы DWDM | 268–270 | `p0268:c01`–`p0270:c01` | wavelength/spectral channels, direct optical multiplexing/switching, dispersion/interference/diffraction/reflection |
| Частотные планы | 271–272 | `p0271:c01`–`p0272:c01` | CWDM vs DWDM, fixed grids, flexible grid, spectral overlap |
| Оборудование и топологии | 272–273 | `p0272:c01`–`p0273:c01` | linear/ring/mesh, T-MUX, OADM, amplifiers, dispersion compensation |
| Терминальные мультиплексоры | 273–275 | `p0273:c01`–`p0275:c01` | transponders, O-E-O wavelength conversion, optical mux/demux, filters/gratings |
| OADM | 275–276 | `p0275:c01`–`p0276:c01` | fixed-wavelength optical add/drop |
| Оптические усилители | 276 | `p0276:c01` | EDFA, Raman amplification, transparent optical amplification |
| Компенсация дисперсии | 277 | `p0277:c01` | G.652/G.655 context, chromatic/PMD compensation, DSP-based compensation |
| Mesh / OXC / ROADM / WSS | 277–281 | `p0277:c01`–`p0281:c01` | optical cross-connects, remote reconfiguration, direction/color flexibility, wavelength-selective switching |

Boundary anchors: [p0268:c01](../../../rag/chunks/p0201-p0300/p0268-c01.md) → [p0281:c01](../../../rag/chunks/p0201-p0300/p0281-c01.md) → [p0282:c01](../../../rag/chunks/p0201-p0300/p0282-c01.md).

## Главный принцип

**DWDM масштабирует оптическую магистраль, передавая несколько независимых спектральных каналов одновременно в одном волокне и выполняя ключевые операции непосредственно над световыми сигналами.** Это частный случай frequency-division multiplexing: каждый канал занимает свой участок спектра и может независимо усиливаться, вводиться/выводиться или коммутироваться.

## Что важно вынести

1. **“Волна” — инженерное сокращение.** Source отдельно уточняет, что более точное понятие — спектральный канал; длина волны обозначает его центральную wavelength/frequency. `p0268:c01`–`p0269:c01`.
2. **DWDM использует optical physics как механизм обработки.** Dispersion, interference, diffraction и reflection применяются не только как impairments, но и как основы mux/demux/switching devices. `p0269:c01`–`p0270:c01`.
3. **DWDM — частный случай FDM, но операции могут выполняться напрямую в optical domain.** В отличие от SDH/OTN processing, optical mux/switching itself does not require O-E-O conversion. `p0270:c01`.
4. **Frequency plan is resource allocation.** Fixed plans give equal-width slots; flexible grid allows different slot widths as long as they do not overlap. Narrower spacing increases spectral efficiency but raises equipment/coding requirements. `p0271:c01`–`p0272:c01`.
5. **Topology uses specialized optical nodes.** Linear chains use terminal multiplexers, OADM, amplifiers and optional dispersion compensators; ring adds path redundancy; mesh needs cross-connect capability. `p0272:c01`–`p0277:c01`.
6. **Transponder bridges client optics and a DWDM spectral channel.** Source describes fixed client→wavelength association in the basic model and O-E-O wavelength conversion using tunable lasers. `p0273:c01`.
7. **Optical mux/demux may use filters or diffraction structures.** Thin-film filters scale poorly because cascaded losses accumulate; diffraction-phase structures are presented as better suited to many channels. `p0273:c01`–`p0275:c01`.
8. **OADM performs fixed add/drop.** A module extracts one configured wavelength and can insert the same wavelength after it has been removed, avoiding a same-wavelength collision. `p0275:c01`–`p0276:c01`.
9. **Optical amplifier ≠ regenerator.** EDFA/Raman amplifiers increase optical power without converting the signal into electrical form; a regenerator restores signal form/timing through conversion. `p0276:c01`.
10. **Dispersion remains a transport constraint.** Source discusses special fiber, compensation devices and DSP-based receiver compensation; exact need depends on rate/system. `p0277:c01`.
11. **OXC enables mesh topology.** Optical cross-connects can be optoelectronic or fully photonic; source calls the latter lambda routers. `p0277:c01`–`p0278:c01`.
12. **ROADM turns wavelength routing into remotely changeable state.** Administrator can alter switching tables without sending an engineer to physically add/drop modules for each change. `p0278:c01`–`p0281:c01`.
13. **WSS is the core wavelength-selection function.** It selects required wavelengths from multiple incoming colourless signals according to a switching table and combines selected channels on an output. `p0279:c01`–`p0280:c01`.
14. **Reconfigurable does not automatically mean colorless/directionless.** Source explicitly distinguishes basic ROADM from architectures where any local port can use any wavelength and any line direction. `p0281:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed optical components/mechanisms; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта optical channel → mux/add-drop/amplify/switch.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance и source-snapshot findings.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 268–281 **не обнаружено** → `summary.md` не создаётся.
- `p0282:c01` начинает **«Вопросы к части II»**, относящиеся сразу к главам 6–9. Поэтому chapter-specific `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG содержит footer contamination, OCR/glyph substitutions и потерю spatial semantics у optical paths/filters/WSS diagrams. Grid spacing, amplifier reach/bandwidth, standards and device-capability statements are source snapshots and are not asserted as current universal design limits.
