# -*- coding: utf-8 -*-
"""Part 09: Section 21 - Subnetting/VLSM + Section 22 - IPv6 Detailed"""

SECTIONS_09 = """

<!-- ============ SECTION 21: SUBNETTING & VLSM ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 21</span>
    <div class="chapter-title">مرجع Subnetting و VLSM</div>
    <div class="chapter-title-en">CIDR Table, Subnetting &amp; VLSM Examples</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    Subnetting هو تقسيم شبكة كبيرة إلى شبكات صغيرة متعددة لتقليل حجم broadcast domain وتحسين الأمان وكفاءة التوجيه. CIDR (Classless Inter-Domain Routing) هو الترميز الحديث للأقنعة بصيغة <code class="inline">/n</code> بدلاً من الأقنعة العشرية. VLSM (Variable Length Subnet Mask) هي توسعة لـ subnetting تسمح باستعمال أقنعة مختلفة الطول داخل نفس الشبكة لتفادي إهدار العناوين. مثلاً، في شبكة 192.168.1.0/24 يمكن استخدام /30 لوصلات point-to-point، /27 لشبكات مستخدمين صغار، /25 لشبكة مستخدمين كبيرة. كل شبكة فرعية لها: Network Address (الأول)، Broadcast (الأخير)، Hosts (ما بينهما).
</div>

<div class="section-title">جدول CIDR الكامل</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>CIDR</th>
            <th>Subnet Mask</th>
            <th>Wildcard Mask</th>
            <th>Hosts/Subnet</th>
            <th>Subnets in /24</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>/30</td><td>255.255.255.252</td><td>0.0.0.3</td><td>2</td><td>64</td></tr>
        <tr><td>/29</td><td>255.255.255.248</td><td>0.0.0.7</td><td>6</td><td>32</td></tr>
        <tr><td>/28</td><td>255.255.255.240</td><td>0.0.0.15</td><td>14</td><td>16</td></tr>
        <tr><td>/27</td><td>255.255.255.224</td><td>0.0.0.31</td><td>30</td><td>8</td></tr>
        <tr><td>/26</td><td>255.255.255.192</td><td>0.0.0.63</td><td>62</td><td>4</td></tr>
        <tr><td>/25</td><td>255.255.255.128</td><td>0.0.0.127</td><td>126</td><td>2</td></tr>
        <tr><td>/24</td><td>255.255.255.0</td><td>0.0.0.255</td><td>254</td><td>1</td></tr>
        <tr><td>/23</td><td>255.255.254.0</td><td>0.0.1.255</td><td>510</td><td>0.5 (supernet)</td></tr>
        <tr><td>/22</td><td>255.255.252.0</td><td>0.0.3.255</td><td>1022</td><td>0.25</td></tr>
        <tr><td>/21</td><td>255.255.248.0</td><td>0.0.7.255</td><td>2046</td><td>0.125</td></tr>
        <tr><td>/20</td><td>255.255.240.0</td><td>0.0.15.255</td><td>4094</td><td>0.0625</td></tr>
        <tr><td>/19</td><td>255.255.224.0</td><td>0.0.31.255</td><td>8190</td><td>-</td></tr>
        <tr><td>/18</td><td>255.255.192.0</td><td>0.0.63.255</td><td>16382</td><td>-</td></tr>
        <tr><td>/17</td><td>255.255.128.0</td><td>0.0.127.255</td><td>32766</td><td>-</td></tr>
        <tr><td>/16</td><td>255.0.0.0</td><td>0.255.255.255</td><td>65534</td><td>-</td></tr>
    </tbody>
</table>

<div class="section-title">عناوين RFC 1918 الخاصة</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>Class</th>
            <th>Range</th>
            <th>CIDR Block</th>
            <th>Number of /24s</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Class A</td><td>10.0.0.0 - 10.255.255.255</td><td>10.0.0.0/8</td><td>256 × 256 = 65,536</td></tr>
        <tr><td>Class B</td><td>172.16.0.0 - 172.31.255.255</td><td>172.16.0.0/12</td><td>16 × 256 = 4,096</td></tr>
        <tr><td>Class C</td><td>192.168.0.0 - 192.168.255.255</td><td>192.168.0.0/16</td><td>256</td></tr>
        <tr><td>CGNAT</td><td>100.64.0.0 - 100.127.255.255</td><td>100.64.0.0/10</td><td>1,024</td></tr>
        <tr><td>Loopback</td><td>127.0.0.0 - 127.255.255.255</td><td>127.0.0.0/8</td><td>-</td></tr>
        <tr><td>Link-local</td><td>169.254.0.0 - 169.254.255.255</td><td>169.254.0.0/16</td><td>-</td></tr>
        <tr><td>Benchmark</td><td>198.18.0.0 - 198.19.255.255</td><td>198.18.0.0/15</td><td>-</td></tr>
    </tbody>
</table>

<div class="section-title">حساب IP Subnetting - الخطوات</div>
<div class="body-text">
    لحساب معلومات أي شبكة فرعية، اتبع هذه الخطوات: (1) اكتب IP المضيف بالصيغة الثنائية. (2) ارسم خطاً فاصلاً بين network portion و host portion حسب CIDR (مثلاً /24 = أول 24 بت للشبكة). (3) لـ Network Address: اجعل كل host bits = 0. (4) لـ Broadcast Address: اجعل كل host bits = 1. (5) لـ First Host: Network + 1. (6) لـ Last Host: Broadcast - 1. (7) لـ Wildcard Mask: عكس Subnet Mask (مثلاً 255.255.255.192 → 0.0.0.63).
</div>

<div class="section-title">مثال محلول: حساب شبكة 192.168.10.130/26</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>المعطى</th>
            <th>القيمة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>IP المضيف</td><td>192.168.10.130</td></tr>
        <tr><td>CIDR</td><td>/26 (Subnet Mask 255.255.255.192)</td></tr>
        <tr><td>Host bits</td><td>32-26 = 6</td></tr>
        <tr><td>Hosts/Subnet</td><td>2^6 - 2 = 62</td></tr>
        <tr><td>Subnet block size</td><td>2^6 = 64</td></tr>
        <tr><td>Network</td><td>192.168.10.128 (الـ 128 مضاعف 64)</td></tr>
        <tr><td>First Host</td><td>192.168.10.129</td></tr>
        <tr><td>Last Host</td><td>192.168.10.190</td></tr>
        <tr><td>Broadcast</td><td>192.168.10.191</td></tr>
        <tr><td>Wildcard</td><td>0.0.0.63</td></tr>
    </tbody>
</table>

<div class="section-title">VLSM - مثال شامل</div>
<div class="body-text">
    لنفترض أن لدينا شبكة 192.168.1.0/24 ونريد تقسيمها لتغطية: (1) شبكة LAN كبيرة 60 مضيفاً، (2) شبكة LAN صغيرة 25 مضيفاً، (3) شبكة 10 مضيفين، (4) ثلاثة وصلات point-to-point (2 مضيفين لكل منها).
</div>

<table class="subnet-table">
    <thead>
        <tr>
            <th>الشبكة</th>
            <th>عدد المضيفين</th>
            <th>CIDR المطلوب</th>
            <th>عنوان الشبكة</th>
            <th>نطاق المضيفين</th>
            <th>Broadcast</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>LAN1 (Users)</td><td>60</td><td>/26 (62 hosts)</td><td>192.168.1.0</td><td>.1 - .62</td><td>.63</td></tr>
        <tr><td>LAN2 (Servers)</td><td>25</td><td>/27 (30 hosts)</td><td>192.168.1.64</td><td>.65 - .94</td><td>.95</td></tr>
        <tr><td>LAN3 (Printers)</td><td>10</td><td>/28 (14 hosts)</td><td>192.168.1.96</td><td>.97 - .110</td><td>.111</td></tr>
        <tr><td>WAN R1-R2</td><td>2</td><td>/30 (2 hosts)</td><td>192.168.1.112</td><td>.113 - .114</td><td>.115</td></tr>
        <tr><td>WAN R1-R3</td><td>2</td><td>/30 (2 hosts)</td><td>192.168.1.116</td><td>.117 - .118</td><td>.119</td></tr>
        <tr><td>WAN R2-R3</td><td>2</td><td>/30 (2 hosts)</td><td>192.168.1.120</td><td>.121 - .122</td><td>.123</td></tr>
        <tr><td>المتبقي (للتوسعة)</td><td>-</td><td>/28 متبقي</td><td>192.168.1.124</td><td>.125 - .126</td><td>.127</td></tr>
    </tbody>
</table>

<div class="tip-box">
    <div class="tip-box-title">قاعدة ذهبية لـ VLSM</div>
    <div class="tip-box-body">
        عند تقسيم شبكة بـ VLSM، ابدأ من أكبر مجموعة مضيفين إلى أصغر. السبب: لو بدأت من /30 ثم حاولت وضع /26، قد لا تجد مساحة متصلة. الطريقة: رتّب الشبكات المطلوبة تنازلياً حسب عدد المضيفين، ثم وزّع IPs بالترتيب، بدءاً من أول IP في الشبكة الأم. هذه الطريقة تضمن عدم التداخل (overlap) وأقصى استخدام للعناوين.
    </div>
</div>

<div class="section-title">حساب سريع في الرأس - اختصارات</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>CIDR</th>
            <th>Block Size (آخر أوكتات)</th>
            <th>Quick Network Calculation</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>/24</td><td>256</td><td>أي IP → network هو .0 من نفس الـ /24</td></tr>
        <tr><td>/25</td><td>128</td><td>الـ IP الأخير &lt; 128 → network .0؛ ≥ 128 → network .128</td></tr>
        <tr><td>/26</td><td>64</td><td>تجد أقرب مضاعف 64 ≤ IP: 0، 64، 128، 192</td></tr>
        <tr><td>/27</td><td>32</td><td>أقرب مضاعف 32: 0، 32، 64، 96، 128، 160، 192، 224</td></tr>
        <tr><td>/28</td><td>16</td><td>أقرب مضاعف 16</td></tr>
        <tr><td>/29</td><td>8</td><td>أقرب مضاعف 8</td></tr>
        <tr><td>/30</td><td>4</td><td>أقرب مضاعف 4</td></tr>
    </tbody>
</table>

<div class="warn-box">
    <div class="warn-box-title">حفظ الـ Magic Numbers</div>
    <div class="warn-box-body">
        احفظ هذه الأرقام لاختبار CCNA لأنها تأتي مراراً: Block sizes: /30 → 4، /29 → 8، /28 → 16، /27 → 32، /26 → 64، /25 → 128. عدد المضيفين: 2، 6، 14، 30، 62، 126 (Block size - 2). قناع الشبكة: 252، 248، 240، 224، 192، 128. الـ Wildcard: 3، 7، 15، 31، 63، 127. تمرّن على حلّ مسائل subnetting في 60 ثانية أو أقل للنجاح في الامتحان.
    </div>
</div>


<!-- ============ SECTION 22: IPv6 DETAILED ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 22</span>
    <div class="chapter-title">IPv6 - القسم التفصيلي المستقل</div>
    <div class="chapter-title-en">IPv6 Addressing, Routing, ACLs &amp; Services</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    IPv6 (Internet Protocol version 6) صُمم لمعالجة استنفاد عناوين IPv4. يستعمل 128 بت بدلاً من 32 (أي 3.4×10^38 عنوان تقريباً). مميزاته: (1) لا حاجة لـ NAT/PAT في الشبكات الداخلية (العناوين متاحة بكثرة)، (2) Header أبسط لمعالجة أسرع، (3) دعم أصلي لـ IPsec، (4) دعم stateless autoconfiguration (SLAAC)، (5) لا Broadcast (يستعمل Multicast بدلاً منه)، (6) عناوين link-local تلقائية (fe80::). أنواع عناوين IPv6: <strong>Global Unicast</strong> (2000::/3 - قابلة للتوجيه)، <strong>Link-Local</strong> (fe80::/10 - للشبكة المحلية فقط)، <strong>Unique Local</strong> (fc00::/7 - مثل RFC 1918)، <strong>Multicast</strong> (ff00::/8)، <strong>Anycast</strong> (مخصص لمجموعة).
</div>

<div class="section-title">أنواع عناوين IPv6</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">النوع</th>
            <th style="width: 25%;">Prefix</th>
            <th style="width: 25%;">النطاق</th>
            <th style="width: 25%;">الاستخدام</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Global Unicast</td><td>2000::/3</td><td>عالمي</td><td>العنوان الرسمي على الإنترنت.</td></tr>
        <tr><td>Link-Local</td><td>fe80::/10</td><td>الشبكة المحلية فقط</td><td>للتواصل بين جيران على نفس link (Neighbors Discovery).</td></tr>
        <tr><td>Unique Local (ULA)</td><td>fc00::/7 (fd00::/8)</td><td>عالمي (لكن داخلي)</td><td>مثل RFC 1918 في IPv4.</td></tr>
        <tr><td>Multicast</td><td>ff00::/8</td><td>متعدد</td><td>الإرسال لمجموعة من الأجهزة (بديل البث في IPv4).</td></tr>
        <tr><td>Loopback</td><td>::1/128</td><td>محلي</td><td>مثل 127.0.0.1.</td></tr>
        <tr><td>Unspecified</td><td>::/128</td><td>محلي</td><td>عنوان فارغ (للإرسال من جهاز لا يزال يكتسب IP).</td></tr>
        <tr><td>Solicited-Node</td><td>ff02::1:ff00:0/104</td><td>link-local</td><td>تلقائي، لاستبدال ARP في IPv6.</td></tr>
    </tbody>
</table>

<div class="section-title">Multicast Address المعروفة</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">العنوان</th>
            <th style="width: 25%;">المجموعة</th>
            <th style="width: 35%;">الوصف</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>ff02::1</td><td>All Nodes</td><td>كل الأجهزة على link (بديل broadcast في IPv4).</td></tr>
        <tr><td>ff02::2</td><td>All Routers</td><td>كل الراوترات على link.</td></tr>
        <tr><td>ff02::5</td><td>OSPF</td><td>كل راوترات OSPF.</td></tr>
        <tr><td>ff02::6</td><td>OSPF DR/BDR</td><td>OSPF Designated Routers.</td></tr>
        <tr><td>ff02::a</td><td>EIGRP</td><td>كل راوترات EIGRP.</td></tr>
        <tr><td>ff02::1:ff00:0/104</td><td>Solicited-Node</td><td>عنوان تلقائي يولّد لكل IPv6 host لاستبدال ARP.</td></tr>
        <tr><td>ff02::fb</td><td>mDNS</td><td>Multicast DNS.</td></tr>
    </tbody>
</table>

<div class="section-title">اختصار كتابة IPv6</div>
<div class="body-text">
    قواعد اختصار عناوين IPv6: (1) إسقاط الأصفار الأولى في كل مقطع 16-بت (مثل 09ab → 9ab). (2) استبدال أطول سلسلة من المقاطع الصفرية المتتالية بـ <code class="inline">::</code> مرة واحدة فقط في العنوان. مثلاً: <code class="inline">2001:0db8:0000:0000:0000:0000:0000:0001</code> يُختصر إلى <code class="inline">2001:db8::1</code>. عناوين مثل <code class="inline">2001:db8:0:0:1:0:0:1</code> لا تختصر بـ <code class="inline">::</code> مرتين، بل تكتب <code class="inline">2001:db8::1:0:0:1</code> (اختر أطول سلسلة صفرية للاختصار).
</div>

<div class="section-title">EUI-64: توليد IPv6 من MAC</div>
<div class="body-text">
    EUI-64 يولّد host portion من عنوان IPv6 من MAC address المضيف. الخطوات: (1) يقسم الـ MAC (48 بت) إلى نصفين (24 بت لكل). (2) يُدخل <code class="inline">FFFE</code> في المنتصف (الـ OUI + FFFE + الـ NIC-specific). (3) يقلب البت السابع (U/L bit) من أول أوكتات. مثلاً: MAC = <code class="inline">00:1A:2B:3C:4D:5E</code>. بعد إدراج FFFE: <code class="inline">00:1A:2B:FF:FE:3C:4D:5E</code>. بعد قلب البت السابع (00 → 02): <code class="inline">02:1A:2B:FF:FE:3C:4D:5E</code>. لعنوان شبكة <code class="inline">2001:db8:1::/64</code> يكون الـ IPv6 الكامل: <code class="inline">2001:db8:1::21a:2bff:fe3c:4d5e</code>.
</div>

<div class="section-title">أوامر IPv6</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 30%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">ipv6 unicast-routing</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل توجيه IPv6 على الراوتر. <strong>مطلوب</strong> قبل أي IPv6 routing.</td>
            <td class="no-col">no ipv6 unicast-routing</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 enable</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل IPv6 على الواجهة وتوليد link-local تلقائياً.</td>
            <td class="no-col">no ipv6 enable</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address &lt;ipv6&gt;/&lt;prefix&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين IPv6 ثابت.</td>
            <td class="no-col">no ipv6 address</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address &lt;prefix&gt;/&lt;len&gt; eui-64</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين IPv6 باستعمال EUI-64 (يولّد host portion من MAC).</td>
            <td class="no-col">no ipv6 address &lt;prefix&gt; eui-64</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address autoconfig</td>
            <td class="mode-col">Interface Config</td>
            <td>الحصول على IPv6 عبر SLAAC (Stateless Address AutoConfig).</td>
            <td class="no-col">no ipv6 address autoconfig</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address dhcp</td>
            <td class="mode-col">Interface Config</td>
            <td>الحصول على IPv6 عبر DHCPv6 (Stateful).</td>
            <td class="no-col">no ipv6 address dhcp</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address fe80::1 link-local</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين link-local address يدوياً (الافتراضي: توليد تلقائي).</td>
            <td class="no-col">no ipv6 address fe80::1 link-local</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 nd other-config-flag</td>
            <td class="mode-col">Interface Config</td>
            <td>علم O في RA - يطلب من المضيفين الحصول على معلومات إضافية (DNS) من DHCPv6.</td>
            <td class="no-col">no ipv6 nd other-config-flag</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 nd managed-config-flag</td>
            <td class="mode-col">Interface Config</td>
            <td>علم M في RA - يطلب من المضيفين الحصول على IPv6 كاملاً من DHCPv6 (Stateful).</td>
            <td class="no-col">no ipv6 nd managed-config-flag</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 nd prefix &lt;prefix&gt;/&lt;len&gt; &lt;valid-lifetime&gt; &lt;preferred-lifetime&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تخصيص prefix في RA.</td>
            <td class="no-col">no ipv6 nd prefix</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 route &lt;network&gt;/&lt;prefix&gt; &lt;next-hop&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت IPv6.</td>
            <td class="no-col">no ipv6 route</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 route ::/0 &lt;next-hop&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>Default route IPv6.</td>
            <td class="no-col">no ipv6 route ::/0</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 traffic-filter &lt;name&gt; in|out</td>
            <td class="mode-col">Interface Config</td>
            <td>تطبيق IPv6 ACL على الواجهة.</td>
            <td class="no-col">no ipv6 traffic-filter</td>
        </tr>
    </tbody>
</table>

<div class="section-title">DHCPv6 على الراوتر</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 28%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">ipv6 dhcp pool &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء DHCPv6 pool.</td>
            <td class="no-col">no ipv6 dhcp pool</td>
        </tr>
        <tr>
            <td class="cmd-col">address prefix &lt;prefix&gt;/&lt;len&gt;</td>
            <td class="mode-col">DHCPv6 Pool</td>
            <td>تحديد prefix للعناوين.</td>
            <td class="no-col">no address prefix</td>
        </tr>
        <tr>
            <td class="cmd-col">dns-server &lt;ipv6&gt;</td>
            <td class="mode-col">DHCPv6 Pool</td>
            <td>تعيين DNS server.</td>
            <td class="no-col">no dns-server</td>
        </tr>
        <tr>
            <td class="cmd-col">domain-name &lt;name&gt;</td>
            <td class="mode-col">DHCPv6 Pool</td>
            <td>تعيين اسم النطاق.</td>
            <td class="no-col">no domain-name</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 dhcp server &lt;pool&gt; [rapid-commit]</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل الجهاز كـ DHCPv6 server على الواجهة.</td>
            <td class="no-col">no ipv6 dhcp server</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 dhcp relay destination &lt;ipv6&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل الجهاز كـ DHCPv6 relay.</td>
            <td class="no-col">no ipv6 dhcp relay</td>
        </tr>
    </tbody>
</table>

<div class="section-title">SLAAC vs DHCPv6 (Stateless vs Stateful)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 20%;">النمط</th>
            <th style="width: 15%;">RA Flags</th>
            <th style="width: 30%;">طريقة توليد IP</th>
            <th style="width: 35%;">متى يستعمل</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>SLAAC</td><td>M=0, O=0</td><td>المضيف يولّد IPv6 من RA prefix + EUI-64 أو عشوائي</td><td>الوضع الافتراضي، شبكات بسيطة.</td></tr>
        <tr><td>SLAAC + DHCPv6</td><td>M=0, O=1</td><td>المضيف يولّد IP عبر SLAAC، يحصل على DNS/NTP من DHCPv6</td><td>الأكثر شيوعاً اليوم.</td></tr>
        <tr><td>Stateful DHCPv6</td><td>M=1, O=1</td><td>المضيف يحصل على IP كاملاً من DHCPv6</td><td>عند الحاجة لتتبع leases.</td></tr>
        <tr><td>Manual</td><td>N/A</td><td>تعيين يدوي</td><td>السيرفرات وأجهزة الإنتاج الحرجة.</td></tr>
    </tbody>
</table>

<div class="section-title">Neighbor Discovery Protocol (NDP)</div>
<div class="body-text">
    NDP يحل محل ARP في IPv4. يستعمل ICMPv6 type 135 (Solicitation) و 136 (Advertisement). عملية اكتشاف الجيران: (1) الجهاز يحتاج MAC للجار فيصل لـ Solicited-Node Multicast. (2) الجار المسجل في تلك المجموعة يجيب بـ Neighbor Advertisement يحوي MAC. عملية اكتشاف الراوتر: (1) المضيف يرسل Router Solicitation (RS) إلى ff02::2. (2) الراوتر يجيب بـ Router Advertisement (RA) إلى ff02::1 يحوي prefix والإعدادات.
</div>

<div class="section-title">مثال: إعداد IPv6 كامل</div>
<div class="code-block">
Router(config)# <span class="prompt">ipv6 unicast-routing</span>
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ipv6 enable</span>
Router(config-if)# <span class="prompt">ipv6 address 2001:db8:1::1/64</span>
Router(config-if)# <span class="prompt">ipv6 address fe80::1 link-local</span>
Router(config-if)# <span class="prompt">ipv6 nd other-config-flag</span>     <span class="comment">! O=1: DNS via DHCPv6</span>
Router(config-if)# <span class="prompt">exit</span>

<span class="comment">! إعداد DHCPv6 Pool للـ DNS</span>
Router(config)# <span class="prompt">ipv6 dhcp pool DNS-OPTIONS</span>
Router(config-dhcpv6)# <span class="prompt">dns-server 2001:4860:4860::8888</span>
Router(config-dhcpv6)# <span class="prompt">domain-name cairo-net.local</span>
Router(config-dhcpv6)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ipv6 dhcp server DNS-OPTIONS</span>
Router(config-if)# <span class="prompt">exit</span>

<span class="comment">! Default route</span>
Router(config)# <span class="prompt">ipv6 route ::/0 2001:db8:acad::1</span>

<span class="comment">! ACL IPv6 - منع telnet من خارج</span>
Router(config)# <span class="prompt">ipv6 access-list BLOCK-TELNET</span>
Router(config-ipv6-acl)# <span class="prompt">permit ipv6 2001:db8:1::/64 any</span>
Router(config-ipv6-acl)# <span class="prompt">deny tcp any any eq 23</span>
Router(config-ipv6-acl)# <span class="prompt">permit ipv6 any any</span>
Router(config-ipv6-acl)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/1</span>     <span class="comment">! WAN</span>
Router(config-if)# <span class="prompt">ipv6 traffic-filter BLOCK-TELNET in</span>
Router(config-if)# <span class="prompt">exit</span>

Router# <span class="prompt">show ipv6 interface brief</span>
GigabitEthernet0/0    [up/up]
    FE80::1
    2001:DB8:1::1
GigabitEthernet0/1    [up/up]
    FE80::2
    2001:DB8:ACAD::2

Router# <span class="prompt">show ipv6 route</span>
IPv6 Routing Table - 7 entries
C   2001:DB8:1::/64 [0/0]
    via GigabitEthernet0/0, directly connected
S*  ::/0 [1/0]
    via 2001:DB8:ACAD::1, GigabitEthernet0/1
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة لـ IPv6</div>
    <div class="tip-box-body">
        لا تخلط بين <code class="inline">ipv6 enable</code> (يفعل IPv6 على الواجهة ويولّد link-local فقط) و <code class="inline">ipv6 unicast-routing</code> (يفعل التوجيه على الجهاز بالكامل). كلاهما مطلوب لكي يعمل IPv6 routing. للتحقق من عمل IPv6، استخدم <code class="inline">show ipv6 interface brief</code> (للحالة) و <code class="inline">show ipv6 route</code> (للجدول) و <code class="inline">show ipv6 neighbors</code> (لجدول NDP - بديل ARP).
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">ملاحظة أمنية</div>
    <div class="warn-box-body">
        IPv6 ليس آمناً بالتلقائية! يجب تطبيق نفس ممارسات IPv4 الأمنية: ACLs على الحدود، DHCPv6 Snooping، RA Guard، Source Guard، uRPF. هجوم Rogue RA شائع: مهاجم يرسل RAs بعنوان prefix وهمي ليخطف الحركة. الحماية: <code class="inline">ipv6 nd ra guard</code> على بورتات المستخدمين. وأيضاً تأكد من تصفية <code class="inline">::/0 route</code> وعدم نشره على البورتات الخطأ.
    </div>
</div>

"""
