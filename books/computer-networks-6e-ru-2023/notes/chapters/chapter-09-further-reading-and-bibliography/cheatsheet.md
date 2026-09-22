# Шпаргалка: как использовать главу 9

## Goal

Глава 9 нужна не для диагностики сети, а для выбора следующего источника после завершения основной книги.

## 1. Сначала выберите предметную область

| Раздел | Область |
|---|---|
| 9.1.1 | Введение и общая картина компьютерных сетей |
| 9.1.2 | Физический уровень |
| 9.1.3 | Канальный уровень |
| 9.1.4 | MAC / Ethernet / Wi-Fi / Bluetooth |
| 9.1.5 | Сетевой уровень / IP / routing / SDN |
| 9.1.6 | Транспортный уровень / TCP / UDP |
| 9.1.7 | Прикладной уровень / Web / media / CDN / IoT |
| 9.1.8 | Сетевая безопасность |

## 2. Для общей ориентации

В начале 9.1 источник указывает типы публикаций, за которыми стоит следить:

- журналы и периодические издания IEEE/ACM;
- SIGCOMM и связанные publications;
- конференции SIGCOMM, NSDI, MobiSys, SOSP и OSDI.

Это discovery channels, а не operational tools.

## 3. Representative reading paths

### Введение

RAG рекомендует, среди прочего:

- Comer — «The Internet Book»;
- Kurose and Ross — «Computer Networking»;
- McCullough — «How the Internet Happened»;
- Naughton — «A Brief History of the Future»;
- Severance — «Introduction to Networking».

### Физический уровень

Направления: 5G, satellite Internet, fiber optics, copper/access networks.

### Канальный уровень

Направления: error-control coding, reliable transmission, retransmission и flow control.

### MAC

Направления: Wi-Fi, Bluetooth, Carrier Ethernet, bridges/spanning tree и Ethernet practice.

### Сетевой уровень

Направления: TCP/IP network layer, IP/ARP/ICMP, routing, SDN и router algorithms/implementation.

### Транспортный уровень

Направления: TCP/UDP, IPv4/IPv6 context и internet speed measurement.

### Прикладной уровень

Направления: Web, DASH/HLS, VoIP, IoT application protocols, CDN и video streaming.

### Сетевая безопасность

Направления: security engineering, cryptography engineering, steganography, PKI/protocols, adversarial thinking и malware detection.

## 4. Когда использовать 9.2

Раздел 9.2 — не tutorial, а алфавитная библиография.

Использовать его, когда:

- в 9.1 выбрана конкретная работа;
- в основной главе книги встретилась ссылка на автора/статью;
- нужна полная библиографическая запись.

## 5. Как читать рекомендации

Не считать любую ссылку универсально «лучшей». Сам источник группирует материалы по назначению и уровню детализации: некоторые работы обзорные, некоторые исторические, некоторые практические, некоторые требуют более глубокого технического фона.

## Next action

1. Определить тему, которую нужно углубить.
2. Перейти в соответствующий подпункт 9.1.x.
3. Выбрать источник по описанию в RAG.
4. При необходимости найти полную запись в 9.2.
5. Дальнейшее содержание выбранного внешнего источника находится вне scope этой главы.

## Modifying action

[Not applicable]

## Verification / acceptance checks

Навигация по главе считается корректной, когда:

- выбранный 9.1.x соответствует нужной предметной области;
- конкретная рекомендация действительно присутствует в RAG;
- полная библиографическая запись при необходимости ищется в 9.2;
- содержание рекомендованного внешнего источника не приписывается главе 9 без отдельного чтения этого источника;
- operational-команды не импортируются из предыдущих глав.

## Rollback

[Not applicable]
