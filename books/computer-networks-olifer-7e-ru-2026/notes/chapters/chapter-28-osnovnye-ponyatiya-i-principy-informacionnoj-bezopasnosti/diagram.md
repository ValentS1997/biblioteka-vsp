# Диаграммы — глава 28. Информационная безопасность

RAG `p0892:c01–p0924:c01`, PDF 892–924; **rag_only**. Схемы по тексту, а не реконструкции рисунков 28.1–28.11. Не демонстрируют живую security posture.

## Контроль доступа: идентификация, аутентификация, авторизация

~~~mermaid
flowchart TD
  S["Субъект: пользователь / процесс"] --> I["Identification: заявленная identity"]
  I --> A["Authentication: подтверждение подлинности"]
  A --> POLICY["Authorization: правила subject / object / operation"]
  POLICY --> DEC{"Доступ к объекту разрешён?"}
  DEC -->|Да| OP["Разрешённая операция"]
  DEC -->|Нет| DENY["Отклонить операцию"]
  OBJECT["Объект: файл / сервис / устройство"] --> POLICY
~~~

[p0892](../../../rag/chunks/p0801-p0900/p0892-c01.md)–[p0895](../../../rag/chunks/p0801-p0900/p0895-c01.md). Authentication не влечёт автоматически любое authorization.

## Модели безопасности и risk management

~~~mermaid
flowchart TD
  CIA["CIA / КЦД: confidentiality, integrity, availability"] --> MODEL["Security requirements системы"]
  PH["Parkerian Hexad: authenticity, possession, utility + CIA"] --> MODEL
  MODEL --> ASSET["Активы и сервисы"]
  ASSET --> V["Уязвимости"]
  ASSET --> TH["Угрозы"]
  V --> RISK["Оценка: ущерб + вероятность"]
  TH --> RISK
  RISK --> DEC{"Risk response"}
  DEC --> ACCEPT["Принятие"]
  DEC --> ELIM["Устранение"]
  DEC --> REDUCE["Снижение"]
  DEC --> TRANS["Перенаправление"]
~~~

[p0895](../../../rag/chunks/p0801-p0900/p0895-c01.md)–[p0902](../../../rag/chunks/p0901-p1000/p0902-c01.md). Никакие бизнес-оценки и вероятности конкретной организации не вычислены.

## Иерархия и непрерывный цикл защиты

~~~mermaid
flowchart TD
  TOP["Руководство: top-down решения и бюджет"] --> LEG["Legislative: правовые нормы и стандарты"]
  LEG --> ADM["Administrative: политика и ответственность"]
  ADM --> PROC["Procedural: people, backup, operations"]
  PROC --> TECH["Technical: access controls, firewall/IDS/crypto"]
  TECH --> OBS["Audit / контроль исполнения"]
  OBS --> NEW["Новые угрозы и уязвимости"]
  NEW --> TOP
  WEAK["Weakest link + balanced defense"] -.-> TECH
  LAYER["Defense in depth"] -.-> PROC
~~~

[p0907](../../../rag/chunks/p0901-p1000/p0907-c01.md)–[p0913](../../../rag/chunks/p0901-p1000/p0913-c01.md). Модель не заменяет назначенную policy или контроль её реализации.

## Схемы криптографических задач

~~~mermaid
flowchart TD
  GOAL["Криптографическая задача"] --> SYM["Confidentiality: symmetric encryption"]
  GOAL --> DH["Agreement: Diffie–Hellman"]
  GOAL --> PUB["Public-key encryption: RSA (пример)"]
  GOAL --> HASH["Integrity: keyed H(X,K)"]
  SYM --> K["Общий secret key нужен обеим сторонам"]
  DH --> SHARED["Каждая сторона вычисляет общий secret"]
  PUB --> PAIR["Open key + private key"]
  PAIR --> CERT["Защита от подмены public key / сертификат"]
  HASH --> COMP["Получатель сверяет digest"]
  SHARED -.-> K
~~~

[p0913](../../../rag/chunks/p0901-p1000/p0913-c01.md)–[p0924](../../../rag/chunks/p0901-p1000/p0924-c01.md). **Важно:** игрушечные параметры DH/RSA, `x mod n`, DES/3DES и MD2/MD4/MD5 **не являются** безопасным production recipe. Алгоритмы и схемы не подтверждены современными спецификациями в режиме rag_only.

## Operational boundary

Никаких сканирований, cryptographic-key generation, тестов attack, изменения политик, шлюзов и ролей не проводилось. Access, compliance, tests и rollback: **[Needs confirmation]**.
