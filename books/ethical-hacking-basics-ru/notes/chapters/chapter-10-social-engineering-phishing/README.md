# Глава 10 — социальная инженерия, фишинг и физический доступ

> Общее название главы — редакционное. Source RAG подтверждает разделы `10.1 Принципы, Претекстинг, Физическая соц.инженерия` и `10.2 Фишинговые атаки, Беспроводная соц.инженерия, Автоматизация`. Статус: `RAG_GROUNDED`; reading state не меняется.

## Источник и границы

- Книга: «Основы этичного хакинга», А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Canonical source: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- PDF pages **274–297**, 1-indexed: **24 страницы / 36 addressable RAG chunks**.
- Первый chunk: `p0274:c01`; последний: `p0297:c01`.
- Overlap chunks: p. 274–281, 287, 291, 292, 296.
- PDF p. **298** начинает `11.1 Wi-Fi - типы, аутентификация, шифрование, BYOD, атаки` и исключена.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY`; RAG: `READY_WITH_KNOWN_LIMITATIONS`; chapter contract: v1.7.

## Структура

| Раздел | PDF pages | Содержание |
| --- | ---: | --- |
| **10.1 Принципы, Претекстинг, Физическая соц.инженерия** | 274–282 | принципы влияния, цели social engineering, pretexting, phishing/vishing/smishing/impersonation, физический доступ, tailgating, baiting |
| **10.2 Фишинговые атаки, Беспроводная соц.инженерия, Автоматизация** | 283–297 | phishing indicators, contact spam, quid pro quo, social networks, website cloning concepts, watering-hole/wireless social engineering, automation tooling, source summary |

Boundary anchors: p.282 → p.283; p.297 → p.298.

## Главный принцип

**Социальная инженерия эксплуатирует доверие, контекст и человеческие решения; defensive control должен уменьшать зависимость от “правильной реакции пользователя” и создавать проверяемые каналы подтверждения.** Source описывает как психологические принципы, так и phishing/physical/wireless automation. Offensive examples сохраняются как threat-model material, но не превращаются в scripts/templates/campaign playbook.

## Карта знаний

1. **Принципы влияния:** взаимность, обязательство/приверженность, социальное доказательство, власть, симпатия, дефицит. `p0274:c01`–`p0275:c01`.
2. **Pretexting:** заранее подготовленный сценарий, согласованный с желаемым результатом; source показывает credential-seeking examples. `p0275:c01`–`p0276:c01`.
3. **Векторы:** phishing, vishing, smishing, impersonation; физические техники включают tailgating/baiting. `p0276:c01`–`p0282:c01`.
4. **Phishing analysis:** unusual claims, requests for personal data, sender/address anomalies, mismatched visible/actual links, suspicious attachments and pressure/authority cues. `p0283:c01`–`p0285:c01`.
5. **Trust abuse:** contact spam, compromised/cloned social identities and quid pro quo exploit trusted relationships. `p0286:c01`–`p0287:c01`.
6. **Web/wireless deception:** cloned websites, watering-hole concepts and rogue/imitated wireless access points are source threat patterns. `p0288:c01`–`p0294:c01`.
7. **Automation:** source names phishing/social-engineering campaign tools and payload-oriented frameworks; chapter artifacts retain only taxonomy and defensive implications. `p0286:c01`, `p0294:c01`–`p0297:c01`.
8. **Defense:** awareness, independent callback/verification channels, access badges/mantraps/biometrics, link/domain inspection and technical email/web/network controls reduce reliance on trust alone.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [source-findings.md](source-findings.md)

Отдельного блока **«Практическое задание»** / review questions на PDF pp. 274–297 не обнаружено.

## Safety boundary

Source содержит phishing campaign tooling, cloned-site delivery, rogue wireless AP, credential collection, malicious attachments/payloads and automated social-engineering frameworks. Эти техники могут facilitate credential theft, malware delivery and impersonation. Здесь они документируются для анализа угроз и защиты; runnable phishing/credential-harvesting/payload workflow не воспроизводится. Authorized campaign scope, target list, legal/HR approval, data handling and stop conditions: **[Needs confirmation]**.
