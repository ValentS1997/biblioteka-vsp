# Глава 2 — команды, UI-пути, источники и границы

**RAG-only**; PDF pages 59–92. Здесь глава преимущественно состоит из операций в GUI, а не CLI. Заменяйте все значения тестовых учётных записей, URL, токенов, bind DN и паролей на значения собственной тестовой среды. Не используйте авторские дефолтные секреты.

## 1. Группы и роли пользователей Zabbix

| Операция из главы | Класс | Что меняется, риск, проверка, rollback |
|---|---|---|
| `Users → User groups` (просмотр) | Read-only | Инвентаризация групп и прав; [p0061](../../../rag/chunks/p0001-p0100/p0061-c01.md) |
| `Create user group` → `Group name` / `Frontend access` | State-changing после Add | Создаётся группа и выбирается `System default` или LDAP; риск — неправильный метод входа; проверить свойства группы; rollback процедуры `[Needs confirmation]`; [p0061](../../../rag/chunks/p0001-p0100/p0061-c01.md) |
| `Template permissions` / `Host permissions` → `Read` / `Read-write` | State-changing | Изменяется объектный доступ. Рецепт Networking: Template group `Templates/Network devices` с Read-write; Infrastructure: `Linux servers`; Buying/Inventory: обе группы с Read. Проверка — итоговый scope; rollback `[Needs confirmation]`; [p0062](../../../rag/chunks/p0001-p0100/p0062-c01.md)–[p0064](../../../rag/chunks/p0001-p0100/p0064-c01.md) |
| `Users → Authentication` → MFA-параметры | State-changing | Для группы может потребоваться MFA, но сперва метод должен быть настроен в Authentication. Риск — невозможность входа; конкретные поля/откат `[Needs confirmation]`; [p0062](../../../rag/chunks/p0001-p0100/p0062-c01.md) |
| `Users → User roles` (просмотр) | Read-only | Проверить существующие User/Admin/Super admin и назначенные ограничения; [p0065](../../../rag/chunks/p0001-p0100/p0065-c01.md) |
| `Create user role` → `User type` / `Access to UI elements` / `Access to actions` | State-changing после Add | В примере User+ role: тип Admin, Maintenance UI и действие Create and edit maintenance. Проверка — в отдельном тестовом аккаунте; риск расширенных прав; rollback `[Needs confirmation]`; [p0066](../../../rag/chunks/p0001-p0100/p0066-c01.md)–[p0071](../../../rag/chunks/p0001-p0100/p0071-c01.md) |
| `Users → Users` (просмотр) | Read-only | Проверить membership/роль и наличие записи; [p0072](../../../rag/chunks/p0001-p0100/p0072-c01.md) |
| `Create user` → `Username` / `User groups` / `Password` / `Permissions → Role` | State-changing | Создаёт аккаунт. Примеры Cloud Hoster — `s_network`, `y_network`, `r_infra`, `e_buy`. Пароли не переносить из тестового пособия. Верификация — права в тестовом входе; rollback `[Needs confirmation]`; [p0073](../../../rag/chunks/p0001-p0100/p0073-c01.md)–[p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md) |

**Важное ограничение:** роли `Super admin` в таблице p74 дают чтение и запись **всех** шаблонов/хостов, в отличие от обычных групповых ограничений. Нельзя считать аккаунт `s_network` ограниченным только Network devices без дополнительной проверки; подробнее [source-findings](source-findings.md).

## 2. SAML / Microsoft Entra ID + JIT (GUI и один файл)

Источник: [p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md)–[p0086](../../../rag/chunks/p0001-p0100/p0086-c01.md). Действия **State-changing** (в IdP и Zabbix):

1. Подготовить Azure/Entra пользователей и группу, в примере `zbx_admin`.
2. `Azure → Enterprise Applications → New Application → Create your own application`, создать учебное приложение Zabbix.
3. `Users and Groups`: назначить пользователя или группу, затем `Single sign-on → SAML`.
4. Собрать параметры IdP Entity ID, SSO URL, SLO URL, SP Entity ID, username attribute, SP format; при JIT — group/user name/last name attributes и mapping (p79). **Точные values на снимках экрана из p82–84 отсутствуют в текстовом RAG → `RAG_MISS`.**
5. В примере сертификат IdP сохраняют редактором в файл:

```sh
vim /usr/share/zabbix/conf/certs/idp.cert
```

Класс: **State-changing при записи**. Файл содержит сертификат IdP; источник не приводит процедуры обновления или rollback сертификата: `[Needs confirmation]`. Использовать только сертификат из согласованного IdP; [p0082](../../../rag/chunks/p0001-p0100/p0082-c01.md)–[p0083](../../../rag/chunks/p0001-p0100/p0083-c01.md).
6. `Users → Authentication → SAML settings`: настроить указанные атрибуты. JIT включать лишь после проверки сопоставления внешней группы с минимально необходимой локальной группой/ролью; [p0083](../../../rag/chunks/p0001-p0100/p0083-c01.md)–[p0084](../../../rag/chunks/p0001-p0100/p0084-c01.md).
7. Без JIT — связать уже существующий локальный аккаунт с правильным Azure-domain; с JIT — проверить создание аккаунта на первом входе. [p0084](../../../rag/chunks/p0001-p0100/p0084-c01.md)–[p0086](../../../rag/chunks/p0001-p0100/p0086-c01.md).

**Проверка:** вход через IdP и соответствие фактической роли/группы заданному mapping. **Риск:** отказ входа либо неверная роль из внешней группы. **Rollback:** `[Needs confirmation]` в данной главе.

## 3. OpenLDAP + JIT

Источник: [p0087](../../../rag/chunks/p0001-p0100/p0087-c01.md)–[p0092](../../../rag/chunks/p0001-p0100/p0092-c01.md).

Авторский пример запускает **только тестовое окружение** Docker. Сохранено имя источникового образа, но оно не верифицировано через образ/registry; команды ниже — запись RAG, **не готовая production-инструкция**:

```sh
docker run -p 389:389 -p 636:636 --name openldap-server --detach oicts/openldap:1.0.0
docker run -p 8081:80 -p 4443:443 --name phpldapadmin --hostname phpldapadmin --link openldap-server:ldap-host --env PHPLDAPADMIN_LDAP_HOSTS=ldap-host --detach osixia/phpldapadmin:0.9.0
```

Класс: **State-changing** — создаёт контейнеры, публикует порты `389/636/8081/4443`, инициирует сервисы; при входе/обращении к LDAP создаёт дополнительную рабочую нагрузку. **Предупреждение авторов:** в тестовом примере могут быть устаревшие версии. Достоверность `oicts/openldap:1.0.0` и безопасность публикуемых портов: `[Needs confirmation]`, **не запускать как проверенный рецепт**. Полный rollback/очистка контейнеров не заданы источником: `[Needs confirmation]`.

Для тестового phpLDAPadmin URL: `https://<TEST_LDAP_HOST>:4443` (read-only обращение, но аутентификация создаёт сессию); тестовые `Login DN` и пароль источника намеренно **не публикуются как действительные credentials** — взять значения своего окружения. [p0087](../../../rag/chunks/p0001-p0100/p0087-c01.md).

| Действие Zabbix | Класс | Условия/риск и проверка |
|---|---|---|
| `Users → Users`: добавить Admin в `Internal` | State-changing | Сохранить внутренний способ входа перед сменой default LDAP; проверка — доступ администратора; подробный rollback `[Needs confirmation]`; [p0088](../../../rag/chunks/p0001-p0100/p0088-c01.md) |
| `Users → Authentication`: выбрать default `LDAP` | State-changing | При неправильном соединении/группе возможно потерять пользовательский вход; делать после Internal; [p0089](../../../rag/chunks/p0001-p0100/p0089-c01.md) |
| `LDAP settings → Servers → Add` | State-changing | Добавить LDAP server, bind credentials (секрет `<LDAP_BIND_PASSWORD>`), JIT group mapping при необходимости; скриншот полей есть, значения из текста не извлекаются; `RAG_MISS`; [p0089](../../../rag/chunks/p0001-p0100/p0089-c01.md)–[p0090](../../../rag/chunks/p0001-p0100/p0090-c01.md) |
| `Sign out` → test user login | Workload-generating / изменение сессии | Проверить LDAP-вход; при JIT первый вход создаст учётную запись (state-changing как эффект JIT); [p0090](../../../rag/chunks/p0001-p0100/p0090-c01.md)–[p0091](../../../rag/chunks/p0001-p0100/p0091-c01.md) |
| `Users → Users` проверка после первого входа | Read-only | Убедиться, что создана правильная локальная запись и назначены ожидаемые права, не только что пароль принят; [p0091](../../../rag/chunks/p0001-p0100/p0091-c01.md)–[p0092](../../../rag/chunks/p0001-p0100/p0092-c01.md) |

## Критерии принятия главы

Группы и роли разделены; тестовый пользователь видит только согласованные объекты, меню и действия; пароль проверяется выбранным источником; JIT создаёт правильный локальный user/role/group при первом входе; внутренний административный доступ сохраняется после переключения default LDAP. Любой неописанный откат или поля из рисунков: `[Needs confirmation]`.

RAG-only, проверка фактических текущих версий Entra/OpenLDAP или Docker registry не выполнялась.
