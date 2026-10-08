# Mermaid — глава 29. Authentication, Authorization, Access Control

PDF pp. 925–954; RAG p0925:c01–p0954:c01; **rag_only**. Схемы концептуальные, не экспорт рисунков 29.1–29.16. Ниже нет рабочих команд или сертификатов.

## Факторы и решение о доступе

~~~mermaid
flowchart TD
  USER["Пользователь / процесс"] --> ID["Identification: заявленный ID"]
  ID --> FACTOR{"Authenticator"}
  FACTOR --> K["Knowledge: пароль / секрет"]
  FACTOR --> P["Possession: аппаратный ключ"]
  FACTOR --> B["Inherence: биометрия"]
  K --> VERIFY["Verifier: проверка подлинности"]
  P --> VERIFY
  B --> VERIFY
  VERIFY --> POLICY["Authorization: subject + object + operation"]
  POLICY --> DEC{"Access decision"}
  DEC -->|Allow| RESOURCE["Ресурс"]
  DEC -->|Deny| BLOCK["Отказ"]
~~~

[p0925](../../../rag/chunks/p0901-p1000/p0925-c01.md)–[p0926](../../../rag/chunks/p0901-p1000/p0926-c01.md), [p0943](../../../rag/chunks/p0901-p1000/p0943-c01.md). Наличие двух этапов с knowledge не делает их двумя независимыми факторами.

## Challenge-response / OTP

~~~mermaid
sequenceDiagram
  participant C as Клиент / токен
  participant S as Аутентификатор
  C->>S: Идентификатор / запрос
  S-->>C: Новый Challenge / ID
  Note over C: Формирование ответа по секрету и challenge
  C->>S: Response
  Note over S: Независимая проверка по сохранённому контексту
  alt Ответ подтверждён
    S-->>C: Success
  else Проверка не прошла
    S-->>C: Failure
  end
~~~

[p0929](../../../rag/chunks/p0901-p1000/p0929-c01.md)–[p0931](../../../rag/chunks/p0901-p1000/p0931-c01.md). PPP CHAP и SAM — **два отдельных примера**, схема показывает только общий принцип; не спецификация криптографических полей. Time-based OTP использует общий секрет и время [p0932](../../../rag/chunks/p0901-p1000/p0932-c01.md)–[p0933](../../../rag/chunks/p0901-p1000/p0933-c01.md).

## Цифровая подпись и сертификат

~~~mermaid
flowchart LR
  DOC["Документ / код"] --> HASH["Digest"]
  HASH --> SIGN["Signature по private key владельца"]
  SIGN --> RECEIVE["Данные + подпись"]
  CA["CA: подписанный сертификат"] --> CERT["Identity ↔ public key"]
  CERT --> CHECK["Trust/validity check"]
  RECEIVE --> VERIFY["Проверка подписи public key"]
  CHECK --> VERIFY
  VERIFY --> RESULT["Подтверждение подлинности и целостности при заданных предпосылках"]
~~~

[p0934](../../../rag/chunks/p0901-p1000/p0934-c01.md)–[p0941](../../../rag/chunks/p0901-p1000/p0941-c01.md). Подпись ≠ шифрование. В RAG нет полной реализации проверки X.509 и форматирования RSA.

## Access matrix, DAC, MAC, RBAC

~~~mermaid
flowchart TD
  MAT["Access matrix: subjects × objects × operations"] --> OBJ["Object view: ACL"]
  MAT --> SUB["Subject view: capability list"]
  OBJ --> DAC["DAC: владелец назначает права"]
  MAT --> MAC["MAC: central labels / classification + categories"]
  MAT --> RBAC["RBAC: roles bind permissions"]
  RBAC --> ASSIGN["Users assigned roles"]
  DAC --> ENFORCE["Access-control decision"]
  MAC --> ENFORCE
  ASSIGN --> ENFORCE
~~~

[p0943](../../../rag/chunks/p0901-p1000/p0943-c01.md)–[p0952](../../../rag/chunks/p0901-p1000/p0952-c01.md). В source rule MAC требуется совпадение хотя бы одной категории; **это не универсальная политика для всех MAC**.

## Single Sign-On (SSO)

~~~mermaid
sequenceDiagram
  participant U as Пользователь
  participant I as Identity Provider
  participant S as Service Provider
  U->>I: Первичный запрос и аутентификатор
  I-->>U: Токен после успешной проверки
  U->>S: Запрос сервиса с токеном
  Note over S: Проверить trusted issuer и статус токена
  S-->>U: Сервис при выполнении правил доступа
  Note over U,I: Обновление при завершении срока действия
~~~

[p0953](../../../rag/chunks/p0901-p1000/p0953-c01.md)–[p0954](../../../rag/chunks/p0901-p1000/p0954-c01.md). Kerberos упомянут как пример, без wire-level сценария. Действительные правила, clock skew, audience и revocation требуют source вне rag_only — **[Needs confirmation]**.

## Operational boundary

Реальные IdP, CA, SSO, сертификаты/ключи и access policy не изучались и не менялись. Diagram ≠ deployment. Контроль изменений и rollback: **[Needs confirmation]**.
