# Cheatsheet — глава 10: social engineering / phishing defense

## Symptom / problem framing

Нужно определить, **какие механизмы доверия и подтверждения личности/запроса позволяют social-engineering атаке сработать**, и какие controls снижают вероятность успешной манипуляции без зависимости только от внимательности пользователя.

## Baseline / context

| Область | Source framing |
| --- | --- |
| Influence | reciprocity, commitment, social proof, authority, liking, scarcity |
| Pretexting | заранее подготовленная история/сценарий |
| Communication | phishing, vishing, smishing, impersonation |
| Physical | tailgating, badges, mantraps/controlled access, baiting |
| Digital trust | sender/domain/link/attachment cues |
| Social networks | cloned/compromised identities and trusted contacts |
| Wireless | rogue/imitated AP concepts |
| Automation | campaign tooling and social-engineering frameworks |

## Read-only checks

1. Существует ли out-of-band способ подтвердить request от helpdesk/finance/management?
2. Требуют ли процессы ever disclosure of passwords/OTP/MFA approval to support staff?
3. Есть ли approved contact directory / callback number independent from the message itself?
4. Проверяются ли sender domain, actual URL target and attachment type before action?
5. Для physical access: individual badge validation, visitor escort and anti-tailgating controls?
6. Для wireless: known SSID/security baseline and rogue-AP monitoring?
7. Кто принимает/хранит reports о suspicious messages and what evidence is needed? [Needs confirmation].

## Interpretation

- Authority/urgency/reward cues are **signals**, not proof of phishing.
- A familiar logo/display name is not identity proof.
- Mismatched link text vs actual destination is a strong review cue, but URL appearance alone is not sufficient attribution.
- Contact from a known social account may still be compromised/cloned.
- User awareness helps, but controls should support independent verification and limit blast radius.
- Physical possession of a badge-like object or following an authorized person through a door is not authorization.

## Next action

For defense: **pause high-risk request → verify through independent channel → classify data/action sensitivity → report suspicious artifact → preserve evidence → contain affected identity/device if compromise is confirmed**.

## Modifying action

Defensive configuration changes may include email filtering, MFA policy, access-control procedures, visitor workflows, wireless controls and URL/domain protections; exact implementation is environment-specific **[Needs confirmation]**. Offensive campaign setup, rogue AP and payload delivery are not operationalized.

## Verification / acceptance checks

- Password/OTP requests from support are rejected by policy.
- High-risk business actions use independent approval/callback.
- Security awareness includes sender/domain/link/attachment and urgency/authority cues.
- Physical access requires individual authorization.
- Wireless clients/users have a trusted SSID/onboarding baseline.
- Phishing report path and incident escalation are known.
- Actual control implementation/effectiveness: **[Needs confirmation]**.

## Rollback

For awareness/process changes rollback is usually procedural. For email/access/wireless controls, rollback must be implementation-specific and tested before production change: **[Needs confirmation]**.
