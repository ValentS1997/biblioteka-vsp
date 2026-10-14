# Анализ главы 2 — часть II: «Протоколы и инструменты прикладного уровня»

**Книга:** О. И. Цилюрик, «Сети Linux. Модели и приложения», БХВ-Петербург, 2024, ISBN 978-5-9775-1890-1. Inventory: 0039; book_id: linux-networks-tsilyurik-ru-2024. Номер издания: [Needs confirmation].

## Структура и границы RAG

«Анализ главы 2» — пользовательская команда. В первоисточнике это **ЧАСТЬ II**, не пронумерованная глава. Начало: [PDF 62](../../../rag/chunks/p0001-p0100/p0062-c01.md) — заголовок части II, PDF стр. **62**, печатная с. **61**. Последняя: [PDF 131](../../../rag/chunks/p0101-p0200/p0131-c01.md) — список источников, PDF стр. **131**, печатная с. **130**. Следующий заголовок «ЧАСТЬ III» расположен в RAG `rag/chunks/p0101-p0200/p0132-c01.md` и не входит в объём.

Охват: PDF 62–131, **70** страниц, **71** адресуемый чанк (дополнительный `p0130:c02`, [здесь](../../../rag/chunks/p0101-p0200/p0130-c02.md)). Диапазон ID: `linux-networks-tsilyurik-ru-2024:p0062:c01` — `linux-networks-tsilyurik-ru-2024:p0131:c01`.

Source `source/book.pdf`; SHA256 `f266b9e3fdcacfac736dd01e0a36a7391648ea2b159a2c291a2b8ca720b372b9`. RAG ACCEPTED, `corpus_generation_id=4f4904c70b519f263a84555223687e90bc171b99d2d5c3024d484c19f11da5ac`, `index_generation_id=b1355d2d8ea929ec484e1980dfdf932f922e2a65f9ce2a761c97e85b47bdc7d7`. Чтение только RAG (без PDF fallback, веба и модельной памяти); шаблон chapter-artifact-collection v1.7.

## Основная идея

От диагностики интерфейсов, маршрутизации, DNS и трафика автор переходит к запуску сетевых служб и проверке прикладных протоколов. Для службы приводится схема **установка → конфигурация → запуск через systemd → проверка статуса → при необходимости автозапуск**, затем контроль реальной сетевой доступности; брандмауэр и клиенты требуют самостоятельной проверки. Основание: [PDF 62](../../../rag/chunks/p0001-p0100/p0062-c01.md), [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md), [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md).

## Карта части II

| Тема | Печатные страницы | RAG |
|---|---:|---|
| Наблюдение: ping, traceroute, netstat, DNS, tcpdump, Wireshark | 61–66 | [PDF 64](../../../rag/chunks/p0001-p0100/p0064-c01.md), [PDF 65](../../../rag/chunks/p0001-p0100/p0065-c01.md), [PDF 66](../../../rag/chunks/p0001-p0100/p0066-c01.md), [PDF 67](../../../rag/chunks/p0001-p0100/p0067-c01.md) |
| Тестирование: sftp, scp, Netcat и различия реализаций | 67–69 | [PDF 68](../../../rag/chunks/p0001-p0100/p0068-c01.md), [PDF 69](../../../rag/chunks/p0001-p0100/p0069-c01.md), [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md) |
| Принципы запуска сетевых служб и systemd | 69–70 | [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md), [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md) |
| SSH: удалённые команды, файлы, mc, графические сеансы, скрипты | 70–80 | [PDF 72](../../../rag/chunks/p0001-p0100/p0072-c01.md), [PDF 74](../../../rag/chunks/p0001-p0100/p0074-c01.md), [PDF 75](../../../rag/chunks/p0001-p0100/p0075-c01.md), [PDF 76](../../../rag/chunks/p0001-p0100/p0076-c01.md), [PDF 80](../../../rag/chunks/p0001-p0100/p0080-c01.md), [PDF 82](../../../rag/chunks/p0001-p0100/p0082-c01.md) |
| DHCP: адресные пулы, аренда, isc-dhcp-server | 81–85 | [PDF 83](../../../rag/chunks/p0001-p0100/p0083-c01.md), [PDF 84](../../../rag/chunks/p0001-p0100/p0084-c01.md), [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md), [PDF 86](../../../rag/chunks/p0001-p0100/p0086-c01.md) |
| DNS: bind, dnsmasq, systemd-resolved, выбор серверов | 85–99 | [PDF 87](../../../rag/chunks/p0001-p0100/p0087-c01.md), [PDF 88](../../../rag/chunks/p0001-p0100/p0088-c01.md), [PDF 91](../../../rag/chunks/p0001-p0100/p0091-c01.md), [PDF 94](../../../rag/chunks/p0001-p0100/p0094-c01.md), [PDF 97](../../../rag/chunks/p0001-p0100/p0097-c01.md), [PDF 99](../../../rag/chunks/p0001-p0100/p0099-c01.md) |
| Брандмауэр: netfilter, iptables, ufw | 100–106 | [PDF 101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 103](../../../rag/chunks/p0101-p0200/p0103-c01.md), [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md), [PDF 106](../../../rag/chunks/p0101-p0200/p0106-c01.md) |
| inetd/xinetd, telnet, systemd socket activation | 107–117 | [PDF 108](../../../rag/chunks/p0101-p0200/p0108-c01.md), [PDF 109](../../../rag/chunks/p0101-p0200/p0109-c01.md), [PDF 111](../../../rag/chunks/p0101-p0200/p0111-c01.md), [PDF 113](../../../rag/chunks/p0101-p0200/p0113-c01.md), [PDF 115](../../../rag/chunks/p0101-p0200/p0115-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md) |
| Прокси: SOCKS/Dante, SSH-туннели, socksify и sockstat | 118–129 | [PDF 119](../../../rag/chunks/p0101-p0200/p0119-c01.md), [PDF 121](../../../rag/chunks/p0101-p0200/p0121-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md), [PDF 126](../../../rag/chunks/p0101-p0200/p0126-c01.md), [PDF 128](../../../rag/chunks/p0101-p0200/p0128-c01.md), [PDF 129](../../../rag/chunks/p0101-p0200/p0129-c01.md), [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md) |
| Заключение и список источников | 129–130 | [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md), [PDF 131](../../../rag/chunks/p0101-p0200/p0131-c01.md) |

## Артефакты

- [Операционная шпаргалка](cheatsheet.md)
- [Классифицированные команды](commands.md)
- [Mermaid-схемы](diagram.md)
- [Компактная SVG-шпаргалка](visual-cheatsheet.svg)
- [Подробная SVG-шпаргалка](visual-cheatsheet-detailed.svg)
- [Расхождения первоисточника](source-findings.md)

## Условия и ограничения

Отдельного издательского итогового summary либо блока контрольных вопросов в конце части II нет: conditional `summary.md`, `review-questions.md`, `review-answers.md` не создаются. Изображения 2.1–2.17 (скриншоты, GUI, схема прокси) не представлены в RAG в виде изображений; созданные SVG основаны только на тексте.

Исторические демонстрации установки сервисов, брандмауэра, открытого SOCKS и изменения DNS **не являются готовой безопасной конфигурацией**. Без дополнительных измерений текущего хоста их результаты [Needs confirmation]. Разногласия сохранены в [source-findings.md](source-findings.md). Прогресс чтения не меняется.
