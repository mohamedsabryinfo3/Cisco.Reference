# 📚 مذكرة سيسكو الشاملة - Cisco IOS Commands Reference

<div dir="rtl">

مرجع تفاعلي شامل لأوامر Cisco IOS مع بحث فوري، حاسبة subnetting احترافية، بنك أسئلة كامل لـ CCNA/CCNP وأسئلة المقابلات، وبطاقات تعليمية تفاعلية. مكتوب بـ Next.js 16 + TypeScript + Tailwind CSS.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-4-38bdf8.svg)

## ✨ المميزات الرئيسية

### 📚 تبويب الأوامر (Commands)
- **27 قسماً** يغطي منهج CCNA 200-301 بالكامل + مواضيع متقدمة من CCNP ENARSI
- **362 أمر Cisco** قابل للنسخ بنقرة واحدة
- **97 جدول مرجعي** (Subnetting، AD، LSAs، إلخ)
- بحث فوري في كل الأوامر
- شريط جانبي (sidebar) مع scroll spy
- Scroll spy يبرز القسم الحالي تلقائياً

### ❓ تبويب بنك الأسئلة (Question Bank)
- **162 سؤال شامل**:
  - **68 سؤال CCNA** (OSI, TCP/UDP, VLANs, STP, OSPF, EIGRP, DHCP, NAT, ACLs, IPv6, Subnetting, Security, Automation)
  - **40 سؤال CCNP** (BGP, OSPF Advanced, EIGRP Advanced, FHRP, Layer 2, QoS, IPsec/VPN, SDN)
  - **54 سؤال مقابلات** (Basic Networking, Subnetting, Routing, Switching, Security, Troubleshooting, Real-World)
- بحث وفلترة حسب الفئة والموضوع والمستوى
- تتبع التقدم مع نسبة مئوية
- نظام مفضلة + علّم كمفهوم
- حفظ تلقائي في localStorage
- شرح عربي + English explanation

### 🧮 تبويب حاسبة Subnet (SubnetPro)
حاسبة subnetting احترافية شاملة بـ 5 تبويبات فرعية:

#### 1. محلل IP (IP Analyzer)
- إدخال صيغ متعددة: `192.168.1.130/26` أو `10.0.0.5 255.0.0.0`
- عرض: Network، Subnet Mask، Wildcard، Broadcast، First/Last Host، Hosts count
- التمثيل الثنائي 32-بت ملوّن (Network/Borrowed/Host bits)
- أوامر Cisco الجاهزة للنسخ (interface، ip address، ip route، OSPF، ACL)
- الحل خطوة بخطوة بالعربية
- **زر "نسخ الكل"** لنسخ التقرير الكامل
- **Subnet Finder**: ابحث عن الـ prefix المناسب حسب عدد المضيفين أو عدد الشبكات
- تصور نطاق العناوين (Network - First/Last Host - Broadcast)

#### 2. مقسم الشبكات (Network Divider - FLSM)
- تقسيم شبكة لعدد محدد من الشبكات المتساوية (Fixed Length)
- يدعم أي prefix جديد (مثلاً /24 → /26)
- جدول كامل بكل subnets: Network، First/Last Host، Broadcast
- نسخ الكل أو نسخ subnet واحد

#### 3. مقسم VLSM (Variable Length Subnet Mask)
- **يدعم أكثر من صنف (Class A/B/C/custom)** - ميزة فريدة!
- تقسيم حسب عدد المضيفين (يرتّب تنازلياً تلقائياً)
- يحسب الـ prefix المناسب لكل شبكة
- يعرض جدولاً كاملاً: Network، Range، Broadcast، Mask، Wildcard
- نسخ كل التقرير أو نسخ subnet واحد
- يكشف النقص في المساحة

#### 4. أدوات (Tools)
- **Subnetting Practice**: أسئلة عشوائية لتدريب الـ subnetting
- **Quick Converter**: تحويل سريع بين IP/Mask و Prefix/Wildcard/Network

#### 5. مرجع دراسي (Study Reference)
- جدول CIDR الشامل (16-30) مع بحث
- جدول أصناف IPv4 (Class A-E)
- عناوين IPv4 الخاصة (Loopback، APIPA، CGNAT، إلخ)
- قاعدة الحساب والـ Magic Numbers

### 🃏 تبويب الفلاش كارد (Flashcards)
- **80 بطاقة تعليمية** على شكل أسئلة امتحان/انترفيو (وليس مجرد مراجعة):
  - **36 سؤال امتحان** (Exam Style)
  - **44 سؤال انترفيو** (Interview Style)
  - يمكن فلترتها حسب النوع
- 6 فئات: Fundamentals، Routing، Switching، Security، Services، Advanced
- 3D flip animation للقلب
- تتبع التقدم مع نسبة مئوية
- ترتيب عشوائي (shuffle)
- اختصارات لوحة المفاتيح: `←/→` للتنقل، `Space` للقلب، `L` للتعليم
- سيناريوهات واقعية مع كل سؤال انترفيو
- حفظ التقدم في localStorage

### 🔬 تبويب لاب عملي (Labs)
- **6 سيناريوهات عملية كاملة**:
  1. إعداد راوتر أساسي + تأمين SSH (مبتدئ)
  2. VLANs + Trunking بين سويتشين (مبتدئ)
  3. OSPF Single-Area بين راوترين (متوسط)
  4. NAT Overload (PAT) للوصول للإنترنت (متوسط)
  5. HSRP بين راوترين (Active/Standby) (متوسط)
  6. ACL لحماية سيرفر + Filter Inbound (متوسط)
- كل سيناريو يحوي: الأهداف، الطوبولوجيا، خطوات الإعداد الكاملة مع الأوامر، التحقق، والمشاكل الشائعة
- فلترة حسب المستوى + بحث
- نسخ أوامر كل خطوة

### 🎨 ميزات إضافية
- **Dark Mode** + Light Mode
- **RTL Layout** عربي مع LTR للأكواد والأوامر
- **Bidi Isolation**: حل مشكلة عكس النص العربي/الإنجليزي
- **Responsive Design**: متجاوب مع الموبايل
- **خط Cairo** للعربية + JetBrains Mono للأكواد
- **Cisco Tech Colors**: الألوان الرسمية لسيسكو

## 🛠️ التقنيات المستخدمة

| التقنية | الإصدار | الاستخدام |
|---|---|---|
| Next.js | 16.1.3 | Framework (App Router) |
| TypeScript | 5 | اللغة |
| Tailwind CSS | 4 | Styling |
| shadcn/ui | - | UI Components |
| Lucide Icons | - | Icons |
| React | 19 | Library |

## 📁 هيكل المشروع

```
src/
├── app/
│   ├── globals.css          # CSS + Bidi fixes + Dark mode + 3D flip
│   ├── layout.tsx           # Root layout مع RTL + خطوط
│   └── page.tsx             # الصفحة الرئيسية مع 5 تبويبات
├── components/
│   ├── QuestionBank.tsx     # بنك الأسئلة (162 سؤال)
│   ├── SubnetCalculator.tsx # حاسبة SubnetPro (5 تبويبات)
│   ├── Flashcards.tsx       # 80 بطاقة تفاعلية
│   └── Labs.tsx             # 6 سيناريوهات عملية
├── data/
│   ├── cisco-data.ts        # أقسام 1-4
│   ├── cisco-data-part2.ts  # أقسام 5-9
│   ├── cisco-data-part3.ts  # أقسام 10-15
│   ├── cisco-data-part4.ts  # أقسام 16-22
│   ├── cisco-data-part5.ts  # أقسام 23-27
│   ├── index.ts             # فهرس الأوامر + search index
│   ├── questions-ccna.ts    # 68 سؤال CCNA
│   ├── questions-ccnp.ts    # 40 سؤال CCNP
│   ├── questions-interview.ts # 54 سؤال مقابلات
│   ├── questions-index.ts    # فهرس الأسئلة
│   ├── flashcards.ts        # 80 بطاقة تعليمية
│   └── lab-topologies.ts    # 6 سيناريوهات عملية
└── lib/
    ├── db.ts                # Prisma client
    └── utils.ts             # Helpers
```

## 🚀 التشغيل المحلي

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/cisco-ios-reference.git
cd cisco-ios-reference

# 2. Install dependencies
bun install  # أو npm install

# 3. Run development server
bun run dev  # أو npm run dev

# 4. Open in browser
# http://localhost:3000
```

## 📊 الإحصائيات

| الميزة | العدد |
|---|---|
| الأقسام الرئيسية | 27 |
| أوامر Cisco قابلة للنسخ | 362 |
| جداول مرجعية | 97 |
| أسئلة في بنك الأسئلة | 162 |
| بطاقات Flashcards | 80 |
| سيناريوهات Labs | 6 |
| تبويبات رئيسية | 5 |
| تبويبات فرعية في حاسبة Subnet | 5 |

## 🎯 المنهج المغطى

### CCNA 200-301
- Network Fundamentals (OSI, TCP/UDP, IPv4/IPv6)
- Network Access (VLANs, STP, Port Security, EtherChannel)
- IP Connectivity (Static, OSPF, EIGRP, NAT)
- IP Services (DHCP, NTP, Syslog, SNMP, SSH)
- Security Fundamentals (ACLs, 802.1x, AAA, Passwords)
- Automation & Programmability (REST API, NETCONF, YANG)

### CCNP ENARSI (إضافات)
- BGP (eBGP, iBGP, Attributes, Route Reflectors)
- OSPF Advanced (Areas, Stub, NSSA, LSAs, Virtual-Link)
- EIGRP Advanced (DUAL, SIA, Stub, Named Mode)
- FHRP (HSRP, VRRP, GLBP)
- Layer 2 Advanced (DHCP Snooping, DAI, IPSG, Loop/Root Guard)
- QoS (DSCP, Policing vs Shaping, LLQ, CBWFQ)
- IPsec/VPN (IKE, ESP, GRE)
- IPv6 Advanced (SLAAC, DHCPv6, NDP, Prefix Delegation)
- SDN/NFV (NETCONF, RESTCONF, YANG, VRF, MPLS)

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🤝 المساهمة

المساهمات مرحب بها! يرجى:
1. Fork المشروع
2. إنشاء branch للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الـ branch (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📧 التواصل

- المؤلف: Z.ai Network Engineering
- الإصدار: 1.0
- التاريخ: 2026

## 🙏 شكر خاص

- Cisco Systems للتدريب والشهادات
- Next.js Team للـ framework الممتاز
- shadcn/ui للمكتبات الجميلة
- Lucide للأيقونات

---

⭐ إذا كان هذا المشروع مفيداً لك، فلا تنسَ إعطاؤه نجمة على GitHub!

</div>

## 🇬🇧 English Summary

A comprehensive interactive reference for Cisco IOS commands with:
- **27 sections** covering CCNA 200-301 + CCNP ENARSI
- **362 copyable commands** with explanations
- **162 questions** (68 CCNA + 40 CCNP + 54 Interview)
- **80 flashcards** (exam-style + interview-style)
- **6 practical lab topologies** with step-by-step configurations
- **Professional Subnet Calculator** (5 tabs: Analyzer, Divider, VLSM, Tools, Reference)
- Dark mode, RTL Arabic layout, responsive design
- Built with Next.js 16 + TypeScript + Tailwind CSS 4

## License

MIT License - feel free to use, modify, and distribute.
