# Шпаргалка: оценка рисков ИБ

## Базовая модель

```text
asset
  +
vulnerability
  +
threat
  ↓
likelihood × impact
  ↓
risk
  ↓
treatment
  ↓
residual risk
```

## Инвентаризация

Для каждого информационного актива:
- ценность;
- жизненный цикл;
- связанные системы;
- оборудование;
- ПО;
- каналы связи;
- облачные сервисы.

## Качественная оценка

Пример шкал из главы:

- ущерб: низкий / средний / высокий;
- вероятность: вероятно / невероятно / крайне невероятно.

Результат — qualitative risk matrix.

## Количественная оценка

```text
SLE = Asset Value × Exposure Factor
ALE = SLE × ARO
```

Где:
- SLE — ущерб от одного события;
- ARO — среднегодовая частота;
- ALE — ожидаемый среднегодовой ущерб.

## Обработка риска

1. Снижение — уменьшить вероятность и/или ущерб.
2. Исключение — устранить сам сценарий возникновения риска.
3. Передача — страхование или договорная передача.
4. Принятие — оставить риск в текущем виде осознанно.

## Владение

Каждый риск должен иметь:
- owner;
- текущий уровень;
- treatment;
- residual risk;
- acceptance/risk appetite decision.

## Read-only checks

1. Реестр информационных активов есть?
2. Ценность определена?
3. Связанные ИТ-активы описаны?
4. Для риска есть threat/vulnerability scenario?
5. Назначен owner?
6. Определена probability?
7. Определён impact?
8. Есть qualitative/quantitative method?
9. Посчитан residual risk?
10. Есть treatment plan?
11. Risk appetite определён?
12. Есть risk register?

## Next action

```text
inventory
→ value assets
→ model threats
→ assess likelihood/impact
→ build risk register
→ choose treatment
→ reassess residual risk
```

## Verification

- каждый риск связан с активом;
- owner определён;
- оценка воспроизводима;
- treatment соответствует критичности;
- residual risk сравнивается с acceptance criteria;
- risk register актуализируется.

## Rollback

Для организационного risk-management process rollback не определён.

Rollback: `[Not applicable]`.
