// Cisco Flashcards - Exam & Interview Questions
// Mapped to CCNA 200-301, CCNP ENARSI, and Real Interview Scenarios
export interface Flashcard {
  id: string;
  category: 'fundamentals' | 'routing' | 'switching' | 'security' | 'services' | 'advanced';
  type: 'exam' | 'interview' | 'concept';
  difficulty: 'easy' | 'medium' | 'hard';
  front: string;
  back: string;
  example?: string;
  scenario?: string;
}

export const FLASHCARDS: Flashcard[] = [
  // ============== Fundamentals ==============
  {
    id: 'fc-1', category: 'fundamentals', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: كم عدد طبقات OSI Model؟',
    back: '7 طبقات: Physical (1) → Data Link (2) → Network (3) → Transport (4) → Session (5) → Presentation (6) → Application (7).',
    example: 'L4 = TCP/UDP, L3 = IP/Routers, L2 = MAC/Switches'
  },
  {
    id: 'fc-2', category: 'fundamentals', type: 'interview', difficulty: 'easy',
    front: 'سؤال انترفيو: اشرح OSI 7-Layer Model؟',
    back: 'OSI هو نموذج مرجعي: Physical (الكابلات، الـ bits)، Data Link (Ethernet، MAC)، Network (IP، Routing)، Transport (TCP/UDP، Ports)، Session (إنهاء الجلسات)، Presentation (Encryption، Compression)، Application (HTTP، FTP، SMTP).',
    scenario: 'لو سُئلت: "اشرح كيف تنتقل الحزمة من طبقة لأخرى" - اذكر Encapsulation: كل طبقة تضيف header.'
  },
  {
    id: 'fc-3', category: 'fundamentals', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: كم host يسمح به /27؟',
    back: '30 host. الحساب: 32 - 27 = 5 host bits. 2^5 = 32 - 2 = 30. الـ subnet mask = 255.255.255.224. الـ wildcard = 0.0.0.31.'
  },
  {
    id: 'fc-4', category: 'fundamentals', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما الـ subnet mask و wildcard لـ /26؟',
    back: 'Subnet mask = 255.255.255.192. Wildcard = 0.0.0.63. الحساب: 32 - 26 = 6 host bits. 2^6 = 64 block size. الـ mask = 256 - 64 = 192. الـ wildcard = 256 - 192 = 63.'
  },
  {
    id: 'fc-5', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: لو لديك 192.168.1.130/26، ما هي الشبكة؟',
    back: 'Network = 192.168.1.128. Broadcast = 192.168.1.191. First host = .129. Last host = .190. Block size = 64 (2^6). 130 ينحدر في نطاق 128-191.',
    scenario: 'هذا سؤال شائع جداً في المقابلات. تدرّب على حلّه في 30 ثانية.'
  },
  {
    id: 'fc-6', category: 'fundamentals', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحan: ما هي عناوين RFC 1918 الخاصة؟',
    back: '(1) 10.0.0.0/8 (Class A). (2) 172.16.0.0/12 (Class B، 172.16.0.0 - 172.31.255.255). (3) 192.168.0.0/16 (Class C). تستعمل NAT للوصول للإنترنت.'
  },
  {
    id: 'fc-7', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين TCP و UDP؟',
    back: 'TCP: موثوق، connection-oriented، 3-way handshake، يضمن الترتيب، flow control. يستعمل في HTTP/SSH/FTP. UDP: غير موثوق، connectionless، أسرع، أخف. يستعمل في DNS/DHCP/VoIP/Streaming.',
    scenario: 'السؤال يأتي متعدد الأوجه: "متى تختار TCP ومتى UDP؟" - TCP للبيانات الحرجة، UDP للوقت الحقيقي.'
  },
  {
    id: 'fc-8', category: 'fundamentals', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما الـ port لـ SSH و Telnet و HTTP و HTTPS؟',
    back: 'SSH = TCP 22. Telnet = TCP 23. HTTP = TCP 80. HTTPS = TCP 443. DNS = UDP 53. DHCP = UDP 67/68. BGP = TCP 179.'
  },
  {
    id: 'fc-9', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: اشرح TCP 3-way handshake؟',
    back: '(1) SYN: العميل يرسل SYN برقم تسلسلي (seq=2000) ليطلب اتصالاً. (2) SYN-ACK: الخادم يؤكد (ack=2001) ويرسل SYN الخاص به (seq=5000). (3) ACK: العميل يؤكد (ack=5001). بعدها الاتصال ESTABLISHED.',
    scenario: 'قد يسألك: "كم عدد الـ packets لإنشاء TCP connection؟" - الإجابة: 3.'
  },
  {
    id: 'fc-10', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين Hub و Switch و Router؟',
    back: 'Hub (L1): يكرر الإشارة لكل البورتات، broadcast domain واحد. Switch (L2): يقرأ MAC، يفصل collision domains (كل بورت = CD). Router (L3): يقرأ IP، يفصل broadcast domains.',
    scenario: 'لو سُئلت "ما الـ broadcast domain في hub؟" - الإجابة: 1 (hub بالكامل BD واحد).'
  },
  {
    id: 'fc-11', category: 'fundamentals', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما الفرق بين Unicast و Multicast و Broadcast؟',
    back: 'Unicast: 1-to-1 (HTTP). Multicast: 1-to-group (OSPF، streaming video). Broadcast: 1-to-all (ARP، DHCP). Anycast: 1-to-nearest (DNS root، IPv6).'
  },
  {
    id: 'fc-12', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما وظيفة ARP؟',
    back: 'ARP (Address Resolution Protocol) يحوّل IPv4 → MAC على نفس الشبكة الفرعية. يرسل ARP broadcast "من يملك IP X؟" فيجيب الجار بـ MAC الخاص به. النتيجة تُخزن في ARP cache.',
    scenario: 'سؤال شائع: "لو لديك PC IP 192.168.1.10 وتريد الوصول لـ 8.8.8.8، ما الذي يحدث أولاً؟" - ARP للـ gateway، وليس لـ 8.8.8.8.'
  },

  // ============== Routing ==============
  {
    id: 'fc-13', category: 'routing', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما ترتيب AD من الأعلى موثوقية؟',
    back: 'Direct(0) > Static exit-if(0) > Static next-hop(1) > eBGP(20) > EIGRP Internal(90) > IGRP(100) > OSPF(110) > IS-IS(115) > RIP(120) > EIGRP External(170) > iBGP(200) > Unknown(255).',
    example: 'القاعدة: الأقل AD يفوز'
  },
  {
    id: 'fc-14', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: لو تعلم الراوتر نفس الشبكة من OSPF و EIGRP، أيهما يستخدم؟',
    back: 'EIGRP لأن AD=90 أقل من OSPF AD=110. القاعدة: الأقل AD يفوز.',
    scenario: 'كيف تجعل الراوتر يفضل OSPF؟ غير AD: distance ospf 90 (مثل EIGRP) ثم Longest Prefix Match يحسم.'
  },
  {
    id: 'fc-15', category: 'routing', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما قاعدة Longest Prefix Match؟',
    back: 'عند وجود عدة مسارات لنفس الوجهة، يختار الراوتر المسار بأطول قناع شبكة (الأكثر تحديداً). /24 يفوز على /16 يفوز على /8 يفوز على /0 (default).'
  },
  {
    id: 'fc-16', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: اشرح حالات OSPF Neighbor State؟',
    back: 'Down → Init → Two-Way → ExStart → Exchange → Loading → Full. Full = الحالة المستقرة (LSAs متطابقة). Two-Way = تأكد ثنائي الاتجاه. ExStart/Exchange = تبادل DBD. Loading = طلب LSAs.',
    scenario: 'سؤال شائع: "كم state قبل Full؟" - 6 states.'
  },
  {
    id: 'fc-17', category: 'routing', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما OSPF wildcard لـ 255.255.255.0؟',
    back: '0.0.0.255. الـ wildcard = 255.255.255.255 - subnet mask. لـ /24 (255.255.255.0): 255.255.255.255 - 255.255.255.0 = 0.0.0.255.',
    example: 'OSPF يستعمل wildcard وليس subnet mask!'
  },
  {
    id: 'fc-18', category: 'routing', type: 'exam', difficulty: 'hard',
    front: 'سؤال امتحان: ما أنواع LSA في OSPF؟',
    back: 'Type 1 (Router LSA، داخل area). Type 2 (Network LSA، من DR). Type 3 (Summary LSA، بين areas من ABR). Type 4 (ASBR Summary). Type 5 (AS External، من ASBR). Type 7 (NSSA External).'
  },
  {
    id: 'fc-19', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: كيف يتم انتخاب DR في OSPF؟',
    back: '(1) أعلى priority يفوز (الافتراضي 1، 0 = لا DR أبداً). (2) عند التعادل، أعلى router-id. لجعل راوتر DR: ip ospf priority 100.',
    scenario: 'تحذير: الانتخاب لا يُعاد بدون reload OSPF أو clear ip ospf process.'
  },
  {
    id: 'fc-20', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين OSPF Stub و Totally Stubby و NSSA؟',
    back: 'Stub: لا Type 5 LSAs (لا مسارات خارجية). Totally Stubby: لا Type 3 ولا 5 (default route فقط). NSSA: مثل Stub لكن يسمح بـ ASBR محلي (Type 7).',
    scenario: 'استعمل Stub في leaf areas لتقليل LSAs.'
  },
  {
    id: 'fc-21', category: 'routing', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما الفرق بين EIGRP و OSPF؟',
    back: 'EIGRP: Hybrid، تقارب سريع (DUAL+FS)، Unequal Cost LB (variance). OSPF: Link-State،_areas، Cost=bw reference. EIGRP AD=90، OSPF AD=110. EIGRP أسرع، OSPF أكثر معيارية.'
  },
  {
    id: 'fc-22', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: اشرح EIGRP DUAL: FD, RD, FC, Successor, FS؟',
    back: 'FD (Feasible Distance): أقل تكلفة من الراوتر للوجهة. RD (Reported Distance): التكلفة من الجار. FC (Feasibility Condition): RD < FD. Successor: الجار الأساسي. FS (Feasible Successor): احتياطي يحقق FC.',
    scenario: 'سؤال متقدم: "متى يستعمل EIGRP الـ FS؟" - عند فشل Successor، فوراً بدون إعادة حساب.'
  },
  {
    id: 'fc-23', category: 'routing', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما EIGRP SIA ولماذا يحدث؟',
    back: 'SIA (Stuck in Active): الراوتر أرسل Query ولم يتلقّ Reply خلال active-time (3 دقائق). يُلغي الجوار. الأسباب: راوتر بطيء، شبكة غير مستقرة، query انتشر بعيداً.',
    example: 'الحل: summarization + stub routing'
  },
  {
    id: 'fc-24', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين eBGP و iBGP؟',
    back: 'eBGP: بين ASes مختلفة، AD=20، TTL=1، next-hop يتغير. iBGP: داخل AS، AD=200، TTL=255، next-hop لا يتغير (يحتاج next-hop-self). iBGP يحتاج full-mesh أو Route Reflector.',
    scenario: 'لو سُئلت: "لماذا iBGP لا يعلن مسارات iBGP أخرى؟" - منع loops.'
  },
  {
    id: 'fc-25', category: 'routing', type: 'exam', difficulty: 'hard',
    front: 'سؤال امتحan: اذكر BGP Path Selection attributes بالترتيب؟',
    back: '(1) Weight (الأعلى يفوز). (2) Local Preference (الأعلى). (3) Locally originated. (4) AS-Path (الأقصر). (5) Origin (IGP<EGP<?). (6) MED (الأدنى). (7) eBGP > iBGP. (8) Oldest. (9) Router-ID (الأقل).',
    example: 'Weight محلي للراوتر فقط'
  },

  // ============== Switching ==============
  {
    id: 'fc-26', category: 'switching', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما VLAN ولماذا نستخدمه؟',
    back: 'VLAN (Virtual LAN) تقسيم منطقي للشبكة. فوائده: فصل broadcast domains، تحسين الأمان، تقليل حركة البث، مرونة نقل المستخدمين. كل VLAN = subnet منفصل.'
  },
  {
    id: 'fc-27', category: 'switching', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما الفرق بين Access Port و Trunk Port؟',
    back: 'Access: 1 VLAN، بدون تاج 802.1Q، للمستخدمين. Trunk: عدة VLANs، مع تاج 802.1Q، بين سويتشات. Native VLAN على الـ trunk يرسل بدون تاج (افتراضي VLAN 1).'
  },
  {
    id: 'fc-28', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما VLAN Hopping Attack وكيف نمنعه؟',
    back: 'هجوم بالـ double-tagged 802.1Q للوصول لـ VLAN غير مصرح. الوقاية: (1) تغيير Native VLAN لـ VLAN غير مستخدم (999). (2) switchport nonegotiate. (3) switchport mode access صريح على بورتات المستخدمين.',
    scenario: 'سؤال أمني شائع في مقابلات Cisco Security.'
  },
  {
    id: 'fc-29', category: 'switching', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما STP ولماذا؟',
    back: 'STP (Spanning Tree، 802.1D) يمنع حلقات L2. ينتخب Root Bridge، يحظر المنافذ الزائدة. بدون STP: Broadcast Storm يوقف الشبكة في ثوانٍ.',
    example: 'PVST+ = شجرة لكل VLAN (Cisco)'
  },
  {
    id: 'fc-30', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: كيف يتم انتخاب Root Bridge في STP؟',
    back: 'الأصغر Bridge ID (Priority + MAC). الـ Priority الافتراضي 32768. لجعل سويتش Root: spanning-tree vlan <id> priority 4096 أو root primary.',
    scenario: 'تلميح: ضبط priority أقل من البقية يكفي.'
  },
  {
    id: 'fc-31', category: 'switching', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما PortFast ولماذا لا نضعه على Trunk؟',
    back: 'PortFast يتجاوز Listening/Learning ويدخل Forwarding فوراً. للمستخدمين فقط. على Trunk: قد يسبب حلقة فورية قبل اكتشاف STP. التفعيل: spanning-tree portfast على interface.'
  },
  {
    id: 'fc-32', category: 'switching', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما BPDU Guard؟',
    back: 'يحظر بورت access إن استلم BPDU (سويتش متصل غير مصرح). يضعه في errdisable. مع PortFast على access. التفعيل: spanning-tree portfast bpduguard default.'
  },
  {
    id: 'fc-33', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين RSTP و STP؟',
    back: 'RSTP (802.1w) أسرع بكثير (1-3 ثوانٍ vs 30-50 ثانية). أدوار: Root، Designated، Alternate، Backup، Edge. حالات: Discarding، Learning، Forwarding. RSTP يدعم rapid convergence عبر Alternate ports.',
    scenario: 'الفئة PVST+ = شجرة لكل VLAN. Rapid PVST+ = RSTP لكل VLAN.'
  },
  {
    id: 'fc-34', category: 'switching', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما EtherChannel وبروتوكولاته؟',
    back: 'EtherChannel: تجميع روابط في port-channel واحد. PAgP (Cisco: desirable/auto)، LACP (IEEE: active/passive)، On (يدوي). شرط: نفس speed/duplex/VLANs/STP.'
  },
  {
    id: 'fc-35', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما Port Security وأنماط الانتهاك؟',
    back: 'Port Security يقيّد MAC addresses على البورت. الانتهاكات: (1) protect: إسقاط بصمت. (2) restrict: إسقاط + تسجيل. (3) shutdown (افتراضي): errdisable. التفعيل: switchport port-security + maximum + mac-address sticky.'
  },
  {
    id: 'fc-36', category: 'switching', type: 'interview', difficulty: 'hard',
    front: 'سؤال انترفيو: اشرح DHCP Snooping و DAI و IP Source Guard؟',
    back: 'DHCP Snooping: trust خوادم DHCP، untrust بورتات المستخدمين، يبني binding table (MAC↔IP↔VLAN↔Port). DAI: يفحص ARP ضد binding table (يمنع ARP spoofing). IP Source Guard: يفحص source IP+MAC (يمنع IP spoofing).'
  },

  // ============== Security ==============
  {
    id: 'fc-37', category: 'security', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحan: ما الفرق بين Telnet و SSH؟',
    back: 'Telnet: plaintext (TCP 23)، خطير. SSH: مشفّر (TCP 22)، يستعمل RSA keys. استعمل SSH v2 دائماً. الإعداد: crypto key generate rsa + ip ssh version 2 + transport input ssh.'
  },
  {
    id: 'fc-38', category: 'security', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما أنواع كلمات المرور في IOS؟',
    back: 'Type 0 (plaintext)، Type 5 (MD5)، Type 7 (Vigenère، ضعيف)، Type 8 (PBKDF2-SHA256)، Type 9 (Scrypt، الأقوى). استعمل enable algorithm-type scrypt secret (Type 9).'
  },
  {
    id: 'fc-39', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: اشرح AAA؟',
    back: 'Authentication (من أنت؟ username/password). Authorization (ماذا يسمح لك؟ privileges). Accounting (ماذا فعلت؟ log). بروتوكولان: RADIUS (IETF، UDP، يشفّر password فقط) و TACACS+ (Cisco، TCP، يشفّر كل payload).',
    scenario: 'سؤال شائع: "متى تختار TACACS+؟" - لإدارة الأجهزة (device admin).'
  },
  {
    id: 'fc-40', category: 'security', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما الفرق بين Standard و Extended ACL؟',
    back: 'Standard (1-99، 1300-1999): يفحص المصدر فقط. ضعه قرب الوجهة. Extended (100-199، 2000-2699): يفحص src+dst+protocol+port. ضعه قرب المصدر. Named ACLs أوضح.'
  },
  {
    id: 'fc-41', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: أين تضع Standard ACL و Extended ACL؟',
    back: 'Standard ACL قرب الوجهة (يفحص المصدر فقط، فقد يرفض حركة مشروعة). Extended ACL قرب المصدر (يفحص كل التفاصيل، يوفر عرض النطاق). القاعدة الذهبية.',
    scenario: 'سؤال شائع جداً. اربطه بمبدأ "وفّر bandwidth" + "لا ترفض حركة مشروعة".'
  },
  {
    id: 'fc-42', category: 'security', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما 802.1x ومكوناته؟',
    back: '802.1x = مصادقة على بورت. ثلاثة عناصر: Supplicant (العميل)، Authenticator (السويتش)، Authentication Server (RADIUS). يستعمل EAP على L2. غالباً مع MAB للطابعات.'
  },
  {
    id: 'fc-43', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما هجوم MAC Flooding وكيف نمنعه؟',
    back: 'المهاجم يرسل آلاف الإطارات بـ MACs وهمية. السويتش يملأ جدول MAC ويفيض، فيتحول لـ Hub (يرسل كل الحركة لكل البورتات - sniffing). الوقاية: Port Security بـ maximum + violation.',
    scenario: 'سؤال أمني شائع. اربطه بـ CAM table overflow.'
  },

  // ============== Services ==============
  {
    id: 'fc-44', category: 'services', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما DHCP DORA؟',
    back: 'Discover (العميل broadcast يبحث عن خادم). Offer (الخادم يقترح IP). Request (العميل يقبل). ACK (الخادم يؤكد + الإعدادات). 4 رسائل للحصول على IP.'
  },
  {
    id: 'fc-45', category: 'services', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما DHCP Relay ولماذا؟',
    back: 'ip helper-address <dhcp-ip> على الواجهة. يحوّل بث DHCP (broadcast) إلى unicast موجه لخادم DHCP في شبكة أخرى. ضروري لأن بث DHCP لا يعبر الراوتر.'
  },
  {
    id: 'fc-46', category: 'services', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما أنواع NAT الثلاثة؟',
    back: '(1) Static NAT: 1-to-1 يدوي. (2) Dynamic NAT: pool. (3) PAT (NAT Overload): many-to-1 + ports. الـ PAT هو الأكثر شيوعاً في المنازل والشركات الصغيرة.'
  },
  {
    id: 'fc-47', category: 'services', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين Inside Local و Inside Global؟',
    back: 'Inside Local = IP داخلي (RFC 1918) قبل NAT (مثلاً 192.168.1.10). Inside Global = IP عام بعد NAT (مثلاً 203.0.113.2:51152). Outside = الوجهة على الإنترنت.',
    scenario: 'سؤال شائع في تشخيص NAT. تذكّر: Local = قبل، Global = بعد.'
  },
  {
    id: 'fc-48', category: 'services', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما NTP stratum؟',
    back: 'Stratum = مستوى القرب من مصدر الوقت. Stratum 0 = atomic clock مباشر. 1 = متصل مباشر. 2 = عميل لـ 1. كلما أصغر = أكثر موثوقية. الافتراضي للراوتر = 8.'
  },
  {
    id: 'fc-49', category: 'services', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما Syslog severity levels؟',
    back: '(0) Emergencies، (1) Alerts، (2) Critical، (3) Errors، (4) Warnings، (5) Notifications، (6) Informational، (7) Debugging. الـ trap الافتراضي = Informational (5).'
  },
  {
    id: 'fc-50', category: 'services', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما SNMPv3 ولماذا أفضل من v2c؟',
    back: 'SNMPv3: مصادقة (auth SHA/MD5) + تشفير (priv AES/DES) + access control. v2c: community string plaintext (sniffer يقرأها). استعمل v3 دائماً في الإنتاج.'
  },
  {
    id: 'fc-51', category: 'services', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما HSRP ولماذا نستخدمه؟',
    back: 'HSRP (Hot Standby Router Protocol): توفير Default Gateway متاح. راوتران يشاركان VIP + VMAC. Active يحمل الحركة، Standby احتياطي. Preempt لاستعادة Active. Cisco-Proprietary.',
    scenario: 'سؤال شائع: "ما الفرق بين HSRP و VRRP؟" - HSRP Cisco، VRRP IETF مفتوح، VRRP preempt مفعّل افتراضياً.'
  },
  {
    id: 'fc-52', category: 'services', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما HSRP Virtual MAC؟',
    back: 'v1: 0000.0c07.acXX (XX=group 0-255). v2: 0000.0c9f.fXXX (XXX=group 0-4095). VRRP: 0000.5e00.01XX. GLBP: 0007.b400.XXYY.'
  },

  // ============== Advanced ==============
  {
    id: 'fc-53', category: 'advanced', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما أنواع عناوين IPv6؟',
    back: 'Global Unicast (2000::/3). Link-Local (fe80::/10). ULA (fc00::/7). Multicast (ff00::/8). Loopback (::1). Unspecified (::).'
  },
  {
    id: 'fc-54', category: 'advanced', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما EUI-64؟',
    back: 'توليد host portion من MAC: (1) إدراج FFFE في وسط الـ MAC (24+FFFE+24). (2) قلب البت السابع (U/L bit). مثال: MAC 00:1A:2B:3C:4D:5E → 0200:1A:2B:FF:FE:3C:4D:5E.'
  },
  {
    id: 'fc-55', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما SLAAC vs DHCPv6؟',
    back: 'SLAAC (StateLess): المضيف يولّد IPv6 من RA prefix + EUI-64. لا خادم. Stateful DHCPv6: الخادم يعطي IP كامل. Stateless DHCPv6 (O flag): SLAAC لـ IP + DHCPv6 لـ DNS/NTP. يحدد RA flags M/O.',
    scenario: 'سؤال شائع: "ما الفرق بين M و O flags؟" - M=Managed (Stateful)، O=Other (DNS).'
  },
  {
    id: 'fc-56', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما NDP ولماذا بديل ARP؟',
    back: 'NDP (Neighbor Discovery Protocol) بديل ARP في IPv6. يستعمل ICMPv6 (133-137). RS/RA لـ router discovery، NS/NA لـ neighbor discovery، DAD لـ duplicate detection. لا يوجد broadcast في IPv6 (multicast فقط).'
  },
  {
    id: 'fc-57', category: 'advanced', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما DSCP EF؟',
    back: 'EF (Expedited Forwarding) = DSCP 46. للأولوية القصوى - VoIP. LLQ (Low Latency Queueing) يحجز priority queue. الـ CoS المقابل = 5. لا يتأخر.'
  },
  {
    id: 'fc-58', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما الفرق بين Policing و Shaping؟',
    back: 'Policing: يرمي الحزمة الفائضة (drop). يستعمل على حدود ISP (صارم). Shaping: يؤجل في طابور (smooth). يستعمل على حدود Customer→ISP. Shaping أنعم على TCP.',
    scenario: 'سؤال شائع: "متى تختار Shaping؟" - للـ TCP-based traffic الذي يتحسس فقد.'
  },
  {
    id: 'fc-59', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما IPsec ومكوناته؟',
    back: 'IPsec = تشفير IP. IKE (تفاوض SA)، AH (مصادقة فقط)، ESP (تشفير+مصادقة). أوضاع: Transport (payload فقط)، Tunnel (كل الحزمة). خوارزميات: AES-256 + SHA-256.',
    scenario: 'سؤال شائع: "ما الفرق بين Tunnel و Transport؟" - Tunnel يشفّر الـ IP header الأصلي.'
  },
  {
    id: 'fc-60', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما VRF ولماذا؟',
    back: 'VRF (Virtual Routing & Forwarding): جداول توجيه متعددة على راوتر واحد. عزل L3، يسمح بـ overlapping IPs. استعمال في MPLS VPN، Multi-tenancy.',
    scenario: 'سؤال متقدم: "ما الفرق بين VRF و VLAN؟" - VLAN = L2، VRF = L3.'
  },
  {
    id: 'fc-61', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما SDN ولماذا؟',
    back: 'SDN (Software-Defined Networking): فصل control plane (controller) عن data plane (switches). OpenFlow Southbound، REST Northbound. مركزية، برمجية، vendor-agnostic.',
    scenario: 'أمثلة: Cisco DNA Center، VMware NSX، Juniper Contrail.'
  },
  {
    id: 'fc-62', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما MPLS؟',
    back: 'MPLS (Multi-Protocol Label Switching): 4-byte label بين L2/L3. PE يضع (push) label، P يبدل (swap)، PE يزيل (pop). أسرع من IP lookup، يدعم Traffic Engineering + VPNs.',
    scenario: 'الـ label = 20-bit، TTL = 8-bit، 3-bit EXP (QoS)، 1-bit S (stack).'
  },

  // ============== Configuration & Troubleshooting ==============
  {
    id: 'fc-63', category: 'fundamentals', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما الأوضاع الأربعة في Cisco IOS؟',
    back: '(1) User EXEC (Router>). (2) Privileged EXEC (Router#). (3) Global Config (Router(config)#). (4) Sub-modes: Interface (config-if)#، Router (config-router)#، Line (config-line)#.'
  },
  {
    id: 'fc-64', category: 'fundamentals', type: 'exam', difficulty: 'easy',
    front: 'سؤال امتحان: ما اختصارات لوحة المفاتيح في IOS؟',
    back: 'Tab (إكمال)، Ctrl+A (بداية السطر)، Ctrl+E (نهاية)، Ctrl+P (السابق)، Ctrl+Z (خروج لـ Privileged)، Ctrl+Shift+6 (إيقاف ping)، ? (مساعدة).'
  },
  {
    id: 'fc-65', category: 'fundamentals', type: 'exam', difficulty: 'medium',
    front: 'سؤال امتحان: ما config-register 0x2102 vs 0x2142؟',
    back: '0x2102 (الافتراضي): يحمّل IOS من flash + startup-config. 0x2142: يحمّل IOS لكن يتجاهل startup-config (يستعمل في Password Recovery).'
  },
  {
    id: 'fc-66', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: كيف تستعيد كلمة مرور راوتر مفقودة؟',
    back: '(1) Ctrl+Break في الـ POST لـ ROMmon. (2) confreg 0x2142 (تجاهل startup). (3) reset. (4) enable (لا password). (5) copy start run. (6) غيّر passwords. (7) config-register 0x2102. (8) reload.',
    scenario: 'سؤال شائع في المقابلات. تدرّب على المحاكاة.'
  },
  {
    id: 'fc-67', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: OSPF لا يشكل جوار، ما الأسباب؟',
    back: '(1) hello/dead غير متطابق. (2) area ID مختلف. (3) مصادقة مختلفة. (4) ACL يحجب proto 89. (5) network type مختلف. (6) نفس router-id. (7) passive-interface. (8) MTU مختلف. (9) subnet mask مختلف.',
    scenario: 'تدرّب على show ip ospf neighbor + debug ip ospf hello.'
  },
  {
    id: 'fc-68', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: BGP جار في Idle، ما الأسباب؟',
    back: '(1) لا connectivity (ping لا يعمل). (2) ACL يحجب TCP 179. (3) NAT يحوّل TCP 179. (4) neighbor IP/AS خاطئ. (5) source-interface خاطئ (update-source). (6) password MD5 مختلف. (7) TTL غير كافٍ (ebgp-multihop).',
    scenario: 'تشخيص: telnet <ip> 179 من الجار.'
  },

  // ============== Real-World Scenarios ==============
  {
    id: 'fc-69', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: شبكتك فيها Broadcast Storm، ماذا تفعل؟',
    back: '(1) تحقق من CPU على السويتشات (show processes cpu). (2) حدد البورت بنسبة استخدام عالٍ. (3) STP configuration error - تحقق من Root Bridge. (4) storm-control broadcast level 1 كحل سريع. (5) ابحث عن حلقة فيزيائية. (6) فعل BPDU Guard + Loop Guard.',
    scenario: 'سيناريو حقيقي شائع في production.'
  },
  {
    id: 'fc-70', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: صمّم شبكة VLAN آمنة لـ 5 أقسام. كيف؟',
    back: '(1) VLAN لكل قسم (Sales=10، IT=20، HR=30، Finance=40، Mgmt=99). (2) Inter-VLAN routing عبر L3 switch + ACLs. (3) 802.1x للمصادقة. (4) Port Security على كل access. (5) DHCP Snooping + DAI + IPSG. (6) BPDU Guard. (7) Native VLAN 999. (8) VTP transparent. (9) NTP + Syslog.',
    scenario: 'سؤال تصميم شائع. اربطه بـ Defense-in-Depth.'
  },
  {
    id: 'fc-71', category: 'routing', type: 'interview', difficulty: 'hard',
    front: 'سؤال انترفيو: صمّم WAN بين HQ و 10 فروع مع redundancy.',
    back: '(1) Two ISPs في HQ (BGP multi-homing). (2) DMVPN لـ tunnel mesh بين الفروع و HQ. (3) IPsec encryption. (4) OSPF داخل الـ DMVPN. (5) IP SLA + Object Tracking لـ failover. (6) Floating static route كاحتياطي. (7) QoS لـ VoIP priority. (8) 4G backup للفروع المهمة. (9) NetFlow لـ monitoring.',
    scenario: 'سؤال تصميم enterprise. اسرد المميزات بترتيب logical.'
  },
  {
    id: 'fc-72', category: 'switching', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: اشرح Three-Tier Campus Design.',
    back: 'Core (L3، redundancy، لا policies). Distribution (L3، ACLs، summarization، HSRP). Access (L2، port security، PoE، PortFast). الـ Core يربط buildings، Distribution يفصل VLANs، Access يخدم المستخدمين.',
    scenario: 'الاتجاه الحديث: Spine-Leaf في Data Centers.'
  },
  {
    id: 'fc-73', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما Defense-in-Depth؟',
    back: 'نهج متعدد الطبقات للأمان: Physical (غرف مقفلة) → Perimeter (edge FW، BGP blackholing) → Network (ACLs، VLANs، 802.1x) → Host (host FW، EDR) → Application (WAF) → Data (encryption) → Identity (MFA) → Monitoring (SIEM) → Response (IR).',
    scenario: 'لا تعتمد على طبقة واحدة. لو فشلت، البقية تكمّل.'
  },
  {
    id: 'fc-74', category: 'services', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: VoIP لا يعمل، ماذا تفحص؟',
    back: '(1) QoS: priority queue (LLQ) لـ RTP، EF marking. (2) Jitter <30ms، Loss <1%. (3) DHCP option 150 (TFTP). (4) CDP/LLDP للـ phone. (5) Voice VLAN. (6) CODEC (G.711/G.729). (7) SIP signaling. (8) NAT (SIP ALG).',
    scenario: 'استعمل IP SLA UDP jitter للقياس.'
  },
  {
    id: 'fc-75', category: 'routing', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: كيف تحقق High Availability في الشبكة؟',
    back: '(1) Redundant devices (Active/Active أو Active/Standby). (2) HSRP/VRRP لـ gateway. (3) EtherChannel لـ bandwidth+redundancy. (4) Dual WAN. (5) IP SLA tracking. (6) RSTP لـ fast convergence. (7) BGP multi-homing. (8) VSS/vPC. (9) Cluster. (10) Backup power.',
    scenario: 'الهدف: 99.999% availability (5 nines = 5 min/year downtime).'
  },
  {
    id: 'fc-76', category: 'fundamentals', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: كيف تختار بين L2 و L3 switch؟',
    back: 'L2 switch: رخيص، يفصل collision domains، لا routing. لـ access layer. L3 switch: مكلف، يفصل broadcast domains، routing بين VLANs بدون راوتر. لـ distribution/core. L3 أفضل في الشبكات الكبيرة.',
    scenario: 'سؤال تصميم. ربطه بحجم الشبكة.'
  },
  {
    id: 'fc-77', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما SD-WAN؟',
    back: 'SD-WAN: فصل control plane (orchestrator) عن data plane. فوائد: multi-link LB، application-aware routing (VoIP→MPLS، bulk→Internet)، central management (vManage)، auto VPN (DMVPN)، analytics، cloud onramping.',
    scenario: 'أمثلة: Cisco Viptela، VMware VeloCloud، Fortinet.'
  },
  {
    id: 'fc-78', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما EVPN-VXLAN؟',
    back: 'EVPN (Ethernet VPN): BGP-based control plane لـ MAC+IP. VXLAN: data plane (L2 في UDP). فوائد على VLANs: 16M segments (vs 4K VLANs)، MAC mobility، active-active L3 gateways، لا STP، control plane learning.',
    scenario: 'سؤال Data Center شائع. تستعمله Cisco ACI.'
  },
  {
    id: 'fc-79', category: 'advanced', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما Anycast ومتى يستعمل؟',
    back: 'Anycast: عنوان مشترك بين أجهزة متعددة، الرسالة تصل لأقرب جهاز (حسب metric). استعمالات: DNS root servers (13 منطقياً، آلاف فعلياً)، 6to4، CDNs، DDoS mitigation (attacker يصيب أقرب anycast neighbor).',
    scenario: 'Anycast ≠ Multicast. Anycast = 1-to-nearest.'
  },
  {
    id: 'fc-80', category: 'security', type: 'interview', difficulty: 'medium',
    front: 'سؤال انترفيو: ما CoPP ولماذا؟',
    back: 'CoPP (Control Plane Policing): QoS policy لحماية CPU من DoS. rate-limit الحركة الواردة للـ CPU (routing protocols، management، unwanted). يمنع استنزاف CPU. control-plane + service-policy input.',
    scenario: 'سؤال أمني متقدم. اربطه بـ ICMP flood، TCP SYN flood.'
  },
];

export const FLASHCARD_CATEGORIES = {
  fundamentals: { label: 'الأساسيات', labelEn: 'Fundamentals', color: '#049fd9' },
  routing: { label: 'التوجيه', labelEn: 'Routing', color: '#002b5c' },
  switching: { label: 'السويتش', labelEn: 'Switching', color: '#00bceb' },
  security: { label: 'الأمان', labelEn: 'Security', color: '#e74c3c' },
  services: { label: 'الخدمات', labelEn: 'Services', color: '#27ae60' },
  advanced: { label: 'متقدم', labelEn: 'Advanced', color: '#8e44ad' },
};

export const FLASHCARD_TYPES = {
  exam: { label: 'امتحان', labelEn: 'Exam', color: '#dc2626', icon: 'FileText' },
  interview: { label: 'انترفيو', labelEn: 'Interview', color: '#7c3aed', icon: 'Users' },
  concept: { label: 'مفهوم', labelEn: 'Concept', color: '#0891b2', icon: 'Brain' },
};
