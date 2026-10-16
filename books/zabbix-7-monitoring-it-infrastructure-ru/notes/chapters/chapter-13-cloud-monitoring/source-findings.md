# Глава 13 — source findings и границы воспроизводимости

**Source policy:** только принятый RAG PDF 490–510. Цитируются разные версии исходника без молчаливого исправления. Статус `RAG_MISS` означает значение/формулу/политику, присутствующую лишь на рисунке или во внешнем файле.

## 1. [Source wording/code mismatch] AWS Access key — номер шага сохранения

- **Вариант A:** [p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md) шаг **18** предписывает создать Access key, сохранить access key + secret в безопасном хранилище и нажать Done.
- **Вариант B:** той же страницей в шаге **21** написано «обязательно укажите ключ, который вы сохранили в шаге 19», но **шаг 19** — переход к веб-интерфейсу Zabbix.
- **Вывод:** номер шага, к которому отсылает текст, внутренне не соответствует описанию. Реальная пара IAM ключей берётся из **локально созданного ключа с сохранённым секретом**, а не из гипотетического шага. Никаких credential literals в Git.

## 2. [Source wording/code mismatch] Azure Tenant ID — номер шага

- **Вариант A:** [p0503](../../../rag/chunks/p0501-p0600/p0503-c01.md) шаг 21 отправляет в `Tenant properties`, а [p0504](../../../rag/chunks/p0501-p0600/p0504-c01.md) продолжение до шага 22 просит записать tenant ID.
- **Вариант B:** [p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md) в списке macros `{$AZURE.TENANT.ID}` ссылается на шаг **22**, который начинается с создания host в Zabbix, тогда как tenant ID берётся с предыдущего шага просмотра свойств tenant.
- **Вывод:** ссылка на шаг может вводить в заблуждение. Источник подтверждает **назначение macro**, но не исправляет нумерацию; проверять, что в нём реально Tenant ID, а не другое поле.

## 3. [Needs confirmation] Enterprise application и App registration — связь идентичностей

- [p0499](../../../rag/chunks/p0401-p0500/p0499-c01.md)–[p0500](../../../rag/chunks/p0401-p0500/p0500-c01.md) настраивают `Enterprise applications → Create your own application` и записывают Application ID шага 5.
- [p0500](../../../rag/chunks/p0401-p0500/p0500-c01.md)–[p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md) затем отдельно `App registrations → New registration`, создают secret на регистрации, после чего [p0503](../../../rag/chunks/p0501-p0600/p0503-c01.md) предлагают выбрать участника с именем `Zabbix book monitoring` для Reader.
- Текст **не разъясняет верификацию тождества** этих объектов и как именно сопоставляется Application ID первого с секретом второго. UI/screenshots содержат поля, но не структурированы в RAG.
- **Вывод:** не утверждать, что любой выбранный Application ID и secret из этих двух этапов образуют рабочие credentials без проверки фактического client/application/tenant principal. `[Needs confirmation]`.

## 4. [Source extraction issue / RAG_MISS] AWS inline IAM policy и точные значения AWS macros

- В [p0493](../../../rag/chunks/p0401-p0500/p0493-c01.md) IAM policy переходит в JSON, но содержимое показано на **рис. 13.5**, а не в текстовых RAG chunks. [p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md) показывает AWS credentials и region на **рис. 13.12**, текст подтверждает только региональный macro `{$AWS.REGION}`.
- [p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md) прямо рекомендует проверять **последние permissions каждого шаблона** отдельно, так как новые функции могут требовать иных scopes.
- **Вывод:** оригинальная AWS IAM policy, её actions/resources, названия всех AWS access-key macros и least-privilege security review = `RAG_MISS` или `[Needs confirmation]`. Не сочинять JSON по общей AWS документации.

## 5. [Needs confirmation / cost] CloudWatch оплачивается

- [p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md) предупреждает, что AWS CloudWatch — платная услуга, рекомендует ознакомиться с тарифами до работы. Стоимость, использование, ставки и лимиты **в книге не рассчитаны**.
- **Вывод:** запуск discovery/API calls может повлечь плату и использовать квоты; текущая тарификация не проверялась из-за RAG-only. Не обещать «бесплатный мониторинг AWS» и не включать агрессивный опрос без оценки.

## 6. [Security-sensitive] Azure role Reader, client secret, lifecycle

- [p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md) устанавливает срок действия client secret, [p0502](../../../rag/chunks/p0501-p0600/p0502-c01.md) говорит, что его Value показывается один раз и нужно хранить в секретном vault. [p0503](../../../rag/chunks/p0501-p0600/p0503-c01.md) выдаёт `Reader` на выбранную Subscription.
- Текст не описывает автоматическую ротацию ключей, policy ограничений Azure API или сценарий отзыва credentials/role. Отсутствующие поля формы и политика доступа = `[Needs confirmation]`.
- **Вывод:** не передавать `{$AZURE.PASSWORD}` и другие IDs/секреты как реальные значения в repo, CI, issue или чат. Не расширять роль выше Reader для устранения ошибки, пока не выяснена причина.

## 7. [Security-sensitive] Добавление `zabbix` в группу Docker

- [p0508](../../../rag/chunks/p0501-p0600/p0508-c01.md) содержит `gpasswd -a zabbix docker` как шаг для мониторинга контейнеров, за которым следует restart Agent 2.
- Текст **не объясняет**, как доступ к Docker engine влияет на привилегии локального пользователя, какие есть ограничения socket, rootless mode, принципы least privilege и безопасный rollback. Это не доказательство безопасности.
- **Вывод:** членство `docker` может дать чрезвычайно широкие права через Docker daemon; не выполнять на production host автоматически. Подтвердить authorization/mitigations отдельно, `[Needs confirmation]`.

## 8. [Source extraction issue / RAG_MISS] AWS/Azure JavaScript, LLD и Docker preprocessing

- **AWS**: JavaScript API call виден лишь на рис. 13.16 ([p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)); exact LLD prototype template linkage — рисунки 13.14–13.15, готовый script code не извлечён.
- **Azure**: шесть LLD правил описаны на [p0506](../../../rag/chunks/p0501-p0600/p0506-c01.md), Script JavaScript код только на рис. 13.35 ([p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)); API endpoint/JSONPath/config values `RAG_MISS`.
- **Docker**: [p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md) текстом подтверждены master `docker.info`, `docker.containers.discovery`, `docker.container_info`, macro `{#NAME}` и два правила discovery. Точные item/preprocessing JSONPath и plugin access fields не приводятся текстом.
- **Вывод:** нельзя выдавать Mermaid/commands как полноценный самостоятельный deploy script без нужных значений. Не реконструировать figure-only values.

## 9. [Needs confirmation] RAG и конец книги

- Последний содержательный chunk главы — [p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md) с Docker «Дополнительная информация». Текстовая страница 511 отсутствует; [p0512](../../../rag/chunks/p0501-p0600/p0512-c01.md) содержит рекламный материал книги «Linux для разработчиков», **не часть главы 13**.
- Нет отдельного chapter-end summary, review questions/answers или проверочных упражнений. Эти условные файлы не публикуются.
- Ни одного проверенного полного rollback для AWS keys/IAM policy, Azure app/secret/Reader, Docker group membership и автоматически созданных hosts не представлено. `[Needs confirmation]`.

**Статус чтения не изменён.**
