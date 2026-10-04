# Шпаргалка: Chapter 1 — от локального симптома к реальному incident scope

## Symptom / problem framing

Исходный симптом:

- Docker не может занять TCP/8080;
- на workstation уже работает неизвестный процесс `ms`;
- второй процесс `ssupd` слушает `0.0.0.0:9150`;
- родитель — `gilded-sdk-update`;
- update script обфусцирован.

На этом этапе подтверждено только наличие подозрительной activity на одной workstation.

Критическая ошибка — интерпретировать локальную очистку как доказательство того, что весь incident завершён.

## Baseline / context

Workstation принадлежит cloud solutions architect и имеет legitimate developer access.

В главе attacker получает с неё:

- SSH private key;
- `known_hosts`;
- database credential;
- AWS credentials.

Workstation имеет доступ к:

- internal development servers;
- CI/CD runner;
- AWS account;
- S3 buckets.

Поэтому blast radius определяется не только процессами на endpoint, но и trust relationships.

## Read-only checks

### Локальная activity

```bash
ss -natp | grep LISTEN | grep 8080
ps -f 18450
ps -f 18449
ps --ppid 18449 -f
ss -natp | grep LISTEN | grep -E "ms|ssupd|gilded-sdk-update"
cat /opt/gilded/SDK/setup/gilded-sdk-update
```

Что дают:

- listening ports;
- PID/PPID relationship;
- связанные child processes;
- exposure listener на `0.0.0.0`;
- содержимое installer/update script.

### После события

```bash
ps -ef | grep -E "ms|ssupd|gilded"
ls -la /opt/gilded/
ss -natp | grep -E "8080|9150"
journalctl --since "6 days ago" | grep -i "gilded\|ssupd\|ms.*8080"
journalctl --since "Apr 07 16:34" --until "Apr 07 16:42" | grep -i "connect\|network\|tcp"
crontab -l -u jm
ls -la /etc/systemd/system/ | grep -i "gilded\|ssupd\|ms"
ls -la /home/jm/.config/autostart/ 2>/dev/null
```

Эти проверки подтверждают состояние workstation и historical activity.

Они не подтверждают отсутствие compromise вне workstation.

## Interpretation

### Что означают локальные признаки

`ms` на `127.0.0.1:8080`:

- локальный web service;
- доступен процессам на victim host.

`ssupd` на `0.0.0.0:9150`:

- listener на всех interfaces;
- в кейсе это Tor/SOCKS component;
- attacker использует его как pivot.

Обфусцированный installer:

- повышает подозрительность;
- сам по себе не определяет полный impact.

### Почему "clean host" недостаточно

В кейсе attacker до локальной cleanup уже:

- скачал SSH keys;
- использовал SOCKS tunnel;
- подключился к internal servers;
- собрал дополнительные credentials;
- использовал AWS credentials;
- получил доступ к S3;
- создал EC2 instance;
- staging/exfiltration уже произошли.

Следовательно:

```text
no process ≠ no attacker access
no persistence on host ≠ no persistence elsewhere
clean malware scan ≠ incident closed
```

## Next action

После подтверждения unauthorized SDK activity глава явно показывает необходимость расширить scope.

Проверить направления:

1. Использовались ли stolen credentials вне workstation.
2. Использовались ли SSH keys на других systems.
3. Какие internal systems были reachable через victim workstation.
4. Какие AWS actions выполнялись Jordan credentials.
5. Были ли созданы attacker-controlled cloud resources.
6. Какие S3/data resources были accessed.
7. Ставили ли тот же Gilded Freight SDK другие developers.

Глава не даёт конкретных CLI-команд для всех этих проверок. Добавлять их из model memory нельзя.

## Modifying action

### Jordan: остановка процессов

```bash
killall ms ssupd gilded-sdk-update
```

Effect:

- останавливает обнаруженные процессы на workstation.

Risk:

- может уничтожить часть live evidence;
- не отзываются уже украденные credentials;
- не удаляются attacker resources вне workstation.

Verification, показанная в главе:

```bash
ps -ef | grep -E "ssupd|gilded|ms"
```

Rollback: `[Needs confirmation]`.

### Jordan: удаление SDK tree

```bash
sudo rm -fr /opt/gilded/
```

Effect:

- удаляет локальное дерево Gilded SDK.

Risk:

- destructive action;
- удаляет потенциальные forensic artifacts;
- не влияет на downstream compromise.

Verification:

- позже `ls -la /opt/gilded/` возвращает отсутствие каталога.

Rollback: `[Needs confirmation]`.

### Attacker-side state changes

В главе attacker создаёт EC2 instance и копирует туда данные. Эти действия описаны для понимания compromise chain и не являются defensive recommendation.

## Verification / acceptance checks

### Host-level acceptance

Source показывает:

- processes отсутствуют;
- `/opt/gilded/` отсутствует;
- ports 8080/9150 не слушаются;
- persistence locations не показывают artifacts;
- malware scan без findings.

Это достаточно только для вывода:

**"на workstation не видно текущей activity этого implant"**.

### Incident-level acceptance

Глава показывает, что host-level acceptance была ошибочно принята за incident closure.

Перед closure должны быть исследованы downstream paths, прямо названные в разделе `What Remained`:

- other developer installations;
- AWS/CloudTrail activity Jordan credentials;
- SSH key use;
- attacker-created EC2 resource;
- stolen/active database credentials.

Полный universal exit criterion в Chapter 1 не формализован — `[Needs confirmation]`.

## Rollback

| Action | Rollback |
|---|---|
| `killall ms ssupd gilded-sdk-update` | `[Needs confirmation]` |
| `sudo rm -fr /opt/gilded/` | `[Needs confirmation]` |
| malware scan | `[Not applicable]` для показанного результата |
| attacker-created EC2 / copied data | defensive rollback procedure в Chapter 1 не описана |

## Главная памятка

Когда найден suspicious endpoint activity:

```text
1. Подтвердить факт
2. Не путать initial host со всем scope
3. Определить credentials и trust paths
4. Проверить downstream use
5. Проверить cloud / internal systems / same software
6. Только затем решать, что incident containment достаточен
```
