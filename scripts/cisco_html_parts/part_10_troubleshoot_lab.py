# -*- coding: utf-8 -*-
"""Part 10: Section 23 - Troubleshooting & Show Commands + Section 24 - Lab Scenarios"""

SECTIONS_10 = """

<!-- ============ SECTION 23: TROUBLESHOOTING & SHOW COMMANDS ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 23</span>
    <div class="chapter-title">Troubleshooting &amp; Show Commands - المرجع الكامل</div>
    <div class="chapter-title-en">Master Reference for Verification &amp; Diagnostics</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    الأوامر العرضية (<code class="inline">show</code>) هي أكثر ما يستخدمه مهندس الشبكات يومياً، سواء للتشخيص أو للتأكد من سلامة الإعداد. هذا القسم هو مرجع شامل لكل الأوامر العرضية مصنّفة حسب الوظيفة. القاعدة الذهبية للتشخيص: ابدأ من الـ Physical Layer (السلك، الضوء)، ثم الـ Data Link (MAC، ARP)، ثم الـ Network (IP، routing)، ثم التطبيقات. كل أمر <code class="inline">show</code> يلبي سؤالاً تشخيصياً محدداً، فهم الـ "ماذا يخبرني هذا الأمر؟" هو مفتاح الاحتراف.
</div>

<div class="section-title">أوامر العرض العامة (System)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show version</td><td class="mode-col">Privileged EXEC</td><td>إصدار IOS، نوع المعالج، حجم الذاكرة، config-register، اسم الجهاز، مدة التشغيل. أساسي لأي تشخيص.</td></tr>
        <tr><td class="cmd-col">show running-config</td><td class="mode-col">Privileged EXEC</td><td>الإعداد الكامل الحالي في RAM.</td></tr>
        <tr><td class="cmd-col">show running-config | section &lt;text&gt;</td><td class="mode-col">Privileged EXEC</td><td>فلترة قسم محدد من الإعداد.</td></tr>
        <tr><td class="cmd-col">show running-config | include &lt;text&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض الأسطر التي تحتوي كلمة محددة.</td></tr>
        <tr><td class="cmd-col">show running-config | begin &lt;text&gt;</td><td class="mode-col">Privileged EXEC</td><td>البدء من أول سطر يحتوي على الكلمة.</td></tr>
        <tr><td class="cmd-col">show startup-config</td><td class="mode-col">Privileged EXEC</td><td>الإعداد المحفوظ في NVRAM.</td></tr>
        <tr><td class="cmd-col">show boot</td><td class="mode-col">Privileged EXEC</td><td>إعدادات الإقلاع، config-register، مصدر IOS.</td></tr>
        <tr><td class="cmd-col">show processes cpu</td><td class="mode-col">Privileged EXEC</td><td>استخدام CPU خلال 5 ثواني/1 دقيقة/5 دقائق + قائمة العمليات.</td></tr>
        <tr><td class="cmd-col">show processes cpu history</td><td class="mode-col">Privileged EXEC</td><td>رسم بياني نصي لاستخدام CPU عبر آخر 60 ثانية وساعة و72 ساعة.</td></tr>
        <tr><td class="cmd-col">show memory</td><td class="mode-col">Privileged EXEC</td><td>استخدام الذاكرة: free، used.</td></tr>
        <tr><td class="cmd-col">show flash:</td><td class="mode-col">Privileged EXEC</td><td>محتوى flash مع حجم الملفات والمساحة الحرة.</td></tr>
        <tr><td class="cmd-col">show env all</td><td class="mode-col">Privileged EXEC</td><td>درجات الحرارة، الفولتية، سرعات المراوح (إن وُجدت).</td></tr>
        <tr><td class="cmd-col">show inventory</td><td class="mode-col">Privileged EXEC</td><td>قائمة العتاد مع Serial Numbers.</td></tr>
        <tr><td class="cmd-col">show clock</td><td class="mode-col">Privileged EXEC</td><td>التاريخ والوقت.</td></tr>
        <tr><td class="cmd-col">show history</td><td class="mode-col">User/Privileged</td><td>قائمة آخر الأوامر المنفّذة.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر الواجهات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip interface brief</td><td class="mode-col">Privileged EXEC</td><td>عرض كل الواجهات مع IP وحالتها (up/down/administratively down). <strong>أكثر أمر استخداماً!</strong></td></tr>
        <tr><td class="cmd-col">show ipv6 interface brief</td><td class="mode-col">Privileged EXEC</td><td>نفس السابق لكن لعناوين IPv6.</td></tr>
        <tr><td class="cmd-col">show interfaces</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل كاملة: MAC، IP، إحصائيات الإرسال/الاستقبال، أخطاء، MTU.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show interfaces description</td><td class="mode-col">Privileged EXEC</td><td>كل الواجهات مع الأوصاف والحالة في جدول.</td></tr>
        <tr><td class="cmd-col">show interfaces status</td><td class="mode-col">Privileged EXEC</td><td>للسويتش: السرعة، duplex، VLAN، نوع الاتصال.</td></tr>
        <tr><td class="cmd-col">show ip interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>إعدادات IP على الواجهة: proxy-arp، redirects، ACLs.</td></tr>
        <tr><td class="cmd-col">show ipv6 interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>إعدادات IPv6 على الواجهة.</td></tr>
        <tr><td class="cmd-col">show interfaces counters</td><td class="mode-col">Privileged EXEC</td><td>عدد الحزم والبايتات المرسلة والمستلمة لكل واجهة.</td></tr>
        <tr><td class="cmd-col">show interfaces counters errors</td><td class="mode-col">Privileged EXEC</td><td>أخطاء لكل واجهة: CRC، runts، giants، input errors، output errors.</td></tr>
        <tr><td class="cmd-col">show controllers &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>نوع الكابل (DTE/DCE) - ضروري لوصلات Serial.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر CDP/LLDP (الجيران)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show cdp</td><td class="mode-col">Privileged EXEC</td><td>هل CDP مفعّل عالمياً؟</td></tr>
        <tr><td class="cmd-col">show cdp neighbors</td><td class="mode-col">Privileged EXEC</td><td>قائمة الجيران: الجهاز، الواجهة المحلية والبعيدة، نوع الجهاز.</td></tr>
        <tr><td class="cmd-col">show cdp neighbors detail</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل كاملة: IP، IOS version، platform.</td></tr>
        <tr><td class="cmd-col">show cdp entry &lt;name&gt;</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل جار محدد بالاسم.</td></tr>
        <tr><td class="cmd-col">show cdp interface</td><td class="mode-col">Privileged EXEC</td><td>الواجهات المفعّل عليها CDP.</td></tr>
        <tr><td class="cmd-col">show lldp</td><td class="mode-col">Privileged EXEC</td><td>حالة LLDP العامة.</td></tr>
        <tr><td class="cmd-col">show lldp neighbors</td><td class="mode-col">Privileged EXEC</td><td>قائمة جيران LLDP (معيار IEEE 802.1AB - مفتوح، ليس Cisco-Proprietary).</td></tr>
        <tr><td class="cmd-col">show lldp neighbors detail</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل جيران LLDP.</td></tr>
        <tr><td class="cmd-col">show lldp interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>حالة LLDP على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">cdp run</td><td class="mode-col">Global Config</td><td>تفعيل CDP عالمياً (مفعّل افتراضياً).</td></tr>
        <tr><td class="cmd-col">cdp enable</td><td class="mode-col">Interface Config</td><td>تفعيل CDP على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">no cdp enable</td><td class="mode-col">Interface Config</td><td>تعطيل CDP على واجهة (موصى به على بورتات-facing-Internet).</td></tr>
        <tr><td class="cmd-col">lldp run</td><td class="mode-col">Global Config</td><td>تفعيل LLDP عالمياً (معطّل افتراضياً).</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر MAC Address Table و ARP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show mac address-table</td><td class="mode-col">Privileged EXEC</td><td>عرض جدول MAC الكامل في السويتش (VLAN، MAC، Port، Type).</td></tr>
        <tr><td class="cmd-col">show mac address-table dynamic</td><td class="mode-col">Privileged EXEC</td><td>فقط MACs المتعلمة ديناميكياً.</td></tr>
        <tr><td class="cmd-col">show mac address-table static</td><td class="mode-col">Privileged EXEC</td><td>MACs الثابتة المعرّفة يدوياً.</td></tr>
        <tr><td class="cmd-col">show mac address-table interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>MACs على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show mac address-table vlan &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>MACs في VLAN محدد.</td></tr>
        <tr><td class="cmd-col">show ip arp</td><td class="mode-col">Privileged EXEC</td><td>جدول ARP على الراوتر (IP ↔ MAC ↔ Interface).</td></tr>
        <tr><td class="cmd-col">show ip arp &lt;ip&gt;</td><td class="mode-col">Privileged EXEC</td><td>البحث عن MAC لعنوان IP محدد.</td></tr>
        <tr><td class="cmd-col">clear arp-cache</td><td class="mode-col">Privileged EXEC</td><td>مسح جدول ARP الديناميكي.</td></tr>
        <tr><td class="cmd-col">clear mac address-table dynamic</td><td class="mode-col">Privileged EXEC</td><td>مسح MACs الديناميكية.</td></tr>
        <tr><td class="cmd-col">show ipv6 neighbors</td><td class="mode-col">Privileged EXEC</td><td>جدول NDP (بديل ARP في IPv6).</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر VLAN و Trunking</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show vlan brief</td><td class="mode-col">Privileged EXEC</td><td>كل VLANs مع أسمائها والبورتات المنتمية.</td></tr>
        <tr><td class="cmd-col">show vlan</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل كاملة عن VLANs.</td></tr>
        <tr><td class="cmd-col">show vlan id &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل VLAN محدد.</td></tr>
        <tr><td class="cmd-col">show interfaces trunk</td><td class="mode-col">Privileged EXEC</td><td>كل بورتات الـ trunk و VLANs المسموحة.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt; trunk</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل trunk على واجهة.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt; switchport</td><td class="mode-col">Privileged EXEC</td><td>الإعداد الإداري والتشغيلي للبورت (access/trunk).</td></tr>
        <tr><td class="cmd-col">show dtp interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>حالة DTP على واجهة.</td></tr>
        <tr><td class="cmd-col">show vtp status</td><td class="mode-col">Privileged EXEC</td><td>إعدادات VTP: الإصدار، الوضع، النطاق، revision.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر STP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show spanning-tree</td><td class="mode-col">Privileged EXEC</td><td>كل تفاصيل STP: VLANs، Root Bridge، الأولوية، البورتات وأدوارها.</td></tr>
        <tr><td class="cmd-col">show spanning-tree vlan &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>STP لـ VLAN محدد.</td></tr>
        <tr><td class="cmd-col">show spanning-tree summary</td><td class="mode-col">Privileged EXEC</td><td>ملخص إعدادات STP: الوضع، UplinkFast، BackboneFast.</td></tr>
        <tr><td class="cmd-col">show spanning-tree root</td><td class="mode-col">Privileged EXEC</td><td>Root Bridge لكل VLAN.</td></tr>
        <tr><td class="cmd-col">show spanning-tree interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>STP على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show spanning-tree blockedports</td><td class="mode-col">Privileged EXEC</td><td>كل البورتات المحظورة.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر التوجيه</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip route</td><td class="mode-col">Privileged EXEC</td><td>جدول التوجيه IPv4 الكامل.</td></tr>
        <tr><td class="cmd-col">show ip route static</td><td class="mode-col">Privileged EXEC</td><td>المسارات الثابتة فقط.</td></tr>
        <tr><td class="cmd-col">show ip route connected</td><td class="mode-col">Privileged EXEC</td><td>المسارات المتصلة مباشرة.</td></tr>
        <tr><td class="cmd-col">show ip route ospf|eigrp|bgp|rip</td><td class="mode-col">Privileged EXEC</td><td>المسارات من بروتوكول محدد.</td></tr>
        <tr><td class="cmd-col">show ip route &lt;network&gt;</td><td class="mode-col">Privileged EXEC</td><td>تفاصيل مسار محدد.</td></tr>
        <tr><td class="cmd-col">show ip route &lt;ip-addr&gt;</td><td class="mode-col">Privileged EXEC</td><td>المسار المستخدم للوصول إلى IP محدد.</td></tr>
        <tr><td class="cmd-col">show ip route summary</td><td class="mode-col">Privileged EXEC</td><td>ملخص إحصائي للجدول.</td></tr>
        <tr><td class="cmd-col">show ipv6 route</td><td class="mode-col">Privileged EXEC</td><td>جدول التوجيه IPv6.</td></tr>
        <tr><td class="cmd-col">show ip protocols</td><td class="mode-col">Privileged EXEC</td><td>كل بروتوكولات التوجيه المفعّلة وإعداداتها.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر Ping &amp; Traceroute</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الأمر</th>
            <th style="width: 15%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 15%;">مثال</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">ping &lt;ip&gt;</td>
            <td class="mode-col">User/Privileged</td>
            <td>إرسال 5 ICMP Echo Requests. <code class="inline">!</code> = نجاح، <code class="inline">.</code> = timeout، <code class="inline">U</code> = unreachable، <code class="inline">M</code> = MTU.</td>
            <td class="example-col">ping 8.8.8.8</td>
        </tr>
        <tr>
            <td class="cmd-col">ping &lt;ip&gt; source &lt;src&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>تحديد source IP. مفيد لتشخيص مسارات.</td>
            <td class="example-col">ping 8.8.8.8 source loopback0</td>
        </tr>
        <tr>
            <td class="cmd-col">ping &lt;ip&gt; repeat &lt;n&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عدد محدد من الحزم بدلاً من 5.</td>
            <td class="example-col">ping 8.8.8.8 repeat 100</td>
        </tr>
        <tr>
            <td class="cmd-col">ping &lt;ip&gt; size &lt;bytes&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>ضبط حجم الحزمة.</td>
            <td class="example-col">ping 8.8.8.8 size 1500 df-bit</td>
        </tr>
        <tr>
            <td class="cmd-col">traceroute &lt;ip&gt;</td>
            <td class="mode-col">User/Privileged</td>
            <td>تتبع المسار هوب بهوب. يستعمل UDPProbe بورت عالٍ (33434+) أو ICMP.</td>
            <td class="example-col">traceroute 8.8.8.8</td>
        </tr>
        <tr>
            <td class="cmd-col">traceroute &lt;ip&gt; source &lt;src&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>تحديد source IP.</td>
            <td class="example-col">traceroute 8.8.8.8 source lo0</td>
        </tr>
        <tr>
            <td class="cmd-col">traceroute &lt;ip&gt; probe &lt;n&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عدد probes لكل هوب (الافتراضي 3).</td>
            <td class="example-col">traceroute 8.8.8.8 probe 5</td>
        </tr>
        <tr>
            <td class="cmd-col">traceroute &lt;ip&gt; numeric</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عدم محاولة حلّ DNS للأسماء (أسرع).</td>
            <td class="example-col">traceroute 8.8.8.8 numeric</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر Debug</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">debug ip icmp</td><td class="mode-col">Privileged EXEC</td><td>عرض كل رسائل ICMP المرسلة والمستلمة على الجهاز.</td></tr>
        <tr><td class="cmd-col">debug ip packet [detail]</td><td class="mode-col">Privileged EXEC</td><td>عرض كل حزمة IP. <strong>خطر على الإنتاج!</strong> استخدم مع ACL لتقليل الإخراج.</td></tr>
        <tr><td class="cmd-col">debug ip routing</td><td class="mode-col">Privileged EXEC</td><td>عرض تغيرات جدول التوجيه.</td></tr>
        <tr><td class="cmd-col">debug ip ospf hello</td><td class="mode-col">Privileged EXEC</td><td>عرض OSPF Hellos.</td></tr>
        <tr><td class="cmd-col">debug ip ospf adj</td><td class="mode-col">Privileged EXEC</td><td>عرض عملية تكوين OSPF adjacency.</td></tr>
        <tr><td class="cmd-col">debug eigrp packets</td><td class="mode-col">Privileged EXEC</td><td>عرض حزم EIGRP.</td></tr>
        <tr><td class="cmd-col">debug ip bgp</td><td class="mode-col">Privileged EXEC</td><td>عرض نشاط BGP.</td></tr>
        <tr><td class="cmd-col">debug ip nat</td><td class="mode-col">Privileged EXEC</td><td>عرض كل ترجمة NAT.</td></tr>
        <tr><td class="cmd-col">debug arp</td><td class="mode-col">Privileged EXEC</td><td>عرض نشاط ARP.</td></tr>
        <tr><td class="cmd-col">debug spanning-tree events</td><td class="mode-col">Privileged EXEC</td><td>عرض أحداث STP.</td></tr>
        <tr><td class="cmd-col">debug ip http</td><td class="mode-col">Privileged EXEC</td><td>عرض نشاط HTTP server على الجهاز.</td></tr>
        <tr><td class="cmd-col">undebug all / u all</td><td class="mode-col">Privileged EXEC</td><td><strong>تعطيل كل debug</strong>. حيلة ذهبية عند فيضان الإخراج!</td></tr>
        <tr><td class="cmd-col">no debug all</td><td class="mode-col">Privileged EXEC</td><td>نفس <code class="inline">undebug all</code>.</td></tr>
        <tr><td class="cmd-col">terminal monitor</td><td class="mode-col">User EXEC (VTY)</td><td>عرض رسائل debug و syslog على جلسة VTY الحالية.</td></tr>
        <tr><td class="cmd-col">terminal no monitor</td><td class="mode-col">User EXEC</td><td>إيقاف عرض رسائل على الجلسة.</td></tr>
    </tbody>
</table>

<div class="warn-box">
    <div class="warn-box-title">تحذير خطور - Debug على الإنتاج</div>
    <div class="warn-box-body">
        أوامر <code class="inline">debug</code> قد تسبب load هائل على CPU وتوقف الجهاز! في الإنتاج: (1) استخدم دائماً <code class="inline">terminal monitor</code> على VTY لترى الإخراج. (2) قيّد <code class="inline">debug ip packet</code> بـ ACL: <code class="inline">debug ip packet detail 100</code> حيث ACL 100 يصف الحركة المهتم بها. (3) فعّل <code class="inline">logging buffered debugging</code> ليُحفظ بدل عرضه فوراً. (4) إذا حدث فيضان، اضغط فوراً <code class="inline">Ctrl+Shift+6</code> ثم نفّذ <code class="inline">u all</code> لتعطيل كل debug.
    </div>
</div>


<!-- ============ SECTION 24: LAB SCENARIOS ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 24</span>
    <div class="chapter-title">Lab Scenarios - سيناريوهات عملية</div>
    <div class="chapter-title-en">Step-by-Step Practical Topologies</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    ست سيناريوهات عملية لتطبيق الأوامر في سياق واقعي. كل سيناريو يحوي طوبولوجيا، خطوات إعداد متسلسلة، أوامر تحقق، وأخطاء شائعة. ينصح بتطبيق كل سيناريو على Packet Tracer أو GNS3 أو EVE-NG بعد قراءة الشرح النظري لترسيخ المفاهيم.
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 1: إعداد أولي كامل لراوتر + تأمين SSH</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> راوتر واحد (R1) متصل بـ PC عبر كابل console (للإعداد الأولي) ومنفذ LAN (G0/0).<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">ادخل إلى وضع الإعداد عبر console وغيّر اسم الجهاز: <code class="inline">enable</code> → <code class="inline">configure terminal</code> → <code class="inline">hostname Cairo-R01</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">ضبط الـ hostname-domain و توليد RSA keys: <code class="inline">ip domain-name cairo.local</code> ثم <code class="inline">crypto key generate rsa modulus 2048</code></div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">إنشاء حساب admin: <code class="inline">username admin privilege 15 algorithm-type scrypt secret S3cr3t!2026</code></div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">ضبط enable secret: <code class="inline">enable algorithm-type scrypt secret En@ble!S3cr3t</code></div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">تفعيل SSHv2: <code class="inline">ip ssh version 2</code></div></div>
        <div class="lab-step"><div class="lab-step-num">6</div><div class="lab-step-content">ضبط VTY للسماح بـ SSH فقط: <code class="inline">line vty 0 15</code> → <code class="inline">login local</code> → <code class="inline">transport input ssh</code></div></div>
        <div class="lab-step"><div class="lab-step-num">7</div><div class="lab-step-content">ضبط الواجهة: <code class="inline">interface g0/0</code> → <code class="inline">ip address 192.168.1.1 255.255.255.0</code> → <code class="inline">no shutdown</code></div></div>
        <div class="lab-step"><div class="lab-step-num">8</div><div class="lab-step-content">حفظ الإعداد: <code class="inline">end</code> → <code class="inline">copy run start</code></div></div>
        <div class="lab-step"><div class="lab-step-num">9</div><div class="lab-step-content">التحقق: من PC، شغّل <code class="inline">ssh -l admin 192.168.1.1</code>. على الراوتر <code class="inline">show ip ssh</code> و <code class="inline">show ssh</code></div></div>
    </div>
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 2: VLANs &amp; Trunking بين سويتشين</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> SW1 و SW2 متصلين عبر Trunk (G0/1-G0/1). PC1 على SW1 في VLAN 10، PC2 على SW2 في VLAN 20.<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">على SW1: أنشئ VLANs: <code class="inline">vlan 10</code> → <code class="inline">name SALES</code>، <code class="inline">vlan 20</code> → <code class="inline">name IT</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">اضبط بورت PC1: <code class="inline">interface fa0/5</code> → <code class="inline">switchport mode access</code> → <code class="inline">switchport access vlan 10</code> → <code class="inline">spanning-tree portfast</code></div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">اضبط Trunk على G0/1: <code class="inline">switchport trunk encapsulation dot1q</code> → <code class="inline">switchport mode trunk</code> → <code class="inline">switchport trunk allowed vlan 10,20</code> → <code class="inline">switchport nonegotiate</code></div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">على SW2: كرر الخطوات 1-3 (نفس VLANs والـ trunk)</div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">اضبط بورت PC2 على SW2 في VLAN 20: <code class="inline">switchport access vlan 20</code></div></div>
        <div class="lab-step"><div class="lab-step-num">6</div><div class="lab-step-content">التحقق: <code class="inline">show vlan brief</code> و <code class="inline">show interfaces trunk</code> على السويتشين</div></div>
        <div class="lab-step"><div class="lab-step-num">7</div><div class="lab-step-content">لاحظ: PC1 و PC2 لا يستطيعان ping بعضهما لأنهما في VLANs مختلفة بدون routing</div></div>
    </div>
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 3: OSPF Single-Area بين راوترين</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> R1 و R2 متصلين عبر WAN (10.0.0.0/30). كل راوتر له شبكة LAN خلفه (192.168.1.0/24 على R1، 192.168.2.0/24 على R2).<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">على R1: اضبط الواجهات: <code class="inline">interface g0/0</code> → <code class="inline">ip address 192.168.1.1 255.255.255.0</code> → <code class="inline">no shutdown</code>، <code class="inline">interface s0/0/0</code> → <code class="inline">ip address 10.0.0.1 255.255.255.252</code> → <code class="inline">no shutdown</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">على R2: نفس الشيء لكن بـ IPs مختلفة: LAN 192.168.2.1/24، WAN 10.0.0.2/30</div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">على R1: فعّل OSPF: <code class="inline">router ospf 1</code> → <code class="inline">router-id 1.1.1.1</code> → <code class="inline">network 192.168.1.0 0.0.0.255 area 0</code> → <code class="inline">network 10.0.0.0 0.0.0.3 area 0</code> → <code class="inline">passive-interface g0/0</code></div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">على R2: نفس الشيء مع router-id 2.2.2.2 و شبكات R2</div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">التحقق: <code class="inline">show ip ospf neighbor</code> (يجب أن تري R2 كـ FULL) و <code class="inline">show ip route ospf</code> (يجب أن تري 192.168.2.0/24)</div></div>
        <div class="lab-step"><div class="lab-step-num">6</div><div class="lab-step-content">اختبر: من PC1 (192.168.1.10) ping PC2 (192.168.2.10). يجب أن تنجح.</div></div>
    </div>
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 4: NAT Overload (PAT) للوصول للإنترنت</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> R1 له واجهة inside (G0/0) موصولة بشبكة 192.168.1.0/24 وواجهة outside (G0/1) موصولة بـ ISP (203.0.113.2/30). المضيفون في inside يحتاجون للوصول للإنترنت.<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">اضبط الواجهات: <code class="inline">interface g0/0</code> → <code class="inline">ip address 192.168.1.1 255.255.255.0</code> → <code class="inline">ip nat inside</code> → <code class="inline">no shutdown</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">واجهة outside: <code class="inline">interface g0/1</code> → <code class="inline">ip address 203.0.113.2 255.255.255.252</code> → <code class="inline">ip nat outside</code> → <code class="inline">no shutdown</code></div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">أنشئ ACL تصف الحركة الداخلية: <code class="inline">access-list 1 permit 192.168.1.0 0.0.0.255</code></div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">فعّل PAT: <code class="inline">ip nat inside source list 1 interface g0/1 overload</code></div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">أضف default route إلى ISP: <code class="inline">ip route 0.0.0.0 0.0.0.0 203.0.113.1</code></div></div>
        <div class="lab-step"><div class="lab-step-num">6</div><div class="lab-step-content">التحقق: من PC، ping 8.8.8.8. على R1: <code class="inline">show ip nat translations</code> (ترى entries) و <code class="inline">show ip nat statistics</code></div></div>
    </div>
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 5: HSRP بين راوترين</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> R1 و R2 على نفس شبكة LAN (192.168.1.0/24). R1 IP 192.168.1.2، R2 IP 192.168.1.3. الـ gateway الافتراضي للمضيفين هو 192.168.1.254 (virtual).<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">على R1 (Active): <code class="inline">interface g0/0</code> → <code class="inline">ip address 192.168.1.2 255.255.255.0</code> → <code class="inline">standby 1 ip 192.168.1.254</code> → <code class="inline">standby 1 priority 110</code> → <code class="inline">standby 1 preempt</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">على R2 (Standby): <code class="inline">interface g0/0</code> → <code class="inline">ip address 192.168.1.3 255.255.255.0</code> → <code class="inline">standby 1 ip 192.168.1.254</code> → <code class="inline">standby 1 priority 100</code> → <code class="inline">standby 1 preempt</code></div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">التحقق: <code class="inline">show standby brief</code> على R1 يظهر Active، على R2 يظهر Standby</div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">اختبار الفشل: افصل كابل R1. خلال ثوانٍ، يجب أن يصبح R2 Active تلقائياً.</div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">أعد ربط R1. خلال فترة preempt، يستعيد R1 دور Active.</div></div>
    </div>
</div>

<div class="lab-scenario">
    <div class="lab-scenario-header">Lab 6: ACL لمنع شبكة محددة</div>
    <div class="lab-scenario-body">
        <strong>الطوبولوجيا:</strong> R1 موصول بشبكة 192.168.1.0/24 (LAN) و ISP عبر WAN. تريد السماح لكل الحركة خارجية ما عدا شبكة 192.168.1.50 التي تريد منعها من الوصول للإنترنت.<br><br>
        <div class="lab-step"><div class="lab-step-num">1</div><div class="lab-step-content">أنشئ named ACL: <code class="inline">ip access-list extended BLOCK-ONE</code></div></div>
        <div class="lab-step"><div class="lab-step-num">2</div><div class="lab-step-content">أضف قاعدة deny: <code class="inline">10 deny ip host 192.168.1.50 any</code></div></div>
        <div class="lab-step"><div class="lab-step-num">3</div><div class="lab-step-content">أضف قاعدة permit: <code class="inline">20 permit ip any any</code></div></div>
        <div class="lab-step"><div class="lab-step-num">4</div><div class="lab-step-content">طبّق ACL على الواجهة outside outbound: <code class="inline">interface g0/1</code> → <code class="inline">ip access-group BLOCK-ONE out</code></div></div>
        <div class="lab-step"><div class="lab-step-num">5</div><div class="lab-step-content">التحقق: من 192.168.1.50 ping 8.8.8.8 (يفشل). من 192.168.1.10 ping 8.8.8.8 (ينجح).</div></div>
        <div class="lab-step"><div class="lab-step-num">6</div><div class="lab-step-content">عرض عدادات التطابق: <code class="inline">show access-lists BLOCK-ONE</code></div></div>
    </div>
</div>

"""
