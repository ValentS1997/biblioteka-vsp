# Cheatsheet — глава 28. Информационная безопасность

Source: `computer-networks-olifer-7e-ru-2026`, PDF 892–924, RAG p0892:c01–p0924:c01. **rag_only**. Учебный checklist, а не заключение об уровне безопасности реальной ИС.

## Symptom / problem framing

Задача: определить, что именно является нарушением — **неверная идентичность / доступ**, нарушение **confidentiality, integrity, availability**, отсутствие неотказуемости либо иной аспект гексады; связать **актив/субъект/операцию**, **уязвимость**, **угрозу**, **возможную атаку**, **бизнес-ущерб** и **контрмеру**. Наличие продукта security само по себе не доказывает защищённость.

## Baseline / context

| Ось | Опорные понятия | RAG |
|---|---|---|
| Access control | субъект → операция → объект; identification, authentication, authorization | p0892–p0895 |
| Safety properties | КЦД/CIA; Parkerian Hexad; non-repudiation в тексте | p0895–p0898 |
| Risk | asset → vulnerability/threat → attack → impact/probability | p0898–p0902 |
| Attacks | passive/active, DoS/DDoS, malicious code, phishing | p0902–p0906 |
| Controls | legislative, administrative, procedural, technical | p0907–p0908 |
| Principles | top-down, process, layered, balanced, economically reasonable | p0908–p0913 |
| Crypto | key secrecy, symmetric vs asymmetric; key distribution; DH, RSA, H(X,K) | p0913–p0924 |

## Read-only checks

1. **Доступ.** Для каждого критичного ресурса названы субъекты (включая processes), операции и allow/deny policy? Отделены идентификатор, подтверждение идентичности и решение о разрешениях? [p0892–p0895]
2. **CIA.** Что является нарушением confidentiality, integrity и availability именно в данном сервисе, включая критичные требования по задержке? Нельзя трактовать возможность аутентификации как защиту всех трёх свойств. [p0895–p0897]
3. **Дополнительные свойства.** Есть ли требование доказательства авторства/факта действия, физического владения носителем и usability, отсутствующее в «узкой» CIA-модели? [p0897–p0898]
4. **Threat modeling.** Какая уязвимость и какой субъект/путь её использования дают реалистичный сценарий угрозы? Не смешивать словарь vulnerability/threat/attack/impact. [p0898–p0901]
5. **Risk.** Есть оценка вероятности и бизнес-ущерба, срок/контекст оценки и приоритет? Назначено ли решение accept/eliminate/reduce/transfer и владелец? [p0901–p0902]
6. **Тип атаки.** Passive reconnaissance либо active DoS/DDoS, malware, identity deception? Сохранены ли легитимность и границы аудита? [p0902–p0906]
7. **Defense in depth.** Разделены юридический, policy, operational и technical уровни; имеются ли резервные барьеры и независимая проверка наиболее слабого входа? [p0907–p0911]
8. **Economics.** Оценены ли residual risk, стоимость внедрения и косвенная потеря продуктивности? «Разумная достаточность» не значит игнорировать значимый риск. [p0912–p0913]
9. **Keys and trust.** Различены симметричное шифрование, DH согласование ключа, RSA public/private, сертификаты для проверки принадлежности public key и keyed digest? Учебные числа и алгоритмы не считать современной рекомендованной криптоконфигурацией. [p0914–p0924]

## Interpretation

- Authentication **не** то же, что authorization: корректно вошедший пользователь может не иметь права выполнять операцию.
- CIA — классификатор свойств, не чекбокс полной безопасности; авторская гексада включает аспекты possession и utility, а не только триаду.
- Risk требует **impact и likelihood**; severity технической находки не заменяет бизнес-оценку.
- Firewall/IDS/antivirus недостаточны без управления, процедур и корректного access control. Блокировка единственного канала не поможет при обходном канале.
- Шифрование отвечает прежде всего за confidentiality, keyed digest — за обнаружение изменения/аутентичность при соответствующей защищённой реализации. Key distribution/identity binding критичны.
- **MD2/MD4/MD5, простой `x mod n`, toy DH/RSA и DES/3DES не интерпретировать как безопасную production-рекомендацию.** Source-findings содержит исходные claims и границы.

## Next action

В реальном разрешённом контексте собрать **read-only evidence**: реестр активов, матрицу субъект/операция/объект, service dependencies, policy, назначенных owners, угрозы, существующие controls, уровень аудита, инвентаризацию криптографических алгоритмов/версий (без секретов), статусы патчей и оценку бизнес-влияния. Всё, чего нет в источнике и среде, **[Needs confirmation]**.

## Modifying action

Изменения access rights, ключей и алгоритмов, security policy, firewall/IDS, audit и системы авторизации могут остановить сервис либо потерять доступ. Глава **не содержит** подтверждённых CLI, конфигураций, разрешений, change window и криптографических migration-процедур. Нельзя выполнять сетевые сканирования без согласованного scope.

## Verification / acceptance checks

- Подтверждён источник каждого вывода, а не лишь общая терминология.
- AAA, CIA, business risk, 4 control layers и security-as-process разнесены.
- Toy cryptography отделена от реальной security posture.
- Сохранены разделение attack/threat/vulnerability и доказательства воздействия.
- Никакая уязвимость, атака, компрометация или «система защищена» не объявлена без измерений.

## Rollback

Read-only review: **[Not applicable]**. Реальные изменения криптографии, контроля доступа, правил и конфигураций требуют версионирования, тестов, окна обслуживания и плана отката: **[Needs confirmation]**. Ни одна production-система не изменена.
