# Cheatsheet — глава 6: линии связи

## Symptom / problem framing

**Проблема:** физический линк может «подниматься», но передавать сигнал с недостаточным margin, excessive attenuation/noise/crosstalk или spectral distortion. Для анализа нужно идти от среды и signaling к измеримым параметрам линии, а не сразу к higher-layer symptoms. `p0183:c01`–`p0214:c01`.

## Baseline / context

| Область | Source model | RAG |
| --- | --- | --- |
| Line abstraction | link / channel / circuit | `p0183:c01`–`p0184:c01` |
| Termination | DTE / DCE | `p0186:c01` |
| Medium | guided copper/fiber vs unguided radio | `p0184:c01`–`p0185:c01` |
| Signal | amplitude / frequency / phase / wavelength | `p0188:c01`–`p0190:c01` |
| Spectrum | Fourier harmonics / significant spectrum width | `p0189:c01`–`p0193:c01` |
| Power | attenuation / dB / dBm / link budget | `p0194:c01`–`p0197:c01` |
| Frequency response | bandwidth in Hz | `p0198:c01`–`p0199:c01` |
| Interference | noise / SNR / NEXT / FEXT / BER | `p0199:c01`–`p0202:c01` |
| Information rate | baud / bit/s / states / physical coding | `p0202:c01`–`p0207:c01` |
| Copper | STP/UTP / coax | `p0207:c01`–`p0209:c01` |
| Fiber | SMF/MMF / attenuation / dispersion | `p0209:c01`–`p0212:c01` |
| Cabling system | horizontal / vertical / campus | `p0213:c01`–`p0214:c01` |

## Read-only checks

1. Что именно анализируется: **physical link**, logical channel или end-to-end circuit?
2. Какой medium: copper/fiber/[wireless outside this chapter's wired focus]?
3. Какова длина passive segment и есть ли intermediate repeater/regenerator/amplifier?
4. Каков **link budget**: transmit level, losses/gains, receiver sensitivity? `p0194:c01`–`p0197:c01`.
5. Не смешиваются ли **bandwidth (Hz)** и **capacity/data rate (bit/s)**? `p0198:c01`–`p0203:c01`.
6. Каков SNR и есть ли external noise / crosstalk? Для multi-pair copper source рассматривает NEXT/FEXT. `p0199:c01`–`p0202:c01`.
7. Какая BER наблюдается/допускается? Фактическая BER конкретного линка: **[Needs confirmation]**.
8. Какой physical coding и сколько distinguishable states используется? Без этого capacity line нельзя выводить только из cable type. `p0202:c01`–`p0207:c01`.
9. Для copper: category/shielding/termination/length соответствуют выбранному physical protocol? **[Needs confirmation]** для реального линка.
10. Для fiber: SMF/MMF, wavelength/window, source type, attenuation and dispersion budget? **[Needs confirmation]**.
11. Structured cabling path проходит через какие horizontal/vertical/campus elements? `p0213:c01`–`p0214:c01`.

## Interpretation

- **Attenuation alone is not line quality.** Нужно учитывать frequency dependence, noise, bandwidth и receiver sensitivity. `p0193:c01`–`p0202:c01`.
- **dB and dBm answer different questions.** dB expresses a ratio; dBm expresses an absolute power level relative to a fixed reference. `p0194:c01`–`p0197:c01`.
- **Link budget is a boundary check.** Received level after losses must remain above receiver threshold with required margin; exact margin policy is **[Needs confirmation]** because source does not prescribe one universal value.
- **Bandwidth in Hz is a property of frequency transfer; capacity in bit/s also depends on coding.** One cable can support different rates under different physical-layer schemes. `p0198:c01`–`p0204:c01`.
- **Higher signaling rate broadens spectrum and increases susceptibility to line limitations.** `p0204:c01`–`p0206:c01`.
- **More signal states can carry more bits per symbol, but noise limits distinguishability.** `p0205:c01`–`p0207:c01`.
- **Twisting/shielding target interference; they do not eliminate every impairment.** `p0207:c01`–`p0209:c01`.
- **Fiber removes most electromagnetic interference concerns but introduces optical impairments.** `p0209:c01`–`p0212:c01`.
- **SCS reduces operational chaos.** Standardized paths/panels make moves/adds/changes cheaper than ad-hoc recabling. `p0213:c01`–`p0214:c01`.

## Next action

Для physical-layer troubleshooting использовать порядок:

**identify link/media → verify length/topology → inspect power/link budget → check bandwidth/coding compatibility → assess noise/crosstalk/BER → inspect termination/cable class → for fiber inspect mode/wavelength/dispersion → only then escalate to higher layers**.

Это source-grounded diagnostic sequence; конкретные test instruments, commands and thresholds require platform/standard confirmation.

## Modifying action

**[Not applicable].** Глава не содержит executable configuration commands. Замена cable/media, transmitter power, termination or topology are physical changes and require environment-specific plan/rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- различить link / channel / circuit и DTE / DCE;
- объяснить, зачем используется Fourier/spectrum view;
- различить attenuation, dB, dBm and link budget;
- объяснить bandwidth Hz vs capacity bit/s;
- объяснить SNR, NEXT/FEXT и BER;
- различить baud и bit rate;
- объяснить смысл Shannon/Nyquist limits без вывода production rate из одной формулы;
- сравнить UTP/STP/coax/SMF/MMF по физическим trade-offs;
- назвать основные fiber impairments;
- объяснить hierarchy structured cabling.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для физического изменения линии rollback должен быть спроектирован отдельно: исходный кабель/порт/оптика/patching должны быть зафиксированы до изменения.
