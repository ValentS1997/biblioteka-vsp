# Авторское итоговое резюме главы 9

**Источник:** `9.2 Спуфинг-атаки (ARP, DNS, DHCP, sslstrip) и их обнаружение`, **Шаг 7**, начинается в `ethical-hacking-basics-ru:p0271:c02` и продолжается через `p0272:c01`, `p0272:c02`, `p0273:c01`.

## 1. Packet capture / sniffing

Source подводит итог: sniffing — перехват сообщений, проходящих через network interface, на уровне L2 с передачей захваченных данных приложению анализа. Автор отдельно напоминает, что фактически на L2 захватываются frames, хотя в обиходе используется выражение packet capture.

## 2. Capture tools

В summary перечислены tcpdump, Windump, tshark и Wireshark. Wireshark выделяется protocol decoding, statistics, protocol hierarchy, endpoints и expert information.

## 3. Доставка трафика к анализатору

В switched network нужный трафик не всегда проходит через analyst interface. Source рассматривает SPAN/port mirroring как легитимный способ копировать трафик на monitoring port; также упоминаются spoofing-методы как способ перехвата, но они являются отдельной high-risk attack boundary.

## 4. Spoofing classes

Автор повторяет концепции:
- ARP poisoning для изменения L2 forwarding;
- DNS spoofing/redirection;
- DHCP exhaustion/rogue DHCP;
- sslstrip как исторический MITM example.

Эти техники показывают, как attacker может перенаправить traffic, но не являются готовым разрешением на выполнение.

## 5. Detection / protection

Source summary связывает defensive detection с:
- unsolicited ARP activity;
- tracing MAC to switch ports;
- reverse-path checks for suspicious source IP paths;
- unexpected DHCP offers / excessive DHCPDISCOVER;
- local DNS controls, TCP discussion and DNSSEC.

## Boundary

- p. 273 завершает главу 9.
- p. 274 начинает главу 10.
- Spoofing/MITM/DHCP-exhaustion actions в ходе анализа не выполнялись.
