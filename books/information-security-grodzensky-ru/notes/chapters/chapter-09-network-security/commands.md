# Средства и механизмы главы 9

Shell-команд в главе нет. Ниже — только классы технологий и контролей, явно названные в RAG.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| Proxy server | Посредник между пользователем и ресурсом | stateful/network | Контролирует доступ, может кэшировать/фильтровать | Policy/traffic observation | [Needs confirmation] |
| Reverse proxy | Доступ внешних пользователей к внутренним ресурсам через посредника | stateful/network | Публикует/посредничает доступ | Traffic/policy check | [Needs confirmation] |
| SWG | Secure Web Gateway | stateful/network | URL/app filtering, SSL inspection, integration | Policy and event verification | [Needs confirmation] |
| Packet filter | Сетевая фильтрация | stateful/network | Фильтрация по packet headers | Rule/traffic verification | [Needs confirmation] |
| Stateful inspection | Контроль пакетов и состояния сессий | stateful/network | Использует state table | Session/policy check | [Needs confirmation] |
| NGFW | Application-aware firewall | stateful/network | Анализ приложений/пользователей/трафика | Policy/event verification | [Needs confirmation] |
| IDS/IPS | Detection / prevention | monitor/block | Обнаруживает или блокирует вторжения | Alert/blocking result | [Needs confirmation] |
| VPN / GOST VPN | Удалённый защищённый доступ | stateful/network | Организует remote access | Connection/policy verification | [Needs confirmation] |
| Anti-APT | Защита от целевых атак | analysis/response | Sensors + sandbox + endpoint capabilities | Detection workflow | [Needs confirmation] |
| Sandbox | Анализ неизвестного объекта | workload-generating | Выполняет объект в эмулируемой среде | Behavioral verdict | [Not applicable] |
| EDR | Endpoint detection/response | monitor/response | Детектирует аномальные процессы/IOC | Endpoint event | [Needs confirmation] |
| NAC | Network access control | state-changing | Классифицирует устройства и управляет доступом | Access/quarantine status | [Needs confirmation] |
| EMM | Mobile-device policy control | state-changing | Используется NAC для проверки mobile posture | Agent/policy state | [Needs confirmation] |
| SIEM | Централизация событий | observability | Получает события от СЗИ | Event ingestion | [Not applicable] |

## Proxy types из источника

- gateway;
- direct proxy;
- reverse proxy;
- transparent proxy;
- SOCKS proxy;
- DNS proxy;
- web proxy.

## SWG-функции, перечисленные в главе

- блокирование заражённых сайтов;
- блокирование опасных web applications;
- URL filtering;
- SSL inspection;
- IPS integration;
- threat-intelligence/cloud-service integration;
- DLP integration;
- caching/compression;
- mobile-user protection;
- IM filtering;
- access-control policies;
- traffic shaping;
- reporting.

## NAC-сценарии

- isolate host on EDR/AV signal;
- quarantine unknown host;
- vulnerability scan before access;
- check EMM agent on mobile device;
- restrict device if policy is not met.

## Operational boundary

- CLI-команд нет.
- Firewall/proxy/NAC vendor syntax не добавлялся.
- YARA упомянута только как capability sandbox, без правил.
- Текущие protocol/security best practices не подменяют source terminology.
