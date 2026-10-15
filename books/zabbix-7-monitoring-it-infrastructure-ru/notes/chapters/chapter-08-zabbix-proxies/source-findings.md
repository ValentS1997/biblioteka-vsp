# Глава 8 — source findings: противоречия, риски и RAG_MISS

Основание: **RAG-only PDF 336–370**. Варианты исходника фиксируются **как источник**, без молчаливой коррекции внешним знанием, реконструкции рисунков или удаления спорной формулировки.

## 1. [Source code mismatch] Слитые аргументы `chmod` и регистр `Systemctl` в PSK

- **Вариант A (p354):** `chmod 400/etc/zabbix/proxy_psk.key` не отделяет числовую маску прав от пути пробелом; команда в буквальном виде не соответствует обычному синтаксису из двух аргументов. Кроме того, `Systemctl restart zabbix-proxy` начинается с заглавного `S` — [p0354](../../../rag/chunks/p0301-p0400/p0354-c01.md).
- **Вариант B:** рядом p354 записано `chown zabbix:zabbix /etc/zabbix/proxy_psk.key`; ранее p339 используется `systemctl enable zabbix-proxy` и `systemctl start zabbix-proxy` со строчными буквами — [p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md).
- **Решение:** сохранить оба literal источника, **не выдавать сломанные строки за проверенные команды** и не исправлять их молча. Утверждение о реальных file permissions/отсутствии секретов в логах и корректная процедура рестарта = `[Needs confirmation]`.

## 2. [Source code mismatch] `Zabbix-proxy` с заглавной буквы как service unit

- **Вариант A:** в разделе активного proxy [p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md) написано `systemctl restart Zabbix-proxy`.
- **Вариант B:** инсталляционная инструкция [p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md) использует `systemctl start zabbix-proxy` (строчное `zabbix-proxy`). В PSK разделе [p0354](../../../rag/chunks/p0301-p0400/p0354-c01.md) написано `Systemctl restart zabbix-proxy`.
- **Решение:** неверные/несогласованные варианты написания systemctl и unit не переносить в автоматизацию; фактическое имя unit на установленном целевом Linux и restart / rollback = `[Needs confirmation]`.

## 3. [Destructive / source risk] Удаление SQLite файла прокси разрушает ещё не доставленные метрики

- **Исходная команда:** `rm /tmp/zabbix_proxy.sqlite3` рекомендована авторами как способ решения проблем SQLite — [p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md).
- **Непосредственное уточнение:** [p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md) прямо предупреждает, что proxy DB служит кэшем и может содержать **несинхронизированные метрики**, которые будут потеряны при удалении.
- **Вывод:** фразу «можно просто удалить» нельзя превращать в безопасную инструкцию обслуживания. Перед любой операцией требуется подтверждение загрузки накопленных данных, backup, локальная политика восстановления. **Полное восстановление неопубликованных измерений** в тексте `[Needs confirmation]`.
- Дополнительно **`DBName=/tmp/zabbix_proxy.sqlite3`** — учебный путь p338, а поведение `/tmp` и политика долговременного хранения в production не подтверждены исходником.

## 4. [Destructive / source risk] Буфер в памяти и гибридный режим

- Текст [p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md) различает hybrid (новые установки), memory и disk (старые установки) и говорит, что hybrid при рестарте переносит значения в DB, а memory-only может потерять их.
- При этом время retention задаётся `ProxyOfflineBuffer`, для которого [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md) приводит **default 1 час**.
- **Вывод:** «прокси собирает данные при обрыве связи» **не означает гарантированное отсутствие потерь**. Точные условия flush, shutdown/crash, disk capacity, filesystem и реальный режим в целевой версии = `[Needs confirmation]`.

## 5. [Sensitive operational detail] Вывод секретного PSK на экран

- [p0353](../../../rag/chunks/p0301-p0400/p0353-c01.md) генерирует ключ через `openssl rand -hex 128 > /etc/zabbix/proxy_psk.key` и предлагает проверить содержимое через `cat /etc/zabbix/proxy_psk.key`.
- [p0354](../../../rag/chunks/p0301-p0400/p0354-c01.md) требует ограничения доступа к этому файлу; [p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md) признаёт риск утечки и отсутствие встроенного срока истечения PSK.
- **Вывод:** не публиковать значение ключа в Git, терминальных логах, скриншотах, чатах или документах. Источник **не содержит** политики ротации, безопасного распространения секрета, проверки file permissions без чтения PSK и безостановочного cutover — `[Needs confirmation]`.

## 6. [Security-sensitive] Permissive SELinux / отключение AppArmor и отсутствие TLS

- [p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md) предлагает включить permissive SELinux либо разрешить proxy в SELinux, а для Ubuntu в lab допускает отключение AppArmor. [p0342](../../../rag/chunks/p0301-p0400/p0342-c01.md)/[p0346](../../../rag/chunks/p0301-p0400/p0346-c01.md) оставляют `No encryption` для первых примеров.
- [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md) объясняет, что секретные macros передаются открытым текстом без шифрования server↔proxy.
- **Вывод:** лабораторные упрощения не следует считать безопасными настройками production. Корректный SELinux/AppArmor policy/TLS режим и сетевые правила требуют `[Needs confirmation]`.

## 7. [Destructive / unsafe migration] Удаление существующих hosts при переносе Discovery

- [p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md) предлагает удалить `lar-book-disc-lnx` и `lar-book-disc-win` «для избежания дублирования». [p0362](../../../rag/chunks/p0301-p0400/p0362-c01.md) аналогично предлагает удалить `lar-book-lnx-agent-auto`, затем перенаправить `ServerActive` на proxy.
- **Риск:** потеря конфигурации, привязок, исторических данных/доступности в управляемой инфраструктуре. Источник не подтверждает, что переназначение Discovery без удаления невозможно; это **учебный сценарий**, не универсальный migration playbook.
- **Вывод:** не повторять удаление на production; перед миграцией проверять зависимости, backup, историю и идентификаторы. Undo/восстановление `[Needs confirmation]`.

## 8. [Source ambiguity] `ServerActive` с несколькими адресами и совет указывать один proxy

- [p0358](../../../rag/chunks/p0301-p0400/p0358-c01.md) демонстрирует `ServerActive=192.168.2.175,192.168.2.174` **для proxy group** с двумя proxy.
- [p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md) говорит, что для авторегистрации/Discovery нужно указывать в `ServerActive` только **тот proxy**, куда нужно передавать данные, поскольку агент будет пытаться работать со всеми перечисленными.
- **Интерпретация:** разные сценарии (HA proxy group против single proxy discovery) могут объяснять разницу; **не утверждать**, что варианты эквивалентны и рекомендованы для одного режима. Реальная маршрутизация в конкретной конфигурации = `[Needs confirmation]`.

## 9. [Source wording/code mismatch] Путь Zabbix Agent 2 на Windows

- В главе 8 [p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md) фигурирует `C:\Program Files\Zabbix agent\zabbix_agent2` без прежнего `.conf`.
- В предыдущей главе 7 [p0292](../../../rag/chunks/p0301-p0400/p0292-c01.md) фигурирует `C:\Program Files\Zabbix Agent 2\zabbix_agent2.conf`; оба источниковых пути имеют различия в имени каталога и расширении файла.
- **Решение:** не переносить путь p361 как гарантированный Windows config путь; фактический путь программы/config и stop/start агента = `[Needs confirmation]`.

## 10. [Needs confirmation] Скриншотные поля и режимы proxy HA

- `Administration → Proxies` (p341–347), `Encryption` (p354), proxy group UI/threshold/failover (p356–360), `Remote Zabbix proxy health` macros (p366–367) показаны рисунками, поля/значения которых не представлены отдельно в text chunks.
- Из текста подтверждаются `ProxyMode`, `Hostname`, `Server`, `DBName`, `ProxyBufferMode`, `TLSConnect`, `TLSAccept`, `TLSPSKIdentity`, `TLSPSKFile`, `StatsAllowedIP`, `Minimum number of proxies`, `Failover period`, `Address for active agents`. Полный UI payload для конкретного proxy/группы = `RAG_MISS`.
- Failover SNMP trapper [p0360](../../../rag/chunks/p0301-p0400/p0360-c01.md) может потребовать доставки traps на все group members и создать нагрузку; конфигурация без проверки = `[Needs confirmation]`.

## 11. [Needs confirmation] Нет chapter-end вопросов и процедур отката

[p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md) заканчивается объяснением категорий proxy queue, [p0371](../../../rag/chunks/p0301-p0400/p0371-c01.md) начинает следующую главу. Отдельных `summary`, `review questions` или ответов нет. Условные файлы не создаются. **Не даны** восстановление удалённой SQLite DB и данных из RAM, возвращение уже удалённых hosts, rollback PSK и HA group: `[Needs confirmation]`.
