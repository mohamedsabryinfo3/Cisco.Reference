# -*- coding: utf-8 -*-
"""Part 03: Section 5 - Interfaces & IP + Section 6 - VLANs & Trunking + Section 7 - VTP & EtherChannel"""

SECTIONS_03 = """

<!-- ============ SECTION 5: INTERFACES & IP ADDRESSING ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 05</span>
    <div class="chapter-title">إعداد الواجهات وعناوين IP</div>
    <div class="chapter-title-en">Interfaces &amp; IP Addressing</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    الواجهات (Interfaces) هي المنافذ الفيزيائية أو الافتراضية التي يتصل من خلالها الجهاز بالشبكة. إعدادها بشكل صحيح يشمل تعيين عنوان IP (أو IPv6)، تفعيلها بـ <code class="inline">no shutdown</code>، وضبط المعاملات الفيزيائية مثل السرعة وضغط الإرسال (Speed/Duplex) في الواجهات النحاسية. كل واجهة لها اسم بنوعها ورقمها مثل <code class="inline">GigabitEthernet0/0</code> أو <code class="inline">FastEthernet0/1</code>، وتختلف تسميتها حسب نوع الجهاز وعدد منافذه.
</div>

<div class="section-title">أوامر إعداد الواجهة الأساسية</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 30%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 18%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">interface &lt;type&gt; &lt;number&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>الدخول إلى وضع إعداد واجهة محددة. الأنواع الشائعة: <code class="inline">GigabitEthernet</code>، <code class="inline">FastEthernet</code>، <code class="inline">Serial</code>، <code class="inline">Loopback</code>، <code class="inline">VLAN</code> (سويتش فقط)، <code class="inline">Tunnel</code>، <code class="inline">Port-channel</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">interface range &lt;range&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إعداد عدة واجهات دفعة واحدة. <code class="inline">interface range gi0/1 - 4</code>. يمكن استخدام الفاصلة للواجهات غير المتتالية: <code class="inline">interface range gi0/1, gi0/3</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">ip address &lt;ip&gt; &lt;mask&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين عنوان IPv4 وقناع الشبكة للواجهة. القناع بصيغة عشرية: <code class="inline">255.255.255.0</code> أو CIDR مختصرة <code class="inline">/24</code> (في بعض إصدارات IOS).</td>
            <td class="no-col">no ip address</td>
        </tr>
        <tr>
            <td class="cmd-col">ip address &lt;ip&gt; &lt;mask&gt; secondary</td>
            <td class="mode-col">Interface Config</td>
            <td>إضافة عنوان IP ثانوي على نفس الواجهة (Secondary IP). نادراً ما يُستخدم اليوم، شائع في الانتقال من نطاق إلى آخر.</td>
            <td class="no-col">no ip address &lt;ip&gt; &lt;mask&gt; secondary</td>
        </tr>
        <tr>
            <td class="cmd-col">no shutdown</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل الواجهة (رفعها). الواجهات تكون administratively down افتراضياً. <strong>أكثر أمر يُنسى!</strong></td>
            <td class="no-col">shutdown</td>
        </tr>
        <tr>
            <td class="cmd-col">description &lt;text&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>وصف نصي للواجهة. يظهر في <code class="inline">show interfaces</code> و <code class="inline">show running-config</code>. ممتاز للتوثيق المباشر.</td>
            <td class="no-col">no description</td>
        </tr>
        <tr>
            <td class="cmd-col">speed &lt;10/100/1000/auto&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط سرعة الواجهة. الافتراضي auto. عند ضبطها يدوياً يجب ضبط duplex يدوياً أيضاً لتجنب عدم تطابق duplex.</td>
            <td class="no-col">no speed</td>
        </tr>
        <tr>
            <td class="cmd-col">duplex &lt;auto/full/half&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط وضع الـ duplex. <code class="inline">full</code> = إرسال واستقبال متزامن. <code class="inline">half</code> = إرسال أو استقبال في وقت واحد فقط (قديم).</td>
            <td class="no-col">no duplex</td>
        </tr>
        <tr>
            <td class="cmd-col">mtu &lt;bytes&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط وحدة الإرسال القصوى (Maximum Transmission Unit). الافتراضي 1500 بايت لإيثرنت. رفعه يدعم Jumbo Frames.</td>
            <td class="no-col">no mtu</td>
        </tr>
        <tr>
            <td class="cmd-col">bandwidth &lt;kbps&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط قيمة العرض الترددي للواجهة (تستخدم في حسابات OSPF/EIGRP). <strong>لا يغيّر السرعة الفيزيائية الفعلية!</strong></td>
            <td class="no-col">no bandwidth</td>
        </tr>
        <tr>
            <td class="cmd-col">delay &lt;usec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط قيمة التأخير بالميكروثانية. تؤثر على حسابات EIGRP metric. <strong>لا يضيف تأخيراً فيزيائياً!</strong></td>
            <td class="no-col">no delay</td>
        </tr>
        <tr>
            <td class="cmd-col">arp timeout &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط مدة بقاء مدخلات ARP (الافتراضي 14400 ثانية = 4 ساعات).</td>
            <td class="no-col">no arp timeout</td>
        </tr>
        <tr>
            <td class="cmd-col">no ip proxy-arp</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل proxy-arp (موصى به أمنياً - يمكن استغلال proxy-arp في هجمات MitM).</td>
            <td class="no-col">ip proxy-arp</td>
        </tr>
        <tr>
            <td class="cmd-col">no ip redirects</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل ICMP redirects (موصى به أمنياً).</td>
            <td class="no-col">ip redirects</td>
        </tr>
        <tr>
            <td class="cmd-col">no ip unreachables</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل ICMP unreachable (يمنع كشف الشبكة من قبل المهاجم).</td>
            <td class="no-col">ip unreachables</td>
        </tr>
    </tbody>
</table>

<div class="section-title">إعداد IPv6 على الواجهات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 33%;">الشرح</th>
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
            <td>تفعيل IPv6 على الواجهة وتوليد link-local address تلقائياً (fe80::...).</td>
            <td class="no-col">no ipv6 enable</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address &lt;ipv6&gt;/&lt;prefix&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين عنوان IPv6 ثابت. مثل <code class="inline">ipv6 address 2001:db8:1::1/64</code>.</td>
            <td class="no-col">no ipv6 address</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address &lt;prefix&gt;/&lt;len&gt; eui-64</td>
            <td class="mode-col">Interface Config</td>
            <td>توليد IPv6 باستخدام EUI-64 من MAC address. مثل <code class="inline">ipv6 address 2001:db8:1::/64 eui-64</code>.</td>
            <td class="no-col">no ipv6 address &lt;prefix&gt;/&lt;len&gt; eui-64</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address autoconfig</td>
            <td class="mode-col">Interface Config</td>
            <td>الحصول على IPv6 تلقائياً عبر SLAAC (StateLess Address AutoConfig) من رسائل RA.</td>
            <td class="no-col">no ipv6 address autoconfig</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 address dhcp</td>
            <td class="mode-col">Interface Config</td>
            <td>الحصول على IPv6 عبر DHCPv6.</td>
            <td class="no-col">no ipv6 address dhcp</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 nd other-config-flag</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط علم O في رسائل RA ليطلب من المضيفين الحصول على إعدادت أخرى (DNS) عبر DHCPv6.</td>
            <td class="no-col">no ipv6 nd other-config-flag</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 nd managed-config-flag</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط علم M في RA ليطلب من المضيفين الحصول على IPv6 كاملاً عبر DHCPv6 (stateful).</td>
            <td class="no-col">no ipv6 nd managed-config-flag</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 traffic-filter &lt;acl&gt; in|out</td>
            <td class="mode-col">Interface Config</td>
            <td>تطبيق ACL على حركة IPv6 (في/خارج الواجهة).</td>
            <td class="no-col">no ipv6 traffic-filter</td>
        </tr>
    </tbody>
</table>

<div class="section-title">الواجهات الافتراضية (Loopback و Tunnel و Sub-if)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 32%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 36%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">interface loopback &lt;n&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء واجهة loopback افتراضية. لا تنزل أبداً ما لم تُعطّل يدوياً. تستخدم لـ router-id، إدارة الجهاز، و BGP update source.</td>
            <td class="no-col">no interface loopback &lt;n&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">interface tunnel &lt;n&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء واجهة tunnel. تستخدم لـ GRE، IPsec، إلخ. تحتاج ضبط <code class="inline">tunnel source</code> و <code class="inline">tunnel destination</code>.</td>
            <td class="no-col">no interface tunnel &lt;n&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">interface &lt;type&gt;&lt;num&gt;.&lt;sub-if&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء واجهة فرعية (sub-interface). مثل <code class="inline">interface gigabitEthernet0/0.10</code>. تستخدم في Router-on-a-Stick لـ inter-VLAN routing.</td>
            <td class="no-col">no interface &lt;type&gt;&lt;num&gt;.&lt;sub-if&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">encapsulation dot1Q &lt;vlan-id&gt; [native]</td>
            <td class="mode-col">Sub-Interface</td>
            <td>تحديد encapsulation بنمط 802.1Q و VLAN-id للواجهة الفرعية. <code class="inline">native</code> للـ native VLAN (untagged).</td>
            <td class="no-col">no encapsulation dot1Q</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض حالة الواجهات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 15%;">الوضع</th>
            <th style="width: 47%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip interface brief</td><td class="mode-col">Privileged EXEC</td><td>عرض كل الواجهات وعناوينها وحالتها (up/down) في جدول مختصر. <strong>أكثر أمر استخداماً!</strong></td></tr>
        <tr><td class="cmd-col">show ipv6 interface brief</td><td class="mode-col">Privileged EXEC</td><td>نفس السابق لكن لعناوين IPv6.</td></tr>
        <tr><td class="cmd-col">show interfaces</td><td class="mode-col">Privileged EXEC</td><td>عرض كل التفاصيل: الحالة، IP، MAC، إحصائيات الإرسال والاستقبال، أخطاء، MTU.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل واجهة محددة فقط.</td></tr>
        <tr><td class="cmd-col">show interfaces description</td><td class="mode-col">Privileged EXEC</td><td>عرض كل الواجهات مع أوصافها وحالتها في جدول.</td></tr>
        <tr><td class="cmd-col">show interfaces status</td><td class="mode-col">Privileged EXEC (Switch)</td><td>عرض حالة بورتات السويتش: السرعة، الـ duplex، الـ VLAN، نوع الاتصال.</td></tr>
        <tr><td class="cmd-col">show ip interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض إعدادات IP على واجهة: proxy-arp، redirects، access-class، إلخ.</td></tr>
        <tr><td class="cmd-col">show controllers &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض نوع الكابل المتصل (DTE/DCE) في الواجهات التسلسلية. مهم لمعرفة من يوفر إشارة clocking.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد واجهة راوتر بـ IPv4 و IPv6</div>
<div class="code-block">
Router(config)# <span class="prompt">interface gigabitEthernet0/0/0</span>
Router(config-if)# <span class="prompt">description WAN-Link-to-ISP</span>
Router(config-if)# <span class="prompt">ip address 203.0.113.2 255.255.255.252</span>
Router(config-if)# <span class="prompt">no ip proxy-arp</span>
Router(config-if)# <span class="prompt">no ip redirects</span>
Router(config-if)# <span class="prompt">no ip unreachables</span>
Router(config-if)# <span class="prompt">ipv6 enable</span>
Router(config-if)# <span class="prompt">ipv6 address 2001:db8:acad::2/64</span>
Router(config-if)# <span class="prompt">no shutdown</span>
Router(config-if)# <span class="prompt">exit</span>
Router(config)# <span class="prompt">ipv6 unicast-routing</span>
</div>

<div class="code-block-title">مثال 5.2: Router-on-a-Stick (Inter-VLAN Routing)</div>
<div class="code-block">
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">no shutdown</span>          <span class="comment">! الواجهة الفيزيائية تظل up دائماً</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0.10</span>
Router(config-subif)# <span class="prompt">encapsulation dot1Q 10</span>
Router(config-subif)# <span class="prompt">ip address 192.168.10.1 255.255.255.0</span>
Router(config-subif)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0.20</span>
Router(config-subif)# <span class="prompt">encapsulation dot1Q 20</span>
Router(config-subif)# <span class="prompt">ip address 192.168.20.1 255.255.255.0</span>
Router(config-subif)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0.99</span>
Router(config-subif)# <span class="prompt">encapsulation dot1Q 99 native</span>
Router(config-subif)# <span class="prompt">ip address 192.168.99.1 255.255.255.0</span>
Router(config-subif)# <span class="prompt">exit</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للاب</div>
    <div class="tip-box-body">
        عند ضبط Router-on-a-Stick، يجب أن تكون الواجهة الفيزيائية (مثل <code class="inline">gigabitEthernet0/0</code>) مرفوعة (<code class="inline">no shutdown</code>) قبل ضبط أي sub-if. لا تضع IP على الواجهة الفيزيائية نفسها، بل على كل sub-if. وفي السويتش المتصل، اجعل البورت trunk مع <code class="inline">switchport trunk encapsulation dot1q</code> و <code class="inline">switchport mode trunk</code>.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">خطأ شائع قاتل!</div>
    <div class="warn-box-body">
        نسيان <code class="inline">no shutdown</code> على الواجهة بعد ضبط IP هو الخطأ الأول في كل لاب CCNA تقريباً. الواجهة ستبقى <code class="inline">administratively down</code> حتى لو ضبطت IP بشكل صحيح. تحقق دائماً بـ <code class="inline">show ip interface brief</code> وابحث عن <code class="inline">up/up</code> في عمود الحالة. كذلك في sub-interfaces، تأكد أن الواجهة الفيزيائية <code class="inline">up</code> قبل ضبط الإعداد الفرعي.
    </div>
</div>


<!-- ============ SECTION 6: VLANs & TRUNKING ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 06</span>
    <div class="chapter-title">أساسيات السويتش - VLANs &amp; Trunking</div>
    <div class="chapter-title-en">VLANs, Trunking &amp; DTP</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    الـ VLANs (Virtual LANs) هي تقسيم منطقي للشبكة على نفس البنية التحتية الفيزيائية. كل VLAN يمثل مجال بث منفصل (Broadcast Domain)، فلا تمرر إطارات البث بينها إلا عبر راوتر (Inter-VLAN Routing). تعتمد VLANs على معيار IEEE 802.1Q لإضافة تاج (Tag) لكل إطار يحدد VLAN المصدر. أنواع المنافذ في السويتش: <strong>Access Port</strong> (يحوي إطارات VLAN واحد فقط، بدون تاج)، <strong>Trunk Port</strong> (يحوي إطارات عدة VLANs مع تاج 802.1Q)، <strong>Dynamic Port</strong> (يتفاوض على النوع عبر DTP).
</div>

<div class="section-title">أوامر إنشاء وإعداد VLAN</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 32%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 16%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">vlan &lt;id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء VLAN معرّف بـ ID (1-4094). ID 1 محجوز (default)، 1002-1005 محجوزة لـ FDDI/Token Ring، 1006-4094 هي extended VLAN.</td>
            <td class="no-col">no vlan &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">vlan &lt;id&gt;-&lt;id2&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عدة VLANs مرة واحدة (نطاق).</td>
            <td class="no-col">no vlan &lt;id&gt;-&lt;id2&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">name &lt;name&gt;</td>
            <td class="mode-col">VLAN Config</td>
            <td>تعيين اسم للـ VLAN. يجب أن يكون ≤32 حرفاً ولا يحوي مسافات. <code class="inline">name SALES</code>.</td>
            <td class="no-col">no name</td>
        </tr>
        <tr>
            <td class="cmd-col">state active|suspended</td>
            <td class="mode-col">VLAN Config</td>
            <td>تفعيل أو تعليق VLAN. الـ suspended لا يمرر حركة لكن يحتفظ بتعريفه.</td>
            <td class="no-col">no state</td>
        </tr>
        <tr>
            <td class="cmd-col">interface vlan &lt;id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء واجهة SVI (Switch Virtual Interface). تتيح توجيه الحركة بين VLANs من داخل السويتش (Layer 3 switch).</td>
            <td class="no-col">no interface vlan &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip routing</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل التوجيه على سويتش Layer 3 (مطلوب قبل أي inter-VLAN routing على السويتش نفسه).</td>
            <td class="no-col">no ip routing</td>
        </tr>
        <tr>
            <td class="cmd-col">vtp mode transparent</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط VTP على وضع transparent (لا يرسل ولا يستقبل، فقط يحفظ محلياً - الأكثر أماناً).</td>
            <td class="no-col">no vtp mode</td>
        </tr>
    </tbody>
</table>

<div class="section-title">ضبط منفذ Access</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 33%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">switchport mode access</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط البورت كـ access port دائم (يحوي VLAN واحد).</td>
            <td class="no-col">no switchport mode</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport access vlan &lt;id&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين VLAN للـ access port. الافتراضي VLAN 1 (لا يوصى به).</td>
            <td class="no-col">no switchport access vlan</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport voice vlan &lt;id&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين Voice VLAN منفصل لحركة الصوت (VoIP). يضع تاج 802.1Q على إطارات الصوت فقط.</td>
            <td class="no-col">no switchport voice vlan</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport host</td>
            <td class="mode-col">Interface Config</td>
            <td>أمر مختصر يقوم بثلاثة أمور: ضبط البورت access، تعطيل PAgP، تعطيل 802.1x. مفيد للبورتات المتصلة بمضيف واحد.</td>
            <td class="no-col">no switchport host</td>
        </tr>
    </tbody>
</table>

<div class="section-title">ضبط منفذ Trunk (802.1Q)</div>
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
            <td class="cmd-col">switchport trunk encapsulation dot1q</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط encapsulation إلى 802.1Q (المعيار الحديث). بعض السويتشات تدعم أيضاً ISL القديم (محذور).</td>
            <td class="no-col">no switchport trunk encapsulation</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport mode trunk</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط البورت كـ trunk دائم. يتطلب ضبط encapsulation مسبقاً على بعض السويتشات.</td>
            <td class="no-col">no switchport mode</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk allowed vlan &lt;list&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تحديد VLANs المسموح مرورها عبر الـ trunk. <code class="inline">10,20,30</code> أو نطاق <code class="inline">10-30</code>. الافتراضي: كل VLANs (1-4094).</td>
            <td class="no-col">no switchport trunk allowed vlan</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk allowed vlan add &lt;list&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>إضافة VLANs للقائمة المسموحة بدون حذف القائمة الحالية.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk allowed vlan remove &lt;list&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>حذف VLANs من القائمة المسموحة.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk allowed vlan except &lt;list&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>السماح بكل VLANs ماعدا المذكورة.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk allowed vlan all</td>
            <td class="mode-col">Interface Config</td>
            <td>إعادة الافتراضي (السماح بكل VLANs).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport trunk native vlan &lt;id&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط Native VLAN. إطارات الـ Native VLAN لا تأخذ تاج 802.1Q (untagged). الافتراضي VLAN 1 (لا يوصى به أمنياً - استخدم VLAN unused مثل 999).</td>
            <td class="no-col">no switchport trunk native vlan</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport nonegotiate</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل DTP (Dynamic Trunking Protocol). <strong>موصى به بشدة</strong> - يمنع هجمات rogue switch.</td>
            <td class="no-col">no switchport nonegotiate</td>
        </tr>
    </tbody>
</table>

<div class="section-title">DTP (Dynamic Trunking Protocol) - أنواع الأوضاع</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">الوضع</th>
            <th style="width: 35%;">السلوك</th>
            <th style="width: 40%;">الملاحظة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">switchport mode access</code></td><td>يضع البورت access دائماً، يرسل DTP لتفاوض لكنه لا يقبل تحويله لـ trunk.</td><td>آمن للبورتات المتصلة بالمضيفين.</td></tr>
        <tr><td><code class="inline">switchport mode trunk</code></td><td>يضع البورت trunk دائماً، يرسل DTP لتفاوض مع الطرف الآخر.</td><td>الأكثر استخدمًا للـ trunks الدائمة.</td></tr>
        <tr><td><code class="inline">switchport mode dynamic desirable</code></td><td>يفاوض بنشاط ليصبح trunk. يرسل DTP frames.</td><td>قديم - لا يوصى به (هجوم VLAN hopping).</td></tr>
        <tr><td><code class="inline">switchport mode dynamic auto</code></td><td>لا يفاوض، لكنه يقبل أن يصبح trunk إن طلب الطرف الآخر.</td><td>قديم - لا يوصى به أمنياً.</td></tr>
        <tr><td><code class="inline">switchport nonegotiate</code></td><td>يعطّل DTP تماماً. يجب ضبط النوع يدوياً.</td><td>الأكثر أماناً - موصى به في الإنتاج.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض VLAN</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show vlan brief</td><td class="mode-col">Privileged EXEC</td><td>عرض كل VLANs مع أسمائها وحالتها والبورتات المنتمية إليها في جدول مختصر.</td></tr>
        <tr><td class="cmd-col">show vlan</td><td class="mode-col">Privileged EXEC</td><td>عرض كامل تفاصيل VLAN.</td></tr>
        <tr><td class="cmd-col">show vlan id &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل VLAN محدد.</td></tr>
        <tr><td class="cmd-col">show vlan name &lt;name&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل VLAN بالاسم.</td></tr>
        <tr><td class="cmd-col">show interfaces trunk</td><td class="mode-col">Privileged EXEC</td><td>عرض كل بورتات الـ trunk، والـ VLANs المسموحة على كل واحد.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt; trunk</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل trunk على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show interfaces &lt;iface&gt; switchport</td><td class="mode-col">Privileged EXEC</td><td>عرض الإعداد الإداري (admin mode) والتشغيلي (operational mode) للبورت.</td></tr>
        <tr><td class="cmd-col">show dtp interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض حالة DTP على واجهة محددة.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد VLANs و Trunk بين سويتشين</div>
<div class="code-block-title">المثال 6.1: VLAN + Trunk بين SW1 و SW2</div>
<div class="code-block">
<span class="comment">! على SW1</span>
SW1(config)# <span class="prompt">vlan 10</span>
SW1(config-vlan)# <span class="prompt">name SALES</span>
SW1(config-vlan)# <span class="prompt">exit</span>
SW1(config)# <span class="prompt">vlan 20</span>
SW1(config-vlan)# <span class="prompt">name IT</span>
SW1(config-vlan)# <span class="prompt">exit</span>
SW1(config)# <span class="prompt">vlan 99</span>
SW1(config-vlan)# <span class="prompt">name MGMT</span>
SW1(config-vlan)# <span class="prompt">exit</span>

<span class="comment">! ضبط بورت access</span>
SW1(config)# <span class="prompt">interface fastEthernet0/5</span>
SW1(config-if)# <span class="prompt">switchport mode access</span>
SW1(config-if)# <span class="prompt">switchport access vlan 10</span>
SW1(config-if)# <span class="prompt">spanning-tree portfast</span>
SW1(config-if)# <span class="prompt">exit</span>

<span class="comment">! ضبط trunk إلى SW2</span>
SW1(config)# <span class="prompt">interface gigabitEthernet0/1</span>
SW1(config-if)# <span class="prompt">switchport trunk encapsulation dot1q</span>
SW1(config-if)# <span class="prompt">switchport mode trunk</span>
SW1(config-if)# <span class="prompt">switchport trunk allowed vlan 10,20,99</span>
SW1(config-if)# <span class="prompt">switchport trunk native vlan 99</span>
SW1(config-if)# <span class="prompt">switchport nonegotiate</span>
SW1(config-if)# <span class="prompt">exit</span>

<span class="comment">! نفس الإعداد ينطبق على SW2</span>
</div>

<div class="warn-box">
    <div class="warn-box-title">هجوم VLAN Hopping - حذر!</div>
    <div class="warn-box-body">
        إذا أبقيت Native VLAN على 1 (الافتراضي)، يستطيع مهاجم إرسال إطار 802.1Q مزدوج (double-tagged) ليصل إلى VLAN لا ينتمي إليه. الحلول: (1) استخدم Native VLAN غير مستخدم (مثل 999) ولا تحوي أي مضيف، (2) عطّل DTP بـ <code class="inline">switchport nonegotiate</code> على كل trunks، (3) ضع بورتات المستخدمين بـ <code class="inline">switchport mode access</code> صريحاً ولا تتركها dynamic auto.
    </div>
</div>


<!-- ============ SECTION 7: VTP & ETHERCHANNEL ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 07</span>
    <div class="chapter-title">VTP و EtherChannel</div>
    <div class="chapter-title-en">VTP &amp; EtherChannel (LACP/PAgP)</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    <strong>VTP (VLAN Trunking Protocol)</strong> هو بروتوكول خاص بسيسكو يسمح بمزامنة إعدادات VLAN بين سويتشات على نفس VTP domain. أنواع أوضاع VTP أربعة: Server (إنشاء وحذف VLANs)، Client (يستقبل فقط)، Transparent (يحفظ محلياً ولا يتأثر)، Off (مثل Transparent لكنه لا يمرر VTP frames - الجديد في IOS 15+). <strong>EtherChannel</strong> هي تقنية تجميع عدة روابط فيزيائية في رابط منطقي واحد لزيادة العرض الترددي وتوفير التحميل (Load Balancing) والاحتياط (Redundancy). بروتوكولات التفاوض على EtherChannel نوعان: <strong>LACP</strong> (معيار IEEE 802.3ad) و <strong>PAgP</strong> (Cisco-Proprietary).
</div>

<div class="section-title">أوامر VTP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 32%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 16%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">vtp mode &lt;server|client|transparent|off&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط وضع VTP. الأكثر أماناً: <code class="inline">transparent</code> أو <code class="inline">off</code>.</td>
            <td class="no-col">no vtp mode</td>
        </tr>
        <tr>
            <td class="cmd-col">vtp domain &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط اسم نطاق VTP. كل السويتشات في نفس النطاق يجب أن تحوي نفس الاسم.</td>
            <td class="no-col">no vtp domain</td>
        </tr>
        <tr>
            <td class="cmd-col">vtp password &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط كلمة مرور لـ VTP. كلمة المرور يجب أن تتطابق عبر النطاق. مشفّرة بـ Type 7.</td>
            <td class="no-col">no vtp password</td>
        </tr>
        <tr>
            <td class="cmd-col">vtp version &lt;1|2|3&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط إصدار VTP. VTPv3 هو الأحدث ويدعم extended VLANs و неизвест-أنواع VLANs. VTPv2 الافتراضي.</td>
            <td class="no-col">no vtp version</td>
        </tr>
        <tr>
            <td class="cmd-col">vtp pruning</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل VTP Pruning: عدم إرسال حركة البث إلى سويتشات لا تحتوي بورتات في VLAN معين. يقلل من حركة البث على الـ trunks.</td>
            <td class="no-col">no vtp pruning</td>
        </tr>
        <tr>
            <td class="cmd-col">show vtp status</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض كل إعدادات VTP: الإصدار، الوضع، النطاق، عدد الإصدارات.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show vtp password</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض كلمة مرور VTP الحالية.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show vtp counters</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض إحصائيات حزم VTP المرسلة والمستلمة.</td>
            <td class="no-col">N/A</td>
        </tr>
    </tbody>
</table>

<div class="warn-box">
    <div class="warn-box-title">خطر VTP Server بـ revision number أعلى!</div>
    <div class="warn-box-body">
        خطأ VTP الكلاسيكي: عند إضافة سويتش جديد بإعداد factory (VTP server، revision=0) ثم ضبط نطاق VTP، إذا كانت لهذا السويتش revision number أعلى من السويتشات الأخرى (مثلاً بسبب تكوين سابق)، فإنه سيمحو كل VLANs على الشبكة! الحماية: (1) استخدم VTP transparent/off افتراضياً، (2) عند إضافة سويتش جديد، نفّذ <code class="inline">vtp mode transparent</code> قبل ضبط النطاق لتفادي هذا الخطأ، (3) أو استخدم VTPv3 الذي يحمي من هذا بـ <code class="inline">vtp primary</code>.
    </div>
</div>

<div class="section-title">أوامر EtherChannel (Layer 2)</div>
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
            <td class="cmd-col">channel-group &lt;1-6&gt; mode active</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل LACP بوضع active (يفاوض بنشاط). مجموعات 1-6 في السويتشات القديمة، 1-128 في الحديثة.</td>
            <td class="no-col">no channel-group</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-group &lt;n&gt; mode passive</td>
            <td class="mode-col">Interface Config</td>
            <td>LACP بوضع passive (لا يفاوض لكنه يقبل إن طلب الطرف الآخر).</td>
            <td class="no-col">no channel-group</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-group &lt;n&gt; mode desirable</td>
            <td class="mode-col">Interface Config</td>
            <td>PAgP بوضع desirable (يفاوض بنشاط - Cisco-Proprietary).</td>
            <td class="no-col">no channel-group</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-group &lt;n&gt; mode auto</td>
            <td class="mode-col">Interface Config</td>
            <td>PAgP بوضع auto (لا يفاوض لكن يقبل - Cisco-Proprietary).</td>
            <td class="no-col">no channel-group</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-group &lt;n&gt; mode on</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل EtherChannel بدون بروتوكول تفاوض (يدوي). كلا الطرفين يجب أن يضبطا <code class="inline">on</code>.</td>
            <td class="no-col">no channel-group</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-protocol lacp|pagp</td>
            <td class="mode-col">Interface Config</td>
            <td>تحديد البروتوكول المستخدم صراحةً (يستخدم بدلاً من mode). أكثر وضوحاً.</td>
            <td class="no-col">no channel-protocol</td>
        </tr>
        <tr>
            <td class="cmd-col">port-channel load-balance &lt;method&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط طريقة load balancing: <code class="inline">src-mac</code>، <code class="inline">dst-mac</code>، <code class="inline">src-dst-mac</code>، <code class="inline">src-ip</code>، <code class="inline">dst-ip</code>، <code class="inline">src-dst-ip</code>، إلخ.</td>
            <td class="no-col">no port-channel load-balance</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر EtherChannel (Layer 3)</div>
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
            <td class="cmd-col">interface port-channel &lt;n&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء واجهة Port-Channel منطقية. يمكن ضبط IP عليها إذا كانت Layer 3.</td>
            <td class="no-col">no interface port-channel &lt;n&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">no switchport</td>
            <td class="mode-col">Interface Config</td>
            <td>تحويل واجهة سويتش من Layer 2 إلى Layer 3 (راوتر). يسمح بضبط IP مباشرة.</td>
            <td class="no-col">switchport</td>
        </tr>
        <tr>
            <td class="cmd-col">channel-group &lt;n&gt; mode active</td>
            <td class="mode-col">Physical Interface</td>
            <td>إضافة الواجهة الفيزيائية إلى مجموعة port-channel (نفس الأمر Layer 2/3).</td>
            <td class="no-col">no channel-group</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض EtherChannel</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show etherchannel summary</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص كل مجموعات EtherChannel، الواجهات المنخرطة فيها وحالتها. الحرف <code class="inline">+</code> يعني port مفعّل.</td></tr>
        <tr><td class="cmd-col">show etherchannel &lt;n&gt; port-channel</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل port-channel محدد.</td></tr>
        <tr><td class="cmd-col">show etherchannel load-balance</td><td class="mode-col">Privileged EXEC</td><td>عرض طريقة load balancing الحالية.</td></tr>
        <tr><td class="cmd-col">show lacp neighbor</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران LACP.</td></tr>
        <tr><td class="cmd-col">show pagp neighbor</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران PAgP.</td></tr>
        <tr><td class="cmd-col">show interfaces port-channel &lt;n&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض حالة واجهة port-channel المنطقية.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: EtherChannel LACP بين سويتشين</div>
<div class="code-block">
<span class="comment">! على SW1</span>
SW1(config)# <span class="prompt">interface range gigabitEthernet0/1 - 2</span>
SW1(config-if-range)# <span class="prompt">switchport trunk encapsulation dot1q</span>
SW1(config-if-range)# <span class="prompt">switchport mode trunk</span>
SW1(config-if-range)# <span class="prompt">switchport trunk allowed vlan 10,20,99</span>
SW1(config-if-range)# <span class="prompt">channel-group 1 mode active</span>
SW1(config-if-range)# <span class="prompt">exit</span>
SW1(config)# <span class="prompt">port-channel load-balance src-dst-ip</span>

<span class="comment">! على SW2 - نفس الإعداد</span>
SW2(config)# <span class="prompt">interface range gigabitEthernet0/1 - 2</span>
SW2(config-if-range)# <span class="prompt">switchport trunk encapsulation dot1q</span>
SW2(config-if-range)# <span class="prompt">switchport mode trunk</span>
SW2(config-if-range)# <span class="prompt">switchport trunk allowed vlan 10,20,99</span>
SW2(config-if-range)# <span class="prompt">channel-group 1 mode passive</span>     <span class="comment">! passive على الطرف الآخر</span>
SW2(config-if-range)# <span class="prompt">exit</span>

<span class="comment">! تحقق</span>
SW1# <span class="prompt">show etherchannel summary</span>
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        ...
Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)       LACP        Gi0/1(P)   Gi0/2(P)
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة عملية لـ EtherChannel</div>
    <div class="tip-box-body">
        شروط نجاح EtherChannel: (1) كل البورتات المنخرطة يجب أن تكون لها نفس الإعدادات (Speed, Duplex, VLANs المسموحة، STP settings). (2) استخدم LACP في الإنتاج لأنه معيار IEEE، لا PAgP لأنه Cisco-Proprietary. (3) استخدم <code class="inline">active</code> على طرف و <code class="inline">passive</code> على الآخر (ولا تستخدم <code class="inline">passive</code> على الطرفين معاً فلن يتفاوضا). (4) يمكن تجميع 2-8 روابط نشطة في LACP.
    </div>
</div>

"""
