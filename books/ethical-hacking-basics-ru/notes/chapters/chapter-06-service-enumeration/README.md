# Глава 6 — перечисление сервисов и прикладной разведки

> Общее название главы — редакционное. Source RAG подтверждает разделы `6.1 Сервисы, RPC, RMI, SMB` и `6.2 SNMP, SMTP, Web-Based`; отдельное название всей главы 6 — [Needs confirmation]. Статус: `RAG_GROUNDED`; reading state не меняется.

## Источник и границы

- Книга: «Основы этичного хакинга», А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Канонический источник: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- PDF pages **140–168**, 1-indexed: **29 страниц / 32 addressable RAG chunks**.
- Первый chunk: `p0140:c01`; последний: `p0168:c02`; overlap chunks на p. 143, 158, 168.
- PDF p. 169 начинает `7.1 Эксплойты, сбор/взлом паролей` и исключена.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY` по v1.3; legacy RAG: `READY_WITH_KNOWN_LIMITATIONS`; chapter contract: v1.7.

## Структура

| Раздел | PDF pages | Фокус |
| --- | ---: | --- |
| **6.1 Сервисы, RPC, RMI, SMB** | 140–157 | service/version enumeration, RPC/rpcbind, Java RMI, NetBIOS/SMB, shares/users, SMB countermeasures |
| **6.2 SNMP, SMTP, Web-Based** | 158–168 | SNMP MIB/OID, SMTP behavior, web directories/CMS metadata, protocol-specific countermeasures, source summary |

## Основной принцип

После port discovery источник переходит на application-level enumeration: задача — выяснить, **какую дополнительную информацию раскрывает уже найденный сервис**. Это могут быть версии, RPC registrations, SMB shares, SNMP system metadata, SMTP capabilities, web/CMS metadata. Результаты нужно документировать для дальнейшей работы, но доступность сервиса сама по себе не даёт разрешения на credential testing или дальнейшее воздействие. Основание: `p0140:c01`, `p0168:c01`–`p0168:c02`.

## Карта знаний

1. **Service/version:** nmap service/version и NSE расширяют простой port scan до protocol-specific inspection. `p0140:c01`–`p0143:c01`.
2. **RPC/RMI:** rpcbind/portmap и RMI registry могут раскрывать зарегистрированные программы, объекты и динамические порты. `p0143:c01`–`p0147:c01`.
3. **SMB/NetBIOS:** host/workgroup/version/share/user data зависят от auth и protocol policy. `p0148:c01`–`p0156:c01`.
4. **SMB defense:** отключение устаревшего SMBv1, лишнего sharing/NetBIOS и ограничение SMB host/network firewalls. `p0157:c01`.
5. **SNMP:** MIB/OID могут раскрывать hostname, kernel, interfaces и contacts; source рекомендует v3, authentication, encryption и access restrictions. `p0158:c01`–`p0159:c01`.
6. **SMTP:** protocol dialogue может раскрывать capability/address behavior; source предлагает уменьшать user/address leakage и предотвращать open relay. `p0160:c01`–`p0162:c01`.
7. **Web:** directory/CMS enumeration раскрывает paths, versions, themes/plugins/users; это активные HTTP requests. `p0162:c01`–`p0167:c01`.
8. **Defense:** ограничивать доступ и metadata exposure на каждом сервисе. `p0157:c01`, `p0159:c01`, `p0162:c01`, `p0167:c01`–`p0168:c02`.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [source-findings.md](source-findings.md)

Отдельного блока практических заданий / review questions на PDF pp. 140–168 не обнаружено.

## Safety boundary

Enumeration создаёт network/application workload и может раскрывать чувствительные данные. Credential/user brute-force sequences, login attempts и write-capable management operations не превращаются в runnable procedures. Target, authorization, credentials, rate и lockout policy: **[Needs confirmation]**.
