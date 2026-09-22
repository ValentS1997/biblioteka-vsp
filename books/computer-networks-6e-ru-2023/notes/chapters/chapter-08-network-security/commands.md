# Команды и инструменты главы 8

В главе 8 инструменты упоминаются в контексте reconnaissance, traffic observation и обучения безопасности. Здесь они фиксируются без превращения атакующих примеров в пошаговый runbook.

| Команда / инструмент | Назначение | Что проверить | Тип |
|---|---|---|---|
| `traceroute` | Наблюдать сетевой путь до целевого хоста | Последовательность промежуточных hops, видимая из разрешенной среды | workload-generating |
| `tcpdump` | Перехватывать и просматривать доступный интерфейсу traffic | Реально видимые packets/headers в собственной или явно разрешенной среде | read-only |
| Wireshark | Анализировать захваченный network traffic | Protocol fields и traffic patterns в собственной или явно разрешенной среде | read-only |
| `telnet` | В главе приведен как пример простого TCP connection tool | Только факт установления разрешенного TCP connection к явно разрешенному service | workload-generating |

## Safety boundary

Использовать capture/reconnaissance tools только на собственных системах или в среде с явным разрешением.

Глава описывает connect/half-open/FIN/Xmas scanning и другие attack techniques для объяснения adversary model. Точные operational sequences для таких действий в canonical artifacts не воспроизводятся.

## `traceroute`

Раздел 8.2.1 описывает utility `traceroute`, которая использует возрастающие TTL и ICMP responses, чтобы получить представление о маршруте.

Эффект: создает диагностический network traffic.

Допустимая интенсивность/политика для конкретной сети: [Needs confirmation].

## `tcpdump` и Wireshark

Раздел 8.2.2 называет `tcpdump` и Wireshark инструментами traffic capture.

В canonical context они считаются read-only observation tools; возможность увидеть чужой traffic зависит от network access и authorization boundary.

## `telnet`

Раздел о port scanning упоминает `telnet` как generic connection tool. Источник не задает конкретную безопасную test target или canonical syntax для главы 8, поэтому команда с адресом/портом не формируется.

## Не подтверждены как canonical CLI

Глава обсуждает firewalls, IDS/IPS, IPsec, VPN, WPA2/802.11i, PGP, DNSSEC и SSL/TLS, но не задает универсальные configuration commands для этих механизмов. Такие команды из общих знаний не добавляются.
