# -*- coding: utf-8 -*-
"""Part 07: Section 14 - FHRP + Section 15 - ACLs + Section 16 - NAT"""

SECTIONS_07 = """

<!-- ============ SECTION 14: FHRP - HSRP / VRRP / GLBP ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 14</span>
    <div class="chapter-title">FHRP - HSRP / VRRP / GLBP</div>
    <div class="chapter-title-en">First Hop Redundancy Protocols</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    بروتوكولات FHRP (First Hop Redundancy Protocols) توفر توفيراً متاحاً (High Availability) للـ Default Gateway على المضيفين. بدونها، إن فشل الراوتر الـ gateway، ستتوقف كل المضيفين عن الوصول للإنترنت حتى تُعيد إعدادهم يدوياً بـ gateway جديد. تحل FHRP هذه المشكلة عبر إنشاء <strong>عنوان MAC وهمي</strong> (Virtual MAC) و <strong>عنوان IP وهمي</strong> (Virtual IP) يشاركه راوتران أو أكثر. عند فشل الراوتر الأساسي (Active)، يأخذ الراوتر الثانوي (Standby) الدور تلقائياً خلال ثوانٍ معدودة. ثلاث بروتوكولات شائعة: <strong>HSRP</strong> (Cisco-Proprietary، الأكثر شيوعاً)، <strong>VRRP</strong> (معيار IETF مفتوح RFC 5798)، <strong>GLBP</strong> (Cisco-Proprietary، يدعم Load Balancing على عكس الباقي).
</div>

<div class="section-title">مقارنة بين بروتوكولات FHRP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 18%;">البروتوكول</th>
            <th style="width: 17%;">النوع</th>
            <th style="width: 15%;">RFC</th>
            <th style="width: 15;">Load Balancing</th>
            <th style="width: 35%;">الملاحظة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>HSRPv1</td><td>Cisco</td><td>N/A</td><td>لا</td><td>IPv4 فقط. Active/Standby.</td></tr>
        <tr><td>HSRPv2</td><td>Cisco</td><td>N/A</td><td>لا</td><td>IPv4/IPv6. يدعم Millisecond timers.</td></tr>
        <tr><td>VRRPv3</td><td>IETF</td><td>RFC 5798</td><td>لا (إلا يدوياً)</td><td>Master/Backup. معيار مفتوح.</td></tr>
        <tr><td>GLBP</td><td>Cisco</td><td>N/A</td><td><strong>نعم (تلقائي)</strong></td><td>Active AVF و AVG. يوزع الـ MACs على المضيفين.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر HSRP</div>
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
            <td class="cmd-col">standby &lt;group&gt; ip &lt;virtual-ip&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط Virtual IP لمجموعة HSRP. مثلاً: <code class="inline">standby 1 ip 192.168.1.254</code>.</td>
            <td class="no-col">no standby &lt;group&gt; ip</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; priority &lt;0-255&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط priority (الافتراضي 100). الأعلى يصبح Active.</td>
            <td class="no-col">no standby &lt;group&gt; priority</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; preempt</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل Preempt - يستعيد الراوتر دور Active عندما يكون priority أعلى. <strong>موصى به</strong> لتفادي scenario حيث الراوتر الأقل priority يبقى active.</td>
            <td class="no-col">no standby &lt;group&gt; preempt</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; timers &lt;hello&gt; &lt;hold&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط Hello و Hold timer بالثواني. الافتراضي 3s/10s.</td>
            <td class="no-col">no standby &lt;group&gt; timers</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; timers msec &lt;hello&gt; &lt;hold&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط timers بالملي ثانية (HSRPv2). مثل <code class="inline">standby 1 timers msec 200 800</code>.</td>
            <td class="no-col">no standby &lt;group&gt; timers</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; track &lt;obj&gt; decrement &lt;n&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تتبع حالة واجهة أخرى (مثلاً WAN) وتخفيض priority إن فشلت. يستعمل لتفعيل switchover عند فشل uplink.</td>
            <td class="no-col">no standby &lt;group&gt; track</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; authentication md5 key-chain &lt;name&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل مصادقة MD5 على HSRP.</td>
            <td class="no-col">no standby &lt;group&gt; authentication</td>
        </tr>
        <tr>
            <td class="cmd-col">standby version 2</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل HSRPv2 (يدعم IPv6 و msec timers).</td>
            <td class="no-col">no standby version</td>
        </tr>
        <tr>
            <td class="cmd-col">standby &lt;group&gt; ipv6 &lt;ipv6&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط IPv6 virtual address لـ HSRPv2.</td>
            <td class="no-col">no standby &lt;group&gt; ipv6</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر VRRP</div>
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
            <td class="cmd-col">vrrp &lt;group&gt; ip &lt;virtual-ip&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط VRRP virtual IP.</td>
            <td class="no-col">no vrrp &lt;group&gt; ip</td>
        </tr>
        <tr>
            <td class="cmd-col">vrrp &lt;group&gt; priority &lt;0-255&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط priority (الافتراضي 100).</td>
            <td class="no-col">no vrrp &lt;group&gt; priority</td>
        </tr>
        <tr>
            <td class="cmd-col">vrrp &lt;group&gt; preempt</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل preempt. مفعّل افتراضياً في VRRP.</td>
            <td class="no-col">no vrrp &lt;group&gt; preempt</td>
        </tr>
        <tr>
            <td class="cmd-col">vrrp &lt;group&gt; timers advertise &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط فترة الإعلان.</td>
            <td class="no-col">no vrrp &lt;group&gt; timers</td>
        </tr>
        <tr>
            <td class="cmd-col">vrrp &lt;group&gt; track &lt;obj&gt; decrement &lt;n&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تتبع واجهة وتخفيض priority عند الفشل.</td>
            <td class="no-col">no vrrp &lt;group&gt; track</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر GLBP</div>
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
            <td class="cmd-col">glbp &lt;group&gt; ip &lt;virtual-ip&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط GLBP virtual IP.</td>
            <td class="no-col">no glbp &lt;group&gt; ip</td>
        </tr>
        <tr>
            <td class="cmd-col">glbp &lt;group&gt; priority &lt;0-255&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط priority لانتخاب AVG (Active Virtual Gateway).</td>
            <td class="no-col">no glbp &lt;group&gt; priority</td>
        </tr>
        <tr>
            <td class="cmd-col">glbp &lt;group&gt; preempt</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل preempt لاستعادة دور AVG.</td>
            <td class="no-col">no glbp &lt;group&gt; preempt</td>
        </tr>
        <tr>
            <td class="cmd-col">glbp &lt;group&gt; weighting &lt;weight&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط weight لانتخاب AVF (Active Virtual Forwarder) - يحدد من يقوم بـ forwarding الحركة.</td>
            <td class="no-col">no glbp &lt;group&gt; weighting</td>
        </tr>
        <tr>
            <td class="cmd-col">glbp &lt;group&gt; load-balancing &lt;method&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط طريقة load balancing: <code class="inline">round-robin</code>، <code class="inline">weighted</code>، <code class="inline">host-dependent</code>.</td>
            <td class="no-col">no glbp &lt;group&gt; load-balancing</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض FHRP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 45%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show standby brief</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص HSRP: المجموعات، Active/Standby، priority.</td></tr>
        <tr><td class="cmd-col">show standby</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل كاملة عن HSRP.</td></tr>
        <tr><td class="cmd-col">show vrrp brief</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص VRRP.</td></tr>
        <tr><td class="cmd-col">show glbp brief</td><td class="mode-col">Privileged EXEC</td><td>عرض ملخص GLBP: AVG، AVFs.</td></tr>
        <tr><td class="cmd-col">show vrrp</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل VRRP.</td></tr>
        <tr><td class="cmd-col">show glbp</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل GLBP.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: HSRP بين راوترين</div>
<div class="code-block">
<span class="comment">! على R1 (الأساسي - Active)</span>
R1(config)# <span class="prompt">interface gigabitEthernet0/0</span>
R1(config-if)# <span class="prompt">ip address 192.168.1.2 255.255.255.0</span>
R1(config-if)# <span class="prompt">standby 1 ip 192.168.1.254</span>
R1(config-if)# <span class="prompt">standby 1 priority 110</span>
R1(config-if)# <span class="prompt">standby 1 preempt</span>
R1(config-if)# <span class="prompt">standby 1 timers msec 200 msec 800</span>
R1(config-if)# <span class="prompt">standby 1 track 1 decrement 20</span>      <span class="comment">! track object 1</span>
R1(config-if)# <span class="prompt">exit</span>
R1(config)# <span class="prompt">track 1 interface serial0/0/0 line-protocol</span>
R1(config-track)# <span class="prompt">exit</span>

<span class="comment">! على R2 (الثانوي - Standby)</span>
R2(config)# <span class="prompt">interface gigabitEthernet0/0</span>
R2(config-if)# <span class="prompt">ip address 192.168.1.3 255.255.255.0</span>
R2(config-if)# <span class="prompt">standby 1 ip 192.168.1.254</span>
R2(config-if)# <span class="prompt">standby 1 priority 100</span>      <span class="comment">! افتراضي</span>
R2(config-if)# <span class="prompt">standby 1 preempt</span>
R2(config-if)# <span class="prompt">exit</span>

R1# <span class="prompt">show standby brief</span>
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State    Active          Standby         Virtual IP
Gi0/0       1    110 P  Active  local           192.168.1.3     192.168.1.254
</div>

<div class="info-box">
    <div class="info-box-title">عناوين MAC الافتراضية لكل بروتوكول</div>
    <div class="info-box-body">
        HSRPv1: <code class="inline">0000.0c07.acXX</code> (XX = رقم المجموعة، 0-255).<br>
        HSRPv2: <code class="inline">0000.0c9f.fXXX</code> (XXX = 0-4095).<br>
        VRRP: <code class="inline">0000.5e00.01XX</code> (XX = رقم المجموعة).<br>
        GLBP: <code class="inline">0007.b400.XXYY</code> (XX = group، YY = AVF number).<br>
        <br>
        معرفة عناوين MAC الوهمية مفيدة في تشخيص ARP في الـ packet captures.
    </div>
</div>


<!-- ============ SECTION 15: ACLs ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 15</span>
    <div class="chapter-title">Access Control Lists (ACLs)</div>
    <div class="chapter-title-en">Standard, Extended &amp; IPv6 ACLs</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    ACLs (Access Control Lists) هي قواعد شرطية تُطبّق على حركة المرور عبر واجهة أو بروتوكول، لتقرير إذا كان يجب السماح أو رفض حزمة معينة. تستعمل ACLs في: (1) تصفية حركة المرور (Security)، (2) تحديد حركة معينة لـ NAT، (3) تحديد الشبكات المعلَن عنها في بروتوكولات التوجيه، (4) تقييد الوصول إلى VTY، (5) تحديد حركة لـ QoS. أنواع ACLs الأساسية: <strong>Standard ACL</strong> (القديم، يفحص المصدر فقط - أرقام 1-99 و 1300-1999)، <strong>Extended ACL</strong> (ييفحص المصدر، الوجهة، البروتوكول، البورت - 100-199 و 2000-2699)، <strong>Named ACLs</strong> (القابلة للقراءة، حديثة)، <strong>IPv6 ACLs</strong> (تفاصيل مختلفة).
</div>

<div class="section-title">قواعد ACL الذهبية</div>
<div class="body-text">
    (1) كل ACL تنتهي ضمنياً بقاعدة <code class="inline">deny any</code>. (2) الترتيب مهم جداً - القواعد تُقوّم من الأعلى للأسفل. (3) Standard ACL توضع قرب الوجهة (لتفادي رفض الحركة المنتمية من الوجهة). (4) Extended ACL توضع قرب المصدر (لتوفير عرض النطاق). (5) قاعدة واحدة على الأقل من <code class="inline">permit</code> في ACL وإلا فكل الحركة ستُرفض. (6) لا تنسَ تطبيق الـ ACL على واجهة مع <code class="inline">in</code> أو <code class="inline">out</code>.
</div>

<div class="section-title">أوامر Standard IPv4 ACLs</div>
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
            <td class="cmd-col">access-list &lt;1-99|1300-1999&gt; permit &lt;source&gt; [&lt;wildcard&gt;]</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء قاعدة Standard ACL تسمح بالمصدر. مثل <code class="inline">access-list 10 permit 192.168.1.0 0.0.0.255</code>.</td>
            <td class="no-col">no access-list &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list &lt;id&gt; deny &lt;source&gt; [&lt;wildcard&gt;]</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء قاعدة رفض.</td>
            <td class="no-col">no access-list &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list &lt;id&gt; permit any</td>
            <td class="mode-col">Global Config</td>
            <td>السماح بكل المصادر (صيغة مختصرة لـ <code class="inline">0.0.0.0 255.255.255.255</code>).</td>
            <td class="no-col">no access-list &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list &lt;id&gt; remark &lt;text&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إضافة تعليق للـ ACL.</td>
            <td class="no-col">no access-list &lt;id&gt; remark</td>
        </tr>
        <tr>
            <td class="cmd-col">ip access-group &lt;id&gt; in|out</td>
            <td class="mode-col">Interface Config</td>
            <td>تطبيق ACL على واجهة (داخل أو خارج).</td>
            <td class="no-col">no ip access-group &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">access-class &lt;id&gt; in</td>
            <td class="mode-col">Line Config</td>
            <td>تطبيق ACL على VTY (تحكم بمن يستطيع Telnet/SSH إلى الجهاز).</td>
            <td class="no-col">no access-class &lt;id&gt;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر Extended IPv4 ACLs</div>
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
            <td class="cmd-col">access-list &lt;100-199|2000-2699&gt; permit|deny &lt;protocol&gt; &lt;src&gt; &lt;src-wild&gt; &lt;dst&gt; &lt;dst-wild&gt; [&lt;port-ops&gt;] [&lt;established&gt;]</td>
            <td class="mode-col">Global Config</td>
            <td>قاعدة Extended ACL كاملة. البروتوكول: <code class="inline">ip, tcp, udp, icmp, ...</code>. Port ops: <code class="inline">eq, gt, lt, neq, range</code>.</td>
            <td class="no-col">no access-list &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list 100 permit tcp 192.168.1.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 80</td>
            <td class="mode-col">Global Config</td>
            <td>السماح بـ HTTP من 192.168.1.0/24 إلى 10.0.0.0/24.</td>
            <td class="no-col">no access-list 100 ...</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list 100 permit tcp any 10.0.0.0 0.0.0.255 established</td>
            <td class="mode-col">Global Config</td>
            <td>السماح بـ TCP الرد على اتصال بدأه الطرف الآخر (مفيد لجدار حماية بسيط).</td>
            <td class="no-col">no ...</td>
        </tr>
        <tr>
            <td class="cmd-col">access-list 100 deny icmp any any echo</td>
            <td class="mode-col">Global Config</td>
            <td>رفض ping inbound.</td>
            <td class="no-col">no access-list 100 ...</td>
        </tr>
    </tbody>
</table>

<div class="section-title">Named ACLs (الأكثر استخداماً اليوم)</div>
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
            <td class="cmd-col">ip access-list standard|extended &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء named ACL ودخول وضع الإعداد.</td>
            <td class="no-col">no ip access-list &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">[&lt;seq&gt;] permit|deny &lt;rules&gt;</td>
            <td class="mode-col">Named ACL</td>
            <td>إضافة قاعدة مع sequence number (يدعم ترتيب دقيق وإدراج في موضع محدد).</td>
            <td class="no-col">no &lt;seq&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">&lt;seq&gt; permit ...</td>
            <td class="mode-col">Named ACL</td>
            <td>إدراج قاعدة في موقع محدد. مثلاً: <code class="inline">15 permit tcp any any eq 443</code> لإدراجها قبل القاعدة 20.</td>
            <td class="no-col">no &lt;seq&gt;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">IPv6 ACLs</div>
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
            <td class="cmd-col">ipv6 access-list &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء IPv6 ACL. كل IPv6 ACLs هي named فقط (لا توجد numbered IPv6 ACLs).</td>
            <td class="no-col">no ipv6 access-list &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">permit|deny &lt;protocol&gt; &lt;src&gt;/&lt;len&gt; &lt;dst&gt;/&lt;len&gt;</td>
            <td class="mode-col">IPv6 ACL</td>
            <td>قاعدة IPv6 ACL.</td>
            <td class="no-col">no permit|deny ...</td>
        </tr>
        <tr>
            <td class="cmd-col">ipv6 traffic-filter &lt;name&gt; in|out</td>
            <td class="mode-col">Interface Config</td>
            <td>تطبيق IPv6 ACL على واجهة.</td>
            <td class="no-col">no ipv6 traffic-filter</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض ACLs</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 45%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show access-lists</td><td class="mode-col">Privileged EXEC</td><td>عرض كل ACLs وقواعدها وعدادات التطابق.</td></tr>
        <tr><td class="cmd-col">show access-lists &lt;name|id&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض ACL محدد.</td></tr>
        <tr><td class="cmd-col">show ip access-lists</td><td class="mode-col">Privileged EXEC</td><td>عرض فقط ACLs IPv4.</td></tr>
        <tr><td class="cmd-col">show ipv6 access-list</td><td class="mode-col">Privileged EXEC</td><td>عرض IPv6 ACLs.</td></tr>
        <tr><td class="cmd-col">show ip interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض الـ ACLs المطبّقة على واجهة.</td></tr>
        <tr><td class="cmd-col">clear access-list counters &lt;id&gt;</td><td class="mode-col">Privileged EXEC</td><td>تصفير عدادات التطابق في ACL.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: Extended Named ACL لحماية سيرفر</div>
<div class="code-block">
Router(config)# <span class="prompt">ip access-list extended PROTECT-SERVER</span>
Router(config-ext-nacl)# <span class="prompt">remark Block all access to Server VLAN except HTTP/HTTPS/DNS</span>
Router(config-ext-nacl)# <span class="prompt">10 permit tcp any host 192.168.50.10 eq 80</span>      <span class="comment">! HTTP</span>
Router(config-ext-nacl)# <span class="prompt">20 permit tcp any host 192.168.50.10 eq 443</span>     <span class="comment">! HTTPS</span>
Router(config-ext-nacl)# <span class="prompt">30 permit udp any host 192.168.50.10 eq 53</span>      <span class="comment">! DNS</span>
Router(config-ext-nacl)# <span class="prompt">40 permit tcp any host 192.168.50.10 eq 22</span>      <span class="comment">! SSH from management</span>
Router(config-ext-nacl)# <span class="prompt">50 permit icmp any host 192.168.50.10 echo</span>      <span class="comment">! ping only</span>
Router(config-ext-nacl)# <span class="prompt">100 deny ip any host 192.168.50.10</span>             <span class="comment">! block everything else</span>
Router(config-ext-nacl)# <span class="prompt">200 permit ip any any</span>                         <span class="comment">! allow other traffic</span>
Router(config-ext-nacl)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip access-group PROTECT-SERVER out</span>
Router(config-if)# <span class="prompt">exit</span>

Router# <span class="prompt">show access-lists PROTECT-SERVER</span>
Extended IP access list PROTECT-SERVER
    10 permit tcp any host 192.168.50.10 eq www (5 matches)
    20 permit tcp any host 192.168.50.10 eq 443 (12 matches)
    30 permit udp any host 192.168.50.10 eq domain (45 matches)
    ...
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة لـ Wildcard Mask</div>
    <div class="tip-box-body">
        Wildcard Mask = عكس Subnet Mask. للحصول عليها: <code class="inline">255.255.255.255 - subnet_mask</code>. أمثلة سريعة: <code class="inline">/24</code> → <code class="inline">0.0.0.255</code>، <code class="inline">/25</code> → <code class="inline">0.0.0.127</code>، <code class="inline">/30</code> → <code class="inline">0.0.0.3</code>، <code class="inline">/32</code> → <code class="inline">0.0.0.0</code> (host). لعنوان واحد فقط استخدم <code class="inline">host</code> keyword: <code class="inline">permit ip 10.0.0.1 0.0.0.0 any</code> = <code class="inline">permit ip host 10.0.0.1 any</code>.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">تحذير: Extended ACL على الواجهة الخاطئة</div>
    <div class="warn-box-body">
        ضع Extended ACL دائماً <strong>قرب المصدر</strong> (inbound على الواجهة القريبة من المصدر) لتوفير عرض النطاق ورفض الحركة قبل عبورها الشبكة. ضع Standard ACL قرب الوجهة (outbound على الواجهة الأخيرة) لأنه لا يفحص إلا المصدر، فلو وضعته قرب المصدر قد يرفض حركة مشروعة يجب أن تصل وجهات أخرى.
    </div>
</div>


<!-- ============ SECTION 16: NAT ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 16</span>
    <div class="chapter-title">Network Address Translation</div>
    <div class="chapter-title-en">Static, Dynamic &amp; PAT (NAT Overload)</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    NAT (Network Address Translation) يحوّل عناوين IP الخاصة (RFC 1918: 10.0.0.0/8، 172.16.0.0/12، 192.168.0.0/16) إلى عناوين IP عامة قابلة للتوجيه على الإنترنت. أنواع NAT الأساسية: <strong>Static NAT</strong> (تطابق 1-to-1 يدوي)، <strong>Dynamic NAT</strong> (مجموعة عناوين عامة تُوزع ديناميكياً)، <strong>PAT (NAT Overload)</strong> (يستخدم بورت واحد لعدة مضيفين - الأكثر شيوعاً في المنازل والشركات الصغيرة). يقوم الراوتر بتعريف واجهة <strong>inside</strong> (مواجهة للشبكة الداخلية) وواجهة <strong>outside</strong> (مواجهة للإنترنت). يطبّق NAT على الواجهة ثم تُعرف القواعد بشكل عام.
</div>

<div class="section-title">أوامر NAT العامة</div>
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
            <td class="cmd-col">ip nat inside</td>
            <td class="mode-col">Interface Config</td>
            <td>تعريف الواجهة كـ inside (مواجهة للشبكة الداخلية).</td>
            <td class="no-col">no ip nat inside</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat outside</td>
            <td class="mode-col">Interface Config</td>
            <td>تعريف الواجهة كـ outside (مواجهة للإنترنت).</td>
            <td class="no-col">no ip nat outside</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat inside source static &lt;local-ip&gt; &lt;global-ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>Static NAT - تطابق دائم 1-to-1. مثلاً: <code class="inline">ip nat inside source static 192.168.1.10 203.0.113.10</code>.</td>
            <td class="no-col">no ip nat inside source static &lt;local-ip&gt; &lt;global-ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat inside source static tcp &lt;local&gt; &lt;port&gt; &lt;global&gt; &lt;port&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>Port Forwarding - ترجمة بورت محدد. مثل <code class="inline">ip nat inside source static tcp 192.168.1.10 80 203.0.113.10 80</code>.</td>
            <td class="no-col">no ip nat inside source static tcp ...</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat pool &lt;name&gt; &lt;start&gt; &lt;end&gt; netmask &lt;mask&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء pool عناوين IP عامة لـ Dynamic NAT.</td>
            <td class="no-col">no ip nat pool &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat pool &lt;name&gt; &lt;start&gt; &lt;end&gt; prefix-length &lt;len&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء pool بصيغة CIDR.</td>
            <td class="no-col">no ip nat pool</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat inside source list &lt;acl&gt; pool &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>Dynamic NAT - ترجمة الحركة الموصوفة في ACL إلى pool.</td>
            <td class="no-col">no ip nat inside source list &lt;acl&gt; pool &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat inside source list &lt;acl&gt; interface &lt;iface&gt; overload</td>
            <td class="mode-col">Global Config</td>
            <td><strong>PAT (NAT Overload)</strong> - تستعمل عنوان IP واحد (IP الواجهة) لترجمة كل الحركة الداخلية عبر بورتات متعددة.</td>
            <td class="no-col">no ip nat inside source list ...</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat translation timeout &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط مدة بقاء entries في جدول NAT.</td>
            <td class="no-col">no ip nat translation timeout</td>
        </tr>
        <tr>
            <td class="cmd-col">ip nat translation max-entries &lt;n&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط حد أقصى لعدد entries (مفيد لمنع استنزاف الذاكرة).</td>
            <td class="no-col">no ip nat translation max-entries</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض NAT</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 45%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip nat translations</td><td class="mode-col">Privileged EXEC</td><td>عرض جدول ترجمات NAT النشطة (pro=TCP/UDP، inside local، inside global، outside).</td></tr>
        <tr><td class="cmd-col">show ip nat translations verbose</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل إضافية: مدة الإنشاء، flags.</td></tr>
        <tr><td class="cmd-col">show ip nat statistics</td><td class="mode-col">Privileged EXEC</td><td>عرض إحصائيات NAT: عدد الترجمات، عدد الحدث، peak.</td></tr>
        <tr><td class="cmd-col">clear ip nat translations *</td><td class="mode-col">Privileged EXEC</td><td>مسح كل ترجمات NAT الديناميكية (الثابتة تبقى).</td></tr>
        <tr><td class="cmd-col">clear ip nat translations &lt;args&gt;</td><td class="mode-col">Privileged EXEC</td><td>مسح ترجمات محددة.</td></tr>
        <tr><td class="cmd-col">debug ip nat</td><td class="mode-col">Privileged EXEC</td><td>تصحيح تفصيلي - اعرض كل حزمة مترجمة. تحذير: قد يسبب load عالٍ في الإنتاج!</td></tr>
        <tr><td class="cmd-col">debug ip nat detailed</td><td class="mode-col">Privileged EXEC</td><td>تصحيح أكثر تفصيلاً.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: PAT - ترجمة كل الشبكة إلى IP WAN</div>
<div class="code-block">
<span class="comment">! تعريف inside و outside</span>
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip address 192.168.1.1 255.255.255.0</span>
Router(config-if)# <span class="prompt">ip nat inside</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/1</span>
Router(config-if)# <span class="prompt">ip address 203.0.113.2 255.255.255.252</span>
Router(config-if)# <span class="prompt">ip nat outside</span>
Router(config-if)# <span class="prompt">exit</span>

<span class="comment">! تعريف الحركة التي تترجم</span>
Router(config)# <span class="prompt">access-list 1 permit 192.168.1.0 0.0.0.255</span>

<span class="comment">! PAT - ترجمة كل الحركة إلى IP الواجهة outside</span>
Router(config)# <span class="prompt">ip nat inside source list 1 interface gigabitEthernet0/1 overload</span>

Router# <span class="prompt">show ip nat translations</span>
Pro Inside global       Inside local       Outside local      Outside global
tcp 203.0.113.2:51152   192.168.1.10:51152  8.8.8.8:53         8.8.8.8:53
tcp 203.0.113.2:51211   192.168.1.20:51211  142.250.180.14:443 142.250.180.14:443
</div>

<div class="code-block-title">مثال 16.2: Port Forwarding لسيرفر ويب داخلي</div>
<div class="code-block">
<span class="comment">! نشر السيرفر الداخلي 192.168.1.10:80 على 203.0.113.2:8080</span>
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip nat inside</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/1</span>
Router(config-if)# <span class="prompt">ip nat outside</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">ip nat inside source static tcp 192.168.1.10 80 203.0.113.2 8080 extendable</span>
</div>

<div class="info-box">
    <div class="info-box-title">من داخل إلى خارج: NAT Order of Operations</div>
    <div class="info-box-body">
        ترتيب معالجة الحزمة من داخل إلى خارج: (1) <code class="inline">inbound ACL</code> على الواجهة، (2) <code class="inline">inbound rate-limit/policy</code>، (3) <code class="inline">internal-to-local NAT</code>، (4) <code class="inline">routing lookup</code>، (5) <code class="inline">Crypto map (if applicable)</code>، (6) <code class="inline">outbound ACL</code>، (7) <code class="inline">outbound NAT</code>. للأسفل إلى الداخل، ترتيب معاكس. فهم هذا الترتيب يساعد على تشخيص مشاكل ACL + NAT المتشابكة.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">PAT ومشاكل التطبيقات</div>
    <div class="warn-box-body">
        بعض التطبيقات لا تعمل بشكل صحيح عبر PAT لأنها تضمّن IP في payload (مثل FTP Active، SIP، H.323). الحل: استعمل <code class="inline">ip nat service ...</code> لإصلاح التطبيقات، أو فعّل ALG (Application Layer Gateway). FTP: <code class="inline">ip nat service ftp tcp port 21</code>. أو استخدم FTP Passive Mode الذي لا يضمّن IP. لـ SIP: <code class="inline">ip nat service sip udp 5060</code>.
    </div>
</div>

"""
