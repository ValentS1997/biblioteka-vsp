# Команды главы 6

Команды основаны только на RAG главы 6. Network-changing actions могут нарушить connectivity, поэтому read-only checks отделены от modifying actions.

## Read-only / observation

| Команда | Что проверяет | Risk |
|---|---|---|
| `docker network ls` | Docker networks/drivers/scope | read-only |
| `docker container ls -a` / `docker ps` | Containers/published ports | read-only |
| `docker inspect <container> --format '{{ .NetworkSettings.SandboxKey }}'` | Docker netns path | read-only |
| `docker network inspect <network>` / `docker inspect <network>` | Network/IPAM/options | read-only |
| `ip addr` / `ifconfig` / `ip route` | Interfaces/addresses/routes | read-only |
| `ip netns list` | Linux-visible netns aliases | read-only |
| `iptables -t nat -L` | NAT rules | read-only |
| `ls -ltr /var/run/docker/netns` | Docker netns objects | read-only |
| `nsenter --net=$overlay_namespace ip link show` | Interfaces in overlay netns | read-only |
| `nsenter --net=$overlay_namespace ip neighbor show` | Neighbor table | read-only |
| `tcpdump -i eth0 port 4789` | VXLAN underlay traffic | packet capture |

## Default bridge

```bash
docker run -dit --name bbox busybox:latest
docker container ls -a
docker exec -it bbox sh
ip addr
```

Effect: creates/runs container on default bridge.

Verification: source container receives address in `172.17.0.0/16` and host sees veth attached to `docker0`.

Rollback:

```bash
docker container rm bbox --force
```

Risk: force-removes container.

## Expose Docker netns to ip netns

```bash
container_id=bbox
container_netns=$(docker inspect ${container_id} --format '{{ .NetworkSettings.SandboxKey }}')
ln -sv ${container_netns} /var/run/netns/${container_id}
ip netns list
```

Effect: creates symlink. Verification: alias appears in `ip netns list`. Rollback exact command absent: `[Needs confirmation]`.

## User-defined bridge

```bash
docker network create -d bridge mybridge
docker run -dit --name mybox3 --net mybridge busybox:latest
docker run -dit --name mybox4 --net mybridge busybox:latest
docker exec -it mybox3 sh
ping mybox4
```

Effect: creates network + containers. Acceptance: name-based ping succeeds.

## Host network

```bash
docker run -dit --name hostnet --network host busybox:latest
docker exec -it hostnet sh
ip addr
```

Effect: shares host network namespace. Risk: reduced network isolation.

## None network

```bash
docker run -dit --name nonenet --network none busybox:latest
docker exec -it nonenet sh
ifconfig -a eth0
```

Acceptance: no external `eth0` in source.

## NAT inspection

```bash
iptables -t nat -L
```

Read-only. Source shows bridge subnet MASQUERADE.

## Port publishing

```bash
docker run -dit --name test1 -P nginx:latest
docker ps
curl localhost:<assigned-port>
```

```bash
docker run -dit --name test2 -p 8080:80 nginx:latest
docker ps
```

```bash
docker run -dit --name test3 -p 8081:80/tcp -p 8081:80/udp nginx:latest
docker ps
```

Effect: publishes host ports. Risk: changes external exposure.

## MACVLAN bridge

Preflight:

```bash
ifconfig -a eth0
```

Create:

```bash
docker network create --driver=macvlan   --subnet=<subnet>/<prefix>   --gateway=<gateway>   --ip-range=<range>   -o parent=eth0 macvnet
```

Verification:

```bash
docker network ls
docker network inspect macvnet
```

Attach:

```bash
docker run -dit --name mymac --network macvnet busybox:latest
docker exec -it mymac sh
ip addr
ip route
```

Risk: consumes physical-subnet addresses and depends on upstream NIC/switch behavior.

## Host-side MACVLAN interface

```bash
ip link add macnet0 link eth0 type macvlan mode bridge
ip addr add <ip>/<prefix> dev macnet0
ip link set macnet0 up
```

Verification:

```bash
ip addr | grep mac
ping -c 5 <container-ip>
```

Rollback not specified in source: `[Needs confirmation]`.

## MACVLAN trunk

```bash
docker network create --driver=macvlan   --subnet=<subnet>/<prefix>   --gateway=<gateway>   --ip-range=<range>   -o parent=eth1.50 macvnet1
docker network inspect macvnet1
```

## Swarm overlay

Observe:

```bash
docker network ls
docker inspect ingress
```

Source demonstrates standalone attachment to ingress failing:

```bash
docker run -dit --name test_container --network ingress busybox:latest
```

Expected: permission error because ingress is not manually attachable.

Create custom attachable overlay:

```bash
docker network create --driver overlay --attachable my-overlay
docker run -dit --name test_container --network my-overlay busybox:latest
```

Verification:

```bash
ls -ltr /var/run/docker/netns
docker exec -it test_container sh
ip addr
```

## docker_gwbridge

```bash
docker inspect docker_gwbridge
```

Read-only. Source uses it to explain external connectivity and IP masquerade.

## Cross-host overlay

```bash
ping <remote-overlay-container-ip>
```

Acceptance: ICMP replies across hosts.

## VXLAN packet capture

```bash
tcpdump -i eth0 port 4789
```

Expected: VXLAN traffic encapsulating overlay packets.

Overlay namespace:

```bash
overlay_namespace=/var/run/docker/netns/1-<network-id>
nsenter --net=$overlay_namespace ip link show
nsenter --net=$overlay_namespace tcpdump -vv -epni any arp
nsenter --net=$overlay_namespace ip neighbor show
```

Expected: `br0`, `vxlan0`, veths and overlay IP↔MAC entries.

## Safety boundary

- Do not change `iptables` merely because source inspects it.
- `ip link`/`ip addr add` modify host networking.
- MACVLAN depends on physical network assumptions.
- Published ports change attack surface.
- Overlay creation changes Swarm distributed state.
