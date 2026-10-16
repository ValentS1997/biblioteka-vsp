# Глава 10 — Mermaid: Zabbix API, Python и управление через карту

Основание: **accepted RAG PDF 412–433**. Диаграммы представляют *отношения из текста*, а не скрытые скриншотные команды. Отсутствующий исходный код `RAG_MISS`.

## 1. User → permissions → API token ([p0413](../../../rag/chunks/p0401-p0500/p0413-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md))

```mermaid
flowchart TD
  G["User group: API Users"] --> HOST["Host group permissions"]
  G --> TMPL["Template group permissions"]
  HOST --> USER["API user / выбранная роль"]
  TMPL --> USER
  USER --> TOKEN["Users → API tokens: token + expiry"]
  TOKEN --> ACCESS["API calls в рамках effective permissions"]
  USER --> WARN["Super admin в учебном рецепте — не production default"]
```

Источник на p416 предлагает отключить expiry, но p417 сам рекомендует разумный срок и ротацию.

## 2. API host.get → host/IP file ([p0418](../../../rag/chunks/p0401-p0500/p0418-c01.md)–[p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md))

```mermaid
flowchart LR
  PY["Python requests + API token"] --> RPC["POST JSON-RPC 2.0: host.get"]
  RPC --> ZBX["Zabbix API: hostid/host/interfaces"]
  ZBX --> FILTER["Отбор interfaces с main = 1"]
  FILTER --> FILE["generate_host_file: hostname + IP"]
  FILE --> RESULTS["Учебный текстовый файл results"]
```

В тексте разнится `/home/zabbix/results` vs `/home/results`; API-read и локальная запись имеют разные последствия.

## 3. Jumphost: превращение данных мониторинга в системное состояние ([p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md)–[p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md))

```mermaid
flowchart TD
  API["host.get + IP interfaces"] --> SCRIPT["Внешний host_pull_zabbix.py"]
  SCRIPT --> HOSTS["Перезаписать целиком /etc/hosts"]
  HOSTS --> SSH["SSH по именам из Zabbix"]
  CRON["*/15 cron"] --> SCRIPT
  HOSTS --> RISK["Риск утраты существующих локальных имен"]
  RISK --> NEED["Backup + rollback / code review: Needs confirmation"]
```

В источнике прямо указано, что перезапись `/etc/hosts` полная, поэтому использование на реальном бастионе без защиты запрещено как учебное допущение.

## 4. Map UI → elevated execution boundary ([p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)–[p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md))

```mermaid
flowchart TD
  USER["User role (низкие права)"] --> MAP["Monitoring → Maps → target host"]
  MAP --> MENU["Host/Enable или Host/Disable"]
  MENU --> EXEC["Execute Zabbix custom script"]
  EXEC --> PRIV["Другой пользователь с повышенными правами"]
  PRIV --> PY["enable_disable-host.py (внешний код, RAG_MISS)"]
  PY --> API["Zabbix API"]
  API --> STATUS["Observed host Disabled / Enable"]
  API --> MAINT["В тексте также упомянут maintenance period"]
  STATUS --> QUESTION["Не установлено, одинаков ли фактический эффект"]
  MAINT --> QUESTION
```

Скриншоты 10.18–10.19 не позволяют построить подтверждённую точную команду, а фактический вид API change без загрузки скрипта неизвестен.

## 5. Manual input увеличивает изменяемую область ([p0432](../../../rag/chunks/p0401-p0500/p0432-c01.md)–[p0433](../../../rag/chunks/p0401-p0500/p0433-c01.md))

```mermaid
flowchart TD
  BEFORE["Script command: {HOST.HOST}"] --> AFTER["Script command: {MANUALINPUT}"]
  AFTER --> PROMPT["Input prompt / Default string"]
  PROMPT --> VALIDATE["Input validation rule: значение на рисунке = RAG_MISS"]
  VALIDATE --> TARGET["Введённый вручную target host"]
  TARGET --> EXEC["Привилегированное действие"]
  TARGET --> RISK["Нужна проверка authorization на конечном host"]
```

## 6. Общая последовательность диагностики

```mermaid
flowchart TD
  BEGIN["Пользователь / группа / API token"] --> READ["read-only host.get"]
  READ --> CHECK["Hostid, интерфейс, IP, фильтрация"]
  CHECK --> DECIDE{"Требуется изменение состояния?"}
  DECIDE -- "Нет" --> OUTPUT["Только файл результатов в lab"]
  DECIDE -- "Да" --> REVIEW["Code review + scope + backup + approval"]
  REVIEW --> MODIFY["Jumphost/Map action, только в контролируемой среде"]
  MODIFY --> VERIFY["Статус host, сохранность /etc/hosts, журнал"]
```

Расхождения строк, токены и критичные изменения из источника — [source-findings.md](source-findings.md).
