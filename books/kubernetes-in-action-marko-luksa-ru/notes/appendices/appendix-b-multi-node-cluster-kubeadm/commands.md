# Приложение B — команды

| Команда | Класс | Effect / risk | Проверка | Rollback |
|---|---|---|---|---|
| `ip addr` | read-only | IP inventory | Найти interface address | N/A |
| `setenforce 0` | state-changing | Временно ослабляет SELinux enforcement | [Needs confirmation] | [Needs confirmation] |
| `systemctl disable firewalld && systemctl stop firewalld` | state-changing | Отключает firewall service | [Needs confirmation] | [Needs confirmation] |
| `yum install -y docker kubelet kubeadm kubectl kubernetes-cni` | state-changing | Устанавливает source-era stack | package state | [Needs confirmation] |
| `systemctl enable/start docker` | state-changing | Запускает Docker | service status [Needs confirmation] | [Needs confirmation] |
| `systemctl enable/start kubelet` | state-changing | Запускает kubelet | service status [Needs confirmation] | [Needs confirmation] |
| `sysctl -w net.bridge.bridge-nf-call-iptables=1` | state-changing | Меняет runtime sysctl | [Needs confirmation] | [Needs confirmation] |
| `swapoff -a ...` | state-changing | Отключает swap и меняет fstab | [Needs confirmation] | [Needs confirmation] |
| `shutdown now` | state-changing | Выключает VM | VM stopped | Power on |
| `hostnamectl --static set-hostname node1.k8s` | state-changing | Меняет hostname | [Needs confirmation] | [Needs confirmation] |
| `kubeadm init` | state-changing | Инициализирует control plane | `kubectl get po -n kube-system` | [Needs confirmation] |
| `export KUBECONFIG=/etc/kubernetes/admin.conf` | session state | Меняет kubeconfig target в shell | kubectl works | unset/change variable |
| `kubectl get po -n kube-system` | read-only | Проверяет control plane Pods | Running/Pending state | N/A |
| `kubectl get node(s)` | read-only | Node readiness | Ready/NotReady | N/A |
| `kubeadm join ...` | state-changing | Присоединяет worker | `kubectl get nodes` | [Needs confirmation] |
| `kubectl describe node node1.k8s` | read-only | Диагностика NotReady | Conditions | N/A |
| `kubectl apply -f "<SOURCE_WEAVE_URL>"` | state-changing | Разворачивает CNI + RBAC resources | nodes Ready | [Needs confirmation] |
| `kubectl get po --all-namespaces` | read-only | Cluster-wide Pod check | system/CNI Running | N/A |
| `scp root@<MASTER_IP>:/etc/kubernetes/admin.conf ~/.kube/config2` | state-changing/local | Копирует admin kubeconfig; sensitive credential material | file exists | удалить local copy |
| `export KUBECONFIG=~/.kube/config2` | session state | Переключает kubectl target | kubectl access | unset/change variable |

Все версии/URLs/пакеты source-era; current applicability **[Needs confirmation]**.
