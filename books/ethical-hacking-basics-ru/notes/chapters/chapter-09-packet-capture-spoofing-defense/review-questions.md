# Практические задания главы 9

Source содержит два явных блока **«Практическое задание»** в разделе 9.1.

## Задание 1 — tcpdump capture

**Источник:** PDF p. **252**, `ethical-hacking-basics-ru:p0252:c01`.

Source asks to:
1. захватить packets/frames с помощью tcpdump в собственной локальной сети;
2. во время capture взаимодействовать с интернет-ресурсом;
3. сохранить capture в файл.

**Safety adaptation:** выполнять только на разрешённом interface/network. PCAP может содержать чужие credentials, tokens, DNS names, addresses and content. Exact interface, storage path and retention: **[Needs confirmation]**.

## Задание 2 — Wireshark filtering

**Источник:** PDF p. **254**, `ethical-hacking-basics-ru:p0254:c01`.

Source asks to:
1. открыть capture, сохранённый на предыдущем шаге;
2. применить Wireshark filter так, чтобы остался web traffic, относящийся к выполненному browsing activity.

## Что зафиксировать

- capture time window;
- interface;
- capture command/options;
- PCAP hash/path;
- display filter;
- один подтверждённый flow/request family;
- privacy handling.

Actual capture/output/filter result: **[Needs confirmation]**.
