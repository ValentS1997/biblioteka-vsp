# Команды главы 23

Только команды и формы команд, подтвержденные RAG главы 23.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| pip install ansible | Установить Ansible из PyPI | installed version/package availability | state-changing |
| ansible-playbook example.yml | Применить playbook | intended hosts, changed/failed results | workload-generating |
| ansible-playbook global.yml --ask-sudo-pass | Запустить playbook с запросом sudo password | privilege escalation works; failures isolated | workload-generating |
| ansible-galaxy install ANXS.postgresql | Установить external role из примера | role source/version/content reviewed | state-changing |
| ssh-keygen -p | Изменить passphrase SSH private key | key remains usable; new passphrase recorded safely | state-changing |
| ssh-agent | Запустить agent для private keys | socket/session lifetime | state-changing |
| ssh-add | Загрузить keys в agent | expected identities loaded | state-changing |
| tree /srv/salt | Показать Salt config tree | salt/pillar hierarchy | read-only |
| sudo salt <minion> grains.items | Показать grains | host facts used for targeting | read-only |
| sudo salt <minion> pillar.items | Показать pillar view | host-specific variables | read-only |
| sudo salt <minion> state.apply | Применить highstate | changed/failed states | workload-generating |
| sudo salt <minion> state.apply <state-file> | Применить один state file | targeted state only | workload-generating |
| sudo salt '*' state.highstate | Применить highstate ко всем matched minions | blast radius and per-minion result | workload-generating |
| sudo salt <minion> config.get environment | Проверить Salt environment | expected environment | read-only |
| sudo salt <minion> state.show_top | Показать resolved top.sls mapping | expected states/environment | read-only |
| service salt_minion restart | Перезапустить minion после config change | reconnect/registration | state-changing |

## Ansible Vault / credentials

Глава подтверждает:
- ansible-vault как механизм encrypted YAML/INI data;
- --ask-vault-pass для ansible-playbook/ansible;
- --vault-password-file для noninteractive use.

Exact full vault encryption command в доступном RAG не приведен: [Needs confirmation].

Security:
- private SSH keys не хранить в configuration repository;
- SSH credential и sudo credential не должны быть одним master credential;
- password-file снижает security и должен быть доступен только dedicated account.

## Salt key approval

RAG показывает команды salt-key, но OCR неоднозначно отображает короткие флаги:
- list unaccepted: token отображен как -1;
- approve all with confirmation: token отображен как -уА.

Поэтому executable normalized flag forms помечены [Needs confirmation] и не подменяются из model memory.

После approval source показывает connectivity test через Salt test module; OCR имени функции поврежден, exact token: [Needs confirmation].

## High-impact actions

ansible-playbook и Salt state application могут массово менять hosts.

Перед запуском:
1. проверить target set;
2. использовать representative test host/environment;
3. сохранить versioned baseline;
4. применить ограниченный scope;
5. проверить changed/failed output;
6. расширять rollout поэтапно.

Rollback:
- вернуть previous repository revision;
- повторно применить desired state;
- если previous revision/secret state не сохранены: [Needs confirmation].
