# Глава 2 — Mermaid: доступ и внешняя аутентификация

Только [RAG PDF p59–p92](README.md). Схемы реконструируют текст, а не недоступные для машинного извлечения рисунки.

## 1. Разделение слоёв доступа ([p0061](../../../rag/chunks/p0001-p0100/p0061-c01.md)–[p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md))

```mermaid
flowchart TB
  ID["Учётная запись Zabbix"] --> G["Группа пользователя"]
  ID --> R["Роль пользователя"]
  G --> OBJECT["Scope: host groups / template groups"]
  OBJECT --> GRANT["Read либо Read-write"]
  R --> TYPE["User type: User / Admin / Super admin"]
  R --> UI["UI elements / services / modules"]
  R --> API["API / actions / maintenance"]
  GRANT --> EFFECT["Фактическая модель доступа"]
  TYPE --> EFFECT
  UI --> EFFECT
  API --> EFFECT
```

Имена групп **не** равны уровню роли. В книге s_network и r_infra получили Super admin, хотя принадлежали к предметным группам; таблица ролей на p74 требует проверять глобальные права.

## 2. Подготовка Cloud Hoster ([p0061](../../../rag/chunks/p0001-p0100/p0061-c01.md)–[p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md))

```mermaid
flowchart LR
  REQ["Требуемый доступ отдела"] --> GROUP["Создать user group"]
  GROUP --> SCOPE["Назначить host/template permissions"]
  SCOPE --> ROLE["Выбрать User/Admin/Super admin/ User+"]
  ROLE --> USER["Создать user и добавить в группу"]
  USER --> CHECK["Войти тестовым пользователем"]
  CHECK --> DEC{"Меню, объекты, действия соответствуют цели?"}
  DEC -- "Нет" --> ROLE
  DEC -- "Да" --> FIN["Завершить настройку"]
```

## 3. SAML/LDAP без JIT и с JIT ([p0077](../../../rag/chunks/p0001-p0100/p0077-c01.md), [p0084](../../../rag/chunks/p0001-p0100/p0084-c01.md)–[p0086](../../../rag/chunks/p0001-p0100/p0086-c01.md), [p0091](../../../rag/chunks/p0001-p0100/p0091-c01.md)–[p0092](../../../rag/chunks/p0001-p0100/p0092-c01.md))

```mermaid
flowchart TD
  LOGIN["Внешняя аутентификация: SAML/LDAP"] --> IDP["IdP / LDAP проверяет личность"]
  IDP --> VALID{"Проверка успешна?"}
  VALID -- "Нет" --> STOP["Вход отклонён"]
  VALID -- "Да" --> JIT{"JIT-provisioning включён?"}
  JIT -- "Нет" --> LOCAL["Нужен заранее созданный локальный user и права"]
  JIT -- "Да" --> MAP["Сопоставить внешние группы/атрибуты"]
  MAP --> CREATE["Создать/назначить Zabbix user/group/role"]
  LOCAL --> VERIFY["Проверить фактические разрешения в UI"]
  CREATE --> VERIFY
```

## 4. Безопасная последовательность переключения LDAP ([p0088](../../../rag/chunks/p0001-p0100/p0088-c01.md)–[p0091](../../../rag/chunks/p0001-p0100/p0091-c01.md))

```mermaid
flowchart TD
  A["Проверить существующий доступ Admin"] --> B["Назначить Admin в Internal"]
  B --> C["Default authentication → LDAP"]
  C --> D["LDAP settings: server / bind / JIT mapping"]
  D --> E["Выйти, войти тестовым LDAP user"]
  E --> F{"LDAP и требуемые права работают?"}
  F -- "Да" --> G["Проверить созданную запись в Users"]
  F -- "Нет" --> H["Проверить LDAP / mapping; метод отката: Needs confirmation"]
```

**Границы:** последовательность B перед C дана в тексте книги; конкретная процедура отката LDAP/JIT не описана, никаких вымышленных действий в схеме нет.
