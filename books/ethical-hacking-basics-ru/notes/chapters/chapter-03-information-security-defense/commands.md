# Commands and tools — глава 3 (RAG-only)

**Source scope:** PDF pp. 43–71; `ethical-hacking-basics-ru:p0043:c01` … `p0071:c01`. Все команды ниже взяты из конкретных адресуемых chunks, а не дополнены из памяти. **Примеры изменения firewall — только цитаты для анализа; не выполнять на действующей системе.**

## 1. Source-confirmed state-changing: firewall default policy

Источник: PDF **p. 54**, `p0054:c01`. Три строки в книге даны под подписью `[iptables Policy Settings]`.

```bash
# SOURCE EXAMPLE — НЕ ВЫПОЛНЯТЬ БЕЗ ОКНА ИЗМЕНЕНИЙ И RECOVERY PATH
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```

- **Класс:** state-changing.
- **Эффект по источнику:** политика по умолчанию `DROP` для входящих, исходящих и пересылаемых пакетов, не разрешённых ранее правилами.
- **Риск:** отключение управляющего доступа, нарушенная связность, недоступность служб, включая трафик существующих рабочих процессов. Это следует из политики отброса пакетов и зависимостей соединений; **не результат теста**.
- **Verification/acceptance:** [Needs confirmation] — в главе не указан read-only способ просмотра текущего ruleset, защищённый management path или критерии доступности.
- **Rollback:** [Needs confirmation] — источник не задаёт проверенный обратный порядок/команды.
- **Precondition:** разрешённая система, её интерфейсы, текущее состояние фильтрации, out-of-band console/recovery и окно изменения — [Needs confirmation].
- Нельзя считать эти три команды полноценной конфигурацией firewall.

## 2. Source-confirmed state-changing: примеры stateful TCP/22

Источник: PDF **p. 55**, `p0055:c01`; подпись `[iptables State Rules]`. Сохранены исходные строки *без замены синтаксиса*; `eth0` — **только идентификатор из книжного примера**, не подтверждённый интерфейс пользовательской среды.

```bash
# SOURCE EXAMPLE — НЕ ВЫПОЛНЯТЬ БЕЗ ПРОВЕРКИ ПОРЯДКА ПРАВИЛ
iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
```

- **Класс:** state-changing.
- **Эффект по источнику:** добавление правил для входящего TCP/22 и соответствующего исходящего TCP-трафика при указанных состояниях `NEW,ESTABLISHED` / `ESTABLISHED`.
- **Риск:** неверный интерфейс/порядок, неполный allowlist, действие общей default policy, неожиданная потеря доступа.
- **Verification / rollback:** [Needs confirmation] — исходник не определяет команды просмотра, безопасного удаления, гарантированного возврата и внешнего доступа.

## 3. Иные source-mentioned инструменты/примеры

| Инструмент, действие или фрагмент | Класс | Что подтверждено | Источник |
| --- | --- | --- | --- |
| `auditctl` | **state-changing** при установке правил; параметры отсутствуют | В Linux можно добавлять правила аудита в командной строке; точная команда не показана | `p0069:c01`, `p0070:c01` |
| `cat audit.log` | **read-only**, но это лишь запись аудита о ранее выполнявшейся программе | В фрагменте `type=EXECVE` переданы аргументы `a0="cat" a1="audit.log"`; это **не инструкция запускать команду** | `p0070:c01` |
| syslog | **наблюдение**; пересылка/конфигурация — state-changing | Локальная/центральная запись, time/host/process/message, severity, варианты направлений хранения | `p0067:c01`–`p0068:c01` |
| Windows Event Viewer / Event ID | **read-only observation** при просмотре; аудит policy — state-changing | System/Security/Application; пример Event ID `4689` как завершение процесса; настройка success/failure auditing | `p0068:c01`–`p0069:c01` |
| ModSecurity `SecRule RESPONSE_BODY "@rx ..."` | **state-changing** при размещении в конфигурации WAF | Regex для распознавания упоминаний ошибок SQL в теле ответа; многострочный пример повреждён переносами RAG | `p0056:c01` |
| Snort `alert tcp ...` и `pcre` | **config-changing** при включении; alert в примере генерирует наблюдение | Сигнатура: action/protocol/src-dst/port, `msg`, `flow`, `pcre`, `sid`, `rev`; длинные строки извлечены с разрывами | `p0058:c01`, `p0058:c02` |
| Snort / Suricata IDS | **наблюдение**; IPS inline — может блокировать | NIDS, размещение сенсоров, alert; при inline режиме IPS возможен `drop/reject` | `p0057:c01`–`p0059:c01` |
| EDR / Google Rapid Response (GRR) | **наблюдение** либо **state-changing** (изоляция) | Удалённый сбор процессов, памяти, логов/артефактов; возможна изоляция хоста | `p0060:c01`–`p0061:c01` |
| SIEM / ELK | **наблюдение / корреляция**; конфиг не представлен | Корреляция событий, поиск и визуализация нескольких источников | `p0062:c01`–`p0063:c01` |

## 4. Чего **нет** в source RAG

- Нет команды чтения действующей firewall policy, проверенного preflight и smoke-test после изменения.
- Нет полного безопасно-воспроизводимого конфигурационного листинга WAF/Snort: длинные `SecRule` / `pcre` визуально разорваны при текстовом извлечении. **Не нормализовывать их как действующий конфиг** без отдельной верификации.
- Нет параметров `auditctl` для безопасного изменения/удаления, и нет rollback plan.
- Нет подтверждённого адреса/узла, привилегий, backup state или out-of-band channel.

**Run permission:** [Needs confirmation]. **Expected output:** [Needs confirmation]. **Rollback:** [Needs confirmation]. Это справочник примеров источника, а не change ticket.
