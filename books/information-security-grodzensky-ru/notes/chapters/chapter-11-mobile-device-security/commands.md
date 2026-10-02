# Средства и механизмы главы 11

Shell-команд в главе нет. Ниже — только технологии и контроли, явно названные в RAG.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| EMM | Управление корпоративной мобильностью | stateful/control | Policy, container, apps, network controls | Device policy state | [Needs confirmation] |
| Crypto-container | Разделение и шифрование corporate data | state-changing | Отделяет corporate data от personal data | Authorized access only | [Needs confirmation] |
| Mobile AV | Защита от malware | monitor/prevent | Детектирует/предотвращает вредоносное ПО | Security event/status | [Needs confirmation] |
| VPN client | Защищённая передача | stateful/network | Защищает mobile-to-corporate traffic | Tunnel/policy status | [Needs confirmation] |
| EMM proxy | Traffic policy enforcement | stateful/network | Управляет/фильтрует mobile traffic | Policy result | [Needs confirmation] |
| Secure mail client | Защищённая корпоративная почта | stateful/application | Контролирует почтовый доступ | Policy state | [Needs confirmation] |
| Secure file manager | Контролируемый доступ к файлам | stateful/application | Управляет file access | Access-policy result | [Needs confirmation] |
| Secure browser | Контролируемый доступ к internal resources | stateful/application | Применяет corporate browsing policy | Access-policy result | [Needs confirmation] |
| App wrapping | Containerization/policy for third-party apps | state-changing | Применяет настройки/шифрование к приложению | Wrapped-app policy state | [Needs confirmation] |
| Jailbreak detection | Posture control | monitor/enforce | Выявляет попытку повышения привилегий | Alert / restriction state | [Not applicable] |
| Anti-theft | Lost-device response | response | Удаление данных / device restrictions | Response status | [Needs confirmation] |
| Certificate auth / SSO | Аутентификация | stateful/auth | Централизует/усиливает вход | Authentication result | [Needs confirmation] |

## Policy controls из главы

- application installation source;
- permissions;
- geolocation permission;
- Wi-Fi;
- Bluetooth;
- NFC;
- access by user/group;
- context-dependent policy.

## Operational boundary

- MDM/UEM CLI/API syntax отсутствует.
- Remote-wipe execution steps не добавлялись.
- Current Android/iOS platform guidance не подмешивалась.
