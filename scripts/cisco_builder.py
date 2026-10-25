# -*- coding: utf-8 -*-
"""
Cisco IOS Commands Reference - Main Builder
Generates the complete HTML file by combining all parts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cisco_html_parts.part_00_header import HEAD, COVER, TOC
from cisco_html_parts.part_01_intro_modes import SECTIONS_01
from cisco_html_parts.part_02_setup_security import SECTIONS_02
from cisco_html_parts.part_03_interfaces_vlans import SECTIONS_03
from cisco_html_parts.part_04_stp_security_dhcp import SECTIONS_04
from cisco_html_parts.part_05_routing import SECTIONS_05
from cisco_html_parts.part_06_ospf_eigrp import SECTIONS_06
from cisco_html_parts.part_07_fhrp_acl_nat import SECTIONS_07
from cisco_html_parts.part_08_bgp_mgmt_qos import SECTIONS_08
from cisco_html_parts.part_09_subnetting_ipv6 import SECTIONS_09
from cisco_html_parts.part_10_troubleshoot_lab import SECTIONS_10
from cisco_html_parts.part_11_cheatsheet_practice_tips import SECTIONS_11

def build_html():
    parts = [
        HEAD,
        COVER,
        TOC,
        '<div class="main-content">',
        SECTIONS_01,
        SECTIONS_02,
        SECTIONS_03,
        SECTIONS_04,
        SECTIONS_05,
        SECTIONS_06,
        SECTIONS_07,
        SECTIONS_08,
        SECTIONS_09,
        SECTIONS_10,
        SECTIONS_11,
        '</div>',
        '</body></html>',
    ]
    return '\n'.join(parts)

if __name__ == "__main__":
    html = build_html()
    out_path = "/home/z/my-project/scripts/cisco_reference.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML written to: {out_path}")
    print(f"Total size: {len(html):,} chars, {len(html.splitlines()):,} lines")
