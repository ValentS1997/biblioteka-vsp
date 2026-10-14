# Глава 10: схемы работы экспортеров (Mermaid)

**Источник:** PDF 187–208, RAG `p0187:c01`–`p0208:c01`. Все схемы выведены из текста, а не из изображений оригинала.

## Стандартный exporter и внешняя проба

```mermaid
flowchart LR
  APP["Приложение / Consul / MySQL"]
  EXP["Экспортер рядом с экземпляром<br/>:9107 или :9104"]
  PROM["Prometheus<br/>/metrics pull"]
  SITE["Внешняя цель<br/>HTTP / TCP / DNS / ICMP"]
  BLACK["Blackbox Exporter :9115<br/>/probe?module=..."]
  APP -->|"сбор внутренних данных"| EXP
  PROM -->|"scrape"| EXP
  PROM -->|"scrape /probe"| BLACK
  BLACK -->|"сетевой probe"| SITE
```

PDF 187–194, 205–207. Внешняя проба создаёт сетевое взаимодействие: `up` описывает доступность Blackbox, `probe_success` — результата зонда.

## Диагностика доступности

```mermaid
flowchart TD
  A["Prometheus: up"]
  B{"up == 1?"}
  C["Недоступен exporter / его endpoint<br/>[Needs confirmation]"]
  D["Смотреть consul_up / mysql_up / probe_success"]
  E{"Результат == 1?"}
  F["Исходная цель отвечает<br/>по условиям конкретного теста"]
  G["Смотреть DNS, IP, порты, debug,<br/>probe_http_* и duration"]
  A --> B
  B -->|"нет"| C
  B -->|"да"| D
  D --> E
  E -->|"да"| F
  E -->|"нет"| G
```

PDF 188–190, 195–203, 206. Это диагностический flow из главы, а не готовая alert rule.

## Multitarget — как разделить исходную цель и exporter

```mermaid
flowchart LR
  SD["static_configs или service discovery<br/>URL сайта или IP:порт"]
  P["__param_target<br/>параметр запроса /probe"]
  I["instance<br/>имя проверяемой цели"]
  A["__address__<br/>127.0.0.1:9115"]
  B["Blackbox<br/>module=http_2xx/ssh_banner"]
  T["Реальная удалённая цель"]
  SD --> P
  P --> I
  P --> A
  A --> B
  B --> T
```

PDF 205–207. Фактический порядок relabel — копировать первоначальный `__address__` в `__param_target`, затем `instance`, затем заменить `__address__`.

## Какая форма преобразования нужна

```mermaid
flowchart TD
  A["Данные приложения доступны напрямую?"]
  B{"Метрики встроены?"}
  C["Прямой scrape Prometheus"]
  D{"Есть API / данные сервиса?"}
  E["Consul/MySQLd exporter<br/>на экземпляр"]
  F{"Есть только журнал?"}
  G["Grok exporter<br/>regex → Counter/Histogram"]
  H["Удалённая проверка<br/>Blackbox ICMP/TCP/HTTP/DNS"]
  A --> B
  B -->|"да"| C
  B -->|"нет"| D
  D -->|"да"| E
  D -->|"нет"| F
  F -->|"да"| G
  F -->|"нет"| H
```

PDF 187–194. Последняя ветвь — **одна из обсуждаемых в источнике архитектур**, а не утверждение, что Blackbox покрывает любые форматы/цели.
