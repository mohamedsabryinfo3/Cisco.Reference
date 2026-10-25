# -*- coding: utf-8 -*-
"""Part 06: Section 12 - OSPF v2 & v3 + Section 13 - EIGRP v4 & v6"""

SECTIONS_06 = """

<!-- ============ SECTION 12: OSPF v2 & v3 ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 12</span>
    <div class="chapter-title">OSPF v2 &amp; v3</div>
    <div class="chapter-title-en">Open Shortest Path First - IPv4 &amp; IPv6</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    OSPF (Open Shortest Path First) هو بروتوكول توجيه ديناميكي من نوع Link-State، يقوم على معيار مفتوح RFC 2328 (OSPFv2) و RFC 5340 (OSPFv3). يستعمل خوارزمية Dijkstra (Shortest Path First) لحساب أقصر مسار. يقسّم الـ AS إلى <strong>Areas</strong> لتقليل عبء الـ CPU والذاكرة. الـ Area 0 (Backbone) مركزية وتتصل بها باقي الـ Areas. أنواع الـ Areas: <strong>Normal</strong>، <strong>Stub</strong> (لا يستقبل مسارات خارجية)، <strong>Totally Stubby</strong> (لا يستقبل إلا default route)، <strong>NSSA</strong> (Not-So-Stubby Area - يستقبل مسارات داخلية فقط)، <strong>Totally NSSA</strong>. OSPFv2 يعمل مع IPv4 فقط، بينما OSPFv3 يعمل مع IPv6 (وفي الإصدارات الأحدث يدعم Address Family للبروتوكولين معاً).
</div>

<div class="section-title">أوامر OSPFv2 الأساسية (IPv4)</div>
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
            <td class="cmd-col">router ospf &lt;process-id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية OSPF محلية. الـ process-id رقم محلي (1-65535) لا علاقة له بـ AS.</td>
            <td class="no-col">no router ospf &lt;process-id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">router-id &lt;ip&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط router-id يدوياً. يُفضّل استخدام Loopback IP. إن لم يضبط، يختار OSPF أعلى IP من Loopback أو Interface.</td>
            <td class="no-col">no router-id</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;ip&gt; &lt;wildcard&gt; area &lt;id&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل OSPF على شبكة محددة في area معينة. مثلاً: <code class="inline">network 10.0.0.0 0.0.0.255 area 0</code>.</td>
            <td class="no-col">no network &lt;ip&gt; &lt;wildcard&gt; area &lt;id&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;ip&gt; &lt;wildcard&gt; area 0</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط شبكة في backbone area (Area 0).</td>
            <td class="no-col">no network ...</td>
        </tr>
        <tr>
            <td class="cmd-col">passive-interface &lt;iface&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>منع إرسال OSPF Hellos على واجهة معينة (عادةً LAN facing users). يحتفظ بالإعلان عن الشبكة لكن لا يشكل جيران.</td>
            <td class="no-col">no passive-interface</td>
        </tr>
        <tr>
            <td class="cmd-col">passive-interface default</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط كل الواجهات passive افتراضياً. ثم استخدم <code class="inline">no passive-interface</code> لتفعيل البعض.</td>
            <td class="no-col">no passive-interface default</td>
        </tr>
        <tr>
            <td class="cmd-col">auto-cost reference-bandwidth &lt;Mbps&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط مرجع حساب cost. الافتراضي 100 (يعني: 100Mbps → cost 1). يستحسن ضبطه إلى 1000 أو 10000 في الشبكات الحديثة. <strong>يجب ضبطه على كل الراوترات في الـ AS!</strong></td>
            <td class="no-col">no auto-cost reference-bandwidth</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf cost &lt;1-65535&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط cost يدوياً على واجهة محددة. يتجاوز الحساب التلقائي.</td>
            <td class="no-col">no ip ospf cost</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf priority &lt;0-255&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط priority على broadcast networks لانتخاب DR/BDR. الافتراضي 1. <code class="inline">0</code> = لا يمكن أن يصبح DR/BDR أبداً.</td>
            <td class="no-col">no ip ospf priority</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf hello-interval &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط فترة إرسال Hello. الافتراضي 10s لـ broadcast، 30s لـ NBMA. <strong>يجب أن تتطابق بين الجيران!</strong></td>
            <td class="no-col">no ip ospf hello-interval</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf dead-interval &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط فترة Dead. الافتراضي 4× hello. <strong>يجب أن تتطابق بين الجيران!</strong></td>
            <td class="no-col">no ip ospf dead-interval</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf network &lt;type&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط نوع الشبكة: <code class="inline">broadcast</code>، <code class="inline">non-broadcast</code>، <code class="inline">point-to-point</code>، <code class="inline">point-to-multipoint</code>.</td>
            <td class="no-col">no ip ospf network</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر OSPFv2 المتقدمة</div>
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
            <td class="cmd-col">area &lt;id&gt; range &lt;network&gt; &lt;mask&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تلخيص (summarization) مسارات داخلية على ABR. يقلل عدد LSAs في backbone.</td>
            <td class="no-col">no area &lt;id&gt; range ...</td>
        </tr>
        <tr>
            <td class="cmd-col">area &lt;id&gt; stub</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط area كـ Stub (لا تستقبل LSAs خارجية). يستخدم فيleaf areas.</td>
            <td class="no-col">no area &lt;id&gt; stub</td>
        </tr>
        <tr>
            <td class="cmd-col">area &lt;id&gt; stub no-summary</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط area كـ Totally Stubby (لا يستقبل إلا default route). على ABR فقط.</td>
            <td class="no-col">no area &lt;id&gt; stub no-summary</td>
        </tr>
        <tr>
            <td class="cmd-col">area &lt;id&gt; nssa</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط area كـ NSSA (تستقبل LSAs خارجية نوع 7). يستخدم في areas تحتاج استيراد خارجي لكن يجب أن تكون stub.</td>
            <td class="no-col">no area &lt;id&gt; nssa</td>
        </tr>
        <tr>
            <td class="cmd-col">area &lt;id&gt; nssa no-summary</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط area كـ Totally NSSA (تستقبل LSAs نوع 7 لكن لا inter-area LSAs).</td>
            <td class="no-col">no area &lt;id&gt; nssa no-summary</td>
        </tr>
        <tr>
            <td class="cmd-col">area &lt;id&gt; authentication message-digest</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل مصادقة MD5 على area محددة.</td>
            <td class="no-col">no area &lt;id&gt; authentication</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ospf message-digest-key &lt;id&gt; md5 &lt;key&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط مفتاح MD5 على واجهة.</td>
            <td class="no-col">no ip ospf message-digest-key</td>
        </tr>
        <tr>
            <td class="cmd-col">default-information originate [always]</td>
            <td class="mode-col">Router Config</td>
            <td>إعلان default route في OSPF إن وُجد في الجدول. <code class="inline">always</code> = أعلن حتى لو لم يوجد.</td>
            <td class="no-col">no default-information originate</td>
        </tr>
        <tr>
            <td class="cmd-col">redistribute static subnets</td>
            <td class="mode-col">Router Config</td>
            <td>إعادة توزيع المسارات الثابتة في OSPF.</td>
            <td class="no-col">no redistribute static</td>
        </tr>
        <tr>
            <td class="cmd-col">maximum-paths &lt;1-32&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط أقصى عدد مسارات متساوية لـ ECMP load balancing. الافتراضي 4.</td>
            <td class="no-col">no maximum-paths</td>
        </tr>
    </tbody>
</table>

<div class="section-title">OSPFv3 (IPv6)</div>
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
            <td class="cmd-col">ipv6 router ospf &lt;process-id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية OSPFv3 لـ IPv6.IOS القديم.</td>
            <td class="no-col">no ipv6 router ospf</td>
        </tr>
        <tr>
            <td class="cmd-col">ospfv3 &lt;process-id&gt; ipv6 area &lt;id&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل OSPFv3 على الواجهة مباشرةً (IOS 15+). أسلوب حديث بدلاً من network command.</td>
            <td class="no-col">no ospfv3 &lt;pid&gt; ipv6 area</td>
        </tr>
        <tr>
            <td class="cmd-col">ospfv3 authentication ipsec spi &lt;n&gt; sha1/md5 ...</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل مصادقة IPsec على OSPFv3 (يدعم IPsec أصلاً).</td>
            <td class="no-col">no ospfv3 authentication</td>
        </tr>
        <tr>
            <td class="cmd-col">router-id &lt;ip&gt;</td>
            <td class="mode-col">OSPFv3 Config</td>
            <td>ضبط router-id. مطلوب يدوياً في OSPFv3 لأن لا علاقة له بـ IPv4.</td>
            <td class="no-col">no router-id</td>
        </tr>
    </tbody>
</table>

<div class="section-title">OSPFv3 Address-Family (Unified Mode)</div>
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
            <td class="cmd-col">router ospfv3 &lt;process-id&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية OSPFv3 unification.</td>
            <td class="no-col">no router ospfv3</td>
        </tr>
        <tr>
            <td class="cmd-col">address-family ipv4 unicast</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل address family IPv4.</td>
            <td class="no-col">no address-family ipv4 unicast</td>
        </tr>
        <tr>
            <td class="cmd-col">address-family ipv6 unicast</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل address family IPv6.</td>
            <td class="no-col">no address-family ipv6 unicast</td>
        </tr>
        <tr>
            <td class="cmd-col">ospfv3 &lt;pid&gt; ipv4 area &lt;id&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل OSPFv3 لـ IPv4 على الواجهة.</td>
            <td class="no-col">no ospfv3 &lt;pid&gt; ipv4 area</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أنواع LSAs في OSPF</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 12%;">النوع</th>
            <th style="width: 28%;">الاسم</th>
            <th style="width: 25%;">المصدر</th>
            <th style="width: 35%;">النطاق</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>Type 1</td><td>Router LSA</td><td>كل راوتر</td><td>داخل الـ Area</td></tr>
        <tr><td>Type 2</td><td>Network LSA</td><td>DR</td><td>داخل الـ Area</td></tr>
        <tr><td>Type 3</td><td>Summary LSA</td><td>ABR</td><td>بين Areas</td></tr>
        <tr><td>Type 4</td><td>ASBR Summary LSA</td><td>ABR</td><td>بين Areas</td></tr>
        <tr><td>Type 5</td><td>AS External LSA</td><td>ASBR</td><td>كل الـ AS</td></tr>
        <tr><td>Type 7</td><td>NSSA External LSA</td><td>ASBR داخل NSSA</td><td>داخل NSSA</td></tr>
        <tr><td>Type 9</td><td>Opaque LSA (link-local)</td><td>محدد</td><td>للـ MPLS Traffic Engineering</td></tr>
    </tbody>
</table>

<div class="section-title">انتخاب DR/BDR على شبكات Broadcast</div>
<div class="body-text">
    على شبكات Broadcast (مثل الإيثرنت) أو NBMA، تنتخب OSPF راوتراً رئيسياً (Designated Router - DR) ومساعداً (Backup DR - BDR) لتقليل عدد الجيران. كل الراوترات الأخرى (DROthers) تشارك فقط مع DR و BDR، وليس فيما بينها. الانتخاب قائم على: (1) <strong>أعلى Priority</strong> (الافتراضي 1، 0 يعني لا يمكن أن يكون DR)، (2) عند التعادل، أعلى Router-ID. لذلك لضبط راوتر معين كـ DR، اضبط priority عالياً عليه (مثلاً 100) و 0 على الباقين. انتبه أن انتخاب DR غير قابل للإزاحة - إذا دخل راوتر جديد بـ priority أعلى بعد انتخاب DR، فلن يصبح DR حتى لو أُعيد تحميل OSPF.
</div>

<div class="section-title">أوامر عرض OSPF</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 43%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip ospf neighbor</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران OSPF وحالتهم (FULL، 2-Way، ExStart، إلخ).</td></tr>
        <tr><td class="cmd-col">show ip ospf neighbor detail</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل كل جار: priority، state، DR/BDR.</td></tr>
        <tr><td class="cmd-col">show ip ospf</td><td class="mode-col">Privileged EXEC</td><td>عرض معلومات عملية OSPF: router-id، areas، SPF count.</td></tr>
        <tr><td class="cmd-col">show ip ospf interface</td><td class="mode-col">Privileged EXEC</td><td>عرض OSPF على كل الواجهات: cost، hello/dead، network type.</td></tr>
        <tr><td class="cmd-col">show ip ospf interface &lt;iface&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض OSPF على واجهة محددة.</td></tr>
        <tr><td class="cmd-col">show ip ospf database</td><td class="mode-col">Privileged EXEC</td><td>عرض LSD - قاعدة بيانات حالة الروابط (Link-State Database).</td></tr>
        <tr><td class="cmd-col">show ip ospf database router</td><td class="mode-col">Privileged EXEC</td><td>عرض Type 1 LSAs.</td></tr>
        <tr><td class="cmd-col">show ip ospf database network</td><td class="mode-col">Privileged EXEC</td><td>عرض Type 2 LSAs.</td></tr>
        <tr><td class="cmd-col">show ip ospf border-routers</td><td class="mode-col">Privileged EXEC</td><td>عرض ABRs و ASBRs.</td></tr>
        <tr><td class="cmd-col">show ip route ospf</td><td class="mode-col">Privileged EXEC</td><td>عرض مسارات OSPF في جدول التوجيه.</td></tr>
        <tr><td class="cmd-col">show ipv6 ospf neighbor</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران OSPFv3.</td></tr>
    </tbody>
</table>

<div class="section-title">حالات الجوار في OSPF (Neighbor States)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 22%;">الحالة</th>
            <th style="width: 78%;">الوصف</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">Down</code></td><td>البداية - لا يوجد جوار بعد.</td></tr>
        <tr><td><code class="inline">Init</code></td><td>استقبل Hello من جار لكن اسمه ليس في Hello.</td></tr>
        <tr><td><code class="inline">Two-Way</code></td><td>التأكد من وجود الاتصال ثنائي الاتجاه. على broadcast، الانتخاب يحدث هنا.</td></tr>
        <tr><td><code class="inline">ExStart</code></td><td>التفاوض على Master/Slave و sequence number لـ DBD.</td></tr>
        <tr><td><code class="inline">Exchange</code></td><td>تبادل Database Description (DBD) packets.</td></tr>
        <tr><td><code class="inline">Loading</code></td><td>طلب LSAs مفقودة عبر LSR (Link-State Request).</td></tr>
        <tr><td><code class="inline">Full</code></td><td><strong>الحالة المستقرة</strong> - الـ LSAs متطابقة بين الجارين.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد OSPFv2 Single-Area</div>
<div class="code-block">
Router(config)# <span class="prompt">router ospf 10</span>
Router(config-router)# <span class="prompt">router-id 1.1.1.1</span>
Router(config-router)# <span class="prompt">network 10.0.0.0 0.0.0.255 area 0</span>
Router(config-router)# <span class="prompt">network 192.168.1.0 0.0.0.255 area 0</span>
Router(config-router)# <span class="prompt">passive-interface default</span>
Router(config-router)# <span class="prompt">no passive-interface gigabitEthernet0/0</span>   <span class="comment">! للـ WAN</span>
Router(config-router)# <span class="prompt">auto-cost reference-bandwidth 1000</span>
Router(config-router)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip ospf priority 100</span>          <span class="comment">! ليصبح DR</span>
Router(config-if)# <span class="prompt">ip ospf cost 10</span>
Router(config-if)# <span class="prompt">ip ospf hello-interval 10</span>
Router(config-if)# <span class="prompt">ip ospf dead-interval 40</span>
Router(config-if)# <span class="prompt">exit</span>

Router# <span class="prompt">show ip ospf neighbor</span>

Neighbor ID     Pri   State           Dead Time   Address         Interface
1.1.1.2           1   FULL/BDR        00:00:38    10.0.0.2        GigabitEthernet0/0
1.1.1.3           1   FULL/DROTHER    00:00:38    10.0.0.3        GigabitEthernet0/0
</div>

<div class="code-block-title">مثال 12.2: OSPFv3 Multi-Area</div>
<div class="code-block">
Router(config)# <span class="prompt">ipv6 unicast-routing</span>
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ipv6 enable</span>
Router(config-if)# <span class="prompt">ipv6 address 2001:db8:1::1/64</span>
Router(config-if)# <span class="prompt">ospfv3 1 ipv6 area 0</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">interface gigabitEthernet0/1</span>
Router(config-if)# <span class="prompt">ipv6 enable</span>
Router(config-if)# <span class="prompt">ipv6 address 2001:db8:2::1/64</span>
Router(config-if)# <span class="prompt">ospfv3 1 ipv6 area 1</span>          <span class="comment">! area 1</span>
Router(config-if)# <span class="prompt">exit</span>

Router(config)# <span class="prompt">router ospfv3 1</span>
Router(config-router)# <span class="prompt">router-id 1.1.1.1</span>
Router(config-router)# <span class="prompt">area 1 stub</span>                <span class="comment">! area 1 stub</span>
Router(config-router)# <span class="prompt">exit</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة لـ OSPF في اللاب</div>
    <div class="tip-box-body">
        (1) ضع <code class="inline">router-id</code> دائماً يدوياً لتجنب تغييره عند إضافة واجهات. (2) اضبط <code class="inline">auto-cost reference-bandwidth 1000</code> على كل الراوترات لتجنب اختلاف cost بين الراوترات في الشبكة. (3) استخدم <code class="inline">passive-interface default</code> و <code class="inline">no passive-interface</code> على الواجهات الفعلية، لتقليل حركة OSPF على بورتات LAN. (4) للحصول على جوار <code class="inline">FULL</code>، تأكد من تطابق hello/dead بين الجيران، وألا يوجد ACL يمنع بروتوكول 89.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">خطأ شائع: Wildcard vs Subnet Mask</div>
    <div class="warn-box-body">
        OSPF يستعمل <strong>wildcard mask</strong> وليس subnet mask. الفرق: <code class="inline">255.255.255.0</code> كقناع شبكة → <code class="inline">0.0.0.255</code> كـ wildcard (معكوس). كتابة <code class="inline">network 10.0.0.0 255.255.255.0 area 0</code> خطأ شائع جداً - سيُرفضه IOS أو يعطي نتيجة خاطئة. لذلك احفظ: <code class="inline">255.255.255.0</code> ← <code class="inline">0.0.0.255</code>، <code class="inline">255.255.0.0</code> ← <code class="inline">0.0.255.255</code>، <code class="inline">255.0.0.0</code> ← <code class="inline">0.255.255.255</code>.
    </div>
</div>


<!-- ============ SECTION 13: EIGRP v4 & v6 ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 13</span>
    <div class="chapter-title">EIGRP v4 &amp; v6</div>
    <div class="chapter-title-en">Enhanced Interior Gateway Routing Protocol</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    EIGRP (Enhanced Interior Gateway Routing Protocol) هو بروتوكول توجيه هجين (Hybrid) طورته سيسكو أصلاً، ثم أصبح معياراً مفتوحاً في RFC 7868. يجمع EIGRP بين مزايا Distance-Vector (سهولة الإعداد) و Link-State (رؤية كاملة للطوبولوجيا عبر DUAL). يمتاز بـ: (1) تقارب سريع جداً (milliseconds) عبر خوارزمية DUAL و Feasible Successor، (2) استخدام متعدد للمسارات المتساوية وغير المتساوية (ECMP و WCMP)، (3) دعم VLSM، (4) تصرف كـ classless افتراضياً، (5) حركة تحكم محدودة (Hello فقط في الوضع المستقر). أنواع EIGRP الأساسية: <strong>Classic Mode</strong> (القديم بـ AS)، <strong>Named Mode</strong> (الحديث بـ address-family).
</div>

<div class="section-title">أوامر EIGRP Classic Mode</div>
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
            <td class="cmd-col">router eigrp &lt;AS&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية EIGRP بـ AS محدد. كل الراوترات في نفس الـ AS يجب أن تستعمل نفس الرقم. AS 1-65535.</td>
            <td class="no-col">no router eigrp &lt;AS&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">eigrp router-id &lt;ip&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط router-id يدوياً. مطلوب لتفادي انتقاء IP عشوائي.</td>
            <td class="no-col">no eigrp router-id</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;network&gt; &lt;wildcard&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل EIGRP على شبكة. <code class="inline">network 10.0.0.0 0.0.0.255</code>.</td>
            <td class="no-col">no network &lt;network&gt; &lt;wildcard&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;network&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>صيغة classful تلقائية (القناع يأتي من الواجهة). قديم - لا يفضل.</td>
            <td class="no-col">no network &lt;network&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">passive-interface &lt;iface&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>منع إرسال Hellos على واجهة.</td>
            <td class="no-col">no passive-interface</td>
        </tr>
        <tr>
            <td class="cmd-col">passive-interface default</td>
            <td class="mode-col">Router Config</td>
            <td>ضبط كل الواجهات passive افتراضياً.</td>
            <td class="no-col">no passive-interface default</td>
        </tr>
        <tr>
            <td class="cmd-col">no auto-summary</td>
            <td class="mode-col">Router Config</td>
            <td>تعطيل auto-summary (summarization عند حدود classful). <strong>مطلوب</strong> في الشبكات الحديثة - تعطله افتراضياً في IOS 15+.</td>
            <td class="no-col">auto-summary</td>
        </tr>
        <tr>
            <td class="cmd-col">variance &lt;1-128&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل Unequal Cost Load Balancing. <code class="inline">variance 2</code> = استعمل مسارات حتى 2× metric الأقل.</td>
            <td class="no-col">no variance</td>
        </tr>
        <tr>
            <td class="cmd-col">maximum-paths &lt;1-32&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>أقصى عدد مسارات لـ ECMP. الافتراضي 4.</td>
            <td class="no-col">no maximum-paths</td>
        </tr>
        <tr>
            <td class="cmd-col">redistribute static</td>
            <td class="mode-col">Router Config</td>
            <td>إعادة توزيع المسارات الثابتة في EIGRP.</td>
            <td class="no-col">no redistribute static</td>
        </tr>
        <tr>
            <td class="cmd-col">redistribute connected</td>
            <td class="mode-col">Router Config</td>
            <td>إعادة توزيع الشبكات المتصلة مباشرة.</td>
            <td class="no-col">no redistribute connected</td>
        </tr>
        <tr>
            <td class="cmd-col">default-information originate</td>
            <td class="mode-col">Router Config</td>
            <td>إعلان default route في EIGRP.</td>
            <td class="no-col">no default-information originate</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر EIGRP على الواجهة</div>
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
            <td class="cmd-col">ip hello-interval eigrp &lt;AS&gt; &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط فترة Hello. الافتراضي 5s (وصلات سريعة)، 60s (وصلات NBMA &lt;1.544Mbps).</td>
            <td class="no-col">no ip hello-interval eigrp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip hold-time eigrp &lt;AS&gt; &lt;sec&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط Hold Time. الافتراضي 3× hello.</td>
            <td class="no-col">no ip hold-time eigrp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip bandwidth-percent eigrp &lt;AS&gt; &lt;percent&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>نسبة عرض النطاق المسموح لحركة EIGRP. الافتراضي 50%.</td>
            <td class="no-col">no ip bandwidth-percent eigrp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip summary-address eigrp &lt;AS&gt; &lt;network&gt; &lt;mask&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>تلخيص مسارات EIGRP على واجهة محددة.</td>
            <td class="no-col">no ip summary-address eigrp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip authentication mode eigrp &lt;AS&gt; md5</td>
            <td class="mode-col">Interface Config</td>
            <td>تفعيل مصادقة MD5 على EIGRP.</td>
            <td class="no-col">no ip authentication mode eigrp</td>
        </tr>
        <tr>
            <td class="cmd-col">ip authentication key-chain eigrp &lt;AS&gt; &lt;chain&gt;</td>
            <td class="mode-col">Interface Config</td>
            <td>ضبط key chain للمصادقة.</td>
            <td class="no-col">no ip authentication key-chain eigrp</td>
        </tr>
    </tbody>
</table>

<div class="section-title">EIGRP Named Mode (Address Family)</div>
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
            <td class="cmd-col">router eigrp &lt;virtual-name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء عملية EIGRP بـ named instance (string). أسلوب حديث.</td>
            <td class="no-col">no router eigrp &lt;virtual-name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">address-family ipv4 unicast autonomous-system &lt;AS&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل address-family IPv4 وتحديد AS.</td>
            <td class="no-col">no address-family ipv4 unicast</td>
        </tr>
        <tr>
            <td class="cmd-col">address-family ipv6 unicast autonomous-system &lt;AS&gt;</td>
            <td class="mode-col">Router Config</td>
            <td>تفعيل address-family IPv6.</td>
            <td class="no-col">no address-family ipv6 unicast</td>
        </tr>
        <tr>
            <td class="cmd-col">network &lt;network&gt; &lt;wildcard&gt;</td>
            <td class="mode-col">AF Config</td>
            <td>تفعيل EIGRP على شبكة (داخل address-family).</td>
            <td class="no-col">no network ...</td>
        </tr>
        <tr>
            <td class="cmd-col">af-interface &lt;iface&gt;</td>
            <td class="mode-col">AF Config</td>
            <td>الدخول إلى وضع إعداد واجهة في الـ AF.</td>
            <td class="no-col">no af-interface &lt;iface&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">passive-interface</td>
            <td class="mode-col">AF-Interface</td>
            <td>ضبط الواجهة كـ passive.</td>
            <td class="no-col">no passive-interface</td>
        </tr>
        <tr>
            <td class="cmd-col">authentication mode md5</td>
            <td class="mode-col">AF-Interface</td>
            <td>تفعيل MD5 على الواجهة.</td>
            <td class="no-col">no authentication mode</td>
        </tr>
    </tbody>
</table>

<div class="section-title">حساب Metric في EIGRP</div>
<div class="body-text">
    صيغة Metric الكلاسيكية (EIGRP Classic): <code class="inline">Metric = 256 × (K1×BW + K3×Delay) × 256 / K2.../256</code>. K-values افتراضية: K1=1 (bandwidth)، K3=1 (delay)، الباقي 0. لذلك: <code class="inline">Metric = (10^7/min-bandwidth + sum-delays/10) × 256</code>. في IOS 15+، EIGRP يدعم Wide Metric بصيغة 64-bit لتفادي القيم الصفرية على وصلات 10G+.
</div>

<div class="section-title">مفاهيم DUAL الأساسية</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">المصطلح</th>
            <th style="width: 72%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><strong>Feasible Distance (FD)</strong></td><td>أقل تكلفة محسوبة من الراوتر للوجهة.</td></tr>
        <tr><td><strong>Reported Distance (RD)</strong></td><td>التكلفة كما يعلنها الجار (التكلفة من الجار إلى الوجهة).</td></tr>
        <tr><td><strong>Feasibility Condition (FC)</strong></td><td>RD &lt; FD الحالي. شرط أن يصبح الجار Successor Backup.</td></tr>
        <tr><td><strong>Successor</strong></td><td>الجار الذي يستعمله الراوتر للوصول إلى الوجهة (الأقل metric).</td></tr>
        <tr><td><strong>Feasible Successor (FS)</strong></td><td>جار احتياطي يحقق FC. يستعمل فوراً عند فشل Successor بدون انتظار إعادة حساب.</td></tr>
        <tr><td><strong>Active State</strong></td><td>حالة يبحث فيها الراوتر عن مسار بديل - ترسل Query لكل الجيران. تجنبه!</td></tr>
        <tr><td><strong>Passive State</strong></td><td>الحالة الطبيعية المستقرة - الراوتر يعرف مساره.</td></tr>
        <tr><td><strong>Stuck in Active (SIA)</strong></td><td>الراوتر لم يتلقّ Reply على Query خلال الوقت المحدد - مشكلة خطيرة قد تسبب إعادة ضبط الجيران.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر عرض EIGRP</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 40%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 43%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip eigrp neighbors</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران EIGRP وحالتهم و queue count.</td></tr>
        <tr><td class="cmd-col">show ip eigrp neighbors detail</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل كل جار: version، retransmissions.</td></tr>
        <tr><td class="cmd-col">show ip eigrp topology</td><td class="mode-col">Privileged EXEC</td><td>عرض طوبولوجيا EIGRP: كل المسارات Successors و FSs.</td></tr>
        <tr><td class="cmd-col">show ip eigrp topology &lt;network&gt;</td><td class="mode-col">Privileged EXEC</td><td>عرض تفاصيل مسار محدد: FD، RD، Successors، FSs.</td></tr>
        <tr><td class="cmd-col">show ip eigrp interfaces</td><td class="mode-col">Privileged EXEC</td><td>عرض الواجهات المفعّل عليها EIGRP: peers، packets.</td></tr>
        <tr><td class="cmd-col">show ip eigrp traffic</td><td class="mode-col">Privileged EXEC</td><td>عرض إحصائيات الحزم: Hellos، Updates، Queries، Replies.</td></tr>
        <tr><td class="cmd-col">show ip route eigrp</td><td class="mode-col">Privileged EXEC</td><td>عرض مسارات EIGRP في جدول التوجيه.</td></tr>
        <tr><td class="cmd-col">show ipv6 eigrp neighbors</td><td class="mode-col">Privileged EXEC</td><td>عرض جيران EIGRP IPv6.</td></tr>
        <tr><td class="cmd-col">show ip protocols</td><td class="mode-col">Privileged EXEC</td><td>عرض معلومات كل بروتوكولات التوجيه النشطة.</td></tr>
    </tbody>
</table>

<div class="section-title">مثال: EIGRP Classic Single AS</div>
<div class="code-block">
Router(config)# <span class="prompt">router eigrp 100</span>
Router(config-router)# <span class="prompt">eigrp router-id 1.1.1.1</span>
Router(config-router)# <span class="prompt">no auto-summary</span>
Router(config-router)# <span class="prompt">network 10.0.0.0 0.0.0.255</span>
Router(config-router)# <span class="prompt">network 192.168.1.0 0.0.0.255</span>
Router(config-router)# <span class="prompt">passive-interface default</span>
Router(config-router)# <span class="prompt">no passive-interface gigabitEthernet0/0</span>
Router(config-router)# <span class="prompt">variance 2</span>
Router(config-router)# <span class="prompt">maximum-paths 4</span>
Router(config-router)# <span class="prompt">exit</span>

<span class="comment">! تلخيص على واجهة</span>
Router(config)# <span class="prompt">interface gigabitEthernet0/0</span>
Router(config-if)# <span class="prompt">ip summary-address eigrp 100 192.168.0.0 255.255.252.0</span>
Router(config-if)# <span class="prompt">ip authentication mode eigrp 100 md5</span>
Router(config-if)# <span class="prompt">ip authentication key-chain eigrp 100 EIGRP-KEYS</span>
Router(config-if)# <span class="prompt">exit</span>

<span class="comment">! ضبط key chain</span>
Router(config)# <span class="prompt">key chain EIGRP-KEYS</span>
Router(config-keychain)# <span class="prompt">key 1</span>
Router(config-keychain-key)# <span class="prompt">key-string S3cr3t!Pass</span>
Router(config-keychain-key)# <span class="prompt">exit</span>

Router# <span class="prompt">show ip eigrp topology</span>
P 192.168.1.0/24, 1 successors, FD is 3011840
        via 10.0.0.2 (3011840/28160), GigabitEthernet0/0
        via 10.0.0.3 (40514560/281600), GigabitEthernet0/1
<span class="comment">! 10.0.0.2 = Successor، 10.0.0.3 = FS لأن RD (281600) &lt; FD (3011840)</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة عملية</div>
    <div class="tip-box-body">
        لا تنس <code class="inline">no auto-summary</code> أبداً في الشبكات الحديثة! بدونها، يقوم EIGRP بتلخيص على حدود classful (مثلاً 10.0.0.0/8) مما قد يسبب مشكلة مسارات خاطئة. في IOS 15+ هذا التعطيل أصبح افتراضياً، لكن في الإصدارات الأقدم يجب ضبطه يدوياً. وللـ Load Balancing، استعمل <code class="inline">variance 2</code> لتفعيل Unequal Cost Load Balancing (UCMP) - ميزة فريدة في EIGRP لا توجد في OSPF.
    </div>
</div>

"""
