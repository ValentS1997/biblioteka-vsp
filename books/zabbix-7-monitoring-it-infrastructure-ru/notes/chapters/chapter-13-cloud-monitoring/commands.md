# Глава 13 — команды и GUI, подтверждённые RAG

**Источник:** RAG-only PDF 490–510. Действия не выполнялись. `Read-only` — осмотр, `Workload-generating` — обращение к API или агенту, `State-changing` — создание/изменение ресурсов, `Security-sensitive` — IAM, секреты, Docker privileges. Внешние URL только цитируются из книги и **не проверялись на актуальность**.

## 1. AWS Cloud monitoring — API / IAM

| Действие из книги | Класс | Влияние, риск и проверка |
|---|---|---|
| `AWS Console → My Security Credentials → Users → Add users` | State-changing | Отдельная учётная запись Zabbix; не использовать человеческие root access keys ([p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md)–[p0492](../../../rag/chunks/p0401-p0500/p0492-c01.md)) |
| `Create inline policy → JSON → Create policy` | State-changing / Security-sensitive | Полный IAM policy JSON **только на рис. 13.5** — `RAG_MISS`; permissions должны соответствовать используемому AWS template ([p0493](../../../rag/chunks/p0401-p0500/p0493-c01.md)–[p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)) |
| `Access keys → Create access key` | State-changing / Security-sensitive | Access key ID и Secret access key сохраняются в приватном vault, не в Git/логах; обязательно проверить ограничения доступа ([p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)–[p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md)) |
| `Data collection → Hosts → Create host`, шаблон `AWS by HTTP`, группа `Cloud` | State-changing | Учебное имя `lar-book-aws`; template Script/HTTP вызывает облачный API, возможны оплачиваемые CloudWatch запросы ([p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md), [p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md)) |
| `Hosts → Macros` и `{$AWS.REGION}` | State-changing / Security-sensitive | Регион влияет на scope LLD; источник предлагает отдельный host для каждого AWS region. Macro values с рисунка = `RAG_MISS` ([p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md)) |
| `Templates → AWS by HTTP → Discovery` и созданные EC2/RDS/S3 hosts | Read-only в UI; автоматическое обнаружение Workload-generating | Три LLD rules формируют host prototypes; метрики — из resource-specific template ([p0497](../../../rag/chunks/p0401-p0500/p0497-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)) |

Книга **не содержит проверенной AWS CLI shell-команды**, IAM JSON или исчерпывающей стоимости; их нельзя достраивать по памяти. Внимание: [p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md) говорит «ключ сохранён в шаге 19», хотя непосредственная генерация/сохранение выполняется в шаге 18 на той же странице; см. [source-findings.md](source-findings.md).

## 2. Microsoft Azure — приложение, разрешения и secrets

| Действие | Класс | Назначение |
|---|---|---|
| `Azure Portal → Enterprise applications → New application → Create your own application` | State-changing | Создание корпоративного приложения, запись Application ID в текстовом рецепте ([p0499](../../../rag/chunks/p0401-p0500/p0499-c01.md)–[p0500](../../../rag/chunks/p0401-p0500/p0500-c01.md)) |
| `Azure Active Directory → App registrations → New registration` | State-changing | Автор далее создаёт регистрацию приложения отдельно; их identity relationship нельзя угадать по тексту, `[Needs confirmation]` ([p0500](../../../rag/chunks/p0401-p0500/p0500-c01.md)–[p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md)) |
| `Certificates & secrets → New client secret` | State-changing / Security-sensitive | Создать secret с жизненным циклом, сохранить **Value при однократном показе**; без публикации реального значения ([p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md)–[p0502](../../../rag/chunks/p0501-p0600/p0502-c01.md)) |
| `Subscriptions → Access control (IAM) → Add role assignment → Reader` | State-changing / Security-sensitive | Дать Reader выбранному принципалу в нужной Subscription, а не широкие роли ([p0502](../../../rag/chunks/p0501-p0600/p0502-c01.md)–[p0503](../../../rag/chunks/p0501-p0600/p0503-c01.md)) |
| `Tenant properties`, Subscription ID | Read-only | Получить именно ID нужного tenant и subscription без раскрытия данных организации ([p0502](../../../rag/chunks/p0501-p0600/p0502-c01.md)–[p0504](../../../rag/chunks/p0501-p0600/p0504-c01.md)) |
| `Data collection → Hosts → Create host`, `Azure by HTTP`, группа `Cloud` | State-changing | Пример `lar-book-azure`; шаблон создаёт ресурсы по LLD/API ([p0504](../../../rag/chunks/p0501-p0600/p0504-c01.md)–[p0506](../../../rag/chunks/p0501-p0600/p0506-c01.md)) |

**Точные макросы из [p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)**, где вместо секретов использовать полученные локальные значения:

```text
{$AZURE.APP.ID}           = <APPLICATION_ID>
{$AZURE.PASSWORD}         = <CLIENT_SECRET_VALUE>
{$AZURE.SUBSCRIPTION.ID}  = <SUBSCRIPTION_ID>
{$AZURE.TENANT.ID}        = <TENANT_ID>
```

Это **схема данных**, не CLI и не готовый файл с настоящими credentials. Все четыре значения scope целевой среды; secret Value никогда не помещать в файлы артефактов. `Azure by HTTP` имеет **шесть LLD rules**, создающих hosts для VM/DB и специальные resource templates ([p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)). Точные внутренние JavaScript source code/JSONPath fields на рис. 13.33–13.35 = `RAG_MISS`.

## 3. Docker — Agent 2 и права Docker daemon

Текст источника [p0508](../../../rag/chunks/p0501-p0600/p0508-c01.md) предлагает команды только для **подготовленной Linux лаборатории**, не для немедленного применения на production:

```sh
# State-changing: выбор repo под OS; старый Zabbix 7.0 repo из книги.
# RHEL 8
rpm -Uvh https://repo.zabbix.com/zabbix/7.0/rhel/8/x86_64/zabbix-release-7.0-1.el8.noarch.rpm
dnf clean all
dnf install zabbix-agent2

# Ubuntu 22.04, альтернативная ветка (не вместе с RHEL)
wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_7.0-1+ubuntu22.04_all.deb
dpkg -i zabbix-release_7.0-1+ubuntu22.04_all.deb
apt update
apt install zabbix-agent2
```

Пакеты/URLs/подписи **не проверялись**. Нельзя выдавать их за безопасный способ установки текущей версии или одобрять запуск без подписей и утверждённой политики.

```ini
# /etc/zabbix/zabbix_agent2.conf — State-changing при сохранении
Server=<AUTHORIZED_ZABBIX_SERVER_OR_PROXY>
```

```sh
# Команда книги p508, State-changing / Privilege-sensitive:
# НЕ исполнять автоматически. Membership группы docker может дать широкие привилегии.
gpasswd -a zabbix docker

# State-changing: перезапуск агента после утверждённой конфигурации
systemctl restart zabbix-agent2
```

Книга ставит `Server=10.16.16.102` — **только учебный IP**. Команду группы `docker` рассматривать как **опасное изменение модели доступа**: нужны утверждение owner, alternative Docker socket access policy и rollback `[Needs confirmation]`. Сам текст не рассматривает риск privilege escalation.

**Zabbix GUI:** `Data collection → Hosts → Create host → Docker containers` → `Docker by Zabbix agent 2` (**State-changing**). Приёмка: master `Docker: Get info` / key **`docker.info`**, dependent items; LLD rules Docker images/containers; ключ **`docker.containers.discovery`** создаёт `{#NAME}`; другой master **`docker.container_info`** питает per-container dependent metrics ([p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md)). Создание и удаление реальных Docker containers глава не требует.

## 4. Контроль, ограничения и rollback

Последовательность диагностики без изменения конфигурации: убедиться в наличии target resources → credentials/permissions и scope → `AWS/Azure by HTTP` или Docker master item → raw JSON → LLD → host/item prototypes → `Monitoring → Latest data`. Не выводить секреты на экран и не расширять IAM / Docker доступ ради «проверки».

**Нет полного источникового rollback** IAM policies, доступа Azure Reader, secret rotation, удаления созданных hosts, repo packages, доступа Docker группы. Документировать локальный механизм восстановления отдельно; `[Needs confirmation]`. [Source findings](source-findings.md) содержит ошибки ссылок на шаги и ограничения рисунков.
