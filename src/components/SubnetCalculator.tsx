'use client';

import { useState, useMemo, useCallback } from 'react';
import {
  Calculator,
  Network,
  Split,
  Table as TableIcon,
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
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

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
  ipBinary: string;
  networkBinary: string;
  maskBinary: string;
  borrowedBits: number;
  hostBits: number;
}

// IP utilities
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

function isPrivateIp(ip: string): boolean {
  const parts = ip.split('.').map(Number);
  if (parts[0] === 10) return true;
  if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
  if (parts[0] === 192 && parts[1] === 168) return true;
  if (parts[0] === 127) return true; // loopback
  return false;
}

function parseInput(input: string): { ip: string; prefix: number } | null {
  const trimmed = input.trim();
  // Format: 192.168.1.0/24
  let m = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/(\d{1,2})$/);
  if (m) {
    const prefix = parseInt(m[2]);
    if (prefix >= 0 && prefix <= 32) {
      try {
        ipToInt(m[1]); // validate
        return { ip: m[1], prefix };
      } catch { return null; }
    }
  }
  // Format: 192.168.1.0 255.255.255.0
  m = trimmed.match(/^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/);
  if (m) {
    try {
      ipToInt(m[1]);
      const maskInt = ipToInt(m[2]);
      // count bits in mask
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
  const isPrivate = isPrivateIp(ip);

  // borrowed bits (assuming default classful)
  let defaultPrefix = 0;
  if (ipClass === 'A') defaultPrefix = 8;
  else if (ipClass === 'B') defaultPrefix = 16;
  else if (ipClass === 'C') defaultPrefix = 24;
  const borrowedBits = Math.max(0, prefix - defaultPrefix);

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
    ipBinary: intToBinary(ipInt),
    networkBinary: intToBinary(networkInt),
    maskBinary: intToBinary(maskInt),
    borrowedBits,
    hostBits,
  };
}

// VLSM Calculator
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
}

function calcVLSM(baseIp: string, basePrefix: number, requirements: { name: string; hosts: number }[]): VLSMSubnet[] {
  // Sort requirements by descending number of hosts
  const sorted = [...requirements].sort((a, b) => b.hosts - a.hosts);
  let currentInt = ipToInt(baseIp);
  const baseMaskInt = maskFromPrefix(basePrefix);
  currentInt = (currentInt & baseMaskInt) >>> 0; // align to network
  const baseBroadcast = (currentInt | (~baseMaskInt >>> 0)) >>> 0;

  const result: VLSMSubnet[] = [];

  for (const req of sorted) {
    if (req.hosts <= 0) continue;
    // Find smallest prefix that can accommodate hosts + 2 (network + broadcast)
    let needed = req.hosts + 2;
    let hostBits = 1;
    while (Math.pow(2, hostBits) < needed) hostBits++;
    const prefix = 32 - hostBits;
    const blockSize = Math.pow(2, hostBits);
    const subnetMask = maskFromPrefix(prefix);

    // Align current to block size
    const blockStart = Math.floor(currentInt / blockSize) * blockSize;
    const networkInt = blockStart >>> 0;
    const broadcastInt = (networkInt + blockSize - 1) >>> 0;

    // Check if exceeds base
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
    });

    currentInt = (broadcastInt + 1) >>> 0;
  }

  return result;
}

// CIDR Reference Table
const CIDR_TABLE = [
  { cidr: 30, mask: '255.255.255.252', wildcard: '0.0.0.3', hosts: 2, subnets24: 64 },
  { cidr: 29, mask: '255.255.255.248', wildcard: '0.0.0.7', hosts: 6, subnets24: 32 },
  { cidr: 28, mask: '255.255.255.240', wildcard: '0.0.0.15', hosts: 14, subnets24: 16 },
  { cidr: 27, mask: '255.255.255.224', wildcard: '0.0.0.31', hosts: 30, subnets24: 8 },
  { cidr: 26, mask: '255.255.255.192', wildcard: '0.0.0.63', hosts: 62, subnets24: 4 },
  { cidr: 25, mask: '255.255.255.128', wildcard: '0.0.0.127', hosts: 126, subnets24: 2 },
  { cidr: 24, mask: '255.255.255.0', wildcard: '0.0.0.255', hosts: 254, subnets24: 1 },
  { cidr: 23, mask: '255.255.254.0', wildcard: '0.0.1.255', hosts: 510, subnets24: 0.5 },
  { cidr: 22, mask: '255.255.252.0', wildcard: '0.0.3.255', hosts: 1022, subnets24: 0.25 },
  { cidr: 21, mask: '255.255.248.0', wildcard: '0.0.7.255', hosts: 2046, subnets24: 0.125 },
  { cidr: 20, mask: '255.255.240.0', wildcard: '0.0.15.255', hosts: 4094, subnets24: 0.0625 },
  { cidr: 19, mask: '255.255.224.0', wildcard: '0.0.31.255', hosts: 8190, subnets24: 0 },
  { cidr: 18, mask: '255.255.192.0', wildcard: '0.0.63.255', hosts: 16382, subnets24: 0 },
  { cidr: 17, mask: '255.255.128.0', wildcard: '0.0.127.255', hosts: 32766, subnets24: 0 },
  { cidr: 16, mask: '255.0.0.0', wildcard: '0.255.255.255', hosts: 65534, subnets24: 0 },
];

export function SubnetCalculator() {
  const [activeTab, setActiveTab] = useState<'analyzer' | 'vlsm' | 'cidr' | 'classes'>('analyzer');
  return (
    <div className="space-y-6">
      {/* Tab navigation */}
      <div className="flex flex-wrap gap-2">
        <TabButton active={activeTab === 'analyzer'} onClick={() => setActiveTab('analyzer')} icon={<Calculator className="h-4 w-4" />} label="محلل IP" />
        <TabButton active={activeTab === 'vlsm'} onClick={() => setActiveTab('vlsm')} icon={<Split className="h-4 w-4" />} label="مقسم VLSM" />
        <TabButton active={activeTab === 'cidr'} onClick={() => setActiveTab('cidr')} icon={<TableIcon className="h-4 w-4" />} label="جدول CIDR" />
        <TabButton active={activeTab === 'classes'} onClick={() => setActiveTab('classes')} icon={<Layers className="h-4 w-4" />} label="أصناف IP" />
      </div>

      {activeTab === 'analyzer' && <IPAnalyzer />}
      {activeTab === 'vlsm' && <VLSMCalculator />}
      {activeTab === 'cidr' && <CIDRTable />}
      {activeTab === 'classes' && <IPClassesTable />}
    </div>
  );
}

function TabButton({ active, onClick, icon, label }: { active: boolean; onClick: () => void; icon: React.ReactNode; label: string }) {
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
      {label}
    </button>
  );
}

// ============== IP Analyzer ==============
function IPAnalyzer() {
  const [input, setInput] = useState('192.168.1.130/26');
  const [copied, setCopied] = useState<string | null>(null);
  const parsed = useMemo(() => parseInput(input), [input]);
  const info = useMemo(() => parsed ? calculateSubnet(parsed.ip, parsed.prefix) : null, [parsed]);

  const examples = ['192.168.1.130/26', '10.0.0.5/8', '172.16.5.3/22', '192.168.10.0/30', '10.1.1.1/24'];

  const copy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 1500);
  };

  return (
    <div className="space-y-5">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Network className="h-5 w-5 text-[#049fd9]" />
            محلل عنوان IP - IP Analyzer
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-semibold mb-2 block">أدخل عنوان IP مع الـ prefix أو الـ mask:</label>
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="مثال: 192.168.1.130/26 أو 10.0.0.5 255.0.0.0"
                className="font-mono text-base"
                dir="ltr"
              />
              {input && (
                <Button variant="outline" size="icon" onClick={() => setInput('')}>
                  <RefreshCw className="h-4 w-4" />
                </Button>
              )}
            </div>
            <div className="flex flex-wrap gap-2 mt-3">
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
          </div>

          {!info && parsed === null && input && (
            <div className="p-3 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 text-sm flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 shrink-0" />
              صيغة غير صحيحة. استخدم: 192.168.1.0/24 أو 10.0.0.5 255.0.0.0
            </div>
          )}

          {info && (
            <>
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
                <StatBox label="عدد المضيفين" en="Valid Hosts" value={info.hostsCount.toLocaleString()} icon={<Hash className="h-4 w-4" />} />
                <StatBox label="إجمالي العناوين" en="Total Addresses" value={info.totalAddresses.toLocaleString()} icon={<Globe className="h-4 w-4" />} />
                <StatBox label="الـ Prefix" en="Prefix" value={`/${info.prefix}`} icon={<Binary className="h-4 w-4" />} />
                <StatBox label="الصنف" en="Class" value={info.ipClass} icon={<Layers className="h-4 w-4" />} />
              </div>

              {/* Private/Public badge */}
              <div className="flex flex-wrap gap-2">
                <Badge variant={info.isPrivate ? 'default' : 'outline'} className="text-xs">
                  {info.isPrivate ? '🔒 عنوان خاص (RFC 1918)' : '🌐 عنوان عام (Public)'}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  bits مستعارة: {info.borrowedBits}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  bits للمضيف: {info.hostBits}
                </Badge>
              </div>

              {/* Binary visualization */}
              <div className="mt-4">
                <h4 className="text-sm font-bold mb-3 flex items-center gap-2">
                  <Binary className="h-4 w-4 text-[#049fd9]" />
                  التمثيل الثنائي 32-بت (Visual 32-bit)
                </h4>
                <div className="space-y-3 bg-muted/30 p-4 rounded-lg border border-border">
                  <BinaryRow label="IP" binary={info.ipBinary} prefix={info.prefix} type="ip" />
                  <BinaryRow label="Mask" binary={info.maskBinary} prefix={info.prefix} type="mask" />
                  <BinaryRow label="Network" binary={info.networkBinary} prefix={info.prefix} type="network" />
                </div>
                <div className="flex flex-wrap gap-3 mt-3 text-xs">
                  <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-blue-500"></span> Network Bits</span>
                  <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-orange-500"></span> Borrowed Bits</span>
                  <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded bg-gray-400"></span> Host Bits</span>
                </div>
              </div>

              {/* Cisco syntax */}
              <Card className="bg-[#002b5c]/5 dark:bg-[#049fd9]/5 border-[#049fd9]/30">
                <CardContent className="p-4">
                  <h4 className="text-sm font-bold mb-2 flex items-center gap-2 text-[#049fd9]">
                    <Info className="h-4 w-4" />
                    أوامر Cisco الجاهزة
                  </h4>
                  <div className="space-y-2">
                    <CiscoCmd cmd={`interface <iface>`} />
                    <CiscoCmd cmd={`ip address ${info.firstHost} ${info.subnetMask}`} />
                    {info.prefix < 31 && <CiscoCmd cmd={`ip route ${info.network} ${info.subnetMask} <next-hop>`} />}
                    <CiscoCmd cmd={`network ${info.network} ${info.wildcard} area 0`} comment="OSPF" />
                    <CiscoCmd cmd={`access-list 10 permit ${info.network} ${info.wildcard}`} comment="ACL" />
                  </div>
                </CardContent>
              </Card>

              {/* Step-by-step */}
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
                  </ol>
                </CardContent>
              </Card>
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
      {comment && <Badge variant="outline" className="text-[9px]">{comment}</Badge>}
      <code className="font-mono text-xs flex-1 text-[#b1272b] dark:text-[#ff6b6b]" dir="ltr">{cmd}</code>
      <button
        onClick={() => { navigator.clipboard.writeText(cmd); setCopied(true); setTimeout(() => setCopied(false), 1500); }}
        className="text-muted-foreground hover:text-[#049fd9]"
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

function BinaryRow({ label, binary, prefix, type }: { label: string; binary: string; prefix: number; type: 'ip' | 'mask' | 'network' }) {
  // colorize bits
  const bitsArray = binary.replace(/\./g, '').split('');
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-mono font-bold w-20 shrink-0" dir="ltr">{label}:</span>
      <div className="flex flex-wrap gap-0.5 flex-1" dir="ltr">
        {bitsArray.map((bit, i) => {
          let color = 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200';
          if (type === 'mask') {
            color = i < prefix ? 'bg-blue-500 text-white' : 'bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200';
          } else if (type === 'ip' || type === 'network') {
            if (i < prefix) color = 'bg-blue-500 text-white';
            else color = 'bg-orange-400 text-white';
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

// ============== VLSM Calculator ==============
function VLSMCalculator() {
  const [baseInput, setBaseInput] = useState('192.168.1.0/24');
  const [requirements, setRequirements] = useState<{ name: string; hosts: string }[]>([
    { name: 'LAN Users', hosts: '60' },
    { name: 'Servers', hosts: '25' },
    { name: 'Printers', hosts: '10' },
    { name: 'WAN R1-R2', hosts: '2' },
  ]);

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

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Split className="h-5 w-5 text-[#049fd9]" />
          مقسم الشبكات VLSM - VLSM Calculator
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
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
            <div className="grid grid-cols-[1fr_100px_40px] gap-2 text-xs font-semibold text-muted-foreground">
              <span>اسم الشبكة</span>
              <span>عدد المضيفين</span>
              <span></span>
            </div>
            {requirements.map((req, i) => (
              <div key={i} className="grid grid-cols-[1fr_100px_40px] gap-2">
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
                <Button variant="ghost" size="icon" onClick={() => removeRow(i)} className="h-8 w-8 text-red-500">
                  ×
                </Button>
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
                  <th className="px-3 py-2 text-right" dir="ltr">Mask</th>
                </tr>
              </thead>
              <tbody>
                {vlsmResults.map((s, i) => (
                  <tr key={i} className={i % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                    <td className="px-3 py-2 font-medium">{s.name}</td>
                    <td className="px-3 py-2 text-center">{s.requiredHosts}</td>
                    <td className="px-3 py-2 text-center">
                      <span className={s.allocatedHosts === 0 ? 'text-red-500' : 'text-green-600 dark:text-green-400 font-bold'}>
                        {s.allocatedHosts || 'FAIL'}
                      </span>
                    </td>
                    <td className="px-3 py-2 text-center font-mono" dir="ltr">/{s.prefix}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.network}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.firstHost} - {s.lastHost}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.broadcast}</td>
                    <td className="px-3 py-2 font-mono text-xs" dir="ltr">{s.subnetMask}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {vlsmResults && vlsmResults.some(s => s.allocatedHosts === 0) && (
          <div className="p-3 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 text-sm flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            لا توجد مساحة كافية في الشبكة الأساسية. استخدم شبكة أكبر (مثلاً /23 بدلاً من /24).
          </div>
        )}

        <div className="p-3 rounded-lg bg-cyan-50 dark:bg-cyan-950/20 border border-cyan-300 dark:border-cyan-700 text-cyan-800 dark:text-cyan-200 text-sm flex items-start gap-2">
          <Info className="h-4 w-4 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold mb-1">قاعدة VLSM الذهبية:</p>
            <p>رتّب الشبكات تنازلياً حسب عدد المضيفين. السبب: لو بدأت من /30 ثم حاولت وضع /26، قد لا تجد مساحة متصلة.</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ============== CIDR Table ==============
function CIDRTable() {
  const [search, setSearch] = useState('');
  const filtered = CIDR_TABLE.filter(row =>
    !search ||
    row.cidr.toString().includes(search) ||
    row.mask.includes(search) ||
    row.wildcard.includes(search) ||
    row.hosts.toString().includes(search)
  );

  return (
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
          placeholder="بحث: /24، 255، 254، wildcard..."
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
                <th className="px-3 py-2 text-center">Hosts/Subnet</th>
                <th className="px-3 py-2 text-center">Subnets in /24</th>
                <th className="px-3 py-2 text-center">Block Size</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, i) => (
                <tr key={row.cidr} className={i % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                  <td className="px-3 py-2 text-center font-mono font-bold text-[#049fd9]">/{row.cidr}</td>
                  <td className="px-3 py-2 font-mono text-xs" dir="ltr">{row.mask}</td>
                  <td className="px-3 py-2 font-mono text-xs text-amber-600 dark:text-amber-400" dir="ltr">{row.wildcard}</td>
                  <td className="px-3 py-2 text-center font-bold">{row.hosts.toLocaleString()}</td>
                  <td className="px-3 py-2 text-center">{row.subnets24}</td>
                  <td className="px-3 py-2 text-center font-mono">{Math.pow(2, 32 - row.cidr)}</td>
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
              <li><code className="font-mono" dir="ltr">/30</code> = 2 hosts (لـ WAN links)</li>
              <li><code className="font-mono" dir="ltr">/29</code> = 6 hosts (لـ small subnets)</li>
              <li><code className="font-mono" dir="ltr">/28</code> = 14 hosts</li>
              <li><code className="font-mono" dir="ltr">/27</code> = 30 hosts</li>
              <li><code className="font-mono" dir="ltr">/26</code> = 62 hosts</li>
              <li><code className="font-mono" dir="ltr">/24</code> = 254 hosts (Class C default)</li>
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
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ============== IP Classes Table ==============
function IPClassesTable() {
  const classes = [
    { name: 'A', range: '1.0.0.0 - 126.255.255.255', prefix: '/8', defaultMask: '255.0.0.0', private: '10.0.0.0/8', hosts: '16,777,214', use: 'شبكات المؤسسات الكبيرة' },
    { name: 'B', range: '128.0.0.0 - 191.255.255.255', prefix: '/16', defaultMask: '255.255.0.0', private: '172.16.0.0/12', hosts: '65,534', use: 'شبكات متوسطة الحجم' },
    { name: 'C', range: '192.0.0.0 - 223.255.255.255', prefix: '/24', defaultMask: '255.255.255.0', private: '192.168.0.0/16', hosts: '254', use: 'شبكات صغيرة (الأكثر شيوعاً)' },
    { name: 'D', range: '224.0.0.0 - 239.255.255.255', prefix: '-', defaultMask: '-', private: '-', hosts: '-', use: 'Multicast (OSPF، EIGRP، Streaming)' },
    { name: 'E', range: '240.0.0.0 - 255.255.255.255', prefix: '-', defaultMask: '-', private: '-', hosts: '-', use: 'Reserved (Research)' },
  ];

  const special = [
    { ip: '127.0.0.0/8', name: 'Loopback', desc: 'localhost - للـ self-test' },
    { ip: '169.254.0.0/16', name: 'Link-Local', desc: 'APIPA - auto-config عند فشل DHCP' },
    { ip: '0.0.0.0', name: 'Default Route', desc: 'يستعمل في ip route 0.0.0.0 0.0.0.0' },
    { ip: '255.255.255.255', name: 'Broadcast', desc: 'limited broadcast - لكل الأجهزة' },
    { ip: '100.64.0.0/10', name: 'CGNAT', desc: 'Carrier-Grade NAT (RFC 6598)' },
    { ip: '192.0.2.0/24', name: 'TEST-NET', desc: 'للتوثيق والأمثلة (RFC 5737)' },
  ];

  return (
    <div className="space-y-4">
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
