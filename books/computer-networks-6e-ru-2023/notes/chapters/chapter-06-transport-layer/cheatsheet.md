# Шпаргалка: транспортный уровень

## Goal / symptom

Использовать главу 6, когда вопрос относится к communication process-to-process:

- установление или разрыв соединения;
- порт/сокет и multiplexing;
- потеря, дубликаты, порядок данных;
- flow control;
- congestion control;
- TCP/UDP behavior;
- RTT/RTO, window и retransmission;
- real-time transport/jitter;
- transport performance на быстрых или long-delay links.

Конкретный сценарий: [Needs confirmation].

## Baseline / context

| Параметр | Значение |
|---|---|
| Transport protocol | [Needs confirmation] |
| Source/destination process or port | [Needs confirmation] |
| Connection-oriented / connectionless | [Needs confirmation] |
| RTT | [Needs confirmation] |
| Loss / duplicate ACK / ECN signal | [Needs confirmation] |
| Receiver window | [Needs confirmation] |
| Congestion window | [Needs confirmation] |
| MSS / segment size | [Needs confirmation] |
| Application message/stream semantics | [Needs confirmation] |
| Required throughput / delay / jitter | [Needs confirmation] |

## Read-only checks

### 1. Определить transport service

- TCP: reliable ordered byte stream with explicit connection.
- UDP: connectionless datagrams with port multiplexing and minimal built-in mechanisms.
- QUIC: transport over UDP with different connection/stream design.
- RTP/RTCP: real-time media transport/feedback context.

### 2. Для socket-based application

Проверить lifecycle:

```text
server: SOCKET → BIND → LISTEN → ACCEPT
client: SOCKET → CONNECT
both:   SEND / RECEIVE
end:    CLOSE
```

Это API flow, а не shell-команда.

### 3. Отделить flow control от congestion control

Flow control ограничивает sender возможностями receiver.

Congestion control ограничивает offered load возможностями network path.

В TCP работают разные windows: receiver window и congestion window; фактическая отправка ограничивается обоими.

### 4. Проверить reliability state

Для TCP определить:

- sequence/ACK state;
- timeout/retransmission;
- duplicate ACK;
- SACK, если применяется;
- ECN signal, если negotiated/available.

Не считать потерю единственным возможным congestion signal: глава отдельно рассматривает ECN и BBR.

### 5. Проверить RTT и timeout

Transport protocol должен оценивать RTT и выбирать timeout, который не создает систематические ложные retransmissions и не делает recovery чрезмерно медленным.

Конкретные значения: [Needs confirmation].

### 6. Для UDP / real-time

UDP сам не выполняет flow control, congestion control или retransmission.

Для RTP/RTCP проверить:

- sequence/timestamp context;
- jitter;
- playback buffering;
- RTCP feedback о delay/jitter/bandwidth/congestion;
- synchronization requirements.

### 7. Для TCP congestion control

Ключевые concepts главы:

- congestion window;
- slow start;
- AIMD;
- loss/duplicate ACK;
- fast recovery context;
- SACK;
- ECN;
- CUBIC.

Не интерпретировать congestion window как receiver flow-control window.

### 8. Для QUIC / BBR

QUIC работает поверх UDP и ориентирован на уменьшение connection overhead и работу с потоками.

BBR оценивает bottleneck bandwidth и RTT и выбирает рабочую точку на основании этих оценок.

### 9. Для performance

Проверить не только line rate:

- host CPU / processing capacity;
- data copies;
- context switches;
- packet/segment size;
- timer processing;
- header overhead/compression;
- RTT;
- bandwidth-delay product.

Для эффективного заполнения длинного быстрого канала окно должно быть сопоставимо с bandwidth-delay product.

## Interpretation

- Network reliability не отменяет transport responsibilities: transport API, process addressing, connection state и end-to-end semantics остаются.
- ACK транспортного уровня не обязательно означает завершение прикладной операции на удаленном хосте.
- UDP минимален намеренно: дополнительные semantics приложение добавляет самостоятельно.
- TCP сочетает reliability, ordering, flow control и congestion control.
- AIMD связывает efficiency и fairness при конкурирующих потоках.
- Loss-based congestion control может взаимодействовать с очередями/буферами; BBR использует оценки bottleneck bandwidth/RTT.
- Высокий line rate не гарантирует application throughput, если bottleneck — host processing или RTT/window.

## Next action

- IP routing, path, MTU и L3 congestion → глава 5.
- DNS/HTTP/email/application behavior → глава 7.
- Если проблема остается на transport layer, уточнить protocol, connection state, RTT, windows, retransmission/congestion signals и application semantics.

## Modifying action

[Not applicable]

Глава не предоставляет универсальных operational CLI для TCP/UDP/kernel tuning.

## Verification / acceptance checks

Анализ согласован с главой, когда:

- process-to-process transport отделен от host-to-host network delivery;
- connection model и protocol определены;
- flow-control window не смешивается с congestion window;
- reliability analysis учитывает sequence/ACK/timer/retransmission state;
- UDP не наделяется гарантиями, которых в нем нет;
- для real-time traffic учтены jitter/playback/feedback;
- performance рассматривается вместе с RTT и bandwidth-delay product;
- socket API не выдается за shell CLI.

## Rollback

[Not applicable]

Canonical modifying action в главе отсутствует; rollback-команда источником не задана.
