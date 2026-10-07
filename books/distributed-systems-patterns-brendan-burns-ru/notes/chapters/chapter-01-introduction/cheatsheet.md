# Шпаргалка: глава 1 — Введение

## Scope

- RAG: `p0018:c01–p0028:c01`
- PDF: `18–28`
- Source policy: `rag_only`
- Chapter type: conceptual / architecture motivation

## Symptom / problem framing

Современные приложения должны:
- быть постоянно доступными;
- работать через API;
- быть готовыми к быстрому росту нагрузки.

Следствие в framing главы:

~~~text
modern application requirements
→ distributed system
→ reliability/scalability opportunities
+ higher design/build/debug complexity
~~~

Проблема: распределенные системы часто создаются как единичные решения, из-за чего команды повторно решают уже известные архитектурные задачи.

## Baseline / context

Историческая линия:

~~~text
single-purpose machine
→ general-purpose computer
→ time-sharing
→ networked computers
→ client/server
→ Internet + large data centers
→ distributed applications
~~~

Инженерная линия повторного использования:

~~~text
formalized algorithms
→ reusable algorithmic ideas
→ OOP design patterns
→ reusable libraries
→ distributed-system patterns
→ reusable components
~~~

Технологический enabler в главе:

~~~text
containers + images + orchestrators
→ standardized building blocks
→ patterns/components easier to reuse
~~~

## Read-only checks

Это design-review checks, а не shell commands.

1. Повторяется ли архитектурная проблема в нескольких системах/командах?
2. Описывается ли решение независимо от конкретного продукта?
3. Есть ли у команды единое имя и определение для этого решения?
4. Можно ли отделить общий компонент от application-specific logic?
5. Решает ли reuse уже известную проблему вместо повторной реализации с нуля?
6. Не подменяется ли понятие «паттерн» инструкцией по установке конкретной системы?

Количественные checks для reliability, performance и scalability: `[Needs confirmation]`.

## Interpretation

### Если команда постоянно заново решает одну задачу

Вероятный chapter-supported вывод:

~~~text
recurring problem
→ candidate generalized pattern
→ shared description
→ reusable implementation where practical
~~~

### Если обсуждение буксует из-за терминов

~~~text
same idea + different names
→ communication overhead
→ shared pattern vocabulary
→ discussion moves to implementation details
~~~

### Если один и тот же код нужен во многих системах

~~~text
repeated implementation
→ identify reusable component
→ implement once
→ broader reuse and feedback
~~~

### Если решение жестко связано с одним стеком

Это еще не тот уровень абстракции, который автор называет distributed-system pattern. Паттерн должен описывать общую организационную/архитектурную структуру.

## Next action

Для архитектурной задачи:

1. Сформулировать повторяющуюся проблему.
2. Отделить invariant architecture от конкретного product stack.
3. Найти/назвать общий паттерн.
4. Использовать это имя как общий словарь команды.
5. Выделить reusable component, если границы решения позволяют.
6. Проверить конкретную реализацию уже в контексте требований системы.

Шаг 6 в главе не сопровождается метриками или operational procedure — они `[Needs confirmation]`.

## Modifying action

`[Not applicable]`.

Глава 1 не задает конкретных state-changing команд, deployment steps или configuration changes. Ее action layer — архитектурное мышление и организация повторного использования.

## Verification / acceptance checks

Conceptual acceptance:

- команда может объяснить проблему независимо от конкретного продукта;
- паттерн имеет общее название и смысл;
- reusable boundary понятна;
- участники отличают pattern от vendor-specific recipe;
- implementation-specific решения обсуждаются после общего архитектурного уровня.

System acceptance:
- фактическая reliability: `[Needs confirmation]`;
- фактическая scalability: `[Needs confirmation]`;
- latency/capacity thresholds: `[Needs confirmation]`;
- failure-injection criteria: `[Needs confirmation]`.

Глава не предоставляет количественной методики проверки этих свойств.

## Rollback

`[Not applicable]`.

В chapter range отсутствует конкретное state-changing действие, для которого можно было бы дать source-confirmed rollback.

## Три ценности паттернов

### 1. Чужой опыт

~~~text
known problem
→ known pattern
→ меньше обучения на собственных ошибках
~~~

### 2. Общий язык

~~~text
shared name
→ shared mental model
→ быстрее перейти к implementation details
~~~

### 3. Общие компоненты

~~~text
pattern
→ reusable implementation
→ reuse across systems
→ больше feedback
→ выше шанс найти defects
~~~

## Definition boundary

Паттерн распределенной системы в этой главе:

- generalized;
- architectural;
- technology-independent;
- applicable across different environments.

Не паттерн:
- инструкция установки конкретной NoSQL-системы;
- правила конкретного application stack;
- product-specific deployment recipe.

## Container boundary

Глава рассматривает containers/images/orchestrators как строительные блоки, которые помогают создавать reusable components.

Не следует выводить из главы:
- конкретный Kubernetes manifest;
- конкретный Docker command;
- конкретный Sidecar implementation;
- конкретную production topology.

Это материал последующих глав или иной source scope.
