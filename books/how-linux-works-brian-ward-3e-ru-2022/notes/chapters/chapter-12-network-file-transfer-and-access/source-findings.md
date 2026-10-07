# Source findings — глава 12 «Передача файлов по сети и доступ к ним»

**Scope:** `p0368:c01`–`p0389:c01`, PDF/печатные страницы 368–389. Политика **rag_only**: source wording/examples are preserved; no external/model correction is silently substituted.

## F-01 — [Edition/applicability boundary]: `python -m SimpleHTTPServer`

- **Locator:** `p0369:c01`, §12.1.
- Source command: `python -m SimpleHTTPServer`.
- Source says it starts a basic HTTP server for the current directory on port 8000 and explicitly warns not to run it on a public/untrusted network.
- No alternative module/command is supplied in the chapter.
- **Decision:** preserve the exact command as edition content; whether that module name exists on a current target host is **[Needs confirmation]**.

## F-02 — [Source syntax boundary]: CIFS mount source form

- **Locator:** `p0385:c01`, §12.4.9.
- Source client form for smbclient is `\\SERVER\sharename`.
- Immediately afterward the CIFS mount example is:
  `mount -t cifs SERVER:sharename mountpoint -o user=username,pass=password`.
- The source explicitly says the mount form uses `SERVER:sharename`, not `\\SERVER\sharename`.
- **Decision:** do not silently replace the literal source syntax with another form. Current platform-valid mount source syntax is **[Needs confirmation]**.

## F-03 — [Security/applicability boundary]: credential text embedded in CIFS example

- **Locator:** `p0385:c01`.
- The literal source command includes `pass=password` directly in the option string.
- The chapter does not provide a separate credential-file/secret-handling workflow.
- **Decision:** preserve the source command in `commands.md` with a credential-sensitive warning; any safer current method is outside RAG and therefore **[Needs confirmation]**.

## F-04 — [Source wording inconsistency]: Samba `unix password sync = yes`

- **Locators:** `p0381:c01`–`p0382:c01`, §12.4.3.
- Source first says `unix password sync = yes` makes `smbpasswd` change the ordinary Unix password together with the Samba password.
- It then says this can result in a Samba password different from the Linux password and prevent Linux login.
- These two statements do not form a fully clear causal model as extracted.
- **Decision:** artifacts retain only the operational warning that Samba password changes may affect ordinary Unix credentials. Exact synchronization semantics on a real Samba configuration remain **[Needs confirmation]**.

## F-05 — [Source wording issue]: NAS expansion

- **Locator:** `p0377:c01`, §12.3.
- Source expands NAS as **Network Area Storage**.
- The acronym is used later as `NAS` without a second expansion.
- **Decision:** preserve the edition wording in provenance; do not introduce an external correction into source-grounded artifacts.

## F-06 — [Source figures unavailable]: rsync diagrams 12.1–12.2

- **Locators:** `p0372:c01`–`p0373:c01`.
- Figures 12.1 and 12.2 illustrate the difference between copying `dir` and `dir/`.
- The project RAG extraction does not provide the original figures as independent multimodal objects.
- **Decision:** Mermaid/SVG artifacts reconstruct only the text-confirmed directory-layout semantics. Original figure geometry/labels remain **[Needs confirmation]**.

## F-07 — [Source scope boundary]: no explicit chapter summary/review section

- **Locators:** `p0388:c01`–`p0389:c01`, §12.8.
- §12.8 is a concluding thematic discussion about the state and limitations of network file sharing.
- It is not labeled `Выводы`, `Резюме`, `Что дальше?` or equivalent.
- `p0390:c01` begins chapter 13.
- **Decision:** no `summary.md`; no review-question artifacts.

## Current-system applicability

Remote hosts, usernames, share names, passwords, workgroups, interfaces, ports, rsync paths, Samba configuration locations, SSHFS/NFS mountpoints and authentication mechanisms in examples are source context. Values and valid syntax for a live target system remain **[Needs confirmation]** unless supplied by higher-priority evidence.
