# Авторское итоговое резюме главы 6

**Источник:** раздел 6.2, **Шаг 4**, PDF p. **168**, chunks `ethical-hacking-basics-ru:p0168:c01` и `ethical-hacking-basics-ru:p0168:c02`. Ниже — структурированное изложение author summary без внешних дополнений.

## 1. Enumeration выше простого port scan

Автор определяет перечисление как сбор дополнительной информации на уровне приложений: usernames, shares, service details и других данных, пригодных для последующих этапов.

## 2. nmap / NSE

В summary nmap используется не только для определения открытых портов, но и для service identification; NSE scripts добавляют protocol-specific collection logic.

## 3. SMB / RPC / RMI

SMB рассматривается как источник share/user/management metadata. RPC services могут динамически регистрироваться через mapping/registry service; Java использует RMI.

## 4. Metasploit и protocol-specific tools

Metasploit может работать с несколькими protocol families и сохранять часть результатов в backend database. Для SNMP отдельно упоминается snmpwalk; для SMB существуют встроенные Windows/Linux/Samba tools.

## 5. Заметки и countermeasures

Автор рекомендует сохранять результаты enumeration для дальнейшей работы. В финале подчёркивается: у каждой enumerated service должны быть соответствующие защитные меры, а ограничение доступа к сервису — общий defensive principle.

## Boundary

- Summary заканчивается на p. 168.
- p. 169 начинает главу 7.
- Реальные service outputs, target list, authorization и credentials: **[Needs confirmation]**.
