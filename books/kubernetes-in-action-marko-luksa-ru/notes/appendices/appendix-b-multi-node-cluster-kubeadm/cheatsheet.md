# Приложение B — cheatsheet

## Symptom / problem framing

Нужно собрать source-era трехузловой Kubernetes cluster с помощью kubeadm.

## Baseline / context

```text
master.k8s
node1.k8s
node2.k8s
   ↓
kubeadm init / join
   ↓
CNI
   ↓
Ready
```

## Read-only checks

```bash
ip addr
docker ps
kubectl get po -n kube-system
kubectl get node
kubectl get nodes
kubectl describe node node1.k8s
kubectl get po --all-namespaces
```

## Interpretation

- Только master виден после `kubeadm init` — workers еще не joined.
- `NotReady` + `NetworkPluginNotReady` в source означает отсутствие CNI.
- После CNI source ожидает все три nodes в `Ready`.
- Control-plane components запускаются как static Pods из `/etc/kubernetes/manifests`.

## Next action

Порядок source:
1. подготовить ОС и сеть;
2. установить packages;
3. настроить kernel/swap prerequisites;
4. уникализировать hostnames/MAC;
5. проверить name resolution;
6. `kubeadm init`;
7. workers: `kubeadm join ...`;
8. диагностировать `NotReady`;
9. развернуть CNI;
10. проверить `Ready`.

## Modifying action

Source содержит рискованные host-level изменения:

```bash
setenforce 0
systemctl disable firewalld && systemctl stop firewalld
yum install -y docker kubelet kubeadm kubectl kubernetes-cni
systemctl enable docker && systemctl start docker
systemctl enable kubelet && systemctl start kubelet
sysctl -w net.bridge.bridge-nf-call-iptables=1
echo "net.bridge.bridge-nf-call-iptables=1" > /etc/sysctl.d/k8s.conf
swapoff -a && sed -i '/ swap / s/^/#/' /etc/fstab
hostnamectl --static set-hostname node1.k8s
kubeadm init
kubeadm join --token <TOKEN> <MASTER_IP>:6443 --discovery-token-ca-cert-hash sha256:<HASH>
kubectl apply -f "<SOURCE_WEAVE_URL>"
```

## Verification / acceptance checks

```bash
kubectl get nodes
kubectl get po --all-namespaces
```

Source acceptance: master + 2 workers имеют `Ready`; system/CNI Pods работают.

## Rollback

Полного rollback sequence приложение не дает: **[Needs confirmation]**.
Для host security changes это особенно важно.
