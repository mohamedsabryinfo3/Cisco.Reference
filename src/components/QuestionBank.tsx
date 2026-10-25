'use client';

import { useState, useMemo, useEffect } from 'react';
import { ALL_QUESTIONS, CATEGORY_INFO, TOPICS_BY_CATEGORY, QUESTION_STATS } from '@/data/questions-index';
import type { Question } from '@/data/questions-index';
import {
  Search,
  GraduationCap,
  Briefcase,
  Users,
  Filter,
  ChevronDown,
  ChevronUp,
  Eye,
  EyeOff,
  Star,
  CheckCircle2,
  X,
  RefreshCw,
  BookOpen,
  Brain,
  Target,
  Lightbulb,
  Award,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

const CATEGORY_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  GraduationCap,
  Briefcase,
  Users,
};

const DIFFICULTY_CONFIG = {
  easy: { label: 'سهل', color: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300', dot: 'bg-green-500' },
  medium: { label: 'متوسط', color: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300', dot: 'bg-amber-500' },
  hard: { label: 'صعب', color: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300', dot: 'bg-red-500' },
};

const STORAGE_KEY = 'cisco-qb-progress';
const FAV_KEY = 'cisco-qb-favorites';

// Lazy initializer for localStorage-backed Set state
function initFromStorage(key: string): Set<string> {
  if (typeof window === 'undefined') return new Set();
  try {
    const stored = localStorage.getItem(key);
    return new Set(stored ? JSON.parse(stored) : []);
  } catch {
    return new Set();
  }
}

export function QuestionBank() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState<'all' | 'ccna' | 'ccnp' | 'interview'>('all');
  const [activeTopic, setActiveTopic] = useState<string>('all');
  const [activeDifficulty, setActiveDifficulty] = useState<'all' | 'easy' | 'medium' | 'hard'>('all');
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});
  const [learnedQuestions, setLearnedQuestions] = useState<Set<string>>(() => initFromStorage(STORAGE_KEY));
  const [favorites, setFavorites] = useState<Set<string>>(() => initFromStorage(FAV_KEY));
  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false);
  const [showOnlyNotLearned, setShowOnlyNotLearned] = useState(false);

  // Save learned questions (external sync)
  useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(learnedQuestions)));
  }, [learnedQuestions]);

  // Save favorites (external sync)
  useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(FAV_KEY, JSON.stringify(Array.from(favorites)));
  }, [favorites]);

  // Handle category change and reset topic in the click handler (no effect needed)
  const handleCategoryChange = (cat: 'all' | 'ccna' | 'ccnp' | 'interview') => {
    setActiveCategory(cat);
    setActiveTopic('all');
  };

  // Filtered questions
  const filteredQuestions = useMemo(() => {
    return ALL_QUESTIONS.filter(q => {
      // Search
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const matches =
          q.question.toLowerCase().includes(query) ||
          q.answer.toLowerCase().includes(query) ||
          (q.explanation || '').toLowerCase().includes(query) ||
          q.topic.toLowerCase().includes(query) ||
          (q.tags || []).some(t => t.toLowerCase().includes(query));
        if (!matches) return false;
      }
      // Category
      if (activeCategory !== 'all' && q.category !== activeCategory) return false;
      // Topic
      if (activeTopic !== 'all' && q.topic !== activeTopic) return false;
      // Difficulty
      if (activeDifficulty !== 'all' && q.difficulty !== activeDifficulty) return false;
      // Favorites filter
      if (showOnlyFavorites && !favorites.has(q.id)) return false;
      // Not learned filter
      if (showOnlyNotLearned && learnedQuestions.has(q.id)) return false;
      return true;
    });
  }, [searchQuery, activeCategory, activeTopic, activeDifficulty, showOnlyFavorites, showOnlyNotLearned, favorites, learnedQuestions]);

  // Available topics based on active category
  const availableTopics = useMemo(() => {
    if (activeCategory === 'all') {
      return Array.from(new Set(ALL_QUESTIONS.map(q => q.topic))).sort();
    }
    return TOPICS_BY_CATEGORY[activeCategory] || [];
  }, [activeCategory]);

  // Stats for current filter
  const filterStats = useMemo(() => {
    const learned = filteredQuestions.filter(q => learnedQuestions.has(q.id)).length;
    const total = filteredQuestions.length;
    const percent = total > 0 ? Math.round((learned / total) * 100) : 0;
    return { learned, total, percent };
  }, [filteredQuestions, learnedQuestions]);

  const toggleAnswer = (id: string) => {
    setShowAnswers(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleLearned = (id: string) => {
    setLearnedQuestions(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const toggleFavorite = (id: string) => {
    setFavorites(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const toggleAllAnswers = (show: boolean) => {
    const newState: Record<string, boolean> = {};
    if (show) {
      filteredQuestions.forEach(q => { newState[q.id] = true; });
    }
    setShowAnswers(newState);
  };

  const resetProgress = () => {
    if (confirm('هل أنت متأكد من إعادة تعيين كل التقدم؟ سيتم مسح كل الأسئلة المعلّمة والمفضلة.')) {
      setLearnedQuestions(new Set());
      setFavorites(new Set());
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(FAV_KEY);
    }
  };

  return (
    <div className="space-y-6">
      {/* Stats Dashboard */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatCard
          icon={<BookOpen className="h-5 w-5" />}
          label="إجمالي الأسئلة"
          value={QUESTION_STATS.total}
          color="from-blue-500 to-cyan-500"
        />
        <StatCard
          icon={<GraduationCap className="h-5 w-5" />}
          label="أسئلة CCNA"
          value={QUESTION_STATS.ccna}
          color="from-cyan-500 to-blue-600"
        />
        <StatCard
          icon={<Briefcase className="h-5 w-5" />}
          label="أسئلة CCNP"
          value={QUESTION_STATS.ccnp}
          color="from-blue-700 to-blue-900"
        />
        <StatCard
          icon={<Users className="h-5 w-5" />}
          label="أسئلة المقابلات"
          value={QUESTION_STATS.interview}
          color="from-cyan-400 to-teal-500"
        />
      </div>

      {/* Progress Card */}
      <Card className="border-[#049fd9]/30 bg-gradient-to-br from-[#049fd9]/5 to-transparent">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center justify-between text-base">
            <div className="flex items-center gap-2">
              <Target className="h-5 w-5 text-[#049fd9]" />
              <span>تقدمك في المراجعة</span>
            </div>
            <Button variant="ghost" size="sm" onClick={resetProgress} className="text-xs">
              <RefreshCw className="h-3 w-3 ml-1" />
              إعادة تعيين
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">
                الأسئلة المعلمة كمفهومة: {filterStats.learned} من {filterStats.total}
              </span>
              <span className="font-bold text-[#049fd9]">{filterStats.percent}%</span>
            </div>
            <div className="h-3 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#049fd9] to-[#00bceb] transition-all duration-500"
                style={{ width: `${filterStats.percent}%` }}
              />
            </div>
            <div className="text-xs text-muted-foreground text-center">
              {filterStats.percent === 100
                ? '🎉 ممتاز! اكتملت المراجعة - أنت جاهز للامتحان!'
                : filterStats.percent >= 75
                ? '⭐ تقدم رائع! واصل المراجعة'
                : filterStats.percent >= 50
                ? '💪 منتصف الطريق - واصل!'
                : '📚 ابدأ المراجعة - علّم الأسئلة التي فهمتها'}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-5 space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
            <Input
              type="text"
              placeholder="ابحث في الأسئلة... (مثال: OSPF, BGP, subnetting, ARP)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pr-10 pl-4 h-11 text-sm"
              dir="rtl"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X size={16} />
              </button>
            )}
          </div>

          {/* Category Tabs */}
          <div>
            <label className="text-xs font-semibold text-muted-foreground mb-2 block">الفئة:</label>
            <div className="flex flex-wrap gap-2">
              <CategoryTab
                active={activeCategory === 'all'}
                onClick={() => handleCategoryChange('all')}
                label="الكل"
                count={ALL_QUESTIONS.length}
              />
              {Object.entries(CATEGORY_INFO).map(([key, info]) => {
                const Icon = CATEGORY_ICONS[info.icon] || BookOpen;
                const count = QUESTION_STATS[key as keyof typeof QUESTION_STATS];
                return (
                  <CategoryTab
                    key={key}
                    active={activeCategory === key}
                    onClick={() => handleCategoryChange(key as 'ccna' | 'ccnp' | 'interview')}
                    label={info.labelAr}
                    icon={<Icon className="h-4 w-4" />}
                    count={count}
                  />
                );
              })}
            </div>
          </div>

          {/* Topic Filter */}
          <div>
            <label className="text-xs font-semibold text-muted-foreground mb-2 block">الموضوع:</label>
            <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
              <CategoryTab
                active={activeTopic === 'all'}
                onClick={() => setActiveTopic('all')}
                label="كل المواضيع"
                count={activeCategory === 'all' ? ALL_QUESTIONS.length : QUESTION_STATS[activeCategory as keyof typeof QUESTION_STATS]}
              />
              {availableTopics.map(topic => {
                const count = ALL_QUESTIONS.filter(q =>
                  (activeCategory === 'all' || q.category === activeCategory) &&
                  q.topic === topic
                ).length;
                return (
                  <CategoryTab
                    key={topic}
                    active={activeTopic === topic}
                    onClick={() => setActiveTopic(topic)}
                    label={topic}
                    count={count}
                    small
                  />
                );
              })}
            </div>
          </div>

          {/* Difficulty + Quick Filters */}
          <div className="flex flex-wrap items-center gap-3">
            <div>
              <label className="text-xs font-semibold text-muted-foreground mb-2 block">المستوى:</label>
              <div className="flex gap-2">
                <CategoryTab
                  active={activeDifficulty === 'all'}
                  onClick={() => setActiveDifficulty('all')}
                  label="الكل"
                  small
                />
                {(['easy', 'medium', 'hard'] as const).map(d => (
                  <CategoryTab
                    key={d}
                    active={activeDifficulty === d}
                    onClick={() => setActiveDifficulty(d)}
                    label={DIFFICULTY_CONFIG[d].label}
                    small
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Quick Toggles */}
          <div className="flex flex-wrap gap-2 pt-2 border-t border-border">
            <Button
              variant={showOnlyFavorites ? 'default' : 'outline'}
              size="sm"
              onClick={() => setShowOnlyFavorites(!showOnlyFavorites)}
              className="text-xs"
            >
              <Star className={`h-3 w-3 ml-1 ${showOnlyFavorites ? 'fill-current' : ''}`} />
              المفضلة فقط ({favorites.size})
            </Button>
            <Button
              variant={showOnlyNotLearned ? 'default' : 'outline'}
              size="sm"
              onClick={() => setShowOnlyNotLearned(!showOnlyNotLearned)}
              className="text-xs"
            >
              <Brain className="h-3 w-3 ml-1" />
              غير المفهومة فقط
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => toggleAllAnswers(true)}
              className="text-xs"
            >
              <Eye className="h-3 w-3 ml-1" />
              عرض كل الإجابات
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => toggleAllAnswers(false)}
              className="text-xs"
            >
              <EyeOff className="h-3 w-3 ml-1" />
              إخفاء كل الإجابات
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results count */}
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>
          عرض <span className="font-bold text-foreground">{filteredQuestions.length}</span> سؤال
        </span>
        {filteredQuestions.length > 0 && (
          <span className="text-xs">
            المعلم: {filterStats.learned} / المتبقي: {filterStats.total - filterStats.learned}
          </span>
        )}
      </div>

      {/* Questions List */}
      {filteredQuestions.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="py-12 text-center">
            <Search className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-muted-foreground">لا توجد أسئلة مطابقة لمعايير البحث</p>
            <Button
              variant="outline"
              size="sm"
              className="mt-3"
              onClick={() => {
                setSearchQuery('');
                handleCategoryChange('all');
                setActiveTopic('all');
                setActiveDifficulty('all');
                setShowOnlyFavorites(false);
                setShowOnlyNotLearned(false);
              }}
            >
              <RefreshCw className="h-3 w-3 ml-1" />
              مسح الفلاتر
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredQuestions.map((q, idx) => (
            <QuestionCard
              key={q.id}
              question={q}
              index={idx + 1}
              showAnswer={showAnswers[q.id] || false}
              isLearned={learnedQuestions.has(q.id)}
              isFavorite={favorites.has(q.id)}
              onToggleAnswer={() => toggleAnswer(q.id)}
              onToggleLearned={() => toggleLearned(q.id)}
              onToggleFavorite={() => toggleFavorite(q.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// ===================== Stat Card =====================
function StatCard({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  color: string;
}) {
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

// ===================== Category Tab =====================
function CategoryTab({
  active,
  onClick,
  label,
  icon,
  count,
  small,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  icon?: React.ReactNode;
  count?: number;
  small?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full border transition-colors',
        small ? 'px-3 py-1 text-[11px]' : 'px-4 py-1.5 text-xs',
        active
          ? 'bg-[#049fd9] text-white border-[#049fd9] shadow-sm'
          : 'bg-background text-foreground border-border hover:border-[#049fd9]/50 hover:bg-[#049fd9]/5'
      )}
    >
      {icon}
      <span>{label}</span>
      {count !== undefined && (
        <span className={cn(
          'rounded-full px-1.5 py-0.5 text-[10px] font-mono',
          active ? 'bg-white/20' : 'bg-muted'
        )}>
          {count}
        </span>
      )}
    </button>
  );
}

// ===================== Question Card =====================
function QuestionCard({
  question,
  index,
  showAnswer,
  isLearned,
  isFavorite,
  onToggleAnswer,
  onToggleLearned,
  onToggleFavorite,
}: {
  question: Question;
  index: number;
  showAnswer: boolean;
  isLearned: boolean;
  isFavorite: boolean;
  onToggleAnswer: () => void;
  onToggleLearned: () => void;
  onToggleFavorite: () => void;
}) {
  const catInfo = CATEGORY_INFO[question.category];
  const diffConfig = DIFFICULTY_CONFIG[question.difficulty];
  const CatIcon = CATEGORY_ICONS[catInfo.icon] || BookOpen;

  return (
    <Card className={cn(
      'overflow-hidden transition-all',
      isLearned && 'border-green-500/30 bg-green-50/50 dark:bg-green-950/10',
      isFavorite && 'ring-2 ring-amber-400/40'
    )}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 flex-1 min-w-0">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#049fd9]/10 text-[#049fd9] text-xs font-bold font-mono">
              {index}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-2 mb-1.5">
                <Badge variant="outline" className="text-[10px] gap-1">
                  <CatIcon className="h-2.5 w-2.5" />
                  {catInfo.labelAr}
                </Badge>
                <Badge variant="secondary" className="text-[10px]">
                  {question.topic}
                </Badge>
                <Badge className={cn('text-[10px] gap-1', diffConfig.color)} variant="outline">
                  <span className={cn('h-1.5 w-1.5 rounded-full', diffConfig.dot)} />
                  {diffConfig.label}
                </Badge>
              </div>
              <p className="text-[14px] font-medium leading-relaxed text-foreground">
                {question.question}
              </p>
            </div>
          </div>
          {/* Action buttons */}
          <div className="flex items-center gap-1 shrink-0">
            <button
              onClick={onToggleFavorite}
              className={cn(
                'p-1.5 rounded-md transition',
                isFavorite ? 'text-amber-500' : 'text-muted-foreground hover:text-amber-500'
              )}
              title="إضافة للمفضلة"
            >
              <Star className={cn('h-4 w-4', isFavorite && 'fill-current')} />
            </button>
            <button
              onClick={onToggleLearned}
              className={cn(
                'p-1.5 rounded-md transition',
                isLearned ? 'text-green-600' : 'text-muted-foreground hover:text-green-600'
              )}
              title="علّم كمفهوم"
            >
              <CheckCircle2 className={cn('h-4 w-4', isLearned && 'fill-current/20')} />
            </button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        {/* Show Answer Button */}
        <Button
          variant={showAnswer ? 'secondary' : 'default'}
          size="sm"
          onClick={onToggleAnswer}
          className="text-xs"
        >
          {showAnswer ? (
            <>
              <ChevronUp className="h-3 w-3 ml-1" />
              إخفاء الإجابة
            </>
          ) : (
            <>
              <ChevronDown className="h-3 w-3 ml-1" />
              عرض الإجابة
            </>
          )}
        </Button>

        {/* Answer */}
        {showAnswer && (
          <div className="mt-3 space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
            <div className="rounded-lg bg-gradient-to-br from-[#049fd9]/5 to-transparent border border-[#049fd9]/20 p-3.5">
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb className="h-4 w-4 text-[#049fd9]" />
                <span className="text-xs font-bold text-[#049fd9]">الإجابة بالعربية</span>
              </div>
              <p className="text-[13px] leading-relaxed text-foreground/90">
                {question.answer}
              </p>
            </div>

            {question.explanation && (
              <div className="rounded-lg bg-muted/30 border border-border p-3">
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-[10px] font-mono text-muted-foreground">EN</span>
                  <span className="text-xs font-bold text-muted-foreground">English Explanation</span>
                </div>
                <p className="text-[12px] leading-relaxed text-muted-foreground" dir="ltr">
                  {question.explanation}
                </p>
              </div>
            )}

            {/* Tags */}
            {question.tags && question.tags.length > 0 && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {question.tags.map(tag => (
                  <span
                    key={tag}
                    className="text-[10px] px-2 py-0.5 rounded-full bg-muted text-muted-foreground"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
