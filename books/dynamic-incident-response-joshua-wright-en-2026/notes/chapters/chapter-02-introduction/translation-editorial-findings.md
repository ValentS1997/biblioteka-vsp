# Translation / editorial findings — Chapter 2

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0044:c01`–`p0048:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-02-introduction.md`.

## Итог проверки

- Крупных непреведённых narrative-блоков нет.
- Смысл и структура оригинала сохранены.
- Основной v2 debt — mixed-language prose и terminology consistency.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `источника threat intelligence` | mixed-language | `источника разведданных об угрозах` или единый glossary policy |
| `managed service provider` | mixed-language | `поставщика управляемых услуг (MSP)` при первом употреблении |
| `разделом Step-by-Step` | mixed-language heading term | `разделом «Шаг за шагом» (Step-by-Step)` |
| `Software Development Kits (SDKs)` | можно улучшить русскую вводную форму | `комплекты разработки ПО (SDK)` |
| `listener’ы` | awkward transliteration | `сетевые слушатели (listeners)` либо `процессы, прослушивающие порты` |
| `украденные credentials` | mixed-language | `украденные учётные данные` |
| `pivot в AWS-среду` | mixed-language | `переходит в AWS-среду` |
| `аналитик incident response расследует ticket` | рваная mixed-language фраза | `аналитик по реагированию на инциденты расследует обращение` |
| `incident management` | mixed-language | `управление инцидентами` |
| `incident responders` | mixed-language | `специалисты по реагированию на инциденты` |
| `response functions` | mixed-language | `функции реагирования` |
| `acceptable use policy` | mixed-language | `политика допустимого использования` |
| `cyber insurers` | mixed-language | `киберстраховщики` / `страховые компании по киберрискам` |
| `threat intelligence` | recurring glossary drift | унифицировать book-level policy |
| `ransomware и extortion threats` | mixed-language | `ransomware и угрозы вымогательства` |
| `third-party services` | mixed-language | `сторонние сервисы` |
| `shared responsibility models` | mixed-language | `модели совместной ответственности` |
| `remote endpoints` | mixed-language | `удалённые конечные устройства` |
| `incident response teams` | mixed-language | `команды реагирования на инциденты` |
| `stakeholders` | mixed-language | `заинтересованные стороны` |
| `AI` | термин допустим, но book-level choice нужен | `ИИ (AI)` при первом употреблении |

## Style recommendation

Для v2 Chapter 2 лучше использовать принцип:

- narrative prose — максимально русский;
- standard acronyms (SIEM, XDR, SOAR, TTP, SDK) — сохранять;
- English terms оставлять только там, где они реально полезны для professional vocabulary;
- при первом употреблении давать русскую форму + acronym/English term.

## Visual debt

Figures/tables в Chapter 2 отсутствуют, поэтому visual restoration для этой главы не требуется.

## Priority

`MEDIUM-HIGH`

Содержание переведено правильно, но mixed-language плотность заметно выше, чем в Chapter 1. Редакторская нормализация существенно улучшит цельность и читабельность v2.
