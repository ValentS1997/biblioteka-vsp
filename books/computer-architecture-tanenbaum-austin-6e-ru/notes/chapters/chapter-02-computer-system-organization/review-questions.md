# Вопросы и задания — глава 2

**Provenance:** `p0168:c01`–`p0171:c01`, PDF pages 168–171.

Нумерация источника сохранена; формулировки структурно очищены без добавления внешнего содержания.

1. Для datapath на рис. 2.2: загрузка ALU registers 5 ns, ALU 10 ns, write-back 5 ns. Максимум MIPS без pipeline?
2. Зачем в fetch-decode-execute нужен шаг advance PC? Что будет без него?
3. Machine 1: 10 ns/instruction; machine 2: 5 ns/instruction. Достаточно ли этого, чтобы утверждать, что machine 2 быстрее?
4. Для single-chip embedded computer, где memory работает со скоростью CPU, оценить применимость RISC design principles.
5. Монастырь: настоятель диктует одно слово, множество писцов одновременно записывают его в разные книги. Какой processor-level parallelism это напоминает?
6. Каково отношение access time optical disk к register memory в пятиуровневой hierarchy, если диск уже вставлен?
7. В ternary memory один trit ∈ {0,1,2}. Сколько trits нужно для 6-bit number? Формула для n bits.
8. Eye data rate: 10^6 pixels, 3 colors × 64 intensity levels, temporal resolution 100 ms.
9. Ear data rate: sample rate 44 kHz, 16-bit samples.
10. DNA: 3×10^9 nucleotides, 4 symbols, 30,000 genes. Total bits and average bits/gene.
11. Почему 1,073,741,824 bytes — естественный memory size?
12. Построить 7-bit Hamming code with parity for decimal digits 0–9.
13. Построить code for digits 0–9 with Hamming distance 2.
14. Для Hamming total length 2^n−1 вычислить percentage parity bits for n=3…10.
15. Encode extended-ASCII string “Earth” with Hamming parity into 3-hex-digit codewords.
16. Decode: `0D3 DD3 0F2 5C1 1C5 CE3`.
17. Disk: 1024 sectors/track, 7200 rpm. Track transfer rate?
18. Bus cycle 5 ns, 32-bit word/cycle; Ultra4-SCSI 160 MB/s; CPU fetches/executes 32-bit instruction every 25 ns. How much does disk slow CPU?
19. Disk blocks numbered inner→outer. Does allocation direction matter?
20. Read disk: 10,000 cylinders × 4 tracks × 2048 sectors; 10 ms/revolution; adjacent-cylinder seek 1 ms; head switch inside cylinder instantaneous. Total time?
21. Why RAID 2 if RAID 3 corrects a single failed bit/disk with one parity disk?
22. Exact 80-minute CD-ROM type-2 capacity; user-data capacity type 1.
23. CD-R type 1 at 10×: laser pulse duration.
24. Compression required for 133-minute 720×480×24-bit video at 30 fps on one-sided single-layer DVD, with extra 3.5 GB item stated by source.
25. Read 25-GB Blu-ray at 4.5 Mbit/s: total time.
26. How can terminal advertise 2^24 possible colors while keeping one byte per pixel?
27. Alien eye: 10^8 pixels, five channels, 32 levels/channel, 10-ms temporal resolution. GB/s?
28. 1920×1080 display refreshed 75/s. Pixel pulse duration?
29. Laser printer toner estimate from 50×80 chars/page, 2×2 mm per char, 25% toner coverage, 25 μm thickness, 25×8×2 cm cartridge.
30. 64-frequency synchronous modem with n time slots/sec: bit rate?
31. 12-MHz cable, QAM-64, n homes, fraction f inactive. When is per-active-user cable rate > 2 Mbit/s ADSL?
32. Camera 3000×2000, RGB 3 bytes/pixel, JPEG 5× compression, save in 2 s. Required write rate?
33. 24-million-pixel camera, source wording says 6 bytes «per bit», 8-GB card, 5× compression. Image count?
34. Estimate text characters in typical CS book; ASCII+parity bits; media needed for 10,000 books on CDs and single-sided dual-layer DVDs.
35. Write `hamming(ascii, encoded)`: 7 data bits → 11-bit Hamming word.
36. Write `distance(code, n, k)`: minimum Hamming distance among n k-bit codewords.
