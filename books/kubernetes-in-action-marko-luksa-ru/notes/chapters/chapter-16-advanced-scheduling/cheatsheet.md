# Шпаргалка: taints, tolerations и affinity

## 1. Taint vs toleration

~~~text
Node taint
  → "avoid / reject Pods"

Pod toleration
  → "this Pod can tolerate that taint"
~~~

Important:
toleration permits placement, but does not force placement onto that node.

## 2. Taint effects

### NoSchedule

~~~text
new Pod without matching toleration
→ not scheduled to node
~~~

Existing Pods stay.

### PreferNoSchedule

Soft form:
scheduler tries to avoid node, but may place Pod there.

### NoExecute

~~~text
new Pod without toleration
→ not scheduled

existing Pod without toleration
→ evicted
~~~

Highest operational impact.

## 3. Add source taint

~~~bash
kubectl taint node node1.k8s node-type=production:NoSchedule
~~~

Effect:
ordinary Pods without matching toleration avoid node1.

## 4. Matching toleration

Source fragment:

~~~text
tolerations:
- key: node-type
  operator: Equal
  value: production
  effect: NoSchedule
~~~

Operator:
- Equal → match key/value/effect;
- Exists → tolerate any value for key.

## 5. Failure-related tolerations

Source default model:

~~~text
key: node.alpha.kubernetes.io/notReady
effect: NoExecute
operator: Exists
tolerationSeconds: 300

key: node.alpha.kubernetes.io/unreachable
effect: NoExecute
operator: Exists
tolerationSeconds: 300
~~~

Meaning:
Pod tolerates failed/unreachable node for 300 seconds before source control-plane behavior may relocate it.

## 6. nodeSelector

Simple hard rule:

~~~text
nodeSelector:
  gpu: "true"
~~~

Pod can run only on nodes with label gpu=true.

## 7. Required node affinity

~~~text
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: gpu
          operator: In
          values:
          - "true"
~~~

Meaning:
label must match at scheduling time.

Source-era IgnoredDuringExecution:
later label change does not evict Pod.

## 8. Preferred node affinity

~~~text
preferredDuringSchedulingIgnoredDuringExecution:
- weight: 80
  preference:
    matchExpressions:
    - key: availability-zone
      operator: In
      values: [zone1]
- weight: 20
  preference:
    matchExpressions:
    - key: share-type
      operator: In
      values: [dedicated]
~~~

Higher weight = stronger preference.

Not a guarantee.

## 9. Label source nodes

~~~bash
kubectl label node node1.k8s availability-zone=zone1
kubectl label node node1.k8s share-type=dedicated
kubectl label node node2.k8s availability-zone=zone2
kubectl label node node2.k8s share-type=shared
~~~

Inspect:

~~~bash
kubectl get node -L availability-zone -L share-type
~~~

## 10. Pod affinity

Required same-host example:

~~~text
affinity:
  podAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: kubernetes.io/hostname
      labelSelector:
        matchLabels:
          app: backend
~~~

Frontend Pods must schedule in same topology domain as matching backend Pod.

With hostname:
same node.

## 11. topologyKey

Controls co-location domain.

Source examples:
- kubernetes.io/hostname → node;
- failure-domain.beta.kubernetes.io/zone → zone;
- failure-domain.beta.kubernetes.io/region → region;
- custom label rack → rack.

## 12. How podAffinity resolves topology

~~~text
1. find Pods matching labelSelector
2. find Nodes hosting them
3. read topologyKey label value on those Nodes
4. allow/prefer Nodes with same topology value
~~~

## 13. Namespace scope

Source default:
labelSelector matches Pods in same namespace.

Field namespaces can include Pods from other namespaces.

## 14. Preferred pod affinity

~~~text
podAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
  - weight: 80
    podAffinityTerm:
      topologyKey: kubernetes.io/hostname
      labelSelector:
        matchLabels:
          app: backend
~~~

If co-location impossible, scheduler may choose another node.

## 15. Pod anti-affinity

Hard separation:

~~~text
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
  - topologyKey: kubernetes.io/hostname
    labelSelector:
      matchLabels:
        app: frontend
~~~

Effect:
frontend replicas cannot share a node.

On 2-node cluster with 5 replicas:
- 2 may run;
- 3 may remain Pending.

## 16. Preferred anti-affinity

Use soft rule if distribution is desired but co-location is acceptable when capacity is constrained.

## 17. Choosing the mechanism

| Goal | Mechanism |
|---|---|
| Keep arbitrary Pods away from special node | taint |
| Allow selected Pod onto tainted node | toleration |
| Require node labels | required nodeAffinity |
| Prefer node labels | preferred nodeAffinity |
| Co-locate with another workload | podAffinity |
| Separate from another workload | podAntiAffinity |
| Define node/rack/zone/region scope | topologyKey |

## Acceptance model

Before tainting a node:
- list workloads currently on node;
- determine effect;
- for NoExecute, identify which Pods lack toleration;
- have rollback method confirmed.

Before hard affinity:
- verify matching node labels/topology domains exist;
- verify enough capacity exists;
- expect Pending if no valid placement remains.

Before anti-affinity:
- compare requested replicas with available topology domains;
- use preferred form if strict separation is not required.
