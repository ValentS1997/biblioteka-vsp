# Глава 7 — Кодирование и мультиплексирование данных

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0215:c01` … `p0241:c01`.
- PDF pages: **215–241**, включительно; **27** адресуемых RAG chunks.
- Печатные страницы книги: **214–240**.
- На `p0215:c01` явно начинается «Глава 7. Кодирование и мультиплексирование данных».
- На `p0242:c01` явно начинается «Глава 8. Технология первичных сетей OTN»; `p0242:c01` в scope главы 7 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Виды и этапы кодирования | 215–219 | `p0215:c01`–`p0219:c01` | Д-Д / Д-А / А-А / А-Д, carrier/information signal, spectrum and code-selection criteria |
| Дискретная информация → дискретные сигналы | 220–226 | `p0220:c01`–`p0226:c01` | NRZ, AMI, NRZI, bipolar pulse, Manchester, 4B/5B, 64B/66B, B8ZS, HDB3, scrambling |
| Дискретная информация → аналоговые сигналы | 226–231 | `p0226:c01`–`p0231:c01` | ASK/FSK/PSK, BPSK/QPSK, QAM, I/Q representation and modulation |
| Обнаружение и коррекция ошибок | 231–233 | `p0231:c01`–`p0233:c01` | parity, CRC/FCS, FEC, Hamming distance, convolutional codes |
| Аналоговая информация → аналоговые/дискретные сигналы | 233–236 | `p0233:c01`–`p0236:c01` | AM/FM for analog information, ADC/DAC, sampling theorem, PCM |
| Мультиплексирование и коммутация | 236–241 | `p0236:c01`–`p0241:c01` | FDM, WDM/CWDM/DWDM, synchronous/asynchronous TDM, time slots and switching |

Boundary anchors: [p0215:c01](../../../rag/chunks/p0201-p0300/p0215-c01.md) → [p0241:c01](../../../rag/chunks/p0201-p0300/p0241-c01.md) → [p0242:c01](../../../rag/chunks/p0201-p0300/p0242-c01.md).

## Главный принцип

**Кодирование должно согласовать информационный поток с физическими ограничениями линии, а мультиплексирование — эффективно разделить общую линию между несколькими потоками.** Поэтому критерии выбора кода — не только “сколько бит в символе”, но и ширина спектра, синхронизация, помехоустойчивость, возможность обнаружения/коррекции ошибок и требуемая мощность; затем выбранный способ разделения ресурса определяет и compatible switching model.

## Что важно вынести

1. **Есть четыре базовых типа преобразования:** discrete→discrete, discrete→analog, analog→analog, analog→discrete. Термин modulation source использует как частный случай coding для analog signals. `p0215:c01`–`p0216:c01`.
2. **Spectrum is a design constraint.** Information signal must fit line bandwidth; changing coding can narrow/shift spectrum and permit a higher clock/data rate on the same medium. `p0217:c01`–`p0219:c01`.
3. **Self-synchronization matters.** Long runs without transitions make receiver clock recovery difficult; source therefore compares codes not only by spectrum but also by transition behavior. `p0219:c01`–`p0223:c01`.
4. **NRZ/AMI/NRZI/Manchester trade spectrum against synchronization and DC component.** None is “best” universally. `p0220:c01`–`p0223:c01`.
5. **Redundant codes intentionally spend bits to constrain bad patterns and detect violations.** Source examples: 4B/5B, 64B/66B; B8ZS/HDB3 modify AMI zero runs; scrambling algorithmically removes long runs. `p0223:c01`–`p0226:c01`.
6. **Analog modulation for discrete data can encode amplitude, frequency or phase.** Source names ASK/FSK/PSK and combined QAM; BPSK/QPSK and multilevel variants carry more information per symbol. `p0226:c01`–`p0230:c01`.
7. **QAM maps bit groups into amplitude/phase states.** I/Q decomposition provides a practical mathematical/implementation model for modulator/demodulator. `p0228:c01`–`p0231:c01`.
8. **Error detection and correction use redundancy differently.** Parity is simple/weak; CRC/FCS gives stronger detection; FEC adds enough redundancy to permit correction. `p0231:c01`–`p0233:c01`.
9. **Hamming distance formalizes code capability.** Source states an (n)-distance code can detect up to (n-1) errors and correct up to ((n-1)/2) under its described model; Hamming codes suit isolated errors, convolutional codes are presented for bursty-error contexts. `p0232:c01`–`p0233:c01`.
10. **Analog information can be digitized by sampling and quantization.** ADC/DAC plus the Kotelnikov–Nyquist sampling condition lead to PCM; source gives 8 kHz voice sampling and 56/64 Kbit/s examples. `p0234:c01`–`p0236:c01`.
11. **Multiplexing, demultiplexing and switching must use compatible principles.** Source groups FDM, WDM and TDM as the bases for those operations. `p0236:c01`.
12. **FDM/WDM divide spectrum; synchronous TDM divides time into periodic slots.** Source associates FDM/WDM with circuit-switched networks, asynchronous TDM with packet networks, and synchronous TDM with circuit switching. `p0236:c01`–`p0241:c01`.
13. **In synchronous TDM, slot position acts as address/state.** Switching can be implemented by reordering bytes/time slots in buffer memory; loss of synchronization destroys this mapping. `p0239:c01`–`p0241:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed coding/multiplexing mechanisms; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта «information → coding → error control → multiplexing».
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance ограничения главы.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 215–241 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри verified boundary **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит повторяющийся посторонний footer/URL, OCR/glyph substitutions и неполное spatial representation спектров, constellation diagrams и TDM/FDM figures. Numeric rates/frequencies and technology examples remain source snapshots, not current universal deployment limits.
