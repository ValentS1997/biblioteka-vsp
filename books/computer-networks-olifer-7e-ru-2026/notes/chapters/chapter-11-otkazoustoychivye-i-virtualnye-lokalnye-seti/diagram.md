# Diagram — глава 11: L2 redundancy and segmentation

```mermaid
flowchart TD
    PHY[Redundant physical Ethernet topology] --> RISK[L2 loop risk]

    RISK --> STP[STP / RSTP]
    STP --> ROOT[Elect root bridge]
    ROOT --> RP[Choose root ports]
    RP --> DP[Choose designated ports]
    DP --> TREE[One active loop-free tree]
    TREE --> BLOCK[Other links blocked/discarding]

    PHY --> LAG[Link Aggregation]
    LAG --> LACP[LACP / static membership]
    LACP --> LOG[One logical link to upper protocols]
    LOG --> ACTIVE[Several physical members can remain active]
    LOG --> STP

    TREE --> VLAN[VLAN segmentation]
    ACTIVE --> VLAN
    VLAN --> ACC[Access port: end host / untagged]
    VLAN --> TRUNK[Trunk: multiple VLANs / tagged]
    TRUNK --> TAG[802.1Q VID + priority]

    VLAN --> MSTP[MSTP]
    MSTP --> T1[Tree A → VLAN group A]
    MSTP --> T2[Tree B → VLAN group B]

    VLAN --> L3[Inter-VLAN traffic requires L3]
```

## Failure-domain view

```text
redundant links without STP/RSTP
  → loops / frame duplication / unstable learning

single STP tree
  → reliable but some links idle

LAG
  → active parallel capacity between two systems

VLAN
  → separate broadcast/L2 domains

MSTP
  → different VLAN groups use different active trees
```

Provenance: `p0326:c01`–`p0350:c01`.
