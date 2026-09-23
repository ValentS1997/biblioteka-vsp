# Команды и operational actions главы 31

Глава 31 — преимущественно организационная и процессная. Она упоминает Git, cron, Ansible, Salt, Puppet, Chef, Packer, Terraform и другие инструменты, но не даёт точных shell command lines, которые можно безопасно перенести как canonical CLI.

Не выдумывать команды из других глав.

## Operational reference

| Команда / действие | Назначение | Что проверить | Тип |
|---|---|---|---|
| Assign one ticket owner | Устранить неоднозначность ответственности | owner явно указан; задача не потеряна | state-changing |
| Human acknowledgement of new ticket | Подтвердить, что запрос прочитан и понят | user получил план/следующий шаг | workload-generating |
| Triage / dispatch ticket | Определить приоритет и исполнителя | impact, context, skills, workload | state-changing |
| Store configuration/IaC in version control | Сделать изменения трассируемыми | authoritative repository and history | state-changing |
| Promote change dev → test → prod | Проверить изменение до production | same change/config reaches each stage | state-changing |
| Revert problematic versioned change | Вернуть known-good change state | problematic change identified and bypassed/reverted | state-changing |
| Risk assessment | Подготовить DR priorities | assets, threats, consequences, service priority | read-only |
| DR exercise | Проверить, что recovery plan реально исполним | contacts, backups, procedures, restored service | workload-generating |
| Update policy | Изменить formal requirement | authority, review, communication, effective date | state-changing |
| Update procedure | Изменить implementation steps | still satisfies governing policy | state-changing |
| Change SLA / support target | Зафиксировать service expectation | target measurable and operationally achievable | state-changing |
| Document licensing/compliance concern | Preserve auditable escalation | issue and management response recorded | state-changing |

## Automation boundary

Chapter rules:

~~~text
task repeated more than twice
→ candidate for automation

process not understood
→ do not automate yet
~~~

Before automation:
- document current process;
- identify expected state;
- identify failure modes;
- define verification;
- define rollback.

After automation:
- version-control configuration/code;
- test in lower environment;
- monitor result.

Exact tool command:
[Needs confirmation].

## Infrastructure as code

Source-supported model:

~~~text
desired configuration
→ version control
→ automated application
→ compare system with standard
→ trace changes
~~~

Tools mentioned:
- Puppet;
- Ansible;
- Salt;
- Chef;
- Packer;
- Terraform;
- Git.

Exact commands are not supplied by this chapter.

## Environment promotion

State-changing workflow:

~~~text
versioned change
→ development
→ test
→ production
~~~

Preconditions:
- change recorded;
- lower environment exists;
- test/acceptance criteria defined;
- monitoring exists.

Verification:
- intended state reached;
- no unexpected regression;
- audit trail identifies the change.

Rollback:
- chapter describes identifying the problematic commit/change and temporarily bypassing/reverting it;
- exact VCS command: [Needs confirmation].

## Ticket ownership

State-changing action:
- assign exactly one owner/coordinator.

Verification:
- owner visible;
- request status visible;
- no duplicate uncoordinated effort.

Rollback:
- reassign ownership explicitly;
- preserve history.

Do not equate ownership with blame.

## Ticket dispatch

Dispatcher duties from chapter:
- review new tickets;
- request missing context;
- establish priority;
- select an appropriate assignee;
- track timely completion.

Exact ticket-system API/CLI:
[Needs confirmation].

## Documentation update

State-changing action:
- update authoritative documentation/configuration source.

Verification:
- document is searchable;
- affected users/admins can access it;
- obsolete duplicate copy is not treated as authoritative.

Rollback:
- version/history restore if supported;
- exact command: [Needs confirmation].

## DR risk assessment

Read-only planning action:

~~~text
asset
→ threat
→ consequence
→ service priority
→ mitigation/recovery need
~~~

Do not assume one plan covers every threat.

## DR exercise

Type:
- workload-generating and potentially disruptive.

Preconditions:
- approved scenario;
- responsible leader;
- communication path;
- backups/recovery media available;
- production impact bounded.

Verify:
- contacts work;
- offline information is accessible;
- recovery sequence is executable;
- restored system is tested;
- return-to-normal step is understood.

Rollback:
- terminate exercise and restore normal operations according to the local DR plan;
- exact technical commands: [Needs confirmation].

## Disaster-recovery data set

Keep accessible even if network services fail:
- contacts;
- recovery steps;
- backup inventory/schedule;
- network maps;
- cloud access data;
- software/license data;
- installation media;
- hardware/software configuration;
- startup/recovery order.

Security:
- recovery materials may contain highly sensitive credentials;
- exact storage/encryption/access design: [Needs confirmation].

## Policy change

Policy:
- defines requirement/rule.

Procedure:
- defines implementation.

Before changing policy:
- identify authority/stakeholders;
- check consistency with other policies;
- identify legal/compliance impact.

Verification:
- policy is published/communicated;
- procedures still implement it;
- exceptions/escalation are clear.

Rollback:
- restore prior approved policy if governance permits;
- exact governance workflow: [Needs confirmation].

## SLA change

Before changing:
- define service scope;
- support hours;
- response expectations;
- queue priority;
- measurable compliance indicators.

Verification:
- required telemetry/ticket data exists to calculate the target.

Rollback:
- return to prior agreed SLA only through the governing agreement process;
- exact process: [Needs confirmation].

## Legal/compliance action boundary

The chapter lists publication-era laws and standards, primarily U.S.-centric.

Do not turn these into present-day legal commands or compliance instructions.

Current:
- applicability;
- version;
- jurisdiction;
- retention requirement;
- notification requirement;
- audit scope;

are all [Needs confirmation] without current authoritative legal/compliance sources.

## Software-license concern

Source-supported process:

~~~text
identify license mismatch
→ document quantities/terms
→ escalate in writing
→ request written response
→ preserve record
~~~

Do not silently install or normalize unlicensed software.

## No exact shell CLI

This chapter does not provide canonical executable command lines for:
- Git;
- cron;
- Ansible;
- Puppet;
- Chef;
- Salt;
- Packer;
- Terraform;
- ticketing systems;
- DR tooling;
- policy/SLA systems.

Do not invent them.
