# Приложение B — diagrams

```mermaid
flowchart TD
  VM[3 VMs / bridged network] --> OS[OS + packages]
  OS --> Prereq[host prerequisites]
  Prereq --> Init[kubeadm init on master]
  Init --> Join[kubeadm join on workers]
  Join --> NR[Nodes NotReady]
  NR --> Desc[kubectl describe node]
  Desc --> CNI[Deploy CNI]
  CNI --> Ready[3 nodes Ready]
```

```mermaid
flowchart LR
  Manifest[/etc/kubernetes/manifests] --> Kubelet
  Kubelet --> APIServer[kube-apiserver Pod]
  Kubelet --> Scheduler[kube-scheduler Pod]
  Kubelet --> Controller[kube-controller-manager Pod]
  Kubelet --> Etcd[etcd Pod]
```
