# Протокольные операции и команды — глава 24

Source: p0721:c01–p0783:c01, PDF pp. 721–783, policy rag_only.

## CLI
**Подтверждённых исполнимых команд LTE/5G/IMS/GTP/satellite CLI нет.** Книга описывает протокольные операции, условные адреса и архитектуру; не содержит vendor runbook. Не реконструировать show/config из памяти модели.

## LTE / GTP / RAN

| Объект / операция | Роль по источнику | Воздействие | RAG |
|---|---|---|---|
| Cell search / attach preamble | UE находит соту и инициирует доступ | signaling, workload-generating | p0735 |
| C-RNTI / DCI | локальный временный radio ID и сигнализация выделения resource blocks | data/control radio access; reassignment state-changing | p0735–p0736 |
| Subscriber authentication MME/HSS | проверка учётных данных UE | контроль доступа; security sensitive | p0726, p0737 |
| GTP-C | создание/изменение туннельных контекстов | **state-changing** control plane | p0734 |
| GTP-U / TEID | передача IP user packet в IP/UDP/GTP с локальным tunnel ID | data-plane, workload-generating | p0732–p0734 |
| UDP 2152 | указан в примере GTP user packet | source-stated port, не готовый endpoint | p0733 |
| UDP 2151 | упомянут в схеме data-forwarding вопреки соседнему примеру | source conflict; проверить перед использованием | p0739 |
| PGW↔SGW↔base station | двухуровневые туннели, перепривязка при mobility | создание/изменение state-changing | p0731–p0739 |
| Handover | смена base station и, иногда, SGW/MME/ключей | потенциальный service disruption | p0740–p0744 |
| Idle / paging | обнаружение неактивного UE и вызов к обслуживанию | control signaling | p0744–p0745 |
| OFDMA DL / SC-FDMA UL | использование радиоресурсов | network workload | p0747 |
| MAC HARQ ACK/NACK | retransmissions и error correction | workload-generating, не CLI | p0749 |

## SIP/IMS и 5G

| Операция | Роль | Risk class | RAG |
|---|---|---|---|
| SIP REGISTER | регистрация/обновление местоположения пользователя услуги | session state-changing, auth-related | p0751 |
| SIP INVITE / TRYING / RINGING / OK / ACK | установка и подтверждение вызова | session/signaling workload | p0751 |
| SIP CANCEL / BYE / BUSY HERE | отмена, завершение, отказ | state-changing session lifecycle | p0751 |
| RTP | передача медиа после SIP setup | user traffic workload | p0751, p0760 |
| P-CSCF / S-CSCF / I-CSCF | proxy, serving registration, interrogation IMS | архитектурные роли | p0755–p0760 |
| AMF / SMF / UPF / AUSF / NRF | 5G mobility/access, session, user forwarding, authentication, registry | сервисные функции, не shell команды | p0766–p0767 |
| NSSF / network slice | выбор и специализация logical service network | изменение slice policy state-changing | p0764–p0765 |
| REST/HTTP service interfaces | обращения между сетевыми функциями 5G | API architecture, конкретных вызовов нет | p0767 |

## Спутник и NTN

- GEO/MEO/LEO, Ku/Ka/L/S/V и inter-satellite optical/radio links: типы физического доступа, не конфигурационные команды (p0774–p0778).
- Starlink/Iridium: примеры сетей на дату учебника, а не подтверждённая текущая спецификация оборудования (p0779–p0782).
- 5G NTN transparent/regenerative modes, HAPS и изменения HARQ/handover: архитектурные понятия; нет исполнимых настроек спутника, базовой станции или терминала (p0782–p0783).

## Safety / rollback / verification

Не отправлять реальный SIP INVITE/REGISTER и GTP-C сообщения, не менять slice/TEID и handover параметры без согласованного плана — это влияет на активные соединения. Real environment, access, versions, change window, post-check и rollback: **[Needs confirmation]**. Source port/mapping конфликт см. source-findings.md.
