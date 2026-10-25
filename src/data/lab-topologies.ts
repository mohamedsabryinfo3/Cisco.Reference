// Cisco Lab Topologies - Real-world scenarios with step-by-step configurations
export interface LabStep {
  description: string;
  commands: string;
  explanation?: string;
}

export interface LabTopology {
  id: string;
  title: string;
  titleEn: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: string;
  objectives: string[];
  topology: string;
  steps: LabStep[];
  verification: string[];
  commonIssues: string[];
  tags: string[];
}

export const LAB_TOPOLOGIES: LabTopology[] = [
  {
    id: 'lab-1',
    title: 'إعداد راوتر أساسي + تأمين SSH',
    titleEn: 'Basic Router Setup + SSH Hardening',
    difficulty: 'beginner',
    duration: '30-45 دقيقة',
    objectives: [
      'إعداد hostname و banner',
      'تأمين enable secret بـ Type 9 (Scrypt)',
      'إنشاء حساب admin محلي',
      'تفعيل SSHv2 فقط (تعطيل Telnet)',
      'ضبط VTY لـ SSH فقط',
    ],
    topology: 'Router R1 — PC (Console + LAN)',
    steps: [
      {
        description: '1. ادخل للإعداد وغيّر اسم الجهاز',
        commands: `enable
configure terminal
hostname Cairo-R01`,
        explanation: 'اسم الجهاز يظهر في الـ prompt. يجب أن يبدأ بحرف.',
      },
      {
        description: '2. فعّل service password-encryption و timestamps',
        commands: `service password-encryption
service timestamps log datetime msec localtime show-timezone
no ip domain-lookup`,
        explanation: 'password-encryption يشفّر Type 7 (weak) لكنه حد أدنى. timestamps ضرورية لتفسير السجلات.',
      },
      {
        description: '3. اضبط banner MOTD (تحذير قانوني)',
        commands: `banner motd ^C
*******************************************
*  CAIRO EDGE ROUTER - AUTHORIZED ACCESS   *
*  All sessions are logged and monitored  *
*  Unauthorized access will be prosecuted  *
*******************************************
^C`,
        explanation: 'الـ banner يحمي قانونياً. استعمل رمز محدد غير شائع (مثل ^C).',
      },
      {
        description: '4. اضبط enable secret بـ Type 9 (الأقوى)',
        commands: `enable algorithm-type scrypt secret S3cr3t!En@ble2026`,
        explanation: 'Type 9 (Scrypt) هو الأقوى حالياً. تجنّب enable password (plaintext).',
      },
      {
        description: '5. أنشئ حساب admin',
        commands: `username admin privilege 15 algorithm-type scrypt secret S3cr3t!Adm1n2026
username operator privilege 5 algorithm-type sha256 secret Oper@tor2026`,
        explanation: 'privilege 15 = administrator كامل. privilege 5 = read-only limited.',
      },
      {
        description: '6. اضبط SSH (domain + RSA keys + version 2)',
        commands: `ip domain-name cairo-net.local
crypto key generate rsa modulus 2048
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3`,
        explanation: 'RSA 2048-بت هو الأدنى الموصى به. SSHv2 يرفض اتصالات v1.',
      },
      {
        description: '7. أمن console و VTY',
        commands: `line console 0
  login local
  logging synchronous
  exec-timeout 5 0
  exit
line vty 0 15
  login local
  transport input ssh
  transport output ssh
  logging synchronous
  exec-timeout 10 0
  exit`,
        explanation: 'transport input ssh يمنع Telnet. exec-timeout يمنع الجلسات المعلقة.',
      },
      {
        description: '8. أضف حماية ضد brute-force',
        commands: `login block-for 120 attempts 3 within 30
login quiet-mode access-class MGMT-NETWORK
login delay 2
login on-failure log
login on-success log
ip access-list standard MGMT-NETWORK
  permit 10.10.10.0 0.0.0.255
  exit`,
        explanation: 'بعد 3 محاولات فاشلة في 30 ثانية، يحظر 120 ثانية. الـ quiet-mode يسمح لشبكة الإدارة بالدخول دائماً.',
      },
      {
        description: '9. اضبط الواجهة واحفظ',
        commands: `interface gigabitEthernet 0/0
  ip address 192.168.1.1 255.255.255.0
  no shutdown
  exit
exit
copy running-config startup-config`,
        explanation: 'لا تنسَ no shutdown! الأكثر نسياناً. احفظ دائماً بعد كل تغيير ناجح.',
      },
    ],
    verification: [
      'show ip ssh — يجب أن يظهر SSH v2',
      'show ssh — يجب أن تظهر جلسة عند الاتصال',
      'ssh -l admin 192.168.1.1 من PC',
      'show running-config | include secret — تأكد Type 9',
      'show login failures — محاولات الفشل',
    ],
    commonIssues: [
      'نسيان no shutdown على الواجهة',
      'نسيان crypto key generate rsa — SSH لن يعمل',
      'transport input all بدلاً من ssh — Telnet سيُسمح',
      'exec-timeout 0 0 — جلسة لا تنتهي (خطر أمني)',
    ],
    tags: ['security', 'ssh', 'basic', 'password'],
  },
  {
    id: 'lab-2',
    title: 'VLANs + Trunking بين سويتشين',
    titleEn: 'VLANs and Trunking Between Switches',
    difficulty: 'beginner',
    duration: '30-45 دقيقة',
    objectives: [
      'إنشاء VLANs (10، 20، 99)',
      'ضبط Access Ports للمستخدمين',
      'ضبط Trunk بين سويتشين',
      'تغيير Native VLAN لـ 999 (أمني)',
      'تعطيل DTP',
    ],
    topology: 'SW1 ====Trunk==== SW2 | PC1 (VLAN 10) on SW1 | PC2 (VLAN 20) on SW2',
    steps: [
      {
        description: '1. على SW1: أنشئ VLANs وأعطها أسماء',
        commands: `vlan 10
  name SALES
  exit
vlan 20
  name IT
  exit
vlan 99
  name MGMT
  exit
vlan 999
  name NATIVE
  exit`,
      },
      {
        description: '2. اضبط بورت PC1 (Access، VLAN 10)',
        commands: `interface fastEthernet 0/5
  switchport mode access
  switchport access vlan 10
  spanning-tree portfast
  spanning-tree bpduguard enable
  exit`,
        explanation: 'PortFast + BPDU Guard على بورتات Access فقط (للمستخدمين).',
      },
      {
        description: '3. اضبط Trunk إلى SW2',
        commands: `interface gigabitEthernet 0/1
  switchport trunk encapsulation dot1q
  switchport mode trunk
  switchport trunk allowed vlan 10,20,99
  switchport trunk native vlan 999
  switchport nonegotiate
  exit`,
        explanation: 'Native VLAN = 999 (غير مستخدم) يحمي من VLAN Hopping. nonegotiate يوقف DTP.',
      },
      {
        description: '4. على SW2: كرر نفس الخطوات (VLANs + Trunk)',
        commands: `vlan 10
  name SALES
  exit
vlan 20
  name IT
  exit
vlan 99
  name MGMT
  exit
vlan 999
  name NATIVE
  exit

interface gigabitEthernet 0/1
  switchport trunk encapsulation dot1q
  switchport mode trunk
  switchport trunk allowed vlan 10,20,99
  switchport trunk native vlan 999
  switchport nonegotiate
  exit`,
      },
      {
        description: '5. على SW2: اضبط بورت PC2 (VLAN 20)',
        commands: `interface fastEthernet 0/5
  switchport mode access
  switchport access vlan 20
  spanning-tree portfast
  spanning-tree bpduguard enable
  exit`,
      },
      {
        description: '6. اضبط SVI للـ Management (VLAN 99)',
        commands: `interface vlan 99
  ip address 192.168.99.2 255.255.255.0
  no shutdown
  exit
ip default-gateway 192.168.99.1`,
        explanation: 'ip default-gateway ضروري للـ L2 switches (لا routing). على L3 switch: ip routing + default route.',
      },
    ],
    verification: [
      'show vlan brief — كل VLANs موجودة مع البورتات',
      'show interfaces trunk — يجب أن يظهر Trunk مع VLANs المسموحة',
      'show interfaces switchport — تأكد operational mode = trunk',
      'ping بين PC1 و PC2 — يجب أن يفشل (في VLANs مختلفة بدون routing)',
    ],
    commonIssues: [
      'Native VLAN مختلف على الطرفين — BPDU violation',
      'نسيان switchport trunk allowed vlan — سيُسمح لكل VLANs',
      'وضع Trunk قبل encapsulation على سويتش يدعم ISL',
      'نسيان switchport mode access على بورتات المستخدمين — قد يتفاوض trunking',
    ],
    tags: ['vlan', 'trunk', 'switching', 'security'],
  },
  {
    id: 'lab-3',
    title: 'OSPF Single-Area بين راوترين',
    titleEn: 'OSPF Single-Area Between Two Routers',
    difficulty: 'intermediate',
    duration: '45-60 دقيقة',
    objectives: [
      'تفعيل OSPF على R1 و R2',
      'ضبط router-id يدوياً (Loopback)',
      'ضبط passive-interface على LAN',
      'انتخاب R1 كـ DR',
      'التحقق من neighborship FULL',
    ],
    topology: 'R1 (LAN1: 192.168.1.0/24) ====WAN 10.0.0.0/30==== R2 (LAN2: 192.168.2.0/24)',
    steps: [
      {
        description: '1. على R1: اضبط Loopback والواجهات',
        commands: `interface loopback 0
  ip address 1.1.1.1 255.255.255.255
  exit
interface gigabitEthernet 0/0
  ip address 192.168.1.1 255.255.255.0
  no shutdown
  exit
interface serial 0/0/0
  ip address 10.0.0.1 255.255.255.252
  no shutdown
  exit`,
      },
      {
        description: '2. على R1: فعّل OSPF بـ router-id',
        commands: `router ospf 1
  router-id 1.1.1.1
  network 192.168.1.0 0.0.0.255 area 0
  network 10.0.0.0 0.0.0.3 area 0
  passive-interface gigabitEthernet 0/0
  auto-cost reference-bandwidth 1000
  exit`,
        explanation: 'router-id يدوي يمنع تغيره. auto-cost reference-bandwidth 1000 يضبط cost للـ gigabit. passive-interface على LAN يمنع Hellos.',
      },
      {
        description: '3. على R2: اضبط Loopback والواجهات',
        commands: `interface loopback 0
  ip address 2.2.2.2 255.255.255.255
  exit
interface gigabitEthernet 0/0
  ip address 192.168.2.1 255.255.255.0
  no shutdown
  exit
interface serial 0/0/0
  ip address 10.0.0.2 255.255.255.252
  no shutdown
  exit`,
      },
      {
        description: '4. على R2: فعّل OSPF',
        commands: `router ospf 1
  router-id 2.2.2.2
  network 192.168.2.0 0.0.0.255 area 0
  network 10.0.0.0 0.0.0.3 area 0
  passive-interface gigabitEthernet 0/0
  auto-cost reference-bandwidth 1000
  exit`,
      },
      {
        description: '5. على R1: اجعله DR (priority عالي)',
        commands: `interface serial 0/0/0
  ip ospf priority 100
  ip ospf cost 10
  ip ospf hello-interval 10
  ip ospf dead-interval 40
  exit`,
        explanation: 'priority 100 يجعل R1 يفوز بانتخاب DR. على Point-to-Point لا يوجد DR/BDR (يحدث فقط على Broadcast).',
      },
      {
        description: '6. أضف default route للـ Internet (إن وُجد)',
        commands: `ip route 0.0.0.0 0.0.0.0 203.0.113.1
router ospf 1
  default-information originate
  exit`,
        explanation: 'default-information originate تنشر default route في OSPF.',
      },
    ],
    verification: [
      'show ip ospf neighbor — يجب FULL',
      'show ip ospf interface — تأكد cost و hello/dead',
      'show ip route ospf — تأكد المسارات',
      'ping من PC1 (192.168.1.10) إلى PC2 (192.168.2.10)',
      'show ip protocols — تأكد router-id',
    ],
    commonIssues: [
      'network 192.168.1.0 255.255.255.0 area 0 — خطأ! OSPF يستعمل wildcard (0.0.0.255)',
      'hello/dead غير متطابقين بين الجارين — Init ولا يصل FULL',
      'نسيان router-id — قد يختار IP غير متوقع',
      'ACL يحجب proto 89 — لا neighborship',
    ],
    tags: ['ospf', 'routing', 'ipv4'],
  },
  {
    id: 'lab-4',
    title: 'NAT Overload (PAT) للوصول للإنترنت',
    titleEn: 'NAT Overload (PAT) for Internet Access',
    difficulty: 'intermediate',
    duration: '30-45 دقيقة',
    objectives: [
      'تعريف inside/outside interfaces',
      'إنشاء ACL للحركة الداخلية',
      'تفعيل PAT (NAT Overload)',
      'ضبط default route',
      'التحقق من ترجمات NAT',
    ],
    topology: 'LAN (192.168.1.0/24) — R1 — WAN (203.0.113.0/30) — ISP',
    steps: [
      {
        description: '1. اضبط الواجهات وعيّن inside/outside',
        commands: `interface gigabitEthernet 0/0
  ip address 192.168.1.1 255.255.255.0
  ip nat inside
  ip access-group OUTBOUND-PROTECT in
  no shutdown
  exit
interface gigabitEthernet 0/1
  ip address 203.0.113.2 255.255.255.252
  ip nat outside
  no shutdown
  exit`,
        explanation: 'inside = مواجه للـ LAN. outside = مواجه للإنترنت. ACL inbound لحماية LAN.',
      },
      {
        description: '2. أنشئ ACL للحركة الداخلية (للـ NAT)',
        commands: `ip access-list standard NAT-ALLOW
  permit 192.168.1.0 0.0.0.255
  exit`,
      },
      {
        description: '3. فعّل PAT (NAT Overload)',
        commands: `ip nat inside source list NAT-ALLOW interface gigabitEthernet 0/1 overload`,
        explanation: 'overload = PAT. يستعمل IP الواجهة الخارجية + بورتات متعددة. الأكثر شيوعاً.',
      },
      {
        description: '4. أضف default route',
        commands: `ip route 0.0.0.0 0.0.0.0 203.0.113.1`,
      },
      {
        description: '5. اضبط timeouts و max entries',
        commands: `ip nat translation timeout 3600
ip nat translation max-entries 5000`,
        explanation: 'timeout بالثواني. max-entries يمنع استنزاف الذاكرة.',
      },
      {
        description: '6. (اختياري) Port Forwarding لسيرفر ويب داخلي',
        commands: `ip nat inside source static tcp 192.168.1.10 80 203.0.113.2 8080 extendable`,
        explanation: 'extendable يسمح بـ port forwarding متعدد على نفس IP. السيرفر 192.168.1.10:80 يُنشر كـ 203.0.113.2:8080.',
      },
    ],
    verification: [
      'show ip nat translations — يجب أن تظهر entries',
      'show ip nat statistics — إحصائيات',
      'ping من PC إلى 8.8.8.8 — يجب النجاح',
      'clear ip nat translations * — مسح الـ dynamic entries',
      'debug ip nat (briefly) — تتبع الحزم',
    ],
    commonIssues: [
      'نسيان ip nat inside/outside على الواجهات',
      'ACL لا يطابق الشبكة الداخلية',
      'default route مفقود — NAT يعمل لكن لا routing خارجي',
      'overlap في port forwarding — استعمل extendable',
    ],
    tags: ['nat', 'pat', 'wan', 'internet'],
  },
  {
    id: 'lab-5',
    title: 'HSRP بين راوترين (Active/Standby)',
    titleEn: 'HSRP Active/Standby Redundancy',
    difficulty: 'intermediate',
    duration: '30-45 دقيقة',
    objectives: [
      'ضبط HSRP Virtual IP كـ Gateway للمضيفين',
      'ضبط Priority لانتخاب Active',
      'تفعيل Preempt لاستعادة Active',
      'ضبط Object Tracking لتتبع WAN',
      'اختبار الفشل و recovery',
    ],
    topology: 'R1 (192.168.1.2) + R2 (192.168.1.3) — LAN 192.168.1.0/24 — Virtual IP: 192.168.1.254',
    steps: [
      {
        description: '1. على R1 (سيلعب Active): اضبط الواجهة و HSRP',
        commands: `interface gigabitEthernet 0/0
  ip address 192.168.1.2 255.255.255.0
  standby 1 ip 192.168.1.254
  standby 1 priority 110
  standby 1 preempt
  standby 1 timers msec 200 msec 800
  standby 1 track 1 decrement 30
  exit`,
        explanation: 'priority 110 يفوز (افتراضي 100). preempt لاستعادة Active عند العودة. timers msec لـ HSRPv2 (أسرع).',
      },
      {
        description: '2. اضبط Object Tracking للـ WAN',
        commands: `track 1 interface serial 0/0/0 line-protocol
  exit`,
        explanation: 'لو فشل WAN، ينخفض priority بـ 30 (110-30=80) فيصبح R2 (100) Active.',
      },
      {
        description: '3. على R2 (سيلعب Standby): نفس الإعداد لكن priority 100 (افتراضي)',
        commands: `interface gigabitEthernet 0/0
  ip address 192.168.1.3 255.255.255.0
  standby 1 ip 192.168.1.254
  standby 1 priority 100
  standby 1 preempt
  standby 1 timers msec 200 msec 800
  exit`,
        explanation: 'preempt على الـ Standby مهم: لو فشل R1 ثم عاد، يجب أن يستعيد Active.',
      },
      {
        description: '4. فعّل HSRPv2 + authentication',
        commands: `interface gigabitEthernet 0/0
  standby version 2
  standby 1 authentication md5 key-string S3cr3t!HSRP
  exit`,
        explanation: 'HSRPv2 يدعم IPv6 + msec timers. MD5 authentication يمنع rogue HSRP.',
      },
      {
        description: '5. اضبط DHCP للـ LAN (Gateway = Virtual IP)',
        commands: `ip dhcp excluded-address 192.168.1.1 192.168.1.10
ip dhcp excluded-address 192.168.1.2 192.168.1.3
ip dhcp excluded-address 192.168.1.254
ip dhcp pool LAN-POOL
  network 192.168.1.0 255.255.255.0
  default-router 192.168.1.254
  dns-server 8.8.8.8 1.1.1.1
  lease 0 8
  exit`,
        explanation: 'default-router = Virtual IP. المضيفون يستعملون VIP كـ gateway. عند فشل R1، يستلم R2 VIP دون interruption.',
      },
    ],
    verification: [
      'show standby brief — Active على R1، Standby على R2',
      'show standby — تفاصيل كاملة (priority، preempt، timers)',
      'افصل R1 — خلال 800ms يصبح R2 Active',
      'أعد ربط R1 — خلال preempt يستعيد Active',
      'ping مستمر من PC إلى 8.8.8.8 — يجب أن لا ينقطع أكثر من ثانية',
    ],
    commonIssues: [
      'نسيان preempt — الـ Standby يبقى Active بعد عودة الـ Primary',
      'group number مختلف على الطرفين — لا يتشكلان',
      'Virtual IP مختلفة — لا يعملان معاً',
      'نسيان HSRP authentication — يعملان لكن بدون أمان',
    ],
    tags: ['hsrp', 'fhrp', 'redundancy', 'lan'],
  },
  {
    id: 'lab-6',
    title: 'ACL لحماية سيرفر + Filter Inbound',
    titleEn: 'ACL Server Protection + Inbound Filtering',
    difficulty: 'intermediate',
    duration: '30-45 دقيقة',
    objectives: [
      'إنشاء named Extended ACL',
      'السماح بـ HTTP/HTTPS/DNS فقط للسيرفر',
      'رفض باقي الحركة للسيرفر',
      'تطبيق ACL outbound على واجهة LAN',
      'استعمال sequence numbers للإضافة',
    ],
    topology: 'Internet — R1 — LAN (192.168.1.0/24) — Server (192.168.1.10)',
    steps: [
      {
        description: '1. أنشئ named Extended ACL',
        commands: `ip access-list extended PROTECT-SERVER
  remark "Allow HTTP/HTTPS to web server"
  10 permit tcp any host 192.168.1.10 eq 80
  20 permit tcp any host 192.168.1.10 eq 443
  30 permit udp any host 192.168.1.10 eq 53
  40 permit tcp any host 192.168.1.10 eq 53
  remark "Allow SSH only from management"
  50 permit tcp 10.10.10.0 0.0.0.255 host 192.168.1.10 eq 22
  remark "Allow ICMP echo for troubleshooting"
  60 permit icmp any host 192.168.1.10 echo
  remark "Deny everything else to server"
  100 deny ip any host 192.168.1.10 log
  remark "Allow all other LAN traffic"
  200 permit ip any any
  exit`,
        explanation: 'sequence numbers (10، 20، 100) تسمح بإضافة قواعد بينها (مثلاً 15). log في deny يسجّل المحاولات.',
      },
      {
        description: '2. طبّق ACL على واجهة LAN (outbound)',
        commands: `interface gigabitEthernet 0/0
  ip access-group PROTECT-SERVER out
  exit`,
        explanation: 'outbound = الحركة الخارجة من الراوتر للسيرفر (المستقبِل).',
      },
      {
        description: '3. أضف قاعدة لاحقاً (مثلاً SMTP للسيرفر)',
        commands: `ip access-list extended PROTECT-SERVER
  25 permit tcp any host 192.168.1.10 eq 25
  exit`,
        explanation: '25 ينحشر بين 20 و 30. الـ ACL تُعيد ترتيب نفسها.',
      },
      {
        description: '4. فعّل logging للـ ACL hits',
        commands: `ip access-list extended PROTECT-SERVER
  100 deny ip any host 192.168.1.10 log-input
  exit`,
        explanation: 'log-input يعطي معلومات أكثر: source interface + MAC. مفيد للـ forensics.',
      },
      {
        description: '5. اضبط ACL inbound للحماية من spoofing',
        commands: `ip access-list standard ANTI-SPOOF-IN
  permit 192.168.1.0 0.0.0.255
  deny any log
  exit
interface gigabitEthernet 0/0
  ip access-group ANTI-SPOOF-IN in
  exit`,
        explanation: 'في inbound على LAN: السماح فقط بـ IPs الشبكة الداخلية. يمنع spoofing.',
      },
    ],
    verification: [
      'show access-lists PROTECT-SERVER — تأكد من القواعد والعدادات',
      'show ip interface gigabitEthernet 0/0 — تأكد تطبيق ACL',
      'clear access-list counters — إعادة تصفير العدادات',
      'curl http://192.168.1.10 — يجب النجاح',
      'telnet 192.168.1.10 23 — يجب الفشل (لم يُسمح)',
    ],
    commonIssues: [
      'تطبيق ACL inbound بدلاً من outbound — قد يمنع الحركة',
      'نسيان permit ip any any في النهاية — كل الحركة تُرفض (denied by default)',
      'ترتيب القواعد خاطئ — الـ deny بعد permit لا يعمل',
      'log بدون log-input — لا source interface في السجل',
    ],
    tags: ['acl', 'security', 'firewall', 'filtering'],
  },
];

export const LAB_DIFFICULTY_CONFIG = {
  beginner: { label: 'مبتدئ', labelEn: 'Beginner', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' },
  intermediate: { label: 'متوسط', labelEn: 'Intermediate', color: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300' },
  advanced: { label: 'متقدم', labelEn: 'Advanced', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' },
};
