# Глава 19. Продвинутые методы планирования подов

**Книга:** №0033 · `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · второе, русское издание (2026).  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`; **source_policy:** `rag_only`.

## Provenance и готовность

- **Границы подтверждены:** PDF/печатные страницы **641–667** включительно; заголовок `p0641:c01`, заключительное «Резюме» `p0666:c01`, дополнительные источники `p0667:c01`, глава 20 начинается на p0668 (TOC `p0019:c01`).
- **RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0641:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0667:c01`, 27 адресных chunks из `rag/chunks/p0601-p0700/p####-c01.md`. Source format PDF; EPUB spine Not applicable.
- **Canonical PDF:** `source/book.pdf` SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`; `failed_checks: []`; corpus `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** book readiness GitHub Actions `38394894818` ранее PASS; current source acceptance и v1.7 contract проверены в `main`. Не заявляем новый CLI readiness run.
- **Режим:** только существующий книжный RAG. Прямое чтение PDF, внешние ссылки, модельная память для исправления текста и живой Kubernetes запрещены. Пробелы: **[Needs confirmation]**.

## Карта главы

| Тема | Страницы | Основной результат |
|---|---:|---|
| Требования и kube-scheduler | 641–644 | Незанятые Pod → фильтрация → оценка → привязка nodeName, kubelet |
| Прямой выбор узла через nodeName | 645–648 | nginx Deployment: 5 реплик на одном minikube-m02, scheduler bypass |
| nodeSelector | 648–652 | node-type=superfast → только m02/m03; node-type=slow отсутствует → rollout Pending |
| nodeAffinity | 652–656 | required NotIn extremelyslow; preferred In fast/superfast, rollout restart |
| Taints/tolerations | 656–663 | NoSchedule / PreferNoSchedule / NoExecute, `tolerationSeconds: 60`, 403 не участвует |
| Статические Pod | 663–664 | kubelet на конкретном узле, mirror Pod, файлы или URL |
| Конфигурация планировщика | 664–666 | Профили и плагины; NodeRestriction, percentageOfNodesToScore |
| Резюме и ссылки | 666–667 | Заключение и переход к autoscaling |

## Ключевая модель

**kube-scheduler** наблюдает ещё не назначенные Pod через API, выполняет **filter** по требованиям, **score** подходящих узлов и привязку Pod к выбранному узлу. **kubelet** запускает назначенную рабочую нагрузку (pp642–643). Уже выполняющиеся Pod не мигрируют при обычном изменении меток; нужен новый Pod/перезапуск, внешний descheduler упомянут отдельно (pp644, 653, 655).

Для размещения:
- `spec.nodeName`: прямая привязка, обход scheduler, очень жёсткая и хрупкая (pp645–648).
- `spec.nodeSelector`: все заданные равенства с labels узла обязательны; отсутствие нужной метки даёт **Pending** и может остановить rolling Deployment (pp648–651).
- `spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution` — жёсткие ограничения; `preferredDuringSchedulingIgnoredDuringExecution` — мягкие с весом (pp652–656).
- **taint** ставится **на узел**; **toleration** — в Pod. `NoSchedule` запрещает новое назначение без допуска, `PreferNoSchedule` мягко отталкивает, `NoExecute` также вытесняет существующие Pod (pp656–662).
- `tolerationSeconds: 60` допускает работу на узле с `NoExecute` ограниченное время; добавление отдельного `NoSchedule` в учебном опыте предотвращает возврат Pod на такой узел после выселения (pp660–662).
- **Static Pod** управляется локальным kubelet и его файлом/URL; API видит зеркальный Pod, а не управляющий объект. Не заменяет DaemonSet для запуска на каждом узле (p663).
- Scheduler profiles, extension points, NodeRestriction, `percentageOfNodesToScore` обсуждаются теоретически; источник не показывает применённый/проверенный рабочий scheduler config. Особое замечание: p666 `KubeSchedulerConfiguration v1alpha1`/`algorithmSource` против p664 перехода на конфигурацию v1.23, **[Needs confirmation]**.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — symptom, baseline, read-only checks, interpretation, next action, modifications, verification, rollback.
- [commands.md](commands.md) — только поддержанные RAG команды, фрагменты YAML, effects/risks/rollback.
- [diagram.md](diagram.md) — схемы планирования, Affinity, taint/NoExecute, static Pod.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная карта главы.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная карта главы.
- [summary.md](summary.md) — пересказ раздела «Резюме» p666.
- [source-findings.md](source-findings.md) — проблемы извлечения, неоднозначности CLI и конфигурации, реальные ограничения source.

**Контрольные вопросы/ответы:** [Not applicable]; самостоятельного финального раздела вопросов/упражнений в главе нет; встроенные пошаговые упражнения учтены в cheatsheet/commands.

## Evidence anchors

- [Overview p0642](../../../rag/chunks/p0601-p0700/p0642-c01.md)
- [Filter/score p0643](../../../rag/chunks/p0601-p0700/p0643-c01.md)
- [No rescheduling; minikube p0644](../../../rag/chunks/p0601-p0700/p0644-c01.md)
- [nodeName p0647](../../../rag/chunks/p0601-p0700/p0647-c01.md)
- [nodeSelector p0650](../../../rag/chunks/p0601-p0700/p0650-c01.md)
- [Pending rollout p0651](../../../rag/chunks/p0601-p0700/p0651-c01.md)
- [Affinity scenario p0653](../../../rag/chunks/p0601-p0700/p0653-c01.md)
- [Affinity YAML p0654](../../../rag/chunks/p0601-p0700/p0654-c01.md)
- [Rollout restart p0656](../../../rag/chunks/p0601-p0700/p0656-c01.md)
- [Taint effects p0657](../../../rag/chunks/p0601-p0700/p0657-c01.md)
- [taint commands p0658](../../../rag/chunks/p0601-p0700/p0658-c01.md)
- [Tolerations p0659](../../../rag/chunks/p0601-p0700/p0659-c01.md)
- [Pending on taint p0660](../../../rag/chunks/p0601-p0700/p0660-c01.md)
- [NoSchedule fix p0661](../../../rag/chunks/p0601-p0700/p0661-c01.md)
- [Malformed cleanup p0662](../../../rag/chunks/p0601-p0700/p0662-c01.md)
- [Static Pod p0663](../../../rag/chunks/p0601-p0700/p0663-c01.md)
- [Profiles p0664](../../../rag/chunks/p0601-p0700/p0664-c01.md)
- [NodeRestriction p0665](../../../rag/chunks/p0601-p0700/p0665-c01.md)
- [Scheduler config mismatch and summary p0666](../../../rag/chunks/p0601-p0700/p0666-c01.md)

## CI acceptance boundary

Подготовка этой коллекции не является доказательством успешного запуска kubectl, планировщика, автоматического выселения на другом кластере или совместимости исторического KubeSchedulerConfiguration. Проверка репозитория относится к структуре артефактов, RAG-ссылкам и SVG, не к живому планированию.

## Operational boundary

Материал из книги, не рабочий runbook без валидации: имена узлов, версии k8s, политики и доступность scheduler, реальные taints, cluster ownership, uptime, rollback **[Needs confirmation]**. Не запускались kubectl/minikube; не изменены PDF/LFS, RAG, registry, metadata, даты/статус чтения.
