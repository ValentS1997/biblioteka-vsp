# Команды и системные примитивы — глава 2

**Provenance:** RAG `p0076:c01`–`p0171:c01`.

## Shell / administrative commands

**[Not applicable].**

Chapter RAG не содержит operational CLI sequence для Linux, firmware, RAID tools, PCI utilities, disks или networking. Такие команды не добавляются.

## Source-confirmed processor primitives

| Primitive | Source meaning |
|---|---|
| fetch | load next instruction from memory |
| decode | determine instruction type/resources |
| execute | perform operation through datapath/ALU |
| LOAD | move operand from memory to register |
| STORE | move register value to memory |
| control transfer | change instruction flow |
| PC advance | point to next instruction |

## System mechanisms

| Mechanism | Role | Class |
|---|---|---|
| DMA | controller reads/writes memory without CPU moving every word | system mechanism |
| interrupt | controller signals CPU after I/O completion | control transfer |
| bus arbitration | resolves simultaneous bus requests | shared-resource policy |
| cycle stealing | I/O consumes memory/bus cycles otherwise available to CPU | performance effect |
| SCSI command block | controller sends commands to target device | device protocol |
| cache-line fill | transfer block from memory after miss | memory-system operation |

## Named interfaces

Source discusses IDE/EIDE, SCSI, RAID 0–5, PCI, PCI Express, ASCII, Unicode and UTF-8. No configuration syntax is supplied.

## Source listing

Page 79 contains a Java-like interpreter illustrating fetch/decode/execute. Extracted method declaration is malformed, so the listing is not reproduced as executable code. See [source-findings.md](source-findings.md).

## State-changing actions

**[Not applicable].**

## Verification

Any future CLI command must have explicit chapter-RAG evidence. Familiar tools such as `lspci`, `hdparm`, `smartctl`, `mdadm` are intentionally absent.

## Rollback

**[Not applicable].**
