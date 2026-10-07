# Cheatsheet — глава 16 «Компиляция программ из исходного кода на языке C»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0442:c01`–`p0457:c01`, PDF/печатные страницы 442–457. Только `rag_only`.

## Symptom / problem framing

Типовые задачи/сбои главы:

1. безопасно распаковать исходный архив;
2. понять, какой build system использует пакет;
3. настроить install prefix и dependency paths;
4. разобрать generic `configure: error: C compiler cannot create executables`;
5. локализовать зависимость через `config.log` / `pkg-config`;
6. проверить `make install` до реального изменения системы;
7. применить patch на правильном уровне каталогов;
8. отличить первичную compiler/preprocessor error от каскадных `make[N]` failures.

Рабочая модель: **inspect → configure → build → test → dry-run install → install → verify**.

## Baseline / context

| Объект | Модель главы | PDF |
|---|---|---:|
| Source archive | `.tar.gz`, `.tar.bz2`, `.tar.xz`; inspect before extract | 443–444 |
| Package docs | README / INSTALL are primary package instructions | 444 |
| Build metadata | Makefile, Makefile.in, configure, CMakeLists.txt | 444–445 |
| Autoconf | `configure` probes host and generates build files | 445 |
| Install prefix | defaults to `/usr/local` in source model; can use `--prefix` | 446–447,453 |
| Out-of-tree build | keeps source tree unchanged while varying build options | 448 |
| Flags | `CPPFLAGS`, `CFLAGS`, `LDFLAGS` | 448–449 |
| config.log | detailed configure evidence | 449–450 |
| pkg-config | resolves package compile/link flags from `.pc` metadata | 450–452 |
| Standard targets | clean, distclean, check, install-strip | 449–450 |
| Patch | unified diff + `patch -pN` path stripping | 453–454 |
| Troubleshooting | read first causal error, not recursive make tail | 454–456 |

## Read-only checks

```sh
tar tvf package.tar
tar ztvf package.tar.gz
./configure --help
make -n
make -n install
pkg-config --libs zlib
pkg-config --list-all
less config.log
```

Source-guided inspection:

- inspect archive paths before extraction;
- inspect README and INSTALL before building;
- inspect the beginning of a patch to determine expected working directory;
- if `configure` fails, use `config.log` and search backward from the relevant error;
- for recursive make failures, identify the earliest compiler/preprocessor error that precedes propagation.

## Interpretation

| Observation | Meaning from source | Still unchecked |
|---|---|---|
| Archive members all under `package-version/` | Extraction should remain grouped in one tree | Trustworthiness/content still not proven |
| Archive has top-level loose files | Extracting in current directory will clutter it | Whether files overwrite anything |
| Archive contains absolute paths | Source treats archive as suspicious/unsafe | Actual tar implementation behavior [Needs confirmation] |
| `./configure` succeeds | Host probes completed and build files were generated | `make` may still fail |
| `C compiler cannot create executables` | Generic configure failure; inspect `config.log` | Root cause may be flags/toolchain/filesystem |
| `pkg-config --libs zlib` returns `-lz` | pkg-config knows library metadata | Header flags/version/runtime compatibility |
| `make -n install` shows unexpected path | Install target would modify wrong/unwanted location | Whether prefix/options can correct it |
| `patch` asks “File to patch:” | Working dir/path level or source version likely mismatched | Exact `-p` value/version |
| Nested make ends in `Error 2` | Usually propagated failure | First causal compiler/tool error |
| `make: prog: Command not found` | Required tool is absent or not resolvable by PATH | Correct package/path |

## Next action

1. Verify archive structure and package documentation.
2. Build in an isolated/non-system prefix when learning/testing.
3. Run `./configure --help` before adding custom flags.
4. Keep include flags in `CPPFLAGS`, linker/search/rpath flags in `LDFLAGS`.
5. If configure fails, inspect `config.log` before changing anything else.
6. Build, then run the package's test target if present.
7. Run `make -n install` and verify every destination path before installation.
8. For patches, confirm source version + current working directory + strip level.
9. If rollback/install ownership is unclear → **[Needs confirmation]**.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| Extract source archive | Creates source tree/files | Path traversal/overwrite risk from untrusted archive |
| `./configure` | Generates Makefile/config headers/cache/log | Modifies build tree |
| `./configure --prefix=...` | Changes installation destination | Wrong prefix changes system/user layout |
| `CPPFLAGS=... ./configure` | Changes preprocessing tests/build flags | Wrong header/version selection |
| `LDFLAGS=... ./configure` | Changes linker/library/rpath behavior | Wrong library/version selection |
| `make` | Compiles project | Executes project build rules |
| `make check` | Runs test suite | May be CPU/time/resource intensive |
| `make clean` | Removes generated objects/binaries/libs | Destructive to build outputs |
| `make distclean` | Removes generated build/config files | Returns tree toward unpacked state |
| `make install` | Copies software to install prefix | **High impact**; may overwrite installed files |
| `make install-strip` | Installs stripped binaries/libs | Debug information removed |
| `checkinstall make install` | Tracks install into package workflow | Executes install and package-state changes |
| `patch -p0/-p1 < patch_file` | Modifies source files | Wrong tree/strip level can partially corrupt source |
| Edit `.pc` file | Alters future dependency flags | System/build-wide downstream effects |

## Verification / acceptance checks

| Change | Verification | Acceptance |
|---|---|---|
| Extraction | list resulting tree | Files confined to expected source directory |
| Configure | expected Makefile/config files + no error | Prefix/flags match intent |
| Custom flags | inspect `config.log` / generated build command | Correct include/library paths appear |
| Build | `make` completes | Expected artifacts exist |
| Tests | `make check` | Test target completes according to package |
| Install preview | `make -n install` | Only intended prefix/paths/actions |
| Install | inspect installed files + run intended binary | Installation isolated/functional |
| Patch | inspect diff result + rebuild/test | Only intended hunks/files changed |
| pkg-config path | relevant pkg-config query returns expected flags | Correct package metadata is selected |

## Rollback

- Source-tree experiment: remove isolated build/install tree and re-extract from the original archive.
- `make clean`: rebuild generated artifacts.
- `make distclean`: rerun configure and rebuild.
- `make install`: chapter provides no universal uninstall/transaction rollback. Prefer an isolated prefix or distro package wrapper; otherwise rollback is **[Needs confirmation]**.
- Patch: safest recovery is a clean source tree/re-extraction unless the package/version-control workflow gives a known reverse path.
- Flag/environment changes: remove the temporary assignment and reconfigure from a clean/distclean build tree.
- `.pc` edits: restore prior file before relying on pkg-config again.

## Guardrails

- Inspect archives before extraction.
- Treat absolute paths in an unknown source archive as a stop condition per source guidance.
- Read README/INSTALL before inventing build flags.
- Do not interpret successful `configure` as proof that compilation will succeed.
- Use `make -n install` before real installation.
- Prefer isolated prefixes for experiments.
- Do not edit source/Makefiles blindly when the error is only a downstream recursive make message.
- Prefer changing `prog` to `./prog` in a Makefile over broadening PATH with `.`.
