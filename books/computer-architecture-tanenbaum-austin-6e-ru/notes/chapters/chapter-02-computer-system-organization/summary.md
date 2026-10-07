# Краткое содержание главы 2

**Provenance:** `p0167:c01`–`p0168:c01`, PDF pages 167–168.

## Processor

Computer systems have three major components: processor, memory and I/O.

Processor behavior follows fetch–decode–execute. The source notes that this behavior can itself be implemented by a lower-level interpreter.

Performance is improved through pipelines, superscalar functional units and multiple processors.

Parallel systems include:

- array/SIMD-style processors applying one operation to different data;
- multiprocessors sharing memory;
- multicomputers with private memory and message exchange.

## Memory

Main memory stores active programs/data and has much lower latency than secondary storage. Cache reduces average access time; error-correcting codes can improve reliability.

Secondary storage has higher and often location-dependent access time. The chapter discusses magnetic disks, SSD, RAID and optical media.

## I/O

I/O devices transfer information into/out of the computer and connect through controllers and one or more interconnects/buses.

Examples include display/terminal devices, mice, printers, modems and cameras.

For character representation, the source contrasts ASCII with Unicode and describes UTF-8 as an increasingly important interoperable encoding.

## Chapter synthesis

```text
processor throughput
+ memory hierarchy/locality
+ storage latency/reliability
+ I/O controller/interconnect bandwidth
= observable system performance
```
