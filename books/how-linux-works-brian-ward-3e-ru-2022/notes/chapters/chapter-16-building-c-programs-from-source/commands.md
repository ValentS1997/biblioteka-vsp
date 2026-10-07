# Команды и интерфейсы — глава 16 «Компиляция программ из исходного кода на языке C»

**Provenance:** `p0442:c01`–`p0457:c01`, PDF/печатные страницы 442–457. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only/dry-run; **WG** — workload-generating; **SC** — state-changing; **SC-D** — destructive/high-impact.

## 1. Inspect source archive before extraction

```sh
tar tvf archive.tar
tar ztvf archive.tar.gz
```

**Class:** RO.

The chapter uses archive listing to detect:
- whether files are grouped under one package directory;
- whether top-level loose files would clutter the current directory;
- suspicious absolute-path members.

Extraction commands themselves are referenced back to chapter 2 but not repeated explicitly here; no new syntax is invented.

## 2. Configure with GNU Autoconf

```sh
./configure
./configure --prefix=$HOME/mycoreutils
./configure --prefix=new_prefix
./configure --help
```

**Class:** SC build-tree generation.

Source says configure can create:
- one or more Makefiles;
- `config.h`;
- `config.cache`;
- diagnostic output/log evidence.

Useful source options:

```text
--bindir=directory
--sbindir=directory
--libdir=directory
--disable-shared
--with-package=directory
```

Not every `configure` recognizes every `--with-package` form.

## 3. Out-of-tree build concept

Source describes creating a separate build directory and invoking the source tree's `configure` from there.

**Class:** SC build-tree creation.

No exact shell command sequence is supplied in the retrieved text, so none is invented.

## 4. Configure environment/flags

```sh
CPPFLAGS=-DDEBUG ./configure
./configure CPPFLAGS=-DDEBUG
CPPFLAGS=-Iinclude_dir ./configure
LDFLAGS=-Llib_dir ./configure
LDFLAGS="-Llib_dir -Wl,-rpath=lib_dir" ./configure
```

Source roles:
- `CPPFLAGS`: preprocessor/include flags;
- `CFLAGS`: compiler flags;
- `LDFLAGS`: linker/library search/rpath flags.

The source demonstrates a malformed example:

```sh
CPPFLAGS=Iinclude_dir ./configure
```

which leads to `C compiler cannot create executables`. It is included only as failure evidence, not as a recommended command.

## 5. Build, test and install

```sh
make
make check
make -n install
make install
make clean
make distclean
make install-strip
```

Classification:

| Command | Class | Effect |
|---|---|---|
| `make` | WG/SC | Builds project artifacts |
| `make check` | WG | Runs package test suite if provided |
| `make -n install` | RO/dry-run | Prints install commands without applying them under source model |
| `make install` | SC-D | Installs/copies files to configured locations |
| `make clean` | SC-D build tree | Removes object/executable/library build outputs |
| `make distclean` | SC-D build tree | Also removes generated config/Makefiles/logs |
| `make install-strip` | SC-D | Installs while stripping symbols/debug information |

The chapter explicitly requires reviewing `make -n install` before real install.

## 6. Package-building wrapper

Literal source command:

```sh
checkinstall make install
```

The text shows it with a root prompt (`#`).

**Class:** SC-D package/install state.

Source description:
- tracks files that installation would place on system;
- creates a `.deb`;
- resulting package can later be handled with `dpkg`.

RPM-related source tools are named:
- `rpmdev-setuptree`;
- `rpmbuild`.

No full RPM command sequence is provided, so none is invented.

## 7. config.log inspection

Source suggests opening `config.log` with `less`, going to the end using uppercase `G`, then reverse-searching with `?`.

```sh
less config.log
```

**Class:** RO.

Search target can be a fragment from configure output such as `for more details`.

## 8. pkg-config

```sh
pkg-config --libs zlib
pkg-config --list-all
```

General source syntax:

```text
pkg-config options package1 package2 ...
```

Source metadata files end in `.pc`.

Example source path:
`/usr/lib/x86_64-linux-gnu/pkgconfig/openssl.pc`.

The text says a pkg-config installed under `/usr/local` normally searches `/usr/local/lib/pkgconfig`.

## 9. PKG_CONFIG_PATH / .pc handling

Source-supported approaches for nonstandard `.pc` paths:
1. create symlinks/copies into the main pkgconfig directory;
2. set `PKG_CONFIG_PATH` to include additional pkgconfig directories.

**Class:** SC environment/filesystem configuration.

No concrete `export PKG_CONFIG_PATH=...` command is shown in retrieved text, so no syntax is invented.

Source says editing a `.pc` file could add linker flags such as `-Wl,-rpath=${libdir}`; this changes downstream build behavior.

## 10. Applying patches

```sh
patch -p0 < patch_file
patch -p1 < patch_file
```

**Class:** SC source tree.

- `-p0`: keep path components as represented by patch.
- `-p1`: strip one leading path component in the source example.

A prompt:

```text
File to patch:
```

is treated as evidence that working directory/path level/source version does not match expectations.

## 11. Build troubleshooting / package lookup

Source commands for missing header investigation:

```sh
man 2 time
man 3 time
apt-file search pkg.h
yum provides */pkg.h
```

Classification:
- `man`: RO documentation lookup;
- `apt-file search`, `yum provides`: RO package metadata queries in the source context.

The exact current availability/syntax of distro tools is **[Needs confirmation]**.

## 12. Make error interpretation

Source examples:

```text
make: *** [target] Error 1
make: *** [target] Error 1 (ignored)
make[3]: *** [file.o] Error 1
make[2]: *** [all] Error 2
make: *** [all] Error 2
```

Operational reading:
- `(ignored)` means the Makefile intentionally ignores that error;
- nested `make[N]` lines often propagate an earlier compiler/tool failure;
- inspect the error immediately before the first relevant make failure.

## 13. Local helper executable in a broken Makefile

Source recommends changing a command from:

```text
prog
```

to:

```text
./prog
```

when the build created a helper in the current directory but assumes `.` is in PATH.

The source also gives temporarily adding `.` to PATH as an alternative. These artifacts do **not** promote that fallback because it broadens command lookup; the narrower source-supported edit is preferred.

## Command discipline

- Inspect archive structure before extraction.
- Read README/INSTALL before introducing custom flags.
- Use stage-correct variables: `CPPFLAGS`, `CFLAGS`, `LDFLAGS`.
- Read `config.log` before guessing at configure failures.
- Use `make -n install` before real install.
- Treat `make install`, `install-strip`, package wrappers and `patch` as modifying actions.
- Preserve literal source syntax when examples are internally inconsistent; record the mismatch instead of silently correcting it.
