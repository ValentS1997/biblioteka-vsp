# Средства и механизмы главы 12

Shell-команд в главе нет.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| DLP gateway | Контроль сетевых каналов | monitor/block | Анализирует передачу sensitive data на периметре | Events / blocked transfer | [Needs confirmation] |
| DLP endpoint agent | Контроль локальных каналов | monitor/block | Контролирует print, removable media, local apps и др. | Endpoint events | [Needs confirmation] |
| iCap integration | Интеграция DLP с proxy | integration | Передаёт traffic/content на анализ в описанной модели | Integration events | [Needs confirmation] |
| UEBA | Поведенческий контекст | analysis | Выявляет аномалии по контексту пользователя/сущности | Behavioral alerts | [Not applicable] |
| DAG | Governance неструктурированных данных | analysis/control | Audit rights/actions + access workflow | Rights/action reports | [Needs confirmation] |
| Classifier | Классификация содержимого | analysis | Определяет тип чувствительной информации | Classification result | [Not applicable] |
| Security label | Мандатный контроль | state-changing | Связывает label с разрешёнными действиями | Policy result | [Needs confirmation] |
| IT audit tooling | Аудит ИТ/доступа | read-only | Используется как часть технических мер | Audit findings | [Not applicable] |
| Active Directory integration | Анализ прав | reference/control | DAG отслеживает изменения прав | Rights-change visibility | [Needs confirmation] |

## DLP coverage из источника

- email;
- web;
- messengers;
- removable media;
- printing;
- encrypted traffic via endpoint agent.

## DLP dimensions

```text
placement:
├─ gateway
└─ host

enforcement:
├─ detect
└─ block
```

## DAG capabilities

- continuous audit;
- file-access analysis;
- sensitive-data discovery;
- access-request automation;
- AD rights-change analysis.

## Operational boundary

- CLI/API syntax отсутствует.
- Blocking rules не приводятся.
- Insider-investigation procedures не добавлялись.
