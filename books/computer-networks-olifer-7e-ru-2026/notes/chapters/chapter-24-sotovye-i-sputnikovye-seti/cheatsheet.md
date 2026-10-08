# Cheatsheet — глава 24. Сотовые и спутниковые сети

Source: computer-networks-olifer-7e-ru-2026; PDF pp. 721–783; RAG p0721:c01–p0783:c01; policy: **rag_only**. Только концептуальная диагностика, **не результаты измерений/проверки работающей операторской сети**.

## Symptom / problem framing

Различать типы отказов и деградаций: radio coverage/airtime, attach/authentication, IP и GTP user plane, handover/paging, SIP registration/IMS и медиа RTP, конфигурацию функций 5G и динамику спутникового доступа. Фраза «нет сети» ничего не говорит об уровне неисправности.

## Baseline / context

| Участок | Компоненты / состояние | RAG |
|---|---|---|
| LTE RAN | UE, сота/base station, C-RNTI, OFDMA DL / SC-FDMA UL, resource block | p0723–p0725, p0735–p0736, p0747 |
| EPC / LTE control | MME, HSS, subscriber/auth, SGW, PGW; разделение ролей | p0725–p0727 |
| LTE user plane | GTP-U/TEID, направление PGW↔SGW↔base station, таблицы туннелей | p0731–p0734, p0739 |
| Mobility | attach, handover, idle/paging, change of target cell, roaming | p0735–p0745 |
| Multimedia | SIP/IMS, P-/S-/I-CSCF, HSS, RTP | p0750–p0760 |
| 5G service | slices, eMBB/URLLC/MIoT, NSSF, AMF/SMF/UPF, 5G NR | p0762–p0769 |
| Satellite/NTN | GEO/MEO/LEO, gateway, inter-satellite links, Doppler, transparent/regenerative mode | p0774–p0783 |

## Read-only checks

Это **вопросы к доступным наблюдениям**, не готовые команды оператора.

1. UE получает сигнал и синхронизацию нужной соты? Есть временный C-RNTI и назначенные ресурсные блоки? Подтверждена ли аутентификация, а не только радиодоступ? [p0735–p0737]
2. Назначен ли IP-адрес и построена ли необходимая цепочка туннелей? Отличаются ли GTP signaling/control от user plane? [p0731–p0739]
3. Где именно теряются пакеты: radio access, локальный GTP-туннель base station↔SGW, SGW↔PGW или внешний IP? TEID локален для направления и **не является сквозным идентификатором UE**. [p0732–p0734]
4. При handover меняются ли base station, SGW, MME, C-RNTI и сессионные ключи? Был ли разрешён доступ к ресурсам целевой соты? [p0740–p0743]
5. Если данные работают, но звонок не устанавливается: прошла ли отдельная SIP/IMS registration, каков результат INVITE, доступен ли P-/S-/I-CSCF, установлен ли RTP-путь? [p0750–p0760]
6. Для 5G: какая услуга/слайс, какие управляющие функции, известен ли уровень виртуализации? Разделены ли радиодоступ/транспорт и 5G Core? [p0764–p0768]
7. Для спутников: GEO/MEO/LEO, шлюз и видимость, необходимость inter-satellite relay, прогнозируемый handover и влияние Doppler/погоды? [p0774–p0783]
8. Проверены ли источники значений для скоростей, задержек и количества спутников? Данные книги относятся к историческому срезу; текущие значения **[Needs confirmation]**. [p0763, p0779–p0782]

## Interpretation

- Присутствие радиосигнала ≠ успешный attach, авторизация или функционирующий IP/GTP тракт.
- Рабочий интернет ≠ успешная SIP registration, установление голосового вызова или прохождение RTP.
- GTP-C устанавливает/меняет туннели, GTP-U несёт user packets; IP-адрес UE не должен использоваться транзитными маршрутизаторами для маршрутизации по внутреннему туннельному пути.
- LTE и 5G Core представляют **разные архитектурные модели**. Механически переносить функции MME/SGW/PGW в интерфейсы 5G SBA нельзя.
- Network slice — логическая специализация ресурсов/функций, а не автоматически выделенная физическая сеть и не доказательство соблюдения SLA.
- LEO handover может происходить даже при неподвижном наземном терминале, потому что перемещается покрытие спутника.
- Сами по себе FHSS/beamforming/радиопокрытие не дают доказательства полной криптографической защиты и отказоустойчивости.

## Next action

Построить топологический и сервисный dependency snapshot: UE → RAN → SGW/PGW либо 5G Core/UPF → external network; отдельный signaling graph (MME/HSS или AMF/AUSF) и, при голосе, IMS. Для спутника обозначить орбиту, radio link, gateway и маршрутизацию. Наблюдения, owner, версии, действующие статусы — **[Needs confirmation]**.

## Modifying action

Создание/сброс туннелей и сессий, смена слайса, регистрация SIP, изменение radio parameters, cell reselection/handover или NTN политики может разорвать услуги. В книге **нет** платформенных команд, разрешённого scope, precheck, change window и регламентированного rollback. Никаких production-настроек не выполнять по одному учебному анализу.

## Verification / acceptance checks

- RAN/control-plane/user-plane/IMS и спутниковый транспорт разделены.
- GTP-U и GTP-C, TEID и UE-IP, attach и handover различены.
- SIP signaling и RTP media не смешаны.
- Функции LTE и 5G не слиты в одну схему.
- Не заявлены текущие Starlink/Iridium/SLA или регуляторные разрешения без live evidence.
- Конфликтные порты/имена/числа исходника отмечены в source-findings.md.

## Rollback

Read-only анализ: **[Not applicable]**. Для state-changing действий нет подтверждённых команд/снимков/порядка отката: **[Needs confirmation]**. Ни один реальный network element не изменён.
