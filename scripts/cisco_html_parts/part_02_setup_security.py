# -*- coding: utf-8 -*-
"""Part 02: Section 3 - Basic Setup & System Management + Section 4 - Passwords & Security"""

SECTIONS_02 = """

<!-- ============ SECTION 3: BASIC SETUP & SYSTEM MANAGEMENT ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 03</span>
    <div class="chapter-title">الإعداد الأساسي وإدارة النظام</div>
    <div class="chapter-title-en">Basic Setup &amp; System Management</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    بعد ضبط أوضاع الراوتر والتنقل بينها، تأتي مرحلة الإعداد الأساسي للجهاز قبل أي تكوين شبكي. تشمل هذه المرحلة تعيين اسم الجهاز (Hostname)، رسائل التحذير (Banners)، ضبط التوقيت، إدارة الذاكرة والإعدادات، وأوامر إدارة النظام التي تشكل البنية التحتية لكل الإعدادات اللاحقة. يلاحظ أن أي خطأ في هذه المرحلة قد يسبب مشكلات في خدمات متقدمة مثل التشفير (SSH) الذي يعتمد على اسم الجهاز و DNS Domain.
</div>

<div class="section-title">أوامر الاسم والوصف (Identity)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 30%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 33%;">الشرح</th>
            <th style="width: 20%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">hostname &lt;name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين اسم الجهاز. يجب أن يبدأ بحرف ويفضّل ألا يحوي مسافات. الأسماء الحساسة لإدارة الشبكة تحتوي عادةً على معلومات الموقع والدور مثل <code class="inline">Cairo-Edge-R01</code>.</td>
            <td class="no-col">no hostname</td>
        </tr>
        <tr>
            <td class="cmd-col">description &lt;text&gt;</td>
            <td class="mode-col">Interface/Sub-if</td>
            <td>إضافة وصف نصي للواجهة (مثل: <code class="inline">Link to ISP-Primary</code>). يظهر في <code class="inline">show interfaces</code> و <code class="inline">show running-config</code>.</td>
            <td class="no-col">no description</td>
        </tr>
    </tbody>
</table>

<div class="section-title">رسائل التحذير (Banners)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 20%;">مثال</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">banner motd <i>delim</i></td>
            <td class="mode-col">Global Config</td>
            <td>رسالة اليوم (Message of the Day) تظهر قبل طلب الدخول. تستخدم قانونياً للتنبيه بأن الوصول غير المصرّح به جريمة. الرمز المحدد (Delimiter) يبدأ وينهي الرسالة، أي رمز ممكن لكن # أو ^ شائعة.</td>
            <td class="example-col">banner motd #<br>UNAUTHORIZED ACCESS PROHIBITED<br>#</td>
        </tr>
        <tr>
            <td class="cmd-col">banner login <i>delim</i></td>
            <td class="mode-col">Global Config</td>
            <td>رسالة تظهر قبل طلب اسم المستخدم وكلمة المرور.</td>
            <td class="example-col">banner login ^CAuth Only^C</td>
        </tr>
        <tr>
            <td class="cmd-col">banner exec <i>delim</i></td>
            <td class="mode-col">Global Config</td>
            <td>رسالة تظهر بعد تسجيل الدخول بنجاح (عند دخول EXEC mode).</td>
            <td class="example-col">banner exec ^Welcome admin^C</td>
        </tr>
        <tr>
            <td class="cmd-col">banner incoming <i>delim</i></td>
            <td class="mode-col">Global Config</td>
            <td>رسالة تظهر عند اتصال وارد من طرف خارجي عبر terminal server.</td>
            <td class="example-col">banner incoming ^CIncoming^C</td>
        </tr>
    </tbody>
</table>

<div class="warn-box">
    <div class="warn-box-title">ملاحظة قانونية هامة</div>
    <div class="warn-box-body">
        رسالة <code class="inline">banner motd</code> ليست مجرد تزيين؛ في كثير من الدول (بما فيها مصر والسعودية والإمارات)، يتطلب القانون عرض تحذير صريح قبل محاولة الوصول ليكون أي وصول غير مصرّح به "جريمة مع سبق الإصرار". يستحسن أن تشمل الرسالة: (1) أن النظام للاستخدام المصرّح به فقط، (2) أن كل الأنشطة مراقبة ومسجّلة، (3) أن الوصول غير المصرّح به ممنوع ويعرض صاحبه للمساءلة القانونية.
    </div>
</div>

<div class="section-title">أوامر التوقيت (Time)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 32%;">الأمر</th>
            <th style="width: 18%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">clock set &lt;hh:mm:ss&gt; &lt;day&gt; &lt;month&gt; &lt;year&gt;</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>ضبط التوقيت يدوياً. الترتيب: الساعة:الدقيقة:الثانية اليوم الشهر السنة. مثلاً: <code class="inline">clock set 14:30:00 25 Oct 2026</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">clock timezone &lt;name&gt; &lt;hours&gt; [&lt;mins&gt;]</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط المنطقة الزمنية. لمصر: <code class="inline">clock timezone EET 2 0</code> (شرق أوروبا +2 ساعة صيفاً وشتاءً). للسعودية: <code class="inline">clock timezone AST 3 0</code>.</td>
            <td class="no-col">no clock timezone</td>
        </tr>
        <tr>
            <td class="cmd-col">clock summer-time &lt;zone&gt; recurring</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل التوقيت الصيفي تلقائياً. متوقف في مصر منذ 2014، لكن مفعّل في بعض الدول الأخرى.</td>
            <td class="no-col">no clock summer-time</td>
        </tr>
        <tr>
            <td class="cmd-col">ntp server &lt;ip&gt; [version 2-4]</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط خادم NTP للمزامنة التلقائية. يحوّل الجهاز إلى عميل NTP.</td>
            <td class="no-col">no ntp server &lt;ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">ntp master [&lt;stratum&gt;]</td>
            <td class="mode-col">Global Config</td>
            <td>تحويل الجهاز إلى خادم NTP مصدر (Master). الـ stratum الافتراضي 8.</td>
            <td class="no-col">no ntp master</td>
        </tr>
        <tr>
            <td class="cmd-col">ntp authenticate</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل مصادقة NTP (موصى به في بيئات الإنتاج).</td>
            <td class="no-col">no ntp authenticate</td>
        </tr>
        <tr>
            <td class="cmd-col">show ntp status</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض حالة المزامنة مع خادم NTP (synchronized أو unsynchronized).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show ntp associations</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض الجهاز الذي تتم مزامنته، وقيم stratum والـ reach.</td>
            <td class="no-col">N/A</td>
        </tr>
    </tbody>
</table>

<div class="section-title">إدارة الذاكرة والإعدادات</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 30%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">copy running-config startup-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>حفظ الإعداد الحالي إلى NVRAM ليصبح الإعداد الابتدائي. يكافئ <code class="inline">write memory</code> و <code class="inline">wr</code>.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">copy running-config tftp:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>نسخ الإعداد الحالي إلى خادم TFTP خارجي كنسخة احتياطية. سيطلب عنوان الخادم واسم الملف.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">copy flash: tftp:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>نسخ ملف من flash (مثل صورة IOS) إلى خادم TFTP. يستخدم لعمل نسخة احتياطية من نظام IOS.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">copy tftp: flash:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>تحميل ملف (عادة صورة IOS جديدة) من خادم TFTP إلى flash. يستخدم لترقية نظام IOS.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">erase flash:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>مسح محتوى flash (تحذير: يحذف ملف IOS!). يستخدم قبل تحميل نسخة جديدة فقط.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">erase startup-config</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>مسح الإعداد المحفوظ في NVRAM. عند إعادة التحميل بعدها يدخل الجهاز في وضع الإعداد الابتدائي (Setup Mode).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">format flash:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>تهيئة flash (أكثر شمولاً من erase). يحذف كل الملفات ويعيد بناء نظام الملفات.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">dir flash:</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض محتوى flash مع حجم الملفات والمساحة الحرة.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">boot flash:&lt;filename&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد ملف IOS معين لتحميله عند الإقلاع. مفيد عند توفر عدة إصدارات IOS في flash.</td>
            <td class="no-col">no boot flash:</td>
        </tr>
    </tbody>
</table>

<div class="section-title">أوامر إضافية لإدارة النظام</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 40%;">الشرح</th>
            <th style="width: 15%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">no ip domain-lookup</td>
            <td class="mode-col">Global Config</td>
            <td>تعطيل تحويل الأسماء. يمنع الجهاز من محاولة حلّ الأوامر الخاطئة كأنها أسماء DNS، مما يسرّع CLI بشكل كبير.</td>
            <td class="no-col">ip domain-lookup</td>
        </tr>
        <tr>
            <td class="cmd-col">logging synchronous</td>
            <td class="mode-col">Line Config</td>
            <td>إعادة عرض الموجّه والسطر الحالي بعد ظهور رسائل syslog، بدلاً من تشويشها على ما تكتب. ينصح به بشدة على console و vty.</td>
            <td class="no-col">no logging synchronous</td>
        </tr>
        <tr>
            <td class="cmd-col">exec-timeout &lt;min&gt; &lt;sec&gt;</td>
            <td class="mode-col">Line Config</td>
            <td>تسجيل الخروج التلقائي بعد مدة من عدم النشاط. <code class="inline">exec-timeout 5 0</code> = 5 دقائق. <code class="inline">exec-timeout 0 0</code> = لا تنتهي الجلسة (غير محبذ أمنياً).</td>
            <td class="no-col">no exec-timeout</td>
        </tr>
        <tr>
            <td class="cmd-col">service password-encryption</td>
            <td class="mode-col">Global Config</td>
            <td>تشفير كل كلمات المرور غير المشفّرة في الإعداد باستخدام خوارزمية ضعيفة (Type 7). يُفعّل دائماً كحد أدنى من الحماية.</td>
            <td class="no-col">no service password-encryption</td>
        </tr>
        <tr>
            <td class="cmd-col">service timestamps log datetime msec</td>
            <td class="mode-col">Global Config</td>
            <td>إضافة تاريخ ووقت بالمللي ثانية لكل رسالة syslog. ضروري للتشخيص الدقيق.</td>
            <td class="no-col">no service timestamps</td>
        </tr>
        <tr>
            <td class="cmd-col">logging buffered &lt;size&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تخزين رسائل syslog في RAM بدلاً من عرضها على console فقط. <code class="inline">logging buffered 51200</code> = 50KB.</td>
            <td class="no-col">no logging buffered</td>
        </tr>
        <tr>
            <td class="cmd-col">logging &lt;ip&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إرسال رسائل syslog إلى خادم syslog مركزي (مثل Kiwi أو Splunk).</td>
            <td class="no-col">no logging &lt;ip&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">logging trap &lt;level&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد مستوى الخطورة الأدنى للرسائل المرسلة إلى خادم syslog. المستويات: emergencies(0) → debugging(7).</td>
            <td class="no-col">no logging trap</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مثال: إعداد نظامي شامل</div>
<div class="code-block-title">مثال 3.1: إعداد أولي كامل قبل أي تكوين شبكي</div>
<div class="code-block">
Router&gt; <span class="prompt">enable</span>
Router# <span class="prompt">configure terminal</span>
Router(config)# <span class="prompt">hostname Cairo-Edge-R01</span>
Cairo-Edge-R01(config)# <span class="prompt">banner motd ^C</span>
***********************************************
*  CAIRO EDGE ROUTER - AUTHORIZED ACCESS ONLY *
*  All sessions are logged and monitored      *
*  Unauthorized access will be prosecuted     *
***********************************************
^C
Cairo-Edge-R01(config)# <span class="prompt">no ip domain-lookup</span>
Cairo-Edge-R01(config)# <span class="prompt">clock timezone EET 2 0</span>
Cairo-Edge-R01(config)# <span class="prompt">service password-encryption</span>
Cairo-Edge-R01(config)# <span class="prompt">service timestamps log datetime msec localtime show-timezone</span>
Cairo-Edge-R01(config)# <span class="prompt">service timestamps debug datetime msec localtime show-timezone</span>
Cairo-Edge-R01(config)# <span class="prompt">logging buffered 51200 informational</span>
Cairo-Edge-R01(config)# <span class="prompt">ntp server 162.159.200.1</span>      <span class="comment">! Cloudflare NTP</span>
Cairo-Edge-R01(config)# <span class="prompt">ntp update-calendar</span>
Cairo-Edge-R01(config)# <span class="prompt">line console 0</span>
Cairo-Edge-R01(config-line)# <span class="prompt">logging synchronous</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exec-timeout 10 0</span>            <span class="comment">! 10 دقائق</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exit</span>
Cairo-Edge-R01(config)# <span class="prompt">line vty 0 4</span>
Cairo-Edge-R01(config-line)# <span class="prompt">logging synchronous</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exec-timeout 5 0</span>             <span class="comment">! 5 دقائق فقط</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exit</span>
Cairo-Edge-R01(config)# <span class="prompt">exit</span>
Cairo-Edge-R01# <span class="prompt">copy run start</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">نصيحة للاب</div>
    <div class="tip-box-body">
        عند بناء لاب تدريبي، نفّذ <code class="inline">no ip domain-lookup</code> و <code class="inline">logging synchronous</code> على <code class="inline">line console 0</code> و <code class="inline">line vty 0 4</code> في بداية كل جلسة. هذان الأمران يضاعفان سرعة كتابتك للأوامر ويمنعان تشويش رسائل syslog على ما تكتب، وهو من أكثر النصائح عملية التي يقدّرها الطلاب في اللاب.
    </div>
</div>


<!-- ============ SECTION 4: PASSWORDS & BASIC SECURITY ============ -->
<div class="chapter-header">
    <span class="chapter-tag">CHAPTER 04</span>
    <div class="chapter-title">كلمات المرور والأمان الأساسي</div>
    <div class="chapter-title-en">Passwords &amp; Basic Security</div>
    <div class="chapter-divider"></div>
</div>

<div class="body-text">
    تأمين الوصول إلى أجهزة الشبكة هو خط الدفاع الأول في حماية البنية التحتية. تتضمن هذه المرحلة تعيين كلمات مرور قوية على كل منافذ الوصول (Console، VTY، AUX)، تشفيرها في الإعداد، وتفعيل أساليب مصادقة أكثر تقدماً مثل AAA والـ SSH بدلاً من Telnet. الجدير بالذكر أن كلمات المرور في IOS لها أنواع مختلفة (Type 0، 5، 7، 8، 9) تختلف في قوة التشفير، فهم هذه الأنواع ضروري لاختيار المستوى المناسب من الأمان.
</div>

<div class="section-title">أنواع كلمات المرور في Cisco IOS</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 20%;">النوع</th>
            <th style="width: 25%;">خوارزمية التشفير</th>
            <th style="width: 35%;">مستوى الأمان</th>
            <th style="width: 20%;">متى يُستخدم</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">Type 0</code></td><td>Plain Text (بدون تشفير)</td><td>لا أمان (نص ظاهر)</td><td>محظور في الإنتاج</td></tr>
        <tr><td><code class="inline">Type 5</code></td><td>MD5 (Salted)</td><td>متوسط (مخترق الآن)</td><td>قديم - تجنّبه</td></tr>
        <tr><td><code class="inline">Type 7</code></td><td>Cisco Vigenère (ضعيف)</td><td>ضعيف جداً (قابل للفك بسهولة)</td><td>تلقائي من <code class="inline">service password-encryption</code> - كحد أدنى</td></tr>
        <tr><td><code class="inline">Type 8</code></td><td>PBKDF2-SHA256</td><td>قوي (10,000 دورة)</td><td>موصى به حديثاً</td></tr>
        <tr><td><code class="inline">Type 9</code></td><td>Scrypt</td><td>قوي جداً (memory-hard)</td><td>الأقوى الموصى به</td></tr>
    </tbody>
</table>

<div class="section-title">كلمة مرور وضع التنفيذ المميّز (Enable Password)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
            <th style="width: 17%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">enable password &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين كلمة مرور للوصول إلى Privileged EXEC. تُخزن كنص ظاهر (Type 0) ما لم يُفعّل <code class="inline">service password-encryption</code> فتتحول إلى Type 7 (ضعيف). <strong>تجنّب هذا الأمر</strong>.</td>
            <td class="no-col">no enable password</td>
        </tr>
        <tr>
            <td class="cmd-col">enable secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين كلمة مرور مشفّرة بـ MD5 (Type 5). أقوى بكثير من <code class="inline">enable password</code> ويلغي مفعولها إن وُجدت.</td>
            <td class="no-col">no enable secret</td>
        </tr>
        <tr>
            <td class="cmd-col">enable algorithm-type sha256 secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين كلمة مرور مشفّرة بـ SHA256 (Type 8). أكثر أماناً من Type 5. متاح في IOS 15+.</td>
            <td class="no-col">no enable secret</td>
        </tr>
        <tr>
            <td class="cmd-col">enable algorithm-type scrypt secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين كلمة مرور مشفّرة بـ Scrypt (Type 9) - الأقوى حالياً. متاح في IOS 15.3(3)M+.</td>
            <td class="no-col">no enable secret</td>
        </tr>
        <tr>
            <td class="cmd-col">enable secret level &lt;1-15&gt; &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين كلمة مرور لـ Privileged EXEC لمستوى صلاحية معين (1-15). المستوى 15 = Administrator الكامل.</td>
            <td class="no-col">no enable secret level &lt;1-15&gt;</td>
        </tr>
    </tbody>
</table>

<div class="section-title">كلمات مرور خطوط الوصول (Console / VTY / AUX)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 28%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 38%;">الشرح</th>
            <th style="width: 17%;">العكس (no)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">line console 0</td>
            <td class="mode-col">Global → Line</td>
            <td>الدخول إلى وضع إعداد خط console (المنفذ الفيزيائي التسلسلي).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">line vty 0 4</td>
            <td class="mode-col">Global → Line</td>
            <td>إعداد أول 5 جلسات VTY (Telnet/SSH). بعض الأجهزة الحديثة تدعم 16 (0 15).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">line vty 0 15</td>
            <td class="mode-col">Global → Line</td>
            <td>إعداد كل جلسات VTY الست عشرة دفعة واحدة.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">line aux 0</td>
            <td class="mode-col">Global → Line</td>
            <td>إعداد منفذ AUX (النادر الآن، كان يستخدم للمودم). ينصح بتعطيله.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">password &lt;pass&gt;</td>
            <td class="mode-col">Line Config</td>
            <td>تعيين كلمة مرور لخط الوصول المحدد. تُخزن كـ Type 0 أو 7 (ضعيفة). قديم.</td>
            <td class="no-col">no password</td>
        </tr>
        <tr>
            <td class="cmd-col">login</td>
            <td class="mode-col">Line Config</td>
            <td>تفعيل طلب كلمة المرور عند الدخول إلى الخط. يتطلب أن تكون <code class="inline">password</code> معرّفة. قديم.</td>
            <td class="no-col">no login</td>
        </tr>
        <tr>
            <td class="cmd-col">login local</td>
            <td class="mode-col">Line Config</td>
            <td>تفعيل المصادقة عبر قاعدة بيانات المستخدمين المحلية (المعرّفة بـ <code class="inline">username</code>). <strong>موصى به</strong>.</td>
            <td class="no-col">no login local</td>
        </tr>
        <tr>
            <td class="cmd-col">login authentication &lt;name&gt;</td>
            <td class="mode-col">Line Config</td>
            <td>تفعيل المصادقة عبر AAA (يستخدم RADIUS/TACACS+). يتطلب تفعيل <code class="inline">aaa new-model</code>.</td>
            <td class="no-col">no login authentication</td>
        </tr>
        <tr>
            <td class="cmd-col">transport input ssh</td>
            <td class="mode-col">Line Config</td>
            <td>تحديد أن بروتوكول SSH فقط مسموح للوصول (يمنع Telnet الأقل أماناً). <strong>موصى به بشدة</strong>.</td>
            <td class="no-col">transport input all</td>
        </tr>
        <tr>
            <td class="cmd-col">transport input telnet ssh</td>
            <td class="mode-col">Line Config</td>
            <td>السماح بكل من Telnet و SSH (لا يوصى به للإنتاج).</td>
            <td class="no-col">transport input none</td>
        </tr>
        <tr>
            <td class="cmd-col">transport output ssh</td>
            <td class="mode-col">Line Config</td>
            <td>تحديد أن الجهاز يسمح ببدء جلسات SSH خارجية فقط (مفيد أمنياً).</td>
            <td class="no-col">transport output all</td>
        </tr>
    </tbody>
</table>

<div class="section-title">إنشاء حسابات المستخدمين المحلية</div>
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
            <td class="cmd-col">username &lt;name&gt; privilege &lt;0-15&gt; secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء حساب مستخدم محلي مع كلمة مرور مشفّرة Type 5 (MD5) ومستوى صلاحية. <code class="inline">privilege 15</code> = Administrator كامل.</td>
            <td class="no-col">no username &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">username &lt;name&gt; algorithm-type sha256 secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء حساب مع كلمة مرور Type 8 (SHA256). أكثر أماناً.</td>
            <td class="no-col">no username &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">username &lt;name&gt; algorithm-type scrypt secret &lt;pass&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إنشاء حساب مع كلمة مرور Type 9 (Scrypt) - الأقوى حالياً.</td>
            <td class="no-col">no username &lt;name&gt;</td>
        </tr>
        <tr>
            <td class="cmd-col">username &lt;name&gt; view &lt;view-name&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>إسناد Role-Based View إلى المستخدم (للسيطرة الدقيقة على الأوامر المتاحة لكل دور).</td>
            <td class="no-col">no username &lt;name&gt; view</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa new-model</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل نموذج AAA (Authentication, Authorization, Accounting). يحوّل كل المصادقة إلى AAA افتراضياً.</td>
            <td class="no-col">no aaa new-model</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authentication login default local</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط طريقة المصادقة الافتراضية لكل خطوط الوصول باستخدام قاعدة المستخدمين المحلية.</td>
            <td class="no-col">no aaa authentication login default</td>
        </tr>
        <tr>
            <td class="cmd-col">aaa authorization exec default local</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط التفويض الافتراضي لمنح المستخدم وضع EXEC حسب <code class="inline">privilege</code> المعرّف في حسابه المحلي.</td>
            <td class="no-col">no aaa authorization exec default</td>
        </tr>
    </tbody>
</table>

<div class="section-title">إعداد SSH (البديل الآمن لـ Telnet)</div>
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
            <td class="cmd-col">ip domain-name &lt;domain&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تعيين اسم النطاق. مطلوب لتوليد مفاتيح RSA لـ SSH.</td>
            <td class="no-col">no ip domain-name</td>
        </tr>
        <tr>
            <td class="cmd-col">crypto key generate rsa modulus 2048</td>
            <td class="mode-col">Global Config</td>
            <td>توليد زوج مفاتيح RSA بطول 2048 بت (موصى به). يقوم بتفعيل SSH v1 تلقائياً. أدنى طول مقبول حالياً 1024.</td>
            <td class="no-col">crypto key zeroize rsa</td>
        </tr>
        <tr>
            <td class="cmd-col">crypto key zeroize rsa</td>
            <td class="mode-col">Global Config</td>
            <td>حذف كل مفاتيح RSA الحالية. يوقف SSH.</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ssh version 2</td>
            <td class="mode-col">Global Config</td>
            <td>تفعيل SSHv2 فقط (الأكثر أماناً). يرفض اتصالات SSHv1.</td>
            <td class="no-col">no ip ssh version</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ssh time-out &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>ضبط مهلة تسجيل الدخول لـ SSH بالثواني (الافتراضي 120).</td>
            <td class="no-col">no ip ssh time-out</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ssh authentication-retries &lt;1-5&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>عدد محاولات تسجيل الدخول قبل قطع الاتصال (الافتراضي 3).</td>
            <td class="no-col">no ip ssh authentication-retries</td>
        </tr>
        <tr>
            <td class="cmd-col">ip ssh source-interface &lt;iface&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>تحديد الواجهة المصدر التي يستخدمها الجهاز عند بدء جلسات SSH خارجية (مفيد في الفحص الأمني للسجلات).</td>
            <td class="no-col">no ip ssh source-interface</td>
        </tr>
        <tr>
            <td class="cmd-col">show ip ssh</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض حالة وإعدادات SSH (الإصدار، timeout، retries).</td>
            <td class="no-col">N/A</td>
        </tr>
        <tr>
            <td class="cmd-col">show ssh</td>
            <td class="mode-col">Privileged EXEC</td>
            <td>عرض جلسات SSH النشطة حالياً على الجهاز.</td>
            <td class="no-col">N/A</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مثال شامل: تأمين راوتر كامل</div>
<div class="code-block-title">مثال 4.1: إعداد أمان كامل لراوتر</div>
<div class="code-block">
Router(config)# <span class="prompt">hostname Cairo-Edge-R01</span>
Cairo-Edge-R01(config)# <span class="prompt">service password-encryption</span>
Cairo-Edge-R01(config)# <span class="prompt">no ip domain-lookup</span>
Cairo-Edge-R01(config)# <span class="prompt">no service tcp-small-servers</span>
Cairo-Edge-R01(config)# <span class="prompt">no service udp-small-servers</span>
Cairo-Edge-R01(config)# <span class="prompt">no ip http server</span>                <span class="comment">! تعطيل HTTP القديم</span>
Cairo-Edge-R01(config)# <span class="prompt">no ip http secure-server</span>       <span class="comment">! تعطيل HTTPS (حسب سياسة الأمان)</span>

<span class="comment">! إنشاء حسابات المستخدمين</span>
Cairo-Edge-R01(config)# <span class="prompt">username admin privilege 15 algorithm-type scrypt secret S3cr3t-P@ss!2026</span>
Cairo-Edge-R01(config)# <span class="prompt">username operator privilege 5 algorithm-type sha256 secret Oper@tor2026</span>
Cairo-Edge-R01(config)# <span class="prompt">username monitor privilege 1 algorithm-type sha256 secret M0n!tor2026</span>

<span class="comment">! كلمة مرور enable</span>
Cairo-Edge-R01(config)# <span class="prompt">enable algorithm-type scrypt secret En@ble!S3cr3t!</span>

<span class="comment">! إعداد SSH</span>
Cairo-Edge-R01(config)# <span class="prompt">ip domain-name cairo-net.local</span>
Cairo-Edge-R01(config)# <span class="prompt">crypto key generate rsa modulus 2048</span>
The name for the keys will be: Cairo-Edge-R01.cairo-net.local
% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 4 seconds)

Cairo-Edge-R01(config)# <span class="prompt">ip ssh version 2</span>
Cairo-Edge-R01(config)# <span class="prompt">ip ssh time-out 60</span>
Cairo-Edge-R01(config)# <span class="prompt">ip ssh authentication-retries 3</span>

<span class="comment">! تأمين console</span>
Cairo-Edge-R01(config)# <span class="prompt">line console 0</span>
Cairo-Edge-R01(config-line)# <span class="prompt">login local</span>
Cairo-Edge-R01(config-line)# <span class="prompt">logging synchronous</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exec-timeout 5 0</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exit</span>

<span class="comment">! تأمين VTY - SSH فقط</span>
Cairo-Edge-R01(config)# <span class="prompt">line vty 0 15</span>
Cairo-Edge-R01(config-line)# <span class="prompt">login local</span>
Cairo-Edge-R01(config-line)# <span class="prompt">transport input ssh</span>
Cairo-Edge-R01(config-line)# <span class="prompt">transport output ssh</span>
Cairo-Edge-R01(config-line)# <span class="prompt">logging synchronous</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exec-timeout 10 0</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exit</span>

<span class="comment">! تعطيل AUX</span>
Cairo-Edge-R01(config)# <span class="prompt">line aux 0</span>
Cairo-Edge-R01(config-line)# <span class="prompt">no exec</span>
Cairo-Edge-R01(config-line)# <span class="prompt">exit</span>

<span class="comment">! تفعيل AAA لاستخدام RADIUS لاحقاً</span>
Cairo-Edge-R01(config)# <span class="prompt">aaa new-model</span>
Cairo-Edge-R01(config)# <span class="prompt">aaa authentication login default local</span>
Cairo-Edge-R01(config)# <span class="prompt">aaa authorization exec default local</span>
Cairo-Edge-R01(config)# <span class="prompt">exit</span>
Cairo-Edge-R01# <span class="prompt">copy run start</span>
</div>

<div class="tip-box">
    <div class="tip-box-title">قاعدة ذهبية للأمان</div>
    <div class="tip-box-body">
        استخدم دائماً <code class="inline">enable secret</code> بدلاً من <code class="inline">enable password</code> (الذي يُخزن كنص ظاهر). وعند توفر IOS 15.3+، استخدم <code class="inline">algorithm-type scrypt</code> للوصول إلى أقوى تشفير متاح (Type 9). تجنّب أيضاً <code class="inline">password</code> العادية في خطوط VTY، واستخدم بدلاً منها <code class="inline">login local</code> مع حسابات مستخدمين محلية، أو أفضل: AAA عبر RADIUS/TACACS+.
    </div>
</div>

<div class="warn-box">
    <div class="warn-box-title">أخطاء شائعة يجب تجنّبها</div>
    <div class="warn-box-body">
        1) <strong>نسيان <code class="inline">no shutdown</code></strong> على الواجهة بعد ضبط IP فيبقى الواجهة معطّلة.<br>
        2) <strong>نسيان <code class="inline">login</code> أو <code class="inline">login local</code></strong> على خط VTY، فيدخل أي شخص بدون مصادقة.<br>
        3) <strong>استخدام <code class="inline">transport input telnet</code></strong> وحده، فيتمرّر كل الباسوورد بـ plain text على الشبكة.<br>
        4) <strong>عدم ضبط <code class="inline">exec-timeout</code></strong> على VTY فيبقى المستخدم مسجّلاً للدخول إلى أجل غير مسمى.<br>
        5) <strong>استخدام Telnet بدلاً من SSH</strong> في الإنتاج - هذا انتحار أمني في أي مراجعة.
    </div>
</div>

<div class="section-title">مستويات الصلاحيات (Privilege Levels)</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 15%;">المستوى</th>
            <th style="width: 35%;">الصلاحيات</th>
            <th style="width: 50%;">الاستخدام النموذجي</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code class="inline">Level 0</code></td><td>أوامر disable/enable/logout/exit فقط</td><td>مستوى غير مستخدم عملياً، أقل صلاحية.</td></tr>
        <tr><td><code class="inline">Level 1</code></td><td>User EXEC (الافتراضي)</td><td>مستخدمين عاديين لعرض إحصائيات الواجهة والـ routing.</td></tr>
        <tr><td><code class="inline">Level 2-14</code></td><td>مخصص للتخصيص</td><td>يتيح تخصيص صلاحيات دقيقة لمستخدمين محددين (مثلاً مسؤول شبكة فرعية فقط).</td></tr>
        <tr><td><code class="inline">Level 15</code></td><td>Privileged EXEC الكامل (enable mode)</td><td>Administrator - كل الصلاحيات، حفظ الإعدادات وإعادة التحميل.</td></tr>
    </tbody>
</table>

<div class="section-title">أوامر إضافية لحماية الجهاز</div>
<table class="cmd-table">
    <thead>
        <tr>
            <th style="width: 35%;">الأمر</th>
            <th style="width: 17%;">الوضع</th>
            <th style="width: 35%;">الشرح</th>
            <th style="width: 13%;">العكس</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="cmd-col">security passwords min-length &lt;n&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>فرض طول أدنى لكلمات المرور (موصى به: 12+).</td>
            <td class="no-col">no security passwords min-length</td>
        </tr>
        <tr>
            <td class="cmd-col">login block-for &lt;sec&gt; attempts &lt;n&gt; within &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>حماية ضد brute-force: بعد N محاولات فاشلة خلال X ثانية، يحظر الجهاز كل المحاولات لمدة Y ثانية. <code class="inline">login block-for 60 attempts 3 within 30</code>.</td>
            <td class="no-col">no login block-for</td>
        </tr>
        <tr>
            <td class="cmd-col">login quiet-mode access-class &lt;acl&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>السماح لمصادر موثوقة (في الـ ACL) بالوصول حتى أثناء فترة الحظر.</td>
            <td class="no-col">no login quiet-mode</td>
        </tr>
        <tr>
            <td class="cmd-col">login delay &lt;sec&gt;</td>
            <td class="mode-col">Global Config</td>
            <td>فرض ثانية أو أكثر بين كل محاولة دخول (مضاد brute-force إضافي).</td>
            <td class="no-col">no login delay</td>
        </tr>
        <tr>
            <td class="cmd-col">login on-failure log</td>
            <td class="mode-col">Global Config</td>
            <td>تسجيل كل محاولة دخول فاشلة في syslog.</td>
            <td class="no-col">no login on-failure log</td>
        </tr>
        <tr>
            <td class="cmd-col">login on-success log</td>
            <td class="mode-col">Global Config</td>
            <td>تسجيل كل محاولة دخول ناجحة في syslog.</td>
            <td class="no-col">no login on-success log</td>
        </tr>
        <tr>
            <td class="cmd-col">access-class &lt;acl&gt; in</td>
            <td class="mode-col">Line Config</td>
            <td>تقييد الوصول إلى VTY بمصادر محددة في ACL (مثلاً: فقط شبكة الإدارة 10.10.10.0/24).</td>
            <td class="no-col">no access-class</td>
        </tr>
    </tbody>
</table>

<div class="section-title">مثال: حماية متقدمة ضد brute-force</div>
<div class="code-block">
Router(config)# <span class="prompt">login block-for 120 attempts 3 within 30</span>
Router(config)# <span class="prompt">login quiet-mode access-class MGMT-NETWORK</span>
Router(config)# <span class="prompt">login delay 2</span>
Router(config)# <span class="prompt">login on-failure log</span>
Router(config)# <span class="prompt">login on-success log</span>
Router(config)# <span class="prompt">ip access-list standard MGMT-NETWORK</span>
Router(config-std-nacl)# <span class="prompt">permit 10.10.10.0 0.0.0.255</span>
Router(config-std-nacl)# <span class="prompt">permit host 192.168.1.100</span>
Router(config-std-nacl)# <span class="prompt">exit</span>
Router(config)# <span class="prompt">line vty 0 15</span>
Router(config-line)# <span class="prompt">access-class MGMT-NETWORK in</span>
Router(config-line)# <span class="prompt">exit</span>
</div>

"""
