# Диаграмма: cloud lifecycle и cost feedback

~~~mermaid
flowchart TD
    A["Need workload"] --> B{"Service model"}
    B -->|IaaS| C["Manage OS + virtual network/storage + app"]
    B -->|PaaS| D["Manage code/app while provider manages platform"]
    B -->|SaaS| E["Use provider-managed application"]

    C --> F["Choose provider + region/zone"]
    D --> F
    E --> F

    F --> G["Design IAM + network exposure"]
    G --> H["Choose image + storage semantics"]
    H --> I{"One-off or repeatable?"}

    I -->|One-off| J["Web/CLI/API operation"]
    I -->|Repeatable graph| K["IaC: CloudFormation / Terraform"]
    K --> L["Version-controlled infrastructure definition"]
    L --> J

    J --> M["Provision resource"]
    M --> N["Wait/observe state transition"]
    N --> O["Verify reachability + SSH/service"]
    O --> P["Measure usage + cost"]

    P --> Q{"Capacity still needed?"}
    Q -->|Yes| R["Right-size / autoscale / monitor"]
    R --> P
    Q -->|No| S{"Need recovery point?"}
    S -->|Yes| T["Snapshot / preserve state"]
    S -->|No| U["Stop / destroy"]
    T --> U

    U --> V["Verify resource removed and billing stopped"]

    W["Storage choice"] --> H
    W --> W1["Object: durable network objects"]
    W --> W2["Block: attachable virtual disk"]
    W --> W3["Ephemeral: lost with instance deletion"]

    X["Security boundary"] --> G
    X --> X1["Least privilege IAM"]
    X --> X2["Minimize public perimeter"]
    X --> X3["Bastion/VPN for private hosts"]
~~~

## Смысл диаграммы

Глава рассматривает cloud как управляемый lifecycle, а не как «сервер где-то ещё». Provisioning, state transitions, network exposure, identity, storage semantics и cost должны проверяться как единая система.
