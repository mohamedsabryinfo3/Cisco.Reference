# -*- coding: utf-8 -*-
"""Part 00: HTML Head + CSS + Cover + TOC"""

HEAD = """<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>مذكرة أوامر سيسكو الشاملة - Cisco IOS Commands Reference</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@page { size: 210mm 297mm; margin: 0; }
:root {
    --c-bg: #FFFFFF;
    --c-text: #1A1A1A;
    --c-text-soft: #4A4A4A;
    --c-cisco-blue: #049FD9;
    --c-cisco-turq: #00BCEB;
    --c-cisco-dark: #002B5C;
    --c-cisco-light: #E0F4FA;
    --c-code-bg: #F4F6F9;
    --c-code-border: #D1D9E0;
    --c-tip-bg: #FFF7E0;
    --c-tip-border: #FFB800;
    --c-warn-bg: #FDECEC;
    --c-warn-border: #E74C3C;
    --c-table-header: #002B5C;
    --c-table-alt: #F8FBFC;
}
* { box-sizing: border-box; }
html, body {
    margin: 0; padding: 0; width: 210mm;
    background: var(--c-bg);
    color: var(--c-text);
    font-family: 'Cairo', 'Noto Sans', sans-serif;
    font-size: 11pt; line-height: 1.6; direction: rtl;
}
@media screen {
    html { background: #888; display: flex; justify-content: center; }
    body { margin: 20px auto; box-shadow: 0 0 30px rgba(0,0,0,0.4); }
}

.cover {
    width: 210mm; height: 297mm; box-sizing: border-box;
    background: linear-gradient(135deg, #002B5C 0%, #049FD9 100%);
    color: #FFFFFF; position: relative; overflow: hidden; break-after: page;
}
.cover::before {
    content: ""; position: absolute; top: -100px; left: -100px;
    width: 400px; height: 400px; border-radius: 50%;
    background: rgba(0, 188, 235, 0.15);
}
.cover::after {
    content: ""; position: absolute; bottom: -150px; right: -150px;
    width: 500px; height: 500px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
}
.cover-inner {
    position: relative; z-index: 2; height: 100%;
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 50mm 25mm 30mm 25mm;
}
.cover-top { display: flex; justify-content: space-between; align-items: center; }
.cover-badge {
    background: rgba(255, 255, 255, 0.18); border: 2px solid rgba(255, 255, 255, 0.4);
    padding: 8px 18px; border-radius: 30px; font-size: 12pt; font-weight: 600;
}
.cover-logo-text {
    font-family: 'Inter', sans-serif; font-size: 28pt; font-weight: 800;
    letter-spacing: 2px; color: #FFFFFF;
}
.cover-logo-text span { color: #00BCEB; }
.cover-middle { text-align: center; padding: 0 10mm; }
.cover-title-ar {
    font-size: 38pt; font-weight: 900; line-height: 1.2;
    margin-bottom: 15px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.cover-title-en {
    font-family: 'Inter', sans-serif; font-size: 17pt; font-weight: 600;
    color: #00BCEB; margin-bottom: 30px; letter-spacing: 1px;
}
.cover-subtitle {
    font-size: 13pt; font-weight: 400; line-height: 1.6;
    color: rgba(255, 255, 255, 0.92); max-width: 80%; margin: 0 auto 30px;
}
.cover-tags { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-top: 25px; }
.cover-tag {
    background: rgba(0, 188, 235, 0.25); border: 1px solid #00BCEB;
    padding: 6px 14px; border-radius: 20px; font-size: 11pt; font-weight: 500;
}
.cover-bottom { text-align: center; }
.cover-decor-line { width: 80px; height: 4px; background: #00BCEB; margin: 15px auto; border-radius: 2px; }
.cover-meta {
    font-size: 10pt; color: rgba(255, 255, 255, 0.7); line-height: 1.7;
    border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 20px; margin-top: 15px;
}

.toc-page { padding: 25mm 22mm; break-after: page; }
.toc-title {
    font-size: 26pt; font-weight: 800; color: var(--c-cisco-dark);
    text-align: center; margin-bottom: 8px; border-bottom: 3px solid var(--c-cisco-blue); padding-bottom: 12px;
}
.toc-subtitle { text-align: center; color: var(--c-text-soft); font-size: 11pt; margin-bottom: 30px; }
.toc-list { list-style: none; padding: 0; margin: 0; }
.toc-item {
    display: flex; align-items: baseline; padding: 6px 0;
    font-size: 10.5pt; border-bottom: 1px dotted #D0D7DE; line-height: 1.5;
}
.toc-num {
    background: var(--c-cisco-blue); color: #FFF; min-width: 26px; height: 26px;
    border-radius: 6px; display: inline-flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 9.5pt; margin-left: 12px; flex-shrink: 0;
}
.toc-text { flex: 1; color: var(--c-text); font-weight: 500; }
.toc-text small { color: var(--c-text-soft); font-weight: 400; font-size: 9pt; }
.toc-page-num { color: var(--c-cisco-blue); font-weight: 700; margin-right: 8px; }

.main-content { padding: 16mm 16mm 18mm 16mm; }
.chapter-header { break-after: avoid; break-inside: avoid; margin-top: 20px; margin-bottom: 14px; }
.chapter-header:first-of-type { margin-top: 0; }
.chapter-tag {
    display: inline-block; background: var(--c-cisco-blue); color: #FFF;
    padding: 4px 14px; border-radius: 4px; font-size: 9pt; font-weight: 600;
    letter-spacing: 1px; margin-bottom: 8px;
}
.chapter-title { font-size: 20pt; font-weight: 800; color: var(--c-cisco-dark); line-height: 1.25; margin: 6px 0 4px; }
.chapter-title-en { font-family: 'Inter', sans-serif; color: var(--c-cisco-blue); font-size: 11pt; font-weight: 600; margin-bottom: 8px; }
.chapter-divider { width: 100%; height: 2px; background: linear-gradient(to left, var(--c-cisco-blue), transparent); margin: 8px 0; }

.section { margin-top: 18px; }
.section-title {
    font-size: 13pt; font-weight: 700; color: var(--c-cisco-dark);
    border-right: 5px solid var(--c-cisco-blue); padding-right: 12px; margin: 14px 0 8px; line-height: 1.4;
}
.subsection-title { font-size: 11.5pt; font-weight: 700; color: var(--c-cisco-blue); margin: 12px 0 6px; }
.body-text { margin: 8px 0; text-align: justify; line-height: 1.75; color: var(--c-text); }
.body-text strong { color: var(--c-cisco-dark); font-weight: 700; }

.cmd-table {
    width: 100%; border-collapse: collapse; margin: 12px 0;
    font-size: 9.5pt; background: #FFF; border: 1px solid var(--c-code-border); break-inside: avoid;
}
.cmd-table th {
    background: var(--c-table-header); color: #FFF; padding: 7px 9px;
    text-align: right; font-weight: 700; font-size: 9.5pt; border-bottom: 2px solid var(--c-cisco-blue);
}
.cmd-table td { padding: 6px 9px; border-bottom: 1px solid #E5EBF0; vertical-align: top; line-height: 1.5; }
.cmd-table tr:nth-child(even) td { background: var(--c-table-alt); }
.cmd-table tr:last-child td { border-bottom: none; }
.cmd-table code {
    font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 9pt;
    color: var(--c-cisco-dark); background: #F0F4F8; padding: 1px 5px; border-radius: 3px;
    direction: ltr; display: inline-block; white-space: nowrap;
}
.cmd-table .cmd-col {
    direction: ltr; text-align: left; font-family: 'JetBrains Mono', monospace;
    font-size: 9pt; color: #B1272B; background: #FFF8F8; font-weight: 500;
    white-space: pre-wrap; word-wrap: break-word; word-break: break-all;
}
.cmd-table .mode-col { color: var(--c-cisco-blue); font-weight: 600; font-size: 8.5pt; direction: ltr; text-align: left; white-space: nowrap; }
.cmd-table .example-col {
    direction: ltr; text-align: left; font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt; background: #F8F8F8; color: #333; white-space: pre-wrap;
    word-break: break-word; border-right: 1px solid #EEE; padding-right: 8px;
}
.cmd-table .no-col {
    direction: ltr; text-align: left; font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt; color: #888; font-style: italic; white-space: pre-wrap; word-break: break-word;
}

.code-block {
    background: var(--c-code-bg); border: 1px solid var(--c-code-border);
    border-right: 4px solid var(--c-cisco-blue); padding: 9px 13px; margin: 10px 0;
    border-radius: 4px; direction: ltr; text-align: left;
    font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 9pt;
    line-height: 1.55; color: #2D3436; white-space: pre-wrap; word-break: break-word; break-inside: avoid;
}
.code-block-title {
    background: var(--c-cisco-dark); color: #FFF; padding: 4px 10px;
    font-size: 9pt; font-weight: 600; border-radius: 4px 4px 0 0;
    direction: rtl; text-align: right; margin-bottom: -1px;
}

.tip-box {
    background: var(--c-tip-bg); border: 1px solid var(--c-tip-border);
    border-right: 5px solid var(--c-tip-border); padding: 9px 13px;
    margin: 11px 0; border-radius: 4px; break-inside: avoid;
}
.tip-box-title { color: #B7791F; font-weight: 700; margin-bottom: 4px; font-size: 10pt; }
.tip-box-body { color: #4A3A1A; font-size: 10pt; line-height: 1.6; }

.warn-box {
    background: var(--c-warn-bg); border: 1px solid var(--c-warn-border);
    border-right: 5px solid var(--c-warn-border); padding: 9px 13px;
    margin: 11px 0; border-radius: 4px; break-inside: avoid;
}
.warn-box-title { color: #C0392B; font-weight: 700; margin-bottom: 4px; font-size: 10pt; }
.warn-box-body { color: #4A1A1A; font-size: 10pt; line-height: 1.6; }

.info-box {
    background: var(--c-cisco-light); border: 1px solid var(--c-cisco-blue);
    border-right: 5px solid var(--c-cisco-blue); padding: 9px 13px;
    margin: 11px 0; border-radius: 4px; break-inside: avoid;
}
.info-box-title { color: var(--c-cisco-dark); font-weight: 700; margin-bottom: 4px; font-size: 10pt; }
.info-box-body { color: #1A3A4A; font-size: 10pt; line-height: 1.6; }

code.inline {
    font-family: 'JetBrains Mono', monospace; background: #F0F4F8;
    color: var(--c-cisco-dark); padding: 1px 5px; border-radius: 3px;
    font-size: 9.5pt; direction: ltr; display: inline-block;
}
.mode-badge {
    display: inline-block; background: var(--c-cisco-dark); color: #00BCEB;
    padding: 1px 6px; border-radius: 3px; font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt; font-weight: 600; direction: ltr; white-space: nowrap;
}

.subnet-table {
    width: 100%; border-collapse: collapse; font-size: 8.5pt;
    margin: 12px 0; break-inside: avoid;
}
.subnet-table th { background: var(--c-cisco-dark); color: #FFF; padding: 5px; text-align: center; font-size: 8.5pt; }
.subnet-table td { padding: 4px 5px; text-align: center; border-bottom: 1px solid #E5EBF0; font-family: 'JetBrains Mono', monospace; font-size: 8.5pt; }
.subnet-table tr:nth-child(even) td { background: var(--c-table-alt); }

.question-block {
    background: #FAFAFA; border: 1px solid #E0E0E0;
    border-right: 4px solid var(--c-cisco-blue); padding: 11px 13px;
    margin: 12px 0; border-radius: 4px; break-inside: avoid;
}
.question-num {
    background: var(--c-cisco-blue); color: #FFF; padding: 2px 8px;
    border-radius: 3px; font-weight: 700; font-size: 9pt; margin-left: 6px;
}
.question-text { font-weight: 600; color: var(--c-cisco-dark); margin: 6px 0; line-height: 1.6; }
.answer-block {
    background: #F0F8F4; border-right: 4px solid #27AE60; padding: 7px 11px;
    margin-top: 8px; border-radius: 4px; font-size: 10pt; line-height: 1.6;
}
.answer-label { color: #27AE60; font-weight: 700; margin-left: 4px; }

.lab-scenario {
    background: linear-gradient(to bottom, #F8FBFC 0%, #FFFFFF 100%);
    border: 1px solid var(--c-cisco-blue); border-radius: 8px;
    padding: 0; margin: 16px 0; break-inside: avoid; overflow: hidden;
}
.lab-scenario-header {
    background: linear-gradient(to left, var(--c-cisco-dark), var(--c-cisco-blue));
    color: #FFF; padding: 9px 14px; font-weight: 700; font-size: 11pt;
}
.lab-scenario-body { padding: 11px 14px; }
.lab-step { display: flex; gap: 10px; margin: 9px 0; break-inside: avoid; }
.lab-step-num {
    background: var(--c-cisco-blue); color: #FFF; min-width: 24px; height: 24px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 10pt; flex-shrink: 0;
}
.lab-step-content { flex: 1; font-size: 10pt; line-height: 1.6; }

.footer-note { margin-top: 30px; padding-top: 10px; border-top: 1px solid #E0E0E0; text-align: center; color: #888; font-size: 9pt; }
.no-break { break-inside: avoid; }
</style>
</head>
<body>
"""

COVER = """
<!-- ============ COVER PAGE ============ -->
<div class="cover">
    <div class="cover-inner">
        <div class="cover-top">
            <div class="cover-logo-text">CISCO<span> IOS</span></div>
            <div class="cover-badge">CCNA &amp; CCNP</div>
        </div>
        <div class="cover-middle">
            <div class="cover-title-ar">مذكرة أوامر سيسكو الشاملة</div>
            <div class="cover-title-en">Cisco IOS Commands Complete Reference</div>
            <div class="cover-decor-line"></div>
            <div class="cover-subtitle">
                مرجع احترافي وشامل لأوامر راوترات وسويتشات سيسكو (Cisco IOS) مخصص للمذاكرة والمراجعة الشاملة لامتحانات CCNA 200-301 و CCNP ENARSI مع شرح عربي مفصل وأمثلة عملية
            </div>
            <div class="cover-tags">
                <span class="cover-tag">Router Modes</span>
                <span class="cover-tag">VLANs &amp; Trunking</span>
                <span class="cover-tag">OSPF / EIGRP</span>
                <span class="cover-tag">BGP</span>
                <span class="cover-tag">ACLs / NAT</span>
                <span class="cover-tag">IPv6</span>
                <span class="cover-tag">HSRP/VRRP</span>
                <span class="cover-tag">Port Security</span>
                <span class="cover-tag">QoS</span>
            </div>
        </div>
        <div class="cover-bottom">
            <div class="cover-decor-line"></div>
            <div class="cover-meta">
                المرجع التقني الشامل &middot; أعدّه مهندس شبكات معتمد<br>
                Cisco IOS Commands Reference Guide &middot; CCNA 200-301 &amp; CCNP ENARSI Coverage<br>
                Edition 1.0 &middot; 2026
            </div>
        </div>
    </div>
</div>
"""

TOC = """
<!-- ============ TABLE OF CONTENTS ============ -->
<div class="toc-page">
    <div class="toc-title">جدول المحتويات</div>
    <div class="toc-subtitle">Table of Contents &mdash; 27 قسماً رئيسياً</div>
    <ul class="toc-list">
        <li class="toc-item"><span class="toc-num">1</span><span class="toc-text">المقدمة وكيفية استخدام المذكرة <small>Introduction &amp; Usage Guide</small></span></li>
        <li class="toc-item"><span class="toc-num">2</span><span class="toc-text">أوضاع الراوتر (Router Modes &amp; Navigation) <small>User/Privileged/Global/Interface Config</small></span></li>
        <li class="toc-item"><span class="toc-num">3</span><span class="toc-text">الإعداد الأساسي وإدارة النظام <small>Basic Setup &amp; System Management</small></span></li>
        <li class="toc-item"><span class="toc-num">4</span><span class="toc-text">كلمات المرور والأمان الأساسي <small>Passwords &amp; Basic Security</small></span></li>
        <li class="toc-item"><span class="toc-num">5</span><span class="toc-text">إعداد الواجهات وعناوين IP <small>Interfaces &amp; IP Addressing</small></span></li>
        <li class="toc-item"><span class="toc-num">6</span><span class="toc-text">أساسيات السويتش - VLANs &amp; Trunking <small>VLANs, DTP, Voice VLAN</small></span></li>
        <li class="toc-item"><span class="toc-num">7</span><span class="toc-text">VTP و EtherChannel <small>VTP Modes, LACP, PAgP</small></span></li>
        <li class="toc-item"><span class="toc-num">8</span><span class="toc-text">Spanning Tree Protocol <small>STP, RSTP, PVST+, BPDU Guard</small></span></li>
        <li class="toc-item"><span class="toc-num">9</span><span class="toc-text">Port Security <small>MAC Limit, Violation Modes</small></span></li>
        <li class="toc-item"><span class="toc-num">10</span><span class="toc-text">DHCP Server &amp; Relay <small>Pool, Helper-Address, DHCP Snooping</small></span></li>
        <li class="toc-item"><span class="toc-num">11</span><span class="toc-text">التوجيه الثابت <small>Static &amp; Default Routing</small></span></li>
        <li class="toc-item"><span class="toc-num">12</span><span class="toc-text">OSPF v2 &amp; v3 <small>Single &amp; Multi-Area</small></span></li>
        <li class="toc-item"><span class="toc-num">13</span><span class="toc-text">EIGRP v4 &amp; v6 <small>Classic &amp; Named Mode</small></span></li>
        <li class="toc-item"><span class="toc-num">14</span><span class="toc-text">FHRP - HSRP / VRRP / GLBP <small>First Hop Redundancy</small></span></li>
        <li class="toc-item"><span class="toc-num">15</span><span class="toc-text">Access Control Lists (ACLs) <small>Standard, Extended, IPv6</small></span></li>
        <li class="toc-item"><span class="toc-num">16</span><span class="toc-text">Network Address Translation <small>Static, Dynamic, PAT</small></span></li>
        <li class="toc-item"><span class="toc-num">17</span><span class="toc-text">BGP الأساسي <small>eBGP, iBGP, Attributes</small></span></li>
        <li class="toc-item"><span class="toc-num">18</span><span class="toc-text">إدارة الشبكة <small>SNMP, Syslog, NTP, SSH</small></span></li>
        <li class="toc-item"><span class="toc-num">19</span><span class="toc-text">Quality of Service (QoS) <small>Classification, Marking, Queuing</small></span></li>
        <li class="toc-item"><span class="toc-num">20</span><span class="toc-text">802.1x &amp; AAA Authentication <small>RADIUS, TACACS+</small></span></li>
        <li class="toc-item"><span class="toc-num">21</span><span class="toc-text">مرجع Subnetting و VLSM <small>CIDR Table, VLSM Examples</small></span></li>
        <li class="toc-item"><span class="toc-num">22</span><span class="toc-text">IPv6 - القسم التفصيلي المستقل <small>Addressing, ND, DHCPv6, ACLs</small></span></li>
        <li class="toc-item"><span class="toc-num">23</span><span class="toc-text">Troubleshooting &amp; Show Commands <small>Master Reference</small></span></li>
        <li class="toc-item"><span class="toc-num">24</span><span class="toc-text">Lab Scenarios - سيناريوهات عملية <small>Step-by-Step Topologies</small></span></li>
        <li class="toc-item"><span class="toc-num">25</span><span class="toc-text">Cheat Sheet - صفحة المرجع السريع <small>Quick Reference Card</small></span></li>
        <li class="toc-item"><span class="toc-num">26</span><span class="toc-text">أسئلة الممارسة مع الإجابات <small>Practice Questions</small></span></li>
        <li class="toc-item"><span class="toc-num">27</span><span class="toc-text">نصائح الامتحان والأخطاء الشائعة <small>Exam Tips &amp; Common Mistakes</small></span></li>
    </ul>
    <div style="margin-top: 30px; padding: 14px; background: #F8FBFC; border-right: 4px solid var(--c-cisco-blue); border-radius: 4px;">
        <strong style="color: var(--c-cisco-dark);">ملاحظة:</strong>
        <span style="font-size: 10pt; line-height: 1.6;">جميع الأوامر والأكواد في هذه المذكرة مكتوبة باللغة الإنجليزية كما هي في واجهة Cisco IOS الأصلية، بينما الشرح والملاحظات باللغة العربية. استخدم جدول المحتويات أعلاه للتنقل السريع بين المواضيع.</span>
    </div>
</div>
"""
