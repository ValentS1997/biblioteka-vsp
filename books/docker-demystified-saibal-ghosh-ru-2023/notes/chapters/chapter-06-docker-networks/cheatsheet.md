# Шпаргалка: Docker networks

## 1. Default networks

```bash
docker network ls
```

| Network | Driver | Mental model |
|---|---|---|
| `bridge` | bridge | isolated container network via `docker0` |
| `host` | host | share host network namespace |
| `none` | null | no external network interface |

## 2. Default bridge

```text
container
  eth0 172.17.0.x
    │
  veth pair
    │
 docker0 172.17.0.1/16
    │
 host NIC
```

Read-only:

```bash
docker exec -it <container> sh
ip addr
```

Container IP comes from Docker IPAM.

## 3. Docker network namespace

```bash
docker inspect <container> --format '{{ .NetworkSettings.SandboxKey }}'
```

Source path form:

```text
/var/run/docker/netns/<id>
```

Direct Linux check:

```bash
ip netns list
```

By default it does not show Docker namespaces because Linux tool expects `/var/run/netns`.

Source workaround:

```bash
container_id=<container>
container_netns=$(docker inspect ${container_id} --format '{{ .NetworkSettings.SandboxKey }}')
ln -sv ${container_netns} /var/run/netns/${container_id}
ip netns list
```

Effect: creates a host symlink. Rollback exact cleanup command is not shown in source.

## 4. Default vs user-defined bridge

Default bridge:
- container-to-container by IP works;
- source example says name-based ping does not.

User-defined bridge:

```bash
docker network create -d bridge mybridge
docker run -dit --name mybox3 --net mybridge busybox:latest
docker run -dit --name mybox4 --net mybridge busybox:latest
docker exec -it mybox3 sh
ping mybox4
```

Acceptance: name resolves and ICMP replies arrive.

## 5. Host network

```bash
docker run -dit --name hostnet --network host busybox:latest
docker exec -it hostnet sh
ip addr
```

Container shares host network stack and IP addresses. Source says port mapping parameters are ignored.

## 6. None network

```bash
docker run -dit --name nonenet --network none busybox:latest
docker exec -it nonenet sh
ifconfig -a eth0
```

Expected source result: no `eth0` external interface.

## 7. Share another container's network namespace

Source behavior:
- new container has its own processes/filesystem;
- no independent network stack;
- shares IP addresses and ports with existing container;
- communication can use loopback.

Exact Docker command syntax is absent in retrieved chapter RAG: `[Needs confirmation]`.

## 8. NAT / port mapping

```bash
iptables -t nat -L
```

Source shows POSTROUTING MASQUERADE for `172.17.0.0/16`.

Random publish:

```bash
docker run -dit --name test1 -P nginx:latest
docker ps
curl localhost:<assigned-port>
```

Explicit:

```bash
docker run -dit --name test2 -p 8080:80 nginx:latest
```

TCP + UDP:

```bash
docker run -dit --name test3 -p 8081:80/tcp -p 8081:80/udp nginx:latest
```

## 9. MACVLAN prerequisites from source

- Linux host;
- kernel ≥ 3.9, preferably ≥ 4.0;
- subnet matches parent;
- NIC in promiscuous mode;
- one MACVLAN network per parent interface in one subnet;
- IP range/auxiliary exclusions can be specified.

## 10. MACVLAN bridge

```bash
ifconfig -a eth0
docker network create --driver=macvlan   --subnet=<subnet>   --gateway=<gateway>   --ip-range=<range>   -o parent=eth0 macvnet
docker network inspect macvnet
docker run -dit --name mymac --network macvnet busybox:latest
docker exec -it mymac sh
ip addr
ip route
```

Source default behavior:
- containers in same MACVLAN communicate;
- host↔container direct communication via parent does not work by default.

## 11. Host-side MACVLAN link

```bash
ip link add macnet0 link eth0 type macvlan mode bridge
ip addr add <ip>/<prefix> dev macnet0
ip link set macnet0 up
ping -c 5 <container-ip>
```

Effect: changes host network state. Rollback is not explicitly specified: `[Needs confirmation]`.

## 12. MACVLAN trunk bridge 802.1Q

```bash
docker network create --driver=macvlan   --subnet=<subnet>   --gateway=<gateway>   --ip-range=<range>   -o parent=eth1.50 macvnet1
```

Difference: parent is VLAN subinterface.

## 13. Overlay / Swarm

Swarm provides `ingress` overlay and `docker_gwbridge` bridge.

```bash
docker network ls
docker inspect ingress
```

Ingress is not manually attachable for standalone `docker run` in source.

Custom attachable overlay:

```bash
docker network create --driver overlay --attachable my-overlay
docker run -dit --name test_container --network my-overlay busybox:latest
```

## 14. Overlay namespace

```bash
ls -ltr /var/run/docker/netns
docker network ls
overlay_namespace=/var/run/docker/netns/1-<network-id>
nsenter --net=$overlay_namespace ip link show
```

Expected elements: `br0`, veth interfaces, `vxlan0`.

## 15. docker_gwbridge

```bash
docker inspect docker_gwbridge
```

Source model:
- overlay interface handles container-to-container traffic;
- second interface via `docker_gwbridge` provides external connectivity;
- shown config has IP masquerade enabled.

## 16. VXLAN

```text
original Ethernet frame
  + VXLAN header
  + outer UDP
  + outer IP
  + outer MAC
```

Source:
- L2 virtual network over physical L3;
- UDP 4789;
- VNI segments traffic;
- VTEP encapsulates/decapsulates.

Observe:

```bash
tcpdump -i eth0 port 4789
nsenter --net=$overlay_namespace tcpdump -vv -epni any arp
nsenter --net=$overlay_namespace ip neighbor show
```

## Acceptance

Нужно уметь объяснить bridge/host/none, default vs user bridge, namespace+veth+docker0, NAT/port mapping, MACVLAN bridge/trunk, ingress/attachable overlay, docker_gwbridge, VXLAN/VNI/VTEP/UDP 4789.
