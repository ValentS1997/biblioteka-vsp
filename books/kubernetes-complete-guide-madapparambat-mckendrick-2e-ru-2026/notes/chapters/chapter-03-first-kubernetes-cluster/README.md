# Глава 3. Установка первого кластера Kubernetes

**Книга:** Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.  
**Inventory:** 0033 · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 03  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · **Source mode:** `rag_only`.

## Provenance и границы

- **Chapter title / slug:** «Установка первого кластера Kubernetes» / `chapter-03-first-kubernetes-cluster`.
- **Chapter boundary: VERIFIED.** Глава начинается на PDF/печатной стр. **115**, заканчивается на стр. **142** (раздел «Дополнительные источники информации»); глава 4 начинается на **143**.
- **Boundary evidence:** RAG-оглавление на стр. 8–9, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0115:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0141:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0142:c01`, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0143:c01`.
- **RAG chunk range:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0115:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0142:c01` (28 PDF-страниц, адресные chunk c01). **Source locators:** PDF `115`–`142`; **printed pages:** 115–142; EPUB spine: Not applicable.
- **Canonical source:** `source/book.pdf`; **SHA-256:** `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`.
- **Preflight:** canonical readiness v1.3 and artifact collection v1.7 verified on main, source SHA and manifest agree, previous readiness CI PASS; no new RAG generation.
- **Source policy:** direct reading of canonical PDF, external-source lookup, and filling gaps from model memory prohibited. Versions and platform claims are historical statements from the book, **not externally verified current guidance**.

## Цель и главный принцип

Глава переводит теорию глав 1–2 в практику: развернуть **локальный учебный кластер** с помощью `minikube` или `kind`, подтвердить связь `kubectl` с кластером и корректность узлов/компонентов. **Развертывание production-кластера** требует отдельного выбора и управления инфраструктурой; minikube и kind рассматриваются авторами как инструменты разработки и тестирования (PDF 116–135).

## Карта главы

| Область | PDF | Содержание |
|---|---:|---|
| Требования и minikube | 115–119 | `kubectl`, ≥2 CPU, 2 ГБ RAM, 20 ГБ disk; установка minikube, драйверы и конфигурация |
| Первый кластер и его проверка | 120–125 | VirtualBox/Docker/Podman; `minikube start/status`, kubeconfig, `kubectl get nodes` |
| Управление жизненным циклом и HA | 126–129 | `stop/pause/unpause/delete`, multi-node, `--ha=true`, профили |
| Kind | 129–135 | Установка, `kind create cluster`, YAML из `control-plane` и `worker`, проверка и удаление |
| Учебные среды и production-подходы | 135–141 | Killercoda; GKE/EKS/AKS; OpenShift/Rancher/Tanzu; kubeadm/kops/Kubespray, IaC и on-prem эксплуатация |
| Резюме и источники | 141–142 | Закрепление навыков; переход к Pod в главе 4 |

## Комплект артефактов

- [cheatsheet.md](cheatsheet.md) — подготовка, baseline, проверки, критерии, эксплуатационные границы и возврат состояния.
- [commands.md](commands.md) — source-confirmed команды, классификация и риски; shell-команды являются примерами, а не безусловными инструкциями запуска.
- [diagram.md](diagram.md) — концептуальная карта создания и жизненного цикла учебного кластера.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — обязательный компактный SVG.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — обязательный детальный SVG.
- [summary.md](summary.md) — перенесенное из RAG оригинальное резюме главы (стр. 141–142).
- [source-findings.md](source-findings.md) — предупреждения о расхождении текста/кода, устаревшем API и непроверенных командах.

**Review questions/exercises:** [Not applicable] — отдельный заключительный блок вопросов и упражнений в RAG главы 3 не обнаружен; `review-questions.md` и `review-answers.md` не создаются.

## Быстрые RAG-доказательства

- [Технические требования, p0116](../../../rag/chunks/p0101-p0200/p0116-c01.md)
- [Драйверы minikube, p0119](../../../rag/chunks/p0101-p0200/p0119-c01.md)
- [Первый start, p0121](../../../rag/chunks/p0101-p0200/p0121-c01.md)
- [Проверка minikube, p0125](../../../rag/chunks/p0101-p0200/p0125-c01.md)
- [Stop/pause, p0126](../../../rag/chunks/p0101-p0200/p0126-c01.md)
- [Delete и multi-node, p0127](../../../rag/chunks/p0101-p0200/p0127-c01.md)
- [Kind config, p0132](../../../rag/chunks/p0101-p0200/p0132-c01.md)
- [Kind verification, p0134](../../../rag/chunks/p0101-p0200/p0134-c01.md)
- [Production alternatives, p0136](../../../rag/chunks/p0101-p0200/p0136-c01.md)
- [Резюме, p0141](../../../rag/chunks/p0101-p0200/p0141-c01.md)

## Ограничения

Ни один кластер фактически не создан или изменен. Результаты CLI в книге — **примерные выводы автора**, а не наблюдения реальной инфраструктуры. Minikube/kind требуют локальных ресурсов, загрузок и настроенной среды; инструкции не подтверждены на текущих версиях платформ. Удаление локального кластера уничтожает его состояние (p0127, p0134); **rollback [Needs confirmation]**, восстановления книга не дает. **Reading status и progress не изменялись.**
