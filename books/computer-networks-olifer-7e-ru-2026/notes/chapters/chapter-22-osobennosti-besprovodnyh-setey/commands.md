# Команды и протокольные операции — глава 22

RAG PDF pages 662–686, chunks p0662:c01–p0686:c01; strict rag_only.

## Исполнимые OS/router CLI

**Нет подтверждённых CLI-команд** Linux, OpenWrt, MikroTik, Wi-Fi, LTE или сенсорных платформ. В главе вводятся понятия, классы сети, принципы MAC/радио и энергосбережения, но не приводятся исполнимые команды/конфиги. Не дополнять из памяти командами iw, tcpdump, nmcli, hostapd, batctl, vendor radio/mesh CLI и т. п.

## Названные технологии и протокольные действия

| Понятие / операция | Описание по источнику | Класс и ограничения | RAG |
|---|---|---|---|
| FDM / TDM / WDM | Мультиплексирование разделяемой среды на подсреды | Concept, не CLI; настройка каналов может менять доступность | p0666 |
| Модуляция / адаптивное кодирование | Приспосабливает параметры передачи к изменчивой среде | PHY function; изменение конфигурации state-changing | p0665–p0666 |
| CSMA/CD и CSMA/CA | В тексте сравниваются методы доступа проводных/беспроводных сетей; есть source typo CDMA/CD | Named technology, не запускаемая процедура | p0663, p0666, p0668 |
| AP association / bridge / repeater | Соединение клиентов, повтор кадра, работа в общем сегменте | Data plane; reconfigure AP/repeater — state-changing | p0671–p0672 |
| Ad Hoc discovery/join | Beacons/прослушивание, link establishment, адресация и route join | Протокольные стадии; host/radio state-changing | p0675–p0676 |
| OSPF | Упомянут как пример распределённых маршрутизирующих функций | Example only; нельзя утверждать его применение в произвольном MANET | p0674 |
| MANET / VANET / FANET / WSN | Классы самоорганизующихся мобильных/сенсорных сетей | Taxonomy, не команды | p0676, p0684 |
| Mobile IP | В книге приведён пример сохранения IP-адреса при перемещении | Named protocol, детали в главе 14 | p0678 |
| Authentication / encryption | Защита присоединения и данных от прослушивания | Security design; actual authentication modes не настроены | p0679–p0680 |
| Power adaptation / sleep | Регулирование TX и времени работы радиоинтерфейса | Radio operating mode, potentially state-changing | p0681 |
| Energy-aware routing | Учет числа передач, дальности, уровня батареи | Routing policy changes are state-changing | p0682–p0683 |
| Wi-Fi, Bluetooth, ZigBee, Thread, LTE/5G, LoRaWAN | Классы радиотехнологий в типологии главы | Не CLI и не гарантия поддержки устройством | p0683–p0686 |

## Change discipline

- **Read-only:** изучать уже собранные RF measurements, сведения о PHY/MAC, карту покрытия, список узлов, топологию, политику безопасности.
- **Workload-generating:** проведение активного radio/site survey или экспериментов с каналами создаёт эфирную нагрузку, но пошаговой процедуры в книге нет.
- **State-changing:** настройка channel/TX power, связи AP, routing, encryption/authentication, sleep interval может прервать доступ.
- **Security boundary:** не давать инструкций к spoofing/jamming; источники описывают их как угрозы, а не проверенные методики.
- **Verification:** действующая среда, команды и ожидаемые показатели [Needs confirmation].
- **Rollback:** сохранить исходные настройки и план возврата до любых изменений; конкретный алгоритм отката из RAG [Needs confirmation].

Все значения скорости, диапазонов, времени автономности и латентности — **исторические или примерные данные книги**, не live performance tests.
