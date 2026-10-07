# Commands and tools — глава 4 (RAG-only, safe classification)

Источник: PDF pp. 72–98, `p0072:c01` … `p0098:c01`. Здесь перечислены **только команды и инструменты, явно названные в книге**. Ни один пример с чужим доменом/адресом из книги не является разрешением запускать его. Пользователь не предоставил target/authorization: **[Needs confirmation]**. Все угловые placeholders ниже — **редакционная маскировка конкретной цели**, а не исходные аргументы.

## 1. Прямо показанные команды/формы

| Форма из главы (либо с явной подстановкой target) | Класс | Возможный эффект и источник |
| --- | --- | --- |
| `whois <AUTHORIZED_DOMAIN>` | **workload-generating** (запрос к реестру), изменение конфигурации цели не предполагается | В книге: `whois wiley.com`, PDF p. 75–77; исторические регистрационные поля могут быть скрыты |
| `whois <AUTHORIZED_IP>` | **workload-generating** (WHOIS lookup) | В книге: `whois 63.97.119.2`, p. 78–79; адресной блок в источнике имеет противоречивую запись, см. source-findings |
| `theHarvester -d <AUTHORIZED_DOMAIN> -b bing` | **workload-generating** (поиск внешних источников) | В книге: `theHarvester -d wiley.com -b bing`, p. 80; пример даёт хосты, не гарантируя email/IP |
| `sherlock --fo smithsearch <AUTHORIZED_USERNAME_1> <AUTHORIZED_USERNAME_2>` | **workload-generating** (проверки множества сторонних сайтов) | На p. 82 исходный вариант включает `jsmith smith johnsmith`; вывод не подтверждает личность; `--fo` сохранён **как в RAG**, семантика и доступность флага [Needs confirmation] |
| `host <AUTHORIZED_FQDN>` | **workload-generating** (DNS) | Источник `host www.sybex.com` и reverse lookup `host 208.215.179.132`, p. 84 |
| `host <AUTHORIZED_FQDN> <APPROVED_DNS_SERVER>` | **workload-generating** (DNS к выбранному серверу) | Источник `host www.sybex.com 4.2.2.1`, p. 84 |
| `nslookup` → `set type=ns` → `<AUTHORIZED_DOMAIN>` | **workload-generating** (интерактивные DNS-запросы) | p. 85, в источнике пример для `sybex.com`; `set type=A` и `server <APPROVED_DNS_SERVER>` — смена типа и сервера внутри процесса |
| `dig mx <AUTHORIZED_DOMAIN> @<APPROVED_DNS_SERVER>` | **workload-generating** (DNS) | p. 86: источник `dig mx wiley.com @car-ibextdns-01.wiley.com` |
| `dig axfr <AUTHORIZED_DOMAIN> @<APPROVED_AUTHORITATIVE_NS>` | **workload-generating, sensitive** (запрос передачи целой DNS-зоны) | p. 87: источник `dig axfr domain.com @192.168.86.51`; запрос может раскрыть множество внутренних имён. **Не применять к сторонним зонам без согласования** |
| `dnsrecon -d <AUTHORIZED_DOMAIN> -D <APPROVED_WORDLIST> -t brt` | **workload-generating, increased traffic** (wordlist-перебор DNS-имён) | p. 87: источник использует `-D /usr/share/wordlists/dnsmap.txt`; лимит запросов/нагрузки не указан |
| `ipconfig /displaydns` | **read-only local check** | p. 88–89: читает кэш DNS в Windows; не является запросом к внешнему DNS |
| `httrack` | **workload-generating, potentially high** | p. 94: интерактивное зеркало веб-сайта; запросы множества файлов; глубина/лимиты/политика запроса [Needs confirmation] |

**Примечание:** строка `sherlock --fo ...` приведена только как запись источника, без предположения, что этот флаг работает в актуальной версии Sherlock. Формы с `<PLACEHOLDER>` не являются автоматически готовым production-command. **Версия утилиты и успешность запуска не проверялись.**

## 2. Концептуальные и браузерные инструменты

| Инструмент или запись из источника | Класс | RAG |
| --- | --- | --- |
| EDGAR, SEC, регистраторы/RIR WHOIS, публичные отчёты | Чтение публичных материалов; веб-доступ генерирует запрос | `p0073:c01`–`p0079:c01` |
| Maltego, CrossLinked, Spokeo/PeekYou и другие поисковики людей | Внешние обращения, обработка персональных данных; точных CLI-команд нет | `p0081:c01` |
| `p0f` (пассивное наблюдение трафика интерфейса) | **read-only observation** после разрешения на capture; отдельная команда/аргументы отсутствуют | `p0091:c01` |
| Wireshark, browser Recon plugin, Wappalyzer, Netcraft, DevTools | Наблюдение/изучение веб-технологий; посещение сайтов создаёт трафик | `p0091:c01`–`p0093:c02` |
| Google keywords `inurl:`, `intext:`, `site:`, `filetype:`, `link:` | Поисковый запрос к сервису; синтаксис операторов подтверждён на p. 95/98; конкретная актуальная поддержка [Needs confirmation] | `p0095:c01`, `p0098:c01` |
| Shodan | Поиск индексированных устройств/IoT; CLI синтаксиса нет, доступ/достоверность [Needs confirmation] | `p0096:c01`–`p0097:c01` |

## 3. State-changing действия

**[Not applicable] для подтверждённых исполняемых source-команд.** В пределах главы отсутствует приведённая конфигурационная команда изменения удалённой среды; однако сетевой трафик, загрузка сайта и сбор данных **не равны read-only network observation**. При массовом запросе возможна нагрузка на целевую службу.

**Effect:** DNS/WHOIS/HTTP-запросы, обращение к поисковым API и возможная генерация множества записей на удалённых системах. **Risks:** превышение rate-limit, раскрытие проверяемых идентификаторов, нарушение допустимого scope/политики сервиса. **Verification:** только в согласованной лаборатории или после утверждения задачи; критерии в исходнике [Needs confirmation]. **Rollback:** [Needs confirmation] — сетевые запросы нельзя «отменить». **Секреты/API-ключи:** не приводятся.
