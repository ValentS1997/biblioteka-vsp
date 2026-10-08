# Команды, процедуры и формулы — глава 28

Источник: PDF 892–924, RAG p0892:c01–p0924:c01, **rag_only**. Обозначения учебные, не исполнимые инструкции.

## CLI

**Подтверждённых platform CLI, команд криптогенерации, сканирования уязвимостей или атаки нет.** Глава упоминает продукты/механизмы (Nessus, McAfee, firewall, IDS/IPS), но не задаёт запуск, права доступа, scope, параметры или rollback. Создавать команды из общих знаний запрещено.

## Контролируемый доступ и управление риском

| Элемент / операция | Смысл в тексте | Классификация | RAG |
|---|---|---|---|
| Subject / object / operation | Субъект действует над ресурсом по правилам | access-control decision | p0892–p0893 |
| Identification | Идентификатор пользователя, процесса, сервиса | identity lifecycle state | p0893 |
| Authentication | Проверка права субъекта выдавать себя за заявленную идентичность | security/control | p0894–p0895 |
| Authorization | Разрешённая операция над объектом | access-control state-changing policy | p0895 |
| Vulnerability scanning | Поиск «отпечатков» дефектов по ответам системы | **workload-generating**, только санкционированно | p0899 |
| Risk assessment | Бизнес-ущерб + вероятность | read-only analysis if inputs available | p0901 |
| Risk decision | Accept, eliminate, reduce, transfer | governance / policy state | p0902 |
| Layered controls | Legal, administrative, procedural, technical | security program, не конфигурация | p0907–p0908 |
| Continuous protection cycle | Threat/vulnerability → risk → policy → action | governance workflow | p0909 |

## Учебная криптография, не production recipes

| Формула/механизм | Содержание источника | Ограничение | RAG |
|---|---|---|---|
| `Y = F_k(X)`, `X = F'_k(Y)` | Symmetric encryption/decryption с общим секретным ключом | Алгоритм/режим/nonce не заданы | p0914–p0915 |
| `n(n−1)/2` | Уникальные попарные symmetric keys для `n` участников | Модель полного попарного обмена | p0917 |
| `a=D^A mod P`, `b=D^B mod P` | Public values в DH при private A/B | Малые числа только учебные, нет аутентификации сторон | p0917–p0918 |
| `K=b^A mod P=a^B mod P` | Совпадающий общий секрет в DH | Источник: D=7, P=13, A=2, B=4 → K=3; **криптографически небезопасный игрушечный пример** | p0918 |
| `N=P·Q`, `M=(P−1)(Q−1)` | RSA key setup, разделяемые роли E/D | Источник: P=7, Q=13; недостаточны для реальной стойкости | p0922 |
| `E·D ≡ 1 (mod M)` | Выбор закрытого D к открытому E | В примере N=91, E=5, D=29 | p0922 |
| `C=X^E mod N` | RSA шифрование блока в тексте | X=82, C=10 — только иллюстрация, padding/format не описаны | p0922 |
| `M=H(X,K)`, `M'=H(X,K)` | Совпадение параметрических дайджестов для контроля integrity | Алгоритм/обработка ключа неизвестны, сравнение не абсолютное доказательство отсутствия изменений | p0923–p0924 |
| `x mod n` | Автор приводит как пример «односторонней» хеш-функции | **Не считать криптостойким хешем**; см. source-findings.md | p0923 |

## Safety / verification

Публикация public key — не доказательство **его принадлежности** заявленному пользователю: текст p0923 отдельно требует защиту от подмены с помощью сертификатов. Алгоритмы DES/3DES, MD2/MD4/MD5 и неуточнённый «SHA 20 байт» в исходном тексте — исторические примеры, **не настройки современных защищённых систем**.

Read-only допустимо анализировать уже доступные метаданные и политики в рамках прав доступа. Scanning/изменение прав/ключей — workload-generating или state-changing и требует подтверждённого authority, scope, prechecks, verification, rollback. **[Needs confirmation]**. Никаких реальных команд не выполнялось.
