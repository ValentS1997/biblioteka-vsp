# Ответы на контрольные вопросы и задачи — глава 8

> Основание: вопросы `review-questions.md`, chapter RAG и canonical chapter artifacts. Security answers are explanatory/defensive. Вопросы, требующие внешнего исследования, помечены `[Needs confirmation]`.

1. Строгое complete mediation ухудшает прежде всего **производительность/latency**: каждое обращение к объекту приходится заново проверять через security mechanism, что добавляет CPU/I/O overhead.

2. CRC рассчитан на случайные ошибки, а не на активного противника. Злоумышленник может изменить message и **пересчитать CRC**, потому что CRC не использует secret key. Поэтому он не обеспечивает cryptographic integrity/authenticity.

3. Это **FIN scan** порта 21: отправляются FIN probes без установленного connection. Закрытый TCP port обычно отвечает RST, open port часто молчит. `host102:21` явно отвечает RST → host активен, port21 закрыт. Для остальных отсутствие ответа означает «open либо filtered/unreachable»; FIN scan сам по себе не доказывает, что host активен.

4. Flags FIN+PSH+URG — классический **Xmas scan**. На localhost сам host заведомо активен. Ports25 и10000 отвечают RST → закрыты. 22 и80 не отвечают в показанном trace → в обычной модели Xmas scan это соответствует open/filtered; без firewall context нельзя различить эти два состояния абсолютно.

5.  
   а) HTTP: attacker, контролирующий DNS destination, может читать/изменять traffic и полностью impersonate site.  
   б) HTTPS с self-signed cert защищает только если Alice заранее знает/pins правильный cert. Если она просто принимает любой warning, attacker подставит свой self-signed cert.  
   в) HTTPS с valid CA-signed cert: attacker без private key/valid cert не сможет пройти certificate validation; confidentiality/integrity/authenticity TLS сохраняются, хотя attacker может вызвать DoS.

6. Alerts50, false positives10 → TP=40, FP=10. Реальных атак70 → FN=30. TN=999,920.  
   Precision (40/50=) **0.80**.  
   Recall (40/70≈) **0.571**.  
   F1 ≈ **0.667**.  
   Accuracy ((40+999920)/10^6=) **99.996%**.

7. Это **base-rate fallacy**: атаки крайне редки, поэтому огромный TN count делает accuracy почти100%, хотя IDS пропустила30 из70 атак. Для security важнее precision/recall/FPR, а не одна accuracy.

8. В исходной RFC5961/Linux комбинации off-path attacker мог использовать side channel challenge-ACK rate, чтобы статистически выяснять наличие TCP connection/часть его state. Для defensive answer достаточно: наблюдается глобальная реакция TCP stack на invalid probes и по ней различается «существующий connection» vs «нет connection». Пошаговое воспроизведение exploit packets здесь не приводится; проверять только в изолированной лаборатории.

9. Начало plaintext: **“The time has come, the Walrus said, to talk of many things: of shoes and ships and sealing-wax, of cabbages and kings…”** — отрывок из *The Walrus and the Carpenter* Льюиса Кэрролла.

10. После columnar-transposition recovery получается: **“two computers are said to be interconnected if they are able to exchange information”**.

11. Не автоматически. Ciphertext короткого transposition key под monoalphabetic substitution всё ещё нужно cryptanalyze; без substitution key исходная column ordering неизвестна. Но сама transposition обычно имеет небольшое key space и message может быть атаковано напрямую, поэтому такая «защита ключа» не делает систему криптографически сильной.

12. Да, результат **тот же**: character substitution действует независимо на каждый symbol, а transposition только переставляет positions. Поэтому (T(S(P))=S(T(P))).

13. **[Needs confirmation]** Для вычисления 77-bit OTP нужен исходный ciphertext bitstring с илл. 8.11. Pad вычисляется как (K=Coplus P).

14. Можно заранее согласовать бесконечную последовательность book/page/offset и брать successive text bits только один раз. Но book text не является truly random, а если библиотека/порядок известны attacker, это **не настоящий one-time pad**; information-theoretic security требует случайного секретного keystream.

15. Bit duration при250 Gbit/s =4 ps. За это время свет в fiber проходит (2·10^8·4·10^{-12}=8·10^{-4}) m =800 µm. При «длине фотона»1 µm получается примерно **800 photons per bit interval**.

16. Eve выбирает правильный quantum basis с вероятностью1/2. При неправильном basis Bob после sift получает wrong bit с вероятностью1/2. Средняя error rate: **1/2·1/2=25%** sifted key.

17. Оба вида redundancy помогают проверять candidate key. Known fixed prefix даёт немедленный known-plaintext test; hash suffix требует расшифровать candidate message и проверить hash, но также валидирует правильность key. Hash лучше связывает redundancy со всем message, но не устраняет brute-force verification.

18. Нужны:  
   - **freshness** — nonce/timestamp/sequence number, чтобы не replay старую transaction;  
   - **cryptographic integrity/redundancy** — MAC/hash/signature over identities+amount+freshness.  
   Просто шифрования полей недостаточно.

19. Даже идеальный E2E cipher не защищает endpoints. Два пути: **скомпрометировать/изъять endpoint до encryption/после decryption** либо получить keys/plaintext от участников (legal compulsion, insider, social engineering). Traffic metadata также остаётся наблюдаемой, хотя не раскрывает content.

20. (10^{16}) speedup требует (log_2 10^{16}≈53.15) doublings. По1.5 года: **≈79.7 года** при неизменном законе Мура.

21. **(2^{256}≈1.16·10^{77})** keys. Это астрономически большое пространство; поиск внешних сравнений из физики/астрономии прямо требуется вопросом, поэтому конкретные internet examples: **[Needs confirmation]** в RAG-only режиме.

22. В CBC insertion одного ciphertext bit сдвигает block boundaries. Без внешнего framing/resynchronization **все последующие blocks** будут интерпретироваться со смещением и фактически повреждены, а не только один-два блока.

23. CBC требует примерно **один block-cipher encryption на block**. CFB требует один block-cipher invocation на feedback unit; при full-block CFB затраты сопоставимы, а при (r)-bit feedback — примерно block_size/(r) раз больше операций. Поэтому CBC эффективнее мелкосегментного CFB.

24. Сообщение вида (E_B(D_A(P))): Bob применяет свой private key (D_B), получает (D_A(P)), затем применяет Alice public key (E_A) и получает (P). Outer layer обеспечивает confidentiality для Bob, inner operation — Alice signature.

25. Модификация ломает RSA: private exponent должен быть inverse modulo (arphi(n)) (или Carmichael function), а не modulo (n). Более того, если (d) вычисляется как inverse public (e) modulo public (n), любой может вычислить (d) расширенным Euclid. Схема становится **тривиально взламываемой**.

26. Да, немедленно. Если (d_1=e_2) и (n_1=n_2), public key второго пользователя раскрывает private exponent первого. Shared modulus сам по себе тоже опасен. Ключи нужно заменить.

27. Если Bob после получения signed document держит его только в RAM и crashes, он может потерять document/transaction state, но другая сторона считать delivery завершённой. Решение — **stable storage/write-ahead log до подтверждения**, затем ACK/commit.

28. Trudy не может просто заменить и message, и signature: для нового message нужна signature, создаваемая Alice private key. Bob проверит подпись и заметит подмену, если attacker не способен forge signature или найти допустимую hash collision.

29. Уязвимость — **birthday/collision attack**: attacker заранее генерирует множество безобидных вариантов договора и множество выгодных ему вариантов, меняя несущественные детали, пока не найдёт пару с одинаковым hash. Жертва подписывает hash безобидного текста, после чего подпись математически подходит коллидирующему мошенническому документу. Защита — collision-resistant hash и проверка exact bytes перед подписью.

30. Для181 возможного дня:  
   (P=1-prod_{i=0}^{24}(181-i)/181≈) **0.824**, то есть около **82.4%**.

31. Да, если используется слабый hash. Secretary может подготовить много семантически одинаковых вариантов честного dictated message и много поддельных вариантов, меняя whitespace/wording до hash collision. Marilyn проверит честный текст, но signature/hash затем может быть перенесён на colliding malicious variant. Сильный collision-resistant hash устраняет практичность такого attack.

32. Да. Уже общий secret key можно использовать как **authenticated secure channel/MAC**: Bob передаёт свой public key по каналу, защищённому shared key, и Alice проверяет integrity/authenticity. Тогда MITM не сможет заменить key.

33. Alice должна проверить CA signature certificate с известным root public key, validity/name/usage/revocation, убедиться, что subject — Bob, а затем потребовать **proof of possession** соответствующего private key (challenge/signature или authenticated handshake).

34. Построить certification path: получить certificate CA X, подписанный его parent, затем parent и т.д. до trust anchor Alice; проверить все signatures/validity/name constraints. После chain validation Bob должен доказать possession private key из своего certificate.

35. Обычно **нет**. AH authenticates IP header fields, а NAT изменяет addresses (и часто transport mapping), из-за чего integrity check ломается. NAT-friendly deployments используют ESP/NAT-T/tunnel architecture вместо AH через NAT.

36. Если нужна просто digest function — **SHA-256** как SHA-2 member. Если нужна message authentication между Alice и Bob с shared secret — **HMAC-SHA-256**, а не plain hash.

37. HMAC намного дешевле RSA signature по CPU и размеру, не требует public-key operations/certificate validation. Минус: shared secret означает отсутствие nonrepudiation.

38. Inbound filtering блокирует внешние attacks/unsolicited traffic. Outbound filtering ограничивает malware callbacks, exfiltration и spoofed-source traffic из compromised hosts. Эффективность ограничена encryption/tunneling, allowed ports и false positives, поэтому firewall — только один слой defense.

39. Public announcement/несекретный operational status внутри уже защищённой site-to-site VPN не требует дополнительной application encryption. Passwords, payroll, keys или sensitive management traffic разумно защищать end-to-end дополнительно, если LAN endpoints/gateways/admins не входят в один trust boundary.

40. Сделать challenge responses **direction-specific**, например включить identity/role: Bob отвечает MAC/enc(`R_A,"Bob"`), Alice — MAC/enc(`R_B,"Alice"`), либо использовать разные keys по направлениям. Тогда отражённый ciphertext от другой стороны не является допустимым response.

41. Alice вычисляет (125^{12}mod227), Bob — (82^3mod227). Оба получают **212** — общий secret.

42. а) Без authentication MITM подменяет public DH values и устанавливает отдельный key с Alice и Bob.  
   б) Секретность (p) или (g) не является правильным решением: protocol parameters обычно public; если attacker их узнает, MITM остаётся. Нужно **authenticate DH exchange** (signature/MAC/certificate).

43. Identity A не является secret; Bob должен знать, **с кем связывать ticket/session key** и какую security context использовать. Поэтому A можно передать plaintext рядом с opaque encrypted ticket.

44. Nonces/timestamps обеспечивают **freshness**, главным образом поддерживая authentication и replay resistance. Они сами по себе не дают confidentiality/availability/nonrepudiation; integrity нужна, чтобы attacker не мог их безнаказанно заменить.

45. Это блокирует конкретный known-fixed-prefix attack, пока случайный per-user prefix остаётся secret. Но он просто превращается во **второй secret key**: при утечке/known plaintext проблема возвращается; повторное использование и структура messages всё ещё могут давать cryptanalytic information.

46. Public-key encryption обеспечивает confidentiality (encrypt recipient public key). Digital signature/private-key operation + hash даёт integrity/authentication и может поддерживать nonrepudiation. **Availability криптографией не обеспечивается** — attacker всё ещё может блокировать/DoS traffic.

47. Plain message digest сам по себе не даёт confidentiality или availability и против активного attacker не гарантирует authenticity: attacker может пересчитать digest. Integrity/authentication требуют keyed MAC или signature; nonrepudiation — digital signature. Поэтому одним обычным digest все пять свойств не обеспечить.

48. Не излишество, если (R_{A1}) и (R_{A2}) связывают разные protocol exchanges/стадии freshness. Повторное использование одного nonce в двух ролях может открыть replay/reflection ambiguity. Без точной message sequence илл. Needham–Schroeder нельзя безопасно удалить один запрос.

49. При отказе AS новые users не смогут получить initial tickets; при отказе TGS нельзя получить новые service tickets. Existing valid tickets могут работать до expiry. То есть страдает **availability**, но security не должна автоматически снижаться; compromise этих servers, напротив, критичен для всей trust domain.

50. Обычно повторять authentication не нужно: nonce/challenge не обязан быть secret, если attacker всё равно не может сформировать требуемый cryptographic response. Важно, что (R_B) fresh и response cryptographically bound к Bob/Alice/session.

51. По той же причине (R_B) можно послать plaintext: challenge обеспечивает freshness, а не confidentiality. Encryption полезна только если конкретная схема дополнительно полагается на secrecy nonce; нормальный challenge-response не должен.

52. Smart card сама содержит private key и PIN verifier. Terminal передаёт card transaction details+fresh nonce; card показывает amount/merchant на собственном display, пользователь вводит PIN **на карте**, карта после проверки PIN подписывает transaction. Private key/PIN не покидают card; банк проверяет signature и nonce. Compromised cashier terminal не может подделать другую сумму незаметно, если пользователь проверяет card display.

53. Это phishing: ссылка в письме вела на поддельный bank site, который собрал credentials. Attacker затем использовал их против настоящего банка и выполнил transaction позже; отсутствие «новых операций» на fake page только создало ложное чувство безопасности. Защита — не входить по mail links, проверять origin/TLS и использовать phishing-resistant MFA.

54. PGP сжимает message **до encryption**, чтобы уменьшить размер/bandwidth и убрать статистическую redundancy/patterns, облегчающие cryptanalysis. После encryption compression почти неэффективна.

55. Да. Один content ciphertext можно multicast всем, но session key должен быть доступен каждому authorised recipient — например, тот же session key шифруется отдельно public key каждого участника. Overhead/key-management растёт с group size; membership/revocation требуют обновления.

56. Нет. Нужен корректный public key recipient, доверие к его binding и PGP-compatible software/private key на стороне получателя. Произвольный internet address не гарантирует наличие/валидность этих условий.

57. SSL/TLS nonces обеспечивают freshness и входят в key derivation, чтобы даже при одинаковом premaster secret sessions получали разные keys. Они предотвращают replay/precomputation; секретными быть не обязаны.

58. Capacity при 1 LSB каждого RGB channel: (2048·1536·3=9,437,184) bits = **1,179,648 bytes =1.125 MiB**. Из файла2.5 MiB это **45%**. После compression×4 файл0.625 MiB — **помещается целиком**.

59. Да. Steganographic channel хранит arbitrary bits, поэтому вместо ASCII можно embed encoded music. Максимальный объём определяется количеством доступных LSB pixels/channels, а не типом payload; music нужно предварительно представить как binary file.

60. 60 MiB → (60·2^{20}·8/3≈167,772,160) pixels. Для aspect3:2 (W=3k,H=2k): **примерно 15,864×10,576 pixels**. После compression×3 (20 MiB): **примерно 9,159×6,106 pixels**.

61. Создать долгоживущую **псевдонимную digital-signature key pair**, опубликовать public key как identity псевдонима и подписывать каждый post private key. Remailer скрывает реальную identity, а signature не даёт Trudy писать от имени того же pseudonym.

62. **[Needs confirmation]** Вопрос требует внешнего исследования Meltdown/Spectre. В RAG-only режиме не добавляю интернет-описание, отсутствующее в главе.

63. Возможны rogue/evil-twin AP, compromised hotel AP или локальные attacks на неправильно изолированный WLAN. Уникальный hotel password не гарантирует end-to-end confidentiality: operator/AP видит plaintext protocols; fake AP может попытаться перехватить authentication. HTTPS/TLS остаётся необходимой end-to-end защитой.

64. **[Needs confirmation]** Требуется внешний поиск реального privacy case.

65. Educational construction: CSPRNG, seeded key, генерирует keystream; каждый input byte XOR с next keystream byte, та же операция decrypts. Для реальной безопасности нельзя писать «свой хороший RNG» — использовать проверенный stream cipher/CSPRNG и nonce/key discipline.

66. В постановке есть несогласованность: **SHA-2 не имеет стандартного 20-byte digest** (SHA-256=32 bytes и т.д.), а FIPS 180-1 относится к старому SHA-1. Корректный SHA-256 API должен иметь минимум 32-byte output buffer; 20 bytes означали бы SHA-1 или явное truncation.

67. Educational CBC: pad input до 8-byte blocks; (C_0=IV); для каждого (P_i): (X_i=P_ioplus C_{i-1}), затем применить toy substitution (E_k) к каждому byte → (C_i). Decrypt inverse substitution, XOR previous ciphertext, remove documented padding. Caesar-like substitution не является secure cipher; пример только демонстрирует chaining.

68. Toy RSA: проверить primes (p,q); (n=pq), (z=(p-1)(q-1)); выбрать (e) with gcd(e,z)=1; найти (d=e^{-1}mod z). Для ASCII byte (m<n): encrypt (c=m^emod n), decrypt (m=c^dmod n). Нужно (n>255). Это учебная схема: real RSA требует large keys и secure padding, посимвольный textbook RSA небезопасен.
