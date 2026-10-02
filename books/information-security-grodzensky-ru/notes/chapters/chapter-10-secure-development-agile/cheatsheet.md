# Шпаргалка: безопасная разработка приложений

Цель: встроить анализ безопасности в цикл разработки и понимать границы SAST/DAST.

## Problem framing

В книге быстрые изменения Agile связываются с риском того, что отдельная финальная проверка не успевает за частыми версиями продукта.

Рабочая модель:

```text
code change
   ↓
analysis
   ↓
finding
   ↓
triage
   ↓
fix
   ↓
retest
```

## Типовые ошибки кода из главы

- buffer overflow;
- memory leak;
- stack overflow;
- uninitialized variable;
- access-right violation;
- syntax error;
- algorithmic error.

## SAST vs DAST

| Подход | Что анализируется | Сильная сторона в логике главы |
|---|---|---|
| SAST | Исходный код без исполнения | Видит структурные/логические проблемы в коде |
| DAST | Программа во время выполнения | Видит runtime-ошибки на фактическом пути выполнения |

Источник рекомендует использовать оба подхода.

## False positive / false negative

- false positive — scanner сигнализирует об ошибке, которой фактически нет;
- false negative — scanner пропускает существующую проблему.

Это означает: finding требует triage, а отсутствие finding не является абсолютным доказательством отсутствия дефекта.

## Read-only checks

1. Интегрирован ли code analysis в version-management process?
2. Проверяется ли изменившийся код между версиями?
3. Используются ли SAST и DAST там, где это применимо?
4. Отслеживаются ли false positive / false negative?
5. Поддерживает ли scanner нужные языки?
6. Достаточна ли скорость анализа для текущего development cadence?
7. Есть ли интеграция с системой управления версиями?
8. Может ли scanner визуализировать execution/data-flow graphs?
9. Проверяются ли ERP/web applications отдельными специализированными средствами?
10. Есть ли повторный анализ после исправления?

## Interpretation

### SAST finding

Требует подтверждения контекста: scanner может дать false positive.

### DAST finding

Показывает проблему при конкретном runtime-path, но отсутствие ошибки на проверенном пути не исключает другие дефекты.

### Только SAST или только DAST

По позиции главы — неполное покрытие.

### Browser developer tools

Полезны для:
- просмотра source;
- анализа загруженных ресурсов;
- HTML/JavaScript inspection;
- client-side storage/state inspection.

Но не заменяют специализированные анализаторы.

## Next action

1. Определить точки интеграции анализа в development lifecycle.
2. Выбрать scanner по языкам/скорости/integration capabilities.
3. Запускать SAST для исходного кода.
4. Добавлять DAST для runtime-поведения.
5. Выполнять triage findings.
6. Исправлять подтверждённые проблемы.
7. Повторно анализировать изменённую версию.

## Modifying action

Глава поддерживает:
- исправление дефектов кода;
- корректировку конфигураций ERP/web systems;
- интеграцию анализаторов с version-management systems;
- применение WAF rules как компенсирующей меры в описанном web-сценарии.

Конкретная CI/CD конфигурация: `[Needs confirmation]`.

## Verification / acceptance checks

- подтверждённый defect исправлен;
- повторный анализ больше не показывает тот же finding либо finding объяснён/классифицирован;
- SAST и DAST применяются к соответствующим классам проверки;
- scanner integration соответствует development process;
- false-positive rate не делает процесс непригодным для практической работы.

Конкретные quantitative thresholds: `[Needs confirmation]`.

## Rollback

Source не задаёт rollback для code changes или WAF rules.

Rollback: `[Needs confirmation]`.
