# Шпаргалка: защита информации ограниченного доступа

Цель: связать классификацию информации, доступ, DLP, DAG и организационный режим.

## Baseline

```text
restricted information
      ↓
classification / value
      ↓
access rules
      ↓
DLP + DAG + labels
      ↓
monitor / detect / block
      ↓
audit / correction
```

## DLP

### Что контролирует

- email;
- web;
- messengers;
- removable media;
- printing;
- endpoint channels;
- network traffic.

### Архитектуры из главы

- gateway/network DLP;
- host/endpoint DLP.

### Режимы

- detection;
- blocking.

Blocking требует точной настройки правил: false positives могут нарушить работу организации.

## DAG

Data Access Governance в главе:
- автоматизирует согласование доступа;
- ведёт continuous audit;
- показывает, кто имеет доступ к файлам;
- анализирует critical/sensitive data;
- сигнализирует о неуместном доступе;
- автоматизирует выдачу прав;
- анализирует изменения прав в Active Directory.

## Security labels

Относятся к мандатной модели доступа.

Метка может определять:
- read-only;
- read + edit;
- запрет/разрешение внешней передачи.

## Организационные меры

- security awareness;
- NDA;
- classification;
- valuation;
- risk assessment;
- access regulations;
- incident/leak procedures.

## Read-only checks

1. Какие данные относятся к restricted/confidential?
2. Есть ли классификатор?
3. Кто владелец данных?
4. Кто имеет доступ?
5. Какие каналы утечки контролирует DLP?
6. Где требуется endpoint agent?
7. Какие правила работают только как alert, а какие блокируют?
8. Каков false-positive rate blocking rules?
9. Ведётся ли continuous audit прав и действий?
10. Анализируются ли права Active Directory?
11. Используются ли labels?
12. Есть ли formal commercial-secret regime?

## Next action

```text
inventory data
→ classify
→ map owners/access
→ deploy/verify DLP coverage
→ deploy/verify DAG visibility
→ tune rules
→ formalize organizational regime
```

## Modifying action

Из главы:
- включение DLP-agent;
- настройка gateway interception;
- blocking rules;
- DAG access workflows;
- security labels;
- корректировка ACL/rights;
- NDA/organizational documents;
- режим коммерческой тайны.

Vendor-specific implementation: `[Needs confirmation]`.

## Verification

- DLP видит требуемые каналы;
- DAG показывает фактические права;
- classification обнаруживает sensitive data;
- blocking rules не создают неприемлемых false positives;
- access workflows работают по регламенту;
- commercial-secret documents и процедуры формализованы.

Quantitative thresholds: `[Needs confirmation]`.

## Rollback

Конкретный rollback blocking rules/access changes в главе не задан.

Rollback: `[Needs confirmation]`.
