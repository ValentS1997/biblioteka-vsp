# Команды главы 4

Команды основаны только на RAG главы 4. Network namespace operations изменяют host networking state, поэтому read-only checks отделены от modifying actions.

## Read-only checks

| Команда | Что показывает | Risk | Acceptance |
|---|---|---|---|
| `ip netns list` | Existing network namespaces | read-only | список или пустой output |
| `ip link list \| grep veth` | veth interfaces в текущем namespace | read-only | matching interfaces или пусто |
| `ip netns exec <ns> ip link \| grep veth` | veth внутри target namespace | read-only | target veth visible |
| `ip netns exec <ns> ip addr show` | Interfaces/IP внутри namespace | read-only | assigned IP + link state |
| `ip netns exec <ns> ping <ip>` | L3 reachability между namespaces | active network probe | ICMP replies / loss statistics |
| `ip addr` | Host interfaces | read-only | в Docker example виден `docker0` |

## Create network namespaces

```bash
ip netns add mynetspace
ip netns add mynetspace1
```

Effect: создаёт два isolated network namespaces.

Verification:

```bash
ip netns list
```

Rollback:

```bash
ip netns del mynetspace
ip netns del mynetspace1
```

## Create veth pair

```bash
ip link add veth0 type veth peer name veth1
```

Effect: создаёт full-duplex virtual Ethernet pair в current network namespace.

Verification:

```bash
ip link list | grep veth
```

Rollback до перемещения в namespaces: отдельная delete-command в главе не приводится: `[Needs confirmation]`.

После перемещения cleanup достигается удалением namespaces в лабораторном workflow главы.

## Move veth endpoints into namespaces

```bash
ip link set veth0 netns mynetspace
ip link set veth1 netns mynetspace1
```

Effect: interfaces исчезают из host namespace и переходят в target namespaces.

Verification host-side:

```bash
ip link | grep veth
```

В примере output пустой.

Verification namespace-side:

```bash
ip netns exec mynetspace ip link | grep veth
ip netns exec mynetspace1 ip link | grep veth
```

Rollback: глава не показывает move-back command; cleanup лаборатории — delete namespaces.

## Assign IP addresses

```bash
ip netns exec mynetspace ip addr add 10.0.0.15/24 dev veth0
ip netns exec mynetspace1 ip addr add 10.0.0.16/24 dev veth1
```

Effect: добавляет IPv4 addresses interfaces.

Verification:

```bash
ip netns exec mynetspace ip addr show
ip netns exec mynetspace1 ip addr show
```

Rollback command для удаления addresses отдельно не приводится: `[Needs confirmation]`.

## Bring interfaces up

```bash
ip netns exec mynetspace ip link set veth0 up
ip netns exec mynetspace1 ip link set veth1 up
```

Effect: меняет link state на UP.

Verification: `ip addr show` внутри каждого namespace.

Rollback для DOWN state в источнике не показан: `[Needs confirmation]`.

## Connectivity check

From namespace A:

```bash
ip netns exec mynetspace ping 10.0.0.16
```

From namespace B:

```bash
ip netns exec mynetspace1 ping 10.0.0.15
```

Effect: отправляет ICMP echo probes.

Acceptance в примере: replies without packet loss.

## Cleanup namespaces

```bash
ip netns del mynetspace
ip netns del mynetspace1
```

Effect: удаляет созданные network namespaces и связанные с лабораторией interfaces.

Verification:

```bash
ip netns list
```

Acceptance: created namespaces absent.

Rollback: recreating namespaces manually; state inside deleted namespaces is not preserved by this chapter workflow.

## Docker bridge observation

```bash
ip addr
```

Read-only. Источник демонстрирует host interfaces и default bridge `docker0`.

## Safety boundary

- `ip netns add/del` и `ip link set` изменяют host network namespace state.
- Не выполнять команды на production host без понимания namespace/interface ownership.
- Глава не задаёт production rollout/rollback procedure; это учебный isolated lab.
