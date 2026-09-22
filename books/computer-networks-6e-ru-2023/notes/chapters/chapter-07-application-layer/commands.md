# Команды и инструменты главы 7

| Команда / инструмент | Назначение | Что проверить | Тип |
|---|---|---|---|
| `dig ns @a.edu-servers.net cs.uchicago.edu` | Выполнить DNS-запрос к указанному name server | Ответ с информацией о name servers для домена, соответствующий шагу DNS resolution example | workload-generating |
| `telnet mail.isp.com 25` | Открыть TCP-соединение с SMTP service на порту 25 | SMTP greeting и возможность интерактивно наблюдать SMTP protocol dialogue | workload-generating |

## `dig`

Раздел 7.1.6 прямо предлагает использовать `dig` для практического изучения DNS resolution.

Команда:

```text
dig ns @a.edu-servers.net cs.uchicago.edu
```

отправляет DNS-запрос на `a.edu-servers.net` и выводит ответ.

Эффект: создается реальный DNS query traffic.

Эксплуатационные rate limits или ограничения источником не заданы: [Needs confirmation].

## `telnet` к SMTP

Раздел 7.2 предлагает UNIX/Linux-команду:

```text
telnet mail.isp.com 25
```

с заменой `mail.isp.com` на DNS-имя почтового сервера.

Эффект: устанавливается реальное TCP-соединение с SMTP port 25.

Источник предупреждает, что не каждый mail server разрешает telnet-соединение от неизвестного компьютера и что idle connection может быть закрыт.

После установления соединения глава предлагает protocol command `HELP` для просмотра доступных SMTP commands. Это command внутри SMTP session, а не shell-команда.

## Protocol commands

В chapter RAG показан SMTP dialogue с `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`, а также ESMTP `EHLO`.

Эти команды могут участвовать в реальной отправке сообщения и потому не переносятся в canonical operational table как безопасные read-only действия.

## Не подтверждены для главы

В качестве chapter-specific operational CLI не подтверждены `nslookup`, `curl`, `wget`, `openssl`, `tcpdump` и другие типичные инструменты. Они не добавлены из общих знаний.
