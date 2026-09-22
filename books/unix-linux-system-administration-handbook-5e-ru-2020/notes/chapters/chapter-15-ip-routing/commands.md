# Команды главы 15

Только команды и формы команд, подтвержденные RAG главы 15.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `netstat -rn` | Показать routing table numeric form | destinations, gateways, flags, interfaces | read-only |
| `ip route` | Показать Linux routing table | default route, connected prefixes, source/interface | read-only |
| `route` | Manual route-table command referenced by chapter | exact intended static route and resulting table | depends on subcommand |
| `routed -q` | Passive RIP mode: accept route updates without advertising own | daemon receives updates and does not broadcast its own | state-changing / daemon |
| `vtysh` | Connect to Quagga daemon CLI on Linux | intended daemon/router context | interactive control-plane |
| `quaggaadm` | Connect to Quagga daemon CLI on Solaris, as named by chapter | intended daemon/router context | interactive control-plane |
| `enable` | Enter privileged mode in Quagga/Cisco-style CLI | prompt changes to privileged mode; correct device | privilege-changing |
| `config term` | Enter configuration mode | prompt indicates config mode; correct device/context | state-changing gateway |
| `write` | Save Quagga daemon configuration | intended config file updated after verification | state-changing / persistent |
| `ssh acme-gw.acme.com` | Cisco IOS user access example | correct router identity and expected prompt | interactive / remote access |
| `show interfaces` | Cisco: inspect interfaces | interface list/state before change | read-only |
| `show ?` | Cisco: display help/options for show command | available inspection commands | read-only |
| `show running` | Cisco: display running/dynamic configuration | current live configuration | read-only |
| `show config` | Cisco: display stored/nonvolatile configuration in chapter terminology | compare stored vs running configuration | read-only |
| `enable` | Cisco: enter privileged EXEC mode | "#" prompt and correct router identity | privilege-changing |
| `config term` | Cisco: enter configuration terminal mode | "(config)#" prompt | state-changing gateway |
| `interface Ethernet0` | Cisco: select interface configuration context | correct target interface | state-changing context |
| `ip address 192.225.40.253 255.255.255.0` | Cisco example: change interface IPv4 address | address/mask and management reachability | state-changing / lockout-risk |
| `write mem` | Persist Cisco running configuration after successful change | saved config matches verified running state | state-changing / persistent |
| `hostname <name>` | Set Cisco router hostname | prompt/device identity is unambiguous | state-changing |
| `scp` | Transfer router configuration for backup/editing | backup file is complete and stored safely | read-only or state-changing by direction |
| `tftp` | Transfer router configuration for backup in chapter workflow | backup copy is retrievable | read-only or state-changing by direction |

## Read-only baseline

Linux/FreeBSD routing state:

~~~bash
netstat -rn
ip route
~~~

Cisco:

~~~text
show interfaces
show running
show config
~~~

Before any route/control-plane change capture:

- current routing table;
- current default route;
- directly connected networks;
- current router identity;
- running configuration;
- persistent configuration;
- management path.

## Route interpretation

Chapter model:

~~~text
destination
  ↓
specific matching route?
  ├─ yes → next hop/interface
  └─ no  → default route
             ↓
          next hop
~~~

Gateway must be reachable on a directly connected network.

## routed -q

Passive mode:

~~~text
receive RIP updates
do not advertise own updates
write learned routes into kernel table
~~~

Routes learned dynamically may expire if not refreshed.

Rollback exact daemon/service procedure: `[Needs confirmation]`.

## Quagga

Architecture:

~~~text
zebra
  ↕ kernel routing table
  ↕ protocol daemons:
     ripd
     ripngd
     ospfd
     ospf6d
     bgpd
~~~

CLI flow:

~~~text
vtysh
  ↓
enable
  ↓
config term
  ↓
configuration commands
  ↓
write
~~~

State-changing configuration syntax beyond forms explicitly supplied by chapter: `[Needs confirmation]`.

## Cisco IOS safe workflow

Read-only first:

~~~text
ssh <router>
show interfaces
show running
show config
~~~

Then privilege/configuration:

~~~text
enable
config term
interface Ethernet0
ip address <address> <mask>
~~~

Verification must happen before persistence.

Only after successful verification:

~~~text
write mem
~~~

Chapter explicitly advises keeping configuration backups using scp or tftp.

## High-risk boundaries

### enable

Does not itself change routing, but removes the user-mode safety boundary. Confirm router identity before proceeding.

### config term

Enters a mode where configuration commands modify live state.

### ip address ...

Can immediately break remote access if applied to the management-facing interface.

Required checks:
- correct router;
- correct interface;
- correct address/mask;
- recovery/console path;
- expected route changes.

Rollback exact command: `[Needs confirmation]`.

### write mem

Persists already-running state. Do not run until:
- route table is correct;
- required interfaces are reachable;
- end-to-end path works;
- no unintended route loss occurred.

## Backup / rollback

Chapter recommends backup copies of router configuration and version tracking.

Rollback principle:

~~~text
capture config
  ↓
make one controlled change
  ↓
verify
  ├─ success → persist
  └─ failure → restore prior config
~~~

Exact Cisco/Quagga restoration command is not supplied by chapter: `[Needs confirmation]`.
