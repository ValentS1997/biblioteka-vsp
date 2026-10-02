# Шпаргалка: безопасность мобильных устройств

Цель: связать ownership model, корпоративную политику и EMM-контроли.

## Ownership models

| Модель | Смысл по главе |
|---|---|
| BYOD | Личное устройство сотрудника, используемое под корпоративной политикой |
| COPE | Корпоративное устройство, предоставленное сотруднику |

## Основные задачи EMM

1. Отделить корпоративные данные от личных.
2. Управлять правами и функциями устройства.
3. Защитить передачу данных.

## Data-at-rest

Источник связывает защиту с криптоконтейнером:

```text
device
├─ personal space
└─ corporate crypto-container
   ├─ encrypted data
   └─ password / PIN / biometrics
```

## Data-in-transit

- VPN module;
- proxy/gateway;
- policy server integration.

## Основные EMM-модули

- proxy server;
- app store;
- secure mail client;
- secure file manager;
- secure browser;
- VPN client.

## Threat → control mapping

| Угроза | Контроль из главы |
|---|---|
| Потеря устройства | crypto-container, remote wipe / anti-theft |
| Malware/ransomware | app policy, mobile AV, containerization |
| Phishing | content/reputation-based protection |
| Jailbreak | detect → notify → restrict |
| Botnet participation | application-download restrictions |
| NFC-related risk | policy control for NFC/Wi-Fi/Bluetooth |
| Corporate data leakage | mail/proxy restrictions, EMM policies |

## Read-only checks

1. Устройство BYOD или COPE?
2. Есть ли formal policy/enrollment?
3. Отделены ли corporate и personal data?
4. Используется ли crypto-container?
5. Защищён ли канал передачи через VPN/policy gateway?
6. Контролируется ли app installation?
7. Детектируется ли jailbreak?
8. Есть ли phishing protection?
9. Есть ли remote response при потере устройства?
10. Контролируются ли Wi-Fi/Bluetooth/NFC?
11. Используются ли certificate auth/SSO?
12. Политика зависит от контекста подключения?

## Next action

```text
classify ownership
→ enroll device
→ apply policy
→ isolate corporate data
→ protect network traffic
→ monitor posture
→ restrict / wipe / recover on incident
```

## Modifying action

Изменения, поддержанные главой:
- EMM enrollment;
- применение crypto-container;
- установка mobile AV/VPN;
- ограничение функций устройства;
- управление приложениями;
- application wrapping;
- remote wipe;
- блокировка функций при jailbreak;
- policy-based Wi-Fi/Bluetooth/NFC controls.

Vendor-specific implementation: `[Needs confirmation]`.

## Verification / acceptance checks

- корпоративные данные отделены от личных;
- доступ к container требует авторизации;
- устройство соответствует policy;
- защищённый канал используется там, где это требуется моделью защиты;
- при jailbreak policy изменяет доступ согласно правилам;
- lost-device response способен удалить корпоративные данные в модели главы.

Конкретные CLI/API checks: `[Not applicable]`.

## Rollback

Универсальный rollback EMM-policy в главе не задан.

Rollback: `[Needs confirmation]`.
