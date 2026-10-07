# Cheatsheet — глава 6: service enumeration

## Symptom / problem framing

Port scan показывает, где слушает сервис; enumeration пытается понять, что сервис раскрывает: software/version, RPC registrations, SMB shares/users, SNMP MIB data, SMTP behavior и web/CMS metadata. `p0140:c01`, `p0168:c01`.

## Baseline / context

| Протокол | Что подтверждено source |
| --- | --- |
| RPC/RMI | registered programs, registry/object metadata, dynamic ports |
| SMB/NetBIOS | host/workgroup/version, shares/users depending on access |
| SNMP | system/kernel/contact/interface data via MIB/OID |
| SMTP | banner/capabilities and possible address/user behavior |
| Web/CMS | directories, versions, themes/plugins/users |

## Read-only checks

1. Подтверждены ли host/service/port из разрешённого scope? [Needs confirmation].
2. Есть ли разрешение именно на application enumeration? [Needs confirmation].
3. Определены ли rate и допустимые protocol-specific probes? [Needs confirmation].
4. Может ли auth-related probing вызвать lockout/MFA/alerts? [Needs confirmation].
5. Есть ли approved credentials, если source technique требует authentication? [Needs confirmation].
6. Как хранить sensitive usernames/shares/contact data? [Needs confirmation].

## Interpretation

- Service/version result не гарантирует реальную patch state.
- RPC/RMI registration не доказывает exploitable vulnerability.
- SMB enumeration зависит от auth/version/policy; отсутствие ответа не доказывает отсутствия share/user.
- SNMP response может раскрыть infrastructure metadata; source example community string — историческая demonstration.
- SMTP responses зависят от implementation/configuration.
- Web scanners делают HTTP requests; отдельная “passive detection” внутри tool output не делает весь scan пассивным.

## Next action

Для разрешённой оценки: **known service → минимально необходимая protocol-specific enumeration → evidence → validation → defensive recommendation**. Credential testing и exploit validation требуют отдельного scope.

## Modifying action

Основная enumeration не меняет configuration target, но создаёт workload; auth attempts могут вызвать lockout/rate-limit/alerts. SNMP write capability упоминается как свойство протокола, но state-changing management operations здесь не предлагаются.

## Verification / acceptance checks

- Evidence содержит timestamp, target/service/port, tool/mode и scope.
- Enumeration output не объявляется vulnerability без отдельного доказательства.
- Sensitive identity/share/contact data минимизированы.
- Нет lockout/availability degradation: фактическая проверка [Needs confirmation].
- Defensive recommendation привязана к конкретному protocol exposure.

## Rollback

**[Needs confirmation].** Уже сделанные запросы нельзя отменить; recovery after lockout/rate-limit/service impact зависит от среды. Universal rollback в source отсутствует.
