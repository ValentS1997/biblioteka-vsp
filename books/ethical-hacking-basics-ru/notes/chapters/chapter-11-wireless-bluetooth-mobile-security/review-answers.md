# Разбор практических заданий главы 11

Это RAG-grounded acceptance criteria, а не официальный answer key и не результаты реального wireless testing.

## Задание 1 — monitor/reconnect observation

Expected evidence:
- authorized interface and AP/BSSID;
- channel/time window;
- management/authentication/association frames visible around reconnect;
- distinction between radio-management evidence and application data;
- normal connectivity restored after monitor-mode work.

Actual PCAP/results: **[Needs confirmation]**.

## Задание 2 — survey comparison

Compare:
- SSID/BSSID set visible to each tool;
- channel;
- signal level;
- security-mode labels if available;
- tool/mode differences.

Different results do not automatically mean one tool is wrong: channel hopping, scan timing, adapter support and passive/active behavior can affect visibility.

## Задание 3 — deauthentication lab

The learning objective is to observe that deauthentication causes station reconnect/authentication behavior and creates corresponding radio frames.

Acceptance criteria:
- only owned lab AP/client affected;
- no neighbor/third-party stations targeted;
- start/stop time documented;
- outage impact observed and accepted;
- Wireshark evidence preserved;
- client/AP reconnect normally afterward.

No deauthentication command or result is supplied by these artifacts. Actual execution: **[Needs confirmation]**.
