# Шпаргалка: прикладной уровень

## Goal / context

Использовать главу 7, когда нужно понять поведение конкретного сетевого сервиса:

- name resolution;
- e-mail submission/transfer/retrieval;
- Web/HTTP request-response;
- caching, cookies и tracking;
- streaming audio/video;
- real-time communication;
- CDN/P2P content distribution.

Конкретный сервис/симптом: [Needs confirmation].

## 1. DNS

Проверить:

- какое domain name разрешается;
- recursive или iterative context;
- authoritative vs cached answer;
- record type;
- TTL/cache state;
- zone/delegation;
- privacy path: traditional DNS или encrypted resolver path.

Подтвержденный практический запрос:

```text
dig ns @a.edu-servers.net cs.uchicago.edu
```

Интерпретация:

- root/TLD/authoritative servers выполняют разные роли;
- cached record может устареть согласно TTL;
- DNS name может соответствовать нескольким IP addresses;
- encryption DNS traffic скрывает содержимое query от части observers, но меняет вопрос о том, кто видит resolver traffic.

## 2. Электронная почта

Разделить три этапа:

1. submission от user agent;
2. message transfer между mail servers;
3. final delivery / mailbox access.

Ключевые механизмы:

- SMTP/ESMTP — transfer/submission;
- MIME — типы и представление content;
- DNS MX — выбор receiving mail server;
- IMAP — remote mailbox access;
- webmail — browser-based user agent.

Подтвержденный учебный инструмент:

```text
telnet mail.isp.com 25
```

После greeting глава предлагает `HELP` внутри SMTP session.

## 3. Web / HTTP

Определить:

- URL scheme/host/path;
- HTTP или HTTPS;
- static или dynamic content;
- server-side или client-side generation;
- request method и response status;
- cache state и validation headers;
- persistent/pipelined/multiple connection behavior.

Глава рассматривает HTTP как request-response protocol; HTTPS — HTTP поверх защищенного transport mechanism.

Caching может уменьшить повторную передачу, а headers вроде `Last-Modified`, `Expires`, `ETag` и `Cache-Control` участвуют в cache decisions.

## 4. Web state / privacy

Проверить:

- first-party/third-party cookies;
- tracking across sites/devices;
- cookie syncing;
- browser/device fingerprinting.

Не считать отключение cookies полным устранением tracking: глава отдельно показывает fingerprinting как независимый механизм.

## 5. Streaming audio/video

Разделить:

- encoding/compression;
- transport;
- buffering;
- adaptation;
- real-time signaling.

Для stored streaming:

- network jitter маскируется playback buffer;
- low/high water marks управляют buffer state;
- DASH/HLS делят media на короткие segments;
- client может выбирать representation в зависимости от network conditions.

Для interactive real-time traffic absolute delay важнее, чем для stored playback.

## 6. H.323 / SIP

Оба относятся к real-time communication, но архитектура различается.

H.323 описывается как более полный protocol stack.

SIP — более modular signaling mechanism и может работать поверх TCP или UDP.

Media transfer использует отдельные transport mechanisms; signaling и media не следует смешивать.

## 7. Content delivery

Проверить архитектуру:

- browser cache;
- shared web proxy/cache;
- server farm;
- CDN;
- P2P.

CDN размещает cached copies ближе к clients и распределяет load.

P2P использует ресурсы самих peers.

BitTorrent:

- torrent metadata;
- tracker или DHT;
- chunks;
- rare-piece selection;
- peer incentives/choking strategy.

## Interpretation

- DNS, HTTP, SMTP и media protocols имеют разные application semantics даже при использовании одного transport layer.
- Name resolution и content delivery связаны: DNS может использоваться для направления клиента к подходящей content copy.
- HTTP caching и CDN решают схожую задачу на разных масштабах — уменьшить повторную дальнюю доставку.
- Jitter и delay — разные свойства; buffering помогает со jitter stored media, но добавляет startup delay.
- P2P масштабирует distribution capacity вместе с участниками, но требует discovery, integrity metadata и incentive mechanisms.

## Next action

- Transport behavior TCP/UDP/QUIC → глава 6.
- Network path/routing/IP → глава 5.
- Security mechanisms TLS, attacks, authentication/cryptography → глава 8.
- Если вопрос остается application-layer, уточнить конкретный protocol, object/message/media flow и observed response.

## Modifying action

[Not applicable]

Глава не задает универсальной configuration command для application services.

## Verification / acceptance checks

Анализ согласован с главой, когда:

- конкретный application protocol определен;
- DNS naming/resolution не смешивается с IP routing;
- SMTP transfer не смешивается с mailbox retrieval;
- HTTP request/response и cache state разделены;
- tracking mechanisms не сводятся только к cookies;
- streaming analysis учитывает buffering/jitter/adaptation;
- CDN/P2P различаются по placement/control model;
- `dig` и `telnet` используются только в роли подтвержденных учебных observations.

## Rollback

[Not applicable]

Canonical modifying action в главе отсутствует; rollback-команда источником не задана.
