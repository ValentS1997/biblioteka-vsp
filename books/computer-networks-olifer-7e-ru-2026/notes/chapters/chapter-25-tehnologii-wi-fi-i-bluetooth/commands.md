# Протокольные операции — глава 25

Канонический источник: p0784:c01–p0820:c01, PDF 784–820, режим rag_only.

## Исполнимые CLI

В главе нет platform CLI и готового runbook. Сведения ниже относятся к сообщениям и механизмам Wi-Fi/Bluetooth, а не к командам управления оборудованием.

## Wi-Fi

| Механизм | Роль | Класс воздействия | RAG |
|---|---|---|---|
| Beacon / Probe | пассивный и активный поиск BSS | radio workload | p0789 |
| Authentication / Association / AID | присоединение STA к BSS | state-changing association | p0789–p0790 |
| DHCP | IP-адресация после ассоциации | state-changing addressing | p0790 |
| To AP / From AP / MAC addresses | определение следующего hop, отправителя и назначения | data plane | p0793–p0794 |
| CSMA/CA, DIFS, CW, backoff | конкуренция за эфир | MAC access | p0795–p0798 |
| SIFS / ACK / Duration / NAV | подтверждение и резервирование времени передачи | MAC protocol | p0796–p0799 |
| RTS / CTS | координация доступа при hidden station | additional radio workload | p0798–p0799 |
| WMM/EDCF, AC_VO/VI/BE/BK, TXOP | классы приоритетов и захват эфира | QoS policy change is state-changing | p0800–p0801 |
| A-MSDU / A-MPDU / BAR / Block ACK | aggregation и bitmap acknowledgment | data plane workload | p0801–p0803 |
| OFDMA RU, MU-BAR | распределение ресурса AP, подтверждение DL | centralized scheduling | p0804–p0805 |
| BSRP / BSR / Basic Trigger / Multi-STA Block ACK | управление UL и коллективное подтверждение | control/data plane | p0806 |
| 802.11k/v/r reassociation | neighbor information, network-assisted selection, fast transition | state-changing connection | p0809–p0810 |
| PLMP / P-HWMP / R-HWMP | neighbor peer link и mesh MAC routing | state-changing topology/routing | p0811–p0813 |

## Bluetooth

| Механизм | Роль | Класс | RAG |
|---|---|---|---|
| Discovery / pairing | поиск, проверка и доверие между устройствами | signaling / security state | p0817 |
| SCO / ACL | синхронная и асинхронная передача | Classic traffic class | p0816 |
| FHSS / TDM | hopping и распределение временных слотов | PHY/MAC | p0817–p0818 |
| Bluetooth LE | энергосберегающая PHY/stack модель | PHY mode | p0819 |
| AFH | адаптивное исключение каналов с помехами от Wi-Fi | radio coexistence | p0820 |

## Change-control boundary

Read-only: анализ существующих схем и измерений. Workload-generating: scanning, probe, discovery и диагностический обмен. State-changing: association, security, radio parameters, QoS, mesh routing или Bluetooth pairing.

Реальные конфигурационные команды, параметры сетей, нормативный допуск, post-change verification и rollback: **[Needs confirmation]**. Значения, противоречащие друг другу в источнике (частоты, RU 242/252, мощности, BLE rates), вынесены в source-findings.md.