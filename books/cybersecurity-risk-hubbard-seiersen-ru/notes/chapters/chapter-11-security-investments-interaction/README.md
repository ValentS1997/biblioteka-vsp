# Глава 11. Насколько эффективно взаимодействуют мои вложения в безопасность?

**Книга:** Дуглас У. Хаббард, Ричард Сирсен — «Как оценить риски в кибербезопасности: лучшие инструменты и практики».  
**Book ID:** `cybersecurity-risk-hubbard-seiersen-ru` · **Глава:** 11 · **Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7.  
**Статус:** `RAG_GROUNDED`; анализ основан только на адресуемом каноническом RAG.

## Главная идея

После принятия инвестиционного решения измерения не заканчиваются. Глава показывает, как оценивать **совместную эффективность нескольких вложений в безопасность** через бизнес-аналитику и dimensional modeling.

Авторы предлагают моделировать операционную безопасность вокруг:
- **фактов** — наблюдаемых событий/состояний;
- **измерений** — времени, актива/ценности, риска и других описательных признаков;
- **совпадающих измерений** — общих ключей вроде даты и актива, позволяющих связывать разные security data marts;
- **процессных метрик** — survival/exposure time и accumulated snapshots.

Ключевой тезис: метрики должны позволять не только видеть состояние отдельного control, но и отвечать, **какие комбинации людей, процессов и технологий реально уменьшают риск**.

## Verified RAG boundary

| Поле | Значение |
|---|---|
| Source mode | `rag_only` |
| Начало | EPUB spine **43**, `OPS/ch1-41.xhtml`: «Глава 11. Насколько эффективно взаимодействуют мои вложения в безопасность?» |
| Продолжение/завершение | Spine **44**, `OPS/ch1-42.xhtml`: dimensional modeling, ПУКД, survival analysis, accumulated snapshots, финальные абзацы |
| Следующая глава | Spine **45**, `OPS/ch1-43.xhtml`: «Глава 12. Призыв к действию» |
| Addressable chunks | `e0043:c01–c02` (2), `e0044:c01–c06` (6): всего **8** |
| Boundary check | `e0045:c01` — начало главы 12 |
| Source SHA-256 | `43b5ec48fec54cf506d05b62975c8772978fc4fbbe2a97c97643d8c6ad054481` |
| Печатные страницы | `[Needs confirmation]`; EPUB spine не равен печатной странице |

## Карта главы

| Блок | Смысл | RAG |
|---|---|---|
| Operational metrics after investment | После вложений нужно измерять фактический результат и взаимодействие controls | `e0043:c01` |
| BI / dimensional modeling | Витрины данных строятся вокруг фактов и измерений | `e0043:c01–c02`, `e0044:c01` |
| Conformed dimensions | Общие измерения даты/актива позволяют cross-drill между security domains | `e0044:c01–c02` |
| Security facts | Security fact — событие или состояние; часто мера — наличие/отсутствие, а не деньги | `e0044:c02–c03` |
| KISS / decomposition boundary | Не строить универсальную модель заранее; добавлять признаки по реальной аналитической потребности | `e0044:c03` |
| ПУКД | Пример hidden data-stealing malware, не замеченного COTS security controls | `e0044:c03–c05` |
| Survival analysis | Измерение времени существования ПУКД до обнаружения/блокировки | `e0044:c04` |
| Security data mart for ПУКД | Связь mitigation, malware, HTTP, date, asset, vulnerability dimensions | `e0044:c04–c05` |
| Accumulating snapshot | Модель многоэтапных human/process workflows, например remediation / SDL / CI/CD | `e0044:c05–c06` |

## Dimensional model — базовые сущности

### Fact

Наблюдаемое событие или состояние: изменение firewall rule, блокировка intrusion-prevention system, состояние software на активе, обнаружение угрозы и т. п.

### Dimension

Описательные признаки, по которым задаются вопросы и выполняются drill-down/aggregation:
- date/time;
- asset/value;
- vulnerability/risk;
- mitigation/control;
- malware;
- HTTP/C2;
- process/ticket-related attributes.

### Conformed dimension

Одинаково определённый dimension, используемый несколькими marts. Наиболее важные примеры главы — **date/time** и **asset**. Это даёт возможность сравнивать controls across domains и связывать технические события с одним и тем же объектом ценности.

## Пример ПУКД и survival analysis

ПУКД — «повышенная угроза кражи данных»: data-stealing malware, не замеченное коммерческими security controls в момент появления.

Глава предлагает measuring survival curve: доля угроз, продолжающих существовать, против времени до обнаружения. Source example вводит KPI:
> улучшить на 20% эффективность поиска повышенных угроз, сохраняющихся 70 дней и более.

Это **пример source KPI**, не локальная цель/threshold.

Поля fact table примера включают `mit_id`, `mal_id`, `http_id`, `date_http_start_id`, `date_https_end_id`, `asset_id`, `vuln_id` (`e0044:c04–c05`).

## Process metrics / accumulating snapshot

Для процессов remediation и secure development authors предлагают accumulating snapshot: одна логическая запись на процесс/объект с несколькими датами и duration fields, которые обновляются по мере прохождения стадий. Такой подход позволяет измерять длительность каждой фазы и общий cycle time (`e0044:c05–c06`).

## Conditional artifacts

- Отдельного явно озаглавленного chapter-end «Заключения»/«Резюме» нет → `summary.md` не создаётся.
- Review/control questions/exercises отсутствуют → review-файлы не создаются.
- [source-findings.md](source-findings.md) создаётся из-за отсутствия original figures/tables как полноценных мультимодальных RAG-объектов и необходимости отделить logical data model от physical implementation.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

**Reading progress:** остаётся `planned`; canonical EPUB/RAG не изменяются.
