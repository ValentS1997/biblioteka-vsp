# Резюме главы 8

Источник: раздел 8.5 «Резюме», `p0364:c01`–`p0365:c01`, PDF 364–365.

Глава систематизирует фундаментальные проблемы distributed systems.

## Network uncertainty

Отправленный packet может:

- потеряться;
- задержаться на произвольное время.

То же относится к response.

Если response не пришел, sender не знает:

- дошел ли request;
- был ли он обработан;
- отказал ли remote node;
- потерялся ли response;
- придет ли response позже.

Большинство practical systems используют timeout как failure detector, но timeout не способен отличить network failure от node failure или temporary slowness.

## Clocks

Node clocks могут:

- расходиться между machines;
- корректироваться NTP;
- прыгать вперед или назад;
- иметь неизвестный error interval.

Поэтому physical clock timestamps опасно использовать как доказательство event ordering.

Для duration подходят monotonic clocks; для causal ordering часто нужны другие mechanisms.

## Process pauses

Process может быть остановлен на значительное время — например, GC pause или scheduling delay — а затем продолжить работу.

Во время pause другие nodes могут признать его dead, передать leadership/lease другому node, после чего старый process возобновится и ошибочно будет считать себя прежним owner.

Этот класс проблем мотивирует fencing tokens и другие mechanisms, которые не полагаются только на self-assessment node.

## Partial failures

Partial failure — определяющая характеристика distributed systems.

System goal — продолжать работать, даже если часть components:

- failed;
- slow;
- disconnected;
- temporarily paused.

Обнаружение failure само по себе неточно, а «хромающий» slow node может быть сложнее явно dead node.

## Knowledge and coordination

Machines не имеют shared memory, global variables или perfect common knowledge.

Information передается только messages через unreliable network. Поэтому серьезные decisions обычно требуют protocol involving multiple nodes и quorum/coordination.

## Cost of stronger guarantees

Bounded network latency и hard real-time guarantees технически возможны, но стоят дороже и снижают resource utilization.

Большинство non-safety-critical systems принимают более дешевые components и variable latency, компенсируя это fault-tolerant software.

## System models

Для reasoning алгоритм должен явно определить assumptions:

- timing model;
- node failure model.

Chapter distinguishes synchronous, partially synchronous и asynchronous timing, а также crash-stop, crash-recovery и Byzantine node failures.

Для большинства practical systems наиболее реалистичен partially synchronous crash-recovery model.

## Safety and liveness

Correctness удобно разделять на:

- safety — неправильное событие не должно произойти;
- liveness — система при оговоренных условиях в конце концов должна добиться progress.

Safety обычно требуется сохранять во всех allowed failure scenarios; liveness может зависеть от network recovery и достаточного числа живых nodes.

## Итог

Theoretical reasoning и empirical fault testing нужны одновременно.

Глава 8 намеренно описывает проблемы. Следующая глава, начинающаяся на `p0375:c01`, переходит к abstractions и algorithms, которые предоставляют полезные consistency/consensus guarantees поверх этой ненадежной основы.
