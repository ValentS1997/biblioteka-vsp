# Команды и классификация эффектов — глава 14 «Metasploit Fremework»

**Источник:** canonical RAG PDF **308–331**, chunks `p0308:c01`–`p0331:c01`, SHA-256 `fa3cfb6d7dc9af0354a5c908e606626629929ae54b646ca4eaaa11b7868eb1b9`. Книжная консоль `msf6`/Metasploit v6.3.4-dev — историческая демонстрация. Команды **не выполнялись**, текущая CLI-совместимость **[Needs confirmation]**.

## Локальная справка / просмотр метаданных

| Команда внутри `msfconsole` | Эффект в описании автора | RAG |
|---|---|---|
| `help` / `help search` | **Read-only information:** общий help и сведения о поиске | [p0309:c01](../../../rag/chunks/p0301-p0400/p0309-c01.md), [p0324:c01](../../../rag/chunks/p0301-p0400/p0324-c01.md) |
| `version` | **Read-only information:** версия Framework и Console | [p0324:c01](../../../rag/chunks/p0301-p0400/p0324-c01.md) |
| `show auxiliary` | **Read-only inventory:** каталог вспомогательных модулей | [p0311:c01](../../../rag/chunks/p0301-p0400/p0311-c01.md) |
| `show encoders` | **Read-only inventory:** список encoders | [p0320:c01](../../../rag/chunks/p0301-p0400/p0320-c01.md), [p0321:c01](../../../rag/chunks/p0301-p0400/p0321-c01.md) |
| `show exploits` | **Read-only inventory:** список доступных exploitation modules, но не проверка состояния узла | [p0318:c01](../../../rag/chunks/p0301-p0400/p0318-c01.md) |
| `search` | **Read-only metadata search** по именам/описаниям модулей; без выполнения найденного | [p0310:c01](../../../rag/chunks/p0301-p0400/p0310-c01.md), [p0319:c01](../../../rag/chunks/p0301-p0400/p0319-c01.md) |
| `info` | **Read-only module metadata**, в том числе `Required`, defaults, description, supported targets | [p0312:c01](../../../rag/chunks/p0301-p0400/p0312-c01.md), [p0313:c01](../../../rag/chunks/p0301-p0400/p0313-c01.md) |
| `get` / `getg` | **Read-only state inspection** локального/глобального параметра; значения могут быть чувствительны | [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md), [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md) |

**Не требуется исполнять программу, чтобы использовать эту классификацию:** имена/описания получены из RAG. Любой показанный результат относится лишь к окружению автора.

## Контекстные и изменяющие состояние команды

| Команда/функция в книге | Класс воздействия / предупреждение |
|---|---|
| `msfconsole` | **Local process startup**; при запуске может обращаться к локальному состоянию/БД; не сетевое сканирование само по себе. [p0309:c01](../../../rag/chunks/p0301-p0400/p0309-c01.md) |
| `use`, `back` | **Local console/module context change**; выбор модуля сам по себе не эксплуатация, но контекст определяет последующее действие. [p0310:c01](../../../rag/chunks/p0301-p0400/p0310-c01.md), [p0312:c01](../../../rag/chunks/p0301-p0400/p0312-c01.md) |
| `set`, `setg`, `unset`, `unsetg` | **State-changing variables**; особенно рискованные `RHOSTS`, `RPORT`, `LHOST`, `LPORT`, `PAYLOAD`, `TARGET`. [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md) |
| `save` | **Local persistent file write**: сохраняет конфигурацию в `.msf4/config`; не публиковать секреты. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `makerc` | **Local persistent file write**: экспорт истории команд; может включать адреса/пароли и другие секреты. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `connect` | **Active network connection**, не read-only офлайн-операция; авторский публичный endpoint не проверялся повторно. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `route` | **Network-routing state/context**, просмотр/изменение маршрутов в книге; изменение направления доступа требует согласования. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `sessions` | **Post-exploitation session inventory**, может показывать реальные конфиденциальные сведения; не создавать такие сессии из этой коллекции. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `irb` | **Ruby interpreter / code execution capability**; доступ к интерпретатору не является простой справкой. [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) |
| `msfupdate` | **Software state-changing/update** в авторском тексте; современное существование команды **[Needs confirmation]**. [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md) |
| `run` в сетевых Auxiliary, `wmap_run` | **Active network workload**, включая scan/auth-check/fuzz; возможно изменение состояния и блокировки. Исполняемого сценария нет. [p0313:c01](../../../rag/chunks/p0301-p0400/p0313-c01.md)–[p0315:c01](../../../rag/chunks/p0301-p0400/p0315-c01.md), [p0327:c01](../../../rag/chunks/p0301-p0400/p0327-c01.md)–[p0328:c01](../../../rag/chunks/p0301-p0400/p0328-c01.md) |
| `exploit`, `generate`, `msfvenom`, Metasploit post/evasion | **High-risk exploitation / code generation / AV evasion / credential access**; нет готовых команд, конфигураций target/payload и исходного shellcode. [p0309:c01](../../../rag/chunks/p0301-p0400/p0309-c01.md), [p0315:c01](../../../rag/chunks/p0301-p0400/p0315-c01.md)–[p0324:c01](../../../rag/chunks/p0301-p0400/p0324-c01.md), [p0329:c01](../../../rag/chunks/p0301-p0400/p0329-c01.md)–[p0331:c01](../../../rag/chunks/p0301-p0400/p0331-c01.md) |

## Значения параметров, отмеченные источником

- TCP-scanner: `CONCURRENCY`, `DELAY`, `JITTER`, `PORTS`, `RHOSTS`, `THREADS`, `TIMEOUT` — менять только в разрешённой лаборатории и учитывать стоимость активных запросов. [p0313:c01](../../../rag/chunks/p0301-p0400/p0313-c01.md).
- FTP-auth: `PASS_FILE`, `USER_FILE`, `USERPASS_FILE`, `RHOSTS`, `RPORT`, `STOP_ON_SUCCESS`, `BRUTEFORCE_SPEED`, `THREADS` — секреты и интенсивность online guessing. **Не приводить исполняемую строку для атаки.** [p0314:c01](../../../rag/chunks/p0301-p0400/p0314-c01.md), [p0315:c01](../../../rag/chunks/p0301-p0400/p0315-c01.md).
- Payload: `Singles`, `Stagers`, `Stages`; `LHOST/LPORT`, `TARGET`, `PAYLOAD` упомянуты только как терминология конфигурации, без генерации байтов. [p0315:c01](../../../rag/chunks/p0301-p0400/p0315-c01.md)–[p0317:c01](../../../rag/chunks/p0301-p0400/p0317-c01.md), [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md).
- В исходнике **`USERS_PASS`** не совпадает с показанным параметром `USERPASS_FILE`, а **`LPPORT`** отличается от `LPORT` — реальные имена и версии подтверждать отдельно; никаких «исправленных» онлайн-guessing команд. [p0314:c01](../../../rag/chunks/p0301-p0400/p0314-c01.md), [p0315:c01](../../../rag/chunks/p0301-p0400/p0315-c01.md), [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md).

## Verification without exploitation

Читать уже полученный инвентарь стенда и сведения о модулях/их назначении, документировать допустимый scope, локально сверять параметры и дату демонстрации. Факты `OPEN` порта, HTTP 200/500, каталог модуля, rank/check и открытие Meterpreter в книге — **разные категории свидетельств**. Не переносить их в отчёт как доказательство актуальной уязвимости. [p0313:c01](../../../rag/chunks/p0301-p0400/p0313-c01.md), [p0328:c01](../../../rag/chunks/p0301-p0400/p0328-c01.md), [p0331:c01](../../../rag/chunks/p0301-p0400/p0331-c01.md).

**Rollback: [Needs confirmation]** — исходник не предлагает универсального восстановления после активной эксплуатации, блокировки аккаунтов или записи payload. [source-findings.md](source-findings.md).
