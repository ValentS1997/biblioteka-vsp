# Шпаргалка: защита КИИ

## Рабочая последовательность

```text
organization
   ↓
is it a CII subject?
   ↓
inventory CII objects
   ↓
categorization
   ↓
threat modeling
   ↓
security measures
   ↓
incident reporting / operation
```

## КИИ по главе

КИИ включает:
- объекты КИИ;
- сети электросвязи, обеспечивающие их взаимодействие.

Объекты КИИ:
- информационные системы;
- информационно-телекоммуникационные сети;
- АСУ.

## Значимые и незначимые объекты

- значимый объект — получил одну из трёх категорий значимости;
- незначимый — категория значимости не присвоена.

Первая категория — наиболее высокая по потенциальному ущербу, третья — наиболее низкая.

## Критерии значимости

- социальные последствия;
- политические последствия;
- экономический ущерб;
- экологический ущерб;
- последствия для обороны, безопасности государства и правопорядка.

## Нормативная цепочка в состоянии источника

```text
187-ФЗ
├─ ПП РФ №127 → categorization
├─ ФСТЭК №235 → security system requirements
├─ ФСТЭК №236 → reporting form
└─ ФСТЭК №239 → protection measures
```

## Что инвентаризировать

- объект и назначение;
- субъект;
- архитектура;
- telecom interaction;
- operator;
- hardware/software;
- security controls;
- threats/attackers;
- incident consequences;
- category;
- organizational/technical controls.

## Read-only checks

1. Организация относится к субъектам КИИ по модели источника?
2. Составлен ли перечень объектов?
3. Для каждого объекта определено назначение и архитектура?
4. Зафиксированы сети связи и внешние взаимодействия?
5. Определены threats и attacker categories?
6. Оценены последствия инцидентов?
7. Выполнено categorization?
8. Зафиксирована категория или отсутствие необходимости её присвоения?
9. Определены меры защиты?
10. Есть ли process передачи сведений об инцидентах?

## Next action

```text
survey
→ inventory
→ categorize
→ threat model
→ implement controls
→ maintain reporting and incident process
```

## Verification

- перечень объектов завершён;
- categorization documented;
- threat model соответствует объектам;
- выбранные меры привязаны к категории;
- incident/reporting workflow определён.

## Rollback

Для правовых и организационных изменений rollback в главе не определён.

Rollback: `[Needs confirmation]`.
