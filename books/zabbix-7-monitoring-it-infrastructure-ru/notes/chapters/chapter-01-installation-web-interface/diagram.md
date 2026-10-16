# Глава 1 — диаграммы по RAG (Mermaid)

**Границы:** PDF 20–58; основание: [README](README.md). Диаграммы реконструируют **текстовые** связи, а не оригинальные рисунки 1.1–1.36.

## 1. Взаимодействие компонентов ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md), [p0030](../../../rag/chunks/p0001-p0100/p0030-c01.md))

```mermaid
flowchart LR
  UI["Пользователь → браузер"] --> WEB["NGINX + PHP frontend"]
  WEB --> DB[("MariaDB / MySQL")]
  SV["Zabbix server"] --> DB
  WEB -. "проверка состояния и функции интерфейса" .-> SV
  WEB --> CONFIG["Настройка хостов, шаблонов, панелей"]
```

Смысл: Zabbix server пишет значения и конфигурацию в БД, frontend взаимодействует с той же БД. Без правильно настроенного frontend нельзя удобно конфигурировать систему; сам запуск server этого не доказывает.

## 2. Начальная установка и проверка ([p0020](../../../rag/chunks/p0001-p0100/p0020-c01.md)–[p0030](../../../rag/chunks/p0001-p0100/p0030-c01.md))

```mermaid
flowchart TD
  A["Linux: Rocky 9 / Ubuntu 22.04"] --> B["Репозитории и MariaDB"]
  B --> C["Защищённая настройка БД"]
  C --> D["БД Zabbix, пользователь, права"]
  D --> E["Импорт SQL-схемы"]
  E --> F["zabbix_server.conf → DB параметры"]
  F --> G["Запуск Zabbix server"]
  G --> H{"status и log без ошибок?"}
  H -- "Нет" --> I["Проверить конфигурацию/журнал"]
  I --> F
  H -- "Да" --> J["NGINX/PHP, адрес и порт"]
  J --> K{"Frontend wizard: prerequisites OK и DB?"}
  K -- "Нет" --> L["Проверить конфигурацию NGINX, PHP, DB"]
  L --> J
  K -- "Да" --> M["Finish → вход → Global view"]
```

Здесь нет автоматического «восстановить всё»: конкретный rollback полного развертывания не задан источником.

## 3. Два независимых механизма HA ([p0031](../../../rag/chunks/p0001-p0100/p0031-c01.md)–[p0043](../../../rag/chunks/p0001-p0100/p0043-c01.md))

```mermaid
flowchart TD
  DB[("Единая MariaDB — single source of truth")]
  S1["Zabbix server HA1\nHANodeName + NodeAddress"]
  S2["Zabbix server HA2\nHANodeName + NodeAddress"]
  S1 --> DB
  S2 --> DB
  ST["Active/passive: только один активный server"] -.-> S1
  ST -.-> S2
  K1["keepalived + NGINX на HA1\nVRRP priority 244 (+10 при nginx)"]
  K2["keepalived + NGINX на HA2\nVRRP priority 243 (+10 при nginx)"]
  VIP["VIP: текущий frontend"]
  K1 --> VIP
  K2 --> VIP
  VIP --> DB
  DB --> RISK["Одиночная БД: ограничение HA"]
```

При отказе NGINX на HA1 его приоритет падает с 254 до 244, HA2 с работающим NGINX сохраняет 253 и получает VIP. Это механизм резервирования **frontend**, отдельный от active/passive Zabbix server. База данных одна.

## 4. Где найти нужные данные ([p0046](../../../rag/chunks/p0001-p0100/p0046-c01.md)–[p0058](../../../rag/chunks/p0001-p0100/p0058-c01.md))

```mermaid
flowchart TD
  NEED{"Задача администратора"}
  NEED -->|Проблемы / значения / хосты| MON["Monitoring → Problems, Hosts, Latest data"]
  NEED -->|Здоровье Zabbix / HA| REPORT["Reports → System information"]
  NEED -->|Хосты / шаблоны / discovery| DC["Data collection"]
  NEED -->|Оповещения| ALERT["Alerts → Actions, Media types"]
  NEED -->|Учётные записи| USERS["Users → Groups, Roles, Authentication"]
  NEED -->|Очередь / прокси / системные параметры| ADM["Administration"]
  NEED -->|SLA и сервисы| SVC["Services"]
  NEED -->|Данные инвентаризации| INV["Inventory"]
```

**RAG-политика:** никакие ветки схем не основаны на внешних предположениях. Неустранённые отличия команд: [source-findings.md](source-findings.md).
