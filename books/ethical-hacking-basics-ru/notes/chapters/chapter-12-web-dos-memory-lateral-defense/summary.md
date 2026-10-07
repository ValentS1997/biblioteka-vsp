# Авторское итоговое резюме главы 12

**Источник:** `12.2 Dos, Buffer Over ow, Heap Spraying, Гориз.перемещение, Защита`, **Шаг 11**, начинается в `ethical-hacking-basics-ru:p0348:c02` и продолжается через `p0349:c01`–`p0349:c02`.

## 1. Современная поверхность атак смещается к приложениям

Source summary противопоставляет старые атаки на listening services/network stacks современным application-level attacks, отдельно выделяя веб-приложения как распространённую цель.

## 2. Web application attacks

В финальном блоке повторяются:
- XML external entity abuse;
- SQL injection;
- XSS/session-token theft;
- command/input trust-boundary problems.

Общий defensive вывод source: данные от пользователя нельзя напрямую передавать в подсистемы/interpreters; каждую boundary нужно валидировать.

## 3. Memory corruption

Summary возвращается к buffer overflow и heap spraying как техникам управления execution flow through memory corruption. Эти концепции иллюстрируют impact memory bugs, но chapter artifacts не превращают их в exploit-development instructions.

## 4. Lateral movement

После initial compromise attacker может выполнять дополнительную reconnaissance, privilege escalation and credential access для движения к другим системам и данным.

## 5. Defense-in-depth / breadth and architecture

Source критикует reliance only on “more walls” и расширяет защиту до visibility/control across the stack. Далее вводится **defensible network architecture**: design under the assumption that intrusion can happen, with monitoring, logging, SIEM, segmentation and containment.

## 6. Detection and response

Финальный source вывод:
- logging is required for detection;
- SIEM helps organize/correlate events;
- network/endpoint controls should allow isolation/containment;
- architecture should support seeing and responding to attackers already inside.

## Boundary

- p. 349 — последняя страница книги/RAG.
- Следующей главы в canonical source нет.
- No injection, DoS, memory exploitation or lateral-movement action was executed while creating these artifacts.
