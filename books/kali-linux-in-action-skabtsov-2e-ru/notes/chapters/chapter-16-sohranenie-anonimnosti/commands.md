# Инструменты и влияние — глава 16 «Сохранение анонимности»

**Canonical RAG:** `p0361:c01`–`p0374:c01` (PDF 361–374), source SHA-256 `fa3cfb6d7dc9af0354a5c908e606626629929ae54b646ca4eaaa11b7868eb1b9`. Исходник главы **практически не содержит shell-команд**. Не заменять этот пробел вымышленными инструкциями по созданию VPN, Tor/Proxy маршрута или обходу геоблокировок. Никаких инструментов не запускалось.

## Источниковый inventory

| Название / опция из RAG | Назначение по книге | Класс воздействия / предел |
|---|---|---|
| **Firefox / Facebook Container** | Изоляция Facebook от части стороннего отслеживания | **Browser extension/state changing**; не универсальная анонимность [p0363:c01](../../../rag/chunks/p0301-p0400/p0363-c01.md) |
| **Decentraleyes** | Локальное обслуживание отдельных CDN ресурсов | **Browser extension/traffic alteration**; актуальность не установлена [p0363:c01](../../../rag/chunks/p0301-p0400/p0363-c01.md) |
| **AdNauseam** | Фоновые действия с рекламными сигналами | **Active network activity**, не read-only, эффективность не проверена [p0364:c01](../../../rag/chunks/p0301-p0400/p0364-c01.md) |
| **Прокси / веб-прокси / Google Translate** | Посредник передачи запроса | **Traffic redirection**, оператор может вести журналы; исторический пример [p0364:c01](../../../rag/chunks/p0301-p0400/p0364-c01.md)–[p0366:c01](../../../rag/chunks/p0301-p0400/p0366-c01.md) |
| **Ultrasurf** | Посредничество/ограниченная анонимность | **Network route/service trust change**; состояние продукта **[Needs confirmation]** [p0366:c01](../../../rag/chunks/p0301-p0400/p0366-c01.md)–[p0367:c01](../../../rag/chunks/p0301-p0400/p0367-c01.md) |
| **JonDo / JAP / JonDonym** | Mix-сеть из промежуточных узлов | **Network mediation**, характеристики тарифа/узлов историчны [p0367:c01](../../../rag/chunks/p0301-p0400/p0367-c01.md) |
| **HMA / Geonode proxy list** | Веб-прокси или каталог узлов, настройки Firefox | **External third-party relay**, безопасность и актуальность не проверены [p0367:c01](../../../rag/chunks/p0301-p0400/p0367-c01.md)–[p0369:c01](../../../rag/chunks/p0301-p0400/p0369-c01.md) |
| **VPN (ProtonVPN, Windscribe)** | Защищённый туннель / удалённый доступ | **Network route and identity trust**, имена не являются текущими рекомендациями [p0370:c01](../../../rag/chunks/p0301-p0400/p0370-c01.md) |
| **L2TP/IPsec** | Туннель и криптографический IPsec слой | **Transport security configuration**, отдельный L2TP без шифрования [p0370:c01](../../../rag/chunks/p0301-p0400/p0370-c01.md)–[p0371:c01](../../../rag/chunks/p0301-p0400/p0371-c01.md) |
| **OpenVPN** | TLS-based VPN over TCP/UDP | **Encrypted tunnel**, параметры и ключи конкретного профиля неизвестны [p0371:c01](../../../rag/chunks/p0301-p0400/p0371-c01.md) |
| **WireGuard** | VPN с криптографией Curve25519/ChaCha20/Poly1305/BLAKE2 | **Encrypted tunnel**, никакого current profile в RAG [p0372:c01](../../../rag/chunks/p0301-p0400/p0372-c01.md) |
| **Tor / I2P** | Многоузловые анонимные сети | **External routing/identity model**, без инструкций по обходу контроля [p0372:c01](../../../rag/chunks/p0301-p0400/p0372-c01.md)–[p0373:c01](../../../rag/chunks/p0301-p0400/p0373-c01.md) |
| **Tails live OS** | Использование live ОС для приватной работы | **System/session boot and network egress**, не доказана абсолютная анонимность [p0373:c01](../../../rag/chunks/p0301-p0400/p0373-c01.md)–[p0374:c01](../../../rag/chunks/p0301-p0400/p0374-c01.md) |

## Состав Tails в тексте книги — не установка пакетов

На [p0373:c01](../../../rag/chunks/p0301-p0400/p0373-c01.md), [p0374:c01](../../../rag/chunks/p0301-p0400/p0374-c01.md) перечислены **Tor Browser, OnionShare, Thunderbird/Enigmail, Pidgin/OTR, KeePassXC, Electrum, GnuPG, Tails Greeter, MAT, GNOME Censorship Circumvention**. Не воспроизводить команды установки/запуска на основании данного списка; фактическая поставка современной Tails **[Needs confirmation]**.

## Где автор показывает графические действия

На [p0368:c01](../../../rag/chunks/p0301-p0400/p0368-c01.md), [p0369:c01](../../../rag/chunks/p0301-p0400/p0369-c01.md) приведены **Settings → Network Settings → Connection Settings** Firefox и скриншоты конфигурации прокси. На [p0364:c01](../../../rag/chunks/p0301-p0400/p0364-c01.md)–[p0366:c01](../../../rag/chunks/p0301-p0400/p0366-c01.md) — браузерный пример с Google Translate. Ниже никаких конкретных адресов открытых прокси, операционных URL или внешних обходных маршрутов не публикуется: **их работоспособность и доверие к посреднику не подтверждены**.

## Read-only risk review / verification

Документировать scope, разрешённый источник и назначение трафика, владельцев стороннего узла, возможное журналирование, содержание metadata/fingerprinting, зависимость от пользовательских аккаунтов, ожидаемые эффекты VPN/Proxy/Tor/Tails. Сравнить **наблюдаемость** от веб-сервера, ISP, посредника и локальной ОС. Все оценки «невозможности наблюдения», «полной анонимности», «не оставляет следов» — **[Needs confirmation]**.

## Rollback / sensitive state

Смена browser proxy или VPN маршрутизации меняет действующую сетевую конфигурацию. Автор не приводит полную процедуру rollback профилей, ключей, логов у посредника или конфигурации live-ОС: **[Needs confirmation]**. Отдельная детализация сомнительных утверждений — [source-findings.md](source-findings.md).

**No execution:** команды настройки/тестирования не добавлялись из памяти; сетевых операций не производилось.
