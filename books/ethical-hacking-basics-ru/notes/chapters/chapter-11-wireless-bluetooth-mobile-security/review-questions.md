# Практические задания главы 11

Source содержит три явных блока **«Практическое задание»**.

## Задание 1 — наблюдение Wi‑Fi authentication traffic

**Источник:** PDF p. **301**, `ethical-hacking-basics-ru:p0301:c01`.

Source asks to:
1. enable monitor-mode capture in Wireshark on the wireless interface;
2. observe radio traffic between the local system and AP;
3. disconnect and reconnect;
4. observe the radio traffic during reauthentication.

**Safety:** use only your authorized adapter/AP/client. Monitor mode may interrupt normal connectivity.

## Задание 2 — сравнение WLAN survey results

**Источник:** PDF pp. **307–308**, `p0307:c01`–`p0308:c01`.

Source asks to:
1. list wireless networks visible through the OS;
2. compare them with Kismet, WiFi Explorer or NetSpot;
3. compare available networks by signal level.

This is an observation/survey exercise; do not actively probe neighbors beyond the tool’s approved passive mode.

## Задание 3 — deauthentication lab

**Источник:** PDF pp. **315–316**, `p0315:c01`–`p0316:c01`.

Source asks to use mdk4 against **your own AP**, attempt a deauthentication attack and observe the radio traffic with Wireshark.

Because this is disruptive, the executable deauth command is not reproduced here.

Required lab preconditions:
- owned/explicitly authorized AP and client;
- isolated channel/radio scope;
- outage accepted;
- recovery/reconnect plan;
- no third-party clients in scope.

Actual lab/AP/channel/results: **[Needs confirmation]**.
