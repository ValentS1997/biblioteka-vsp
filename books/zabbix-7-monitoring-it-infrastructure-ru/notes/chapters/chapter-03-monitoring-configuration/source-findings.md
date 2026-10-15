# Глава 3 — source findings (RAG-only)

Эти наблюдения извлечены из адресуемых RAG-chunks PDF **93–160**. Классификации не означают, что внешний продукт проверен на текущую дату. Здесь **сохраняются исходные варианты**, дефекты и пропуски; автоматическая коррекция кода/команд по памяти модели или интернету запрещена.

## 1. [Source code mismatch] Browser: опечатка в названии службы при перезапуске

- **Вариант источника A:** в рецепте browser item после изменения `WebDriverURL` и `StartBrowserPollers` написано `systemctl restart zabbbix-server` (три `b`) — [`zabbix-7-monitoring-it-infrastructure-ru:p0144:c01`](../../../rag/chunks/p0101-p0200/p0144-c01.md).
- **Вариант источника B:** в рецепте JMX (и ранее в главе 1) написано `systemctl restart zabbix-server` — [`zabbix-7-monitoring-it-infrastructure-ru:p0134:c01`](../../../rag/chunks/p0101-p0200/p0134-c01.md).
- **Решение:** оба фрагмента сохранены. Первый **не рекомендован к исполнению**; даже если второй выглядит правдоподобным, окончательную команду для конкретного хоста перед restart следует проверить отдельно. Не перезапускать несуществующую/не ту службу.

## 2. [Source wording/code mismatch] Для Ubuntu в browser-рецепте приведён `dnf`

- **Вариант A:** `Для систем на базе RHEL: dnf install docker-ce`.
- **Вариант B:** `Для Ubuntu: dnf install docker-ce` — [`zabbix-7-monitoring-it-infrastructure-ru:p0144:c01`](../../../rag/chunks/p0101-p0200/p0144-c01.md).
- **Контекст внутри главы:** при установке других пакетов для Ubuntu используется `apt install` ([`zabbix-7-monitoring-it-infrastructure-ru:p0094:c01`](../../../rag/chunks/p0001-p0100/p0094-c01.md), [`zabbix-7-monitoring-it-infrastructure-ru:p0134:c01`](../../../rag/chunks/p0101-p0200/p0134-c01.md), [`zabbix-7-monitoring-it-infrastructure-ru:p0136:c01`](../../../rag/chunks/p0101-p0200/p0136-c01.md)).
- **Решение:** нельзя без подтверждения подменять авторскую строку на выбранную по общим знаниям. Указание на несовпадение обязательно до установки Docker; корректная команда = `[Needs confirmation]`.

## 3. [Source code mismatch] Несогласованность файлов ODBC DSN и описания драйвера

- **Вариант A:** `odbcinst -j` в книге перечисляет `DRIVERS: /etc/odbcinst.ini` и `SYSTEM DATA SOURCES: /etc/odbc.ini` — [`zabbix-7-monitoring-it-infrastructure-ru:p0136:c01`](../../../rag/chunks/p0101-p0200/p0136-c01.md).
- **Вариант B:** p137 сначала редактирует `/etc/odbc.ini` для `[book]` (DSN), а затем снова предлагает `vim /etc/odbc.ini` для просмотра `[MariaDB]`, `Driver=/usr/lib/libmaodbc.so` и `Driver64=/usr/lib64/libmaodbc.so` — [`zabbix-7-monitoring-it-infrastructure-ru:p0137:c01`](../../../rag/chunks/p0101-p0200/p0137-c01.md).
- **Решение:** сохраняем разные путевые указания и не утверждаем, что один из вариантов ошибочен именно на установленной системе. Точное расположение driver config проверяется `odbcinst -j` **на целевой машине**. Работоспособность DSN — через `isql -v book`; не применять запись в файл по догадке.

## 4. [Source wording/code mismatch] Ключ simple check, не подтверждённый отдельной текстовой конфигурацией

- **Вариант A:** текст RAG p116 содержит `net.tcp.services[ssh,,22]` (множественное `services`) — [`zabbix-7-monitoring-it-infrastructure-ru:p0116:c01`](../../../rag/chunks/p0101-p0200/p0116-c01.md).
- **Вариант B:** подробные поля item только на рисунке 3.30 (p117), который не выделен в отдельный RAG-объект — [`zabbix-7-monitoring-it-infrastructure-ru:p0117:c01`](../../../rag/chunks/p0101-p0200/p0117-c01.md).
- **Решение:** нельзя по памяти заменять `services` на другое написание, даже если название выглядит подозрительным. Для воспроизводимого item key требуется `[Needs confirmation]`; в памятке он приведён как *строка источника*, не проверенная командная форма.

## 5. [Needs confirmation] Пример JMX отключает защиту и использует старую тестовую платформу

- **Текст:** p133 предлагает тестовый CentOS 7/Tomcat и `-Dcom.sun.management.jmxremote.authenticate=false`, `-Dcom.sun.management.jmxremote.ssl=false`, порт `12345` — [`zabbix-7-monitoring-it-infrastructure-ru:p0133:c01`](../../../rag/chunks/p0101-p0200/p0133-c01.md).
- **Контекст:** это учебная демонстрация; source не даёт защищённой альтернативной настройки JMX (пароли, TLS, firewall-policy, rollback). Следовательно, эти параметры **не** становятся рекомендуемой production-конфигурацией. Безопасный вариант = `[Needs confirmation]`.

## 6. [Needs confirmation] Широкое разрешение удалённой команды у Zabbix Agent 2

- **Текст:** для работающего примера preprocessing p155 требует `AllowKey=system.run[*]` в `/etc/zabbix/zabbix_agent2.conf`, чтобы выполнить удалённую CLI-команду — [`zabbix-7-monitoring-it-infrastructure-ru:p0155:c01`](../../../rag/chunks/p0101-p0200/p0155-c01.md).
- **Контекст:** разрешается очень широкое выполнение команд, источник не описывает узкую политику AllowKey и полный rollback. Не рекомендовать эту строку вне контролируемой учебной среды. Безопасная альтернатива = `[Needs confirmation]`.

## 7. [Source wording/code mismatch] Secret text скрывает значение, но не шифрует хранение

- **Вариант A:** макросы SNMP предлагается установить с типом `Secret text` — [`zabbix-7-monitoring-it-infrastructure-ru:p0105:c01`](../../../rag/chunks/p0101-p0200/p0105-c01.md).
- **Вариант B:** на той же странице прямо сказано, что эти макросы хранятся в БД Zabbix **нешифрованными**, а полноценная защита требует внешнего хранилища.
- **Решение:** не называть Secret text шифрованием; это ограничение отображения в UI. Конкретный вариант внешнего vault не реализован в главе и остаётся `[Needs confirmation]`.

## 8. [Needs confirmation] Неполные значения на рисунках и внешний JS

- **Точные поля** SNMP dependent/preprocessing (p111–p112), формулы calculated item (p124), master/dependent SQL (p125–p128), HTTP JSONPath (p141–p142), browser macros/dependent JSONPath (p145–p149) и regex из p157 показаны в рисунках, не извлечены как отдельные данные RAG → `RAG_MISS`.
- **Файл browser script:** текст книги даёт ссылку на Packt GitHub (p144–p145) и цитирует отдельные JS-фрагменты (p150–p152); полный внешний файл здесь **не извлечён и не загружен**. При RAG-only нельзя объявлять работоспособным целостный скрипт, реконструированный из обрывков.
- **Контейнер Selenium:** p144 использует `selenium/standalone-chrome:latest` и публикует порты `4444/7900`; безопасность конкретного образа/сети, воспроизводимая версия и rollback **не проверены**. Производственную применимость не утверждать.

## 9. [Needs confirmation] Полный rollback отсутствует

Установка агентов/драйверов, создание SNMPv3 identity, ODBC DSN, external script, trapper values, JMX/Brower services и изменение `AllowKey` не сопровождаются единым проверенным обратным сценарием в главе. Для каждой такой операции rollback = `[Needs confirmation]`. Это **не доказанное противоречие**, а пробел источника для практической эксплуатации.

**Отдельного итога и контрольных вопросов нет:** [p0160](../../../rag/chunks/p0101-p0200/p0160-c01.md) заканчивает раздел предварительной обработки; на [p0161](../../../rag/chunks/p0101-p0200/p0161-c01.md) начинается глава 4. Поэтому необязательные chapter-end артефакты не создаются.
