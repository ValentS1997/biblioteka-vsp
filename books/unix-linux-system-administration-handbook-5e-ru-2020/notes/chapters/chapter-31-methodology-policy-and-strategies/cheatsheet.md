# Шпаргалка: Methodology, policy and strategies

## 1. DevOps model

~~~text
business goal
→ shared Dev/Ops ownership
→ automation
→ measurement
→ sharing
→ continuous improvement
~~~

DevOps is a methodology, not one person, role or tool.

## 2. CLAMS

~~~text
C = Culture
L = Lean
A = Automation
M = Measurement
S = Sharing
~~~

## 3. Culture

Source-supported practices:
- Dev and Ops share responsibility;
- service launch requires automated testing and monitoring;
- code and infrastructure reviews cross team boundaries;
- dev/test/prod should remain aligned;
- shared ChatOps channel supports common context.

Avoid territorial ownership and blame.

## 4. Lean

Ask:
~~~text
What can we do today?
~~~

Prefer incremental progress and real-time coordination over process for process's sake.

## 5. Automation rules

~~~text
Repeated more than twice?
→ automate

Not understood?
→ do not automate
~~~

Automate:
- provisioning;
- configuration;
- promotion;
- testing;
- patch/update deployment.

## 6. Tool-selection rule

~~~text
problem/process
→ choose tool
~~~

Not:
~~~text
tool
→ search for problem
~~~

## 7. Measurement

Measure across:
- business;
- app;
- database;
- subsystem;
- server;
- network.

Metric must have:
- owner/context;
- nominal target;
- anomaly investigation path.

## 8. Sharing

Reduce knowledge silos through:
- wiki;
- presentations;
- demos;
- training;
- conferences/publications.

## 9. System administrator in DevOps

Responsibilities include:
- infrastructure automation;
- patch/security operations;
- CI/CD/monitoring support;
- troubleshooting;
- capacity planning;
- vendor coordination;
- lifecycle management;
- cross-team collaboration.

## 10. Ticket workflow

~~~text
request
→ acknowledge
→ human review
→ clarify
→ one owner
→ prioritize
→ resolve
→ searchable history
~~~

Every task should have one clear owner.

Ownership ≠ blame.

## 11. Ticket metrics

Chapter examples:
- open-ticket count;
- mean close time;
- unresolved percentage;
- workload distribution.

## 12. Dispatcher pattern

Experienced rotating dispatcher:
- watches queue;
- gathers context;
- prioritizes;
- assigns by skill/time;
- tracks completion.

## 13. Documentation value

Documentation reduces:
- single-person dependency;
- rediscovery;
- architecture drift.

It improves:
- reproducibility;
- onboarding;
- consistency;
- maintainability.

## 14. Documentation style

Prefer:
- short focused pages;
- overview first;
- detail by separate page;
- searchable/indexed repository;
- templates;
- comments near configuration.

## 15. One source of truth

~~~text
authoritative source
→ derived copies generated/synchronized
~~~

Avoid multiple manually maintained copies.

## 16. Infrastructure as code

~~~text
desired configuration
→ version control
→ automated application
→ environment comparison
→ change history
~~~

IaC acts as executable documentation.

## 17. Environment separation

~~~text
development
→ test
→ production
~~~

Separate, but as identical as practical.

Promote the same tracked change through stages.

## 18. Production-change ideal

Chapter's desired direction:
- humans avoid direct production admin changes;
- automated tracked process performs change;
- lower environments validate first;
- audit history identifies author/change.

Exact implementation:
[Needs confirmation].

## 19. Disaster recovery

~~~text
assets
→ threats
→ consequences
→ priorities
→ recovery strategy
→ staffing
→ exercise
~~~

## 20. Replication is not backup

~~~text
failover / mirroring
≠ backup
~~~

Keep independent recovery copies.

## 21. DR plan structure

Chapter / NIST-derived:
- purpose/scope;
- operating concept;
- notification/activation;
- recovery sequence;
- return to normal.

Current NIST revision:
[Needs confirmation].

## 22. Offline recovery kit

Keep locally accessible:
- contacts;
- recovery steps;
- backup info;
- network maps;
- cloud access details;
- installation media;
- license/configuration data;
- startup order.

Protect sensitive contents.

## 23. DR leader

Choose someone able to:
- decide with incomplete information;
- communicate clearly;
- coordinate people;
- act under pressure.

Plan for staff absence.

## 24. Security incident planning

Before incident define:
- who leads;
- who communicates;
- legal contacts;
- recovery actions;
- traffic/scale contingencies.

## 25. Policy vs procedure

~~~text
Policy = what is required
Procedure = how it is done
~~~

Policy changes slowly.
Procedure changes with systems/tools.

## 26. Policy areas

Examples:
- information security;
- access;
- assets;
- data classification;
- personnel security;
- physical security;
- incident management;
- business continuity;
- retention;
- privacy.

## 27. SLA

SLA should define:
- service scope;
- support hours;
- response expectations;
- supported environments;
- queue priorities;
- measurable success.

Write for nontechnical users.

## 28. Queue priority

Chapter simplified order:
1. many users cannot work;
2. one user cannot work;
3. enhancement request.

Lower priorities commonly FIFO.

Environment-specific severity model:
[Needs confirmation].

## 29. SLA metrics

Examples:
- on-time/on-budget projects;
- SLA objectives met;
- uptime;
- tickets resolved;
- mean resolution time;
- security incidents handled per procedure.

## 30. Compliance

Chapter surveys:
- CJIS;
- COBIT;
- COPPA;
- FERPA;
- FISMA;
- GLBA;
- HIPAA;
- ISO 27001/27002;
- NERC CIP;
- PCI DSS;
- ITIL;
- SOX ITGC;
- NIST 800-53;
- NIST 800-34.

Current applicability/version:
[Needs confirmation].

## 31. Legal / privacy

Operational rule:
~~~text
requirement
→ written policy
→ communicate
→ acknowledge where required
→ enforce consistently
→ retain auditable record
~~~

Current law is jurisdiction/time dependent:
[Needs confirmation].

## 32. Licensing

If a license mismatch is discovered:

~~~text
document
→ escalate in writing
→ request written response
→ preserve record
~~~

Do not silently normalize unlicensed use.

## 33. Acceptance checklist

Mature operations should have:
- shared ownership;
- understood automation;
- tests/monitoring before production;
- ticket ownership;
- searchable history;
- protected documentation;
- versioned infrastructure/configuration;
- dev/test/prod separation;
- traceable promotion;
- DR plan and offline dependencies;
- policy/procedure separation;
- measurable SLA;
- current compliance validation.
