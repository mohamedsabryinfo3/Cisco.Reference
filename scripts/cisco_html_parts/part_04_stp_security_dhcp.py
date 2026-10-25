# -*- coding: utf-8 -*-
"""Part 04: Section 8 - STP + Section 9 - Port Security + Section 10 - DHCP"""

SECTIONS_04 = """

<!-- ============ SECTION 8: SPANNING TREE PROTOCOL ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 08</span>
    <div class="chapter-title">Spanning Tree Protocol</div>
    <div class="chapter-title-en">STP, RSTP, PVST+ &amp; BPDU Guard</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    بروتوكول الشجرة المتدلية (Spanning Tree Protocol - STP) تم تصميمه من قبل راديا بيرلمان (IEEE 802.1D) لحلّ مشكلة حلقات الطبقة الثانية (Layer 2 loops) التي تحدث عند وجود مسارات زائدة بين السويتشات. بدون STP، تدور إطارات البث في حلقة لا نهائية وتسبب Broadcast Storm الذي يوقف الشبكة في ثوانٍ معدودة. يقوم STP بـ: (1) انتخاب سويتش كجذر (Root Bridge)، (2) حساب أقصر مسار (Cost) من كل سويتش إلى الجذر، (3) حظر (Block) المنافذ الزائدة حتى تبقى شجرة واحدة خالية من الحلقات، (4) تفعيل المنفذ البديل تلقائياً عند فشل المسار الأساسي.
</div>

<div class="section-title">أنواع بروتوكولات الشجرة المتدلية</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 18%;">البروتوكول</th>
            <th style="width: 12%;">المعيار</th>
            <th style="width: 35%;">الميزات</th>
            <th style="width: 35%;">وقت التقارب</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">STP</code></td><td>IEEE 802.1D</td><td>البروتوكول الكلاسيكي. نوع واحد من VLAN لكل الشبكة (Common Spanning Tree).</td><td>30-50 ثانية (Slow)</td></tr>
        <tr><td><code class="inline">PVST+</code></td><td>Cisco</td><td>Per-VLAN Spanning Tree - شجرة منفصلة لكل VLAN. يسمح بضبط Root Bridge مختلف لكل VLAN لـ load balancing.</td><td>30-50 ثانية</td></tr>
        <tr><td><code class="inline">RSTP</code></td><td>IEEE 802.1w</td><td>Rapid STP - أسرع بكثير. أنواع البورتات: Discarding، Learning، Forwarding. أدوار: Root، Designated، Alternate، Backup.</td><td>1-3 ثوانٍ (Fast)</td></tr>
        <tr><td><code class="inline">Rapid PVST+</code></td><td>Cisco</td><td>RSTP لكل VLAN. يستهلك CPU وذاكرة أكثر لكنه الأفضل للشبكات الكبيرة.</td><td>1-3 ثوانٍ</td></tr>
        <tr><td><code class="inline">MST</code></td><td>IEEE 802.1s</td><td>Multiple Spanning Tree - يسمح بتجمع عدة VLANs في Instance واحد لتوفير CPU.</td><td>1-3 ثوانٍ</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر إعداد STP</div>
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
            <td class="cmd-col">spanning-tree mode &lt;mode&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط وضع STP. الخيارات: <code class="inline">pvst</code>، <code class="inline">rapid-pvst</code>، <code class="inline">mst</code>. الافتراضي PVST+.</td>
            <td class="no-col">no spanning-tree mode</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree vlan &lt;id&gt; root primary</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط السويتش كـ Root Bridge الأساسي لـ VLAN محدد. يخفض priority تلقائياً إلى قيمة أقل من أصغر priority في الشبكة.</td>
            <td class="no-col">no spanning-tree vlan &lt;id&gt; root</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree vlan &lt;id&gt; root secondary</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط السويتش كـ Root Bridge الثانوي (البديل) - يأخذ priority أعلى من الأساسي لكن أقل من بقية السويتشات.</td>
            <td class="no-col">no spanning-tree vlan &lt;id&gt; root secondary</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree vlan &lt;id&gt; priority &lt;0-61440&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط priority يدوياً. القيم الصالحة: 0، 4096، 8192، ... 61440 (بمضاعفات 4096). الأصغر = أفضل.</td>
            <td class="no-col">no spanning-tree vlan &lt;id&gt; priority</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree vlan &lt;id&gt; cost &lt;value&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط cost على منفذ محدد. كلما زاد cost قلّ احتمال اختيار المسار.</td>
            <td class="no-col">no spanning-tree vlan &lt;id&gt; cost</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree vlan &lt;id&gt; port-priority &lt;0-240&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط port-priority على الواجهة (الافتراضي 128). أقل قيمة = أعلى أولوية للـ Designated Port.</td>
            <td class="no-col">no spanning-tree vlan &lt;id&gt; port-priority</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree extend system-id</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل Extended System ID (الحقل 1 بت من priority يضاف VLAN ID). مفعّل افتراضياً في IOS 12+.</td>
            <td class="no-col">no spanning-tree extend system-id</td>
        </tr>
    </tbody>
</table>

<div class="section-title">جدول قيم Cost حسب السرعة (Long Path Cost - IEEE 802.1D-2004)</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>السرعة</th>
            <th>Short Path Cost (قديم)</th>
            <th>Long Path Cost (حديث)</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>10 Mbps</td><td>100</td><td>2,000,000</td></tr>
        <tr><td>100 Mbps</td><td>19</td><td>200,000</td></tr>
        <tr><td>1 Gbps</td><td>4</td><td>20,000</td></tr>
        <tr><td>10 Gbps</td><td>2</td><td>2,000</td></tr>
        <tr><td>100 Gbps</td><td>N/A</td><td>200</td></tr>
    </tbody>
</table>

<div class="section-title">ميزات تحسين STP (PortFast / BPDU Guard / BPDU Filter)</div>
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
            <td class="cmd-col">spanning-tree portfast</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل PortFast على بورت access - يتجاوز حالات Listening و Learning ويدخل مباشرةً في Forwarding. <strong>لبورتات المستخدمين فقط</strong>.</td>
            <td class="no-col">no spanning-tree portfast</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree portfast default</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل PortFast تلقائياً على كل بورتات access الجديدة.</td>
            <td class="no-col">no spanning-tree portfast default</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree bpduguard enable</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل BPDU Guard على البورت - إذا وصل BPDU إلى بورت access، يوضع في errdisable. يحمي من وصول سويتش غير مصرّح به.</td>
            <td class="no-col">no spanning-tree bpduguard</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree portfast bpduguard default</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل BPDU Guard على كل بورتات PortFast تلقائياً.</td>
            <td class="no-col">no spanning-tree portfast bpduguard default</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree bpdufilter enable</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل إرسال واستقبال BPDU على البورت. تحذير: قد يسبب حلقات إذا استُخدم بشكل خاطئ.</td>
            <td class="no-col">no spanning-tree bpdufilter</td>
        </tr>
        <tr>
            <td class="cmd-col">errdisable recovery cause bpduguard</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل استرجاع البورت تلقائياً بعد errdisable بسبب bpduguard (بعد 300 ثانية افتراضياً).</td>
            <td class="no-col">no errdisable recovery cause bpduguard</td>
        </tr>
        <tr>
            <td class="cmd-col">errdisable recovery interval &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط مدة الانتظار قبل استرجاع البورت من errdisable (30-86400 ثانية).</td>
            <td class="no-col">no errdisable recovery interval</td>
        </tr>
    </tbody>
</table>

<div class="section-title">ميزات تحسين STP (UplinkFast / BackboneFast)</div>
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
            <td class="cmd-col">spanning-tree uplinkfast</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل UplinkFast - تسريع تبديل uplink blocked إلى forwarding عند فشل uplink الأساسي (تنطبق على Access switches).</td>
            <td class="no-col">no spanning-tree uplinkfast</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree backbonefast</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل BackboneFast - تسريع التقارب عند فشل رابط غير مباشر (Indirect Link Failure).</td>
            <td class="no-col">no spanning-tree backbonefast</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree loopguard default</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل Loop Guard على كل البورتات - يمنع تحول بورت blocked إلى forwarding بسبب فقدان BPDUs (حماية من الحلقات الناجمة عن فشل غير متسق).</td>
            <td class="no-col">no spanning-tree loopguard default</td>
        </tr>
        <tr>
            <td class="cmd-col">spanning-tree guard root</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل Root Guard على البورت - يمنع سويتش متصل من أن يصبح Root Bridge (يضع البورت في errdisabled إن استلم BPDU أفضل).</td>
            <td class="no-col">no spanning-tree guard root</td>
        </tr>
    </tbody>
</table>

<div class="section-title">RSTP - أدوار البورتات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">الدور (Role)</th>
            <th style="width: 30%;">الحالة (State)</th>
            <th style="width: 45%;">الوصف</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">Root Port</code></td><td>Forwarding</td><td>أفضل منفذ إلى Root Bridge على سويتش غير جذر.</td></tr>
        <tr><td><code class="inline">Designated Port</code></td><td>Forwarding</td><td>المنفذ المخصص لإرسال BPDUs على segment معين.</td></tr>
        <tr><td><code class="inline">Alternate Port</code></td><td>Discarding</td><td>منفذ بديل إلى Root Bridge، يحظر في الوضع الطبيعي.</td></tr>
        <tr><td><code class="inline">Backup Port</code></td><td>Discarding</td><td>منفذ احتياطي على نفس السويتش الذي يحوي Designated Port.</td></tr>
        <tr><td><code class="inline">Edge Port</code></td><td>Forwarding</td><td>منفذ متصل بمضيف نهائي (يعادل PortFast في RSTP).</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض STP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 38%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 45%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show spanning-tree</td><td class="mode-col">Privileged EXEC</td><td>عرض كل تفاصيل STP: VLAN، Root Bridge، الأولوية، البورتات وأدوارها.</td></tr>
        <tr><td class="cmd-col">show spanning-tree vlan &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض STP لـ VLAN محدد.</td></tr>
        <tr><td class="cmd-col">show spanning-tree summary</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص إعدادات STP على الجهاز: الوضع، UplinkFast، BackboneFast، إلخ.</td></tr>
        <tr><td class="cmd-col">show spanning-tree root</td><td class="mode-col">Privileged EXEC</td><td>عرض Root Bridge لكل VLAN.</td></tr>
        <tr><td class="cmd-col">show spanning-tree interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض STP على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show spanning-tree blockedports</td><td class="mode-col">Privileged EXEC</td><td>عرض كل البورتات المحظورة.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: ضبط Root Bridge و Secondary</div>
<div class="code-block">
<span class="comment">! على SW1 (Distribution - يجعل Root لـ VLANs 10,20)</span>
SW1(config)# <span class="prompt">spanning-tree mode rapid-pvst</span>
SW1(config)# <span class="prompt">spanning-tree vlan 10 priority 4096</span>     <span class="comment">! VLAN 10 root</span>
SW1(config)# <span class="prompt">spanning-tree vlan 20 priority 4096</span>     <span class="comment">! VLAN 20 root</span>
SW1(config)# <span class="prompt">spanning-tree vlan 30 priority 8192</span>     <span class="comment">! VLAN 30 secondary</span>

<span class="comment">! على SW2 (Secondary - يجعل Root لـ VLANs 30,99 و Secondary لباقي)</span>
SW2(config)# <span class="prompt">spanning-tree mode rapid-pvst</span>
SW2(config)# <span class="prompt">spanning-tree vlan 30 priority 4096</span>     <span class="comment">! VLAN 30 root</span>
SW2(config)# <span class="prompt">spanning-tree vlan 10 priority 8192</span>     <span class="comment">! VLAN 10 secondary</span>
SW2(config)# <span class="prompt">spanning-tree vlan 20 priority 8192</span>     <span class="comment">! VLAN 20 secondary</span>

<span class="comment">! على Access switches - ضبط PortFast و BPDU Guard على كل بورتات access</span>
SW3(config)# <span class="prompt">spanning-tree portfast default</span>
SW3(config)# <span class="prompt">spanning-tree portfast bpduguard default</span>
SW3(config)# <span class="prompt">errdisable recovery cause bpduguard</span>
SW3(config)# <span class="prompt">errdisable recovery interval 300</span>
</div>

<div class="info-box">
    <div class="info-box-title">قاعدة Bridge ID وحساب Root Bridge</div>
    <div class="info-box-body">
        Bridge ID = Bridge Priority (2 bytes) + MAC Address (6 bytes). الـ Priority في الأصل 16 بت، لكن بت واحد مأخوذ لـ Extended System ID، فتتاح 15 بت فقط فعلياً (مضاعفات 4096: 0، 4096، 8192، ...، 61440). الافتراضي 32768. للعثور على Root Bridge: الأصغر Priority أولاً، وعند التعادل الأصغر MAC. لذلك نضبط Priority منخفضة على سويتش قوي من ناحية CPU وله MAC صغير.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">تحذير: PortFast على Trunk = كارثة!</div>
    <div class="warn-box-body">
        لا تفعل PortFast على بورتات Trunk أبداً. PortFast يفترض أن البورت متصل بمضيف واحد لا يرسل BPDUs، فتجاوز Listening/Learning يعني أن البورت يدخل Forwarding فوراً، مما قد يسبب حلقة فورية قبل أن يكتشفها STP. لذلك، استخدم PortFast حصراً على بورتات Access المتصلة بمضيفين نهائيين (PC، printer، AP). أو استخدم <code class="inline">switchport host</code> الذي يفعّل PortFast + يطفئ PAgP + يطفئ 802.1x دفعة واحدة.
    </div>
</div>


<!-- ============ SECTION 9: PORT SECURITY ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 09</span>
    <div class="chapter-title">Port Security</div>
    <div class="chapter-title-en">Switch Port Security</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    Port Security هي ميزة في سويتشات سيسكو تتيح تقييد الوصول إلى بورت محدد بناءً على عنوان MAC للمضيف المتصل. تستخدم أساساً على بورتات Access المتصلة بمستخدمين نهائيين لمنع: (1) وصول أجهزة غير مصرّح بها، (2) هجمات MAC Flooding (إغراق جدول MAC بكفايات زائفة لإجبار السويتش على الفيضان broadcast)، (3) Rogue switches/access points. أنواع انتهاكات Port Security ثلاثة: <strong>Protect</strong> (إسقاط الإطارات المخالفة بصمت)، <strong>Restrict</strong> (إسقاط + تسجيل + SNMP trap)، <strong>Shutdown</strong> (وضع البورت في errdisabled - الأكثر صرامة).
</div>

<div class="section-title">أوامر Port Security</div>
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
            <td class="cmd-col">switchport port-security</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل Port Security على البورت. يتطلب أن يكون البورت access أو trunk دائم (لا dynamic).</td>
            <td class="no-col">no switchport port-security</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security maximum &lt;1-8192&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط الحد الأقصى لعناوين MAC المسموح بها على البورت. الافتراضي 1.</td>
            <td class="no-col">no switchport port-security maximum</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security mac-address &lt;mac&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تعيين MAC محدد مسموح به يدوياً (Static). يفضل استخدامه للأجهزة الحساسة كالسيرفرات.</td>
            <td class="no-col">no switchport port-security mac-address &lt;mac&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security mac-address sticky</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل Sticky Learning - يتعلم MAC المضيف المتصل ديناميكياً ويحفظه في running-config. يكافئ الكتابة اليدوية لكن أوتوماتيكياً.</td>
            <td class="no-col">no switchport port-security mac-address sticky</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security violation &lt;mode&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط سلوك الانتهاك: <code class="inline">protect</code>، <code class="inline">restrict</code>، <code class="inline">shutdown</code>. الافتراضي shutdown.</td>
            <td class="no-col">no switchport port-security violation</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security aging time &lt;1-1440&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط مدة بقاء MAC entry في جدول Port Security بالدقائق (0 = لا تنتهي).</td>
            <td class="no-col">no switchport port-security aging time</td>
        </tr>
        <tr>
            <td class="cmd-col">switchport port-security aging type inactivity|absolute</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط نمط الانتهاء: <code class="inline">absolute</code> (تنتهي بعد المدة) أو <code class="inline">inactivity</code> (تنتهي بعد مدة من عدم النشاط).</td>
            <td class="no-col">no switchport port-security aging type</td>
        </tr>
        <tr>
            <td class="cmd-col">errdisable recovery cause psecure-violation</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل استرجاع البورت تلقائياً بعد errdisable بسبب port-security violation (بعد 300 ثانية افتراضياً).</td>
            <td class="no-col">no errdisable recovery cause psecure-violation</td>
        </tr>
        <tr>
            <td class="cmd-col">errdisable recovery interval &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط مدة الانتظار قبل استرجاع البورت من errdisable (30-86400 ثانية).</td>
            <td class="no-col">no errdisable recovery interval</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مقارنة بين أنواع الانتهاكات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 20%;">النوع</th>
            <th style="width: 25%;">سلوك البورت</th>
            <th style="width: 25%;">تسجيل syslog</th>
            <th style="width: 15%;">SNMP trap</th>
            <th style="width: 15%;">العدادات</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">protect</code></td><td>إسقاط الإطارات المخالفة بصمت، البورت يبقى up</td><td>لا</td><td>لا</td><td>لا</td></tr>
        <tr><td><code class="inline">restrict</code></td><td>إسقاط الإطارات المخالفة، البورت يبقى up</td><td>نعم</td><td>نعم</td><td>نعم</td></tr>
        <tr><td><code class="inline">shutdown</code></td><td>وضع البورت في errdisabled (link down)</td><td>نعم</td><td>نعم</td><td>نعم</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض Port Security</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 43%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show port-security</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص Port Security على كل البورتات.</td></tr>
        <tr><td class="cmd-col">show port-security interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل Port Security على واجهة محددة: الحد، الحالة، عدد الانتهاكات، الـ MACs.</td></tr>
        <tr><td class="cmd-col">show port-security address</td><td class="mode-col">Privileged EXEC</td><td>عرض كل عناوين MAC المحفوظة عبر Port Security.</td></tr>
        <tr><td class="cmd-col">show port-security interface &lt;iface&gt; address</td><td class="mode-col">Privileged EXEC</td><td>عرض عناوين MAC المسموح بها على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show errdisable recovery</td><td class="mode-col">Privileged EXEC</td><td>عرض أسباب errdisable المفعّلة ومدة الاسترجاع.</td></tr>
        <tr><td class="cmd-col">show interfaces status err-disabled</td><td class="mode-col">Privileged EXEC</td><td>عرض كل البورتات في حالة errdisabled حالياً.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: ضبط Port Security على بورت Access</div>
<div class="code-block">
SW1(config)# <span class="prompt">interface fastEthernet0/10</span>
SW1(config-if)# <span class="prompt">switchport mode access</span>
SW1(config-if)# <span class="prompt">switchport access vlan 10</span>
SW1(config-if)# <span class="prompt">switchport port-security</span>
SW1(config-if)# <span class="prompt">switchport port-security maximum 2</span>
SW1(config-if)# <span class="prompt">switchport port-security mac-address sticky</span>
SW1(config-if)# <span class="prompt">switchport port-security violation restrict</span>
SW1(config-if)# <span class="prompt">spanning-tree portfast</span>
SW1(config-if)# <span class="prompt">exit</span>
SW1(config)# <span class="prompt">errdisable recovery cause psecure-violation</span>
SW1(config)# <span class="prompt">errdisable recovery interval 300</span>

<span class="comment">! تحقق بعد لحظات من اتصال المضيف</span>
SW1# <span class="prompt">show port-security interface fastEthernet0/10</span>
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Restrict
Aging Time                 : 0 mins
Aging Type                 : Absolute
Maximum MAC Addresses      : 2
Total MAC Addresses        : 1
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 1
Last Source Address        : a4b3.2c11.8e5d
Security Violation Count   : 0
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للاب</div>
    <div class="tip-box-body">
        استخدم <code class="inline">switchport port-security mac-address sticky</code> في اللاب لتسهيل التعلم الديناميكي وحفظ MACs تلقائياً. بعد ذلك نفّذ <code class="inline">copy run start</code> لتحويل sticky MAC إلى static محفوظ. تجنّب وضع <code class="inline">shutdown</code> في اللاب التدريبي لأنه سيجبرك على استعادة كل بورت يدوياً عبر <code class="inline">shutdown</code> ثم <code class="inline">no shutdown</code> في كل مرة يحدث انتهاك. استخدم <code class="inline">restrict</code> بدلاً منه للاب.
    </div>
</div>


<!-- ============ SECTION 10: DHCP SERVER & RELAY ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 10</span>
    <div class="chapter-title">DHCP Server &amp; Relay</div>
    <div class="chapter-title-en">DHCP Server, Relay &amp; Snooping</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    DHCP (Dynamic Host Configuration Protocol) هو البروتوكول الذي يوزع عناوين IP والإعدادات الأخرى (subnet mask، default gateway، DNS) على الأجهزة تلقائياً. في سيسكو، يمكن تشغيل الراوتر أو السويتش Layer 3 كخادم DHCP، أو إعداد الراوتر كـ DHCP Relay لنقل طلبات DHCP من شبكة لا تحتوي خادم إلى خادم موجود في شبكة أخرى. كما تتيح ميزة <strong>DHCP Snooping</strong> حماية الشبكة من خوادم DHCP الوهمية (Rogue DHCP Servers) التي قد تعطي عناوين IP خاطئة وتستغل حركة الشبكة.
</div>

<div class="section-title">أوامر DHCP Server</div>
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
            <td class="cmd-col">service dhcp</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل خدمة DHCP على الجهاز. مفعّل افتراضياً، لكن يفضل ضبطها صريحاً.</td>
            <td class="no-col">no service dhcp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp excluded-address &lt;ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>استثناء عنوان (أو نطاق) من توزيع DHCP. تستثني عادةً عناوين الـ gateways والسيرفرات الثابتة.</td>
            <td class="no-col">no ip dhcp excluded-address &lt;ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp pool &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء pool DHCP والدخول إلى وضع إعداده.</td>
            <td class="no-col">no ip dhcp pool &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;ip&gt; &lt;mask|/prefix&gt;</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تحديد شبكة الـ pool. مثل <code class="inline">network 192.168.10.0 255.255.255.0</code> أو <code class="inline">network 192.168.10.0 /24</code>.</td>
            <td class="no-col">no network</td>
        </tr>
        <tr>
            <td class="cmd-col">default-router &lt;ip&gt;</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تعيين default gateway (الراوتر) للمضيفين. يصبح option 3 في رسائل DHCP.</td>
            <td class="no-col">no default-router</td>
        </tr>
        <tr>
            <td class="cmd-col">dns-server &lt;ip1&gt; [&lt;ip2&gt;]</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تعيين خادم DNS أو أكثر. option 6 في DHCP.</td>
            <td class="no-col">no dns-server</td>
        </tr>
        <tr>
            <td class="cmd-col">domain-name &lt;domain&gt;</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تعيين اسم النطاق للمضيفين. option 15 في DHCP.</td>
            <td class="no-col">no domain-name</td>
        </tr>
        <tr>
            <td class="cmd-col">lease &lt;days&gt; [&lt;hours&gt; [&lt;mins&gt;]]</td>
            <td class="mode-col">DHCP Pool</td>
            <td>ضبط مدة lease. <code class="inline">lease 1 12</code> = يوم و12 ساعة. <code class="inline">lease infinite</code> = دائم. الافتراضي يوم واحد.</td>
            <td class="no-col">no lease</td>
        </tr>
        <tr>
            <td class="cmd-col">netbios-name-server &lt;ip&gt;</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تعيين خادم WINS (NetBIOS) - نادر في الشبكات الحديثة.</td>
            <td class="no-col">no netbios-name-server</td>
        </tr>
        <tr>
            <td class="cmd-col">option &lt;code&gt; &lt;value&gt;</td>
            <td class="mode-col">DHCP Pool</td>
            <td>تعيين أي option DHCP عام. مثل <code class="inline">option 150 ip 10.10.10.10</code> (TFTP server لـ VoIP).</td>
            <td class="no-col">no option &lt;code&gt;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">DHCP Relay (عبر منفذ غير مباشر)</div>
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
            <td class="cmd-col">ip helper-address &lt;ip&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تحويل بث DHCP (وعدة بروتوكولات أخرى كـ TFTP, DNS, TACACS) من subnet إلى خادم DHCP في subnet آخر. يحوّل البث إلى unicast.</td>
            <td class="no-col">no ip helper-address</td>
        </tr>
        <tr>
            <td class="cmd-col">ip forward-protocol udp &lt;port&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد بروتوكولات UDP إضافية يتم تمريرها عبر helper. الافتراضي: BOOTP/DHCP (67-68)، TFTP (69)، DNS (53)، NetBIOS (137-138)، TACACS (49).</td>
            <td class="no-col">no ip forward-protocol udp</td>
        </tr>
        <tr>
            <td class="cmd-col">no ip broadcast</td>
            <td class="mode-col">Interface Config</td>
            <td>تعطيل تمرير البث المباشر (مفيد لتقليل البث غير الضروري).</td>
            <td class="no-col">ip broadcast</td>
        </tr>
    </tbody>
</table>

<div class="section-title">DHCP Snooping (حماية)</div>
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
            <td class="cmd-col">ip dhcp snooping</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل DHCP Snooping على السويتش.</td>
            <td class="no-col">no ip dhcp snooping</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp snooping vlan &lt;id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل Snooping على VLAN محدد (أو نطاق).</td>
            <td class="no-col">no ip dhcp snooping vlan</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp snooping trust</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط البورت كـ trusted (يسمح بـ DHCP server). استخدمه على بورتات الـ uplink/trunk المتصلة بخادم DHCP.</td>
            <td class="no-col">no ip dhcp snooping trust</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp snooping limit rate &lt;pps&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط حد معدل رسائل DHCP في الثانية على البورت (يمنع DoS).</td>
            <td class="no-col">no ip dhcp snooping limit rate</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp snooping verify mac-address</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل تحقق من MAC المصدر في رأس Ethernet مع MAC في DHCP. يمنع الانتحال.</td>
            <td class="no-col">no ip dhcp snooping verify mac-address</td>
        </tr>
        <tr>
            <td class="cmd-col">ip dhcp snooping information option</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل Option 82 (DHCP Snooping inserts this) - يضيف معلومات البورت السويتش إلى طلب DHCP.</td>
            <td class="no-col">no ip dhcp snooping information option</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض DHCP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 43%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip dhcp pool &lt;name&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض إحصائيات pool: عدد العناوين، المستأجر، المتاح.</td></tr>
        <tr><td class="cmd-col">show ip dhcp binding</td><td class="mode-col">Privileged EXEC</td><td>عرض كل الـ leases النشطة (IP ↔ MAC).</td></tr>
        <tr><td class="cmd-col">show ip dhcp conflict</td><td class="mode-col">Privileged EXEC</td><td>عرض تعارضات العناوين (عنوان معطى لمضيفين).</td></tr>
        <tr><td class="cmd-col">show ip dhcp server statistics</td><td class="mode-col">Privileged EXEC</td><td>عرض إحصائيات الرسائل: عدد الـ Discover, Offer, Request, Ack.</td></tr>
        <tr><td class="cmd-col">show ip dhcp snooping</td><td class="mode-col">Privileged EXEC</td><td>عرض إعدادات DHCP Snooping.</td></tr>
        <tr><td class="cmd-col">show ip dhcp snooping binding</td><td class="mode-col">Privileged EXEC</td><td>عرض الـ bindings (MAC↔IP↔VLAN↔Port).</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: راوتر كخادم DHCP</div>
<div class="code-block">
Router(config)# <span class="prompt">ip dhcp excluded-address 192.168.10.1 192.168.10.10</span>
Router(config)# <span class="prompt">ip dhcp excluded-address 192.168.10.254</span>
Router(config)# <span class="prompt">ip dhcp pool SALES-Pool</span>
Router(dhcp-config)# <span class="prompt">network 192.168.10.0 255.255.255.0</span>
Router(dhcp-config)# <span class="prompt">default-router 192.168.10.1</span>
Router(dhcp-config)# <span class="prompt">dns-server 8.8.8.8 1.1.1.1</span>
Router(dhcp-config)# <span class="prompt">domain-name cairo-net.local</span>
Router(dhcp-config)# <span class="prompt">lease 0 8 0</span>            <span class="comment">! 8 ساعات</span>
Router(dhcp-config)# <span class="prompt">exit</span>

Router# <span class="prompt">show ip dhcp pool SALES-Pool</span>
Pool SALES-Pool :
 Utilization mark (high/low)    : 100 / 0
 Subnet size (first/second)     : 0 / 0
 Total addresses                : 254
 Leased addresses               : 24
 Pending event                  : none
 1 subnet is currently in the pool :
 Current index        IP address range            Leased addresses
 192.168.10.11        192.168.10.1  - 192.168.10.254    24
</div>

<div class="code-block-title">مثال 10.2: DHCP Relay على واجهة</div>
<div class="code-block">
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip address 192.168.20.1 255.255.255.0</span>
Router(config-if)# <span class="prompt">ip helper-address 10.10.10.5</span>     <span class="comment">! خادم DHCP بعيد</span>
Router(config-if)# <span class="prompt">no shutdown</span>
Router(config-if)# <span class="prompt">exit</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للاب</div>
    <div class="tip-box-body">
        عند تشغيل الجهاز كخادم DHCP، استثني دائماً أول 10 عناوين على الأقل (للأجهزة الثابتة كالراوتر نفسه والسيرفرات) والآخر عنوان (للـ broadcast). استخدم <code class="inline">lease infinite</code> في اللاب فقط، ففي الإنتاج قد يسبب استنزاف العناوين. للتحقق من عمل DHCP على جهاز مضيف Windows، استخدم <code class="inline">ipconfig /release</code> ثم <code class="inline">ipconfig /renew</code> على المضيف، و <code class="inline">show ip dhcp binding</code> على الراوتر.
    </div>
</div>

"""
