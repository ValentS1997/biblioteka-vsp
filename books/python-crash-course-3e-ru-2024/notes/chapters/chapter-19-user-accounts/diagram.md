# Диаграмма — глава 19

## Form lifecycle

~~~mermaid
flowchart TD
    A["GET"] --> B["empty or instance-bound form"]
    C["POST"] --> D["form(data=request.POST)"]
    D --> E{"is_valid()?"}
    E -- "no" --> F["render form + errors"]
    E -- "yes" --> G["save / commit=False"]
    G --> H["set relationships if needed"]
    H --> I["final save"]
    I --> J["redirect"]
~~~

## Authentication

~~~mermaid
flowchart LR
    A["anonymous"] --> B["login/register"]
    B --> C["authenticated user"]
    C --> D["@login_required views"]
    C --> E["logout POST"]
    E --> A
~~~

## Authorization

~~~mermaid
flowchart TD
    A["authenticated request"] --> B{"list page?"}
    B -- "yes" --> C["filter(owner=request.user)"]
    B -- "object page" --> D["load Topic/Entry"]
    D --> E{"owner == request.user?"}
    E -- "yes" --> F["allow"]
    E -- "no" --> G["raise Http404"]
~~~

## Ownership migration

~~~mermaid
flowchart TD
    A["add Topic.owner"] --> B["inspect existing User IDs"]
    B --> C["makemigrations"]
    C --> D["choose one-off valid owner ID"]
    D --> E["migration file"]
    E --> F["migrate"]
    F --> G["verify Topic → owner mapping"]
~~~
