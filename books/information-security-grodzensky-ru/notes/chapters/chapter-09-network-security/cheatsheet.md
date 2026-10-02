# Шпаргалка: безопасность компьютерных сетей

Цель: определить роль каждого класса сетевой защиты и не смешивать mediation, filtering, detection и access control.

## Baseline / context

### Proxy / SWG

Функция: посредник между пользователем и внешним/внутренним ресурсом.

В главе названы:
- direct proxy;
- reverse proxy;
- transparent proxy;
- SOCKS proxy;
- DNS proxy;
- web proxy;
- Secure Web Gateway.

### Firewall

Функция: фильтрация трафика по правилам.

Эволюция по книге:
```text
L2 switching
   ↓
packet filtering
   ↓
session gateways
   ↓
stateful inspection
   ↓
NGFW / application-aware control
```

## Современная парадигма главы

Недостаточно решения на основе:

`IP + port + protocol`

Нужно учитывать:

`application + user + content + risk + encrypted traffic`

## NGFW

Названные возможности:
- application-level traffic analysis;
- virus scanning;
- IDS/IPS;
- botnet blocking;
- VPN/GOST VPN;
- mobile support;
- URL filtering;
- directory integration;
- data-leak related functions.

## Anti-APT / sandbox

```text
unknown object
   ↓
pre-analysis
   ↓
sandbox
   ↓
behavior observed
   ├─ benign → deliver
   └─ malicious → block
```

Критерии sandbox из главы:
- поддерживаемые ОС;
- encrypted traffic;
- YARA scanning;
- поддерживаемые file formats;
- SIEM integration.

## NAC

NAC:
- видит подключающиеся устройства;
- классифицирует их;
- проверяет соответствие политике;
- разрешает/ограничивает доступ;
- интегрируется с другими СЗИ.

Примеры:
- EDR обнаружил compromise → NAC изолирует workstation;
- неизвестный host → quarantine → vulnerability scan → access decision;
- mobile device → проверка EMM agent.

## Read-only checks

1. Где выполняется mediation: proxy/SWG?
2. Где выполняется packet/application filtering?
3. Анализируется ли SSL traffic?
4. Есть ли IDS/IPS capability?
5. Есть ли отдельный путь обработки unknown traffic?
6. Интегрирована ли sandbox с SIEM/NGFW?
7. Есть ли NAC enforcement для unmanaged/unknown devices?
8. Может ли EDR инициировать изоляцию endpoint через NAC?
9. Есть ли политики для mobile devices?
10. Есть ли контроль rogue Wi-Fi access points?

## Next action

```text
inventory network controls
→ map control to role
→ find visibility gaps
→ inspect unknown/encrypted traffic
→ enforce device posture
→ integrate detections and response
```

## Modifying action

Изменения, поддержанные главой:
- firewall policy;
- proxy/SWG policy;
- URL filtering;
- SSL traffic inspection;
- IDS/IPS enablement;
- VPN remote access;
- sandbox integration;
- NAC quarantine/isolation;
- EMM enforcement;
- rogue Wi-Fi suppression.

Vendor-specific implementation: `[Needs confirmation]`.

## Verification / acceptance checks

- policy действительно блокирует/разрешает ожидаемый трафик;
- unknown objects проходят соответствующий analysis path;
- malicious object не доставляется получателю в sandbox-сценарии;
- non-compliant host получает ограничение/карантин;
- события передаются в интегрированные средства мониторинга;
- включённые security modules не делают фактическую производительность неприемлемой.

Конкретные команды проверки: `[Not applicable]`.

## Rollback

Конкретные rollback-процедуры в главе отсутствуют.

Rollback: `[Needs confirmation]`.
