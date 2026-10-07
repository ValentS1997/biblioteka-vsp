# Глава 9 — Безопасность

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 9 — «Безопасность»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `659–783`
- Addressable RAG chunk range: `p0659:c01 … p0783:c01`
- Chunks in chapter range: `125`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 659 begins with `Глава 9. Безопасность`;
  - PDF page 784 begins with `Глава 10. Изучение конкретных примеров: Unix, Linux и Android`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 775 and continues onto page 776. Review questions/exercises occupy PDF pages 776–783 and are explicitly numbered 1–62.

## Main principle

Security is a layered property, not a single mechanism:

`policy → protection model → authentication → implementation correctness → malware resistance → defense in depth`.

The chapter repeatedly returns to two engineering rules:

1. make the trusted computing base as small as practical;
2. assume that one defensive layer can fail, so independent layers must remain.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 9.1 | Внешние условия, требующие принятия дополнительных мер безопасности | 661–665 |
| 9.1.1 | Угрозы | 662–665 |
| 9.1.2 | Злоумышленники | 665 |
| 9.2 | Безопасность операционных систем | 665–669 |
| 9.2.1 | Можно ли создать защищенные системы? | 666–667 |
| 9.2.2 | Высоконадежная вычислительная база | 667–669 |
| 9.3 | Управление доступом к ресурсам | 669–677 |
| 9.3.1 | Домены защиты | 669–671 |
| 9.3.2 | Списки управления доступом | 671–674 |
| 9.3.3 | Перечни возможностей | 674–677 |
| 9.4 | Формальные модели систем безопасности | 677–686 |
| 9.4.1 | Многоуровневая защита | 679–682 |
| 9.4.2 | Тайные каналы | 682–686 |
| 9.5 | Основы криптографии | 686–693 |
| 9.5.1 | Шифрование с секретным ключом | 687–688 |
| 9.5.2 | Шифрование с открытым ключом | 688–689 |
| 9.5.3 | Односторонние функции | 689 |
| 9.5.4 | Цифровые подписи | 689–691 |
| 9.5.5 | Криптографические процессоры | 691–693 |
| 9.6 | Аутентификация | 693–706 |
| 9.6.1 | Слабые пароли | 695–697 |
| 9.6.2 | Парольная защита в UNIX | 697–698 |
| 9.6.3 | Одноразовые пароли | 698–700 |
| 9.6.4 | Схема «оклик — отзыв» | 700 |
| 9.6.5 | Физический объект / смарт-карта | 700–703 |
| 9.6.6 | Биометрия | 703–706 |
| 9.7 | Взлом программного обеспечения | 706–725 |
| 9.7.1 | Переполнение буфера | 708–717 |
| 9.7.2 | Форматирующая строка | 717–720 |
| 9.7.3 | Dangling pointers | 720–721 |
| 9.7.4 | NULL-pointer dereference | 721–722 |
| 9.7.5 | Integer overflow | 722–723 |
| 9.7.6 | Command injection | 723–724 |
| 9.7.7 | TOCTOU | 724–725 |
| 9.8 | Инсайдерские атаки | 725–728 |
| 9.8.1 | Логические бомбы | 725–726 |
| 9.8.2 | Лазейки | 726–727 |
| 9.8.3 | Фальсификация входа | 727–728 |
| 9.9 | Вредоносные программы | 728–754 |
| 9.9.1 | Троянские кони | 731–733 |
| 9.9.2 | Вирусы | 733–743 |
| 9.9.3 | Черви | 743–745 |
| 9.9.4 | Программы-шпионы | 745–749 |
| 9.9.5 | Руткиты | 749–754 |
| 9.10 | Средства защиты | 754–773 |
| 9.10.1 | Брандмауэры | 754–756 |
| 9.10.2 | Антивирусные и антиантивирусные технологии | 756–763 |
| 9.10.3 | Электронная подпись двоичных программ | 763–764 |
| 9.10.4 | Тюремное заключение | 764–765 |
| 9.10.5 | Model-based IDS | 765–767 |
| 9.10.6 | Инкапсулированный мобильный код | 767–771 |
| 9.10.7 | Безопасность Java | 771–773 |
| 9.11 | Исследования в области безопасности | 773–775 |
| 9.12 | Краткие выводы | 775–776 |
| — | Вопросы / упражнения | 776–783 |

## Key concepts

- **CIA:** confidentiality, integrity, availability.
- **TCB:** smallest hardware/software base that must be correct for the security policy to hold.
- **POLA / least authority:** each domain receives only the objects and operations it actually needs.
- **Protection domain:** set of `(object, rights)` pairs.
- **ACL:** object-centric sparse representation of the access matrix.
- **Capability list:** domain/process-centric sparse representation of the same matrix.
- **Bell–LaPadula:** confidentiality — read down, write up.
- **Biba:** integrity — read up, write down.
- **Covert channel:** communication path using shared observable state outside the intended protection interface.
- **Steganography:** hides existence of information; the chapter's RGB example stores one secret bit in each color component.
- **Symmetric crypto:** fast, but requires prior shared-key establishment.
- **Public-key crypto:** solves key-distribution problems at much higher computational cost.
- **One-way/hash function:** easy forward evaluation, computationally difficult inversion.
- **Digital signature:** supports authenticity/integrity/nonrepudiation when private keys remain controlled.
- **Salt:** makes precomputed password dictionaries far more expensive.
- **Lamport one-time passwords:** use a reverse one-way hash chain so an observed password does not reveal the next one.
- **Stack canary / DEP / ASLR:** independent mitigations against memory-corruption exploitation.
- **TOCTOU:** security check and privileged use refer to a mutable pathname at different times.
- **Malware classes:** trojan, virus, worm, spyware, rootkit.
- **Defense in depth:** firewall, scanning, signed code, confinement/jailing, IDS, mobile-code sandboxing and language/runtime safety.

## Operational interpretation

For a security incident, classify the violated property and trust boundary first:

`identity` → authentication  
`who may do what` → authorization / ACL / capability  
`secret escaped` → confidentiality / covert channel / credential or key issue  
`data changed` → integrity / privilege or memory-safety issue  
`service unavailable` → availability / resource exhaustion  
`unexpected code runs` → software flaw / malware / mobile-code boundary

Do not confuse:

- authentication with authorization;
- encryption with integrity;
- ACL revocation with revocation of already-open handles;
- a formal access model with proof that implementation contains no covert channels;
- malware removal with restoration of trust;
- a firewall with complete host security.

## Safety boundary for exercises

This chapter contains historical offensive examples and implementation exercises. Artifacts preserve their educational meaning but do not provide deployable exploit, credential-cracking, covert-channel exfiltration or file-infecting malware code. Safe toy/sandbox alternatives are used where appropriate.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- Figures/tables are text-RAG grounded but not independently encoded as multimodal objects.
- Some figure-internal labels are mojibake in the PDF text layer.
- External-site/download tasks remain `[Needs confirmation]` under `rag_only`.
- Historical algorithms and product behavior are not modernized with external sources.
- Practical security exercises are answered at a defensive/conceptual level rather than with operational attack code.
