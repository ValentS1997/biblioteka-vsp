# Cheatsheet — Глава 20. MPLS

Source: computer-networks-olifer-7e-ru-2026; RAG p0608:c01–p0638:c01, PDF 608–638. Policy: rag_only. Данные не относятся к проверенной действующей MPLS-сети.

## Symptom / problem framing

Типовые проблемы для **концептуальной локализации** по главе:
- трафик отнесён не к тому классу FEC или исходящему пути LSP;
- не согласованы IP/IGP reachability, LDP label binding и LFIB;
- TE-туннель не соответствует ограничениям пропускной способности/метрики;
- резервный путь отсутствует, активировался не там или восстановление основного пути запаздывает;
- смешаны понятия локальной MPLS-метки и глобального SR Node-SID.

## Baseline / context

| Уровень | Роль и источник |
|---|---|
| Client / FEC | LER выделяет класс пакетов по префиксу IP, сервису, интерфейсу и др. (p0617) |
| Forwarding | FTN выбирает LSP, LFIB задаёт next hop и Push/Swap/Pop (p0616–p0619) |
| Control | IGP даёт маршруты и topology; LDP — привязку меток, RSVP-TE или SR-MPLS — TE-пути (p0613, p0623–p0633) |
| TE | OSPF/IS-IS TE → TED → CSPF → LSP/Policy; метрики: bandwidth, free reserve, link color, delay (p0628–p0629) |
| Resilience | восстановление через IGP/начальный узел отдельно от локального link/node detour (p0635–p0638) |

## Read-only checks

Все шаги ниже — **вопросы к уже имеющейся схеме/выводу**; конкретной Linux/router CLI в главе нет.

1. Проверен ли нужный FEC и его отображение в FTN на входном LER? [p0616–p0617]
2. На каждом LSR согласован ли входной label, действие LFIB, выходной label и следующий хоп? Локальность меток учтена? [p0608–p0609, p0615–p0616]
3. Корректна ли точка Push/Swap/Pop, PHP и последовательность верхних/нижних меток? [p0618–p0622]
4. Для LDP: есть ли IGP-маршрут, neighbour discovery, LDP session, label mapping и downstream-сосед? Отдельно — выбран ли режим ordered/independent и on-demand/unsolicited? [p0623–p0627]
5. Для TE: какие ограничения пропускной способности, резервирования, цвета и задержки попадают в TED и при CSPF? Это LDP/IGP-путь или независимо выбранный TE-путь? [p0627–p0629]
6. Для SR-MPLS: Node-SID или Adj-SID? Валиден ли порядок SR-Policy, известны ли SRGB/SRLB в модели главы? [p0630–p0633]
7. Для отказа: отказан link, node или path; есть ли заранее рассчитанный detour и возврат к основному LSP? Как активируются верхняя и нижняя метки? [p0635–p0638]

## Interpretation

- Forwarding по LFIB и создание пути LSP — **разные плоскости** (data/control). [p0613–p0616]
- LDP следует IP/IGP-маршруту; RSVP-TE и SR-Policy используют ограничения или выбранную последовательность сегментов. [p0623, p0628–p0633]
- Факт построенного LSP не гарантирует полосу PVC/TE без проверки применяемой модели резервирования и ресурсов. [p0612, p0629]
- Узел с глобальным Node-SID обрабатывается иначе, чем узел с обычными локальными метками. [p0630–p0632]
- Local FRR является **временной защитой**, а не доказательством восстановления/устойчивости всего TE-пути. [p0636–p0638]
- Ряд меток в иллюстрациях конфликтует с соседними словами/таблицами — source-findings.md.

## Next action

Составить read-only модель трассы: ingress LER/FEC → FTN/LSP → (hop, incoming label, LFIB action, outgoing label) → egress LER. При отклонении отметить конкретный уровень: IP/IGP, LDP, TE/CSPF, SR-Policy, FRR. Без фактических конфигураций и наблюдений корректность сети: **[Needs confirmation]**.

## Modifying action

В главе описаны **потенциально изменяющие** действия: установить PVC/LSP, назначить FEC или SID, изменить LFIB/FTN, запустить RSVP-TE с резервированием, применить SR-Policy, перестроить detour. Реальные команды, интерфейсы, maintenance window, права доступа и область воздействия **[Needs confirmation]**. Нельзя трактовать учебные метки/адреса как готовые конфигурации.

## Verification / acceptance checks

Концептуальная проверка считается пройденной, если документированы:
- FEC → LSP → LFIB на пути;
- локальность меток и различие Node-SID/Adj-SID;
- ветка LDP versus RSVP-TE versus SR-MPLS;
- входные TE-ограничения и источник вычисленного пути;
- наличие/отсутствие резерва и разделение fast protection / slower recovery;
- реальные performance и failover measurements не выдуманы.

## Rollback

Для анализа read-only: **[Not applicable]**. Для state-changing действий в RAG **нет конфигурационных команд и проверяемой процедуры rollback**: [Needs confirmation]. При отсутствии rollback изменения не выполнять.
