# Контрольные материалы — глава 6

## Контрольный тест

1. К какому типу относится сеть docker0? A. Bridge. B. None. C. Overlay. D. Ничего из перечисленного.
2. Верное утверждение о VXLAN? A. L2 subnets поверх physical L3. B. L3 поверх L2. C. Level 7. D. Ничего.
3. Как default docker0 обменивается данными между containers? A. IP или names. B. Только names. C. Только IP. D. Ничего.
4. VXLAN tunnel port? A. TCP 2377. B. UDP 2377. C. TCP 4789. D. UDP 4789.
5. Docker network namespace directory? A. `/var/run/docker/` B. `/var/run/netns` C. `/var/run/docker/netns` D. Ничего.
6. Host NIC mode for MACVLAN per source? A. Non-promiscuous. B. Promiscuous. C. Не важно. D. Ничего.
7. Sharing existing container network namespace: A. no own filesystem. B. no network and filesystem. C. separate ports. D. own filesystem, shared network stack.
8. `-P` function? A. Random container-port→host-port mapping. B. Host→random container port. C. Random both. D. Ничего.
9. Correct per source? A. MAC hardcoded on host. B. MAC represented in overlay netns when container added. C. no MAC config. D. generic variable only.
10. `br0` is: A. Physical switch. B. Physical interface. C. Virtual namespace. D. Virtual switch.

## Вопросы

1. Какие types networks создаются в Docker по умолчанию?
2. Что такое network namespace container?
3. Какие networks появляются при Swarm?
4. Что такое docker0?
5. Как выполняется port mapping?
6. Что такое MACVLAN и какие два режима рассматривает глава?
7. Что такое veth?
8. Как работает overlay?
9. Что такое VXLAN?
10. Как source настраивает MACVLAN для ping host→container?

## Provenance

- Test: `p0148:c01`–`p0150:c01`
- Source answer key + questions: `p0150:c01`
