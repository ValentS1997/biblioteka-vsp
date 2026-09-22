# Шпаргалка: сетевая безопасность

## Goal / context

Использовать главу 8 для анализа security property, threat и соответствующего control.

Конкретная система / asset / trust boundary: [Needs confirmation].

## Baseline

| Параметр | Значение |
|---|---|
| Asset / data / service | [Needs confirmation] |
| Confidentiality requirement | [Needs confirmation] |
| Integrity requirement | [Needs confirmation] |
| Availability requirement | [Needs confirmation] |
| Authentication requirement | [Needs confirmation] |
| Nonrepudiation requirement | [Needs confirmation] |
| Trust boundaries | [Needs confirmation] |
| Adversary capability | [Needs confirmation] |
| Existing controls | [Needs confirmation] |
| Key/certificate ownership | [Needs confirmation] |

## Read-only analysis

### 1. Сначала определить security goal

Не начинать с выбора cipher/firewall.

Сначала определить, что требуется защищать:

- confidentiality;
- integrity;
- availability;
- authentication;
- nonrepudiation.

### 2. Проверить design principles

Глава подчеркивает:

- minimize mechanisms / simplicity;
- fail-safe defaults;
- complete mediation;
- least privilege.

Если control нарушает эти принципы, сильный cryptographic algorithm сам по себе не устраняет design risk.

### 3. Классифицировать threat

Основные attack components главы:

- reconnaissance;
- listening/interception;
- spoofing/tampering;
- disruption / DoS.

Использовать эту классификацию для threat model, а не как operational attack recipe.

### 4. Проверить preventive/detective controls

Firewall:
- policy-based traffic filtering.

IDS:
- signature-based detection;
- anomaly-based detection.

IPS:
- inline blocking;
- риск false positive влияет на legitimate traffic.

Проверить false positives и false negatives, а не только количество alerts.

### 5. Выбрать cryptographic primitive по задаче

Symmetric crypto:
- shared secret;
- high-performance encryption;
- AES — основной modern symmetric algorithm, обсуждаемый главой.

Public-key crypto:
- public/private keys;
- RSA и elliptic-curve context;
- полезно для key establishment/signature constructions.

Hash / message digest:
- integrity primitive;
- SHA-family;
- используется в digital signatures.

### 6. Проверить key management

Сильный algorithm бесполезен без надежной связи identity ↔ key.

Проверить:

- certificate;
- CA;
- chain of trust;
- trust anchor;
- revocation/validity context: [Needs confirmation], если конкретная система не дана.

### 7. Проверить authentication protocol

Проверить:

- кто аутентифицируется первым;
- nonces/timestamps;
- replay resistance;
- binding identity к messages/keys;
- trusted third party / KDC, если используется;
- session-key establishment.

Глава отдельно предупреждает, что authentication protocol design легко сделать неправильно.

### 8. Проверить secure connection layer

IPsec:
- transport vs tunnel mode;
- AH/ESP context;
- VPN часто использует tunnel mode.

Wireless:
- WEP рассматривается как сломанный механизм;
- 802.11i/WPA2 — более сильная модель при корректной конфигурации.

### 9. Проверить application security

E-mail:
- PGP combines signature/hash + compression + session encryption + public-key wrapping.

Web:
- DNSSEC authenticates DNS data;
- SSL/TLS supplies authentication/confidentiality/integrity for connection;
- browser scripts increase attack surface;
- sandboxing/code signing constrain executable content.

### 10. Разделить technology и policy

Privacy, anonymity, censorship, steganography и DRM включают не только technical properties, но и competing social/legal interests.

## Observation tools

Source-supported tools:

- `traceroute` — workload-generating path observation;
- `tcpdump` — read-only capture в authorized environment;
- Wireshark — read-only analysis в authorized environment;
- `telnet` — generic TCP connection tool; target syntax source не задает.

## Interpretation

- Confidentiality без integrity не гарантирует, что ciphertext не был изменен.
- Authentication не означает authorization.
- Strong cipher не исправляет weak key management.
- Firewall/IDS/IPS решают разные задачи: filtering, detection и prevention.
- Signature-based detection точнее описывает известный pattern; anomaly detection шире, но может давать менее конкретные alerts.
- Public-key crypto не устраняет необходимость доверять identity-to-key binding.
- Replay resistance требует freshness mechanism вроде nonce/timestamp.
- TLS/IPsec защищают communication channel, но не устраняют application logic bugs или malicious code.

## Next action

- Для конкретного incident сначала зафиксировать asset, trust boundary, evidence и security property.
- Для packet/path observation использовать только authorized environment.
- Для implementation/configuration конкретного firewall/VPN/TLS/WPA mechanism требуется отдельный source/runbook: [Needs confirmation].

## Modifying action

[Not applicable]

Глава не задает универсальной operational configuration sequence.

## Verification / acceptance checks

Security analysis согласован с главой, когда:

- security goal и threat явно различены;
- preventive/detective controls не смешиваются;
- cryptographic algorithm отделен от key management;
- authentication отделена от authorization;
- replay/freshness учтены, если protocol stateful;
- channel protection не принимается за защиту application logic;
- false positives/false negatives учитываются при IDS/IPS;
- tooling применяется только в authorized scope.

## Rollback

[Not applicable]

Canonical modifying action отсутствует; rollback-команда источником не задана.
