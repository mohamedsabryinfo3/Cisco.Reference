# -*- coding: utf-8 -*-
"""Part 05: Section 11 - Static & Default Routing"""

SECTIONS_05 = """

<!-- ============ SECTION 11: STATIC & DEFAULT ROUTING ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 11</span>
    <div class="chapter-title">التوجيه الثابت - Static &amp; Default Routing</div>
    <div class="chapter-title-en">Static &amp; Default Routing</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    التوجيه الثابت (Static Routing) هو إدخال مسارات في جدول التوجيه يدوياً بدلاً من الاعتماد على بروتوكولات ديناميكية مثل OSPF أو EIGRP. يستخدم التوجيه الثابت في حالات: (1) شبكات صغيرة جداً لا تستحق تعقيد بروتوكول ديناميكي، (2) ربط شبكة طرفية بـ ISP (الطرف الناخب default route)، (3) موازنة حمل أو احتياط مع مسار ديناميكي (floating static route). أنواع التوجيه الثابت ثلاثة: <strong>Direct Static</strong> (next-hop IP)، <strong>Directly Connected Static</strong> (exit-interface)، <strong>Fully Specified</strong> (next-hop + exit-interface). <strong>Default Route</strong> هو مسار ثابت خاص يطابق كل الوجهات غير الموجودة في الجدول، يستخدم للوصول للإنترنت.
</div>

<div class="section-title">أوامر التوجيه الثابت (IPv4)</div>
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
            <td class="cmd-col">ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop-ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت عبر عنوان القفزة التالية. مثلاً: <code class="inline">ip route 192.168.50.0 255.255.255.0 10.0.0.2</code>.</td>
            <td class="no-col">no ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop-ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip route &lt;network&gt; &lt;mask&gt; &lt;exit-interface&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت عبر واجهة الخروج. مثل <code class="inline">ip route 192.168.50.0 255.255.255.0 gigabitEthernet0/0</code>. يستعمل في وصلات point-to-point.</td>
            <td class="no-col">no ip route &lt;network&gt; &lt;mask&gt; &lt;exit-interface&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop-ip&gt; &lt;exit-interface&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت كامل التحديد (Fully Specified) - يحدد كلاً من next-hop و exit-interface. مطلوب في حالات معينة.</td>
            <td class="no-col">no ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop-ip&gt; &lt;exit-interface&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop&gt; &lt;AD&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط Administrative Distance (AD). الافتراضي 1. يستخدم لعمل floating static route (مسار احتياطي يتفعل عند فشل الأساسي).</td>
            <td class="no-col">no ip route &lt;network&gt; &lt;mask&gt; &lt;next-hop&gt; &lt;AD&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip route 0.0.0.0 0.0.0.0 &lt;next-hop&gt;</td>
            <td class="mode-col">Global Config</td>
            <td><strong>Default Route</strong> - مسار افتراضي يطابق كل الشبكات. <code class="inline">0.0.0.0 0.0.0.0</code> = القناع والمصدر كلاهما 0 (wildcard).</td>
            <td class="no-col">no ip route 0.0.0.0 0.0.0.0 &lt;next-hop&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip default-network &lt;network&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>طريقة قديمة لضبط default route. تُفضّل <code class="inline">ip route 0.0.0.0 0.0.0.0</code> بدلاً منها.</td>
            <td class="no-col">no ip default-network</td>
        </tr>
        <tr>
            <td class="cmd-col">ip classless</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل behaviour classless - يسمح بالبحث عن أطول تطابق حتى لو الشبكة مفصّلة. مفعّل افتراضياً في IOS 12+. ضروري للـ default route ليعمل.</td>
            <td class="no-col">no ip classless</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر التوجيه الثابت (IPv6)</div>
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
            <td class="cmd-col">ipv6 route &lt;network&gt;/&lt;prefix&gt; &lt;next-hop&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت IPv6. مثل <code class="inline">ipv6 route 2001:db8:50::/64 2001:db8:1::2</code>.</td>
            <td class="no-col">no ipv6 route &lt;network&gt;/&lt;prefix&gt; &lt;next-hop&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 route &lt;network&gt;/&lt;prefix&gt; &lt;exit-interface&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>توجيه ثابت IPv6 عبر واجهة الخروج.</td>
            <td class="no-col">no ipv6 route ...</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 route ::/0 &lt;next-hop&gt;</td>
            <td class="mode-col">Global Config</td>
            <td><strong>Default Route IPv6</strong> - <code class="inline">::/0</code> يطابق كل الشبكات.</td>
            <td class="no-col">no ipv6 route ::/0</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 unicast-routing</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل توجيه IPv6 على الجهاز (مطلوب قبل أي IPv6 routing).</td>
            <td class="no-col">no ipv6 unicast-routing</td>
        </tr>
    </tbody>
</table>

<div class="section-title">جدول Administrative Distances (AD)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">المصدر</th>
            <th style="width: 25%;">الرمز في الجدول</th>
            <th style="width: 15%;">AD</th>
            <th style="width: 25%;">الملاحظة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Connected Interface</td><td><code class="inline">C</code></td><td>0</td><td>الأعلى أولوية</td></tr>
        <tr><td>Static Route (with exit-interface)</td><td><code class="inline">S</code></td><td>0</td><td>يعامل كـ directly connected</td></tr>
        <tr><td>Static Route (with next-hop)</td><td><code class="inline">S</code></td><td>1</td><td>الافتراضي للـ static العادي</td></tr>
        <tr><td>EIGRP Summary</td><td><code class="inline">D EX</code></td><td>5</td><td>المسارات الملخصة من EIGRP</td></tr>
        <tr><td>eBGP (External BGP)</td><td><code class="inline">B</code></td><td>20</td><td>المسارات من AS خارجية</td></tr>
        <tr><td>EIGRP (Internal)</td><td><code class="inline">D</code></td><td>90</td><td>المسارات الداخلية EIGRP</td></tr>
        <tr><td>OSPF</td><td><code class="inline">O</code></td><td>110</td><td>البروتوكول الأكثر شعبية</td></tr>
        <tr><td>IS-IS</td><td><code class="inline">i L1/L2</code></td><td>115</td><td>ISP grade</td></tr>
        <tr><td>RIP</td><td><code class="inline">R</code></td><td>120</td><td>قديم</td></tr>
        <tr><td>EGP</td><td><code class="inline">E</code></td><td>140</td><td>قديم</td></tr>
        <tr><td>ODR</td><td><code class="inline">o</code></td><td>160</td><td>On Demand Routing</td></tr>
        <tr><td>EIGRP (External)</td><td><code class="inline">D EX</code></td><td>170</td><td>المسارات المستوردة من خارج EIGRP</td></tr>
        <tr><td>iBGP (Internal BGP)</td><td><code class="inline">B</code></td><td>200</td><td>المسارات من AS داخلية</td></tr>
        <tr><td>Unknown</td><td><code class="inline">?</code></td><td>255</td><td>لا يثق به أبداً</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض جدول التوجيه</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 42%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 41%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip route</td><td class="mode-col">Privileged EXEC</td><td>عرض جدول التوجيه IPv4 الكامل. أساسي للتشخيص.</td></tr>
        <tr><td class="cmd-col">show ip route static</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط المسارات الثابتة (S).</td></tr>
        <tr><td class="cmd-col">show ip route connected</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط المسارات المتصلة مباشرة (C).</td></tr>
        <tr><td class="cmd-col">show ip route ospf</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط مسارات OSPF (O).</td></tr>
        <tr><td class="cmd-col">show ip route eigrp</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط مسارات EIGRP (D).</td></tr>
        <tr><td class="cmd-col">show ip route bgp</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط مسارات BGP (B).</td></tr>
        <tr><td class="cmd-col">show ip route &lt;network&gt; &lt;mask&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل مسار محدد.</td></tr>
        <tr><td class="cmd-col">show ip route &lt;ip-addr&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض المسار المستخدم للوصول إلى IP محدد.</td></tr>
        <tr><td class="cmd-col">show ip route summary</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص إحصائي لجدول التوجيه.</td></tr>
        <tr><td class="cmd-col">show ip protocols</td><td class="mode-col">Privileged EXEC</td><td>عرض كل بروتوكولات التوجيه المفعّلة وإعداداتها.</td></tr>
        <tr><td class="cmd-col">show ipv6 route</td><td class="mode-col">Privileged EXEC</td><td>عرض جدول التوجيه IPv6.</td></tr>
        <tr><td class="cmd-col">show ip interface brief</td><td class="mode-col">Privileged EXEC</td><td>عرض حالة كل الواجهات - أساسي للتشخيص.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: Floating Static Route (مسار احتياطي)</div>
<div class="code-block">
<span class="comment">! المسار الأساسي عبر OSPF (AD = 110)</span>
<span class="comment">! المسار الاحتياطي ثابت بـ AD = 200 - لن يظهر ما دام OSPF يعمل</span>

Router(config)# <span class="prompt">ip route 192.168.50.0 255.255.255.0 10.0.0.2 200</span>   <span class="comment">! AD 200 = احتياطي</span>
Router(config)# <span class="prompt">router ospf 1</span>
Router(config-router)# <span class="prompt">network 192.168.50.0 0.0.0.255 area 0</span>
Router(config-router)# <span class="prompt">exit</span>

Router# <span class="prompt">show ip route 192.168.50.0</span>
Routing entry for 192.168.50.0/24
  Known via "ospf 1", distance 110, metric 65, type intra area
  <span class="comment">! OSPF مسيطر، المسار الثابت مخفي</span>
</div>

<div class="code-block-title">مثال 11.2: Default Route إلى ISP</div>
<div class="code-block">
Router(config)# <span class="prompt">ip route 0.0.0.0 0.0.0.0 203.0.113.1</span>      <span class="comment">! ISP Gateway</span>
Router(config)# <span class="prompt">ipv6 route ::/0 2001:db8:acad::1</span>
Router(config)# <span class="prompt">exit</span>

Router# <span class="prompt">show ip route static</span>
Gateway of last resort is 203.0.113.1 to network 0.0.0.0

S*   0.0.0.0/0 [1/0] via 203.0.113.1
</div>

<div class="info-box">
    <div class="info-box-title">فهم رمز S* في جدول التوجيه</div>
    <div class="info-box-body">
        الحرف <code class="inline">S*</code> معناه <strong>Static Default Candidate</strong> - المسار الافتراضي الثابت المرشّح للاستخدام. <code class="inline">*</code> تشير إلى candidate default. حين يصبح <code class="inline">Gateway of last resort</code> (يستخدم فعلياً للوصول إلى شبكات غير معروفة) يظهر قبله <code class="inline">+</code> أو مع <code class="inline">S*</code>. عند ورود حركة إلى عنوان IP غير معروف في الجدول، يرسلها الراوتر إلى هذا الـ Gateway.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">Recursive Routing Lookup - مشكلة شائعة</div>
    <div class="warn-box-body">
        عند استخدام <code class="inline">ip route 192.168.50.0 255.255.255.0 10.0.0.2</code> فقط (next-hop بدون exit-interface)، يقوم الراوتر بـ recursive lookup: يبحث عن كيفية الوصول إلى 10.0.0.2 أولاً ثم يقرر الواجهة. هذا يستهلك CPU أكثر لكنه أكثر مرونة (يصمد ضد تغير واجهة الفيزيائية). لتجنب recursive lookup استخدم <code class="inline">ip route ... &lt;exit-interface&gt;</code>، لكن انتبه أن هذا قد يسبب مشكلة ARP على وصلات broadcast (إيثرنت) - فيقوم الراوتر بـ ARP لكل عنوان وجهة، مما يستهلك ذاكرة. الأفضل في الإيثرنت: استخدام next-hop فقط. في الوصلات point-to-point (Serial): يمكن استخدام exit-interface فقط.
    </div>
</div>

<div class="section-title">بروتوكولات التوجيه الديناميكي - مقارنة</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 18%;">البروتوكول</th>
            <th style="width: 10%;">النوع</th>
            <th style="width: 17%;">AD</th>
            <th style="width: 20%;">Metric</th>
            <th style="width: 35%;">الملاحظة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>RIPv2</td><td>Distance-Vector</td><td>120</td><td>Hop count</td><td>قديم، حد أقصى 15 هوب. يدعم VLSM.</td></tr>
        <tr><td>EIGRP</td><td>Hybrid (Advanced DV)</td><td>90</td><td>Composite (BW+Delay)</td><td>أصلاً Cisco-Proprietary، الآن معيار مفتوح (RFC 7868).</td></tr>
        <tr><td>OSPF</td><td>Link-State</td><td>110</td><td>Cost (1/bandwidth)</td><td>المعيار المفتوح، يدعم Areas لتقسيم الـ AS.</td></tr>
        <tr><td>IS-IS</td><td>Link-State</td><td>115</td><td>Cost</td><td>شائع في ISPs، يعمل في Layer 2.5 (بين IP و Ethernet).</td></tr>
        <tr><td>BGP</td><td>Path-Vector</td><td>20 (eBGP) / 200 (iBGP)</td><td>Attributes (AS-path, etc.)</td><td>بروتوكول الإنترنت، يستعمل بين Autonomous Systems.</td></tr>
    </tbody>
</table>

<div class="section-title">قواعد اختيار المسار (Longest Prefix Match)</div>
<div class="body-text">
    عند وجود عدة مسارات لنفس الوجهة، يطبق الراوتر قواعد الترتيب التالية بالتسلسل: (1) <strong>Longest Prefix Match</strong>: يختار المسار بأطول قناع شبكة (الأكثر تحديداً). مثلاً، إن وُجد <code class="inline">10.0.0.0/8</code> و <code class="inline">10.1.1.0/24</code> لوجهة 10.1.1.5، يختار الثاني (أكثر تحديداً). (2) <strong>Administrative Distance</strong>: عند تعادل طول القناع، يختار المسار الأقل AD (الأكثر موثوقية). (3) <strong>Metric</strong>: عند تعادل الـ AD (مثلاً مساران من OSPF)، يختار الأقل metric. (4) <strong>Load Balancing</strong>: عند تعادل كل ما سبق، يقسّم الحركة بين المسارات (ECMP - Equal Cost Multi-Path).
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للمذاكرة</div>
    <div class="tip-box-body">
        احفظ جدول AD عن ظهر قلب! تأتي منه أسئلة في امتحان CCNA تتعلق بـ "أي مسار يختاره الراوتر بين OSPF و EIGRP و Static". القاعدة الذهبية: <code class="inline">Direct (0) &gt; Static (1) &gt; eBGP (20) &gt; EIGRP Internal (90) &gt; IGRP (100) &gt; OSPF (110) &gt; RIP (120) &gt; EIGRP External (170) &gt; iBGP (200)</code>. تذكّر: الـ AD لا يأتي في account إذا كان أحد المسارات <code class="inline">directly connected</code> - فهو دائماً الأقوى.
    </div>
</div>

"""
