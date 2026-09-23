# Команды главы 19

Только команды и формы команд, подтвержденные RAG главы 19.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| curl -s -v -o /dev/null http://<host> | Посмотреть HTTP request/response headers и status без сохранения payload | DNS/connect, Host, status, response headers | read-only |
| curl -H "Host: <vhost>" -s -v -o /dev/null <IP> | Проверить name-based virtual host напрямую по IP | тот же virtual host/status/content metadata без DNS path | read-only |
| curl -O <URL> | Скачать remote object в текущий каталог | имя/размер загруженного файла | state-changing |
| curl -H "Cache-Control: no-cache" <URL> | Запросить cache revalidation при диагностике stale content | сравнить ответ cache layer с origin | workload-generating |
| curl <API-URL> \| jq '.' | Получить JSON API response и отформатировать jq | HTTP success и ожидаемая JSON structure | read-only |
| apachectl start | Запустить Apache с default configuration | syntax check из wrapper и daemon start | state-changing |
| apachectl status | Показать состояние Apache | running state/PID | read-only |
| httpd -t | Проверить Apache configuration syntax | Syntax OK / ошибки config | read-only |
| apachectl graceful | Дождаться закрытия активных connections и graceful reload | новые workers/config без разрыва текущих connections | state-changing |
| apachectl -f <config> -k start | Запустить Apache с явно указанным config file | используется intended config; server starts | state-changing |
| a2enmod <module> | Включить Apache module в Debian/Ubuntu-style hierarchy | symlink/module enabled | state-changing |
| a2dismod <module> | Отключить Apache module | symlink/module disabled; dependencies understood | state-changing |
| htpasswd -c /var/www/.htpasswd <user> | Создать password file и account для Basic Auth | user entry created | state-changing |
| cat /var/www/.htpasswd | Просмотреть htpasswd file из примера | ожидаемая account entry; не публиковать hashes | read-only |
| chown www-data /var/www/.htpasswd | Назначить владельца password file | owner соответствует web-server account | state-changing |
| chmod 600 /var/www/.htpasswd | Ограничить доступ к password file | only owner read/write | state-changing |
| nginx -t | Проверить syntax NGINX configuration | syntax successful before reload/start | read-only |
| nginx -c <config> | Запустить NGINX с alternate configuration file | intended config loaded | state-changing |
| cat /etc/ssl/{private/<site>.key,certs/<site>.crt} > /etc/ssl/private/<site>.pem | Создать combined key/certificate PEM для HAProxy | bundle содержит key+certificate; destination protected | state-changing |
| chmod 400 /etc/ssl/private/<site>.pem | Ограничить permissions HAProxy PEM | readable only by intended owner | state-changing |
| ls -l /etc/ssl/private/<site>.pem | Проверить ownership/mode PEM | restrictive permissions and correct owner | read-only |

## HTTP / curl baseline

Verbose GET:

~~~bash
curl -s -v -o /dev/null http://<host>
~~~

Check:
- connection endpoint;
- request line and Host header;
- HTTP status;
- response headers such as Server, Content-Type, Content-Length and cache metadata.

Virtual host without DNS:

~~~bash
curl -H "Host: <vhost>" -s -v -o /dev/null <IP>
~~~

This is a read-only diagnostic request only to the extent that the remote application treats GET safely; the chapter notes that HTTP method semantics ultimately depend on server-side software.

## Cache diagnosis

Compare layers directly:

~~~text
origin
→ reverse proxy/cache
→ other cache layers
~~~

Request revalidation:

~~~bash
curl -H "Cache-Control: no-cache" <URL>
~~~

Do not assume revalidation succeeded until the response is compared with the origin.

## Apache

Safe precondition:

~~~bash
httpd -t
~~~

Operational commands shown by the chapter:

~~~bash
apachectl start
apachectl status
apachectl graceful
apachectl -f <config> -k start
~~~

graceful waits for current connections to close before reloading.

Module control in Debian/Ubuntu-style layout:

~~~bash
a2enmod <module>
a2dismod <module>
~~~

Exact rollback of an arbitrary module/config change is [Needs confirmation]; disabling a module is only an inverse action when dependencies and site configuration permit it.

## Apache Basic Auth

Create the account file:

~~~bash
htpasswd -c /var/www/.htpasswd <user>
~~~

Then protect it:

~~~bash
chown www-data /var/www/.htpasswd
chmod 600 /var/www/.htpasswd
~~~

Risk:
- Basic Auth credentials are not confidential unless transported over HTTPS;
- even hashed password files should not be broadly readable.

Rollback for account-file changes: [Needs confirmation].

## NGINX

Syntax check:

~~~bash
nginx -t
~~~

Alternate configuration:

~~~bash
nginx -c <config>
~~~

The chapter documents signals TERM/INT, QUIT, USR1, HUP and USR2 for the master process, including HUP for configuration reload, but does not provide a canonical shell command for sending them. Do not invent one here.

Rollback for NGINX config changes: [Needs confirmation].

## HAProxy TLS bundle

HAProxy example expects key and certificate in one PEM:

~~~bash
cat /etc/ssl/{private/<site>.key,certs/<site>.crt} > /etc/ssl/private/<site>.pem
chmod 400 /etc/ssl/private/<site>.pem
ls -l /etc/ssl/private/<site>.pem
~~~

If HAProxy runs as a non-root identity, ownership must match the identity that needs to read the key.

This operation creates sensitive key material in a new file. Secure ownership and permissions are part of the acceptance check.

Rollback/removal procedure for the generated PEM: [Needs confirmation].
