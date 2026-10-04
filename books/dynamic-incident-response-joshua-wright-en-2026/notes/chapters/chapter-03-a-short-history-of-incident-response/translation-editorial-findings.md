# Translation / editorial findings — Chapter 3

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0049:c01`–`p0060:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-03-a-short-history-of-incident-response.md`.

## Итог проверки

- Translation semantically complete.
- Table 2 preserved.
- Listing 24 preserved.
- Figures 7–11 represented as placeholders.
- Главный debt — mixed-language prose и style consistency.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `buffer overflow` | mixed-language | `переполнение буфера` |
| `Remote Shell (RSH)` | acceptable technical term, but first-use policy needed | `Remote Shell (RSH)` сохранить как protocol/tool name |
| `security advisory` | mixed-language | `бюллетени безопасности` |
| `incident response` | repeated mixed-language | `реагирование на инциденты` в narrative |
| `incident handling` | repeated mixed-language | `обработка инцидентов` |
| `contingency response plan` | mixed-language quote translation | `план реагирования на непредвиденные ситуации` |
| `cybersecurity incident response` | mixed-language | `реагирование на киберинциденты` |
| `best practices` | mixed-language | `рекомендуемые практики` |
| `IT-generalists` | awkward mixed form | `IT-специалисты широкого профиля` |
| `generalist` | mixed-language | `специалист широкого профиля` |
| `incident handlers` | mixed-language | `специалисты по обработке инцидентов` |
| `Problem` | source structural label | `Problem («Проблема»)` при первом употреблении |
| `responder’а` | awkward hybrid | `специалиста по реагированию` |
| `checklist` | mixed-language | `контрольный список` |
| `incident response models` | mixed-language | `модели реагирования на инциденты` |
| `cloud identities` | mixed-language | `облачные идентичности` |
| `third-party SaaS` | mixed-language | `сторонние SaaS-сервисы` |
| `AI` | first-use policy | `ИИ (AI)` при первом употреблении |
| `security-роли` | hybrid | `роли специалистов по безопасности` |

## Terminology recommendation

Для Chapter 3 особенно важно различать:

- названия документов и frameworks — сохранять original English titles;
- lifecycle stage names — можно сохранять English в таблицах/сопоставлениях;
- narrative explanation — переводить на русский;
- acronyms CERT, CIAC, SANS, NIST, CSF, RSH, CFAA — сохранять.

## Visual debt

Source содержит Figures 7–11:

- Morris Worm Propagation;
- Timeline of Early Cybersecurity Incidents;
- Randy Marchany with SANS draft;
- SANS Guide v1.5 page;
- Timeline of IR Models and Incidents.

Для illustrated v2 эти figures дают высокий educational value, особенно timeline Figures 8 и 11.

## Priority

`MEDIUM-HIGH`

Глава читается хорошо, но исторический narrative будет заметно цельнее после удаления hybrid English/Russian phrasing и восстановления timelines.
