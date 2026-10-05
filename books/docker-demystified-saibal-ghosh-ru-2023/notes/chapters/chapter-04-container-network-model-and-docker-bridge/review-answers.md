# Ответы к контрольным материалам — глава 4

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | C |
| 2 | C |
| 3 | A |
| 4 | B |
| 5 | D |
| 6 | B |

Ключ `1-C, 2-C, 3-A, 4-B, 5-D, 6-B` прямо приведён в `p0086:c01`.

## Ответы на открытые вопросы

### 1. Что такое network namespace?

Network namespace — отдельный isolated instance Linux network stack. Он имеет собственные interfaces, routes, firewall rules и network devices/settings и изолирован от других namespaces.

### 2. Как работает veth pair?

veth pair — full-duplex virtual Ethernet link из двух interfaces. Один endpoint можно разместить в одном network namespace, другой — в другом. Traffic, отправленный в один конец pair, появляется на другом конце.

### 3. Нарисуйте и объясните Container Network Model

```text
Sandbox A -- Endpoint -- Network -- Endpoint -- Sandbox B
```

Sandbox содержит полный network stack container. Endpoint соединяет sandbox с внешней network. Endpoints, подключённые к одной network, могут взаимодействовать друг с другом.

### 4. Что представляет собой Libnetwork и каковы её функции?

В формулировке главы Libnetwork — реализация CNM и library для создания/управления network stacks. Она стандартизирует interface между Docker daemon и network drivers.

### 5. В чём заключается концепция Linux network bridge?

Linux bridge — Layer-2 device, virtual implementation physical switch в kernel. Вместо множества point-to-point veth pairs namespaces можно подключить к общему bridge, после чего они взаимодействуют через этот bridge.

### 6. Что такое network drivers?

Network drivers — software components, реализующие работу Docker networks. Они могут быть built-in или third-party. В главе перечислены bridge, host, none, overlay и MACVLAN; отдельно рассматриваются IPAM drivers для address management.

## Operational map

```text
CNM abstraction
  ↓
libnetwork
  ↓
network driver + IPAM
  ↓
Linux primitives
namespace + veth + bridge
```

## Provenance

Ответы сформированы только по chapter RAG `p0076:c01`–`p0087:c01`. External sources и model-memory не использовались.
