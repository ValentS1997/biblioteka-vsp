# Глава 10 — команды, JSON-RPC и операции UI по RAG

**Ограничение:** команды взяты из accepted RAG PDF 412–433. Исторические URL внешних скриптов **не проверены**; никакой файл по ним не скачивался. Секрет-токены из книги здесь **заменены placeholders**. Классы: **Read-only**, **Workload-generating**, **State-changing**, **Destructive/security-sensitive**.

## 1. API Users и создание токена

| Путь / действие | Класс | Эффект, риск и проверка |
|---|---|---|
| `Users → User groups → Create user group` → `API Users` | State-changing | Доступ к host/template groups; `Read-write` в примере, в production сужать scope; [p0413](../../../rag/chunks/p0401-p0500/p0413-c01.md)–[p0414](../../../rag/chunks/p0401-p0500/p0414-c01.md) |
| `Users → Users → Create user` → `API`, роль `Super admin` | **Security-sensitive / state-changing** | Учебный Super admin дает широкие полномочия. Источник советует более узкие права; [p0414](../../../rag/chunks/p0401-p0500/p0414-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md) |
| `Users → API tokens → Create API token` → `API book key`, owner `API` | State-changing / secret | В книге предлагается дальний срок/без срока; затем **рекомендуется разумный срок и ротация**. Сохранить auth token в vault; [p0416](../../../rag/chunks/p0401-p0500/p0416-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md) |

## 2. Python-окружение и учебный host.get

Формы команд из [p0418](../../../rag/chunks/p0401-p0500/p0418-c01.md)–[p0421](../../../rag/chunks/p0401-p0500/p0421-c01.md), не скрипт для unattended production:

```sh
# Read-only local navigation
cd /home/zabbix/

# State-changing: пакеты ОС; выбрать только один distro
dnf install python3
apt install python3
dnf install python3-pip
apt install python3-pip

# State-changing: зависимости Python
pip3 install requests

# Workload-generating + filesystem state-changing: скачивание/запись внешнего файла
wget https://raw.githubusercontent.com/PacktPublishing/Zabbix-7-IT-Infrastructure-Monitoring-Cookbook/main/chapter10/api_test.py

# State-changing при сохранении, file content не проверен
vim api_test.py

# Workload-generating API-read + file write (свойства точки входа внешнего файла не проверены)
python3 api_test.py

# Read-only просмотр выходного файла из p421, только на учебном host
cat /home/zabbix/results
```

**Не выполнять обе пары команд установки одновременно.** В RAG сказано, что версия Python 3 может оказаться слишком старой и вызывать ошибки — [p0419](../../../rag/chunks/p0401-p0500/p0419-c01.md).

**API payload, параметры из [p0420](../../../rag/chunks/p0401-p0500/p0420-c01.md) (пример структуры; не полная исполнимая программа):**

```json
{
  "jsonrpc": "2.0",
  "method": "host.get",
  "params": {
    "output": ["hostid", "host"],
    "selectInterfaces": ["interfaceid", "ip", "main"]
  },
  "id": 2,
  "auth": "<API_TOKEN_FROM_SECRET_STORE>"
}
```

Отправка происходит посредством `requests.post(url=url, json=payload)` к **`http://<ZABBIX_SERVER>/api_jsonrpc.php`** в учебной строке p419. HTTP **не защищает токен в канале**, конкретная конфигурация безопасного HTTPS = `[Needs confirmation]`. Сам источник содержит буквальный длинный hex-токен, **здесь его не публикуем**.

Код в тексте определяет `get_hosts(api_token,url)`, затем `generate_host_file(hosts,host_file)` и фильтрует `interface["main"] == "1"` перед записью host/IP. **Ни наличие метода retry/error handling, ни безопасное закрытие файла при исключении не подтверждены**. Результат `cat /home/zabbix/results` на p421 расходится с `/home/results` в p422: [source-findings.md](source-findings.md).

## 3. Jumphost: ОС /etc/hosts — destructive

Из [p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md)–[p0426](../../../rag/chunks/p0401-p0500/p0426-c01.md):

```sh
# State-changing: только изолированный лабораторный jumphost, не production
dnf install python3
apt-get install python3
dnf install python3-pip
apt-get install python3-pip
pip3 install requests
wget https://raw.githubusercontent.com/cheatas/zabbix_scripts/main/host_pull_zabbix.py
vim host_pull_zabbix.py

# DESTRUCTIVE: по предупреждению источника файл /etc/hosts перезаписывается целиком
# Ниже literal команды как описание рецепта, НЕ инструкция запуска на рабочей системе:
python3 host_pull_zabbix.py

# Read-only после теста
cat /etc/hosts
cat /etc/hosts | grep agent

# Workload-generating: SSH к учебному host, требует правильного resolution/authorization
ssh lar-book-agent_passive

# State-changing: создание повторяемого задания
crontab -e
```

Строка cron из источника:
```text
*/15 * * * * $(which python3) /home/host_pull_zabbix.py >> ~/cron.log 2>&1
```

**State-changing/Destructive**: каждые 15 минут потенциально повторно переписывает `/etc/hosts`. Текст не устанавливает, что файл действительно помещён в `/home/` после `wget`, как выполняется privilege escalation для записи `/etc/hosts`, и где лежит backup/rollback. Не добавлять эту запись на рабочей машине без отдельного audit и разрешения. В RAG имеются лишь `generate_host_file(zabbix_hosts, "/etc/hosts")` и вне-книжный исходник скрипта — точные защитные условия `RAG_MISS` ([p0424](../../../rag/chunks/p0401-p0500/p0424-c01.md)–[p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)).

## 4. Карта: Host/Enable и Host/Disable

Команды установки архива из [p0428](../../../rag/chunks/p0401-p0500/p0428-c01.md)–[p0429](../../../rag/chunks/p0401-p0500/p0429-c01.md), **не рекомендуется выполнять без проверки source/подписей**:

```sh
# State-changing: создание каталога
mkdir /etc/zabbix/frontendscripts
cd /etc/zabbix/frontendscripts

# Workload-generating, external source not verified
wget https://github.com/OpensourceICTSolutions/zabbix-toggle-hosts-from-frontend/archive/v2.0.tar.gz
# State-changing: распаковка
tar -xvzf v2.0.tar.gz

# State-changing: удаление архива, может нарушить recovery
rm v2.0.tar.gz

# Источник: mv zabbix-toggle-hosts-from-frontend-2.0/enable_disable-host.py./
# **SOURCE CODE MISMATCH**: слиты имя файла и место назначения, не исполнять literal
# Загруженный enable_disable-host.py не проверен

dnf install python3 python3-pip
apt-get install python3 python3-pip
pip3 install requests
vim enable_disable-host.py
```

p429 указывает `url = 'http://10.16.16.152/api_jsonrpc.php?'` и `token = " <hex token> "`; URL со знаком `?` и **пробелы внутри токена** сохранены как неопределённость исходника. Мы не вставляем оригинальный токен и не объявляем эти строки готовой безопасной конфигурацией.

**Zabbix GUI:** `Alerts → Scripts → Create script` дважды для `Host/Enable` и `Host/Disable`, затем `Monitoring → Maps → [host] → Disable → Execute`; проверка `Monitoring → Hosts → Status = Disabled`, повторно `Enable` ([p0429](../../../rag/chunks/p0401-p0500/p0429-c01.md)–[p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md)). **State-changing / privilege-sensitive.** Точная строка Commands из рисунков 10.18–10.19 и права выполнения = `RAG_MISS`.

**Дополнение:** `Alerts → Scripts`: заменить `{HOST.HOST}` на `{MANUALINPUT}` (**State-changing**); `Advanced configuration` заполняет `Input prompt`, `Default input string`, `Input validation rule` ([p0432](../../../rag/chunks/p0401-p0500/p0432-c01.md)). Ввод имени вручную расширяет scope; regex/validation value на рисунке 10.23 = `RAG_MISS`.

## Приёмка и rollback

- **До API вызовов:** токен ограничен и действителен; исключить его из stdout/shell history/Git.
- **После read-only host.get:** проверить hostid, primary `ip`, полученный файл и ожидаемую ограниченную выборку.
- **Перед jumphost и map scripts:** резервная копия, source code review, отдельный тестовый user, журналирование и подтверждённый rollback (`[Needs confirmation]`).
- **После действий:** подтвердить точное системное состояние host, не только появление кнопки/response.

Полный rollback `/etc/hosts`, автоматической cron записи, операций elevated script, secret rotation и стороннего кода **не описан** в RAG.
