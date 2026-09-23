# Шпаргалка: Configuration Management

## Core model

~~~text
configuration as code
→ version control
→ declarative desired state
→ idempotent operations
→ target hosts
→ apply
→ report changes
→ verify
~~~

## Why CM

Shell-only administration tends toward snowflakes.

CM provides:
- reproducibility;
- history/audit trail;
- shared documentation;
- targeting/orchestration;
- consistent desired state.

## Common primitives

- operations/modules/states;
- parameters;
- variables;
- facts/grains;
- handlers/change reactions;
- dependencies;
- packages/repositories;
- environments;
- client registration.

## Idempotency

Safe repeated application is the design goal.

Prefer state-aware modules over raw shell commands when possible.

If a command has side effects that CM cannot infer, treat it as operationally risky.

## Ansible

~~~text
control node
→ SSH
→ Python on client
→ tasks/playbooks/roles
~~~

Key elements:
- inventory;
- playbooks;
- roles;
- variables/facts;
- handlers;
- tags;
- Jinja templates.

Run:
~~~bash
ansible-playbook example.yml
~~~

For debug scope, chapter recommends tags and limiting execution to a test host.

## Ansible security

Two credential boundaries:
- remote SSH access;
- privilege escalation.

Do not collapse them into one unrestricted credential.

Private SSH keys:
- protect with passphrase;
- do not store in configuration repo;
- use ssh-agent/ssh-add for session access.

Ansible Vault:
- encrypted YAML/INI data;
- --ask-vault-pass for interactive use;
- password-file mode is less secure.

## Salt

~~~text
salt-master
↔ TCP 4505/4506
↔ salt-minion
~~~

New minion:
- configure master;
- restart minion;
- explicitly approve key;
- then test communication.

## Grains vs pillar

Grains:
- originate from minion;
- describe system/facts.

Pillar:
- generated master-side;
- host-specific configuration;
- minions should not see each other's pillar.

Inspect:
~~~bash
salt <minion> grains.items
salt <minion> pillar.items
~~~

## Salt state model

~~~text
top.sls
→ target matching
→ state files
→ state functions
→ desired state
~~~

Run one state:
~~~bash
salt <minion> state.apply <state-file>
~~~

Run highstate:
~~~bash
salt <minion> state.apply
salt '*' state.highstate
~~~

## Targeting

Salt supports:
- ID glob/regex/list;
- grains;
- pillar;
- IP/CIDR;
- compound expressions.

Always verify target expression before large apply.

## Environments

Both configuration and pillar trees can have environment-specific roots.

Use environments deliberately; production/test separation should also align with security boundaries.

## Ansible vs Salt

Ansible:
- agentless;
- SSH/Python;
- easier initial deployment;
- flexible credential design;
- slower at large scale.

Salt:
- master/minion;
- faster execution;
- easier large-scale fan-out;
- master is a high-value security target.

## Repository discipline

- keep one authoritative config repo;
- version everything;
- define hierarchy and ownership;
- separate files by purpose;
- avoid hidden manual changes;
- review third-party roles/formulas;
- encrypt secrets before VCS.

## Safe rollout

~~~text
change code
→ review
→ test on representative system
→ limited rollout
→ inspect results
→ staged expansion
→ production acceptance
~~~

Never use production as first test.

## Drift rule

A CM-managed host should not contain manual changes that cannot be reproduced from the repository.

If emergency manual work occurs:
- capture it;
- translate it into CM code;
- reconcile host to managed state.

## CM vs deployment

Chapter boundary:
- CM is strong at machine state;
- coordinated software deployment is a different problem domain.

Do not overload one tool merely because it can execute commands.

## Security checklist

- dedicated/hardened control node;
- narrow credentials;
- encrypted secrets;
- no private keys in repo;
- explicit Salt key approval;
- separate trust zones;
- audited third-party content;
- staged changes.

## Rollback

Preferred:
~~~text
known-good Git revision
→ re-apply desired state
→ verify
~~~

If no known-good baseline exists: [Needs confirmation].
