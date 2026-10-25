'use client';

import { useState, useMemo } from 'react';
import { LAB_TOPOLOGIES, LAB_DIFFICULTY_CONFIG } from '@/data/lab-topologies';
import type { LabTopology } from '@/data/lab-topologies';
import {
  FlaskConical,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  Target,
  Clock,
  Network,
  AlertTriangle,
  CheckCircle2,
  ListChecks,
  Search,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export function Labs() {
  const [search, setSearch] = useState('');
  const [activeDifficulty, setActiveDifficulty] = useState<'all' | 'beginner' | 'intermediate' | 'advanced'>('all');
  const [expandedLabs, setExpandedLabs] = useState<Set<string>>(new Set());

  const filteredLabs = useMemo(() => {
    return LAB_TOPOLOGIES.filter(lab => {
      if (search && !lab.title.includes(search) && !lab.titleEn.toLowerCase().includes(search.toLowerCase()) && !lab.tags.some(t => t.toLowerCase().includes(search.toLowerCase()))) return false;
      if (activeDifficulty !== 'all' && lab.difficulty !== activeDifficulty) return false;
      return true;
    });
  }, [search, activeDifficulty]);

  const toggleLab = (id: string) => {
    setExpandedLabs(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) newSet.delete(id);
      else newSet.add(id);
      return newSet;
    });
  };

  return (
    <div className="space-y-5">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard label="إجمالي السيناريوهات" value={LAB_TOPOLOGIES.length} icon={<FlaskConical className="h-5 w-5" />} color="from-blue-500 to-cyan-500" />
        <StatCard label="مبتدئ" value={LAB_TOPOLOGIES.filter(l => l.difficulty === 'beginner').length} icon={<Target className="h-5 w-5" />} color="from-green-500 to-emerald-500" />
        <StatCard label="متوسط" value={LAB_TOPOLOGIES.filter(l => l.difficulty === 'intermediate').length} icon={<Target className="h-5 w-5" />} color="from-amber-500 to-orange-500" />
        <StatCard label="متقدم" value={LAB_TOPOLOGIES.filter(l => l.difficulty === 'advanced').length} icon={<Target className="h-5 w-5" />} color="from-red-500 to-rose-500" />
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-5 space-y-3">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="ابحث عن سيناريو... (مثال: OSPF، VLAN، NAT)"
              className="pr-9 pl-4 h-10 text-sm"
              dir="rtl"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-muted-foreground mb-2 block">المستوى:</label>
            <div className="flex flex-wrap gap-2">
              <DifficultyTab active={activeDifficulty === 'all'} onClick={() => setActiveDifficulty('all')} label="الكل" count={LAB_TOPOLOGIES.length} />
              {(['beginner', 'intermediate', 'advanced'] as const).map(d => (
                <DifficultyTab
                  key={d}
                  active={activeDifficulty === d}
                  onClick={() => setActiveDifficulty(d)}
                  label={LAB_DIFFICULTY_CONFIG[d].label}
                  count={LAB_TOPOLOGIES.filter(l => l.difficulty === d).length}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Lab Cards */}
      {filteredLabs.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            لا توجد سيناريوهات مطابقة
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredLabs.map(lab => (
            <LabCard
              key={lab.id}
              lab={lab}
              expanded={expandedLabs.has(lab.id)}
              onToggle={() => toggleLab(lab.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function LabCard({ lab, expanded, onToggle }: { lab: LabTopology; expanded: boolean; onToggle: () => void }) {
  const diffConfig = LAB_DIFFICULTY_CONFIG[lab.difficulty];
  return (
    <Card className="overflow-hidden">
      <CardHeader
        className="cursor-pointer hover:bg-muted/30 transition"
        onClick={onToggle}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 flex-1">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-[#002b5c] to-[#049fd9] text-white">
              <FlaskConical className="h-5 w-5" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-bold text-foreground">{lab.title}</h3>
              <p className="text-sm text-[#049fd9] font-mono" dir="ltr">{lab.titleEn}</p>
              <div className="flex flex-wrap items-center gap-2 mt-2">
                <Badge className={cn('text-[10px]', diffConfig.color)} variant="outline">
                  {diffConfig.label}
                </Badge>
                <Badge variant="outline" className="text-[10px] gap-1">
                  <Clock className="h-2.5 w-2.5" />
                  {lab.duration}
                </Badge>
                {lab.tags.slice(0, 3).map(tag => (
                  <Badge key={tag} variant="outline" className="text-[10px]">#{tag}</Badge>
                ))}
              </div>
            </div>
          </div>
          <div className="shrink-0 text-muted-foreground">
            {expanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </div>
        </div>
      </CardHeader>

      {expanded && (
        <CardContent className="space-y-5 animate-in fade-in slide-in-from-top-2 duration-200">
          {/* Topology */}
          <div className="bg-muted/30 rounded-lg p-3 border border-border">
            <div className="flex items-center gap-2 mb-2">
              <Network className="h-4 w-4 text-[#049fd9]" />
              <span className="text-sm font-bold">الطوبولوجيا</span>
            </div>
            <p className="text-sm font-mono text-foreground" dir="ltr">{lab.topology}</p>
          </div>

          {/* Objectives */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Target className="h-4 w-4 text-[#049fd9]" />
              <span className="text-sm font-bold">الأهداف</span>
            </div>
            <ul className="space-y-1 text-sm pr-6 list-disc">
              {lab.objectives.map((obj, i) => (
                <li key={i} className="text-foreground/90">{obj}</li>
              ))}
            </ul>
          </div>

          {/* Steps */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <ListChecks className="h-4 w-4 text-[#049fd9]" />
              <span className="text-sm font-bold">الخطوات</span>
            </div>
            <div className="space-y-3">
              {lab.steps.map((step, i) => (
                <StepCard key={i} step={step} index={i + 1} />
              ))}
            </div>
          </div>

          {/* Verification */}
          <div className="rounded-lg bg-green-50 dark:bg-green-950/10 border border-green-300 dark:border-green-700 p-3">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
              <span className="text-sm font-bold text-green-700 dark:text-green-400">التحقق</span>
            </div>
            <ul className="space-y-1 text-sm pr-6 list-disc text-green-900 dark:text-green-200">
              {lab.verification.map((v, i) => (
                <li key={i} className="font-mono text-xs" dir="ltr">{v}</li>
              ))}
            </ul>
          </div>

          {/* Common Issues */}
          <div className="rounded-lg bg-amber-50 dark:bg-amber-950/10 border border-amber-300 dark:border-amber-700 p-3">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="h-4 w-4 text-amber-600 dark:text-amber-400" />
              <span className="text-sm font-bold text-amber-700 dark:text-amber-400">مشاكل شائعة</span>
            </div>
            <ul className="space-y-1 text-sm pr-6 list-disc text-amber-900 dark:text-amber-200">
              {lab.commonIssues.map((issue, i) => (
                <li key={i} className="text-xs">{issue}</li>
              ))}
            </ul>
          </div>
        </CardContent>
      )}
    </Card>
  );
}

function StepCard({ step, index }: { step: LabTopology['steps'][0]; index: number }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(step.commands);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <div className="bg-card border border-border rounded-lg p-3">
      <div className="flex items-start justify-between gap-2 mb-2">
        <p className="text-sm font-medium text-foreground flex-1">{step.description}</p>
        <button
          onClick={copy}
          className="shrink-0 text-muted-foreground hover:text-[#049fd9] transition p-1 rounded hover:bg-[#049fd9]/10"
          title="نسخ الأوامر"
        >
          {copied ? <Check className="h-3.5 w-3.5 text-green-500" /> : <Copy className="h-3.5 w-3.5" />}
        </button>
      </div>
      <pre
        dir="ltr"
        className="text-left font-mono text-xs bg-muted dark:bg-muted/40 px-3 py-2 rounded border border-border overflow-x-auto whitespace-pre-wrap"
      >
        {step.commands}
      </pre>
      {step.explanation && (
        <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
          <Info className="inline h-3 w-3 ml-1" />
          {step.explanation}
        </p>
      )}
    </div>
  );
}

function Info({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 16v-4"/>
      <path d="M12 8h.01"/>
    </svg>
  );
}

function StatCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: number; color: string }) {
  return (
    <div className={cn('rounded-xl p-4 text-white bg-gradient-to-br', color)}>
      <div className="flex items-center justify-between mb-1">
        {icon}
        <span className="text-2xl font-black">{value}</span>
      </div>
      <div className="text-xs opacity-90">{label}</div>
    </div>
  );
}

function DifficultyTab({ active, onClick, label, count }: { active: boolean; onClick: () => void; label: string; count: number }) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs transition',
        active
          ? 'bg-[#049fd9] text-white border-[#049fd9]'
          : 'bg-background text-foreground border-border hover:border-[#049fd9]/50'
      )}
    >
      {label}
      <span className={cn(
        'rounded-full px-1.5 py-0.5 text-[10px] font-mono',
        active ? 'bg-white/20' : 'bg-muted'
      )}>
        {count}
      </span>
    </button>
  );
}
