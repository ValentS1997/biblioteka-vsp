# Команды главы 14

В таблицу включены только команды, прямо перечисленные в RAG главы 14. Глава не приводит для них точный синтаксис или options, поэтому он не реконструируется.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `ifconfig` | Конфигурирование wireless/network interface | correct interface, link/address state before and after change | state-changing |
| `iwlist` | Получение списка доступных wireless access points | visible SSID/AP set and expected coverage | read-only |
| `iwconfig` | Настройка wireless connection parameters | selected interface/SSID/settings are intentional | state-changing |
| `wpa_supplicant` | Аутентификация в wireless network или wired 802.1X | authentication succeeds and intended network is reached | state-changing / authentication-session |

## Read-only baseline

Из перечисленных chapter commands гарантированно read-only only `iwlist`.

Перед изменением wireless client configuration следует зафиксировать как минимум:

- target interface;
- currently visible SSIDs/APs;
- intended SSID;
- intended security domain/VLAN;
- current management path.

Exact read-only syntax for `ifconfig`/other tools in this chapter: `[Needs confirmation]`.

## State-changing actions

### `ifconfig`

Chapter role: configure wireless interface.

Risk:
- link loss;
- address loss;
- remote management lockout.

Verification:
- interface is up and attached to intended network;
- expected reachability returns.

Rollback:
- exact rollback command is not provided by chapter RAG: `[Needs confirmation]`.

### `iwconfig`

Chapter role: configure wireless connection parameters.

Risk:
- association to wrong SSID/AP;
- loss of existing wireless session.

Verification:
- intended wireless settings are active;
- client reaches intended network.

Rollback:
- `[Needs confirmation]`.

### `wpa_supplicant`

Chapter role: authenticate to wireless or wired 802.1X network.

Risk:
- failed authentication can leave interface without usable network access;
- wrong policy/credentials may lead to wrong network selection depending on external configuration.

Verification:
- authentication succeeds;
- client receives intended network access.

Rollback:
- `[Needs confirmation]`.

## Non-command diagnostic tools explicitly named by chapter

- cable tester / time-domain reflectometry for electrical cable faults;
- Fluke LanMeter as an example LAN tester;
- T-BERD as an example WAN tester;
- Wireshark as a packet analyzer.

These are not converted into invented CLI commands.

## Operational rule

Do not change speed/duplex, VLAN, MTU, WAP/channel/security or cabling state from this chapter by inventing vendor commands. The chapter explains the concepts but does not supply a canonical CLI for those actions. Use `[Needs confirmation]` until the target platform's own configuration is available.
