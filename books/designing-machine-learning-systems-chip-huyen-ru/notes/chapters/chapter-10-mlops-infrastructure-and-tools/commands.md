# Commands and tools — глава 10

Источник: только канонический RAG PDF 297–334, `p0297-c01`–`p0333-c01`, SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`.

## Исполнение и границы

Глава содержит фрагменты **Dockerfile, Slurm, Airflow Python DAG, Argo YAML и Metaflow**, но текстовый слой местами повреждён (типографика флагов, кавычки, отступы, ключи и операторы). Эти фрагменты **не являются подтверждёнными исполняемыми файлами**. Ни одна команда не выполнялась; `commands.md` фиксирует RAG-доказательства, функции и побочные эффекты.

| Тип действия | Инструмент / фрагмент из RAG | Подтверждённый контекст и ограничения |
| --- | --- | --- |
| Read-only | CPU/GPU/TPU/vCPU, memory/throughput/FLOP/s, cloud quotas, costs | Сопоставление вычислительных ресурсов; нет доступа к реальной инфраструктуре или актуальному тарифу [p0301-c01–p0305-c01] |
| Read-only / modifying local | Jupyter Notebook, JupyterLab, Google Colab, VS Code, Vim, SSH | Среды разработки, подключение к облаку, риск порядка ячеек и зависимостей; конкретная конфигурация отсутствует [p0306-c01–p0311-c01] |
| State-changing / workload | Dockerfile `FROM pytorch/pytorch:latest`, `RUN git clone`, `WORKDIR /fancy-nlp-project` | **Только цитируемые идентификаторы**, не сборочный рецепт: зависимость от изменяемого latest, внешнего git и повреждённых флагов установки; запуск создал бы образ и сеть/вычислительные расходы [p0312-c01–p0313-c01] |
| State-changing | Docker Compose, Kubernetes/K8s, Minikube, AWS EKS, Google GKE | Запуск контейнеров, сеть, replicas и cluster placement; отсутствуют манифесты и право доступа [p0313-c01; p0317-c01] |
| State-changing / workload | Cron, Slurm directives `#SBATCH -J JobName`, `ttSBATCH —time=ll:00:00`, `#SBATCH —mem-per-cpu=4096` | В исходнике есть обрывки job script, но часть `SBATCH`/dash/цифр повреждена; **не отправлять в кластер** [p0314-c01–p0316-c01] |
| State-changing / workload | Airflow `DAG`, `BashOperator`, `DockerOperator`, `schedule_interval` | Python DAG с зависимостями и контейнерным шагом; `dag^dag`, `tl » t2`, кавычки и сетевой адрес Docker повреждены; не копировать в CI [p0318-c01–p0319-c01] |
| State-changing / workload | Argo `kind: Workflow`, `generateName: coinflip`, `when` | YAML-ветвление по результату coin flip; `apiVersion: argoproj.io/vlalphal`, фигурные скобки, отступы повреждены [p0320-c01–p0321-c01] |
| State-changing / workload | Metaflow `FlowSpec`, `@step`, `@batch`, `@conda` | Локальный + AWS workflow; декоратор `Qconda`, кавычки и скобки нарушены; не исполнять [p0321-c01–p0322-c01] |
| State-changing | MLflow Models, SageMaker, Vertex AI, Azure ML, Seldon, Cortex, Ray Serve | Сервисы развёртывания/registry; нет проверенных URL, image tags, deployment options и rollback [p0323-c01–p0327-c01] |
| Read-only / state-changing | MLflow model registry, DVC, GitHub, GitLab | Хранение артефакта, версии данных/кода и зависимостей; публикация новой версии меняет состояние [p0325-c01–p0328-c01] |
| Read-only / state-changing | Amundsen, DataHub, Feast, Tecton | Каталог, вычисление и контроль parity признаков; управление правами и загрузкой обновляет содержимое/данные [p0328-c01–p0330-c01] |

## Типизированные свидетельства (не runnable code)

- `p0312-c01`: `FROM pytorch/pytorch:latest` — без закреплённого digest/версии; не использовать для воспроизводимой сборки без подтверждения.
- `p0316-c01`: `ttSBATCH —time=ll:00:00` — сбой извлечения, а не рабочая директива Slurm.
- `p0319-c01`: `tl » t2` — из текстового слоя нельзя установить точную переменную `t1` или синтаксис оператора.
- `p0320-c01`: `apiVersion: argoproj.io/vlalphal` — значение не подтверждено; `when` со сломанными ограничителями.
- `p0322-c01`: `Qconda(libraries=...)` и `@batch(gpu=2, memory=16000)` — функциональный контекст, не гарантия действительного декоратора/API.

## Preconditions / verification / rollback

До state-changing действий требуются подтверждённые repository и версии, целевая инфраструктура, credentials/permissions, resource quotas, network policy, data classification, idempotency, effect verification, аварийная остановка и rollback. Глава не подтверждает ни одну реальную команду запуска в пользовательской среде: **[Needs confirmation]**. Сверять любые команды с оригинальным кодом/версией отдельно, без silent correction в `rag_only`.
