# Ответы на контрольные вопросы и задачи — глава 7

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Внешние lookup-задания и данные, отсутствующие в RAG, помечены `[Needs confirmation]`.

1. В DNS zone-file имя без завершающей точки считается **относительным** к текущему zone origin. Поэтому `laserjet` автоматически дополняется suffix текущей зоны; точка сделала бы имя абсолютным.

2. При пустом cache iterative resolver делает четыре query/response пары: root → `.edu` → `uchicago.edu` → authoritative server for `cs.uchicago.edu`. Это **8 DNS messages/steps**. На практике так бывает при cold cache/expired TTL, когда ни одна delegation не закэширована.

3. **DS record** в parent zone подтверждает/связывает child DNSKEY с chain of trust.

4. Подпись RRset хранится в **RRSIG**, а проверяется public key из **DNSKEY** record. Поэтому validating resolver использует DNSKEY для проверки RRSIG.

5. CDN/DNS mapper смотрит, от какого recursive resolver (или EDNS Client Subnet) пришёл query, оценивает его network/geographic proximity до candidate content servers и возвращает address ближайшего/наименее загруженного node. Ключевое допущение: **resolver location достаточно хорошо приближает location клиента**; без ECS это иногда неверно.

6. Уже закэшированные names продолжат работать до TTL expiry, а соединения по известным IP могут устанавливаться. Новые/неизвестные DNS names перестанут разрешаться, поэтому Web, mail и множество приложений практически станут недоступны, хотя IP routing как таковой продолжит работать.

7. TCP: reliable ordered transfer, нет UDP-size/truncation проблемы, удобно для large DNS/DNSSEC responses; минусы — handshake latency, connection state, CPU/memory и больше traffic. UDP дешевле и обычно даёт query/response за один RTT, но large response может потребовать retry/TCP.

8. При plaintext DNS запросы могут видеть local network/router, access ISP/on-path observers и recursive resolver. При DoH/DoT on-path observers видят encrypted connection к resolver, но **сам resolver** всё равно знает query; authoritative servers видят queries resolver-а, обычно не конечного устройства.

9. Нет. DNS full name ограничен примерно 253 printable characters, а отдельный label — 63 octets. Один secondary label длиной 253 символа нарушает label limit.

10. Да. Одно DNS name может иметь несколько A/AAAA records — multihoming, load balancing, anycast/service replicas.

11. Да. Например, `example.com` и `example.org` могут указывать на один и тот же IP/host; один из них также может быть CNAME к другому.

12. Это **envelope-level delivery instruction**, потому что оно управляет поведением mail transfer system при недоставке, а не содержанием письма для конечного пользователя.

13. Полю `From:` доверять нельзя — SMTP sender header можно подделать. Проверка: cryptographic mail signature (PGP/S/MIME) либо domain authentication mechanisms/Received-chain; без такой проверки identity не подтверждена.

14. Нужно стандартизовать разные культуры имен: порядок family/given names, отсутствие/несколько фамилий, patronymics, Unicode/scripts/diacritics, transliteration, case/normalization, prefixes/suffixes и проблему совпадающих имён.

15. Ввести новый canonical `firstname.lastname@` и **сохранить старые addresses как aliases/forwarding entries** на те же mailboxes. Затем постепенно обновить address books и внешние контакты.

16. Base64: (4·lceil100/3ceil=) **136 ASCII characters** (включая padding, без line breaks).

17. Правильный Base64 для ASCII `ascii` — **`YXNjaWk=`**. В варианте сокурсника повреждён последний encoded character и отсутствует required padding.

18. Да, если server пересылает message body как opaque ASCII text: binary file можно Base64-encode на sender client и decode на receiver client. Цена — примерно 33% size overhead. Если server валидирует/меняет content, это может не сработать.

19. Например:  
   - whitespace = ровно один ASCII SP;  
   - whitespace = один или более SP/HTAB, возможно с folding CRLF+WSP.  
   Стандарт должен выбрать одно точное определение для interoperable parsing.

20. **[Needs confirmation]** Вопрос прямо просит MIME types, отсутствующие в тексте, из браузера/интернета. Это внешняя информация и вне текущего RAG-only scope.

21. Да. MIME поддерживает разбиение/представление message parts; файл можно разделить на несколько сообщений/parts меньше 1 MB и затем собрать. Нужно учитывать Base64 overhead, поэтому raw chunks должны быть заметно меньше лимита.

22. Нет. IMAP стандартизует **protocol operations и представление данных на wire**, а не внутренний mailbox storage. Сервер может хранить письма как угодно, если корректно реализует IMAP semantics.

23. Стандартный синтаксис: **`https://host.example:8443/path/file`** — port после hostname через двоеточие.

24. Общий FTP URL: **`ftp://<ftp-host>/pub/forReview/newProof.pdf`** (если `ftp/` — filesystem root prefix, он может присутствовать в path). Конкретное hostname в вопросе не задано: **[Needs confirmation]**.

25. Пусть после первого ответа каждый последовательный request добавляет одинаковые 50 ms: pipelining даёт 200 ms против initial150 ms, значит один response interval≈50 ms. (3000=150+(N-1)·50) → **N=58 requests**.

26. TCP обеспечивает reliable byte stream только пока connection существует. Host/link failure всё равно может оборвать connection после частичного request/response; приложение должно обрабатывать timeout/reset, retry, idempotency и восстановление state.

27.  
   а) Календарь — **JavaScript лучше**: всё вычисляется локально, server state не нужен.  
   б) Flight schedule — **PHP/server-side лучше** для запроса authoritative database; JS удобен для UI, но данные всё равно приходят с сервера.  
   в) Полином по пользовательским коэффициентам — **JavaScript лучше**, локальная математика без server round trip.

28. Обычно эффективнее для **JPEG**: image большой и редко меняется, поэтому 304/validation экономит много bytes. HTML чаще меняется и обычно меньше, поэтому вероятность/выигрыш cache validation ниже.

29. Если Expires ещё не наступил, browser вправе использовать cached copy без request к server. Поэтому server может уже иметь новую версию, но **не может прислать её сам**, пока client не revalidate/reload или не истечёт freshness lifetime.

30. Да. ISP может разместить cache/CDN nodes внутри своей сети рядом с subscribers и заключать договоры с content providers. Недостаток — coverage ограничен клиентской базой ISP; для global CDN нужны узлы и routing/mapping во многих сетях.

31. Stereo CD: (44,100·16·2=) **1.4112 Мбит/с**. За час: **635,040,000 bytes ≈635 MB**. Оставшаяся физическая ёмкость нужна для дополнительного времени записи и служебных/ECC/synchronization structures формата диска.

32. 44.1 kHz уже даёт Nyquist frequency 22.05 kHz, покрывая обычный audible band; 88 kHz даёт мало слышимого выигрыша при удвоении data rate. 24-bit samples увеличивают dynamic range/уменьшают quantization noise, но практический выигрыш зависит от analog chain/noise и часто меньше роста объёма.

33. Два часа stereo CD: (1.4112	ext{ Мбит/с}·7200/8=) **1,270,080,000 bytes ≈1.27 GB**.

34. 32 кбит/с ×0.1 s =3200 bit = **400 bytes**. При1 s: **4000 bytes**.

35. При 1 Мбит/с и one-way100 ms в пути находится ~100 kbit=12.5 KB data. Если client посылает resume signal при low-water mark и ждёт round trip, запас должен быть хотя бы ~200 ms traffic = **25 KB**. High-water mark должен быть ниже 2 MB capacity минимум на объём data/control, уже находящийся in flight. Точные thresholds зависят от выбранного control algorithm.

36. Raw video: (2048·1024·16·60≈2.013) Гбит/с. При32:1 → **≈62.9 Мбит/с =7.864 MB/s**. 64 MiB buffer хватает (67,108,864/7,864,320≈8.53) s. До конца осталось10 s → **нет**, примерно 1.47 s видео не хватит.

37. Интерливить соседние audio samples между разными packets и использовать небольшие packets/FEC/packet-loss concealment. Тогда loss удалит отдельные dispersed samples, вызывая небольшой noise/quality drop вместо длинного audible gap.

38. Да. Audio stream тоже имеет fixed playback rate и network jitter; prebuffer + low/high water marks сглаживают arrival variation. Отличаются только bitrate/acceptable latency/размер thresholds.

39. Delay — абсолютное время доставки; jitter — **изменение delay от packet к packet**. Propagation даёт почти постоянный delay, queueing/congestion — variable. Jitter можно сгладить playout buffer; уменьшить физический propagation delay буфером нельзя — буфер лишь добавляет дополнительную latency.

40. (1920·1080·16·60=) **1,990,656,000 бит/с ≈1.99 Гбит/с**.

41. 4K 3840×2160×3 bytes×60 = **11.944 Гбит/с** raw. Для 80 Мбит/с нужен compression ratio примерно **149:1**.

42. Segment boundary может попасть на P/B-frame, зависящий от frames предыдущего segment, поэтому segment нельзя независимо decode/switch representation. Нужно **выравнивать segments по GOP/I-frame** либо вставлять independent I-frame в начало каждого segment.

43. Reordering ломает decode/timing и inter-frame dependencies. Решение — sequence numbers + reorder/jitter buffer. Цена — дополнительная latency/memory; packet, пришедший после playout deadline, всё равно придётся discard.

44. Новый transport protocol не может отменить propagation delay, bandwidth limit и variable queueing по пути. Можно изменить trade-offs reliability/order/congestion, но одновременно гарантировать низкие delay+jitter на перегруженной сети без resource reservation/QoS невозможно.

45. 50 000 clients×3/month=150 000 views/month; 2/3 at21:00 →100 000/month ≈**3333 одновременных starts в день** при 30 днях. По4 Мбит/с →≈13.33 Гбит/с. OC-12≈622 Мбит/с line rate → минимум **22 OC-12** (по payload capacity — порядка 23).

46. CDN мало полезен для rarely requested, highly dynamic/personalized/uncacheable content, маленькой географически локальной аудитории, строгой confidentiality/data-sovereignty модели или когда CDN overhead/cost выше экономии backbone/origin traffic.

47. Для Zipf (p_kpropto1/k). Доля top10 ≈ (H_{10}/H_{2·10^9}approx2.929/21.99≈) **13.3%**.

48. Classic BitTorrent использует **tracker** для peer discovery и `.torrent` metadata/distribution. DHT уменьшает зависимость от tracker, но bootstrap/metadata/indexing всё равно могут иметь централизованные элементы.

49. Modified client может лгать об upload contribution, запускать много identities (Sybil), selectively refuse uploads, эксплуатировать optimistic unchokes или collude с peers. Choking/tit-for-tat incentives уменьшают free-riding, но не делают cheating невозможным.
