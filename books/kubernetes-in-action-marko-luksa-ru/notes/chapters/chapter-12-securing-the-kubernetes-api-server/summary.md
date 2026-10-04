# Резюме главы 12

Источник: явный раздел 12.3 Резюме, RAG chunk p0457:c01.

Глава закрепляет следующие положения:

- API clients могут быть users или applications in Pods;
- applications связаны с ServiceAccount;
- users и ServiceAccounts могут входить в groups;
- каждый namespace получает default ServiceAccount;
- additional ServiceAccounts можно создавать и назначать Pods;
- ServiceAccounts могут ограничивать mountable Secrets;
- ServiceAccounts могут автоматически предоставлять image pull Secrets;
- Role и ClusterRole определяют разрешённые actions/resources;
- RoleBinding и ClusterRoleBinding связывают roles с users/groups/ServiceAccounts;
- cluster поставляется с default ClusterRoles и ClusterRoleBindings.

## Центральная модель

~~~text
authentication
  → identity
  → RBAC authorization

Role / ClusterRole
  → permission set

RoleBinding / ClusterRoleBinding
  → subject + scope
~~~

## Security conclusion

Source chapter repeatedly leads to least privilege:

- separate ServiceAccounts by workload;
- grant only required verbs/resources;
- prefer namespace-limited RoleBinding when cluster-wide scope is not required;
- treat Secret access and cluster-admin as privilege-escalation boundaries.

## Provenance

- Chapter chunks: p0425:c01–p0457:c01
- Summary chunk: p0457:c01
- PDF page: 457
- Printed page: 456
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
