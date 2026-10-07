# Cheatsheet — глава 6: service enumeration

## Symptom / problem framing

Port scan показывает **где** слушает сервис; enumeration пытается понять **что именно сервис раскрывает**: software/version, RPC programs, shares/users, MIB/OID, mail behavior, directories/CMS metadata. Чем ближе проверка к application/authentication layer, тем выше риск влияния и чувствительности данных. `p0140:c01`, `p0168:c01`.

## Baseline / context

| Протокол / слой | Что можно получить по source | RAG |
| --- | --- | --- |
| Service/version | banner/version/cipher/service info через nmap/NSE | `p0140:c01`–`p0143:c01` |
| RPC/rpcbind | registered programs, versions, protocol, dynamic ports | `p0143:c01`–`p0145:c01` |
| Java RMI | registry/object/service metadata; dynamic endpoint info | `p0145:c01`–`p0147:c01` |
| SMB/NetBIOS | host/workgroup/version, shares, users depending on access/auth | `p0148:c01`–`p0156:c01` |
| SNMP | system/kernel/contact/interface data from MIB/OID | `p0158:c01`–`p0159:c01` |
| SMTP | banner/capabilities and possible address/user behavior | `p0160:c01`–`p0162:c01` |
| Web/CMS | directories, server/CMS/version/theme/plugin/user metadata | `p0162:c01`–`p0167:c01` |

## Read-only checks

До активного enumeration проверить:
1. Подтверждены ли host/service/port из разрешённого scope? [Needs confirmation].
2. Есть ли разрешение именно на application enumeration, а не только port scan? [Needs confirmation].
3. Для SMB/SNMP/SMTP/web определены ли допустимые user/address/directory probes и rate? [Needs confirmation].
4. Не будет ли username/password testing вызывать lockout/MFA/alerts? [Needs confirmation].
5. Есть ли approved credentials для authenticated enumeration, если они нужны? `p0151:c01`–`p0154:c01`.
6. Какие данные считаются чувствительными и как их сохранять в evidence? `p0158:c01`–`p0159:c01`.
7. Есть ли baseline сервисов и owner contact на случай impact? [Needs confirmation].

## Interpretation

- **Service/version result** — это заявленная/выведенная информация, а не гарантия истинной patch state. `p0141:c01`–`p0142:c01`.
- **RPC/RMI registration** показывает exposed program/object mapping, но сам по себе не доказывает exploitable vulnerability. `p0143:c01`–`p0147:c01`.
- **SMB shares/users** зависят от auth, protocol version и policy. Неуспешная enumeration не доказывает отсутствие share/user. `p0151:c01`–`p0156:c01`.
- **SNMP community-based response** может раскрывать infrastructure metadata; source example `public` — историческая demonstration, не current credential. `p0158:c01`–`p0159:c01`.
- **SMTP responses** могут различаться по implementation/configuration; user enumeration result требует осторожной трактовки. `p0160:c01`–`p0162:c01`.
- **WPScan/dirb** делают HTTP requests; «passive» labels внутри отдельных WPScan detections не означают, что весь scan не создаёт сетевой трафик. `p0163:c01`–`p0167:c01`.

## Next action

Для разрешённой оценки двигаться по цепочке **known service → минимально необходимая protocol-specific enumeration → evidence → validation → defensive recommendation**. User/password brute force, credential reuse testing и exploit validation требуют отдельного разрешения и не являются автоматическим продолжением enumeration. `p0140:c01`, `p0168:c01`–`p0168:c02`.

## Modifying action

Основная часть enumeration не меняет конфигурацию target, но **генерирует workload и может менять account/security state косвенно**: login attempts могут вызывать lockout, rate limits и alerts; web directory brute enumeration создаёт множество запросов. SNMP write access в source обсуждается как возможность протокола, но chapter artifacts не выполняют и не предлагают SET/config changes. `p0154:c01`, `p0158:c01`, `p0163:c01`–`p0165:c01`.

## Verification / acceptance checks

- Raw evidence содержит timestamp, target/service/port, tool/mode и scope.
- Enumeration result не трактуется как vulnerability без отдельного доказательства.
- Sensitive usernames/shares/contact data не публикуются без необходимости.
- Не было account lockout/availability degradation; фактическая проверка **[Needs confirmation]**.
- Defensive recommendations сопоставлены с конкретным протоколом: SMB restrictions, SNMPv3/auth/encryption/firewall, SMTP information reduction, web access-control/directory-listing controls.
- Any credential testing is separately authorized and documented; иначе **not performed**.

## Rollback

**[Needs confirmation].** Enumeration requests нельзя «отменить»; если вызваны lockout/rate-limit/service degradation, recovery depends on the environment. Source не предоставляет универсальной процедуры account unlock/service recovery. Owner, access path and rollback conditions должны быть определены до risky enumeration.
