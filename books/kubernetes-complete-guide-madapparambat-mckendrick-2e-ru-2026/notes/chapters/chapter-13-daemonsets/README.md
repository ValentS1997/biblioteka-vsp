# Глава 13. Объект DaemonSet: запуск одного пода на каждом узле

**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе, русское (2026)  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **source policy:** `rag_only`.

## Provenance / границы

- **Глава VERIFIED:** PDF/печатные страницы **457–473** включительно. Заголовок p0457; раздел «Резюме» и источники p0473; глава 14 начинается на **474**. Оглавление p0016:c01.
- **Addressable RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0457:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0473:c01` (17 page chunks); путь `rag/chunks/p0401-p0500/p####-c01.md`. EPUB spine: not applicable.
- **Canonical PDF:** `source/book.pdf` SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Book readiness:** workflow `38394894818` PASS; acceptance and v1.7 template checked on `main`. Повторного исполнения readiness CLI не заявлено.
- **Evidence mode:** только chapter RAG, без прямого PDF, внешних источников и корректировок по памяти модели. Неизвестное обозначается **[Needs confirmation]**.

## Структура главы

| Тема | Страницы | Что доказывает источник |
|---|---:|---|
| Назначение DaemonSet | 457–460 | Фоновый Pod на каждом подходящем узле, изменение при добавлении/удалении узла, selector/node affinity |
| Планирование и аудит | 460–462 | Многоузловой minikube с Calico, `get daemonsets -A`, `get po -n kube-system` |
| Fluentd DaemonSet | 462–466 | Исторический образ Fluentd; `selector`/`template`, `hostPath: /var/log`, labels, requests/limits |
| PriorityClass | 466–467 | Приоритеты системных Pod; `fluentd-priority`; предостережение о вытеснении |
| Изменения DaemonSet | 467–469 | `RollingUpdate`/`OnDelete`; образ v4.7→v4.7.5, `rollout status`, `describe ds` |
| Откат и удаление | 469 | `rollout undo`, cascading/orphan, `drain --ignore-daemonsets` |
| Сценарии, практики и альтернативы | 470–473 | kube-proxy, CNI, Ceph, ingress, Fluentd, node-exporter; resources/affinity, sidecar/CronJob/systemd/static Pods |
| Резюме | 473 | Итоги и переход к Helm/операторам |

## Главное

**DaemonSet поддерживает одну управляемую Pod-реплику на каждом подходящем узле**, а не заранее заданное число реплик (p0457–p0460, p0464). Количество Pod определяется набором eligible nodes, `nodeSelector`, `nodeAffinity` и `tolerations`. Увеличение числа подходящих узлов приводит к появлению Pod; изменение условий соответствия — к изменению набора Pod (p0460, p0468).

В отличие от пользовательского Deployment, DaemonSet часто обеспечивает функции самого кластера: CNI, kube-proxy, сбор логов и метрик (p0458, p0470–p0471). Поэтому ошибочное изменение может повлиять сразу на множество узлов и сетевую функциональность.

**Critical source discrepancy:** фрагмент `fluentd-daemonset.yaml` объявляет Namespace `logging`, но DaemonSet `metadata.namespace: kube-system` (p0463). Команда `kubectl describe daemonset ... -n logging` и вывод `kubectl get po -n logging` (p0465) используют **другой namespace**. В `commands.md` это обозначено как непроверенный, несогласованный учебный пример, не runnable production YAML. Не исправлять значение молча.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — baseline, read-only checks, интерпретация, изменение, verification и rollback.
- [commands.md](commands.md) — CLI/YAML из главы, классы эффектов, риски и границы.
- [diagram.md](diagram.md) — Mermaid: topology, обновления, риски и проверка.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная карта.
- [summary.md](summary.md) — оригинальное «Резюме» p0473.
- [source-findings.md](source-findings.md) — несогласованность namespace и прочие замечания.

**Review questions/answers:** [Not applicable], отдельного блока контрольных вопросов или упражнений на p0457–p0473 не найдено.

## Evidence index

- [Назначение, p0457](../../../rag/chunks/p0401-p0500/p0457-c01.md)
- [Типы задач, p0458](../../../rag/chunks/p0401-p0500/p0458-c01.md)
- [Планирование и Services, p0460](../../../rag/chunks/p0401-p0500/p0460-c01.md)
- [Calico DaemonSet, p0461](../../../rag/chunks/p0401-p0500/p0461-c01.md)
- [Fluentd и node-exporter, p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md)
- [Namespace discrepancy, p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md)
- [hostPath и selectors, p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md)
- [Namespace usage in commands, p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md)
- [PriorityClass, p0466](../../../rag/chunks/p0401-p0500/p0466-c01.md)
- [Update strategies, p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)
- [Rollout, p0468](../../../rag/chunks/p0401-p0500/p0468-c01.md)
- [Rollback and deletion, p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md)
- [Cluster system use cases, p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)
- [Best practices, p0471](../../../rag/chunks/p0401-p0500/p0471-c01.md)
- [Alternatives, p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md)
- [Summary, p0473](../../../rag/chunks/p0401-p0500/p0473-c01.md)

## Scope and safety

Никакие `kubectl`/`minikube` команды не выполнялись. Создание/обновление/удаление DaemonSet, назначение PriorityClass и изменение `hostPath` затрагивают все подходящие узлы и потенциально сбор системных логов. `kubectl drain` может нарушить доступность рабочих нагрузок. Показанный Fluentd не демонстрирует наличие работающего Elasticsearch endpoint. Rollback в реальной среде **[Needs confirmation]**. PDF/LFS, RAG, registry и reading status/progress/dates не меняются.
