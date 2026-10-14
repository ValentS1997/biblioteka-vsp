# Глава 10. Запуск рабочих нагрузок производственного уровня в Kubernetes

**Inventory:** `0033` · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Издание:** второе (RU, 2026) · **Chapter:** 10  
**Artifact Collection:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source policy:** `rag_only`

## Scope и provenance

- **Границы: VERIFIED.** PDF/печатные страницы **366–383** включительно. Заголовок главы на p0366, раздел «Резюме» на p0382–p0383, дополнительные источники p0383; глава 11 начинается на p0384. Границы также подтверждены RAG-оглавлением p0014–p0015.
- **Chapter RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0366:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0383:c01`, **18 адресных страниц**; `rag/chunks/p0301-p0400/p####-c01.md`. PDF source locator 366–383, printed pages 366–383, EPUB spine Not applicable.
- **Canonical source PDF:** `source/book.pdf`; SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** book-level readiness run `38394894818` PASS; current `main` RAG acceptance and v1.7 template checked. Повторный readiness CLI запуск здесь не утверждается.
- **Evidence discipline:** только RAG главы, не прямой PDF, не внешние источники, не восполнение пробелов из памяти модели.

## Карта главы

| Раздел | PDF | Предмет |
|---|---:|---|
| Технические требования; HA/FT | 366–369 | Доступность, failover, SPOF, балансировка, разграничение HA приложений и control plane |
| ReplicationController | 370 | Исторический механизм; контроллер как цикл согласования desired/actual |
| ReplicaSet и сравнение | 370–371 | Реплики, селекторы, интеграция с Deployment, отличие от RC |
| Создание ReplicaSet | 372–374 | Многоузловой kind, `replicas: 4`, `matchLabels`, `matchExpressions`, Pod template |
| Self-healing и adoption | 375–376 | Замена удалённого Pod; принятие «голого» Pod и риск совпадающих меток |
| Сервис и отказ узла | 377–378 | `nginx-service`, `port-forward`, `cordon`, `drain`, `delete node`; восстановление реплик |
| Масштабирование | 378–379 | Declarative `apply` с 5 и 2 репликами, imperative `scale` |
| Liveness под ReplicaSet | 379–381 | HTTP GET `/`, ошибка HTTP 403 после удаления `index.html`; перезапуск выполняет kubelet |
| Удаление и orphan | 382 | Default cascading deletion и `--cascade=orphan` |
| Резюме / источники | 382–383 | Итоги темы высокой доступности, переход к Deployment |

## Основной принцип

**ReplicaSet поддерживает заданное количество Pod, отбираемых селектором, используя шаблон `spec.template` (p0370–p0374).** Если Pod исчезает, контроллер создаёт замену; но это **не гарантия нулевого простоя** и не доказательство отказоустойчивости всей системы. Service нужен как точка доступа, а распределение по узлам, сохранность данных и доступность управляющих компонентов требуют отдельной оценки (p0367–p0369, p0377–p0378).

Для ливнес-проверки важно различать *ReplicaSet self-healing* (замена Pod) и *kubelet restart* (перезапуск контейнера в том же Pod), что источник подчёркивает на p0381.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — problem, baseline, read-only, interpretation, modifying action, verification, rollback.
- [commands.md](commands.md) — source-confirmed команды и YAML с классификацией воздействий.
- [diagram.md](diagram.md) — Mermaid-логика репликации, HA и liveness.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактный визуальный конспект.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробный визуальный конспект.
- [summary.md](summary.md) — оригинальное книжное «Резюме» на p0382–p0383.
- [source-findings.md](source-findings.md) — расхождения сценариев, неоднозначности и operational caveats.

**Review questions/answers:** [Not applicable] — самостоятельного блока контрольных вопросов/упражнений на страницах 366–383 нет.

## Точные RAG-ссылки

- [Высокая доступность, p0367](../../../rag/chunks/p0301-p0400/p0367-c01.md)
- [Failover и fault tolerance, p0368](../../../rag/chunks/p0301-p0400/p0368-c01.md)
- [Контроллеры и Deployments, p0369](../../../rag/chunks/p0301-p0400/p0369-c01.md)
- [ReplicationController, p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md)
- [ReplicaSet/RC, p0371](../../../rag/chunks/p0301-p0400/p0371-c01.md)
- [ReplicaSet YAML, p0372](../../../rag/chunks/p0301-p0400/p0372-c01.md)
- [Selectors и adoption, p0373](../../../rag/chunks/p0301-p0400/p0373-c01.md)
- [ReplicaSet apply/describe, p0374](../../../rag/chunks/p0301-p0400/p0374-c01.md)
- [Удаление Pod, p0375](../../../rag/chunks/p0301-p0400/p0375-c01.md)
- [Голый Pod, p0376](../../../rag/chunks/p0301-p0400/p0376-c01.md)
- [Cordon/drain, p0377](../../../rag/chunks/p0301-p0400/p0377-c01.md)
- [Поведение после отказа, p0378](../../../rag/chunks/p0301-p0400/p0378-c01.md)
- [Scale, p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md)
- [Probe YAML, p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md)
- [Unhealthy и kubelet restart, p0381](../../../rag/chunks/p0301-p0400/p0381-c01.md)
- [Delete/Orphan и резюме, p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md)
- [Продолжение резюме, p0383](../../../rag/chunks/p0301-p0400/p0383-c01.md)

## Ограничения и безопасность

Пример `kind create cluster`/ `kubectl drain`/ `kubectl delete node` меняет инфраструктуру, потенциально нарушая доступность; **не выполнять на действующем кластере**. `kubectl exec ... rm index.html` разрушает содержимое контейнера для имитации отказа. Пересечение селекторов может привести к неожиданному захвату или удалению Pod. Списки имён Pod, IP, числовые результаты и версия kind относятся к среде автора, не проверены на текущем кластере. Подробности в [source-findings.md](source-findings.md). Canonical PDF, RAG, registry и статус/прогресс чтения остаются неизменными.
