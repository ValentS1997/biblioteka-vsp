# Chapter 3 diagram

```mermaid
flowchart TD
    A[General switching problem] --> B{Resource model}

    B --> C[Circuit switching]
    C --> C1[Choose route]
    C1 --> C2[Reserve elementary channels]
    C2 --> C3[Build composite channel]
    C3 --> C4[Transfer with fixed bandwidth]
    C4 --> C5[Release reserved resources]

    B --> P[Packet switching]
    P --> P1[Split message into packets]
    P1 --> P2[Header identifies forwarding context]
    P2 --> P3[Buffer / store-and-forward]
    P3 --> P4[Queues and variable delay]

    P4 --> D[Datagram]
    P4 --> L[Logical connection]
    P4 --> V[Virtual circuit]

    D --> D1[Independent packet processing]
    L --> L1[End-system connection state]
    V --> V1[Fixed route + compact label]

    C5 --> X[Comparison]
    D1 --> X
    L1 --> X
    V1 --> X

    X --> Y[Ethernet example]
```

## Interpretation

Circuit switching spends resources before transfer to obtain predictability. Packet switching shares resources dynamically and gains utilization efficiency at the cost of queues, variable delay and possible loss.
