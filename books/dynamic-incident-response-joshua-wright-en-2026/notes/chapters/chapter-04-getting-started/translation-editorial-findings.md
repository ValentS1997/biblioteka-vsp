# Translation / editorial findings — Chapter 4

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0061:c01`–`p0075:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-04-getting-started.md`.

## Итог проверки

- Semantic coverage: good.
- Major concepts preserved.
- Listings 25–26 preserved.
- Figures 12–15 represented.
- Main v2 issue: very high mixed-language density.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `терминов incident response` | mixed-language | `терминов реагирования на инциденты` |
| `формирует подход response team` | mixed-language | `определяет подход команды реагирования` |
| `threat actor или adversary` | redundant hybrid | `субъект угрозы / атакующий` |
| `украденными credentials` | mixed-language | `украденными учётными данными` |
| `environmental incidents` | mixed-language | `инциденты, вызванные внешней средой` |
| `firewall` | style choice | `межсетевой экран (firewall)` first use |
| `root cause` | mixed-language | `корневая причина` |
| `remediation и prevention` | mixed-language | `устранение последствий и предотвращение повторения` |
| `data center` | mixed-language | `центр обработки данных` |
| `cloud provider` | mixed-language | `облачный провайдер` |
| `logging sources` | mixed-language | `источники журналирования` |
| `log file` | mixed-language | `файл журнала` |
| `browser session` | mixed-language | `браузерная сессия` |
| `source IP` | mixed-language | `исходный IP-адрес` |
| `Cyber Threat Intelligence sources` | mixed-language | `источники киберразведки об угрозах` |
| `username` | mixed-language | `имя пользователя` |
| `reporting system` | mixed-language | `система-источник / система регистрации` |
| `MySQL query` | mixed-language | `запрос MySQL` |
| `event type` | mixed-language | `тип события` |
| `aggregate EOI` | mixed-language | `агрегированный EOI` или русский equivalent |
| `threat intelligence feed` | mixed-language | `поток разведданных об угрозах` |
| `file hash` | mixed-language | `хеш файла` |
| `regular-expression match` | mixed-language | `совпадение по регулярному выражению` |
| `quality score` | mixed-language | `оценка качества` |
| `ticket / tickets` | mixed-language | `обращение / карточка инцидента` |
| `root cause` | repeated | `корневая причина` |
| `known-good state` | mixed-language | `заведомо исправное состояние` |
| `stakeholders` | mixed-language | `заинтересованные стороны` |
| `cross-functional coordination` | mixed-language | `межфункциональная координация` |
| `law enforcement` | mixed-language | `правоохранительные органы` |

## Structural / formatting findings

1. YAML metadata содержит literal `\n` внутри списка `third_party_review_flags`; это стоит очистить в v2.
2. MTTD/MTTR equations отсутствуют в RAG; current fail-closed marker корректен и должен быть сохранён, пока equations не будут извлечены из source PDF в отдельном repair process.
3. Figures 12–15 имеют высокую обучающую ценность и должны быть приоритетны для illustrated study edition.

## Visual debt

- Figure 12 — Waterfall of Events
- Figure 13 — Events of Interest
- Figure 14 — Aggregate EOI
- Figure 15 — Incident Response vs Incident Management responsibilities

Особенно важны Figures 12–14: они визуально объясняют vocabulary model главы.

## Priority

`HIGH`

Причина: Chapter 4 вводит базовый словарь всей книги. Terminology drift здесь распространяется на последующие главы, поэтому v2 normalization этой главы должна стать одним из book-level style anchors.
