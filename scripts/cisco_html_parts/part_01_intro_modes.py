# -*- coding: utf-8 -*-
"""Part 01: Section 1 - Introduction + Section 2 - Router Modes"""

SECTIONS_01 = """

<!-- ============ SECTION 1: INTRODUCTION ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 01</span>
    <div class="chapter-title">المقدمة وكيفية استخدام المذكرة</div>
    <div class="chapter-title-en">Introduction &amp; Usage Guide</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    مرحباً بك في المذكرة الشاملة لأوامر سيسكو. صُمّمت هذه المذكرة خصيصاً لمراجعة وتثبيت أوامر نظام Cisco IOS (Internetwork Operating System) المستخدمة في راوترات وسويتشات سيسكو، وهي تغطي بشكل كامل منهج امتحان <strong>CCNA 200-301</strong> بالإضافة إلى مواضيع متقدمة من منهج <strong>CCNP ENARSI</strong> كـ BGP و FHRP و QoS و 802.1x. تم تنظيم المحتوى في 27 قسماً رئيسياً، يحتوي كل منها على جداول مفصلة للأوامر مع شرح عربي واضح وأمثلة تطبيقية عملية.
</div>

<div class="section-title">بنية كل أمر في هذه المذكرة</div>
<div class="body-text">
    كل أمر يتم ذكره في الجداول التالية يحتوي على العناصر التالية بشكل منهجي ومنظم:
</div>
<ul style="padding-right: 20px; line-height: 1.9;">
    <li><strong>الأمر (Command Syntax):</strong> الصيغة الدقيقة للأمر كما يكتب في Cisco IOS، مع وضع المتغيرات بين أقواس زاوية <code class="inline">&lt;variable&gt;</code> والكلمات الاختيارية بين أقواس مربعة <code class="inline">[optional]</code>.</li>
    <li><strong>الوضع (Mode):</strong> الوضع الذي يُكتب فيه الأمر (User EXEC، Privileged EXEC، Global Config، Interface Config، إلخ).</li>
    <li><strong>الشرح (Explanation):</strong> ما الذي يفعله الأمر وكيف يعمل بالضبط.</li>
    <li><strong>مثال (Example):</strong> مثال تطبيقي عملي يوضح الاستخدام الحقيقي للأمر.</li>
    <li><strong>العكس (no command):</strong> الأمر العكسي لإلغاء التأثير، عادةً يكون بنفس الصيغة مسبوقاً بكلمة <code class="inline">no</code>.</li>
</ul>

<div class="section-title">أوضاع Cisco IOS الرئيسية (سطر الأوامر)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 22%;">الوضع (Mode)</th>
            <th style="width: 28%;">الموجّه (Prompt)</th>
            <th style="width: 50%;">الوصف</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>User EXEC</code></td><td class="mode-col">Router&gt;</td><td>الوضع الافتراضي عند الدخول، محدود الصلاحيات، يستخدم لعرض المعلومات فقط.</td></tr>
        <tr><td><code>Privileged EXEC</code></td><td class="mode-col">Router#</td><td>وضع متميز، يسمح بعرض كل المعلومات وحفظ الإعدادات وإعادة التحميل.</td></tr>
        <tr><td><code>Global Config</code></td><td class="mode-col">Router(config)#</td><td>الوضع العام للإعداد، يُستخدم لإعداد المعرفات التي تؤثر على الجهاز بالكامل.</td></tr>
        <tr><td><code>Interface Config</code></td><td class="mode-col">Router(config-if)#</td><td>إعداد واجهة محددة (Interface) كـ GigabitEthernet أو VLAN.</td></tr>
        <tr><td><code>Line Config</code></td><td class="mode-col">Router(config-line)#</td><td>إعداد خطوط الوصول (Console، VTY، AUX).</td></tr>
        <tr><td><code>Router Config</code></td><td class="mode-col">Router(config-router)#</td><td>إعداد بروتوكولات التوجيه الديناميكي (OSPF، EIGRP، BGP).</td></tr>
        <tr><td><code>Subnet Config</code></td><td class="mode-col">Router(config-subif)#</td><td>إعداد واجهة فرعية (Sub-interface) لتقسيم VLANs (Router-on-a-Stick).</td></tr>
        <tr><td><code>VLAN Config</code></td><td class="mode-col">Switch(config-vlan)#</td><td>إعداد VLAN محدد في السويتش.</td></tr>
        <tr><td><code>Controller Config</code></td><td class="mode-col">Router(config-controller)#</td><td>إعداد وحدات التحكم في الواجهات التسلسلية (Serial/WAN).</td></tr>
    </tbody>
</table>

<div class="info-box">
    <div class="info-box-title">ملاحظة هامة حول الموجّهات (Prompts)</div>
    <div class="info-box-body">
        الموجّه هو النص الذي يظهر قبل المؤشر في سطر الأوامر. على سبيل المثال، إذا كان الموجّه <code class="inline">Router&gt;</code> فأنت في وضع User EXEC، أما إذا كان <code class="inline">Router#</code> فأنت في وضع Privileged EXEC. عند رؤية <code class="inline">(config-if)#</code> يلزم الانتباه أنك في إعداد واجهة محددة، وأي أمر تكتبه سيطبّق على هذه الواجهة فقط.
    </div>
</div>

<div class="section-title">اختصارات لوحة المفاتيح الهامة في Cisco IOS</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 25%;">الاختصار</th>
            <th style="width: 75%;">الوظيفة</th>
        </tr>
    </thead>
    <tbody>
        <tr><td class="cmd-col">Tab</td><td>إكمال كتابة الأمر تلقائياً (Auto-complete).</td></tr>
        <tr><td class="cmd-col">Ctrl + A</td><td>الانتقال إلى بداية السطر.</td></tr>
        <tr><td class="cmd-col">Ctrl + E</td><td>الانتقال إلى نهاية السطر.</td></tr>
        <tr><td class="cmd-col">Ctrl + B (←)</td><td>التحرك حرف واحد إلى الخلف (يساراً).</td></tr>
        <tr><td class="cmd-col">Ctrl + F (→)</td><td>التحرك حرف واحد إلى الأمام (يميناً).</td></tr>
        <tr><td class="cmd-col">Ctrl + P (↑)</td><td>استدعاء الأمر السابق من التاريخ.</td></tr>
        <tr><td class="cmd-col">Ctrl + N (↓)</td><td>استدعاء الأمر التالي من التاريخ.</td></tr>
        <tr><td class="cmd-col">Ctrl + U</td><td>حذف كل ما قبل المؤشر من السطر.</td></tr>
        <tr><td class="cmd-col">Ctrl + W</td><td>حذف كلمة واحدة قبل المؤشر.</td></tr>
        <tr><td class="cmd-col">Ctrl + Z</td><td>الخروج من وضع الإعداد إلى Privileged EXEC (مثل <code class="inline">end</code>).</td></tr>
        <tr><td class="cmd-col">Ctrl + C</td><td>إلغاء الأمر الجاري أو الخروج من الإعداد.</td></tr>
        <tr><td class="cmd-col">Ctrl + Shift + 6</td><td>إيقاف تنفيذ أمر (Escape Sequence) مثل إيقاف <code class="inline">ping</code> أو <code class="inline">traceroute</code>.</td></tr>
        <tr><td class="cmd-col">?</td><td>عرض المساعدة السياقية وكل الأوامر المتاحة في الوضع الحالي.</td></tr>
        <tr><td class="cmd-col">command ?</td><td>عرض المعاملات (Parameters) التي يقبلها الأمر.</td></tr>
    </tbody>
</table>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للمذاكرة</div>
    <div class="tip-box-body">
        احفظ اختصارات لوحة المفاتيح جيداً لأنها تختصر الوقت كثيراً في الامتحان العملي (Lab). أكثرها استخداماً: <code class="inline">Tab</code> للإكمال، <code class="inline">Ctrl+Z</code> للخروج السريع، <code class="inline">Ctrl+Shift+6</code> لإيقاف <code class="inline">ping</code>، وعلامة <code class="inline">?</code> للتعرف على المعاملات المتاحة. في امتحان CCNA يُسمح باستخدام <code class="inline">?</code> بحرية، فلا تتردد في استخدامه عند الشك.
    </div>
</div>

<div class="section-title">المنهجية المقترحة للمذاكرة</div>
<div class="body-text">
    أنصحك باتباع منهجية <strong>"الدراسة الطبقية المتدرجة"</strong> للمذاكرة الفعّالة، والتي تتمثل في: (1) اقرأ الشرح العربي لكل أمر بتمعّن لفهم الوظيفة المنطقية، (2) تمعّن في المثال التطبيقي وحاول تطبيقه ذهنياً، (3) تذكّر الوضع (Mode) الذي يُكتب فيه الأمر لأن خطأ الوضع هو خطأ شائع جداً، (4) احفظ الأمر العكسي <code class="inline">no</code> لأنه قد يأتي في الاختبار إزالة إعداد خاطئ، (5) انتقل إلى قسم Lab Scenarios بعد كل قسمين نظريين لتطبيق ما تعلمته. لا تحاول حفظ كل الأوامر مرة واحدة، بل ركّز على فهم المفاهيم الأساسية وستأتي الأوامر تباعاً.
</div>

<div class="section-title">الاختصارات والمصطلحات المستخدمة</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 18%;">الاختصار</th>
            <th style="width: 32%;">التفصير</th>
            <th style="width: 50%;">الشرح</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>IOS</td><td>Internetwork Operating System</td><td>نظام تشغيل سيسكو المستخدم في الراوترات والسويتشات.</td></tr>
        <tr><td>CLI</td><td>Command-Line Interface</td><td>واجهة سطر الأوامر للتفاعل مع الجهاز.</td></tr>
        <tr><td>EXEC</td><td>Execute Mode</td><td>وضع التنفيذ (User أو Privileged).</td></tr>
        <tr><td>NVRAM</td><td>Non-Volatile RAM</td><td>ذاكرة غير طيّارة تخزن ملف الإعداد startup-config.</td></tr>
        <tr><td>RAM</td><td>Random Access Memory</td><td>ذاكرة طيّارة تخزن running-config وتفقد عند إعادة التشغيل.</td></tr>
        <tr><td>Flash</td><td>Flash Memory</td><td>ذاكرة وميضية تخزن نظام IOS نفسه.</td></tr>
        <tr><td>ROM</td><td>Read-Only Memory</td><td>ذاكرة للقراءة فقط، تحوي bootstrap و ROMmon للطوارئ.</td></tr>
        <tr><td>VRP</td><td>VLAN Routing Process</td><td>SVI - Switch Virtual Interface لإنشاء توجيه بين VLANs.</td></tr>
    </tbody>
</table>


<!-- ============ SECTION 2: ROUTER MODES & NAVIGATION ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 02</span>
    <div class="chapter-title">أوضاع الراوتر والتنقل بينها</div>
    <div class="chapter-title-en">Router Modes &amp; Navigation</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    يعتبر فهم أوضاع Cisco IOS المختلفة من أهم الأساسيات التي يجب على كل مهندس شبكات إتقانها قبل التعمق في الأوامر. كل وضع له صلاحيات وحدود معينة، والأوامر المتاحة في وضع قد لا تكون متاحة في وضع آخر. الخطأ الشائع بين المبتدئين هو محاولة تنفيذ أمر إعداد في وضع العرض (User/Privileged EXEC) أو العكس، مما يؤدي إلى رسالة الخطأ المعروفة <code class="inline">% Invalid input detected</code> أو <code class="inline">% Incomplete command</code>.
</div>

<div class="section-title">الانتقال بين الأوضاع (Mode Transitions)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر (Command)</th>
            <th style="width: 18%;">الوضع (Mode)</th>
            <th style="width: 32%;">الشرح</th>
            <th style="width: 22%;">مثال</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">enable</td>
            <td class="mode-col">User EXEC → Privileged</td>
            <td>الانتقال من وضع المستخدم العادي <code class="inline">Router&gt;</code> إلى وضع التنفيذ المميّز <code class="inline">Router#</code>. يتطلب كلمة مرور إن وُجدت.</td>
            <td class="example-col">Router&gt;enable<br>Router#</td>
        </tr>
        <tr>
            <td class="cmd-col">disable</td>
            <td class="mode-col">Privileged → User EXEC</td>
            <td>العودة من وضع التنفيذ المميّز إلى وضع المستخدم العادي بدون الخروج من الجهاز.</td>
            <td class="example-col">Router#disable<br>Router&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">configure terminal</td>
            <td class="mode-col">Privileged → Global Config</td>
            <td>الدخول إلى وضع الإعداد العام. يختصر عادةً بـ <code class="inline">conf t</code>. يُستخدم لكل الأوامر التي تؤثر على الجهاز بالكامل.</td>
            <td class="example-col">Router#configure terminal<br>Router(config)#</td>
        </tr>
        <tr>
            <td class="cmd-col">exit</td>
            <td class="mode-col">أي وضع → الوضع الأعلى</td>
            <td>الخروج من الوضع الحالي إلى الوضع الذي يسبقه مباشرةً. عند استخدامه في Global Config يعود إلى Privileged EXEC.</td>
            <td class="example-col">Router(config)#exit<br>Router#</td>
        </tr>
        <tr>
            <td class="cmd-col">end</td>
            <td class="mode-col">أي وضع فرعي → Privileged</td>
            <td>الخروج مباشرةً من أي وضع فرعي (واجهة، راوتر، خط) إلى Privileged EXEC. يكافئ <code class="inline">Ctrl+Z</code>.</td>
            <td class="example-col">Router(config-if)#end<br>Router#</td>
        </tr>
        <tr>
            <td class="cmd-col">interface &lt;type&gt; &lt;number&gt;</td>
            <td class="mode-col">Global → Interface</td>
            <td>الدخول إلى وضع إعداد واجهة محددة. الأنواع الشائعة: <code class="inline">GigabitEthernet</code>، <code class="inline">FastEthernet</code>، <code class="inline">Serial</code>، <code class="inline">VLAN</code>، <code class="inline">Loopback</code>، <code class="inline">Port-channel</code>.</td>
            <td class="example-col">Router(config)#interface gigabitEthernet 0/0<br>Router(config-if)#</td>
        </tr>
        <tr>
            <td class="cmd-col">interface range &lt;type&gt; &lt;start&gt;-&lt;end&gt;</td>
            <td class="mode-col">Global → Interface Range</td>
            <td>إعداد عدة واجهات متتالية في وقت واحد (مفيد في السويتشات لإعداد بورتات متعددة بنفس الإعدادات).</td>
            <td class="example-col">SW(config)#interface range fa0/1 - 10<br>SW(config-if-range)#</td>
        </tr>
        <tr>
            <td class="cmd-col">line &lt;type&gt; &lt;number&gt;</td>
            <td class="mode-col">Global → Line Config</td>
            <td>الدخول إلى وضع إعداد خط الوصول. الأنواع: <code class="inline">console 0</code>، <code class="inline">vty 0 4</code> أو <code class="inline">vty 0 15</code>، <code class="inline">aux 0</code>.</td>
            <td class="example-col">Router(config)#line vty 0 4<br>Router(config-line)#</td>
        </tr>
        <tr>
            <td class="cmd-col">router &lt;protocol&gt; &lt;args&gt;</td>
            <td class="mode-col">Global → Router Config</td>
            <td>الدخول إلى وضع إعداد بروتوكول توجيه (Router Process). مثل <code class="inline">router ospf 1</code>، <code class="inline">router eigrp 100</code>، <code class="inline">router bgp 65000</code>.</td>
            <td class="example-col">Router(config)#router ospf 1<br>Router(config-router)#</td>
        </tr>
        <tr>
            <td class="cmd-col">vlan &lt;id&gt;</td>
            <td class="mode-col">Global → VLAN Config</td>
            <td>إنشاء VLAN جديد والدخول لوضع إعداده. يختصر بـ <code class="inline">vlan 10</code>.</td>
            <td class="example-col">SW(config)#vlan 10<br>SW(config-vlan)#</td>
        </tr>
        <tr>
            <td class="cmd-col">do &lt;command&gt;</td>
            <td class="mode-col">Global/Sub → EXEC في موضعه</td>
            <td>تنفيذ أمر من نوع Privileged EXEC (مثل <code class="inline">show</code> أو <code class="inline">copy</code>) من داخل أي وضع إعداد بدون الخروج منه. مفيد جداً عند الإعداد.</td>
            <td class="example-col">Router(config-if)#do show run | include hostname</td>
        </tr>
    </tbody>
</table>

<div class="section-title">عرض الإعدادات والحالة (Display Commands)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 30%;">الأمر</th>
            <th style="width: 15%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 20%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">show running-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض الإعداد الحالي الكامل المحفوظ في RAM. يختصر بـ <code class="inline">sh run</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show startup-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض الإعداد المحفوظ في NVRAM والذي سيُحمّل عند إعادة التشغيل. يختصر بـ <code class="inline">sh start</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show version</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض إصدار IOS، نوع المعالج، حجم الذاكرة، اسم الجهاز، قيمة Configuration Register، ووقت التشغيل.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show clock</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض التاريخ والوقت الحاليين للجهاز.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show history</td>
            <td class="mode-col">User/Privileged</td>
            <td>عرض قائمة آخر الأوامر المنفّذة في الجلسة الحالية. مفيد لمراجعة ما كتبته.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">terminal history size &lt;0-256&gt;</td>
            <td class="mode-col">User/Privileged</td>
            <td>تحديد عدد الأوامر التي تُحفظ في الذاكرة المؤقتة للتاريخ (الافتراضي 10-20).</td>
            <td class="no-col">terminal no history size</td>
        </tr>
        <tr>
            <td class="cmd-col">terminal length &lt;0-512&gt;</td>
            <td class="mode-col">User/Privileged</td>
            <td>تحديد عدد الأسطر المعروضة قبل توقف الشاشة على <code class="inline">--More--</code>. صفر يعني عرض كل شيء دفعة واحدة.</td>
            <td class="no-col">terminal length 24</td>
        </tr>
        <tr>
            <td class="cmd-col">show processes cpu</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض استخدام المعالج خلال 5 ثواني و 1 دقيقة و 5 دقائق. مفيد لتشخيص الأداء.</td>
            <td class="no-col">N/A</td>
        </tr>
    </tbody>
</table>

<div class="section-title">حفظ الإعدادات وإعادة التحميل</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 30%;">الأمر</th>
            <th style="width: 15%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 20%;">مثال</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">copy running-config startup-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>حفظ الإعداد الحالي (running) في NVRAM ليصبح الإعداد الابتدائي (startup). يكافئ <code class="inline">write memory</code>.</td>
            <td class="example-col">Router#copy run start</td>
        </tr>
        <tr>
            <td class="cmd-col">write memory</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>اختصار قديم لحفظ الإعداد. لا يزال مدعوماً ويستخدم بكثرة.</td>
            <td class="example-col">Router#wr mem</td>
        </tr>
        <tr>
            <td class="cmd-col">copy startup-config tftp:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>نسخ الإعداد المحفوظ إلى خادم TFTP خارجي كنسخة احتياطية.</td>
            <td class="example-col">Router#copy start tftp:</td>
        </tr>
        <tr>
            <td class="cmd-col">copy tftp: running-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>استرجاع إعداد من خادم TFTP وتطبيقه على الإعداد الحالي (دمج وليس استبدال).</td>
            <td class="example-col">Router#copy tftp: run</td>
        </tr>
        <tr>
            <td class="cmd-col">erase startup-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>مسح الإعداد المحفوظ في NVRAM (إعادة الجهاز إلى حالته المصنعية عند إعادة التشغيل).</td>
            <td class="example-col">Router#erase start</td>
        </tr>
        <tr>
            <td class="cmd-col">reload</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>إعادة تشغيل الجهاز. سيتم تحميل startup-config إن وُجد، أو وضع الإعداد الابتدائي إن لم يوجد.</td>
            <td class="example-col">Router#reload</td>
        </tr>
        <tr>
            <td class="cmd-col">reload in &lt;mm:ss&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>جدولة إعادة تشغيل بعد فترة محددة. مفيدة في حالات التشخيص عن بُعد.</td>
            <td class="example-col">Router#reload in 00:30</td>
        </tr>
        <tr>
            <td class="cmd-col">reload cancel</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>إلغاء إعادة تشغيل مجدولة قبل تنفيذها.</td>
            <td class="example-col">Router#reload cancel</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر النظام الأساسية</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 20%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">hostname &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين اسم الجهاز. يجب أن يبدأ بحرف، ويفضّل ألا يحوي مسافات أو رموز خاصة. يؤثر على الموجّه (Prompt) مباشرةً.</td>
            <td class="no-col">no hostname</td>
        </tr>
        <tr>
            <td class="cmd-col">banner motd #&lt;text&gt;#</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين رسالة اليوم (Message of the Day) التي تظهر لكل من يسجل الدخول. الرمز # محدد لبداية ونهاية الرسالة (يمكن استبداله بأي رمز).</td>
            <td class="no-col">no banner motd</td>
        </tr>
        <tr>
            <td class="cmd-col">banner login #&lt;text&gt;#</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين رسالة تظهر قبل طلب كلمة المرور عند الدخول.</td>
            <td class="no-col">no banner login</td>
        </tr>
        <tr>
            <td class="cmd-col">clock set &lt;hh:mm:ss&gt; &lt;day&gt; &lt;month&gt; &lt;year&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>ضبط التاريخ والوقت يدوياً. يفضل استخدام NTP للمزامنة التلقائية.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">ip domain-lookup</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل تحويل أسماء المضيفين إلى عناوين IP (DNS lookup). مفعّل افتراضياً.</td>
            <td class="no-col">no ip domain-lookup</td>
        </tr>
        <tr>
            <td class="cmd-col">ip host &lt;name&gt; &lt;ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إضافة اسم مضيف مع عنوانه في جدول hosts المحلي للجهاز، لاستخدامه بدلاً من العنوان في الأوامر (مفيد في <code class="inline">ping R1</code> بدلاً من <code class="inline">ping 10.0.0.1</code>).</td>
            <td class="no-col">no ip host &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ip name-server &lt;ip1&gt; &lt;ip2&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين خادم DNS الذي يستخدمه الجهاز لتحويل الأسماء. يمكن إضافة حتى 6 خوادم.</td>
            <td class="no-col">no ip name-server</td>
        </tr>
        <tr>
            <td class="cmd-col">alias exec &lt;shortcut&gt; &lt;command&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء اختصار مخصص لأمر طويل. مثلاً <code class="inline">alias exec s show ip interface brief</code> يجعل <code class="inline">s</code> ينفّذ الأمر الكامل.</td>
            <td class="no-col">no alias exec &lt;shortcut&gt;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أمثلة تطبيقية: إعداد أولي كامل لراوتر</div>
<div class="code-block-title">مثال 2.1: إعداد أولي شامل لراوتر Cisco</div>
<div class="code-block">
Router&gt; <span class="prompt">enable</span>
Router# <span class="prompt">configure terminal</span>
Enter configuration commands, one per line. End with CNTL/Z.
Router(config)# <span class="prompt">hostname Core-RTR-01</span>
Core-RTR-01(config)# <span class="prompt">banner motd #*******************************************</span>
Core-RTR-01(config)# <span class="prompt">*  UNAUTHORIZED ACCESS IS PROHIBITED   *</span>
Core-RTR-01(config)# <span class="prompt">*  Authorized Personnel Only - CCNA Lab  *</span>
Core-RTR-01(config)# <span class="prompt">*******************************************#</span>
Core-RTR-01(config)# <span class="prompt">no ip domain-lookup</span>            <span class="comment">! إيقاف DNS lookup لتسريع كتابة الأوامر الخاطئة</span>
Core-RTR-01(config)# <span class="prompt">ip host SW-01 192.168.1.10</span>    <span class="comment">! اسم محلي مختصر</span>
Core-RTR-01(config)# <span class="prompt">clock timezone EET 2 0</span>         <span class="comment">! توقيت شرق أوروبا (+2)</span>
Core-RTR-01(config)# <span class="prompt">exit</span>
Core-RTR-01# <span class="prompt">clock set 14:30:00 25 Oct 2026</span>
Core-RTR-01# <span class="prompt">copy running-config startup-config</span>
Destination filename [startup-config]?
Building configuration...
[OK]
Core-RTR-01# <span class="prompt">reload</span>
</div>

<div class="info-box">
    <div class="info-box-title">حيلة مفيدة: تعطيل DNS lookup في المذاكرة</div>
    <div class="info-box-body">
        عند كتابة أمر خاطئ مثل <code class="inline">shwo</code> بدلاً من <code class="inline">show</code>، يقوم IOS افتراضياً بمحاولة حلّه كـ hostname عبر DNS، مما يستغرق وقتاً (ترى <code class="inline">Translating...domain server (255.255.255.255)</code>). تنفيذ <code class="inline">no ip domain-lookup</code> يمنع هذا السلوك ويسرّع التجربة العملية في اللاب. لكن انتبه أن تعطيله في بيئة الإنتاج قد يمنع بعض الأوامر التي تعتمد على DNS من العمل.
    </div>
</div>

<div class="section-title">ترتيب التحميل (Boot Sequence) وأوامره</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 32%;">الأمر</th>
            <th style="width: 15%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">boot system &lt;location&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد مكان تحميل ملف IOS عند الإقلاع. يمكن تحديد flash، tftp، أو rom. يُقرأ بترتيب الإدخال.</td>
            <td class="no-col">no boot system</td>
        </tr>
        <tr>
            <td class="cmd-col">config-register &lt;0xNNNN&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط سجل الإعداد (Configuration Register). القيمة الافتراضية 0x2102. القيمة 0x2142 تتجاهل startup-config عند الإقلاع (مفيدة لاستعادة كلمات المرور).</td>
            <td class="no-col">config-register 0x2102</td>
        </tr>
        <tr>
            <td class="cmd-col">show boot</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض إعدادات الإقلاع، بما فيها قيمة config-register ومصدر ملف IOS.</td>
            <td class="no-col">N/A</td>
        </tr>
    </tbody>
</table>

<div class="tip-box">
    <div class="tip-box-title">قيم config-register الهامة للحفظ</div>
    <div class="tip-box-body">
        احفظ القيم التالية جيداً لأنها تأتي في الامتحان:<br>
        <code class="inline">0x2102</code> = القيمة الافتراضية، يحمّل IOS من flash ثم startup-config.<br>
        <code class="inline">0x2142</code> = يحمّل IOS من flash لكن يتجاهل startup-config (يستخدم في إجراء Password Recovery).<br>
        <code class="inline">0x2100</code> = يقلع في ROM Monitor (ROMmon)، يستخدم لتشخيص أعطال IOS أو تحميل نسخة جديدة.<br>
        <code class="inline">0x2122</code> = يحمّل من flash ولا يستخدم أمر boot system لكن يتجاهل startup-config (نادر).
    </div>
</div>

<div class="section-title">إجراء Password Recovery (اختصاراً)</div>
<div class="body-text">
    عند فقدان كلمة مرور الراوتر، يتم الاستعادة عبر الخطوات التالية: (1) أعد تشغيل الجهاز واضغط <code class="inline">Ctrl+Break</code> خلال الـ POST للدخول إلى ROMmon. (2) غيّر قيمة config-register إلى <code class="inline">0x2142</code> باستخدام <code class="inline">confreg 0x2142</code> (في الأجهزة الحديثة) أو <code class="inline">o/r 0x2142</code> (في الأجهزة القديمة). (3) اكتب <code class="inline">reset</code> أو <code class="inline">i</code> لإعادة الإقلاع، وسيتم تجاهل startup-config. (4) عند ظهور الموجّه، ادخل <code class="inline">enable</code> (لن يطلب كلمة مرور)، ثم نفّذ <code class="inline">copy startup-config running-config</code> لاسترجاع الإعداد القديم. (5) غيّر كلمات المرور الجديدة. (6) أعد config-register إلى <code class="inline">0x2102</code> واحفظ الإعداد وأعد التحميل.
</div>

<div class="warn-box">
    <div class="warn-box-title">تحذير أمني</div>
    <div class="warn-box-body">
        إجراء Password Recovery يتطلب وصولاً فيزيائياً إلى كابل Console، لذلك فإن تأمين الوصول الفيزيائي للراوترات في بيئة الإنتاج يعتبر من أهم ضوابط الأمان. في حالات البيانات الحساسة، يُفعّل أيضاً <code class="inline">service password-encryption</code> و <code class="inline">no service password-recovery</code> لمنع استعادة كلمات المرور (استخدم بحذر شديد لأنه لا رجعة بعدها عند الفقدان!).
    </div>
</div>

"""
