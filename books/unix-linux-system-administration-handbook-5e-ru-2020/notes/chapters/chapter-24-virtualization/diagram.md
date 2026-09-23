# Диаграмма: virtualization architecture and lifecycle

~~~mermaid
flowchart TD
    A["Need isolated workload"] --> B{"Isolation model"}

    B -->|Virtual machine| C["Hypervisor"]
    C --> C1["CPU / memory / I/O virtualization"]
    C1 --> D{"Platform"}
    D -->|Xen| E["dom0 manages domU"]
    D -->|KVM| F["Linux kernel hypervisor"]
    D -->|VMware / VirtualBox / bhyve| G["Other hypervisor implementations"]

    E --> H["virt-install / xl"]
    F --> I["virt-install / virsh"]
    G --> J["Platform-specific lifecycle"]

    H --> K["Guest running"]
    I --> K
    J --> K

    K --> L["VM image / snapshot baseline"]
    L --> M["Packer image-as-code"]
    M --> N["Repeatable image build"]
    N --> O["Vagrant development environment"]

    B -->|Container| P["Shared host kernel"]
    P --> P1["Process/filesystem isolation"]
    P1 --> P2["Lower overhead, different isolation model"]

    Q["Operational checks"] --> Q1["current guest state"]
    Q --> Q2["resource allocation"]
    Q --> Q3["console / lifecycle"]
    Q --> Q4["image build result"]

    R["Risks"] --> R1["legacy/full emulation overhead"]
    R --> R2["abrupt process kill"]
    R --> R3["hypervisor-specific image formats"]
    R --> R4["non-repeatable manual image changes"]
~~~

## Смысл диаграммы

Сначала выбирается isolation model, затем hypervisor/provider и lifecycle tooling. Image automation через Packer находится выше конкретного hypervisor, а Vagrant использует готовые providers/images для воспроизводимой development environment.
