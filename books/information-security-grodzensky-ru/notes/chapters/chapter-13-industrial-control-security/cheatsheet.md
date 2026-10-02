# Шпаргалка: защита АСУ ТП

## Архитектура

| Уровень | Типовые компоненты из главы | Основной защитный акцент |
|---|---|---|
| Верхний | MES, SCADA, ERP | сегментация, датадиод, monitoring |
| Средний | PLC | industrial firewall, protocol-aware filtering |
| Нижний | датчики, исполнительные механизмы | физическая и логическая изоляция |

## Основные угрозы

- эксплуатация уязвимостей;
- вредоносное ПО;
- сетевые атаки;
- закладки в ПО/оборудовании.

## Особенность vulnerability management

В АСУ ТП:
- активное сканирование может влиять на технологический процесс;
- patching может быть отложен;
- firmware fix может отсутствовать;
- passive sniffing может использоваться для inventory/version analysis.

## Приказ №31 — логика главы

```text
classify ASU
→ identify threats
→ build threat model
→ define protection requirements
→ implement organizational + technical controls
```

## Уровень значимости и класс

```text
УЗ1 → К1
УЗ2 → К2
УЗ3 → К3
```

УЗ связан с возможным ущербом при нарушении:
- конфиденциальности;
- целостности;
- доступности.

## Read-only checks

1. Какие технологические уровни присутствуют?
2. Какие assets относятся к верхнему/среднему/нижнему уровню?
3. Возможен ли active scan без operational risk?
4. Есть ли passive network visibility?
5. Отделена ли АСУ ТП от corporate network?
6. Есть ли one-way communication там, где требуется архитектурой?
7. Понимает ли firewall industrial protocols?
8. Есть ли inventory сетевых активов?
9. Есть ли monitoring неавторизованного управления?
10. Определены ли УЗ и класс защищённости?
11. Есть ли threat model?
12. Меры соответствуют классу/угрозам?

## Next action

```text
inventory
→ classify
→ threat model
→ choose safe assessment method
→ segment
→ deploy controls per level
→ monitor
→ investigate
```

## Verification / acceptance

- security checks не нарушают normal operation;
- corporate и industrial networks разделены согласно архитектуре;
- middle-level controls видят industrial protocols;
- monitoring выявляет unauthorized control attempts;
- класс защищённости сопоставлен с УЗ;
- набор мер соответствует модели угроз.

## Rollback

Конкретный rollback для industrial controls в главе не задан.

Rollback: `[Needs confirmation]`.
