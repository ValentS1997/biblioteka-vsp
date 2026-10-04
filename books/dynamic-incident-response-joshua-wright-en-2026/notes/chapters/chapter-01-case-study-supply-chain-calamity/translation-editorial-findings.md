# Translation / editorial findings — Chapter 1

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0027:c01`–`p0043:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-01-case-study-supply-chain-calamity.md`.

## Итог проверки

- Крупных непреведённых narrative-блоков не обнаружено.
- Сюжет, technical sequence и causal chain сохранены.
- Основные проблемы Chapter 1 — не смысловые, а редакционные:
  - mixed-language prose;
  - отдельные кальки;
  - один заметный typo в заголовке;
  - несколько фраз, которые можно сделать естественнее без потери technical precision.
- Figures 3–6 отсутствуют как visual assets в текущем русском PDF и остаются отдельным v2 visual debt.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `## Pivot в облако` | смешанный заголовок | `## Переход в облачную среду` |
| `## Экcфильтрация` | typo / вероятно смешение кириллической и латинской `c` | `## Эксфильтрация` |
| `Сбор credentials на сервере разработки` | mixed-language | `Сбор учётных данных на сервере разработки` |
| `CI/CD runner с доступом к build pipeline` | mixed-language, читается рвано | `CI/CD runner с доступом к конвейеру сборки` |
| `Строка подключения к production-базе с read-only credentials` | mixed-language | `Строка подключения к production-базе с учётными данными только для чтения` |
| `Ни cron job, ни systemd service, ни Linux desktop autostart entry.` | наиболее заметный редакционный дефект главы | `Не обнаружено ни заданий cron, ни служб systemd, ни записей автозапуска рабочего стола Linux.` |
| `endpoint detection watch list` | mixed-language | оставить technical term только если он закреплён glossary; иначе `список наблюдения endpoint detection` |

## Terminology decisions for v2

Следует принять единый book-level policy для recurring terms:

- credentials → `учётные данные` в narrative prose; English допустим в code/field names;
- pivot → `переход / точка перехода` либо сохранять English только как established term;
- runner → либо `runner`, либо `раннер` — единообразно по всей книге;
- build pipeline → `конвейер сборки` или `build pipeline` — выбрать один style;
- endpoint / endpoint detection → сохранить English там, где перевод ухудшает точность, но не смешивать формы внутри одной фразы.

## Visual debt

В Chapter 1 source содержит:

- Figure 3 — Server-Side Stealer Notification Console;
- Figure 4 — Victim MiniServe Filesystem View;
- Figure 5 — Compromised NovaRise Assets;
- Figure 6 — NovaRise Breach Investigation Gaps.

Canonical RAG содержит captions и surrounding text, но не самостоятельные image objects.

Для v2:

- repository-safe edition: rights/provenance decision по каждой figure;
- illustrated study edition: восстановить изображения из source PDF с переведёнными captions, если используется private/self-study policy.

## Priority

`MEDIUM`

Chapter 1 уже хорошо читается и может использоваться для обучения.  
Главный v2 эффект здесь даст polishing, consistency и возврат visual context, а не переписывание перевода.
