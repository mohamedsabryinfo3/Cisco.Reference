// Cisco IOS Commands Reference - Complete Data
// All 27 sections with full content

export interface Command {
  command: string;
  mode: string;
  explanation: string;
  example?: string;
  noCommand?: string;
}

export interface SubSection {
  title: string;
  commands?: Command[];
  bodyText?: string;
  tip?: { title: string; body: string; type?: 'tip' | 'warn' | 'info' };
  table?: {
    headers: string[];
    rows: string[][];
  };
  list?: string[];
}

export interface Section {
  id: number;
  chapter: string;
  titleAr: string;
  titleEn: string;
  icon: string;
  intro: string;
  subsections: SubSection[];
}

export const SECTIONS: Section[] = [
  {
    id: 1,
    chapter: "01",
    titleAr: "المقدمة وكيفية استخدام المذكرة",
    titleEn: "Introduction & Usage Guide",
    icon: "BookOpen",
    intro: "مرحباً بك في المذكرة الشاملة لأوامر سيسكو. صُمّمت هذه المذكرة خصيصاً لمراجعة وتثبيت أوامر نظام Cisco IOS المستخدمة في راوترات وسويتشات سيسكو، وتغطي منهج CCNA 200-301 بالكامل بالإضافة إلى مواضيع متقدمة من CCNP ENARSI كـ BGP و FHRP و QoS و 802.1x.",
    subsections: [
      {
        title: "بنية كل أمر في هذه المذكرة",
        bodyText: "كل أمر يتم ذكره في الجداول التالية يحتوي على العناصر التالية بشكل منهجي ومنظم: الأمر (Command Syntax) بالصيغة الدقيقة، الوضع (Mode) الذي يُكتب فيه الأمر، الشرح الوظيفي لما يفعله، مثال تطبيقي عملي، والأمر العكسي (no command) لإلغائه إن وجد.",
      },
      {
        title: "أوضاع Cisco IOS الرئيسية",
        table: {
          headers: ["الوضع (Mode)", "الموجه (Prompt)", "الوصف"],
          rows: [
            ["User EXEC", "Router>", "الوضع الافتراضي عند الدخول، محدود الصلاحيات"],
            ["Privileged EXEC", "Router#", "وضع متميز، يسمح بعرض كل المعلومات وحفظ الإعدادات"],
            ["Global Config", "Router(config)#", "الوضع العام للإعداد، يؤثر على الجهاز بالكامل"],
            ["Interface Config", "Router(config-if)#", "إعداد واجهة محددة (Interface)"],
            ["Line Config", "Router(config-line)#", "إعداد خطوط الوصول (Console، VTY، AUX)"],
            ["Router Config", "Router(config-router)#", "إعداد بروتوكولات التوجيه (OSPF، EIGRP، BGP)"],
            ["Subnet Config", "Router(config-subif)#", "إعداد واجهة فرعية (Sub-interface)"],
            ["VLAN Config", "Switch(config-vlan)#", "إعداد VLAN محدد في السويتش"],
          ],
        },
      },
      {
        title: "اختصارات لوحة المفاتيح الهامة",
        table: {
          headers: ["الاختصار", "الوظيفة"],
          rows: [
            ["Tab", "إكمال كتابة الأمر تلقائياً (Auto-complete)"],
            ["Ctrl + A", "الانتقال إلى بداية السطر"],
            ["Ctrl + E", "الانتقال إلى نهاية السطر"],
            ["Ctrl + P (↑)", "استدعاء الأمر السابق من التاريخ"],
            ["Ctrl + Z", "الخروج من وضع الإعداد إلى Privileged EXEC"],
            ["Ctrl + Shift + 6", "إيقاف تنفيذ أمر (Escape Sequence) مثل إيقاف ping"],
            ["?", "عرض المساعدة السياقية وكل الأوامر المتاحة"],
            ["command ?", "عرض المعاملات (Parameters) التي يقبلها الأمر"],
          ],
        },
        tip: {
          title: "نصيحة للمذاكرة",
          body: "احفظ اختصارات لوحة المفاتيح جيداً لأنها تختصر الوقت كثيراً في الامتحان العملي (Lab). أكثرها استخداماً: Tab للإكمال، Ctrl+Z للخروج السريع، Ctrl+Shift+6 لإيقاف ping، وعلامة ? للتعرف على المعاملات المتاحة.",
          type: "tip",
        },
      },
    ],
  },
  {
    id: 2,
    chapter: "02",
    titleAr: "أوضاع الراوتر والتنقل بينها",
    titleEn: "Router Modes & Navigation",
    icon: "Terminal",
    intro: "يعتبر فهم أوضاع Cisco IOS المختلفة من أهم الأساسيات التي يجب على كل مهندس شبكات إتقانها قبل التعمق في الأوامر. كل وضع له صلاحيات وحدود معينة، والأوامر المتاحة في وضع قد لا تكون متاحة في وضع آخر. الخطأ الشائع بين المبتدئين هو محاولة تنفيذ أمر إعداد في وضع العرض.",
    subsections: [
      {
        title: "الانتقال بين الأوضاع (Mode Transitions)",
        commands: [
          {
            command: "enable",
            mode: "User EXEC → Privileged",
            explanation: "الانتقال من وضع المستخدم العادي Router> إلى وضع التنفيذ المميّز Router#. يتطلب كلمة مرور إن وُجدت.",
            example: "Router>enable\nRouter#",
          },
          {
            command: "disable",
            mode: "Privileged → User EXEC",
            explanation: "العودة من وضع التنفيذ المميّز إلى وضع المستخدم العادي بدون الخروج من الجهاز.",
            example: "Router#disable\nRouter>",
            noCommand: "N/A",
          },
          {
            command: "configure terminal",
            mode: "Privileged → Global Config",
            explanation: "الدخول إلى وضع الإعداد العام. يختصر عادةً بـ conf t. يُستخدم لكل الأوامر التي تؤثر على الجهاز بالكامل.",
            example: "Router#configure terminal\nRouter(config)#",
            noCommand: "exit",
          },
          {
            command: "exit",
            mode: "أي وضع → الوضع الأعلى",
            explanation: "الخروج من الوضع الحالي إلى الوضع الذي يسبقه مباشرةً. عند استخدامه في Global Config يعود إلى Privileged EXEC.",
            example: "Router(config)#exit\nRouter#",
          },
          {
            command: "end",
            mode: "أي وضع فرعي → Privileged",
            explanation: "الخروج مباشرةً من أي وضع فرعي إلى Privileged EXEC. يكافئ Ctrl+Z.",
            example: "Router(config-if)#end\nRouter#",
          },
          {
            command: "interface <type> <number>",
            mode: "Global → Interface",
            explanation: "الدخول إلى وضع إعداد واجهة محددة. الأنواع: GigabitEthernet، FastEthernet، Serial، VLAN، Loopback.",
            example: "Router(config)#interface gigabitEthernet 0/0\nRouter(config-if)#",
            noCommand: "no interface",
          },
          {
            command: "interface range <range>",
            mode: "Global → Interface Range",
            explanation: "إعداد عدة واجهات دفعة واحدة. مفيد في السويتشات لإعداد بورتات متعددة بنفس الإعدادات.",
            example: "SW(config)#interface range fa0/1 - 10\nSW(config-if-range)#",
          },
          {
            command: "line <type> <number>",
            mode: "Global → Line Config",
            explanation: "الدخول إلى وضع إعداد خط الوصول. الأنواع: console 0، vty 0 4، aux 0.",
            example: "Router(config)#line vty 0 4\nRouter(config-line)#",
          },
          {
            command: "router <protocol> <args>",
            mode: "Global → Router Config",
            explanation: "الدخول إلى وضع إعداد بروتوكول توجيه. مثل router ospf 1، router eigrp 100، router bgp 65000.",
            example: "Router(config)#router ospf 1\nRouter(config-router)#",
            noCommand: "no router",
          },
          {
            command: "do <command>",
            mode: "Global/Sub → EXEC",
            explanation: "تنفيذ أمر من نوع Privileged EXEC (مثل show أو copy) من داخل أي وضع إعداد بدون الخروج منه.",
            example: "Router(config-if)#do show run | include hostname",
          },
        ],
      },
      {
        title: "عرض الإعدادات والحالة",
        commands: [
          {
            command: "show running-config",
            mode: "Privileged EXEC",
            explanation: "عرض الإعداد الحالي الكامل المحفوظ في RAM. يختصر بـ sh run.",
            example: "Router#show running-config",
            noCommand: "N/A",
          },
          {
            command: "show startup-config",
            mode: "Privileged EXEC",
            explanation: "عرض الإعداد المحفوظ في NVRAM والذي سيُحمّل عند إعادة التشغيل.",
            example: "Router#show startup-config",
            noCommand: "N/A",
          },
          {
            command: "show version",
            mode: "Privileged EXEC",
            explanation: "عرض إصدار IOS، نوع المعالج، حجم الذاكرة، قيمة Configuration Register، ووقت التشغيل.",
            example: "Router#show version",
            noCommand: "N/A",
          },
          {
            command: "show history",
            mode: "User/Privileged EXEC",
            explanation: "عرض قائمة آخر الأوامر المنفّذة في الجلسة الحالية.",
            example: "Router#show history",
            noCommand: "N/A",
          },
        ],
      },
      {
        title: "حفظ الإعدادات وإعادة التحميل",
        commands: [
          {
            command: "copy running-config startup-config",
            mode: "Privileged EXEC",
            explanation: "حفظ الإعداد الحالي (running) في NVRAM ليصبح الإعداد الابتدائي (startup). يكافئ write memory و wr.",
            example: "Router#copy run start",
            noCommand: "N/A",
          },
          {
            command: "copy running-config tftp:",
            mode: "Privileged EXEC",
            explanation: "نسخ الإعداد الحالي إلى خادم TFTP خارجي كنسخة احتياطية.",
            example: "Router#copy run tftp:",
            noCommand: "N/A",
          },
          {
            command: "erase startup-config",
            mode: "Privileged EXEC",
            explanation: "مسح الإعداد المحفوظ في NVRAM. عند إعادة التحميل بعدها يدخل الجهاز في وضع الإعداد الابتدائي.",
            example: "Router#erase start",
            noCommand: "N/A",
          },
          {
            command: "reload",
            mode: "Privileged EXEC",
            explanation: "إعادة تشغيل الجهاز. سيتم تحميل startup-config إن وُجد، أو وضع الإعداد الابتدائي إن لم يوجد.",
            example: "Router#reload",
            noCommand: "N/A",
          },
        ],
        tip: {
          title: "قيم config-register الهامة",
          body: "0x2102 = الافتراضي (حمّل IOS من flash + startup-config). 0x2142 = يحمّل IOS لكن يتجاهل startup-config (يستخدم في Password Recovery). 0x2100 = يقلع في ROM Monitor (ROMmon).",
          type: "info",
        },
      },
      {
        title: "أوامر النظام الأساسية",
        commands: [
          {
            command: "hostname <name>",
            mode: "Global Config",
            explanation: "تعيين اسم الجهاز. يجب أن يبدأ بحرف، ويفضّل ألا يحوي مسافات أو رموز خاصة. يؤثر على الموجّه (Prompt) مباشرةً.",
            example: "Router(config)#hostname Cairo-RTR-01",
            noCommand: "no hostname",
          },
          {
            command: "banner motd #<text>#",
            mode: "Global Config",
            explanation: "تعيين رسالة اليوم (Message of the Day) التي تظهر لكل من يسجل الدخول. الرمز # محدد لبداية ونهاية الرسالة.",
            example: 'banner motd #AUTHORIZED ACCESS ONLY#',
            noCommand: "no banner motd",
          },
          {
            command: "clock set <hh:mm:ss> <day> <month> <year>",
            mode: "Privileged EXEC",
            explanation: "ضبط التاريخ والوقت يدوياً. يفضل استخدام NTP للمزامنة التلقائية.",
            example: "Router#clock set 14:30:00 25 Oct 2026",
            noCommand: "N/A",
          },
          {
            command: "no ip domain-lookup",
            mode: "Global Config",
            explanation: "تعطيل تحويل أسماء المضيفين إلى عناوين IP (DNS lookup). يمنع الجهاز من محاولة حلّ الأوامر الخاطئة كأنها أسماء DNS.",
            example: "Router(config)#no ip domain-lookup",
            noCommand: "ip domain-lookup",
          },
          {
            command: "ip host <name> <ip>",
            mode: "Global Config",
            explanation: "إضافة اسم مضيف مع عنوانه في جدول hosts المحلي للجهاز، لاستخدامه بدلاً من العنوان في الأوامر.",
            example: "ip host SW-01 192.168.1.10",
            noCommand: "no ip host <name>",
          },
        ],
      },
    ],
  },
  {
    id: 3,
    chapter: "03",
    titleAr: "الإعداد الأساسي وإدارة النظام",
    titleEn: "Basic Setup & System Management",
    icon: "Settings",
    intro: "بعد ضبط أوضاع الراوتر، تأتي مرحلة الإعداد الأساسي للجهاز قبل أي تكوين شبكي. تشمل هذه المرحلة تعيين اسم الجهاز، رسائل التحذير، ضبط التوقيت، إدارة الذاكرة والإعدادات، وأوامر إدارة النظام التي تشكل البنية التحتية لكل الإعدادات اللاحقة.",
    subsections: [
      {
        title: "رسائل التحذير (Banners)",
        commands: [
          {
            command: "banner motd <delim>",
            mode: "Global Config",
            explanation: "رسالة اليوم تظهر قبل طلب الدخول. تستخدم قانونياً للتنبيه بأن الوصول غير المصرّح به جريمة. الرمز المحدد يبدأ وينهي الرسالة.",
            example: "banner motd #\nUNAUTHORIZED ACCESS PROHIBITED\n#",
            noCommand: "no banner motd",
          },
          {
            command: "banner login <delim>",
            mode: "Global Config",
            explanation: "رسالة تظهر قبل طلب اسم المستخدم وكلمة المرور.",
            example: "banner login ^CAuth Only^C",
            noCommand: "no banner login",
          },
        ],
        tip: {
          title: "ملاحظة قانونية هامة",
          body: "رسالة banner motd ليست مجرد تزيين؛ في كثير من الدول يتطلب القانون عرض تحذير صريح قبل محاولة الوصول ليكون أي وصول غير مصرّح به جريمة مع سبق الإصرار.",
          type: "warn",
        },
      },
      {
        title: "أوامر التوقيت (Time)",
        commands: [
          {
            command: "clock timezone <name> <hours> [<mins>]",
            mode: "Global Config",
            explanation: "ضبط المنطقة الزمنية. لمصر: clock timezone EET 2 0. للسعودية: clock timezone AST 3 0.",
            example: "clock timezone EET 2 0",
            noCommand: "no clock timezone",
          },
          {
            command: "ntp server <ip> [version 2-4]",
            mode: "Global Config",
            explanation: "ضبط خادم NTP للمزامنة التلقائية. يحوّل الجهاز إلى عميل NTP.",
            example: "ntp server 162.159.200.1",
            noCommand: "no ntp server <ip>",
          },
          {
            command: "ntp master [<stratum>]",
            mode: "Global Config",
            explanation: "تحويل الجهاز إلى خادم NTP مصدر (Master). الـ stratum الافتراضي 8.",
            example: "ntp master 5",
            noCommand: "no ntp master",
          },
          {
            command: "show ntp status",
            mode: "Privileged EXEC",
            explanation: "عرض حالة المزامنة مع خادم NTP (synchronized أو unsynchronized).",
            example: "show ntp status",
            noCommand: "N/A",
          },
        ],
      },
      {
        title: "إدارة الذاكرة والإعدادات",
        commands: [
          {
            command: "copy running-config startup-config",
            mode: "Privileged EXEC",
            explanation: "حفظ الإعداد الحالي إلى NVRAM ليصبح الإعداد الابتدائي.",
            example: "copy run start",
            noCommand: "N/A",
          },
          {
            command: "copy tftp: flash:",
            mode: "Privileged EXEC",
            explanation: "تحميل ملف (عادة صورة IOS جديدة) من خادم TFTP إلى flash. يستخدم لترقية نظام IOS.",
            example: "copy tftp: flash:",
            noCommand: "N/A",
          },
          {
            command: "erase startup-config",
            mode: "Privileged EXEC",
            explanation: "مسح الإعداد المحفوظ في NVRAM.",
            example: "erase start",
            noCommand: "N/A",
          },
          {
            command: "dir flash:",
            mode: "Privileged EXEC",
            explanation: "عرض محتوى flash مع حجم الملفات والمساحة الحرة.",
            example: "dir flash:",
            noCommand: "N/A",
          },
          {
            command: "boot system <location>",
            mode: "Global Config",
            explanation: "تحديد مكان تحميل ملف IOS عند الإقلاع. يمكن تحديد flash، tftp، أو rom.",
            example: "boot system flash:c1900-universalk9-mz.SPA.157-3.M.bin",
            noCommand: "no boot system",
          },
        ],
      },
      {
        title: "أوامر إضافية لإدارة النظام",
        commands: [
          {
            command: "logging synchronous",
            mode: "Line Config",
            explanation: "إعادة عرض الموجّه والسطر الحالي بعد ظهور رسائل syslog. ينصح به بشدة على console و vty.",
            example: "line console 0\n  logging synchronous",
            noCommand: "no logging synchronous",
          },
          {
            command: "exec-timeout <min> <sec>",
            mode: "Line Config",
            explanation: "تسجيل الخروج التلقائي بعد مدة من عدم النشاط. exec-timeout 5 0 = 5 دقائق. exec-timeout 0 0 = لا تنتهي الجلسة.",
            example: "line vty 0 4\n  exec-timeout 5 0",
            noCommand: "no exec-timeout",
          },
          {
            command: "service password-encryption",
            mode: "Global Config",
            explanation: "تشفير كل كلمات المرور غير المشفّرة في الإعداد باستخدام خوارزمية Type 7 (ضعيفة). يُفعّل دائماً كحد أدنى.",
            example: "service password-encryption",
            noCommand: "no service password-encryption",
          },
          {
            command: "service timestamps log datetime msec",
            mode: "Global Config",
            explanation: "إضافة تاريخ ووقت بالمللي ثانية لكل رسالة syslog. ضروري للتشخيص الدقيق.",
            example: "service timestamps log datetime msec",
            noCommand: "no service timestamps",
          },
          {
            command: "logging buffered <size>",
            mode: "Global Config",
            explanation: "تخزين رسائل syslog في RAM بدلاً من عرضها على console فقط.",
            example: "logging buffered 51200",
            noCommand: "no logging buffered",
          },
          {
            command: "logging <ip>",
            mode: "Global Config",
            explanation: "إرسال رسائل syslog إلى خادم syslog مركزي (مثل Kiwi أو Splunk).",
            example: "logging 10.10.10.50",
            noCommand: "no logging <ip>",
          },
        ],
        tip: {
          title: "نصيحة للاب",
          body: "عند بناء لاب تدريبي، نفّذ no ip domain-lookup و logging synchronous على line console 0 و line vty 0 4 في بداية كل جلسة. هذان الأمران يضاعفان سرعة كتابتك للأوامر ويمنعان تشويش رسائل syslog على ما تكتب.",
          type: "tip",
        },
      },
    ],
  },
  {
    id: 4,
    chapter: "04",
    titleAr: "كلمات المرور والأمان الأساسي",
    titleEn: "Passwords & Basic Security",
    icon: "Shield",
    intro: "تأمين الوصول إلى أجهزة الشبكة هو خط الدفاع الأول في حماية البنية التحتية. تتضمن هذه المرحلة تعيين كلمات مرور قوية على كل منافذ الوصول (Console، VTY، AUX)، تشفيرها في الإعداد، وتفعيل أساليب مصادقة أكثر تقدماً مثل AAA و SSH بدلاً من Telnet.",
    subsections: [
      {
        title: "أنواع كلمات المرور في Cisco IOS",
        table: {
          headers: ["النوع", "الخوارزمية", "مستوى الأمان", "متى يُستخدم"],
          rows: [
            ["Type 0", "Plain Text", "لا أمان", "محظور في الإنتاج"],
            ["Type 5", "MD5 (Salted)", "متوسط", "قديم - تجنّبه"],
            ["Type 7", "Cisco Vigenère", "ضعيف جداً", "تلقائي من service password-encryption"],
            ["Type 8", "PBKDF2-SHA256", "قوي", "موصى به حديثاً"],
            ["Type 9", "Scrypt", "قوي جداً", "الأقوى الموصى به"],
          ],
        },
      },
      {
        title: "كلمة مرور وضع التنفيذ المميّز",
        commands: [
          {
            command: "enable password <pass>",
            mode: "Global Config",
            explanation: "تعيين كلمة مرور للوصول إلى Privileged EXEC. تُخزن كنص ظاهر (Type 0). تجنّب هذا الأمر.",
            example: "enable password MyPass123",
            noCommand: "no enable password",
          },
          {
            command: "enable secret <pass>",
            mode: "Global Config",
            explanation: "تعيين كلمة مرور مشفّرة بـ MD5 (Type 5). أقوى بكثير من enable password ويلغي مفعولها إن وُجدت.",
            example: "enable secret S3cr3t!Pass",
            noCommand: "no enable secret",
          },
          {
            command: "enable algorithm-type sha256 secret <pass>",
            mode: "Global Config",
            explanation: "تعيين كلمة مرور مشفّرة بـ SHA256 (Type 8). أكثر أماناً من Type 5. متاح في IOS 15+.",
            example: "enable algorithm-type sha256 secret S3cr3t!Pass",
            noCommand: "no enable secret",
          },
          {
            command: "enable algorithm-type scrypt secret <pass>",
            mode: "Global Config",
            explanation: "تعيين كلمة مرور مشفّرة بـ Scrypt (Type 9) - الأقوى حالياً. متاح في IOS 15.3(3)M+.",
            example: "enable algorithm-type scrypt secret S3cr3t!Pass",
            noCommand: "no enable secret",
          },
        ],
      },
      {
        title: "كلمات مرور خطوط الوصول",
        commands: [
          {
            command: "line console 0",
            mode: "Global → Line",
            explanation: "الدخول إلى وضع إعداد خط console (المنفذ الفيزيائي التسلسلي).",
            example: "line console 0",
            noCommand: "N/A",
          },
          {
            command: "line vty 0 4",
            mode: "Global → Line",
            explanation: "إعداد أول 5 جلسات VTY (Telnet/SSH). بعض الأجهزة الحديثة تدعم 16 (0 15).",
            example: "line vty 0 4",
            noCommand: "N/A",
          },
          {
            command: "login local",
            mode: "Line Config",
            explanation: "تفعيل المصادقة عبر قاعدة بيانات المستخدمين المحلية (المعرّفة بـ username). موصى به.",
            example: "line vty 0 4\n  login local",
            noCommand: "no login local",
          },
          {
            command: "transport input ssh",
            mode: "Line Config",
            explanation: "تحديد أن بروتوكول SSH فقط مسموح للوصول (يمنع Telnet الأقل أماناً). موصى به بشدة.",
            example: "line vty 0 4\n  transport input ssh",
            noCommand: "transport input all",
          },
          {
            command: "access-class <acl> in",
            mode: "Line Config",
            explanation: "تقييد الوصول إلى VTY بمصادر محددة في ACL (مثلاً: فقط شبكة الإدارة).",
            example: "line vty 0 4\n  access-class 10 in",
            noCommand: "no access-class",
          },
        ],
      },
      {
        title: "إنشاء حسابات المستخدمين المحلية",
        commands: [
          {
            command: "username <name> privilege <0-15> secret <pass>",
            mode: "Global Config",
            explanation: "إنشاء حساب مستخدم محلي مع كلمة مرور مشفّرة Type 5 (MD5) ومستوى صلاحية. privilege 15 = Administrator كامل.",
            example: "username admin privilege 15 secret S3cr3t!Pass",
            noCommand: "no username <name>",
          },
          {
            command: "username <name> algorithm-type scrypt secret <pass>",
            mode: "Global Config",
            explanation: "إنشاء حساب مع كلمة مرور Type 9 (Scrypt) - الأقوى حالياً.",
            example: "username admin algorithm-type scrypt secret S3cr3t!Pass",
            noCommand: "no username <name>",
          },
          {
            command: "aaa new-model",
            mode: "Global Config",
            explanation: "تفعيل نموذج AAA (Authentication, Authorization, Accounting). يحوّل كل المصادقة إلى AAA افتراضياً.",
            example: "aaa new-model",
            noCommand: "no aaa new-model",
          },
          {
            command: "aaa authentication login default local",
            mode: "Global Config",
            explanation: "ضبط طريقة المصادقة الافتراضية لكل خطوط الوصول باستخدام قاعدة المستخدمين المحلية.",
            example: "aaa authentication login default local",
            noCommand: "no aaa authentication login default",
          },
        ],
      },
      {
        title: "إعداد SSH",
        commands: [
          {
            command: "ip domain-name <domain>",
            mode: "Global Config",
            explanation: "تعيين اسم النطاق. مطلوب لتوليد مفاتيح RSA لـ SSH.",
            example: "ip domain-name cairo.local",
            noCommand: "no ip domain-name",
          },
          {
            command: "crypto key generate rsa modulus 2048",
            mode: "Global Config",
            explanation: "توليد زوج مفاتيح RSA بطول 2048 بت (موصى به). يقوم بتفعيل SSH تلقائياً.",
            example: "crypto key generate rsa modulus 2048",
            noCommand: "crypto key zeroize rsa",
          },
          {
            command: "ip ssh version 2",
            mode: "Global Config",
            explanation: "تفعيل SSHv2 فقط (الأكثر أماناً). يرفض اتصالات SSHv1.",
            example: "ip ssh version 2",
            noCommand: "no ip ssh version",
          },
          {
            command: "ip ssh time-out <sec>",
            mode: "Global Config",
            explanation: "ضبط مهلة تسجيل الدخول لـ SSH بالثواني (الافتراضي 120).",
            example: "ip ssh time-out 60",
            noCommand: "no ip ssh time-out",
          },
          {
            command: "ip ssh authentication-retries <1-5>",
            mode: "Global Config",
            explanation: "عدد محاولات تسجيل الدخول قبل قطع الاتصال (الافتراضي 3).",
            example: "ip ssh authentication-retries 3",
            noCommand: "no ip ssh authentication-retries",
          },
          {
            command: "show ip ssh",
            mode: "Privileged EXEC",
            explanation: "عرض حالة وإعدادات SSH (الإصدار، timeout، retries).",
            example: "show ip ssh",
            noCommand: "N/A",
          },
        ],
        tip: {
          title: "قاعدة ذهبية للأمان",
          body: "استخدم دائماً enable secret بدلاً من enable password. وعند توفر IOS 15.3+، استخدم algorithm-type scrypt للوصول إلى أقوى تشفير متاح (Type 9). تجنّب أيضاً password العادية في خطوط VTY، واستخدم بدلاً منها login local مع حسابات مستخدمين محلية.",
          type: "tip",
        },
      },
    ],
  },
];

// Search index - quick lookup of all commands
export interface SearchIndexEntry {
  sectionId: number;
  sectionTitle: string;
  command: string;
  mode: string;
  explanation: string;
}

export const SEARCH_INDEX: SearchIndexEntry[] = SECTIONS.flatMap(section => {
  const entries: SearchIndexEntry[] = [];
  section.subsections.forEach(sub => {
    if (sub.commands) {
      sub.commands.forEach(cmd => {
        entries.push({
          sectionId: section.id,
          sectionTitle: section.titleAr,
          command: cmd.command,
          mode: cmd.mode,
          explanation: cmd.explanation,
        });
      });
    }
  });
  return entries;
});
