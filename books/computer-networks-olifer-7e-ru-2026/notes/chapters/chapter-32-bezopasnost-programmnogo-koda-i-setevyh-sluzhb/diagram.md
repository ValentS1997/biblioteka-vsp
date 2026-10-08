# Диаграммы — глава 32. Безопасность кода и сетевых служб

Source: `computer-networks-olifer-7e-ru-2026`, PDF pp. 1023–1049, RAG p1023:c01–p1049:c01; **rag_only**. Merlin/Mermaid diagrams conceptual, не реконструкции рисунков 32.1–32.4 и не набор команд.

## 1. Безопасность входа и исполнения

~~~mermaid
flowchart TD
  INPUT["Недоверенные входные данные"] --> CHECK["Проверка формата / диапазона / размера"]
  CHECK --> APP["Логика приложения"]
  CHECK --> OTHER["Дополнительный уровень: прикладная фильтрация"]
  APP --> MEMORY["Адресное пространство / стек"]
  MEMORY --> PROTECT["Изоляция процесса / ограничения исполнения"]
  OTHER --> OBS["Наблюдение / антивирус / аудит"]
  PROTECT --> OBS
~~~

Опоры: [p1023](../../../rag/chunks/p1001-p1100/p1023-c01.md)–[p1025](../../../rag/chunks/p1001-p1100/p1025-c01.md), [p1030](../../../rag/chunks/p1001-p1100/p1030-c01.md)–[p1031](../../../rag/chunks/p1001-p1100/p1031-c01.md). Ни одна отдельная проверка не обещает абсолютной безопасности.

## 2. Угроза вредоносного ПО и механизмы обнаружения

~~~mermaid
flowchart TD
  CODE["Потенциально недоверенное ПО"] --> TAX{"Класс по источнику"}
  TAX --> TR["Trojan: маскируется как полезное"]
  TAX --> WO["Worm: распространяет копии по сети"]
  TAX --> VI["Virus: внедряется в файлы"]
  TAX --> HID["Undeclared function / implant"]
  TR --> DET["Signature и heuristic detection"]
  WO --> DET
  VI --> DET
  HID --> DET
  DET --> ISO["Sandbox / quarantine / operator decision"]
~~~

Опоры: [p1025](../../../rag/chunks/p1001-p1100/p1025-c01.md)–[p1032](../../../rag/chunks/p1001-p1100/p1032-c01.md). Классификация и методы — из текста, не доказательство эффективности конкретного продукта.

## 3. Браузер, HTTPS, приватность

~~~mermaid
flowchart TD
  USER["Пользователь / браузер"] --> HTTPS["HTTPS / защищённый канал"]
  HTTPS --> SERVER["Веб-сервис"]
  SERVER --> SESSION["Cookie SID / session state"]
  USER --> HISTORY["История / приватность"]
  SESSION --> SCOPE["Domain / lifetime / privacy"]
  SERVER --> CONTENT["Динамическое содержимое / расширения"]
  CONTENT --> TRUST["Доверие к исполнению на хосте"]
~~~

Опоры: [p1033](../../../rag/chunks/p1001-p1100/p1033-c01.md)–[p1037](../../../rag/chunks/p1001-p1100/p1037-c01.md). В первоисточнике `TSL` и универсальный client-cert claim требуют отдельного source review.

## 4. Почта: происхождение, содержимое, метаданные

~~~mermaid
flowchart LR
  AUTHOR["Отправитель"] --> SUBMIT["SMTP submission / provider authentication"]
  SUBMIT --> RELAY["Почтовые серверы"]
  RELAY --> RECIP["Получатель"]
  AUTHOR --> SIGN["End-to-end signature / S-MIME"]
  SIGN --> RECIP
  AUTHOR --> ENCRYPT["Content encryption"]
  ENCRYPT --> RECIP
  RELAY --> META["Адреса / время / заголовки / тема"]
  META --> PRIV["Privacy risk"]
~~~

Опоры: [p1037](../../../rag/chunks/p1001-p1100/p1037-c01.md)–[p1044](../../../rag/chunks/p1001-p1100/p1044-c01.md). Подпись, encryption и SMTP-auth охватывают **разные** задачи.

## 5. Облако: ответственность и полезные свойства

~~~mermaid
flowchart TD
  CUSTOMER["Клиент облака"] --> MODEL{"SaaS / PaaS / IaaS"}
  MODEL --> PROVIDER["Провайдер: infrastructure/security controls"]
  MODEL --> TENANT["Клиент: приложения / identities / data policy по модели"]
  PROVIDER --> SHARED["Многоарендность + admin-access risks"]
  PROVIDER --> BENEFITS["Резервирование / масштаб / anycast / специалисты"]
  TENANT --> AUDIT["Договор / SLA / аудит / residency"]
  SHARED --> AUDIT
  BENEFITS --> AUDIT
~~~

Опоры: [p1044](../../../rag/chunks/p1001-p1100/p1044-c01.md)–[p1049](../../../rag/chunks/p1001-p1100/p1049-c01.md). Фактическая модель разделения ответственности требует подтверждения договора и продукта: **[Needs confirmation]**.

## Operational boundary

Диаграммы не содержат live IP, credentials, секретов, эксплойт-кода или configuration CLI. Условия безопасного тестирования и rollback действительной системы **[Needs confirmation]**.
