# Глава 6 — Линии связи

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0183:c01` … `p0214:c01`.
- PDF pages: **183–214**, включительно; **32** адресуемых RAG chunks.
- Печатные страницы книги: **182–213**.
- На `p0183:c01` явно начинается «Глава 6. Линии связи».
- На `p0215:c01` явно начинается «Глава 7. Кодирование и мультиплексирование данных»; `p0215:c01` в scope главы 6 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Классификация линий связи | 183–187 | `p0183:c01`–`p0187:c01` | link/channel/circuit, primary/overlay networks, guided/unguided media, DTE/DCE, analog/digital lines |
| Спектральное представление | 187–193 | `p0187:c01`–`p0193:c01` | sinusoid, frequency/wavelength/phase, Fourier spectrum, significant harmonics |
| Затухание и энергетический бюджет | 193–198 | `p0193:c01`–`p0198:c01` | attenuation, dB/dBm, receiver sensitivity, link budget |
| Полоса пропускания и помехи | 198–202 | `p0198:c01`–`p0202:c01` | bandwidth in Hz, waveform distortion, SNR, NEXT/FEXT, BER |
| Пропускная способность и кодирование | 202–207 | `p0202:c01`–`p0207:c01` | capacity vs bandwidth, baud vs bit/s, signal states, Shannon/Nyquist limits |
| Витая пара и коаксиал | 207–210 | `p0207:c01`–`p0210:c01` | STP/UTP, cable categories, coaxial variants |
| Волоконно-оптическая линия | 209–213 | `p0209:c01`–`p0213:c01` | SMF/MMF, light sources, attenuation, chromatic/PMD and nonlinear impairments |
| Структурированная кабельная система | 213–214 | `p0213:c01`–`p0214:c01` | horizontal/vertical/campus subsystems and structured cabling economics |

Boundary anchors: [p0183:c01](../../../rag/chunks/p0101-p0200/p0183-c01.md) → [p0214:c01](../../../rag/chunks/p0201-p0300/p0214-c01.md) → [p0215:c01](../../../rag/chunks/p0201-p0300/p0215-c01.md).

## Главный принцип

**Физическая линия ограничивает то, какие сигналы и с какой скоростью можно передать надёжно; итоговая скорость определяется не только кабелем, но и совместным выбором среды, спектра сигнала, мощности, уровня шума и физического кодирования.** Поэтому «кабель поддерживает N Гбит/с» без указания protocol/encoding, длины и качества линии — неполное утверждение.

## Что важно вынести

1. **Link, channel и circuit — разные абстракции.** Link соединяет соседние узлы; channel — выделяемая часть capacity звена; circuit — end-to-end path через несколько links/channels. `p0183:c01`–`p0184:c01`.
2. **DTE и DCE разделяют источник данных и оконечную аппаратуру линии.** DCE отвечает за physical-layer signaling; DTE генерирует/потребляет данные. В LAN граница может быть условной. `p0186:c01`.
3. **Analog/digital line classification относится к способу работы промежуточной аппаратуры.** Analog lines усиливают analog signal; digital lines используют discrete states и regenerators; source связывает их с FDM/TDM respectively. `p0187:c01`.
4. **Спектр позволяет оценить, как среда исказит сложный сигнал.** Fourier decomposition представляет периодический сигнал набором harmonics; width of significant spectrum — ключ к сопоставлению signal и line. `p0189:c01`–`p0193:c01`.
5. **Attenuation и receiver sensitivity формируют link budget.** Нужно проверить, останется ли received power выше sensitivity threshold после всех losses/gains. `p0194:c01`–`p0197:c01`.
6. **Bandwidth в Hz ≠ capacity в bit/s.** Bandwidth — диапазон частот с допустимым attenuation; capacity — максимальная data rate для конкретных line characteristics и coding/protocol. `p0198:c01`–`p0203:c01`.
7. **Noise и crosstalk надо отличать от attenuation.** Source отдельно рассматривает external/internal interference, SNR, NEXT/FEXT и BER. `p0199:c01`–`p0202:c01`.
8. **Baud rate ≠ bit rate.** Одно signal state change может кодировать несколько bits, либо один bit может требовать нескольких signal changes. `p0204:c01`–`p0205:c01`.
9. **Shannon и Nyquist задают разные границы.** Shannon связывает capacity с bandwidth и SNR; Nyquist — с bandwidth и числом distinguishable signal states при выбранном signaling model. `p0206:c01`–`p0207:c01`.
10. **Twisting, shielding и cable category влияют на interference/bandwidth, но source values — snapshot standard examples.** `p0207:c01`–`p0209:c01`.
11. **SMF и MMF решают разные задачи.** Source связывает single-mode with lower attenuation/longer distances and multimode with easier/cheaper coupling but stronger modal effects. `p0209:c01`–`p0212:c01`.
12. **Fiber тоже не идеален.** Attenuation, chromatic dispersion, polarization-mode dispersion и nonlinear effects ограничивают reach/rate. `p0211:c01`–`p0212:c01`.
13. **Structured cabling — engineering system, а не просто кабель.** Оно стандартизует connectors/panels/routes и делит infrastructure на horizontal, vertical and campus subsystems. `p0213:c01`–`p0214:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed physical-layer metrics/components; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта «medium → signal → impairment → capacity → cable system».
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance и sign-convention findings.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 183–214 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри границы главы **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит footer contamination, OCR/glyph substitutions и деградацию формул/figures. Числовые cable/fiber examples и standards-status statements трактуются как source snapshot, а не как автоматически актуальные design limits.
