'use client';

import { useState, useMemo, useCallback } from 'react';
import {
  Calculator,
  Network,
  Split,
  Table as TableIcon,
  Wrench,
  BookOpen,
  Copy,
  Check,
  Info,
  Lightbulb,
  AlertTriangle,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  Binary,
  Hash,
  Globe,
  Eye,
  Layers,
  FileText,
  Search,
  CheckCircle2,
  Target,
  Zap,
  Terminal,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

// ============================================================
// IP Utilities
// ============================================================
function ipToInt(ip: string): number {
  const parts = ip.split('.').map(Number);
  if (parts.length !== 4 || parts.some(p => isNaN(p) || p < 0 || p > 255)) {
    throw new Error('Invalid IP');
  }
  return ((parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]) >>> 0;
}

function intToIp(int: number): string {
  return [
    (int >>> 24) & 0xff,
    (int >>> 16) & 0xff,
    (int >>> 8) & 0xff,
    int & 0xff,
  ].join('.');
}

function intToBinary(int: number): string {
  let bin = '';
  for (let i = 31; i >= 0; i--) {
    bin += ((int >>> i) & 1).toString();
    if (i % 8 === 0 && i !== 0) bin += '.';
  }
  return bin;
}

function maskFromPrefix(prefix: number): number {
  if (prefix === 0) return 0;
  return (0xffffffff << (32 - prefix)) >>> 0;
}

function getIpClass(firstOctet: number): string {
  if (firstOctet >= 1 && firstOctet <= 126) return 'A';
  if (firstOctet >= 128 && firstOctet <= 191) return 'B';
  if (firstOctet >= 192 && firstOctet <= 223) return 'C';
  if (firstOctet >= 224 && firstOctet <= 239) return 'D (Multicast)';
  if (firstOctet >= 240 && firstOctet <= 255) return 'E (Reserved)';
  return 'Unknown';
}

function getDefaultPrefix(ipClass: string): number {
  if (ipClass === 'A') return 8;
  if (ipClass === 'B') return 16;
  if (ipClass === 'C') return 24;
  return 0;
}

function isPrivateIp(ip: string): boolean {
  const parts = ip.split('.').map(Number);
  if (parts[0] === 10) return true;
  if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
  if (parts[0] === 192 && parts[1] === 168) return true;
  if (parts[0] === 127) return true;
  return false;
}

function getPrivateRange(ip: string): string {
  const parts = ip.split('.').map(Number);
  if (parts[0] === 10) return '10.0.0.0/8 (RFC 1918 Class A)';
  if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return '172.16.0.0/12 (RFC 1918 Class B)';
  if (parts[0] === 192 && parts[1] === 168) return '192.168.0.0/16 (RFC 1918 Class C)';
  if (parts[0] === 127) return '127.0.0.0/8 (Loopback)';
  if (parts[0] === 169 && parts[1] === 254) return '169.254.0.0/16 (APIPA Link-Local)';
  if (parts[0] === 100 && parts[1] >= 64 && parts[1] <= 127) return '100.64.0.0/10 (CGNAT RFC 6598)';
  return 'Public IP';
}

function parseInput(input: string): { ip: string; prefix: number } | null {
  const trimmed = input.trim();
  let m = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2})$/);
  if (m) {
    const prefix = parseInt(m[2]);
    if (prefix >= 0 && prefix <= 32) {
      try {
        ipToInt(m[1]);
        return { ip: m[1], prefix };
      } catch { return null; }
    }
  }
  m = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/);
  if (m) {
    try {
      ipToInt(m[1]);
      const maskInt = ipToInt(m[2]);
      let prefix = 0;
      let v = maskInt >>> 0;
      while (v & 0x80000000) {
        prefix++;
        v = (v << 1) >>> 0;
      }
      if (prefix >= 0 && prefix <= 32) {
        return { ip: m[1], prefix };
      }
    } catch { return null; }
  }
  return null;
}

interface SubnetInfo {
  ip: string;
  prefix: number;
  network: string;
  broadcast: string;
  subnetMask: string;
  wildcard: string;
  firstHost: string;
  lastHost: string;
  hostsCount: number;
  totalAddresses: number;
  ipClass: string;
  isPrivate: boolean;
  privateRange: string;
  ipBinary: string;
  networkBinary: string;
  maskBinary: string;
  broadcastBinary: string;
  borrowedBits: number;
  hostBits: number;
  defaultPrefix: number;
  blockSize: number;
  isHostIp: boolean;
  isValidHost: boolean;
}

function calculateSubnet(ip: string, prefix: number): SubnetInfo {
  const ipInt = ipToInt(ip);
  const maskInt = maskFromPrefix(prefix);
  const networkInt = (ipInt & maskInt) >>> 0;
  const broadcastInt = (networkInt | (~maskInt >>> 0)) >>> 0;
  const hostBits = 32 - prefix;
  const totalAddresses = hostBits === 0 ? 1 : Math.pow(2, hostBits);
  const hostsCount = totalAddresses >= 2 ? totalAddresses - 2 : 0;

  const firstOctet = (ipInt >>> 24) & 0xff;
  const ipClass = getIpClass(firstOctet);
  const defaultPrefix = getDefaultPrefix(ipClass);
  const isPrivate = isPrivateIp(ip);
  const privateRange = getPrivateRange(ip);
  const borrowedBits = Math.max(0, prefix - defaultPrefix);
  const isHostIp = ipInt !== networkInt && ipInt !== broadcastInt;

  return {
    ip,
    prefix,
    network: intToIp(networkInt),
    broadcast: intToIp(broadcastInt),
    subnetMask: intToIp(maskInt),
    wildcard: intToIp((~maskInt) >>> 0),
    firstHost: hostsCount >= 1 ? intToIp(networkInt + 1) : intToIp(networkInt),
    lastHost: hostsCount >= 1 ? intToIp(broadcastInt - 1) : intToIp(broadcastInt),
    hostsCount,
    totalAddresses,
    ipClass,
    isPrivate,
    privateRange,
    ipBinary: intToBinary(ipInt),
    networkBinary: intToBinary(networkInt),
    maskBinary: intToBinary(maskInt),
    broadcastBinary: intToBinary(broadcastInt),
    borrowedBits,
    hostBits,
    defaultPrefix,
    blockSize: totalAddresses,
    isHostIp,
    isValidHost: isHostIp && hostsCount >= 1,
  };
}

// ============================================================
// VLSM Calculator
// ============================================================
interface VLSMSubnet {
  name: string;
  requiredHosts: number;
  allocatedHosts: number;
  prefix: number;
  network: string;
  firstHost: string;
  lastHost: string;
  broadcast: string;
  subnetMask: string;
  wildcard: string;
  cidr: string;
  range: string;
  status: 'ok' | 'fail';
}

function calcVLSM(baseIp: string, basePrefix: number, requirements: { name: string; hosts: number }[]): VLSMSubnet[] {
  const sorted = [...requirements].sort((a, b) => b.hosts - a.hosts);
  let currentInt = ipToInt(baseIp);
  const baseMaskInt = maskFromPrefix(basePrefix);
  currentInt = (currentInt & baseMaskInt) >>> 0;
  const baseBroadcast = (currentInt | (~baseMaskInt >>> 0)) >>> 0;

  const result: VLSMSubnet[] = [];

  for (const req of sorted) {
    if (req.hosts <= 0) continue;
    let needed = req.hosts + 2;
    let hostBits = 1;
    while (Math.pow(2, hostBits) < needed) hostBits++;
    const prefix = 32 - hostBits;
    const blockSize = Math.pow(2, hostBits);
    const subnetMask = maskFromPrefix(prefix);

    const blockStart = Math.floor(currentInt / blockSize) * blockSize;
    const networkInt = blockStart >>> 0;
    const broadcastInt = (networkInt + blockSize - 1) >>> 0;

    if (broadcastInt > baseBroadcast) {
      result.push({
        name: req.name,
        requiredHosts: req.hosts,
        allocatedHosts: 0,
        prefix,
        network: 'INSUFFICIENT SPACE',
        firstHost: '-',
        lastHost: '-',
        broadcast: '-',
        subnetMask: intToIp(subnetMask),
        wildcard: intToIp((~subnetMask) >>> 0),
        cidr: `/${prefix}`,
        range: '-',
        status: 'fail',
      });
      continue;
    }

    result.push({
      name: req.name,
      requiredHosts: req.hosts,
      allocatedHosts: blockSize - 2,
      prefix,
      network: intToIp(networkInt),
      firstHost: intToIp(networkInt + 1),
      lastHost: intToIp(broadcastInt - 1),
      broadcast: intToIp(broadcastInt),
      subnetMask: intToIp(subnetMask),
      wildcard: intToIp((~subnetMask) >>> 0),
      cidr: `/${prefix}`,
      range: `${intToIp(networkInt + 1)} - ${intToIp(broadcastInt - 1)}`,
      status: 'ok',
    });

    currentInt = (broadcastInt + 1) >>> 0;
  }

  return result;
}

// ============================================================
// CIDR Reference Table
// ============================================================
const CIDR_TABLE = [
  { cidr: 31, mask: '255.255.255.254', wildcard: '0.0.0.1', hosts: 2, subnets24: 128, block: 2, use: 'Point-to-Point (RFC 3021)' },
  { cidr: 30, mask: '255.255.255.252', wildcard: '0.0.0.3', hosts: 2, subnets24: 64, block: 4, use: 'WAN Links' },
  { cidr: 29, mask: '255.255.255.248', wildcard: '0.0.0.7', hosts: 6, subnets24: 32, block: 8, use: 'Small subnets' },
  { cidr: 28, mask: '255.255.255.240', wildcard: '0.0.0.15', hosts: 14, subnets24: 16, block: 16, use: 'Small departments' },
  { cidr: 27, mask: '255.255.255.224', wildcard: '0.0.0.31', hosts: 30, subnets24: 8, block: 32, use: 'Medium subnets' },
  { cidr: 26, mask: '255.255.255.192', wildcard: '0.0.0.63', hosts: 62, subnets24: 4, block: 64, use: 'Large subnets' },
  { cidr: 25, mask: '255.255.255.128', wildcard: '0.0.0.127', hosts: 126, subnets24: 2, block: 128, use: 'Half Class C' },
  { cidr: 24, mask: '255.255.255.0', wildcard: '0.0.0.255', hosts: 254, subnets24: 1, block: 256, use: 'Class C default' },
  { cidr: 23, mask: '255.255.254.0', wildcard: '0.0.1.255', hosts: 510, subnets24: 0.5, block: 512, use: 'Supernet (2×C)' },
  { cidr: 22, mask: '255.255.252.0', wildcard: '0.0.3.255', hosts: 1022, subnets24: 0.25, block: 1024, use: 'Supernet (4×C)' },
  { cidr: 21, mask: '255.255.248.0', wildcard: '0.0.7.255', hosts: 2046, subnets24: 0.125, block: 2048, use: 'Supernet (8×C)' },
  { cidr: 20, mask: '255.255.240.0', wildcard: '0.0.15.255', hosts: 4094, subnets24: 0.0625, block: 4096, use: 'Supernet (16×C)' },
  { cidr: 19, mask: '255.255.224.0', wildcard: '0.0.31.255', hosts: 8190, subnets24: 0, block: 8192, use: 'Large enterprise' },
  { cidr: 18, mask: '255.255.192.0', wildcard: '0.0.63.255', hosts: 16382, subnets24: 0, block: 16384, use: 'ISP customer' },
  { cidr: 17, mask: '255.255.128.0', wildcard: '0.0.127.255', hosts: 32766, subnets24: 0, block: 32768, use: 'Half Class B' },
  { cidr: 16, mask: '255.0.0.0', wildcard: '0.255.255.255', hosts: 65534, subnets24: 0, block: 65536, use: 'Class B default' },
];

// ============================================================
// Main Component
// ============================================================
export function SubnetCalculator() {
  const [activeTab, setActiveTab] = useState<'analyzer' | 'divider' | 'vlsm' | 'tools' | 'reference'>('analyzer');
  return (
    <div className="space-y-5">
      {/* Tab navigation */}
      <div className="flex flex-wrap gap-2">
        <TabButton active={activeTab === 'analyzer'} onClick={() => setActiveTab('analyzer')} icon={<Network className="h-4 w-4" />} label="محلل الشبكة" labelEn="Analyzer" />
        <TabButton active={activeTab === 'divider'} onClick={() => setActiveTab('divider')} icon={<Split className="h-4 w-4" />} label="مقسم الشبكات" labelEn="Divider" />
        <TabButton active={activeTab === 'vlsm'} onClick={() => setActiveTab('vlsm')} icon={<Layers className="h-4 w-4" />} label="VLSM" labelEn="VLSM" />
        <TabButton active={activeTab === 'tools'} onClick={() => setActiveTab('tools')} icon={<Wrench className="h-4 w-4" />} label="أدوات" labelEn="Tools" />
        <TabButton active={activeTab === 'reference'} onClick={() => setActiveTab('reference')} icon={<BookOpen className="h-4 w-4" />} label="مرجع دراسي" labelEn="Reference" />
      </div>

      {activeTab === 'analyzer' && <IPAnalyzer />}
      {activeTab === 'divider' && <NetworkDivider />}
      {activeTab === 'vlsm' && <VLSMCalculator />}
      {activeTab === 'tools' && <ToolsView />}
      {activeTab === 'reference' && <StudyReference />}
    </div>
  );
}

function TabButton({ active, onClick, icon, label, labelEn }: { active: boolean; onClick: () => void; icon: React.ReactNode; label: string; labelEn: string }) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition',
        active
          ? 'bg-[#049fd9] text-white shadow-md'
          : 'bg-muted hover:bg-muted/70 text-foreground'
      )}
    >
      {icon}
      <span>{label}</span>
      <span className={cn('text-[10px] hidden sm:inline', active ? 'text-white/70' : 'text-muted-foreground')} dir="ltr">{labelEn}</span>
    </button>
  );
}

// ============================================================
// 1. IP Analyzer
// ============================================================
function IPAnalyzer() {
  const [input, setInput] = useState('192.168.1.130/26');
  const [copied, setCopied] = useState<string | null>(null);
  const [showSteps, setShowSteps] = useState(true);
  const [showBinary, setShowBinary] = useState(true);
  const [subnetFinderMode, setSubnetFinderMode] = useState(false);

  const parsed = useMemo(() => parseInput(input), [input]);
  const info = useMemo(() => parsed ? calculateSubnet(parsed.ip, parsed.prefix) : null, [parsed]);

  const examples = ['192.168.1.0/24', '10.0.0.5/8', '172.16.5.3/22', '192.168.10.5/26', '10.10.10.0/30'];

  const copy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 1500);
  };

  const copyAll = () => {
    if (!info) return;
    const text = `Subnet Analysis Report
=======================
Input: ${info.ip}/${info.prefix}
Class: ${info.ipClass}
${info.isPrivate ? `Private: ${info.privateRange}` : 'Public IP'}

Network Address:  ${info.network}
Subnet Mask:       ${info.subnetMask}
Wildcard (Cisco):  ${info.wildcard}
Broadcast Address: ${info.broadcast}

First Host IP: ${info.firstHost}
Last Host IP:  ${info.lastHost}

Valid Hosts:       ${info.hostsCount}
Total Addresses:   ${info.totalAddresses}
Block Size:        ${info.blockSize}

Borrowed Bits: ${info.borrowedBits}
Host Bits:     ${info.hostBits}

Cisco Commands:
  interface <iface>
  ip address ${info.firstHost} ${info.subnetMask}
  no shutdown
  
  network ${info.network} ${info.wildcard} area 0   (OSPF)
  access-list 10 permit ${info.network} ${info.wildcard}   (ACL)`;
    navigator.clipboard.writeText(text);
    setCopied('all');
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="space-y-5">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between gap-2 text-lg flex-wrap">
            <span className="flex items-center gap-2">
              <Network className="h-5 w-5 text-[#049fd9]" />
              محلل عنوان IP - IP Analyzer
            </span>
            {info && (
              <Button size="sm" variant="default" onClick={copyAll} className="text-xs">
                {copied === 'all' ? <Check className="h-3 w-3 ml-1" /> : <Copy className="h-3 w-3 ml-1" />}
                {copied === 'all' ? 'تم النسخ' : 'نسخ الكل'}
              </Button>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-semibold mb-2 block">أدخل عنوان IP</label>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="192.168.1.130/26 أو 10.0.0.5 255.0.0.0"
              className="font-mono text-base h-11"
              dir="ltr"
            />
            <p className="text-xs text-muted-foreground mt-2">
              صيغ مدعومة: <code className="font-mono bg-muted px-1 rounded" dir="ltr">192.168.1.0/24</code> —
              <code className="font-mono bg-muted px-1 rounded mx-1" dir="ltr">10.0.0.5 255.0.0.0</code> —
              <code className="font-mono bg-muted px-1 rounded mx-1" dir="ltr">172.16.5.3/22</code>
            </p>
          </div>

          {/* Examples */}
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-muted-foreground">أمثلة:</span>
            {examples.map(ex => (
              <button
                key={ex}
                onClick={() => setInput(ex)}
                className="text-[11px] font-mono px-2 py-0.5 rounded bg-muted hover:bg-[#049fd9]/10 hover:text-[#049fd9] transition"
                dir="ltr"
              >
                {ex}
              </button>
            ))}
          </div>

          {/* Options */}
          <div className="flex flex-wrap gap-3">
            <label className="flex items-center gap-2 cursor-pointer text-sm">
              <input
                type="checkbox"
                checked={showSteps}
                onChange={(e) => setShowSteps(e.target.checked)}
                className="w-4 h-4"
              />
              <Lightbulb className="h-4 w-4 text-amber-500" />
              الحل خطوة بخطوة
            </label>
            <label className="flex items-center gap-2 cursor-pointer text-sm">
              <input
                type="checkbox"
                checked={subnetFinderMode}
                onChange={(e) => setSubnetFinderMode(e.target.checked)}
                className="w-4 h-4"
              />
              <Search className="h-4 w-4 text-cyan-500" />
              subnet finder (ابحث عن الشبكة المناسبة)
            </label>
          </div>

          {!info && input && (
            <div className="p-3 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 text-sm flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 shrink-0" />
              صيغة غير صحيحة. استخدم: 192.168.1.0/24 أو 10.0.0.5 255.0.0.0
            </div>
          )}

          {info && (
            <>
              {/* Status badges */}
              <div className="flex flex-wrap gap-2">
                <Badge variant={info.isPrivate ? 'default' : 'outline'} className="text-xs">
                  {info.isPrivate ? '🔒 شبكة خاصة' : '🌐 عنوان عام'}
                </Badge>
                <Badge variant="outline" className="text-xs gap-1">
                  Class {info.ipClass}
                </Badge>
                {info.isHostIp && (
                  <Badge variant="outline" className="text-xs bg-green-50 dark:bg-green-950/20 text-green-700 dark:text-green-300">
                    <CheckCircle2 className="h-3 w-3" />
                    عنوان مضيف صالح
                  </Badge>
                )}
                {!info.isHostIp && info.ip === info.network && (
                  <Badge variant="outline" className="text-xs bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300">
                    عنوان شبكة (وليس مضيف)
                  </Badge>
                )}
                {!info.isHostIp && info.ip === info.broadcast && (
                  <Badge variant="outline" className="text-xs bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300">
                    عنوان بث (Broadcast)
                  </Badge>
                )}
                {info.isPrivate && (
                  <Badge variant="outline" className="text-xs">
                    {info.privateRange}
                  </Badge>
                )}
              </div>

              {/* Main info grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                <InfoCard label="عنوان الشبكة" en="Network Address" value={info.network} onCopy={() => copy(info.network, 'network')} copied={copied === 'network'} color="text-blue-600 dark:text-blue-400" />
                <InfoCard label="قناع الشبكة" en="Subnet Mask" value={info.subnetMask} onCopy={() => copy(info.subnetMask, 'mask')} copied={copied === 'mask'} color="text-purple-600 dark:text-purple-400" />
                <InfoCard label="Wildcard (Cisco)" en="Wildcard Mask" value={info.wildcard} onCopy={() => copy(info.wildcard, 'wc')} copied={copied === 'wc'} color="text-amber-600 dark:text-amber-400" />
                <InfoCard label="عنوان البث" en="Broadcast Address" value={info.broadcast} onCopy={() => copy(info.broadcast, 'bc')} copied={copied === 'bc'} color="text-red-600 dark:text-red-400" />
                <InfoCard label="أول IP مضيف" en="First Host" value={info.firstHost} onCopy={() => copy(info.firstHost, 'fh')} copied={copied === 'fh'} color="text-green-600 dark:text-green-400" />
                <InfoCard label="آخر IP مضيف" en="Last Host" value={info.lastHost} onCopy={() => copy(info.lastHost, 'lh')} copied={copied === 'lh'} color="text-green-600 dark:text-green-400" />
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <StatBox label="عدد المضيفين الصالحين" en="Valid Hosts" value={info.hostsCount.toLocaleString()} icon={<Hash className="h-4 w-4" />} />
                <StatBox label="إجمالي العناوين" en="Total Addresses" value={info.totalAddresses.toLocaleString()} icon={<Globe className="h-4 w-4" />} />
                <StatBox label="Block Size" en="Block Size" value={info.blockSize.toString()} icon={<Binary className="h-4 w-4" />} />
                <StatBox label="Bits" en="Borrowed/Host" value={`${info.borrowedBits}/${info.hostBits}`} icon={<Binary className="h-4 w-4" />} />
              </div>

              {/* Toggle for binary */}
              <label className="flex items-center gap-2 cursor-pointer text-sm">
                <input
                  type="checkbox"
                  checked={showBinary}
                  onChange={(e) => setShowBinary(e.target.checked)}
                  className="w-4 h-4"
                />
                <Eye className="h-4 w-4 text-[#049fd9]" />
                التمثيل البصري للبتات (32-bit)
              </label>

              {/* Binary visualization */}
              {showBinary && (
                <div>
                  <h4 className="text-sm font-bold mb-3 flex items-center gap-2">
                    <Binary className="h-4 w-4 text-[#049fd9]" />
                    التمثيل البصري للبتات (32-bit)
                  </h4>
                  <div className="space-y-3 bg-muted/30 p-4 rounded-lg border border-border">
                    <BinaryRow label="IP" binary={info.ipBinary} prefix={info.prefix} type="ip" />
                    <BinaryRow label="Mask" binary={info.maskBinary} prefix={info.prefix} type="mask" />
                    <BinaryRow label="Network" binary={info.networkBinary} prefix={info.prefix} type="network" />
                    <BinaryRow label="Broadcast" binary={info.broadcastBinary} prefix={info.prefix} type="broadcast" />
                  </div>
                  <div className="flex flex-wrap gap-3 mt-3 text-xs">
                    <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-blue-500"></span> جزء الشبكة الأصلي</span>
                    <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-orange-500"></span> البتات المستعارة</span>
                    <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-gray-400"></span> جزء المضيف</span>
                  </div>
                </div>
              )}

              {/* Address Range Visualization */}
              <div className="bg-gradient-to-br from-[#049fd9]/5 to-transparent border border-[#049fd9]/30 rounded-lg p-4">
                <h4 className="text-sm font-bold mb-3 flex items-center gap-2 text-[#049fd9]">
                  <Target className="h-4 w-4" />
                  تصور نطاق العناوين
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                  <div className="text-center p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                    <div className="text-xs text-muted-foreground">Network</div>
                    <code className="font-mono text-blue-600 dark:text-blue-400 text-base" dir="ltr">{info.network}</code>
                  </div>
                  <div className="text-center p-3 bg-green-50 dark:bg-green-950/20 rounded-lg">
                    <div className="text-xs text-muted-foreground">النطاق الصالح للاستخدام</div>
                    <code className="font-mono text-green-600 dark:text-green-400 text-sm" dir="ltr">{info.firstHost}</code>
                    <div className="text-[10px] my-0.5">—</div>
                    <code className="font-mono text-green-600 dark:text-green-400 text-sm" dir="ltr">{info.lastHost}</code>
                    <div className="text-xs text-muted-foreground mt-1">{info.hostsCount} عنوان</div>
                  </div>
                  <div className="text-center p-3 bg-red-50 dark:bg-red-950/20 rounded-lg">
                    <div className="text-xs text-muted-foreground">Broadcast</div>
                    <code className="font-mono text-red-600 dark:text-red-400 text-base" dir="ltr">{info.broadcast}</code>
                  </div>
                </div>
              </div>

              {/* Cisco syntax */}
              <Card className="bg-[#002b5c]/5 dark:bg-[#049fd9]/5 border-[#049fd9]/30">
                <CardContent className="p-4">
                  <h4 className="text-sm font-bold mb-2 flex items-center gap-2 text-[#049fd9]">
                    <Terminal className="h-4 w-4" />
                    أوامر Cisco الجاهزة
                  </h4>
                  <div className="space-y-2">
                    <CiscoCmd cmd={`interface <iface>`} comment="L3 Interface" />
                    <CiscoCmd cmd={`ip address ${info.firstHost} ${info.subnetMask}`} comment="Assign IP" />
                    <CiscoCmd cmd={`no shutdown`} comment="Enable" />
                    {info.prefix < 31 && <CiscoCmd cmd={`ip route ${info.network} ${info.subnetMask} <next-hop>`} comment="Static Route" />}
                    <CiscoCmd cmd={`network ${info.network} ${info.wildcard} area 0`} comment="OSPF" />
                    <CiscoCmd cmd={`access-list 10 permit ${info.network} ${info.wildcard}`} comment="ACL" />
                    <CiscoCmd cmd={`ip nat inside source list 10 interface <iface> overload`} comment="NAT PAT" />
                    <CiscoCmd cmd={`ip dhcp excluded-address ${info.network} ${info.firstHost}`} comment="DHCP Exclude" />
                  </div>
                </CardContent>
              </Card>

              {/* Step-by-step */}
              {showSteps && (
                <Card className="bg-amber-50/50 dark:bg-amber-950/10 border-amber-300/50">
                  <CardContent className="p-4">
                    <h4 className="text-sm font-bold mb-3 flex items-center gap-2 text-amber-700 dark:text-amber-400">
                      <Lightbulb className="h-4 w-4" />
                      الحل خطوة بخطوة
                    </h4>
                    <ol className="space-y-2 text-sm">
                      <li><strong>1.</strong> الـ prefix هو /{info.prefix} = أول {info.prefix} bits هي network والباقي {info.hostBits} bits هي host.</li>
                      <li><strong>2.</strong> Block size = 2^{info.hostBits} = {info.totalAddresses} عنوان إجمالاً.</li>
                      <li><strong>3.</strong> Network = IP AND Mask = <code className="font-mono px-1 bg-muted rounded" dir="ltr">{info.network}</code></li>
                      <li><strong>4.</strong> Broadcast = Network + (Block - 1) = <code className="font-mono px-1 bg-muted rounded" dir="ltr">{info.broadcast}</code></li>
                      <li><strong>5.</strong> الـ hosts الصالحة: من <code className="font-mono px-1 bg-muted rounded" dir="ltr">{info.firstHost}</code> إلى <code className="font-mono px-1 bg-muted rounded" dir="ltr">{info.lastHost}</code> = {info.hostsCount} مضيف.</li>
                      <li><strong>6.</strong> Wildcard = NOT(Mask) = <code className="font-mono px-1 bg-muted rounded" dir="ltr">{info.wildcard}</code> (يستعمل في OSPF و ACL).</li>
                      <li><strong>7.</strong> Borrowed bits = {info.prefix} - {info.defaultPrefix} (default class {info.ipClass}) = {info.borrowedBits} bits.</li>
                      <li><strong>8.</strong> Wildcard Mask تستعمل لـ: OSPF network command، ACL، BGP network command.</li>
                    </ol>
                  </CardContent>
                </Card>
              )}

              {/* Subnet Finder Mode */}
              {subnetFinderMode && (
                <SubnetFinder baseIp={info.network} basePrefix={info.prefix} maxHosts={info.hostsCount} onUseResult={(ip, prefix) => setInput(`${ip}/${prefix}`)} />
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function CiscoCmd({ cmd, comment }: { cmd: string; comment?: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="flex items-center gap-2 bg-muted/50 rounded px-2 py-1.5">
      {comment && <Badge variant="outline" className="text-[9px] shrink-0">{comment}</Badge>}
      <code className="font-mono text-xs flex-1 text-[#b1272b] dark:text-[#ff6b6b]" dir="ltr">{cmd}</code>
      <button
        onClick={() => { navigator.clipboard.writeText(cmd); setCopied(true); setTimeout(() => setCopied(false), 1500); }}
        className="text-muted-foreground hover:text-[#049fd9] shrink-0"
      >
        {copied ? <Check className="h-3 w-3 text-green-500" /> : <Copy className="h-3 w-3" />}
      </button>
    </div>
  );
}

function InfoCard({ label, en, value, onCopy, copied, color }: { label: string; en: string; value: string; onCopy: () => void; copied: boolean; color: string }) {
  return (
    <div className="bg-card border border-border rounded-lg p-3 hover:shadow-sm transition">
      <div className="text-xs text-muted-foreground mb-1">{label}</div>
      <div className="text-[10px] text-muted-foreground/70 mb-2" dir="ltr">{en}</div>
      <div className="flex items-center justify-between gap-2">
        <code className={cn('font-mono text-base font-bold', color)} dir="ltr">{value}</code>
        <button onClick={onCopy} className="text-muted-foreground hover:text-[#049fd9] transition">
          {copied ? <Check className="h-3.5 w-3.5 text-green-500" /> : <Copy className="h-3.5 w-3.5" />}
        </button>
      </div>
    </div>
  );
}

function StatBox({ label, en, value, icon }: { label: string; en: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-muted/30 rounded-lg p-3 text-center">
      <div className="flex items-center justify-center gap-1.5 text-muted-foreground mb-1">{icon}<span className="text-[10px]">{label}</span></div>
      <div className="text-xl font-black text-foreground" dir="ltr">{value}</div>
      <div className="text-[9px] text-muted-foreground/70" dir="ltr">{en}</div>
    </div>
  );
}

function BinaryRow({ label, binary, prefix, type }: { label: string; binary: string; prefix: number; type: 'ip' | 'mask' | 'network' | 'broadcast' }) {
  const bitsArray = binary.replace(/\./g, '').split('');
  return (
    <div className="flex items-center gap-3 flex-wrap">
      <span className="text-xs font-mono font-bold w-20 shrink-0" dir="ltr">{label}:</span>
      <div className="flex flex-wrap gap-0.5 flex-1 min-w-0" dir="ltr">
        {bitsArray.map((bit, i) => {
          let color = 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200';
          if (type === 'mask') {
            color = i < prefix ? 'bg-blue-500 text-white' : 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200';
          } else if (type === 'ip') {
            if (i < prefix) color = 'bg-blue-500 text-white';
            else color = 'bg-orange-400 text-white';
          } else if (type === 'network') {
            if (i < prefix) color = 'bg-blue-600 text-white';
            else color = 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200';
          } else if (type === 'broadcast') {
            if (i < prefix) color = 'bg-blue-500 text-white';
            else color = 'bg-red-500 text-white';
          }
          return (
            <span key={i} className={cn('inline-flex items-center justify-center w-5 h-6 rounded text-xs font-mono font-bold', color)}>
              {bit}
            </span>
          );
        })}
      </div>
      <span className="text-xs font-mono text-muted-foreground hidden sm:inline" dir="ltr">{binary}</span>
    </div>
  );
}

// ============================================================
// Subnet Finder (within Analyzer)
// ============================================================
function SubnetFinder({ baseIp, basePrefix, maxHosts, onUseResult }: { baseIp: string; basePrefix: number; maxHosts: number; onUseResult: (ip: string, prefix: number) => void }) {
  const [neededHosts, setNeededHosts] = useState('');
  const [neededSubnets, setNeededSubnets] = useState('');

  const result = useMemo(() => {
    const hosts = parseInt(neededHosts);
    const subnets = parseInt(neededSubnets);
    const results: { type: string; value: string; prefix?: number; valid: boolean }[] = [];

    if (hosts > 0) {
      let hb = 1;
      while (Math.pow(2, hb) < hosts + 2) hb++;
      const prefix = 32 - hb;
      const allocHosts = Math.pow(2, hb) - 2;
      results.push({
        type: 'لعدد المضيفين',
        value: `/${prefix} (يتسع لـ ${allocHosts} مضيف)`,
        prefix,
        valid: allocHosts >= hosts,
      });
    }
    if (subnets > 0) {
      let bb = 1;
      while (Math.pow(2, bb) < subnets) bb++;
      const newPrefix = basePrefix + bb;
      const subnetsCount = Math.pow(2, bb);
      const hostsPerSubnet = Math.pow(2, 32 - newPrefix) - 2;
      results.push({
        type: 'لعدد الشبكات',
        value: `/${newPrefix} (${subnetsCount} شبكة × ${hostsPerSubnet} مضيف)`,
        prefix: newPrefix,
        valid: newPrefix <= 30,
      });
    }
    return results;
  }, [neededHosts, neededSubnets, basePrefix]);

  return (
    <Card className="bg-cyan-50/50 dark:bg-cyan-950/10 border-cyan-300/50">
      <CardContent className="p-4 space-y-3">
        <h4 className="text-sm font-bold flex items-center gap-2 text-cyan-700 dark:text-cyan-400">
          <Search className="h-4 w-4" />
          Subnet Finder - ابحث عن الـ prefix المناسب
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-muted-foreground block mb-1">عدد المضيفين المطلوب:</label>
            <Input
              type="number"
              value={neededHosts}
              onChange={(e) => setNeededHosts(e.target.value)}
              placeholder="مثال: 60"
              className="font-mono"
              dir="ltr"
            />
          </div>
          <div>
            <label className="text-xs text-muted-foreground block mb-1">عدد الشبكات المطلوب:</label>
            <Input
              type="number"
              value={neededSubnets}
              onChange={(e) => setNeededSubnets(e.target.value)}
              placeholder="مثال: 8"
              className="font-mono"
              dir="ltr"
            />
          </div>
        </div>
        {result.length > 0 && (
          <div className="space-y-2">
            {result.map((r, i) => (
              <div key={i} className="flex items-center justify-between bg-muted/50 rounded p-2">
                <div>
                  <span className="text-xs text-muted-foreground">{r.type}: </span>
                  <code className="font-mono text-sm font-bold text-[#049fd9]" dir="ltr">{r.value}</code>
                </div>
                {r.prefix !== undefined && r.valid && (
                  <Button size="sm" variant="outline" onClick={() => onUseResult(baseIp, r.prefix!)} className="text-xs">
                    استخدم {r.prefix}
                  </Button>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// 2. Network Divider (FLSM - Fixed Length)
// ============================================================
function NetworkDivider() {
  const [baseInput, setBaseInput] = useState('192.168.1.0/24');
  const [newPrefix, setNewPrefix] = useState('26');
  const [copied, setCopied] = useState<string | null>(null);

  const parsed = useMemo(() => parseInput(baseInput), [baseInput]);
  const result = useMemo(() => {
    if (!parsed) return null;
    const newP = parseInt(newPrefix);
    if (isNaN(newP) || newP < parsed.prefix || newP > 32) return null;
    const borrowedBits = newP - parsed.prefix;
    const numSubnets = Math.pow(2, borrowedBits);
    const hostsPerSubnet = Math.pow(2, 32 - newP) - 2;
    const blockSize = Math.pow(2, 32 - newP);
    const baseInt = ipToInt(parsed.ip);
    const maskInt = maskFromPrefix(parsed.prefix);
    const networkInt = (baseInt & maskInt) >>> 0;

    const subnets = Array.from({ length: numSubnets }, (_, i) => {
      const subnetInt = networkInt + i * blockSize;
      const broadcastInt = subnetInt + blockSize - 1;
      return {
        index: i + 1,
        network: intToIp(subnetInt >>> 0),
        firstHost: intToIp((subnetInt + 1) >>> 0),
        lastHost: intToIp((broadcastInt - 1) >>> 0),
        broadcast: intToIp(broadcastInt >>> 0),
      };
    });

    return { numSubnets, hostsPerSubnet, blockSize, borrowedBits, newPrefix: newP, subnets };
  }, [parsed, newPrefix]);

  const copyAll = () => {
    if (!result) return;
    const text = `FLSM Network Division Report
============================
Base: ${parsed!.ip}/${parsed!.prefix}
New Prefix: /${result.newPrefix}
Subnets: ${result.numSubnets}
Hosts per subnet: ${result.hostsPerSubnet}
Borrowed bits: ${result.borrowedBits}

Subnets:
${result.subnets.map(s => `Subnet ${s.index}: ${s.network} - ${s.broadcast} (hosts: ${s.firstHost}-${s.lastHost})`).join('\n')}`;
    navigator.clipboard.writeText(text);
    setCopied('all');
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between gap-2 text-lg flex-wrap">
          <span className="flex items-center gap-2">
            <Split className="h-5 w-5 text-[#049fd9]" />
            مقسم الشبكات - FLSM Fixed Length
          </span>
          {result && (
            <Button size="sm" onClick={copyAll} className="text-xs">
              {copied === 'all' ? <Check className="h-3 w-3 ml-1" /> : <Copy className="h-3 w-3 ml-1" />}
              {copied === 'all' ? 'تم النسخ' : 'نسخ الكل'}
            </Button>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="text-sm font-semibold mb-2 block">الشبكة الأساسية:</label>
            <Input
              value={baseInput}
              onChange={(e) => setBaseInput(e.target.value)}
              placeholder="192.168.1.0/24"
              className="font-mono"
              dir="ltr"
            />
          </div>
          <div>
            <label className="text-sm font-semibold mb-2 block">الـ Prefix الجديد:</label>
            <Input
              type="number"
              value={newPrefix}
              onChange={(e) => setNewPrefix(e.target.value)}
              placeholder="26"
              className="font-mono"
              dir="ltr"
              min={parsed?.prefix || 0}
              max={32}
            />
          </div>
        </div>

        {result && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <StatBox label="عدد الشبكات" en="Subnets" value={result.numSubnets.toString()} icon={<Layers className="h-4 w-4" />} />
              <StatBox label="مضيف لكل شبكة" en="Hosts/Subnet" value={result.hostsPerSubnet.toString()} icon={<Hash className="h-4 w-4" />} />
              <StatBox label="bits مستعارة" en="Borrowed" value={result.borrowedBits.toString()} icon={<Binary className="h-4 w-4" />} />
              <StatBox label="Block size" en="Block" value={result.blockSize.toString()} icon={<Globe className="h-4 w-4" />} />
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-[#002b5c] text-white">
                    <th className="px-3 py-2 text-center">#</th>
                    <th className="px-3 py-2 text-right" dir="ltr">Network</th>
                    <th className="px-3 py-2 text-right" dir="ltr">First Host</th>
                    <th className="px-3 py-2 text-right" dir="ltr">Last Host</th>
                    <th className="px-3 py-2 text-right" dir="ltr">Broadcast</th>
                    <th className="px-3 py-2 text-center">نسخ</th>
                  </tr>
                </thead>
                <tbody>
                  {result.subnets.map((s, i) => (
                    <tr key={i} className={i % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                      <td className="px-3 py-2 text-center font-mono">{s.index}</td>
                      <td className="px-3 py-2 font-mono text-xs text-blue-600 dark:text-blue-400" dir="ltr">{s.network}/{result.newPrefix}</td>
                      <td className="px-3 py-2 font-mono text-xs text-green-600 dark:text-green-400" dir="ltr">{s.firstHost}</td>
                      <td className="px-3 py-2 font-mono text-xs text-green-600 dark:text-green-400" dir="ltr">{s.lastHost}</td>
                      <td className="px-3 py-2 font-mono text-xs text-red-600 dark:text-red-400" dir="ltr">{s.broadcast}</td>
                      <td className="px-3 py-2 text-center">
                        <button
                          onClick={() => { navigator.clipboard.writeText(`${s.network}/${result.newPrefix}`); setCopied(`s${i}`); setTimeout(() => setCopied(null), 1500); }}
                          className="text-muted-foreground hover:text-[#049fd9]"
                        >
                          {copied === `s${i}` ? <Check className="h-3 w-3 text-green-500" /> : <Copy className="h-3 w-3" />}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {!result && parsed && (
          <div className="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-700 text-amber-800 dark:text-amber-200 text-sm flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            الـ prefix الجديد يجب أن يكون أكبر من أو يساوي {parsed.prefix} وأصغر من أو يساوي 32.
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// 3. VLSM Calculator (supports multiple classes)
// ============================================================
function VLSMCalculator() {
  const [classType, setClassType] = useState<'A' | 'B' | 'C' | 'custom'>('C');
  const [baseInput, setBaseInput] = useState('192.168.1.0/24');
  const [requirements, setRequirements] = useState<{ name: string; hosts: string }[]>([
    { name: 'LAN Users', hosts: '60' },
    { name: 'Servers', hosts: '25' },
    { name: 'Printers', hosts: '10' },
    { name: 'WAN R1-R2', hosts: '2' },
  ]);
  const [copied, setCopied] = useState<string | null>(null);

  // Auto-fill base IP based on class
  const handleClassChange = (cls: 'A' | 'B' | 'C' | 'custom') => {
    setClassType(cls);
    if (cls === 'A') setBaseInput('10.0.0.0/8');
    else if (cls === 'B') setBaseInput('172.16.0.0/16');
    else if (cls === 'C') setBaseInput('192.168.1.0/24');
  };

  const parsed = useMemo(() => parseInput(baseInput), [baseInput]);
  const vlsmResults = useMemo(() => {
    if (!parsed) return null;
    const reqs = requirements
      .filter(r => r.name && r.hosts && parseInt(r.hosts) > 0)
      .map(r => ({ name: r.name, hosts: parseInt(r.hosts) }));
    if (reqs.length === 0) return [];
    return calcVLSM(parsed.ip, parsed.prefix, reqs);
  }, [parsed, requirements]);

  const addRow = () => setRequirements([...requirements, { name: '', hosts: '' }]);
  const removeRow = (i: number) => setRequirements(requirements.filter((_, idx) => idx !== i));
  const updateRow = (i: number, field: 'name' | 'hosts', value: string) => {
    const next = [...requirements];
    next[i] = { ...next[i], [field]: value };
    setRequirements(next);
  };

  const copyAll = () => {
    if (!vlsmResults || vlsmResults.length === 0) return;
    const text = `VLSM Subnet Allocation Report
==============================
Base Network: ${parsed!.ip}/${parsed!.prefix}
Class: ${getIpClass((ipToInt(parsed!.ip) >>> 24) & 0xff)}

Subnets:
${vlsmResults.map((s, i) => `${i + 1}. ${s.name}
   Required: ${s.requiredHosts} hosts
   Allocated: ${s.allocatedHosts} hosts (/${s.prefix})
   Network: ${s.network}
   Range: ${s.range}
   Broadcast: ${s.broadcast}
   Mask: ${s.subnetMask}
   Wildcard: ${s.wildcard}`).join('\n\n')}

Cisco Commands:
${vlsmResults.filter(s => s.status === 'ok').map(s => `interface <iface-${s.name.replace(/\s+/g, '-')}>
  ip address ${s.firstHost} ${s.subnetMask}
  no shutdown`).join('\n\n')}`;
    navigator.clipboard.writeText(text);
    setCopied('all');
    setTimeout(() => setCopied(null), 2000);
  };

  const copySubnet = (s: VLSMSubnet, idx: number) => {
    const text = `Subnet: ${s.name}
Required: ${s.requiredHosts} hosts
Allocated: ${s.allocatedHosts} hosts (/${s.prefix})
Network: ${s.network}
Range: ${s.range}
Broadcast: ${s.broadcast}
Mask: ${s.subnetMask}
Wildcard: ${s.wildcard}

Cisco:
interface <iface>
  ip address ${s.firstHost} ${s.subnetMask}
  no shutdown
network ${s.network} ${s.wildcard} area 0`;
    navigator.clipboard.writeText(text);
    setCopied(`s${idx}`);
    setTimeout(() => setCopied(null), 1500);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between gap-2 text-lg flex-wrap">
          <span className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-[#049fd9]" />
            مقسم VLSM - Variable Length Subnet Mask
          </span>
          {vlsmResults && vlsmResults.length > 0 && (
            <Button size="sm" onClick={copyAll} className="text-xs">
              {copied === 'all' ? <Check className="h-3 w-3 ml-1" /> : <Copy className="h-3 w-3 ml-1" />}
              {copied === 'all' ? 'تم النسخ' : 'نسخ الكل'}
            </Button>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Class selection */}
        <div>
          <label className="text-sm font-semibold mb-2 block">اختر الصنف (Class):</label>
          <div className="flex flex-wrap gap-2">
            {(['A', 'B', 'C', 'custom'] as const).map(cls => (
              <button
                key={cls}
                onClick={() => handleClassChange(cls)}
                className={cn(
                  'px-4 py-1.5 rounded-lg text-xs font-medium transition',
                  classType === cls
                    ? 'bg-[#049fd9] text-white'
                    : 'bg-muted hover:bg-muted/70'
                )}
              >
                {cls === 'custom' ? 'مخصص' : `Class ${cls}`}
                {cls === 'A' && <span className="text-[10px] opacity-70 ml-1" dir="ltr">10.0.0.0/8</span>}
                {cls === 'B' && <span className="text-[10px] opacity-70 ml-1" dir="ltr">172.16.0.0/16</span>}
                {cls === 'C' && <span className="text-[10px] opacity-70 ml-1" dir="ltr">192.168.1.0/24</span>}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-sm font-semibold mb-2 block">الشبكة الأساسية (Base Network):</label>
          <Input
            value={baseInput}
            onChange={(e) => setBaseInput(e.target.value)}
            placeholder="192.168.1.0/24"
            className="font-mono"
            dir="ltr"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-semibold">المتطلبات (Requirements):</label>
            <Button size="sm" variant="outline" onClick={addRow} className="text-xs">+ إضافة صف</Button>
          </div>
          <div className="space-y-2">
            <div className="grid grid-cols-[1fr_120px_40px] gap-2 text-xs font-semibold text-muted-foreground">
              <span>اسم الشبكة</span>
              <span>عدد المضيفين</span>
              <span></span>
            </div>
            {requirements.map((req, i) => (
              <div key={i} className="grid grid-cols-[1fr_120px_40px] gap-2">
                <Input
                  value={req.name}
                  onChange={(e) => updateRow(i, 'name', e.target.value)}
                  placeholder={`Subnet ${i + 1}`}
                  className="text-sm"
                />
                <Input
                  type="number"
                  value={req.hosts}
                  onChange={(e) => updateRow(i, 'hosts', e.target.value)}
                  placeholder="0"
                  className="font-mono text-sm"
                  dir="ltr"
                />
                <Button variant="ghost" size="icon" onClick={() => removeRow(i)} className="h-8 w-8 text-red-500">×</Button>
              </div>
            ))}
          </div>
        </div>

        {vlsmResults && vlsmResults.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[#002b5c] text-white">
                  <th className="px-3 py-2 text-right">الشبكة</th>
                  <th className="px-3 py-2 text-center">المطلوب</th>
                  <th className="px-3 py-2 text-center">المخصص</th>
                  <th className="px-3 py-2 text-center">/Prefix</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Network</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Range</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Broadcast</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Wildcard</th>
                  <th className="px-3 py-2 text-center">نسخ</th>
                </tr>
              </thead>
              <tbody>
                {vlsmResults.map((s, i) => (
                  <tr key={i} className={cn(i % 2 === 0 ? 'bg-card' : 'bg-muted/20', s.status === 'fail' && 'bg-red-50 dark:bg-red-950/20')}>
                    <td className="px-3 py-2 font-medium">{s.name}</td>
                    <td className="px-3 py-2 text-center">{s.requiredHosts}</td>
                    <td className="px-3 py-2 text-center">
                      <span className={s.status === 'fail' ? 'text-red-500' : 'text-green-600 dark:text-green-400 font-bold'}>
                        {s.allocatedHosts || 'FAIL'}
                      </span>
                    </td>
                    <td className="px-3 py-2 text-center font-mono" dir="ltr">/{s.prefix}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.network}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.range}</td>
                    <td className="px-3 py-2 font-mono text-xs text-red-600 dark:text-red-400" dir="ltr">{s.broadcast}</td>
                    <td className="px-3 py-2 font-mono text-xs text-amber-600 dark:text-amber-400" dir="ltr">{s.wildcard}</td>
                    <td className="px-3 py-2 text-center">
                      <button
                        onClick={() => copySubnet(s, i)}
                        className="text-muted-foreground hover:text-[#049fd9]"
                        disabled={s.status === 'fail'}
                      >
                        {copied === `s${i}` ? <Check className="h-3 w-3 text-green-500" /> : <Copy className="h-3 w-3" />}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {vlsmResults && vlsmResults.some(s => s.status === 'fail') && (
          <div className="p-3 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 text-sm flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            لا توجد مساحة كافية في الشبكة الأساسية. استخدم شبكة أكبر (مثلاً Class B أو /23 بدلاً من /24).
          </div>
        )}

        <div className="p-3 rounded-lg bg-cyan-50 dark:bg-cyan-950/20 border border-cyan-300 dark:border-cyan-700 text-cyan-800 dark:text-cyan-200 text-sm flex items-start gap-2">
          <Info className="h-4 w-4 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold mb-1">قاعدة VLSM الذهبية:</p>
            <p>رتّب الشبكات تنازلياً حسب عدد المضيفين. السبب: لو بدأت من /30 ثم حاولت وضع /26، قد لا تجد مساحة متصلة.</p>
            <p className="mt-1">VLSM = Variable Length Subnet Mask - يسمح بأقنعة مختلفة الطول في نفس الشبكة، مما يقلل هدر العناوين.</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ============================================================
// 4. Tools View
// ============================================================
function ToolsView() {
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Wrench className="h-5 w-5 text-[#049fd9]" />
            أدوات مساعدة
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <SubnettingPractice />
            <QuickConverter />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function SubnettingPractice() {
  const [question, setQuestion] = useState<{ ip: string; prefix: number } | null>(null);
  const [answer, setAnswer] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [correct, setCorrect] = useState(false);

  const generate = () => {
    const prefixes = [24, 25, 26, 27, 28, 29, 30];
    const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
    const block = Math.pow(2, 32 - prefix);
    const octet4 = Math.floor(Math.random() * block);
    setQuestion({ ip: `192.168.1.${octet4}`, prefix });
    setAnswer('');
    setShowResult(false);
  };

  const check = () => {
    if (!question) return;
    const info = calculateSubnet(question.ip, question.prefix);
    setCorrect(answer.trim() === info.network);
    setShowResult(true);
  };

  return (
    <Card className="bg-amber-50/50 dark:bg-amber-950/10 border-amber-300/50">
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <Target className="h-4 w-4 text-amber-600" />
          تدريب Subnetting
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {!question ? (
          <Button onClick={generate} className="w-full">ابدأ التدريب</Button>
        ) : (
          <>
            <div className="text-sm bg-muted p-3 rounded">
              ما هو عنوان الشبكة لـ <code className="font-mono font-bold text-[#049fd9]" dir="ltr">{question.ip}/{question.prefix}</code>؟
            </div>
            <Input
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="192.168.1.0"
              className="font-mono"
              dir="ltr"
            />
            <div className="flex gap-2">
              <Button onClick={check} className="flex-1" size="sm">تحقق</Button>
              <Button onClick={generate} variant="outline" size="sm">سؤال جديد</Button>
            </div>
            {showResult && (
              <div className={cn('p-2 rounded text-sm flex items-center gap-2', correct ? 'bg-green-50 dark:bg-green-950/20 text-green-700 dark:text-green-300' : 'bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300')}>
                {correct ? <CheckCircle2 className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
                {correct ? 'إجابة صحيحة! 🎉' : `الإجابة الصحيحة: ${calculateSubnet(question.ip, question.prefix).network}`}
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

function QuickConverter() {
  const [ip, setIp] = useState('192.168.1.1');
  const [mask, setMask] = useState('255.255.255.0');

  const result = useMemo(() => {
    try {
      const ipInt = ipToInt(ip);
      const maskInt = ipToInt(mask);
      let prefix = 0;
      let v = maskInt >>> 0;
      while (v & 0x80000000) {
        prefix++;
        v = (v << 1) >>> 0;
      }
      const wildcard = intToIp((~maskInt) >>> 0);
      const network = intToIp((ipInt & maskInt) >>> 0);
      const broadcast = intToIp((ipInt & maskInt | ~maskInt) >>> 0);
      return { prefix, wildcard, network, broadcast, ipBinary: intToBinary(ipInt), maskBinary: intToBinary(maskInt) };
    } catch {
      return null;
    }
  }, [ip, mask]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <Zap className="h-4 w-4 text-[#049fd9]" />
          محول سريع
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <label className="text-xs text-muted-foreground">IP Address:</label>
          <Input value={ip} onChange={(e) => setIp(e.target.value)} className="font-mono" dir="ltr" />
        </div>
        <div>
          <label className="text-xs text-muted-foreground">Subnet Mask:</label>
          <Input value={mask} onChange={(e) => setMask(e.target.value)} className="font-mono" dir="ltr" />
        </div>
        {result && (
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-muted-foreground">Prefix:</span><code className="font-mono" dir="ltr">/{result.prefix}</code></div>
            <div className="flex justify-between"><span className="text-muted-foreground">Wildcard:</span><code className="font-mono" dir="ltr">{result.wildcard}</code></div>
            <div className="flex justify-between"><span className="text-muted-foreground">Network:</span><code className="font-mono text-blue-600 dark:text-blue-400" dir="ltr">{result.network}</code></div>
            <div className="flex justify-between"><span className="text-muted-foreground">Broadcast:</span><code className="font-mono text-red-600 dark:text-red-400" dir="ltr">{result.broadcast}</code></div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ============================================================
// 5. Study Reference
// ============================================================
function StudyReference() {
  const [search, setSearch] = useState('');
  const filtered = CIDR_TABLE.filter(row =>
    !search ||
    row.cidr.toString().includes(search) ||
    row.mask.includes(search) ||
    row.wildcard.includes(search) ||
    row.hosts.toString().includes(search) ||
    row.use.toLowerCase().includes(search.toLowerCase())
  );

  const classes = [
    { name: 'A', range: '1.0.0.0 - 126.255.255.255', prefix: '/8', defaultMask: '255.0.0.0', private: '10.0.0.0/8', hosts: '16,777,214', use: 'شبكات المؤسسات الكبيرة' },
    { name: 'B', range: '128.0.0.0 - 191.255.255.255', prefix: '/16', defaultMask: '255.255.0.0', private: '172.16.0.0/12', hosts: '65,534', use: 'شبكات متوسطة الحجم' },
    { name: 'C', range: '192.0.0.0 - 223.255.255.255', prefix: '/24', defaultMask: '255.255.255.0', private: '192.168.0.0/16', hosts: '254', use: 'شبكات صغيرة (الأكثر شيوعاً)' },
    { name: 'D', range: '224.0.0.0 - 239.255.255.255', prefix: '-', defaultMask: '-', private: '-', hosts: '-', use: 'Multicast (OSPF، EIGRP، Streaming)' },
    { name: 'E', range: '240.0.0.0 - 255.255.255.255', prefix: '-', defaultMask: '-', private: '-', hosts: '-', use: 'Reserved (Research)' },
  ];

  const special = [
    { ip: '127.0.0.0/8', name: 'Loopback', desc: 'localhost - للـ self-test' },
    { ip: '169.254.0.0/16', name: 'Link-Local (APIPA)', desc: 'auto-config عند فشل DHCP' },
    { ip: '0.0.0.0', name: 'Default Route', desc: 'يستعمل في ip route 0.0.0.0 0.0.0.0' },
    { ip: '255.255.255.255', name: 'Broadcast', desc: 'limited broadcast - لكل الأجهزة' },
    { ip: '100.64.0.0/10', name: 'CGNAT', desc: 'Carrier-Grade NAT (RFC 6598)' },
    { ip: '192.0.2.0/24', name: 'TEST-NET', desc: 'للتوثيق والأمثلة (RFC 5737)' },
    { ip: '198.18.0.0/15', name: 'Benchmark', desc: 'اختبار أداء الشبكات (RFC 2544)' },
    { ip: '203.0.113.0/24', name: 'TEST-NET-3', desc: 'للتوثيق (RFC 5737)' },
  ];

  return (
    <div className="space-y-4">
      {/* CIDR Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <TableIcon className="h-5 w-5 text-[#049fd9]" />
            جدول CIDR المرجعي الشامل
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="بحث: /24، 255، 254، wildcard، wan..."
            className="font-mono"
            dir="ltr"
          />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[#002b5c] text-white">
                  <th className="px-3 py-2 text-center">CIDR</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Subnet Mask</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Wildcard</th>
                  <th className="px-3 py-2 text-center">Hosts</th>
                  <th className="px-3 py-2 text-center">Block Size</th>
                  <th className="px-3 py-2 text-right">الاستخدام</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((row, i) => (
                  <tr key={row.cidr} className={i % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                    <td className="px-3 py-2 text-center font-mono font-bold text-[#049fd9]">/{row.cidr}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{row.mask}</td>
                    <td className="px-3 py-2 font-mono text-xs text-amber-600 dark:text-amber-400" dir="ltr">{row.wildcard}</td>
                    <td className="px-3 py-2 text-center font-bold">{row.hosts.toLocaleString()}</td>
                    <td className="px-3 py-2 text-center font-mono">{row.block}</td>
                    <td className="px-3 py-2 text-xs">{row.use}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div className="p-4 rounded-lg bg-amber-50 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-700">
              <h4 className="text-sm font-bold mb-2 flex items-center gap-2 text-amber-700 dark:text-amber-400">
                <Lightbulb className="h-4 w-4" />
                حفظ سريع
              </h4>
              <ul className="text-sm space-y-1 text-amber-900 dark:text-amber-200">
                <li><code className="font-mono" dir="ltr">/30</code> = 2 hosts (WAN links)</li>
                <li><code className="font-mono" dir="ltr">/29</code> = 6 hosts</li>
                <li><code className="font-mono" dir="ltr">/28</code> = 14 hosts</li>
                <li><code className="font-mono" dir="ltr">/27</code> = 30 hosts</li>
                <li><code className="font-mono" dir="ltr">/26</code> = 62 hosts</li>
                <li><code className="font-mono" dir="ltr">/24</code> = 254 hosts (Class C)</li>
                <li><code className="font-mono" dir="ltr">/23</code> = 510 hosts (Supernet)</li>
              </ul>
            </div>
            <div className="p-4 rounded-lg bg-cyan-50 dark:bg-cyan-950/20 border border-cyan-300 dark:border-cyan-700">
              <h4 className="text-sm font-bold mb-2 flex items-center gap-2 text-cyan-700 dark:text-cyan-400">
                <Info className="h-4 w-4" />
                قاعدة الحساب
              </h4>
              <div className="text-sm space-y-2 text-cyan-900 dark:text-cyan-200">
                <p>عدد المضيفين = <code className="font-mono px-1 bg-muted rounded" dir="ltr">2^(32-prefix) - 2</code></p>
                <p>Wildcard = <code className="font-mono px-1 bg-muted rounded" dir="ltr">255.255.255.255 - mask</code></p>
                <p>Block size = <code className="font-mono px-1 bg-muted rounded" dir="ltr">2^(32-prefix)</code></p>
                <p>Subnets في /24 = <code className="font-mono px-1 bg-muted rounded" dir="ltr">256 / block_size</code></p>
                <p>Borrowed bits = <code className="font-mono px-1 bg-muted rounded" dir="ltr">new_prefix - default_prefix</code></p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* IPv4 Classes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Layers className="h-5 w-5 text-[#049fd9]" />
            أصناف عناوين IPv4 (IP Classes)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-[#002b5c] text-white">
                  <th className="px-3 py-2 text-center">الصنف</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Range</th>
                  <th className="px-3 py-2 text-center">Default</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Default Mask</th>
                  <th className="px-3 py-2 text-right" dir="ltr">Private Block</th>
                  <th className="px-3 py-2 text-center">Hosts</th>
                  <th className="px-3 py-2 text-right">الاستخدام</th>
                </tr>
              </thead>
              <tbody>
                {classes.map((c, i) => (
                  <tr key={c.name} className={i % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                    <td className="px-3 py-2 text-center"><Badge variant="outline" className="font-bold">{c.name}</Badge></td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{c.range}</td>
                    <td className="px-3 py-2 text-center font-mono" dir="ltr">{c.prefix}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{c.defaultMask}</td>
                    <td className="px-3 py-2 font-mono text-xs text-amber-600 dark:text-amber-400" dir="ltr">{c.private}</td>
                    <td className="px-3 py-2 text-center font-bold">{c.hosts}</td>
                    <td className="px-3 py-2 text-xs">{c.use}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Special IPs */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Info className="h-4 w-4 text-[#049fd9]" />
            عناوين IPv4 الخاصة (Special Use)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {special.map((s, i) => (
              <div key={i} className="bg-muted/30 rounded-lg p-3 border border-border">
                <div className="flex items-center justify-between mb-1">
                  <code className="font-mono text-sm font-bold text-[#049fd9]" dir="ltr">{s.ip}</code>
                  <Badge variant="outline" className="text-[10px]">{s.name}</Badge>
                </div>
                <p className="text-xs text-muted-foreground">{s.desc}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
