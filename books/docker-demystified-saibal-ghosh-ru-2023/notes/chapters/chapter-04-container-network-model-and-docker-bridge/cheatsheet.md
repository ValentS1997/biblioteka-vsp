# Шпаргалка: CNM, namespaces, veth и docker0

## 1. CNM

```text
Sandbox
  └─ full network stack
      interfaces
      routes
      DNS
      firewall/network settings

Sandbox ─ Endpoint ─ Network ─ Endpoint ─ Sandbox
```

- Sandbox — изолированный network stack.
- Endpoint — соединяет sandbox с network.
- Network — medium, через который endpoints взаимодействуют.

## 2. Drivers

### Network drivers

Источник делит их на:

- built-in/native;
- third-party/external.

Встроенные:

| Driver | Смысл главы |
|---|---|
| `bridge` | Linux bridge на Docker host; containers могут общаться через bridge |
| `host` | container использует network host |
| `none` | container network stack без внешнего connectivity |
| `overlay` | multi-host network на Linux bridge + VXLAN |
| `MACVLAN` | Linux MACVLAN для соединения interfaces |

### IPAM

IP Address Management driver назначает subnet/IP address, если они не заданы извне.

## 3. Libnetwork

```text
Docker daemon
     ↓
  libnetwork
     ↓
network driver / IPAM driver
```

По главе libnetwork — реализация CNM и interface/library для network stack management.

## 4. Linux network namespace

Namespace — отдельный экземпляр network stack:

- network interfaces;
- routes;
- firewall rules;
- independent network devices/configuration.

Read-only check:

```bash
ip netns list
```

## 5. veth pair

```text
namespace A            namespace B
   veth0  <==========>   veth1
          full-duplex
```

veth pair — point-to-point full-duplex link. После перемещения endpoints в namespaces host namespace больше не показывает их обычным `ip link`.

## 6. Manual namespace lab

Create:

```bash
ip netns add mynetspace
ip netns add mynetspace1
```

Create veth:

```bash
ip link add veth0 type veth peer name veth1
```

Move:

```bash
ip link set veth0 netns mynetspace
ip link set veth1 netns mynetspace1
```

Assign IPs:

```bash
ip netns exec mynetspace ip addr add 10.0.0.15/24 dev veth0
ip netns exec mynetspace1 ip addr add 10.0.0.16/24 dev veth1
```

Bring links up:

```bash
ip netns exec mynetspace ip link set veth0 up
ip netns exec mynetspace1 ip link set veth1 up
```

Verify:

```bash
ip netns exec mynetspace ip addr show
ip netns exec mynetspace1 ip addr show
ip netns exec mynetspace ping 10.0.0.16
ip netns exec mynetspace1 ping 10.0.0.15
```

Cleanup:

```bash
ip netns del mynetspace
ip netns del mynetspace1
```

## 7. Why bridge

Point-to-point veth links do not scale well when many namespaces must communicate.

Instead:

```text
namespace A -- veth                                          Linux bridge
                    /
namespace B -- veth/
```

Linux bridge is described as a Layer-2 device / virtual switch in Linux kernel.

## 8. Docker bridge

```text
container A eth0
      |
    veth
      |
   docker0
      |
    veth
      |
container B eth0
```

Key points from chapter:

- Docker creates bridge on host automatically;
- default bridge is `docker0`;
- Docker bridge is based on Linux bridge;
- container side of veth is `eth0`;
- host-side name begins with `veth`;
- built-in IPAM assigns container IP address.

Read-only host check:

```bash
ip addr
```

Expected: interface `docker0` appears when Docker Engine provides default bridge.

## Acceptance

Нужно уметь объяснить:

- Sandbox / Endpoint / Network;
- libnetwork vs network driver vs IPAM driver;
- network namespace;
- veth pair;
- why point-to-point veth does not scale;
- Linux bridge as L2 virtual switch;
- relationship `eth0 ↔ veth ↔ docker0`;
- difference among bridge/host/none/overlay/MACVLAN as described in source.
