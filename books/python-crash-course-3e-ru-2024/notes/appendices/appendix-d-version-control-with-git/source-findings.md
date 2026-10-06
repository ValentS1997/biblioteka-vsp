# Source findings — приложение Г

## Finding 1 — password vs email wording

Classification: **[Source wording/code mismatch]**

Provenance:
- chunk: `e0035:c01`
- EPUB spine item: `35`
- locator: `OEBPS/Text/978544614112-32.xhtml`

Source prose says Git needs the user's «имя пользователя и пароль».

Immediately afterward the shown configuration is:

```text
user.name
user.email
```

and the next sentence discusses using a fictitious email address.

Therefore «пароль» conflicts with the shown configuration/prose context.

Adjudication: intended word `[Needs confirmation]`.

## Finding 2 — chunk overlap

Classification: **[Source extraction issue]**

Provenance:
- chunk starts: `e0035:c02–c05`

Later chunks begin with repeated continuation fragments from the preceding chunk. Full workflow remains recoverable by adjacent-chunk cross-check.
