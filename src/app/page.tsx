'use client';

import { useState, useMemo, useEffect } from 'react';
import { ALL_SECTIONS, SEARCH_INDEX } from '@/data';
import type { Section, SubSection, Command } from '@/data';
import {
  Search,
  BookOpen,
  Terminal,
  Settings,
  Shield,
  Network,
  Layers,
  GitBranch,
  TreePine,
  Lock,
  Server,
  Route,
  Zap,
  Copy,
  Filter,
  Globe,
  Share2,
  Activity,
  Gauge,
  KeyRound,
  Grid3x3,
  Globe2,
  Search as SearchIcon,
  FlaskConical,
  ListChecks,
  HelpCircle,
  Lightbulb,
  ChevronDown,
  Menu,
  X,
  Moon,
  Sun,
  Info,
  AlertTriangle,
  CheckCircle2,
  TerminalSquare,
  Copy as CopyIcon,
  Check,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  BookOpen,
  Terminal,
  Settings,
  Shield,
  Network,
  Layers,
  GitBranch,
  TreePine,
  Lock,
  Server,
  Route,
  Zap,
  Copy,
  Filter,
  Globe,
  Share2,
  Activity,
  Gauge,
  KeyRound,
  Grid3x3,
  Globe2,
  Search: SearchIcon,
  FlaskConical,
  ListChecks,
  HelpCircle,
  Lightbulb,
};

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSectionId, setActiveSectionId] = useState<number | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);
  const [filterMode, setFilterMode] = useState<'all' | 'commands' | 'tables' | 'tips'>('all');

  // Toggle dark mode
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  // Search results
  const searchResults = useMemo(() => {
    if (!searchQuery.trim()) return [];
    const query = searchQuery.toLowerCase();
    return SEARCH_INDEX.filter(entry =>
      entry.command.toLowerCase().includes(query) ||
      entry.mode.toLowerCase().includes(query) ||
      entry.explanation.toLowerCase().includes(query) ||
      entry.sectionTitle.toLowerCase().includes(query)
    ).slice(0, 50);
  }, [searchQuery]);

  // Scroll spy - detect active section
  useEffect(() => {
    const handleScroll = () => {
      const sections = ALL_SECTIONS.map(s => `section-${s.id}`);
      for (let i = sections.length - 1; i >= 0; i--) {
        const el = document.getElementById(sections[i]);
        if (el && el.getBoundingClientRect().top <= 120) {
          setActiveSectionId(ALL_SECTIONS[i].id);
          break;
        }
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: number) => {
    const el = document.getElementById(`section-${id}`);
    if (el) {
      const offset = 80;
      const top = el.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
    setSidebarOpen(false);
  };

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedCmd(id);
      setTimeout(() => setCopiedCmd(null), 2000);
    } catch (e) {
      console.error('Copy failed', e);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground" dir="rtl">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl">
        <div className="container mx-auto max-w-[1600px] px-4">
          <div className="flex h-16 items-center justify-between gap-4">
            {/* Logo + Title */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 hover:bg-muted rounded-md transition"
                aria-label="Toggle sidebar"
              >
                {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
              <div className="flex items-center gap-2.5">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-[#002b5c] to-[#049fd9] text-white shadow-md">
                  <TerminalSquare size={18} />
                </div>
                <div className="hidden sm:block">
                  <div className="text-sm font-bold leading-tight">مذكرة سيسكو</div>
                  <div className="text-[10px] text-muted-foreground">CCNA & CCNP Reference</div>
                </div>
              </div>
            </div>

            {/* Search */}
            <div className="flex-1 max-w-2xl relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={16} />
              <Input
                type="text"
                placeholder="بحث عن أمر... (مثال: ospf, vlan, nat, hsrp)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-9 pl-4 h-10 text-sm"
                dir="rtl"
              />
              {searchQuery && searchResults.length > 0 && (
                <div className="absolute top-full mt-2 w-full max-h-96 overflow-y-auto bg-popover border border-border rounded-lg shadow-xl z-50">
                  {searchResults.slice(0, 20).map((result, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        scrollToSection(result.sectionId);
                        setSearchQuery('');
                      }}
                      className="w-full text-right p-3 hover:bg-accent transition border-b border-border/30 last:border-0"
                    >
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <code className="text-[12px] text-[#049fd9] font-mono" dir="ltr">
                          {result.command}
                        </code>
                        <Badge variant="outline" className="text-[10px] font-normal">
                          {result.sectionTitle}
                        </Badge>
                      </div>
                      <div className="text-xs text-muted-foreground line-clamp-1">
                        {result.explanation}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Dark mode toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsDark(!isDark)}
              className="h-10 w-10"
              aria-label="Toggle dark mode"
            >
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={cn(
            "fixed lg:sticky top-16 right-0 z-40 h-[calc(100vh-4rem)] w-72 shrink-0 overflow-y-auto bg-sidebar border-l border-sidebar-border transition-transform duration-300",
            sidebarOpen ? "translate-x-0" : "translate-x-full lg:translate-x-0"
          )}
        >
          <nav className="p-4 space-y-1">
            <div className="mb-3 px-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                الأقسام (27)
              </h3>
            </div>
            {ALL_SECTIONS.map(section => {
              const Icon = ICON_MAP[section.icon] || BookOpen;
              const isActive = activeSectionId === section.id;
              return (
                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={cn(
                    "w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm transition text-right",
                    isActive
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "hover:bg-sidebar-accent text-sidebar-foreground"
                  )}
                >
                  <Icon className="h-4 w-4 shrink-0" />
                  <span className="text-[12px] text-muted-foreground font-mono">
                    {section.chapter}
                  </span>
                  <span className="flex-1 text-[12.5px] font-medium leading-tight">
                    {section.titleAr}
                  </span>
                </button>
              );
            })}
          </nav>
        </aside>

        {/* Backdrop for mobile sidebar */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main content */}
        <main className="flex-1 min-w-0">
          {/* Hero Section */}
          <section className="relative overflow-hidden bg-gradient-to-br from-[#002b5c] via-[#001a3d] to-[#049fd9] text-white">
            <div className="absolute inset-0 opacity-10">
              <div className="absolute top-10 right-10 w-64 h-64 rounded-full bg-cyan-300 blur-3xl" />
              <div className="absolute bottom-10 left-10 w-80 h-80 rounded-full bg-blue-500 blur-3xl" />
            </div>
            <div className="container mx-auto max-w-6xl px-6 py-16 relative z-10">
              <div className="flex items-center gap-2 mb-4">
                <Badge className="bg-cyan-500/20 border-cyan-400/40 text-cyan-200 hover:bg-cyan-500/30">
                  CCNA 200-301 &amp; CCNP ENARSI
                </Badge>
                <Badge variant="outline" className="border-white/30 text-white hover:bg-white/10">
                  27 قسماً
                </Badge>
                <Badge variant="outline" className="border-white/30 text-white hover:bg-white/10">
                  200+ أمر
                </Badge>
              </div>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-black mb-4 leading-tight">
                مذكرة أوامر سيسكو الشاملة
              </h1>
              <p className="text-lg md:text-xl text-cyan-100 mb-2 font-mono" dir="ltr">
                Cisco IOS Commands Complete Reference
              </p>
              <p className="text-base md:text-lg text-blue-100/80 max-w-3xl leading-relaxed">
                مرجع تفاعلي شامل لأوامر Cisco IOS مع بحث فوري، شرح عربي مفصل، أمثلة عملية،
                ونصائح للمذاكرة والامتحان. يغطي CCNA 200-301 بالكامل و مواضيع متقدمة من CCNP ENARSI.
              </p>
              <div className="flex flex-wrap gap-3 mt-8">
                <Button
                  onClick={() => scrollToSection(1)}
                  className="bg-cyan-500 hover:bg-cyan-600 text-white"
                >
                  <BookOpen className="h-4 w-4 ml-2" />
                  ابدأ من البداية
                </Button>
                <Button
                  onClick={() => scrollToSection(25)}
                  variant="outline"
                  className="border-white/30 text-white hover:bg-white/10"
                >
                  <ListChecks className="h-4 w-4 ml-2" />
                  Cheat Sheet السريع
                </Button>
                <Button
                  onClick={() => scrollToSection(24)}
                  variant="outline"
                  className="border-white/30 text-white hover:bg-white/10"
                >
                  <FlaskConical className="h-4 w-4 ml-2" />
                  سيناريوهات عملية
                </Button>
              </div>

              {/* Quick stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
                {[
                  { label: 'قسم رئيسي', value: '27', icon: BookOpen },
                  { label: 'أمر Cisco', value: '200+', icon: Terminal },
                  { label: 'جدول مرجعي', value: '50+', icon: Grid3x3 },
                  { label: 'سيناريو عملي', value: '6', icon: FlaskConical },
                ].map((stat, i) => {
                  const Icon = stat.icon;
                  return (
                    <div key={i} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-4">
                      <Icon className="h-6 w-6 mb-2 text-cyan-300" />
                      <div className="text-3xl font-black">{stat.value}</div>
                      <div className="text-xs text-blue-100/80">{stat.label}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>

          {/* Sections */}
          <div className="container mx-auto max-w-6xl px-4 md:px-6 py-10">
            {ALL_SECTIONS.map(section => (
              <SectionRenderer
                key={section.id}
                section={section}
                copiedCmd={copiedCmd}
                onCopy={copyToClipboard}
              />
            ))}
          </div>

          {/* Footer */}
          <footer className="border-t border-border bg-muted/30 mt-12">
            <div className="container mx-auto max-w-6xl px-6 py-8">
              <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-[#002b5c] to-[#049fd9] text-white">
                    <TerminalSquare size={16} />
                  </div>
                  <div>
                    <div className="text-sm font-bold">مذكرة أوامر سيسكو الشاملة</div>
                    <div className="text-xs text-muted-foreground">Cisco IOS Commands Reference</div>
                  </div>
                </div>
                <div className="text-xs text-muted-foreground text-center">
                  © 2026 Z.ai Network Engineering &middot; CCNA 200-301 &amp; CCNP ENARSI Coverage
                </div>
                <div className="flex gap-2">
                  <Badge variant="outline" className="text-[10px]">CCNA</Badge>
                  <Badge variant="outline" className="text-[10px]">CCNP</Badge>
                  <Badge variant="outline" className="text-[10px]">CCIE</Badge>
                </div>
              </div>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
}

// ===================== Section Renderer =====================
function SectionRenderer({
  section,
  copiedCmd,
  onCopy,
}: {
  section: Section;
  copiedCmd: string | null;
  onCopy: (text: string, id: string) => void;
}) {
  const Icon = ICON_MAP[section.icon] || BookOpen;
  return (
    <section
      id={`section-${section.id}`}
      className="mb-16 scroll-mt-20"
    >
      {/* Section Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-[#002b5c] to-[#049fd9] text-white shadow-md">
            <Icon className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-baseline gap-2">
              <span className="text-[10px] font-mono text-muted-foreground">CHAPTER {section.chapter}</span>
              <Badge variant="outline" className="text-[10px]">{section.id} / 27</Badge>
            </div>
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mt-1">
              {section.titleAr}
            </h2>
            <div className="text-sm text-[#049fd9] font-mono mt-0.5" dir="ltr">
              {section.titleEn}
            </div>
          </div>
        </div>
        <div className="h-px bg-gradient-to-l from-[#049fd9] via-[#049fd9]/40 to-transparent" />
        <p className="text-[14px] text-muted-foreground leading-relaxed mt-3 max-w-4xl">
          {section.intro}
        </p>
      </div>

      {/* Subsections */}
      <div className="space-y-8">
        {section.subsections.map((sub, idx) => (
          <SubSectionRenderer
            key={idx}
            subsection={sub}
            sectionId={section.id}
            subIdx={idx}
            copiedCmd={copiedCmd}
            onCopy={onCopy}
          />
        ))}
      </div>
    </section>
  );
}

// ===================== Subsection Renderer =====================
function SubSectionRenderer({
  subsection,
  sectionId,
  subIdx,
  copiedCmd,
  onCopy,
}: {
  subsection: SubSection;
  sectionId: number;
  subIdx: number;
  copiedCmd: string | null;
  onCopy: (text: string, id: string) => void;
}) {
  return (
    <div className="bg-card border border-border rounded-xl overflow-hidden">
      {/* Subsection Title */}
      <div className="border-r-4 border-[#049fd9] pl-4 pr-3 py-2.5 bg-muted/30">
        <h3 className="text-base font-bold text-foreground">
          {subsection.title}
        </h3>
      </div>

      <div className="p-4 md:p-5">
        {/* Body Text */}
        {subsection.bodyText && (
          <p className="text-[13.5px] text-foreground leading-relaxed mb-4 text-justify">
            {subsection.bodyText}
          </p>
        )}

        {/* Table */}
        {subsection.table && (
          <div className="mb-4 overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-[12px]">
              <thead>
                <tr className="bg-[#002b5c] text-white">
                  {subsection.table.headers.map((h, i) => (
                    <th key={i} className="px-3 py-2 text-right font-semibold border-b border-[#049fd9]/40">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {subsection.table.rows.map((row, ri) => (
                  <tr key={ri} className={ri % 2 === 0 ? 'bg-card' : 'bg-muted/20'}>
                    {row.map((cell, ci) => (
                      <td key={ci} className="px-3 py-2 border-b border-border/40 align-top">
                        {cell.includes('←') || /^[a-z0-9].*[a-z0-9]$/i.test(cell) ? (
                          <span dir="ltr" className="font-mono text-[11.5px] inline-block">
                            {cell}
                          </span>
                        ) : (
                          <span className="text-foreground/90">{cell}</span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* List */}
        {subsection.list && (
          <ol className="space-y-2 mb-4 pr-6 list-decimal">
            {subsection.list.map((item, i) => (
              <li key={i} className="text-[12.5px] text-foreground leading-relaxed">
                <span className="inline-block bg-[#049fd9]/10 text-[#049fd9] text-[10px] font-mono px-1.5 py-0.5 rounded ml-2 align-middle">
                  {i + 1}
                </span>
                {item}
              </li>
            ))}
          </ol>
        )}

        {/* Commands Table */}
        {subsection.commands && subsection.commands.length > 0 && (
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-[11.5px]">
              <thead>
                <tr className="bg-[#002b5c] text-white">
                  <th className="px-2 py-2 text-right font-semibold w-[28%]">الأمر (Command)</th>
                  <th className="px-2 py-2 text-right font-semibold w-[15%]">الوضع (Mode)</th>
                  <th className="px-2 py-2 text-right font-semibold w-[37%]">الشرح (Explanation)</th>
                  <th className="px-2 py-2 text-right font-semibold w-[20%]">مثال / العكس</th>
                </tr>
              </thead>
              <tbody>
                {subsection.commands.map((cmd, ci) => (
                  <CommandRow
                    key={ci}
                    cmd={cmd}
                    sectionId={sectionId}
                    subIdx={subIdx}
                    cmdIdx={ci}
                    copiedCmd={copiedCmd}
                    onCopy={onCopy}
                  />
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Tip / Warning / Info box */}
        {subsection.tip && (
          <TipBox tip={subsection.tip} />
        )}
      </div>
    </div>
  );
}

// ===================== Command Row =====================
function CommandRow({
  cmd,
  sectionId,
  subIdx,
  cmdIdx,
  copiedCmd,
  onCopy,
}: {
  cmd: Command;
  sectionId: number;
  subIdx: number;
  cmdIdx: number;
  copiedCmd: string | null;
  onCopy: (text: string, id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const copyId = `${sectionId}-${subIdx}-${cmdIdx}`;
  const isCopied = copiedCmd === copyId;
  const hasExample = cmd.example && cmd.example.trim().length > 0;

  return (
    <tr className="border-b border-border/40 last:border-0 hover:bg-muted/20 transition">
      {/* Command */}
      <td className="px-2 py-2 align-top">
        <div className="flex items-start gap-1.5">
          <button
            onClick={() => onCopy(cmd.command, copyId)}
            className="shrink-0 mt-0.5 text-muted-foreground hover:text-[#049fd9] transition"
            aria-label="Copy command"
            title="نسخ الأمر"
          >
            {isCopied ? <Check size={12} className="text-green-500" /> : <CopyIcon size={12} />}
          </button>
          <code
            dir="ltr"
            className="text-left font-mono text-[11px] text-[#b1272b] dark:text-[#ff6b6b] bg-red-50 dark:bg-red-950/20 px-1.5 py-0.5 rounded block break-all leading-relaxed"
          >
            {cmd.command}
          </code>
        </div>
      </td>

      {/* Mode */}
      <td className="px-2 py-2 align-top">
        <span dir="ltr" className="text-left font-mono text-[10.5px] text-[#049fd9] dark:text-[#00bceb] font-semibold whitespace-nowrap">
          {cmd.mode}
        </span>
      </td>

      {/* Explanation */}
      <td className="px-2 py-2 align-top">
        <p className="text-[12px] text-foreground/85 leading-relaxed">
          {cmd.explanation}
        </p>
      </td>

      {/* Example + no command */}
      <td className="px-2 py-2 align-top">
        {hasExample && (
          <div className="mb-1">
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-[10px] text-[#049fd9] hover:underline"
            >
              {expanded ? '− إخفاء المثال' : '+ عرض المثال'}
            </button>
            {expanded && (
              <pre
                dir="ltr"
                className="mt-1 text-left font-mono text-[10px] bg-muted dark:bg-muted/40 px-2 py-1.5 rounded border border-border overflow-x-auto whitespace-pre-wrap"
              >
                {cmd.example}
              </pre>
            )}
          </div>
        )}
        {cmd.noCommand && cmd.noCommand !== 'N/A' && (
          <div className="text-[10px] text-muted-foreground italic font-mono" dir="ltr">
            <span className="text-[10px]">↩ no:</span> {cmd.noCommand}
          </div>
        )}
      </td>
    </tr>
  );
}

// ===================== Tip Box =====================
function TipBox({ tip }: { tip: NonNullable<SubSection['tip']> }) {
  const config = {
    tip: {
      bg: 'bg-amber-50 dark:bg-amber-950/20',
      border: 'border-amber-300 dark:border-amber-700',
      iconBg: 'bg-amber-500',
      title: 'text-amber-700 dark:text-amber-400',
      body: 'text-amber-900 dark:text-amber-200',
      Icon: Lightbulb,
      label: 'نصيحة',
    },
    warn: {
      bg: 'bg-red-50 dark:bg-red-950/20',
      border: 'border-red-400 dark:border-red-700',
      iconBg: 'bg-red-500',
      title: 'text-red-700 dark:text-red-400',
      body: 'text-red-900 dark:text-red-200',
      Icon: AlertTriangle,
      label: 'تحذير',
    },
    info: {
      bg: 'bg-cyan-50 dark:bg-cyan-950/20',
      border: 'border-cyan-400 dark:border-cyan-700',
      iconBg: 'bg-cyan-500',
      title: 'text-cyan-700 dark:text-cyan-400',
      body: 'text-cyan-900 dark:text-cyan-200',
      Icon: Info,
      label: 'معلومة',
    },
  };
  const type = tip.type || 'tip';
  const c = config[type];
  const Icon = c.Icon;

  return (
    <div className={`mt-4 rounded-lg border-r-4 ${c.bg} ${c.border} p-3.5`}>
      <div className="flex gap-3">
        <div className={`shrink-0 flex h-6 w-6 items-center justify-center rounded-full ${c.iconBg} text-white`}>
          <Icon size={14} />
        </div>
        <div className="flex-1 min-w-0">
          <div className={`text-[12.5px] font-bold mb-1 ${c.title}`}>
            {tip.title}
          </div>
          <div className={`text-[12.5px] leading-relaxed ${c.body}`}>
            {tip.body}
          </div>
        </div>
      </div>
    </div>
  );
}
