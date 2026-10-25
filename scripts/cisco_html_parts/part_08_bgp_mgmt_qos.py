# -*- coding: utf-8 -*-
"""Part 08: Section 17 - BGP + Section 18 - Network Management + Section 19 - QoS + Section 20 - 802.1x"""

SECTIONS_08 = """

<!-- ============ SECTION 17: BGP ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 17</span>
    <div class="chapter-title">BGP الأساسي (CCNP)</div>
    <div class="chapter-title-en">Border Gateway Protocol</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    BGP (Border Gateway Protocol) هو بروتوكول توجيه من نوع Path-Vector، يستخدم على نطاق الإنترنت بين Autonomous Systems (ASes). يصف المعيار RFC 4271 (BGP-4). BGP هو البروتوكول الذي يحوّم الإنترنت - أي صفحة ويب تطلبها تمر عبر عشرات BGP routers. يتميز بـ: (1) موثوقية (TCP port 179)، (2) قابلية توسّع هائلة (400K+ routes في الجدول الكامل)، (3) سياسات غنية (Attributes) للتحكم الدقيق في اختيار المسارات. أنواعه: <strong>eBGP</strong> (External - بين ASes مختلفة)، <strong>iBGP</strong> (Internal - داخل AS واحد). ملاحظة: iBGP يطلب full-mesh أو استخدام Route Reflectors / Confederations.
</div>

<div class="section-title">أوامر BGP الأساسية</div>
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
            <td class="cmd-col">router bgp &lt;AS&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية BGP مع AS محدد. الـ AS رقم (1-4294967295) أو قابلة للتوسعة (AS Numbers 4-byte).</td>
            <td class="no-col">no router bgp &lt;AS&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">bgp router-id &lt;ip&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط router-id يدوياً.</td>
            <td class="no-col">no bgp router-id</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; remote-as &lt;AS&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تعريف جار BGP مع AS التابع له. لو الـ AS مختلف عن AS الراوتر المحلي = eBGP، لو نفس = iBGP.</td>
            <td class="no-col">no neighbor &lt;ip&gt; remote-as</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; description &lt;text&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>وصف الجار للتوثيق.</td>
            <td class="no-col">no neighbor &lt;ip&gt; description</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; update-source &lt;iface&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تحديد الواجهة المصدر لجلسات BGP. <strong>ضروري</strong> في iBGP لتأمين أن الـ TCP source IP مطابق لـ neighbor المتوقع.</td>
            <td class="no-col">no neighbor &lt;ip&gt; update-source</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; next-hop-self</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط الـ next-hop إلى نفسه عند الإعلان لجيران iBGP. <strong>ضروري</strong> في iBGP لأن next-hop لا يتغير افتراضياً.</td>
            <td class="no-col">no neighbor &lt;ip&gt; next-hop-self</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; password &lt;pass&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل مصادقة TCP MD5 مع الجار.</td>
            <td class="no-col">no neighbor &lt;ip&gt; password</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; ebgp-multihop &lt;ttl&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>السماح بـ eBGP مع جار ليس مباشراً متصلاً. ضروري لتشغيل eBGP على loopback.</td>
            <td class="no-col">no neighbor &lt;ip&gt; ebgp-multihop</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; send-community</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل إرسال community attributes للجار.</td>
            <td class="no-col">no neighbor &lt;ip&gt; send-community</td>
        </tr>
        <tr>
            <td class="cmd-col">neighbor &lt;ip&gt; route-map &lt;name&gt; in|out</td>
            <td class="mode-col">Router Config</td>
            <td>تطبيق route-map على الحركة الواردة/الصادرة من الجار.</td>
            <td class="no-col">no neighbor &lt;ip&gt; route-map</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;network&gt; mask &lt;mask&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>الإعلان عن شبكة محددة. يجب أن تكون موجودة في جدول التوجيه لإعلانها.</td>
            <td class="no-col">no network ...</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;network&gt; mask &lt;mask&gt; route-map &lt;name&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>الإعلان عن شبكة مع تطبيق route-map لتعديل attributes.</td>
            <td class="no-col">no network ...</td>
        </tr>
        <tr>
            <td class="cmd-col">redistribute connected|static|ospf|eigrp</td>
            <td class="mode-col">Router Config</td>
            <td>إعادة توزيع المسارات من بروتوكول آخر في BGP. تحذير: قد يسبب مشاكل في الـ AS الكامل.</td>
            <td class="no-col">no redistribute ...</td>
        </tr>
        <tr>
            <td class="cmd-col">aggregate-address &lt;network&gt; &lt;mask&gt; [summary-only]</td>
            <td class="mode-col">Router Config</td>
            <td>تلخيص المسارات إلى network أعرض. <code class="inline">summary-only</code> يخفي المسارات الفردية.</td>
            <td class="no-col">no aggregate-address</td>
        </tr>
    </tbody>
</table>

<div class="section-title">Attributes الهامة في BGP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 18%;">Attribute</th>
            <th style="width: 22%;">النوع</th>
            <th style="width: 25%;">الأولوية</th>
            <th style="width: 35%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><strong>Weight</strong></td><td>Cisco-Proprietary</td><td>1 (الأعلى)</td><td>محلي للراوتر فقط (لا يرسل). أعلى weight = أفضل. 0-65535.</td></tr>
        <tr><td><strong>Local Preference</strong></td><td>Well-known Discretionary</td><td>2</td><td>يُرسل داخل AS. أعلى = أفضل. الافتراضي 100.</td></tr>
        <tr><td><strong>AS-Path</strong></td><td>Well-known Mandatory</td><td>3</td><td>قائمة ASes التي مرّت بها. أقصر = أفضل.</td></tr>
        <tr><td><strong>Origin</strong></td><td>Well-known Mandatory</td><td>4</td><td>IGP (i) &gt; EGP (e) &gt; Incomplete (?)</td></tr>
        <tr><td><strong>MED</strong></td><td>Optional Non-transitive</td><td>5</td><td>أدنى = أفضل. يخبر AS خارجي بأي path أفضل للعودة.</td></tr>
        <tr><td><strong>Community</strong></td><td>Optional Transitive</td><td>N/A</td><td>تاج لتعريف المسارات كمجموعة. مثلاً no-export.</td></tr>
        <tr><td><strong>Next-Hop</strong></td><td>Well-known Mandatory</td><td>N/A</td><td>عنوان القفزة التالية. يجب أن يصل إليه الراوتر.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر Route-Map</div>
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
            <td class="cmd-col">route-map &lt;name&gt; permit|deny &lt;seq&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء route-map و دخول وضع الإعداد.</td>
            <td class="no-col">no route-map &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">match ip address &lt;acl&gt;</td>
            <td class="mode-col">Route-Map</td>
            <td>تطابق مع ACL.</td>
            <td class="no-col">no match ip address</td>
        </tr>
        <tr>
            <td class="cmd-col">match as-path &lt;AS-ACL&gt;</td>
            <td class="mode-col">Route-Map</td><td>تطابق مع AS-path ACL.</td>
            <td class="no-col">no match as-path</td>
        </tr>
        <tr>
            <td class="cmd-col">match community &lt;name&gt;</td>
            <td class="mode-col">Route-Map</td>
            <td>تطابق مع community-list.</td>
            <td class="no-col">no match community</td>
        </tr>
        <tr>
            <td class="cmd-col">set weight &lt;n&gt;</td>
            <td class="mode-col">Route-Map</td>
            <td>ضبط Weight.</td>
            <td class="no-col">no set weight</td>
        </tr>
        <tr>
            <td class="cmd-col">set local-preference &lt;n&gt;</td>
            <td class="mode-col">Route-Map</td>
            <td>ضبط Local Preference.</td>
            <td class="no-col">no set local-preference</td>
        </tr>
        <tr>
            <td class="cmd-col">set metric &lt;n&gt;</td>
            <td class="mode-col">Route-Map</td>
            <td>ضبط MED.</td>
            <td class="no-col">no set metric</td>
        </tr>
        <tr>
            <td class="cmd-col">set as-path prepend &lt;AS&gt; ...</td>
            <td class="mode-col">Route-Map</td>
            <td>إضافة AS entries إلى AS-path. يفيد في التأثير على inbound routing.</td>
            <td class="no-col">no set as-path prepend</td>
        </tr>
        <tr>
            <td class="cmd-col">set community &lt;value&gt; [additive]</td>
            <td class="mode-col">Route-Map</td>
            <td>ضبط community.</td>
            <td class="no-col">no set community</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض BGP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 45%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip bgp summary</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص كل الجيران وعدد المسارات المستلمة وحالة الـ BGP.</td></tr>
        <tr><td class="cmd-col">show ip bgp</td><td class="mode-col">Privileged EXEC</td><td>عرض BGP table - كل المسارات و attributes.</td></tr>
        <tr><td class="cmd-col">show ip bgp &lt;network&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل مسار محدد.</td></tr>
        <tr><td class="cmd-col">show ip bgp neighbors</td><td class="mode-col">Privileged EXEC</td><td>عرض كل الجيران بتفصيل كامل: الحالة، الـ capabilities، الإحصائيات.</td></tr>
        <tr><td class="cmd-col">show ip bgp neighbors &lt;ip&gt; advertised-routes</td><td class="mode-col">Privileged EXEC</td><td>عرض المسارات المعلنة لجار محدد.</td></tr>
        <tr><td class="cmd-col">show ip bgp neighbors &lt;ip&gt; received-routes</td><td class="mode-col">Privileged EXEC</td><td>عرض المسارات المستلمة من جار.</td></tr>
        <tr><td class="cmd-col">show ip bgp community</td><td class="mode-col">Privileged EXEC</td><td>عرض المسارات حسب community.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: eBGP بين راوترين</div>
<div class="code-block">
<span class="comment">! على R1 (AS 65000)</span>
R1(config)# <span class="prompt">router bgp 65000</span>
R1(config-router)# <span class="prompt">bgp router-id 1.1.1.1</span>
R1(config-router)# <span class="prompt">neighbor 203.0.113.2 remote-as 65001</span>
R1(config-router)# <span class="prompt">neighbor 203.0.113.2 description Link-to-R2</span>
R1(config-router)# <span class="prompt">neighbor 203.0.113.2 password BGP-S3cr3t!</span>
R1(config-router)# <span class="prompt">network 192.168.1.0 mask 255.255.255.0</span>
R1(config-router)# <span class="prompt">exit</span>
R1(config)# <span class="prompt">ip route 192.168.1.0 255.255.255.0 null0</span>      <span class="comment">! تثبت المسار</span>

<span class="comment">! على R2 (AS 65001)</span>
R2(config)# <span class="prompt">router bgp 65001</span>
R2(config-router)# <span class="prompt">bgp router-id 2.2.2.2</span>
R2(config-router)# <span class="prompt">neighbor 203.0.113.1 remote-as 65000</span>
R2(config-router)# <span class="prompt">neighbor 203.0.113.1 password BGP-S3cr3t!</span>
R2(config-router)# <span class="prompt">network 192.168.2.0 mask 255.255.255.0</span>
R2(config-router)# <span class="prompt">exit</span>
R2(config)# <span class="prompt">ip route 192.168.2.0 255.255.255.0 null0</span>

R1# <span class="prompt">show ip bgp summary</span>
Neighbor    V   AS  MsgRcvd MsgSent TblVer InQ OutQ Up/Down State/PfxRcd
203.0.113.2 4 65001   15     15      2     0    0 00:10:32 1
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة لـ BGP</div>
    <div class="tip-box-body">
        (1) للـ iBGP بين راوترين في AS، اضبط <code class="inline">neighbor x.x.x.x update-source loopback0</code> على الطرفين. (2) في iBGP، اضبط <code class="inline">neighbor x.x.x.x next-hop-self</code> دائماً لأن next-hop في iBGP لا يتغير تلقائياً. (3) للـ eBGP متعدد القفزات (مثل eBGP على loopbacks)، اضبط <code class="inline">ebgp-multihop 2</code> أو أعلى. (4) استخدم <code class="inline">route-map</code> بدلاً من <code class="inline">network</code> المباشرة لتفادي إعلان مسارات غير مقصودة.
    </div>
</div>


<!-- ============ SECTION 18: NETWORK MANAGEMENT ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 18</span>
    <div class="chapter-title">إدارة الشبكة - SNMP/Syslog/NTP/SSH</div>
    <div class="chapter-title-en">SNMP, Syslog, NTP &amp; SSH Management</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    إدارة الشبكة (Network Management) تشمل مراقبة الأجهزة، جمع السجلات، مزامنة التوقيت، وتأمين الوصول عن بعد. البروتوكولات الرئيسية: <strong>SNMP</strong> (Simple Network Management Protocol) لجمع الإحصائيات والتحكم، <strong>Syslog</strong> لإرسال رسائل السجلات لخادم مركزي، <strong>NTP</strong> لمزامنة التوقيت (ضرورية لتفسير السجلات بشكل صحيح)، <strong>SSH</strong> للوصول الآمن عبر CLI (بديل Telnet غير المشفر).
</div>

<div class="section-title">أوامر SNMP</div>
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
            <td class="cmd-col">snmp-server community &lt;string&gt; RO|RW [acl]</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط community string. RO = Read Only (get)، RW = Read Write (set). استعمل ACL لتحديد IPs المصرّح بها.</td>
            <td class="no-col">no snmp-server community &lt;string&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server host &lt;ip&gt; [version 2c|3] &lt;community&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعريف خادم SNMP traps. يرسل notifications عند حدوث أحداث.</td>
            <td class="no-col">no snmp-server host &lt;ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server location &lt;text&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط قيمة location (يظهر في sysDescr queries).</td>
            <td class="no-col">no snmp-server location</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server contact &lt;text&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط جهة الاتصال المسؤولة.</td>
            <td class="no-col">no snmp-server contact</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server enable traps</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل كل أنواع traps. أو نوع محدد: <code class="inline">snmp-server enable traps snmp authentication</code>.</td>
            <td class="no-col">no snmp-server enable traps</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server view &lt;name&gt; &lt;oid-tree&gt; included|excluded</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء view لتحديد أي MIB tree يمكن الوصول إليه.</td>
            <td class="no-col">no snmp-server view</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server group &lt;name&gt; v3 priv</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء group SNMPv3 مع تشفير (أقوى من v2c).</td>
            <td class="no-col">no snmp-server group</td>
        </tr>
        <tr>
            <td class="cmd-col">snmp-server user &lt;name&gt; &lt;group&gt; v3 auth sha &lt;pass&gt; priv aes 128 &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء مستخدم SNMPv3 مع مصادقة SHA وتشفير AES-128. الأكثر أماناً.</td>
            <td class="no-col">no snmp-server user</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر Syslog</div>
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
            <td class="cmd-col">logging &lt;ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعريف خادم syslog لإرسال الرسائل إليه.</td>
            <td class="no-col">no logging &lt;ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">logging trap &lt;level&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط مستوى الخطورة الأدنى المرسل للخادم.</td>
            <td class="no-col">no logging trap</td>
        </tr>
        <tr>
            <td class="cmd-col">logging source-interface &lt;iface&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد الواجهة المصدر لكل رسائل syslog (مفيد للفحص الأمني للسجلات).</td>
            <td class="no-col">no logging source-interface</td>
        </tr>
        <tr>
            <td class="cmd-col">logging buffered &lt;size&gt; &lt;level&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تخزين رسائل syslog في RAM للمراجعة المحلية. مثل <code class="inline">logging buffered 51200 informational</code>.</td>
            <td class="no-col">no logging buffered</td>
        </tr>
        <tr>
            <td class="cmd-col">logging console &lt;level&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>عرض رسائل syslog على console.</td>
            <td class="no-col">no logging console</td>
        </tr>
        <tr>
            <td class="cmd-col">logging monitor &lt;level&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>عرض رسائل syslog على جلسات terminal (VTY) باستخدام <code class="inline">terminal monitor</code>.</td>
            <td class="no-col">no logging monitor</td>
        </tr>
        <tr>
            <td class="cmd-col">service timestamps log datetime msec</td>
            <td class="mode-col">Global Config</td>
            <td>إضافة timestamp دقيق للرسائل. ضرورية.</td>
            <td class="no-col">no service timestamps</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مستويات Syslog Severity</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 12%;">المستوى</th>
            <th style="width: 22%;">الاسم</th>
            <th style="width: 22%;">الكلمة المفتاحية</th>
            <th style="width: 44%;">الوصف</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>0</td><td>Emergencies</td><td>emergencies</td><td>النظام غير قابل للاستخدام (panic).</td></tr>
        <tr><td>1</td><td>Alerts</td><td>alerts</td><td>تدخل فوري مطلوب.</td></tr>
        <tr><td>2</td><td>Critical</td><td>critical</td><td>حالة حرجة (مثل فشل واجهة رئيسية).</td></tr>
        <tr><td>3</td><td>Errors</td><td>errors</td><td>حالة خطأ.</td></tr>
        <tr><td>4</td><td>Warnings</td><td>warnings</td><td>تحذير.</td></tr>
        <tr><td>5</td><td>Notifications</td><td>notifications</td><td>إشعار طبيعي (مثل up/down interface).</td></tr>
        <tr><td>6</td><td>Informational</td><td>informational</td><td>معلومة (مثل session تم إنشاؤها).</td></tr>
        <tr><td>7</td><td>Debugging</td><td>debugging</td><td>رسائل debug.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد NTP + Syslog + SNMPv3</div>
<div class="code-block">
Router(config)# <span class="prompt">ntp server 162.159.200.1 prefer</span>
Router(config)# <span class="prompt">ntp server 162.159.200.123</span>           <span class="comment">! Cloudflare NTP</span>
Router(config)# <span class="prompt">ntp source gigabitEthernet0/0</span>
Router(config)# <span class="prompt">ntp update-calendar</span>

Router(config)# <span class="prompt">service timestamps log datetime msec localtime show-timezone</span>
Router(config)# <span class="prompt">logging buffered 51200 informational</span>
Router(config)# <span class="prompt">logging trap informational</span>
Router(config)# <span class="prompt">logging source-interface loopback0</span>
Router(config)# <span class="prompt">logging 10.10.10.50</span>          <span class="comment">! Syslog server</span>

Router(config)# <span class="prompt">snmp-server group ADMINS v3 priv</span>
Router(config)# <span class="prompt">snmp-server user admin1 ADMINS v3 auth sha S3cr3t!Auth priv aes 128 Pr1v@cy!Pass</span>
Router(config)# <span class="prompt">snmp-server host 10.10.10.51 version 3 priv admin1</span>
Router(config)# <span class="prompt">snmp-server enable traps</span>
Router(config)# <span class="prompt">snmp-server location Cairo-DC-Room1</span>
Router(config)# <span class="prompt">snmp-server contact NetAdmin 24x7 - netadmin@cairo-net.local</span>
</div>

<div class="warn-box">
    <div class="warn-box-title">تحذير SNMPv2c أمني</div>
    <div class="warn-box-body">
        SNMPv2c يستخدم community string نصية واضحة (sniffer يستطيع قراءتها). <strong>تجنّبه</strong> في الإنتاج عبر الإنترنت. استخدم SNMPv3 الذي يدعم مصادقة وتشفير. إن اضطررت لـ v2c، قيّده بـ ACL: <code class="inline">snmp-server community SECURE-STRING RO 10</code> حيث ACL 10 يسمح فقط لخوادم الإدارة المعروفة.
    </div>
</div>


<!-- ============ SECTION 19: QoS ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 19</span>
    <div class="chapter-title">Quality of Service (QoS)</div>
    <div class="chapter-title-en">Classification, Marking &amp; Queuing</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    QoS (Quality of Service) هي مجموعة تقنيات تضمن أداءً معيناً لحركة معينة عبر الشبكة. تستخدم QoS لـ: (1) إعطاء أولوية لحركة الصوت (VoIP) والفيديو، (2) حجز عرض نطاق للتطبيقات الحرجة، (3) تحديد حدود لاستخدام عرض النطاق. خطوات QoS الرئيسية: <strong>Classification</strong> (تصنيف الحركة)، <strong>Marking</strong> (وضع علامات في رأس الحزمة)، <strong>Queuing</strong> (إدارة طوابير الإرسال)، <strong>Scheduling</strong> (اختيار الحزمة التالية للإرسال)، <strong>Shaping/Policing</strong> (تحديد معدل الإرسال).
</div>

<div class="section-title">قيم DSCP (Differentiated Services Code Point)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">DSCP Name</th>
            <th style="width: 15%;">Decimal</th>
            <th style="width: 20%;">Binary</th>
            <th style="width: 40%;">الاستخدام</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Default (CS0)</td><td>0</td><td>000000</td><td>Best Effort (الافتراضي).</td></tr>
        <tr><td>CS1</td><td>8</td><td>001000</td><td>Bulk traffic (إرسال بكميات كبيرة).</td></tr>
        <tr><td>AF11</td><td>10</td><td>001010</td><td>Assured Forwarding - low priority data.</td></tr>
        <tr><td>AF31</td><td>26</td><td>011010</td><td>Streaming video.</td></tr>
        <tr><td>EF (Expedited Forwarding)</td><td>46</td><td>101110</td><td>VoIP - أقصى أولوية. لا يُؤخّر.</td></tr>
        <tr><td>CS6</td><td>48</td><td>110000</td><td>Network control (routing protocols).</td></tr>
        <tr><td>CS7</td><td>56</td><td>111000</td><td>Reserved.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر QoS الأساسية (MQC - Modular QoS CLI)</div>
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
            <td class="cmd-col">class-map [match-all|match-any] &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء class-map لتصنيف الحركة. <code class="inline">match-all</code> = AND، <code class="inline">match-any</code> = OR (الافتراضي).</td>
            <td class="no-col">no class-map &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">match access-group &lt;acl&gt;</td>
            <td class="mode-col">Class-Map</td>
            <td>تطابق حركة بـ ACL.</td>
            <td class="no-col">no match access-group</td>
        </tr>
        <tr>
            <td class="cmd-col">match protocol &lt;protocol&gt;</td>
            <td class="mode-col">Class-Map</td>
            <td>تطابق بـ NBAR protocol (مثل http، sip، rtp).</td>
            <td class="no-col">no match protocol</td>
        </tr>
        <tr>
            <td class="cmd-col">match dscp &lt;value&gt;</td>
            <td class="mode-col">Class-Map</td>
            <td>تطابق بقيمة DSCP.</td>
            <td class="no-col">no match dscp</td>
        </tr>
        <tr>
            <td class="cmd-col">match cos &lt;0-7&gt;</td>
            <td class="mode-col">Class-Map</td>
            <td>تطابق بقيمة 802.1Q CoS.</td>
            <td class="no-col">no match cos</td>
        </tr>
        <tr>
            <td class="cmd-col">match ip rtp &lt;start&gt; &lt;range&gt;</td>
            <td class="mode-col">Class-Map</td>
            <td>تطابق بـ UDP RTP port range.</td>
            <td class="no-col">no match ip rtp</td>
        </tr>
        <tr>
            <td class="cmd-col">policy-map &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء policy-map.</td>
            <td class="no-col">no policy-map &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">class &lt;class-name&gt;</td>
            <td class="mode-col">Policy-Map</td>
            <td>إسناد class-map إلى policy.</td>
            <td class="no-col">no class</td>
        </tr>
        <tr>
            <td class="cmd-col">set dscp &lt;value&gt;</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>وضع علامة DSCP.</td>
            <td class="no-col">no set dscp</td>
        </tr>
        <tr>
            <td class="cmd-col">set cos &lt;0-7&gt;</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>وضع علامة CoS على L2.</td>
            <td class="no-col">no set cos</td>
        </tr>
        <tr>
            <td class="cmd-col">priority &lt;kbps&gt;</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>ضمان Priority Queue (LLQ) لـ VoIP.</td>
            <td class="no-col">no priority</td>
        </tr>
        <tr>
            <td class="cmd-col">bandwidth &lt;kbps&gt;</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>حجز bandwidth في CBWFQ.</td>
            <td class="no-col">no bandwidth</td>
        </tr>
        <tr>
            <td class="cmd-col">police &lt;cir&gt; conform-action transmit exceed-action drop</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>تحديد rate limit باستخدام policing.</td>
            <td class="no-col">no police</td>
        </tr>
        <tr>
            <td class="cmd-col">shape average &lt;cir&gt;</td>
            <td class="mode-col">Policy-Map-Class</td>
            <td>تخفيف المعدل باستخدام shaping (يؤجل بدل أن يرمي).</td>
            <td class="no-col">no shape average</td>
        </tr>
        <tr>
            <td class="cmd-col">service-policy &lt;name&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تطبيق policy-map على واجهة (in أو out).</td>
            <td class="no-col">no service-policy</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مثال: QoS لـ VoIP</div>
<div class="code-block">
Router(config)# <span class="prompt">class-map match-any VOIP</span>
Router(config-cmap)# <span class="prompt">match protocol sip</span>
Router(config-cmap)# <span class="prompt">match protocol rtp</span>
Router(config-cmap)# <span class="prompt">match ip rtp 16384 16383</span>
Router(config-cmap)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">class-map match-any CRITICAL</span>
Router(config-cmap)# <span class="prompt">match protocol sql</span>
Router(config-cmap)# <span class="prompt">match protocol ssh</span>
Router(config-cmap)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">policy-map QoS-OUT</span>
Router(config-pmap)# <span class="prompt">class VOIP</span>
Router(config-pmap-c)# <span class="prompt">priority 256</span>            <span class="comment">! LLQ 256kbps</span>
Router(config-pmap-c)# <span class="prompt">set dscp ef</span>
Router(config-pmap-c)# <span class="prompt">exit</span>
Router(config-pmap)# <span class="prompt">class CRITICAL</span>
Router(config-pmap-c)# <span class="prompt">bandwidth 512</span>          <span class="comment">! CBWFQ 512kbps</span>
Router(config-pmap-c)# <span class="prompt">set dscp af31</span>
Router(config-pmap-c)# <span class="prompt">exit</span>
Router(config-pmap)# <span class="prompt">class class-default</span>
Router(config-pmap-c)# <span class="prompt">fair-queue</span>             <span class="comment">! WFQ للباقي</span>
Router(config-pmap-c)# <span class="prompt">exit</span>
Router(config-pmap)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/1</span>      <span class="comment">! WAN</span>
Router(config-if)# <span class="prompt">service-policy output QoS-OUT</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">الفرق بين Policing و Shaping</div>
    <div class="tip-box-body">
        <strong>Policing</strong>: يرمي الحزمة الفائضة عن المعدل (drop) - يستعمل في حدود صارمة (ISP إلى Customer). <strong>Shaping</strong>: يؤجل الحزمة الفائضة في طابور (queue) لإرسالها لاحقاً - يستعمل على حدود Customer إلى ISP (يحافظ على الـ TCP sessions). الفرق التقني: Policing يعمل بإرسال أو رمي؛ Shaping يعمل بتأخير الإرسال. الـ Shaping أنعم على التطبيقات لكنه يحتاج ذاكرة أكبر.
    </div>
</div>


<!-- ============ SECTION 20: 802.1x & AAA ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 20</span>
    <div class="chapter-title">802.1x &amp; AAA Authentication</div>
    <div class="chapter-title-en">IEEE 802.1x, RADIUS &amp; TACACS+</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    802.1x هو معيار IEEE للمصادقة على بورتات الشبكة، يستعمل EAP (Extensible Authentication Protocol) على L2. ثلاثة عناصر: <strong>Supplicant</strong> (العميل على المضيف)، <strong>Authenticator</strong> (السويتش)، <strong>Authentication Server</strong> (RADIUS server). AAA (Authentication, Authorization, Accounting) هو إطار شامل لإدارة الوصول: المصادقة (هل أنت من تدّعي؟)، التفويض (ماذا يسمح لك أن تفعل؟)، المحاسبة (ماذا فعلت؟). RADIUS و TACACS+ هما بروتوكولان شائعان لـ AAA، RADIUS قياسي (RFC 2865) يستعمل UDP، TACACS+ Cisco-Proprietary يستعمل TCP.
</div>

<div class="section-title">مقارنة RADIUS و TACACS+</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">الميزة</th>
            <th style="width: 37.5%;">RADIUS</th>
            <th style="width: 37.5%;">TACACS+</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>المعيار</td><td>IETF RFC 2865</td><td>Cisco-Proprietary</td></tr>
        <tr><td>النقل</td><td>UDP 1812/1813</td><td>TCP 49</td></tr>
        <tr><td>التشفير</td><td>password فقط</td><td>كل payload</td></tr>
        <tr><td>الفصل AAA</td><td>مدمج</td><td>منفصل (كل منفصل)</td></tr>
        <tr><td>الاستخدام الأمثل</td><td>مصادقة المستخدمين (802.1x، VPN)</td><td>مصادقة Admin (device admin)</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر AAA</div>
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
            <td class="cmd-col">aaa new-model</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل AAA على الجهاز. <strong>مطلوب</strong> قبل أي AAA config.</td>
            <td class="no-col">no aaa new-model</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authentication login default local</td>
            <td class="mode-col">Global Config</td>
            <td>المصادقة عبر قاعدة المستخدمين المحلية.</td>
            <td class="no-col">no aaa authentication login default</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authentication login default group radius local</td>
            <td class="mode-col">Global Config</td>
            <td>المصادقة عبر RADIUS أولاً، ثم احتياطياً عبر قاعدة محلية.</td>
            <td class="no-col">no aaa authentication login default</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authentication enable default group radius enable</td>
            <td class="mode-col">Global Config</td>
            <td>المصادقة على enable mode عبر RADIUS، احتياطياً عبر enable secret محلي.</td>
            <td class="no-col">no aaa authentication enable default</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authorization exec default group radius local</td>
            <td class="mode-col">Global Config</td>
            <td>التفويض لمنح EXEC عبر RADIUS.</td>
            <td class="no-col">no aaa authorization exec default</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa accounting exec default start-stop group radius</td>
            <td class="mode-col">Global Config</td>
            <td>تسجيل بداية ونهاية جلسات EXEC في RADIUS.</td>
            <td class="no-col">no aaa accounting exec default</td>
        </tr>
        <tr>
            <td class="cmd-col">radius server &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعريف خادم RADIUS باسم (IOS 15+).</td>
            <td class="no-col">no radius server</td>
        </tr>
        <tr>
            <td class="cmd-col">address ipv4 &lt;ip&gt; auth-port 1812 acct-port 1813</td>
            <td class="mode-col">RADIUS Server</td>
            <td>ضبط عنوان RADIUS والبورتات.</td>
            <td class="no-col">no address</td>
        </tr>
        <tr>
            <td class="cmd-col">key &lt;pass&gt;</td>
            <td class="mode-col">RADIUS Server</td>
            <td>ضبط shared secret.</td>
            <td class="no-col">no key</td>
        </tr>
        <tr>
            <td class="cmd-col">tacacs server &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعريف خادم TACACS+.</td>
            <td class="no-col">no tacacs server</td>
        </tr>
        <tr>
            <td class="cmd-col">address ipv4 &lt;ip&gt;</td>
            <td class="mode-col">TACACS Server</td>
            <td>عنوان الخادم.</td>
            <td class="no-col">no address</td>
        </tr>
        <tr>
            <td class="cmd-col">key &lt;pass&gt;</td>
            <td class="mode-col">TACACS Server</td>
            <td>shared secret.</td>
            <td class="no-col">no key</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa group server radius|tacacs+ &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تجميع عدة خوادم في group لتوفير high availability.</td>
            <td class="no-col">no aaa group server</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر 802.1x</div>
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
            <td class="cmd-col">dot1x system-auth-control</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل 802.1x على الجهاز بشكل عام.</td>
            <td class="no-col">no dot1x system-auth-control</td>
        </tr>
        <tr>
            <td class="cmd-col">dot1x critical eapol</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل Critical Authentication (fallback عند فشل RADIUS).</td>
            <td class="no-col">no dot1x critical eapol</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication port-control auto</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل 802.1x على البورت بوضع auto (يطلب مصادقة قبل فتح البورت).</td>
            <td class="no-col">no authentication port-control</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication port-control force-authorized</td>
            <td class="mode-col">Interface Config</td>
            <td>وضع البورت مصرّح دائماً (للبورتات غير المفعّل عليها 802.1x).</td>
            <td class="no-col">no authentication port-control</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication host-mode multi-domain</td>
            <td class="mode-col">Interface Config</td>
            <td>السماح بمضيفين متعددين (data + voice) على نفس البورت.</td>
            <td class="no-col">no authentication host-mode</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication periodic</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل re-authentication الدورية.</td>
            <td class="no-col">no authentication periodic</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication timer reauthenticate &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط فترة re-auth (ساعات/أيام).</td>
            <td class="no-col">no authentication timer</td>
        </tr>
        <tr>
            <td class="cmd-col">mab</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل MAC Authentication Bypass (للأجهزة التي لا تدعم 802.1x مثل الطابعات).</td>
            <td class="no-col">no mab</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد 802.1x + RADIUS + TACACS+</div>
<div class="code-block">
<span class="comment">! إعداد RADIUS لـ 802.1x (مصادقة المستخدمين)</span>
SW1(config)# <span class="prompt">aaa new-model</span>
SW1(config)# <span class="prompt">radius server RADIUS1</span>
SW1(config-radius-server)# <span class="prompt">address ipv4 10.10.10.5 auth-port 1812 acct-port 1813</span>
SW1(config-radius-server)# <span class="prompt">key S3cr3t!R@dius</span>
SW1(config-radius-server)# <span class="prompt">exit</span>

SW1(config)# <span class="prompt">aaa group server radius AAAA-RADIUS</span>
SW1(config-sg-radius)# <span class="prompt">server name RADIUS1</span>
SW1(config-sg-radius)# <span class="prompt">exit</span>

SW1(config)# <span class="prompt">aaa authentication login default group AAAA-RADIUS local</span>
SW1(config)# <span class="prompt">aaa authorization exec default group AAAA-RADIUS local</span>

<span class="comment">! إعداد TACACS+ لـ device admin</span>
SW1(config)# <span class="prompt">tacacs server TAC1</span>
SW1(config-tacacs-server)# <span class="prompt">address ipv4 10.10.10.10</span>
SW1(config-tacacs-server)# <span class="prompt">key T@cacS!Plus</span>
SW1(config-tacacs-server)# <span class="prompt">exit</span>

SW1(config)# <span class="prompt">aaa authentication login ADMIN group TAC1 local</span>
SW1(config)# <span class="prompt">aaa authorization exec ADMIN group TAC1 local</span>
SW1(config)# <span class="prompt">aaa accounting exec ADMIN default start-stop group TAC1</span>

<span class="comment">! تطبيق 802.1x على بورت access</span>
SW1(config)# <span class="prompt">dot1x system-auth-control</span>
SW1(config)# <span class="prompt">interface fastEthernet0/10</span>
SW1(config-if)# <span class="prompt">switchport mode access</span>
SW1(config-if)# <span class="prompt">authentication port-control auto</span>
SW1(config-if)# <span class="prompt">authentication host-mode multi-domain</span>
SW1(config-if)# <span class="prompt">authentication periodic</span>
SW1(config-if)# <span class="prompt">authentication timer reauthenticate 3600</span>
SW1(config-if)# <span class="prompt">mab</span>            <span class="comment">! MAC Authentication Bypass للطابعات</span>
SW1(config-if)# <span class="prompt">exit</span>

<span class="comment">! تطبيق مصادقة TACACS+ على VTY</span>
SW1(config)# <span class="prompt">line vty 0 15</span>
SW1(config-line)# <span class="prompt">login authentication ADMIN</span>
SW1(config-line)# <span class="prompt">exit</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة عملية</div>
    <div class="tip-box-body">
        استخدم دائماً <code class="inline">local</code> كfallback بعد RADIUS/TACACS+ في تكوين AAA. هذا يضمن أنك تستطيع الدخول إلى الجهاز حتى لو فشل خادم RADIUS/TACACS+. أيضاً، اختبر إعداد AAA من جلسة console قبل تطبيقه على VTY، لتفادي القفل عن جهاز إنتاجي. تكوين نموذجي: <code class="inline">aaa authentication login default group TAC1 group AAAA-RADIUS local</code> - يجرب TACACS أولاً، ثم RADIUS، ثم قاعدة محلية.
    </div>
</div>

"""
