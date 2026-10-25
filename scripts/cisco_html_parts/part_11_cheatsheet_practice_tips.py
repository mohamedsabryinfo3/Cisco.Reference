# -*- coding: utf-8 -*-
"""Part 11: Section 25 - Cheat Sheet + Section 26 - Practice Questions + Section 27 - Exam Tips"""

SECTIONS_11 = """

<!-- ============ SECTION 25: CHEAT SHEET ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 25</span>
    <div class="chapter-title">Cheat Sheet - صفحة المرجع السريع</div>
    <div class="chapter-title-en">Quick Reference Card</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    صفحة مرجعية سريعة لأهم الأوامر مصنّفة حسب الوظيفة. احفظ هذه الصفحة جيداً لأنها أكثر ما يُسأل عنه في الامتحانات العملية والنظرية.
</div>

<div class="section-title">أوامر العرض الأكثر استخداماً</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 50%;">الأمر</th>
            <th style="width: 50%;">الاستخدام</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">show ip interface brief</td><td>عرض حالة كل الواجهات</td></tr>
        <tr><td class="cmd-col">show running-config</td><td>الإعداد الحالي الكامل</td></tr>
        <tr><td class="cmd-col">show ip route</td><td>جدول التوجيه</td></tr>
        <tr><td class="cmd-col">show ip ospf neighbor</td><td>جيران OSPF</td></tr>
        <tr><td class="cmd-col">show ip eigrp neighbors</td><td>جيران EIGRP</td></tr>
        <tr><td class="cmd-col">show ip bgp summary</td><td>ملخص BGP</td></tr>
        <tr><td class="cmd-col">show vlan brief</td><td>كل VLANs والبورتات</td></tr>
        <tr><td class="cmd-col">show interfaces trunk</td><td>كل بورتات الـ trunk</td></tr>
        <tr><td class="cmd-col">show mac address-table</td><td>جدول MAC</td></tr>
        <tr><td class="cmd-col">show cdp neighbors</td><td>جيران CDP</td></tr>
        <tr><td class="cmd-col">show spanning-tree</td><td>STP</td></tr>
        <tr><td class="cmd-col">show ip nat translations</td><td>ترجمات NAT</td></tr>
        <tr><td class="cmd-col">show access-lists</td><td>ACLs والعدادات</td></tr>
        <tr><td class="cmd-col">show version</td><td>إصدار IOS</td></tr>
        <tr><td class="cmd-col">show standby brief</td><td>HSRP</td></tr>
        <tr><td class="cmd-col">show port-security interface &lt;iface&gt;</td><td>Port Security</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر الإعداد الأساسية</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الوظيفة</th>
            <th style="width: 65%;">الأمر</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>تغيير اسم الجهاز</td><td class="cmd-col">hostname &lt;name&gt;</td></tr>
        <tr><td>تفعيل الواجهة</td><td class="cmd-col">no shutdown</td></tr>
        <tr><td>تعيين IP</td><td class="cmd-col">ip address &lt;ip&gt; &lt;mask&gt;</td></tr>
        <tr><td>كلمة مرور enable</td><td class="cmd-col">enable secret &lt;pass&gt;</td></tr>
        <tr><td>إنشاء مستخدم</td><td class="cmd-col">username &lt;name&gt; privilege 15 secret &lt;pass&gt;</td></tr>
        <tr><td>تفعيل SSH</td><td class="cmd-col">crypto key generate rsa modulus 2048</td></tr>
        <tr><td>السماح بـ SSH فقط على VTY</td><td class="cmd-col">transport input ssh</td></tr>
        <tr><td>حفظ الإعداد</td><td class="cmd-col">copy run start</td></tr>
        <tr><td>إعادة التحميل</td><td class="cmd-col">reload</td></tr>
        <tr><td>إنشاء VLAN</td><td class="cmd-col">vlan &lt;id&gt; + name &lt;name&gt;</td></tr>
        <tr><td>ضبط access port</td><td class="cmd-col">switchport mode access + switchport access vlan &lt;id&gt;</td></tr>
        <tr><td>ضبط trunk</td><td class="cmd-col">switchport trunk encapsulation dot1q + switchport mode trunk</td></tr>
        <tr><td>Default route</td><td class="cmd-col">ip route 0.0.0.0 0.0.0.0 &lt;next-hop&gt;</td></tr>
        <tr><td>تفعيل OSPF</td><td class="cmd-col">router ospf 1 + network &lt;net&gt; &lt;wildcard&gt; area 0</td></tr>
        <tr><td>تفعيل EIGRP</td><td class="cmd-col">router eigrp 100 + network &lt;net&gt; &lt;wildcard&gt; + no auto-summary</td></tr>
        <tr><td>تفعيل NAT/PAT</td><td class="cmd-col">ip nat inside source list &lt;acl&gt; interface &lt;iface&gt; overload</td></tr>
        <tr><td>HSRP Active</td><td class="cmd-col">standby 1 ip &lt;vip&gt; + standby 1 priority 110 + standby 1 preempt</td></tr>
    </tbody>
</table>

<div class="section-title">قيم يجب حفظها</div>
<table class="subnet-table">
    <thead>
        <tr>
            <th>القيمة</th>
            <th>المعنى</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>0x2102</td><td>config-register افتراضي (حمّل IOS + startup-config)</td></tr>
        <tr><td>0x2142</td><td>config-register لاستعادة كلمة المرور (تجاهل startup-config)</td></tr>
        <tr><td>0x2100</td><td>config-register لـ ROM Monitor</td></tr>
        <tr><td>AD 0/1</td><td>Directly connected / Static</td></tr>
        <tr><td>AD 90</td><td>EIGRP Internal</td></tr>
        <tr><td>AD 110</td><td>OSPF</td></tr>
        <tr><td>AD 120</td><td>RIP</td></tr>
        <tr><td>AD 20/200</td><td>eBGP / iBGP</td></tr>
        <tr><td>TCP 22</td><td>SSH</td></tr>
        <tr><td>TCP 23</td><td>Telnet</td></tr>
        <tr><td>UDP 67/68</td><td>DHCP Server/Client</td></tr>
        <tr><td>UDP 53</td><td>DNS</td></tr>
        <tr><td>UDP 69</td><td>TFTP</td></tr>
        <tr><td>UDP 123</td><td>NTP</td></tr>
        <tr><td>UDP 161/162</td><td>SNMP / SNMP Trap</td></tr>
        <tr><td>TCP 179</td><td>BGP</td></tr>
        <tr><td>UDP 520</td><td>RIP</td></tr>
        <tr><td>Proto 89</td><td>OSPF</td></tr>
        <tr><td>Proto 88</td><td>EIGRP</td></tr>
    </tbody>
</table>

<div class="section-title">أخطاء شائعة تمنعها</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">المشكلة</th>
            <th style="width: 65%;">الحل</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>الواجهة administratively down</td><td>ضبط <code class="inline">no shutdown</code> على الواجهة</td></tr>
        <tr><td>OSPF لا يشكل جوار</td><td>تطابق hello/dead، تطابق area، تطابق authentication، ACL لا يحجب proto 89</td></tr>
        <tr><td>لا يمكن SSH على VTY</td><td>ضبط <code class="inline">login local</code> + إنشاء username + توليد RSA keys + <code class="inline">transport input ssh</code></td></tr>
        <tr><td>NAT لا يترجم</td><td>تأكد من <code class="inline">ip nat inside/outside</code> على الواجهات الصحيحة + ACL تسمح بالشبكة</td></tr>
        <tr><td>Trunk لا يمرر VLAN</td><td>تأكد أن VLAN موجود على كلا السويتشين + في قائمة allowed</td></tr>
        <tr><td>HSRP لا يعمل</td><td>تأكد من تطابق group number و virtual IP على كلا الراوترين</td></tr>
        <tr><td>BGP stuck in Idle</td><td>تأكد من IP الجار و remote-as + connectivity TCP 179</td></tr>
        <tr><td>ACL لا يحجب</td><td>تأكد من تطبيقها على الواجهة بالاتجاه الصحيح (in/out)</td></tr>
    </tbody>
</table>


<!-- ============ SECTION 26: PRACTICE QUESTIONS ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 26</span>
    <div class="chapter-title">أسئلة الممارسة مع الإجابات</div>
    <div class="chapter-title-en">Practice Questions with Detailed Answers</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    مجموعة من الأسئلة العملية محاكية لأسلوب امتحان CCNA 200-301. يغطي كل سؤال مفهوماً أساسياً يجب على كل مهندس شبكات إتقانه. حاول حل السؤال قبل النظر إلى الإجابة.
</div>

<div class="question-block">
    <span class="question-num">Q1</span>
    <span class="question-text">ما هو الوضع الذي يدخله المستخدم بعد تنفيذ أمر <code class="inline">configure terminal</code> بنجاح؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> Global Configuration Mode (وضع الإعداد العام). الموجّه (Prompt) يتغير من <code class="inline">Router#</code> إلى <code class="inline">Router(config)#</code>. من هذا الوضع يمكن الدخول إلى أوضاع فرعية مثل Interface Config أو Router Config.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q2</span>
    <span class="question-text">ما الفرق بين <code class="inline">enable password</code> و <code class="inline">enable secret</code>؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <code class="inline">enable password</code> يخزّن كلمة المرور كنص ظاهر (Type 0) أو بشفرة Type 7 الضعيفة إن فُعّل <code class="inline">service password-encryption</code>. أما <code class="inline">enable secret</code> فيستخدم MD5 (Type 5) أو SHA256/Scrypt (Type 8/9) - أقوى بكثير. <strong>استعمل دائماً enable secret.</strong>
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q3</span>
    <span class="question-text">كم عدد العناوين المضيفين المتاحة في شبكة /28؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> 14 مضيف. الحساب: /28 = 32-28 = 4 host bits. <code class="inline">2^4 = 16</code> عناوين، نطرح 2 (network و broadcast) = 14.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q4</span>
    <span class="question-text">ما الـ Wildcard Mask المقابل لـ Subnet Mask <code class="inline">255.255.255.240</code>؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <code class="inline">0.0.0.15</code>. القاعدة: <code class="inline">255.255.255.255 - 255.255.255.240 = 0.0.0.15</code>.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q5</span>
    <span class="question-text">أي بروتوكول يستعمل Multicast ff02::5؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> OSPF (لإرسال Hello packets). ff02::6 للـ DR/BDR، ff02::a لـ EIGRP، ff02::2 لكل الراوترات، ff02::1 لكل الأجهزة على link.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q6</span>
    <span class="question-text">ما الفرق بين <code class="inline">exit</code> و <code class="inline">end</code> في Cisco IOS؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <code class="inline">exit</code> يخرج من الوضع الحالي إلى الوضع الأب المباشر (مثلاً من Interface Config إلى Global Config). <code class="inline">end</code> (أو <code class="inline">Ctrl+Z</code>) يخرج مباشرة من أي وضع فرعي إلى Privileged EXEC (<code class="inline">Router#</code>).
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q7</span>
    <span class="question-text">ما القيمة الافتراضية لـ Configuration Register؟ وماذا تعمل؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <code class="inline">0x2102</code>. تعني: حمّل iOS من flash، حمّل startup-config من NVRAM، عطّل console break (مرة واحدة فقط بعد 60 ثانية).
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q8</span>
    <span class="question-text">إذا أردت منع جهاز من أن يصبح DR في OSPF على broadcast network، ماذا تضبط؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> اضبط <code class="inline">ip ospf priority 0</code> على الواجهة. الـ priority 0 يعني أن الراوتر لن يكون DR أو BDR أبداً. الافتراضي 1.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q9</span>
    <span class="question-text">ما الفرق بين Standard و Extended ACL؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <strong>Standard ACL</strong> (1-99، 1300-1999) يفحص المصدر فقط. <strong>Extended ACL</strong> (100-199، 2000-2699) يفحص المصدر، الوجهة، البروتوكول، البورت. Standard توضع قرب الوجهة، Extended قرب المصدر.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q10</span>
    <span class="question-text">لماذا يجب ضبط <code class="inline">no auto-summary</code> في EIGRP؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> بدونها، يقوم EIGRP بتلخيص المسارات على حدود classful (مثلاً 10.0.0.0/8 بدلاً من 10.1.0.0/16) مما قد يسبب مسارات خاطئة في الشبكات الحديثة. في IOS 15+ هذا التعطيل أصبح افتراضياً، لكن في الإصدارات الأقدم يجب ضبطه يدوياً.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q11</span>
    <span class="question-text">ما الـ Administrative Distance لـ OSPF؟ ولماذا يفضّل OSPF على RIP؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> AD OSPF = 110. يفضّل OSPF على RIP لـ: (1) تقارب أسرع بكثير، (2) يدعم VLSM، (3) يدعم Areas لتقسيم الـ AS، (4) يحسب المسار الأقصر (Dijkstra) بدل الاعتماد على hop count فقط، (5) لا يحدد 15 hop كحد أقصى.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q12</span>
    <span class="question-text">ما هو الـ BPDU Guard ومتى تستخدمه؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> BPDU Guard يحظر بورت access إن استلم BPDU (سويتش متصل غير مصرّح به). يوضع البورت في errdisabled. <strong>يستعمل فقط على بورتات Access</strong> (مع PortFast)، لا على Trunks. تفعّله بـ <code class="inline">spanning-tree portfast bpduguard default</code>.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q13</span>
    <span class="question-text">كم عدد الـ BGP AS في العالم تقريباً؟ ولماذا يستعمل TCP بدل UDP؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> أكثر من 70,000 AS نشط. يستعمل TCP port 179 لـ: (1) موثوقية (BGP يحمل 400K+ routes، فلا يمكن تحمل فقدان updates)، (2) تحكم تدفق، (3) إعادة إرسال تلقائي للحزم المفقودة.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q14</span>
    <span class="question-text">ما الـ Next-Hop في iBGP ولماذا نحتاج <code class="inline">next-hop-self</code>؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> في iBGP، next-hop لا يتغير افتراضياً (يبقى نفس قيمة eBGP). لو كان next-hop لعنوان IP لا يعرفه الـ iBGP router، لن يستطيع الوصول إليه. الحل: ضبط <code class="inline">neighbor &lt;ip&gt; next-hop-self</code> ليصبح الراوتر المحلي هو الـ next-hop.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q15</span>
    <span class="question-text">كيف تولّد link-local address تلقائياً في IPv6؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> يبدأ prefix <code class="inline">fe80::/10</code>، ثم host portion يولّد بـ EUI-64 من MAC: (1) إدراج <code class="inline">FFFE</code> في وسط الـ MAC (24-بت الأول + FFFE + 24-بت الثاني)، (2) قلب البت السابع في أول أوكتات. مثلاً: MAC 00:1A:2B:3C:4D:5E → link-local <code class="inline">fe80::21a:2bff:fe3c:4d5e</code>.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q16</span>
    <span class="question-text">ما الفرق بين HSRP و VRRP؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> HSRP Cisco-Proprietary، VRRP معيار IETF مفتوح (RFC 5798). HSRP: Active/Standby، MAC <code class="inline">0000.0c07.acXX</code>. VRRP: Master/Backup، MAC <code class="inline">0000.5e00.01XX</code>. VRRP مفعّل preempt افتراضياً، HSRP لا. كلاهما لا يدعم Load Balancing تلقائياً (إلا بضبط متعدد المجموعات).
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q17</span>
    <span class="question-text">كم عدد الـ VLANs الممكنة في شبكة 802.1Q؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> 4094 VLANs (1-4094). VLAN 1 محجوز (default)، 1002-1005 محجوزة (FDDI/Token Ring)، 1006-4094 هي extended VLANs. فعلياً، الاستخدام العملي نادراً يتجاوز 200-300 VLAN.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q18</span>
    <span class="question-text">ما الفرق بين Policing و Shaping في QoS؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <strong>Policing</strong>: يرمي الحزمة الفائضة عن المعدل (drop). يستعمل على حدود ISP-Customer. <strong>Shaping</strong>: يؤجل الحزمة في طابور لإرسالها لاحقاً. يستعمل على حدود Customer-ISP (يحافظ على TCP sessions). Policing صارم، Shaping أنعم.
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q19</span>
    <span class="question-text">ما الفرق بين RADIUS و TACACS+؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> RADIUS (IETF، UDP 1812) يشفّر password فقط، يدمج AAA في حزمة واحدة، أمثل لمصادقة المستخدمين (802.1x، VPN). TACACS+ (Cisco-Proprietary، TCP 49) يشفّر payload كاملاً، يفصل AAA بثلاث خدمات منفصلة، أمثل لإدارة الأجهزة (device admin).
    </div>
</div>

<div class="question-block">
    <span class="question-num">Q20</span>
    <span class="question-text">ما الفرق بين <code class="inline">show running-config</code> و <code class="inline">show startup-config</code>؟</span>
    <div class="answer-block">
        <span class="answer-label">الإجابة:</span> <code class="inline">show running-config</code> يعرض الإعداد الحالي في RAM (المعدّل الآن، غير محفوظ). <code class="inline">show startup-config</code> يعرض الإعداد المحفوظ في NVRAM (الذي سيُحمّل عند الإقلاع). لحفظ الإعداد من RAM إلى NVRAM: <code class="inline">copy running-config startup-config</code>.
    </div>
</div>


<!-- ============ SECTION 27: EXAM TIPS & COMMON MISTAKES ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 27</span>
    <div class="chapter-title">نصائح الامتحان والأخطاء الشائعة</div>
    <div class="chapter-title-en">Exam Tips, Common Mistakes &amp; Best Practices</div>
    <div class="chapter-divider"></div>
</div>

<div class="section-title">نصائح عامة للنجاح في امتحان CCNA</div>
<ul style="padding-right: 20px; line-height: 2;">
    <li><strong>اقرأ السؤال كاملاً</strong> قبل الإجابة. كثير من الأسئلة تدل تفاصيلها على الإجابة الصحيحة.</li>
    <li><strong>احفظ جدول AD</strong> عن ظهر قلب. أكثر سؤال يتكرر: "أي مسار يختار الراوتر بين OSPF و EIGRP؟".</li>
    <li><strong>احفظ جدول Subnetting</strong> (/24 إلى /30 على الأقل). التمرن على حلّ مسائل في 30 ثانية.</li>
    <li><strong>استعمل <code class="inline">?</code></strong> بحرية في اللاب، فالامتحان العملي يسمح به.</li>
    <li><strong>تعوّد على اختصارات الأوامر</strong>: <code class="inline">sh ip int br</code> بدل <code class="inline">show ip interface brief</code>.</li>
    <li><strong>ابدأ بأبسط الحلول</strong> في التشخيص: physical → data link → network → application.</li>
    <li><strong>اضبط <code class="inline">no ip domain-lookup</code> و <code class="inline">logging synchronous</code></strong> على كل جلسة لاب.</li>
    <li><strong>احفظ قيم Port Numbers الشائعة</strong>: SSH 22، Telnet 23، DNS 53، DHCP 67/68، HTTP 80، HTTPS 443، BGP 179.</li>
    <li><strong>استعمل ميزة Tab completion</strong> في CLI لتفادي الأخطاء الإملائية.</li>
    <li><strong>تأكد من إعادة التحميل إن غيّرت إعداداً يحتاج reboot</strong> (مثل تغيير SDM template).</li>
</ul>

<div class="section-title">الأخطاء الشائعة التي يجب تجنبها</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الخطأ</th>
            <th style="width: 30%;">العاقبة</th>
            <th style="width: 35%;">الحل</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>نسيان <code class="inline">no shutdown</code> على الواجهة</td>
            <td>الواجهة administratively down، لا IP routing</td>
            <td>تحقق بـ <code class="inline">show ip int br</code> أن الحالة up/up</td>
        </tr>
        <tr>
            <td>استعمال subnet mask بدل wildcard في OSPF</td>
            <td>OSPF يرفض الأوامر أو يأخذ نتيجة خاطئة</td>
            <td>عكس الـ mask: <code class="inline">255.255.255.0 → 0.0.0.255</code></td>
        </tr>
        <tr>
            <td>نسيان <code class="inline">no auto-summary</code> في EIGRP</td>
            <td>تلخيص على حدود classful، مسارات خاطئة</td>
            <td>أضف <code class="inline">no auto-summary</code> دائماً</td>
        </tr>
        <tr>
            <td>عدم تفعيل <code class="inline">ipv6 unicast-routing</code></td>
            <td>IPv6 routing لا يعمل، RA لا يُرسل</td>
            <td>أضفها دائماً عند ضبط IPv6 على الراوتر</td>
        </tr>
        <tr>
            <td>عدم ضبط <code class="inline">router-id</code> في OSPF</td>
            <td>OSPF يختار IP عشوائي، قد يتغير</td>
            <td>اضبط <code class="inline">router-id X.X.X.X</code> يدوياً</td>
        </tr>
        <tr>
            <td>وضع PortFast على بورت Trunk</td>
            <td>حلقة فورية قبل أن يكتشفها STP</td>
            <td>PortFast فقط على Access Ports</td>
        </tr>
        <tr>
            <td>استعمال <code class="inline">enable password</code> بدل <code class="inline">enable secret</code></td>
            <td>كلمة مرور بنص ظاهر في running-config</td>
            <td>استعمل دائماً <code class="inline">enable secret</code> أو algorithm-type scrypt</td>
        </tr>
        <tr>
            <td>عدم ضبط <code class="inline">login local</code> على VTY</td>
            <td>أي شخص يستطيع SSH بدون مصادقة</td>
            <td>أضف <code class="inline">login local</code> + أنشئ username</td>
        </tr>
        <tr>
            <td>السماح بـ Telnet بدل SSH</td>
            <td>كلمة المرور تمرّ بـ plain text</td>
            <td>اضبط <code class="inline">transport input ssh</code> فقط</td>
        </tr>
        <tr>
            <td>وضع Extended ACL قرب الوجهة بدل المصدر</td>
            <td>إهدار عرض النطاق، تأخير في التصفية</td>
            <td>Extended ACL قرب المصدر، Standard قرب الوجهة</td>
        </tr>
        <tr>
            <td>نسيان <code class="inline">exit</code> بعد <code class="inline">interface</code> أو <code class="inline">router</code></td>
            <td>كتابة الأوامر في الوضع الخاطئ</td>
            <td>اضبط <code class="inline">exit</code> أو <code class="inline">end</code> دائماً</td>
        </tr>
        <tr>
            <td>عدم ضبط <code class="inline">standby preempt</code> في HSRP</td>
            <td>الراوتر الأساسي لا يستعيد دوره بعد العودة</td>
            <td>أضف <code class="inline">standby &lt;n&gt; preempt</code></td>
        </tr>
        <tr>
            <td>عدم ضبط <code class="inline">next-hop-self</code> في iBGP</td>
            <td>iBGP لا يعرف الـ next-hop من eBGP</td>
            <td>أضف <code class="inline">neighbor &lt;ip&gt; next-hop-self</code></td>
        </tr>
        <tr>
            <td>ترك Native VLAN على VLAN 1</td>
            <td>خطر VLAN Hopping Attack</td>
            <td>اضبط Native VLAN إلى غير مستخدم (مثل 999)</td>
        </tr>
        <tr>
            <td>عدم تفعيل <code class="inline">service password-encryption</code></td>
            <td>كلمات المرور بـ plain text في الإعداد</td>
            <td>فعّله دائماً في الإعداد الأولي</td>
        </tr>
    </tbody>
</table>

<div class="section-title">استراتيجيات للاب العملي (Lab Strategy)</div>
<ol style="padding-right: 20px; line-height: 2;">
    <li><strong>اقرأ المتطلبات كاملة قبل البدء.</strong> فهم الطوبولوجيا والمطلوب قبل أي تنفيذ.</li>
    <li><strong>ابدأ من Core إلى Edge.</strong> اضبط الإعدادات على الـ Distribution layer أولاً، ثم الـ Access.</li>
    <li><strong>ضبط اسم وكلمات مرور أولاً.</strong> اضبط الـ hostnames و SSH على كل الأجهزة قبل أي تكوين شبكي.</li>
    <li><strong>اختبر بعد كل خطوة.</strong> لا تكمل على خطأ. <code class="inline">show ip int br</code> و <code class="inline">ping</code> كثيراً.</li>
    <li><strong>وثّق الإعداد بالأوصاف.</strong> أضف <code class="inline">description</code> على كل واجهة لـ troubleshooting أسرع.</li>
    <li><strong>احفظ بعد كل إعداد ناجح.</strong> <code class="inline">copy run start</code> كثيراً، لتفادي فقدان العمل عند فشل الجهاز.</li>
    <li><strong>استعمل notepad مفتوح</strong> لـ staging الأوامر الطويلة قبل لصقها على CLI.</li>
    <li><strong>قم بتسمية ملفات الإعداد</strong> عند التصدير إلى TFTP: <code class="inline">copy run tftp://10.0.0.5/R1-config</code>.</li>
    <li><strong>خطط للفشل.</strong> ضبط Floating Static Routes و HSRP يحفظ وقتك عند فشل شيء في اللاب.</li>
    <li><strong>في نهاية اللاب، تحقق من كل المتطلبات.</strong> اقرأ قائمة المتطلبات وتأكد من كل بند.</li>
</ol>

<div class="section-title">قائمة فحص نهائية قبل تسليم اللاب (Lab Checklist)</div>
<ul style="padding-right: 20px; line-height: 1.9;">
    <li>كل الواجهات <code class="inline">up/up</code> في <code class="inline">show ip int br</code></li>
    <li>كل الراوترات لها <code class="inline">router-id</code> معرّف يدوياً</li>
    <li>كل VTY لها <code class="inline">login local</code> و <code class="inline">transport input ssh</code></li>
    <li>كل كلمات المرور مشفّرة (لا <code class="inline">password</code> نص ظاهر)</li>
    <li>الإعداد محفوظ في NVRAM (<code class="inline">copy run start</code>)</li>
    <li>جيران OSPF/EIGRP/BGP في حالة <code class="inline">FULL/Up</code></li>
    <li>كل VLANs موجودة على كلا السويتشين في Trunk</li>
    <li>Native VLAN غير 1 (مثلاً 999)</li>
    <li>PortFast + BPDU Guard على بورتات Access</li>
    <li>Default route موجودة وتعمل (<code class="inline">show ip route</code>)</li>
    <li>NAT يعمل (<code class="inline">show ip nat translations</code>)</li>
    <li>ACLs مطبّقة على الواجهات الصحيحة بالاتجاه الصحيح</li>
    <li>HSRP Active على الراوتر المطلوب (<code class="inline">show standby brief</code>)</li>
    <li>NTP متزامن (<code class="inline">show ntp status</code>)</li>
    <li>Syslog configured على كل الأجهزة</li>
    <li>الوصول إلى كل الأجهزة عبر SSH يعمل من شبكة الإدارة</li>
    <li>الاتصال: ping من كل المضيفين إلى الإنترنت</li>
    <li>أسماء الأجهزة معرّفة وموصوفة</li>
    <li>أوصاف على كل واجهة</li>
    <li>الإعداد مصدّر إلى TFTP كنسخة احتياطية</li>
</ul>

<div class="tip-box">
    <div class="tip-box-title">النصيحة الذهبية النهائية</div>
    <div class="tip-box-body">
        مهندس الشبكات الناجح ليس من يحفظ كل الأوامر، بل من يفهم <strong>المفاهيم</strong> وراءها. الأوامر تأتي وتذهل مع تطور IOS، لكن المفاهيم (Routing، Switching، Security) ثابتة. ركّز على فهم <strong>لماذا</strong> تستعمل أمراً ما، لا مجرد <strong>كيف</strong>. وعند الشك، استخدم <code class="inline">?</code> و <code class="inline">show</code> بوفرة. مهارة التشخيص (troubleshooting) أهم بكثير من حفظ الأوامر، وهي ما يميّز المهندس المحترف عن المبتدئ.
    </div>
</div>

<div class="footer-note">
    مذكرة أوامر سيسكو الشاملة - Cisco IOS Commands Complete Reference<br>
    CCNA 200-301 &amp; CCNP ENARSI Coverage &middot; Edition 1.0 &middot; 2026
</div>

"""
