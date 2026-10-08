# Diagram — Глава 23. Технологии PHY беспроводных сетей

Source: book_id computer-networks-olifer-7e-ru-2026; PDF 687–720, RAG p0687:c01–p0720:c01, strict rag_only. **Концептуальные схемы по тексту**, не реконструкция PDF-рисунков.

## TX / RX и радиосреда

~~~mermaid
flowchart LR
  D["Биты"] --> MOD["Модулятор / мультиплексор"]
  MOD --> DAC["ЦАП"]
  DAC --> MIX["Смеситель с несущей"]
  MIX --> AMP["Усилитель"]
  AMP --> AT["Антенна TX"]
  AT --> RF["Радиосреда: reflection / diffraction / scattering"]
  RF --> AR["Антенна RX"]
  AR --> LNA["Малошумящий усилитель"]
  LNA --> DET["Детектор / преобразование несущей"]
  DET --> ADC["АЦП"]
  ADC --> DEMOD["Демодулятор / демультиплексор"]
  DEMOD --> O["Восстановленные биты"]
~~~

[p0687](../../../rag/chunks/p0601-p0700/p0687-c01.md)–[p0688](../../../rag/chunks/p0601-p0700/p0688-c01.md). Схема не отражает всё разнообразие аналоговой и цифровой реализации.

## Распространение, link budget и чувствительность

~~~mermaid
flowchart TD
  TX["Ptx"] --> C["Потери TX-кабеля Ltx"]
  C --> G["Gain антенны Gtx"]
  G --> E["EIRP"]
  E --> F["FSPL: f и расстояние d"]
  F --> R["Gain Grx и RX-cable losses"]
  R --> P["Prx на входе приемника"]
  P --> S{"Prx достаточен относительно sensitivity?"}
  S -->|В учебной модели да| M["Положительный запас margin"]
  S -->|Нет| L["Потенциально недостаточный уровень"]
  RF["Multipath / fading / ISI / Doppler / interference"] -. "не моделируются FSPL сами по себе" .-> P
~~~

[p0707](../../../rag/chunks/p0701-p0800/p0707-c01.md)–[p0709](../../../rag/chunks/p0701-p0800/p0709-c01.md). Пример чисел источника — 1 km, 2400 MHz, FSPL 100.04 dB, Prx −72.04 dBm, sensitivity −82 dBm; «100 мВ» конфликтная единица: source-findings.md.

## MIMO и распределение ресурса

~~~mermaid
flowchart TD
  A["Антенны TX и RX"] --> Q{"Режим использования"}
  Q --> D["Spatial diversity: реплики одного сигнала"]
  Q --> M["Spatial multiplexing: параллельные потоки"]
  D --> CSI["Оценка канала / CSI"]
  M --> CSI
  CSI --> BEAM["Beamforming / precoding"]
  BEAM --> MU["MU-MIMO: несколько пользователей"]
~~~

[p0701](../../../rag/chunks/p0701-p0800/p0701-c01.md)–[p0707](../../../rag/chunks/p0701-p0800/p0707-c01.md).

## Методы работы со спектром

~~~mermaid
flowchart TD
  BAND["Общая полоса частот"] --> FH["FHSS: hop между подканалами"]
  BAND --> DS["DSSS: исходный бит → chip sequence"]
  DS --> CD["CDMA: разные коды у пользователей"]
  BAND --> OF["OFDM: один поток → ортогональные поднесущие"]
  OF --> OA["OFDMA: scheduler выделяет поднесущие пользователям"]
  OF --> DSP["IFFT / FFT и cyclic prefix"]
~~~

[p0709](../../../rag/chunks/p0701-p0800/p0709-c01.md)–[p0720](../../../rag/chunks/p0701-p0800/p0720-c01.md). OFDM и OFDMA — не взаимозаменяемые обозначения, FHSS не заменяет криптографическую аутентификацию.

## Risk, verification, rollback

Реальных мощностей, потерь, норм регулятора, CSI или результатов измерений нет: **[Needs confirmation]**. Команды изменения RF параметров и rollback в главе отсутствуют. Диаграммы нельзя использовать как production runbook.
