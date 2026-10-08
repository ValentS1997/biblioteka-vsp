# Cheatsheet — глава 29. Authentication / Authorization / Access Control

Источник: `computer-networks-olifer-7e-ru-2026`; PDF 925–954, RAG p0925:c01–p0954:c01; policy **rag_only**. Схемы — концептуальные; реальный IAM/PKI не проверялся.

## Symptom / problem framing

Различать: неверный **идентификатор/фактор**, неуспешный **challenge/OTP**, недоверенный/недействующий **сертификат**, отсутствие/неверный **права доступа**, ошибочное назначение **ACL/MAC/RBAC**, просроченный/недействительный **SSO token**. «Пользователь не может зайти» не определяет уровень отказа.

## Baseline / context

| Контрольная точка | Что фиксировать | RAG |
|---|---|---|
| Identity / factor | User/process/service, «знаю / имею / являюсь» и реальная независимость факторов | p0925–p0926 |
| Password / challenge | Reusable vs OTP, повторное использование, правила lockout, PAP/CHAP, digest и challenge | p0927–p0931 |
| Hardware auth | Секрет/время/PIN, drift, time-window либо challenge-response | p0931–p0934 |
| Data / key trust | Подпись vs шифрование; identity→public key; CA, RA, revocation/validity | p0934–p0941 |
| Login boundary | ОС local/domain vs app-level identity DB | p0942–p0943 |
| Authorization | Subject, object, operation, least privilege; matrix, ACL, capability | p0943–p0946 |
| DAC / MAC / RBAC | Object owner; central labels/classification/categories; roles/permissions | p0946–p0952 |
| SSO | IdP, SP, trust relationship, token, expiry, renewal | p0953–p0954 |

## Read-only checks

1. **Identity ≠ permission.** Есть ли успешно подтверждённая заявленная идентичность? Какая операция запрошена и какой объект защищается? Есть ли отдельное решение authorization? [p0925, p0943].
2. **Factors.** Действительно ли несколько факторов принадлежат разным классам, или это два вопроса одной категории «знаю»? [p0926].
3. **Reusable password.** Отсутствуют ли признаки reuse, слабых secret и утечки? Какие последствия account lockout для availability? Не применять по умолчанию исторические правила expiration / «3 attempts». [p0927–p0928].
4. **Challenge-response.** Рандомизируется ли challenge; совпадают ли ответ/расчёт verifier; защищён ли секрет? PPP/CHAP пример книги не подменяет проверку применяемого механизма. [p0929–p0931].
5. **OTP/hardware.** Проверить класс и состояние токена, совместимость времени и окна приёма; сам факт «одноразовый» не исключает replay во время действия. [p0931–p0934].
6. **Signature/cert.** Подпись доказывает авторство в предпосылках доверия, но не конфиденциальность. Какие issuer/trust chain, срок, revocation и соответствие identity/public key? [p0934–p0940].
7. **OS/application.** Где осуществляется вход — local OS, domain, application? Как связаны/дублируются учётные данные? [p0942–p0943].
8. **Rights.** Права представлены ACL на объекте, capability на субъекте или динамическим правилом? Назначены ли минимальные привилегии? [p0943–p0946].
9. **DAC/MAC/RBAC.** Кто реально authorizes изменения? Для MAC classification/categories и правило доступа; для RBAC role→permissions и user→roles; для DAC владельцы объектов. Не считать авторское MAC-правило (хотя бы одна общая категория) универсальным. [p0947–p0952].
10. **SSO.** Кто IdP/SP, как проверяется подпись и действительность токена, кто принимает решение по доступу к конкретному сервису, как обновляется сессия? [p0953–p0954].

## Interpretation

- Неуспешный authentication ≠ отсутствие authorizations; успешный authentication ≠ наличие authorizations.
- PAP и MD5/CHAP упомянуты в учебной модели; **нельзя считать их современным рекомендуемым протоколом**.
- Подпись, сертификат и лицензия ПО — **разные проверки**. Certificate verification не ограничивается наличием CA signature.
- DAC удобен, но владелец может неконтролируемо переназначить доступ или скопировать содержимое; MAC централизован, RBAC группирует разрешения в роли.
- SSO повышает удобство и централизацию доверия, но access token не выдаёт все полномочия автоматически.
- CAPTCHA из исходника не гарантирует, что субъект — человек. Современная безопасность и совместимость требуют отдельного подтверждения.

## Next action

Создать read-only карту **identity → authenticator → verifier / IdP → token or certificate → access policy → resource**. Сопоставить доступную конфигурацию, policy owner, аудит, цепочки доверия, сроки/отзыв сертификатов, privileges и role memberships. Исходные данные действующей среды: **[Needs confirmation]**.

## Modifying action

Не менять пароли, OTP seeds, account lockout, CA trust, issued certificates, revocation, ACL, security labels, role assignments, SSO token lifetimes или IdP/SP trust на основании главы. Каждое действие может вызвать блокировку доступа либо компрометацию секретов. Конфигурационные CLI и действующие версии продуктов в RAG не заданы.

## Verification / acceptance checks

- Протокол authentication и authorization решены отдельно.
- Установлены owner, protected object, operation, и источник policy.
- Challenge/OTP/cert/token проверяются как **разные** механизмы.
- Read-only inventory не раскрывает секреты, личные данные или действующие токены.
- Исторические cryptographic/operational claims из source-findings не превращены в current policy.

## Rollback

Read-only анализ: **[Not applicable]**. Для IAM policy/ключей/сертификатов/SSO изменений необходимы approved scope, staging, backup, emergency access, acceptance и возврат к прошлой версии: **[Needs confirmation]**. Изменений не выполнялось.
