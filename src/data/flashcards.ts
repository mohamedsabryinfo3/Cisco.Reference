// Cisco Flashcards - Quick study cards for rapid revision
export interface Flashcard {
  id: string;
  category: 'fundamentals' | 'routing' | 'switching' | 'security' | 'services' | 'advanced';
  front: string;
  back: string;
  example?: string;
}

export const FLASHCARDS: Flashcard[] = [
  // Fundamentals
  { id: 'fc-1', category: 'fundamentals', front: 'OSI Layers (7 layers)?', back: 'L1 Physical, L2 Data Link, L3 Network, L4 Transport, L5 Session, L6 Presentation, L7 Application', example: 'L4 = TCP/UDP, L3 = IP, L2 = MAC' },
  { id: 'fc-2', category: 'fundamentals', front: 'TCP 3-Way Handshake?', back: 'SYN → SYN-ACK → ACK. Establishes TCP connection before data transfer.' },
  { id: 'fc-3', category: 'fundamentals', front: 'TCP vs UDP?', back: 'TCP: reliable, connection-oriented (HTTP, SSH, FTP). UDP: fast, connectionless (DNS, DHCP, VoIP).' },
  { id: 'fc-4', category: 'fundamentals', front: 'ARP Function?', back: 'Resolves IPv4 → MAC address on local subnet. ARP cache stores entries.' },
  { id: 'fc-5', category: 'fundamentals', front: 'Broadcast vs Collision Domain?', back: 'Broadcast: separated by routers. Collision: separated by switches (each port = 1 CD).' },
  { id: 'fc-6', category: 'fundamentals', front: 'RFC 1918 Private IPs?', back: '10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 - not routable on internet.' },
  { id: 'fc-7', category: 'fundamentals', front: 'Common TCP Ports?', back: 'SSH 22, Telnet 23, SMTP 25, HTTP 80, POP3 110, HTTPS 443, RDP 3389, BGP 179' },
  { id: 'fc-8', category: 'fundamentals', front: 'Common UDP Ports?', back: 'DNS 53, DHCP 67/68, TFTP 69, SNMP 161/162, NTP 123, RIP 520, Syslog 514' },
  { id: 'fc-9', category: 'fundamentals', front: 'MTU vs MSS?', back: 'MTU = max packet size (Ethernet 1500). MSS = TCP data size (MTU-40). VPN needs lower.' },

  // Routing
  { id: 'fc-10', category: 'routing', front: 'Administrative Distance order?', back: 'Direct(0) > Static-nh(1) > eBGP(20) > EIGRP-int(90) > OSPF(110) > RIP(120) > EIGRP-ext(170) > iBGP(200)' },
  { id: 'fc-11', category: 'routing', front: 'Longest Prefix Match?', back: 'Most specific route wins. /24 beats /16 beats /8 beats /0 (default).' },
  { id: 'fc-12', category: 'routing', front: 'Default Route syntax?', back: 'ip route 0.0.0.0 0.0.0.0 <next-hop> (IPv4) / ipv6 route ::/0 <next-hop> (IPv6)' },
  { id: 'fc-13', category: 'routing', front: 'Floating Static Route?', back: 'Static with high AD as backup. ip route ... <AD=200>. Activates when primary (OSPF AD=110) fails.' },
  { id: 'fc-14', category: 'routing', front: 'OSPF neighbor states?', back: 'Down → Init → Two-Way → ExStart → Exchange → Loading → Full' },
  { id: 'fc-15', category: 'routing', front: 'OSPF Wildcard vs Subnet Mask?', back: 'OSPF uses WILDCARD (inverse). /24 mask = 255.255.255.0, wildcard = 0.0.0.255' },
  { id: 'fc-16', category: 'routing', front: 'OSPF LSA Types?', back: 'T1 Router, T2 Network, T3 Summary, T4 ASBR Summary, T5 AS External, T7 NSSA External' },
  { id: 'fc-17', category: 'routing', front: 'OSPF Area 0?', back: 'Backbone. All other areas must connect to it. ABR sits between areas.' },
  { id: 'fc-18', category: 'routing', front: 'OSPF DR/BDR election?', back: 'Highest priority wins (default 1, 0=never DR). Tie-breaker: highest router-id.' },
  { id: 'fc-19', category: 'routing', front: 'EIGRP DUAL terms?', back: 'FD=distance to dest. RD=neighbor to dest. FC=RD<FD. Successor=primary. FS=backup.' },
  { id: 'fc-20', category: 'routing', front: 'EIGRP no auto-summary?', back: 'Required to disable classful summarization. Default in IOS 15+. Prevents routing errors.' },
  { id: 'fc-21', category: 'routing', front: 'EIGRP variance?', back: 'Unequal Cost Load Balancing. variance 2 = use paths up to 2× metric. Unique EIGRP feature.' },
  { id: 'fc-22', category: 'routing', front: 'BGP Path Selection?', back: 'Weight > Local-Pref > locally originated > AS-Path length > Origin > MED > eBGP>iBGP > oldest > RID' },
  { id: 'fc-23', category: 'routing', front: 'BGP eBGP vs iBGP?', back: 'eBGP=between ASes (AD=20, TTL=1). iBGP=within AS (AD=200, TTL=255). iBGP needs full-mesh or RR.' },
  { id: 'fc-24', category: 'routing', front: 'BGP next-hop-self?', back: 'Required in iBGP. next-hop doesn\'t change by default. neighbor <ip> next-hop-self.' },
  { id: 'fc-25', category: 'routing', front: 'BGP Communities?', back: 'no-export (don\'t leave AS), no-advertise (don\'t advertise), local-AS, internet.' },

  // Switching
  { id: 'fc-26', category: 'switching', front: 'VLAN definition?', back: 'Logical segmentation of switch. Each VLAN = separate broadcast domain. Requires router for inter-VLAN.' },
  { id: 'fc-27', category: 'switching', front: 'Access vs Trunk port?', back: 'Access=1 VLAN, no tag. Trunk=multiple VLANs, 802.1Q tags (except Native VLAN).' },
  { id: 'fc-28', category: 'switching', front: 'Native VLAN?', back: 'VLAN that sends untagged frames on trunk. Default VLAN 1 (INSECURE). Use VLAN 999 unused.' },
  { id: 'fc-29', category: 'switching', front: 'DTP modes?', back: 'access, trunk, dynamic desirable (PAgP), dynamic auto (PAgP), nonegotiate (safest).' },
  { id: 'fc-30', category: 'switching', front: 'STP purpose?', back: 'Prevent L2 loops. Elects Root Bridge, blocks redundant ports. IEEE 802.1D.' },
  { id: 'fc-31', category: 'switching', front: 'STP timers?', back: 'Hello 2s, Max Age 20s, Forward Delay 15s. Total convergence 30-50s. RSTP: 1-3s.' },
  { id: 'fc-32', category: 'switching', front: 'Bridge ID = ?', back: 'Priority (2 bytes) + MAC (6 bytes). Default priority 32768. Lowest wins Root election.' },
  { id: 'fc-33', category: 'switching', front: 'PortFast purpose?', back: 'Skip Listening/Learning. Forwarding immediately. ONLY on access ports, NEVER on trunks.' },
  { id: 'fc-34', category: 'switching', front: 'BPDU Guard?', back: 'errdisable access port if BPDU received. Prevents rogue switch. Use with PortFast.' },
  { id: 'fc-35', category: 'switching', front: 'VLAN Hopping attack?', back: 'Double-tagged 802.1Q frames. Prevent: change Native VLAN, disable DTP, explicit access mode.' },
  { id: 'fc-36', category: 'switching', front: 'EtherChannel protocols?', back: 'PAgP (Cisco, desirable/auto), LACP (IEEE 802.3ad, active/passive), On (manual). Max 8 active.' },
  { id: 'fc-37', category: 'switching', front: 'VTP modes?', back: 'Server (create/forward), Client (forward only), Transparent (local only), Off (no VTP).' },
  { id: 'fc-38', category: 'switching', front: 'VTP danger?', back: 'Switch with higher revision can wipe all VLANs! Use transparent mode for safety.' },
  { id: 'fc-39', category: 'switching', front: 'Port Security violation modes?', back: 'protect (silent drop), restrict (drop+log), shutdown (errdisable, default).' },
  { id: 'fc-40', category: 'switching', front: 'DHCP Snooping?', back: 'Trust DHCP server ports, untrust user ports. Builds binding table for DAI/IPSG.' },
  { id: 'fc-41', category: 'switching', front: 'Dynamic ARP Inspection?', back: 'Validates ARP against DHCP snooping table. Prevents ARP spoofing (MITM).' },
  { id: 'fc-42', category: 'switching', front: 'IP Source Guard?', back: 'Checks source IP+MAC against DHCP snooping table. Prevents IP spoofing.' },

  // Security
  { id: 'fc-43', category: 'security', front: 'SSH vs Telnet?', back: 'SSH=encrypted (TCP 22). Telnet=plaintext (TCP 23). Always use SSH v2.' },
  { id: 'fc-44', category: 'security', front: 'Password Types?', back: '0=plain, 5=MD5, 7=Vigenère(weak), 8=PBKDF2-SHA256, 9=Scrypt(strongest). Use Type 9.' },
  { id: 'fc-45', category: 'security', front: 'enable secret vs enable password?', back: 'enable secret=encrypted (Type 5+). enable password=plaintext. ALWAYS use secret.' },
  { id: 'fc-46', category: 'security', front: 'AAA = ?', back: 'Authentication (who) + Authorization (what can do) + Accounting (what did).' },
  { id: 'fc-47', category: 'security', front: 'RADIUS vs TACACS+?', back: 'RADIUS=IETF/UDP 1812/encrypt password only. TACACS+=Cisco/TCP 49/encrypt all.' },
  { id: 'fc-48', category: 'security', front: 'Standard ACL?', back: '1-99, 1300-1999. Checks source only. Place near destination.' },
  { id: 'fc-49', category: 'security', front: 'Extended ACL?', back: '100-199, 2000-2699. Checks src+dst+protocol+port. Place near source.' },
  { id: 'fc-50', category: 'security', front: 'Wildcard Mask formula?', back: '255.255.255.255 - subnet_mask. /24→0.0.0.255, /30→0.0.0.3, /32→0.0.0.0' },
  { id: 'fc-51', category: 'security', front: '802.1x components?', back: 'Supplicant (client) + Authenticator (switch) + Auth Server (RADIUS). Uses EAP.' },
  { id: 'fc-52', category: 'security', front: 'login block-for?', back: 'login block-for 60 attempts 3 within 30 = block 60s after 3 fails in 30s. Anti brute-force.' },

  // Services
  { id: 'fc-53', category: 'services', front: 'DHCP DORA?', back: 'Discover (client broadcast) → Offer (server) → Request (client) → ACK (server).' },
  { id: 'fc-54', category: 'services', front: 'DHCP Relay?', back: 'ip helper-address <dhcp-ip>. Forwards DHCP broadcast as unicast to remote server.' },
  { id: 'fc-55', category: 'services', front: 'NAT types?', back: 'Static (1-to-1), Dynamic (pool), PAT/Overload (many-to-1 with ports).' },
  { id: 'fc-56', category: 'services', front: 'PAT config?', back: 'ip nat inside source list <acl> interface <iface> overload' },
  { id: 'fc-57', category: 'services', front: 'NAT inside vs outside?', back: 'inside local=private IP before NAT. inside global=public IP after NAT.' },
  { id: 'fc-58', category: 'services', front: 'NTP stratum?', back: '1-16. Lower=more authoritative. Stratum 1=direct from atomic clock. Default client stratum=8.' },
  { id: 'fc-59', category: 'services', front: 'Syslog severity levels?', back: '0 Emergency, 1 Alert, 2 Critical, 3 Error, 4 Warning, 5 Notification, 6 Info, 7 Debug.' },
  { id: 'fc-60', category: 'services', front: 'SNMP versions?', back: 'v1 (old), v2c (community string, plaintext), v3 (auth+encrypt, recommended).' },
  { id: 'fc-61', category: 'services', front: 'HSRP config?', back: 'standby <group> ip <vip> + standby <group> priority 110 + standby <group> preempt' },
  { id: 'fc-62', category: 'services', front: 'HSRP virtual MAC?', back: 'v1: 0000.0c07.acXX (0-255). v2: 0000.0c9f.fXXX (0-4095). VRRP: 0000.5e00.01XX.' },
  { id: 'fc-63', category: 'services', front: 'VRRP vs HSRP?', back: 'VRRP=IETF open standard. HSRP=Cisco proprietary. VRRP=Master/Backup, default preempt ON.' },
  { id: 'fc-64', category: 'services', front: 'GLBP unique feature?', back: 'Load balancing with single virtual IP + multiple MAC forwarders. AVG+AVF architecture.' },

  // Advanced
  { id: 'fc-65', category: 'advanced', front: 'IPv6 address types?', back: 'Global (2000::/3), Link-Local (fe80::/10), ULA (fc00::/7), Multicast (ff00::/8), Loopback (::1).' },
  { id: 'fc-66', category: 'advanced', front: 'IPv6 EUI-64?', back: 'Insert FFFE in middle of MAC, flip 7th bit. MAC 001A.2B3C.4D5E → 021A:2BFF:FE3C:4D5E.' },
  { id: 'fc-67', category: 'advanced', front: 'IPv6 SLAAC vs DHCPv6?', back: 'SLAAC=stateless (host generates IP from RA). Stateful DHCPv6=server assigns. Stateless=SLAAC+DHCP for DNS.' },
  { id: 'fc-68', category: 'advanced', front: 'NDP purpose?', back: 'Replaces ARP in IPv6. Uses ICMPv6 133-137. RS/RA, NS/NA, DAD.' },
  { id: 'fc-69', category: 'advanced', front: 'IPv6 Multicast ff02::?', back: '::1 All Nodes, ::2 All Routers, ::5 OSPF, ::6 OSPF DR, ::a EIGRP.' },
  { id: 'fc-70', category: 'advanced', front: 'DSCP values?', back: 'CS0=0 (default), CS6=48 (routing), EF=46 (VoIP), AF11=10, AF31=26 (video).' },
  { id: 'fc-71', category: 'advanced', front: 'QoS Policing vs Shaping?', back: 'Policing=drop excess (strict, ISP-side). Shaping=queue excess (smooth, customer-side).' },
  { id: 'fc-72', category: 'advanced', front: 'QoS LLQ?', back: 'Low Latency Queueing. Strict priority for VoIP. priority <kbps>. Required for real-time.' },
  { id: 'fc-73', category: 'advanced', front: 'IPsec components?', back: 'IKE (key exchange) + AH (auth only) + ESP (encrypt+auth). Modes: Transport, Tunnel.' },
  { id: 'fc-74', category: 'advanced', front: 'GRE Tunnel?', back: 'Encapsulates IP-in-IP. Carries multicast (OSPF over internet). No encryption - pair with IPsec.' },
  { id: 'fc-75', category: 'advanced', front: 'VRF?', back: 'Multiple routing tables on one router. L3 isolation. Allows overlapping IPs. Used in MPLS VPNs.' },
  { id: 'fc-76', category: 'advanced', front: 'MPLS labels?', back: '4-byte label between L2/L3. PE pushes, P swaps, PE pops. Faster than IP lookup.' },
  { id: 'fc-77', category: 'advanced', front: 'SDN architecture?', back: 'Separates control plane (controller) from data plane (switches). OpenFlow/NETCONF. Cisco DNA Center.' },
  { id: 'fc-78', category: 'advanced', front: 'REST API?', back: 'HTTP-based: GET (read), POST (create), PUT (update), DELETE. Uses JSON.' },
  { id: 'fc-79', category: 'advanced', front: 'NETCONF vs RESTCONF?', back: 'NETCONF=XML/RPC over SSH 830. RESTCONF=HTTP/JSON. YANG=data modeling.' },
  { id: 'fc-80', category: 'advanced', front: 'CoPP?', back: 'Control Plane Policing. QoS policy to protect CPU from DoS attacks. control-plane + service-policy input.' },
];

export const FLASHCARD_CATEGORIES = {
  fundamentals: { label: 'الأساسيات', labelEn: 'Fundamentals', color: '#049fd9' },
  routing: { label: 'التوجيه', labelEn: 'Routing', color: '#002b5c' },
  switching: { label: 'السويتش', labelEn: 'Switching', color: '#00bceb' },
  security: { label: 'الأمان', labelEn: 'Security', color: '#e74c3c' },
  services: { label: 'الخدمات', labelEn: 'Services', color: '#27ae60' },
  advanced: { label: 'متقدم', labelEn: 'Advanced', color: '#8e44ad' },
};
