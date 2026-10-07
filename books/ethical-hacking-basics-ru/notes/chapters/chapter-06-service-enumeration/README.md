# Глава 6 — перечисление сервисов и прикладной разведки

> Общее название главы — **редакционное**. Source RAG подтверждает `6.1 Сервисы, RPC, RMI, SMB` и `6.2 SNMP, SMTP, Web-Based`; отдельное название всей главы 6 — [Needs confirmation]. Коллекция: `RAG_GROUNDED`; reading state не меняется.

## Источник и provenance

- Книга: **«Основы этичного хакинга»**, А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Канонический источник: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- **PDF pages 140–168**, 1-indexed: **29 PDF-страниц / 32 addressable RAG chunks**.
- Первый chunk: `ethical-hacking-basics-ru:p0140:c01`; последний: `ethical-hacking-basics-ru:p0168:c02`.
- Overlap chunks `c02`: PDF pp. **143, 158, 168**.
- На PDF p. **169** начинается `7.1 Эксплойты, сбор/взлом паролей` — вне scope.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY` по v1.3 на последнем успешном main CI; RAG legacy-compatible `READY_WITH_KNOWN_LIMITATIONS`. Chapter contract: v1.7.

## Разделы

| Раздел | PDF pages | Начальный RAG | Фокус |
| --- | ---: | --- | --- |
| **6.1 Сервисы, RPC, RMI, SMB** | 140–157 | [p0140:c01](../../../rag/chunks/p0101-p0200/p0140-c01.md) | service/version enumeration, RPC/rpcbind, Java RMI, NetBIOS/SMB, shares/users, защитные меры SMB |
| **6.2 SNMP, SMTP, Web-Based** | 158–168 | [p0158:c01](../../../rag/chunks/p0101-p0200/p0158-c01.md) | SNMP/MIB/OID, SMTP user/address enumeration, web directories/CMS/WordPress, countermeasures, source summary |

Boundary anchors: [p0157:c01](../../../rag/chunks/p0101-p0200/p0157-c01.md) → [p0158:c01](../../../rag/chunks/p0101-p0200/p0158-c01.md); [p0168:c01](../../../rag/chunks/p0101-p0200/p0168-c01.md) + `p0168:c02` → [p0169:c01](../../../rag/chunks/p0101-p0200/p0169-c01.md).

## Основной принцип

После port/service discovery источник переходит на **application-level enumeration**: задача — получить дополнительные сведения из уже найденных служб: service/version, RPC registrations, SMB shares/users, SNMP MIB data, SMTP behavior и web/CMS metadata. Найденная информация должна документироваться для следующих этапов, но **сам факт доступного сервиса не означает разрешения на user enumeration, login attempts или brute force**. `p0140:c01`, `p0168:c01`–`p0168:c02`.

## Карта знаний

1. **Service enumeration.** `nmap -sV` и NSE расширяют простой port scan до service/version/protocol-specific inspection. `p0140:c01`–`p0143:c01`.
2. **RPC/RMI.** `rpcinfo`, rpcbind/portmap, Metasploit SunRPC modules и RMI registry enumeration раскрывают зарегистрированные программы/порты/objects; RMI может использовать динамические порты. `p0143:c01`–`p0147:c01`.
3. **SMB/NetBIOS.** `nbtstat`, `nmblookup`, NSE, Metasploit, `nbtscan`, `enum4linux` позволяют собирать names, versions, shares и иногда users. Часть запросов требует authentication; старые/null-session patterns не следует считать универсальными. `p0148:c01`–`p0156:c01`.
4. **SMB defense.** Source рекомендует отключать SMBv1/лишний file sharing/NetBIOS over TCP/IP и ограничивать SMB host/network firewalls. `p0157:c01`.
5. **SNMP.** MIB/OID и `snmpwalk` могут раскрыть hostname, kernel/interface data и contact fields. Source противопоставляет SNMPv1/v2c community strings более защищённой v3 и советует authentication, encryption и access restrictions. `p0158:c01`–`p0159:c01`.
6. **SMTP.** Manual protocol interaction и Metasploit могут проверять user/address behavior; source defense: disable VRFY where possible, reduce information leakage, reject/ignore unknown-address enumeration signals, prevent open relay, use email-security controls. `p0160:c01`–`p0162:c01`.
7. **Web enumeration.** `dirb`, Metasploit web modules и `wpscan` enumerate directories/CMS/users/plugins/themes/version metadata; requests are active and potentially high volume. `p0162:c01`–`p0167:c01`.
8. **Defensive objective.** Reduce exposed metadata, enforce access control, disable directory listing and restrict service reachability. `p0157:c01`, `p0159:c01`, `p0162:c01`, `p0167:c01`–`p0168:c02`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — operational interpretation and acceptance boundaries.
- [commands.md](commands.md) — source-confirmed commands classified by network/security effect; credential brute-force sequences are not operationalized.
- [diagram.md](diagram.md) — Mermaid maps: service→enumeration→evidence and service-specific defenses.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed summary.
- [summary.md](summary.md) — explicit author summary, `6.2 / Шаг 4`, p. 168.
- [source-findings.md](source-findings.md) — extraction anomalies, historical data, ambiguity and safety findings.

**Review questions/exercises:** отдельного блока «Практическое задание» / review questions на PDF pp. 140–168 **не обнаружено**; соответствующие файлы не создаются.

## Safety boundary

Enumeration remains active network/application interaction. Commands that enumerate users, try username/password combinations or invoke WordPress login-brute modules can trigger lockouts, alerts, privacy issues or unauthorized credential testing. No target, credentials, authorization, rate or lockout policy were supplied: **[Needs confirmation]**. Такие действия в `commands.md` описываются как source material, но не превращаются в runnable credential-attack procedure.
