# Source findings — глава 17 «Виртуализация»

**Scope:** `p0458:c01`–`p0477:c01`, PDF/печатные страницы 458–477. Политика **rag_only**: conflicting wording/examples are preserved and isolated instead of silently corrected.

## F-01 — [Source wording/code mismatch]: Docker/Podman substitution direction

- **Locators:** `p0464:c01`–`p0465:c01`, §17.2.1.
- Source states that Podman command-line commands correspond to Docker commands.
- The following sentence says that one can replace `podman` with `docker` in the examples.
- The examples that follow are already written as `docker ...`.
- **Decision:** do not normalize the sentence into a specific substitution rule from model knowledge. Artifacts only record that the chapter claims CLI correspondence and mark the exact replacement direction as source-internally inconsistent.

## F-02 — [Source contradiction]: container filesystem changes after process exit

- **Locator A:** `p0471:c01`, Docker lifecycle discussion.
- Variant A says that after all processes finish, Docker moves the container to an exited state **but still preserves the container, including filesystem changes**, unless cleanup behavior such as `--rm` applies.
- **Locator B:** `p0475:c01`, §17.2.5.
- Variant B says that in Docker-like systems using overlay filesystems, changes made during execution are **removed after the processes finish**.
- These statements lead to different persistence/rollback expectations.
- **Decision:** artifacts do not select one as technically correct. They separate process exit from explicit cleanup and mark persistence semantics as conflicted within the source.

## F-03 — [Source code mismatch]: Python venv directory name

- **Locators:** `p0476:c01`–`p0477:c01`, §17.3.
- Creation command:
  `python3 -m venv test-venv`
- Literal activation command:
  `. test-env/bin/activate`
- The directory names `test-venv` and `test-env` do not match.
- **Decision:** preserve both literal variants. Do not silently rewrite the activation command. Any corrected path is **[Needs confirmation]** under rag_only policy.

## F-04 — [Needs confirmation]: version-specific Docker/Podman/rootless behavior

- **Locators:** `p0464:c01`–`p0471:c01`.
- The chapter describes Docker daemon/privilege behavior, Podman rootless isolation, TAP/`slirp4netns`, rootless overlay behavior and example network topology.
- These are implementation/version-sensitive details from the book's edition context.
- **Decision:** treat them as source-grounded descriptions of the chapter, not as current-system guarantees. Live behavior is **[Needs confirmation]**.

## F-05 — [Needs confirmation]: `latest` example versus stable versioning guidance

- **Locators:** `p0465:c01`–`p0467:c01` and `p0476:c01`.
- The worked Dockerfile uses `FROM alpine:latest`.
- Later the chapter warns that `latest` may introduce changes that break an application and recommends a specific version tag for a base container.
- This is not treated as a contradiction: the first is a teaching example and the latter is operational guidance.
- **Decision:** retain the example literally, but do not promote `latest` as a stable deployment policy.

## F-06 — [Needs confirmation]: no explicit chapter-end summary or review questions

- **Locators:** `p0477:c01` and `p0478:c01`; TOC `p0020:c01`.
- §17.3 ends on page 477.
- Page 478 begins the bibliography.
- The TOC lists no explicit summary/review-question section after §17.3.
- **Decision:** do not create `summary.md`, `review-questions.md` or `review-answers.md`.

## Current-system applicability

Exact hypervisor, Docker, Podman, LXC/LXD, Kubernetes, Minikube, container-networking, storage-driver, privilege and Python-environment behavior on a current target system is **[Needs confirmation]** unless supplied by higher-priority evidence.
