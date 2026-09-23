# Команды главы 15

Только команды и формы команд, подтвержденные RAG главы 15.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `netstat -rn` | Показать routing table numeric form | destinations, gateways, flags, interfaces | read-only |
| `ip route` | Показать Linux routing table | default route, connected prefixes, source/interface | read-only |
| `route` | Manual route-table command referenced by chapter | exact intended static route and resulting table | depends on subcommand |
| `routed -q` | Passive RIP mode: accept route updates without advertising own | daemon receives updates and does not broadcast its own; learned routes enter kernel table | state-changing |
| `vtysh` | Connect to Quagga daemon CLI on Linux | intended daemon/router context; connection alone does not alter config | read-only |
| `quaggaadm` | Connect to Quagga daemon CLI on Solaris, as named by chapter | intended daemon/router context; connection alone does not alter config | read-only |
| `enable` | Enter privileged mode in Quagga/Cisco-style CLI | prompt changes to privileged mode; correct device | state-changing |
| `config term` | Enter configuration mode | prompt indicates config mode; later config commands can modify live state | state-changing |
| `write` | Save Quagga daemon configuration | intended daemon configuration file is written | state-changing |
| `ssh acme-gw.acme.com` | Cisco IOS user access example | correct router identity and expected prompt | read-only |
| `show interfaces` | Cisco: inspect interfaces | interface list/state before change | read-only |
| `show ?` | Cisco: display help/options for show command | available inspection commands | read-only |
| `show running` | Cisco: display running/dynamic configuration | current live configuration | read-only |
| `show config` | Cisco: display stored/nonvolatile configuration in chapter terminology | stored configuration | read-only |
| `enable` | Cisco: enter privileged EXEC mode | `#` prompt and correct router identity | state-changing |
| `config term` | Cisco: enter configuration terminal mode | `(config)#` prompt; later commands can modify live state | state-changing |
| `interface Ethernet0` | Cisco: select interface configuration context | correct target interface | state-changing |
| `ip address 192.225.40.253 255.255.255.0` | Cisco example: change interface IPv4 address | target interface and address/mask; exact success criteria `[Needs confirmation]` | state-changing |
| `write mem` | Persist Cisco configuration after the change has succeeded | source says to save after success; exact acceptance checks `[Needs confirmation]` | state-changing |
| `hostname <name>` | Set Cisco router hostname | prompt/device identity is unambiguous | state-changing |
| `scp` | Copy router configuration for backup/editing in the chapter workflow | backup copy exists on another system; direction matters | read-only |
| `tftp` | Copy router configuration for backup | backup copy exists on another system | read-only |

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

The chapter provides these inspection points; using them as a pre-change baseline is a derived operational arrangement, not a quoted mandatory checklist:

- routing table (`netstat -rn`, `ip route`);
- current router identity (hostname/prompt);
- running configuration (`show running`);
- stored configuration (`show config`).

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

Source-supported checks are limited to identifying the correct router (hostname/prompt) and selecting the intended interface/address syntax. Exact pre-change recovery checks and rollback command: `[Needs confirmation]`.

### write mem

Persists the configuration. The chapter says to run it after the configuration change has succeeded. The exact acceptance-test sequence is `[Needs confirmation]`.

## Backup / rollback

Chapter recommends backup copies of router configuration and version tracking.

The chapter recommends backup copies of router configuration and version tracking, but it does not supply a restoration workflow.

Exact Cisco/Quagga rollback procedure and restoration command: `[Needs confirmation]`.
