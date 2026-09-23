# Шпаргалка: краткая история системного администрирования

## 1. Canonical scope

Source title:
`Краткая история системного администрирования`

В книге раздел ненумерованный.
В biblioteka-vsp он оформлен как canonical chapter 32.

## 2. Timeline

~~~text
1952–1960  system operators
1961–1969  time-sharing
1969–1973  birth of UNIX
1974–1990  UNIX spreads / BSD / networking
1980s      system administrator profession
1987+      documentation / training / conferences
1991–1995  BSD uncertainty / Linux emergence
1996–1999  Windows growth
2000–2009  mixed-platform operations
2010–book  virtualization / cloud / hyperscale
future     IoT management
~~~

## 3. System operator → administrator

Early model:
~~~text
one expensive machine
→ one specialized workload
→ operator
~~~

Later model:
~~~text
general-purpose multiuser system
→ many workloads/users
→ administrator
~~~

## 4. SHARE lesson

Early IBM operators shared:
- experience;
- programs;
- migration knowledge.

Pattern:
~~~text
platform complexity
→ peer community
→ shared operational knowledge
~~~

## 5. Time-sharing

Time-sharing changes the computer from a single-purpose tool into a shared interactive platform.

Operational consequence:
- more users;
- more workloads;
- more persistent shared state;
- broader administration role.

## 6. UNIX origin

Chapter narrative:
- Multics influences the environment;
- Bell Labs exits the project;
- Thompson/Ritchie and colleagues pursue a simpler system;
- PDP-7 becomes an early platform;
- UNIX evolves rapidly.

## 7. UNIX philosophy

~~~text
one tool
→ one task well

tools
→ compose

text streams
→ common interface
~~~

The pipe connects program output to program input.

## 8. Early command set

Named in the chapter:
- as;
- cal;
- cat;
- chdir;
- chmod;
- chown;
- cmp;
- cp;
- date;
- dc;
- du;
- ed.

Later pipeline discussion names:
- grep;
- who.

Modern syntax/options:
[Needs confirmation] from this chapter.

## 9. UNIX spreads

Key narrative:
- publication and academic adoption;
- source-code distribution;
- John Lions documentation;
- Berkeley UNIX / BSD;
- Bill Joy;
- CSRG;
- TCP/IP sockets;
- SunOS;
- AT&T System V.

## 10. Why sysadmins emerge

General-purpose systems need people who can:
- adapt systems to users/applications;
- troubleshoot hardware/software;
- maintain storage/backups;
- create tools/processes;
- support users.

The role becomes broad rather than single-machine operation.

## 11. University ecosystem

The chapter identifies universities as important centers for:
- UNIX use;
- administrator training;
- peer networks;
- experimentation.

Evi Nemeth is presented as a major community figure.

## 12. Profession creates its own tools

The chapter explicitly mentions:
- processes;
- standards;
- policies/instructions;
- tools such as sudo.

Exact sudo usage is not documented here.

## 13. Documentation and training

Professionalization increases demand for:
- practical documentation;
- books;
- conferences;
- training.

Chapter mentions:
- O'Reilly;
- LISA;
- SANS;
- UNIX System Administration Handbook.

Current status of organizations/events:
[Needs confirmation].

## 14. BSD / Linux transition

Narrative:
- commodity PC hardware becomes practical;
- BSDI demonstrates production UNIX on PCs;
- AT&T/BSDI litigation creates uncertainty;
- Linux emerges;
- Linux distributions spread.

Treat causal judgments as authors' historical narrative.

## 15. Transferable skills

~~~text
UNIX operational experience
→ Linux operational experience
~~~

Durable lesson:
platforms change faster than core administration skills.

## 16. Windows era

1990s:
- Windows NT grows;
- platform rivalry intensifies;
- UNIX/Linux admins learn Windows;
- organizations reassess platform choices.

## 17. Mixed-platform era

2000–2009:
~~~text
UNIX + Linux + Windows
→ choose by workload / organization need
~~~

Book-era TCO claims are historical context:
[Needs confirmation] for modern comparison.

## 18. Cloud era

2010–book publication:
- virtualization;
- cloud;
- API-driven infrastructure;
- standardization;
- automation;
- fleets instead of hand-managed individual servers.

## 19. Modern skill shift in chapter

Administrator needs:
- infrastructure creation/scaling;
- DevOps collaboration;
- scripting/automation;
- monitoring;
- calm response to large-scale failures.

## 20. IoT extension

Networked devices still need:
- security;
- performance management;
- availability;
- patching/monitoring planning.

Small size does not remove operational responsibility.

## 21. Publication-era prediction boundary

The chapter cites a prediction for IoT device counts by 2020.

Do not treat it as verified outcome.

Status:
[Needs confirmation].

## 22. Enduring principles

~~~text
serve users
+ understand systems
+ preserve reliability
+ share knowledge
+ adapt tooling
+ automate for scale
= system administration
~~~

## 23. What changed most

Unit of management:

~~~text
single machine
→ shared host
→ networked systems
→ heterogeneous estate
→ virtualized fleet
→ cloud / distributed devices
~~~

## 24. What changed least

Administrator still has to:
- understand dependencies;
- diagnose failures;
- protect availability;
- communicate;
- learn continuously.

## 25. Interpretation boundary

This is a historical narrative, not:
- a current market report;
- a complete history of computing;
- a current product comparison;
- modern CLI documentation.

Use it to understand lineage and recurring operational ideas.
