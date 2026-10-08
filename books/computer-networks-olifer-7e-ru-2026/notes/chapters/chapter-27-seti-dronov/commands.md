# Команды и протокольные операции — глава 27

Source: computer-networks-olifer-7e-ru-2026, PDF pp. 844–883, RAG p0844:c01–p0883:c01, **rag_only**.

## Исполнимый CLI

**В главе отсутствуют подтверждённые команды эксплуатации БПЛА, autopilot, радиоинтерфейсов и router/OS CLI.** MAVLink, AODV, Wi-Fi mesh и Sidelink — имена технологий/протоколов, **не готовые команды для полёта**. Не создавать конфигурацию движения, радио, управления реальным БПЛА или вмешательства в полёт из памяти модели.

## Архитектурные операции

| Функция | Роль из главы | Класс / замечание | RAG |
|---|---|---|---|
| UAV-assisted relay / aerial base station | Временное расширение существующей сети | deployment state-changing | p0847 |
| Gateway drone / cluster head | Пересылка между Ad Hoc, кластерами и инфраструктурой | network topology change | p0853–p0855 |
| Neighbor discovery / joining | Самоорганизация peer links | control/radio workload | p0852, p0868 |
| GNSS/IMU position exchange | Навигация и прогноз связности | sensitive operational state, no live data | p0859–p0861 |
| Wi-Fi mesh (802.11s), R-HWMP | L2 forwarding по MAC | changing peers/route state | p0868–p0869 |
| LTE Sidelink Mode 4 / 5G NR Sidelink Mode 2 | D2D/radio resource selection without base station | radio scheduling workload, не универсальный runbook | p0865 |
| mmWave beamforming / SATCOM | High-rate LoS и BLoS links | RF config state-changing; требования зависят от оборудования | p0866–p0868 |
| DHCP / IPv6 autoconfiguration and ND | Адресация в инфраструктурных и Ad Hoc сценариях | addressing state change | p0870–p0871 |
| Mobile IP | Продолжение IP-сессии между наземными сетями | installation/control-plane change requires owner | p0871–p0872 |
| UDP / TCP / QUIC | Transport payload / reliability and mobility | network workload | p0872 |
| MAVLink / MQTT / CoAP / HTTP(S) / FTP(TFTP) / SNMP / RTP(RTSP) / NTP(PTP) | Примеры FANET application / management / time protocols | protocol labels; no usable commands or port defaults supplied | p0862, p0873 |

## AODV: source-supported message semantics

| Сообщение / поле | Роль | Side effect | RAG |
|---|---|---|---|
| RREQ | Broadcast route discovery, address source/destination | signaling workload; flooding bounded by TTL | p0875–p0878 |
| B-ID + request cache | Identifies requests, suppresses duplicate broadcasts | temporary routing/control state | p0876–p0878 |
| TTL / expanding ring | Limits area, increases to find destination | control traffic increases | p0876–p0878 |
| Reverse route | Next-hop toward RREQ origin learned during flooding | temporary state | p0876–p0878 |
| RREP | Unicast response along reverse route; next-hop/hop count learned | route table modifications | p0878–p0879 |
| Sequence number (SN) | Freshness criterion in lesson's example | route replacement logic | p0878–p0879 |
| RERR | Error propagation after link break; invalidates route | routing state-changing | p0879–p0880 |
| Optional HELLO | A possible link-failure detection mechanism | periodic workload | p0880 |

Пример RREQ увеличивает ограничение TTL 2 → 4 → 6; более длинный маршрут может выиграть по времени прибытия RREQ. Это **учебная топология**; не универсальная настройка AODV или доказательство надёжности. Заявление об RFC 9854 и дополнительных полях позиционирования не подтверждено независимой спецификацией, см. source-findings.md.

## DTN: delivery modes

| Механизм | Смысл | Tradeoff | RAG |
|---|---|---|---|
| Store-carry-forward | Долгое хранение до появления контакта | буфер, retention и unpredictable delay | p0881–p0882 |
| Epidemic replication | Копии во многих узлах | ресурсы памяти, airtime, bandwidth | p0882 |
| PROPHET | Вероятность контакта по истории встреч | assumption о мобильности, не гарантия | p0882 |
| Message ferry | Специальный мобильный узел переносит пакеты между partition | движение/энергия/время доставки | p0883 |

## Preconditions, verification, rollback

Read-only: анализ существующей топологии, записей маршрутизации и данных о коммуникационных потоках. Workload-generating: RREQ/discovery, сообщения датчиков и диагностические каналы. **State-changing:** radio configuration, маршрутизация, IP, изменение ролей, управление движением/миссиями, изменение ключей. Real-world flight safety, доступы, версии платформ и regulatory authorizations **[Needs confirmation]**. Процедура rollback отсутствует. **Ничего не запускалось.**