'use client';

import { useState, useMemo, useEffect, useCallback } from 'react';
import { FLASHCARDS, FLASHCARD_CATEGORIES } from '@/data/flashcards';
import {
  RotateCcw,
  ChevronLeft,
  ChevronRight,
  Shuffle,
  Eye,
  EyeOff,
  Layers,
  Check,
  Brain,
  RefreshCw,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';

const STORAGE_KEY = 'cisco-flashcards-progress';

export function Flashcards() {
  const [activeCategory, setActiveCategory] = useState<'all' | keyof typeof FLASHCARD_CATEGORIES>('all');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [learned, setLearned] = useState<Set<string>>(() => {
    if (typeof window === 'undefined') return new Set();
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return new Set(stored ? JSON.parse(stored) : []);
    } catch { return new Set(); }
  });
  const [shuffled, setShuffled] = useState(false);

  // Filter cards
  const filteredCards = useMemo(() => {
    const cards = activeCategory === 'all'
      ? FLASHCARDS
      : FLASHCARDS.filter(c => c.category === activeCategory);
    return cards;
  }, [activeCategory]);

  // Compute order based on shuffled flag (derived state, no effect needed)
  const order = useMemo(() => {
    const indices = filteredCards.map((_, i) => i);
    if (shuffled) {
      // Shuffle based on a seed that changes when shuffle is toggled on
      // Use a simple deterministic shuffle when shuffled=true
      for (let i = indices.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [indices[i], indices[j]] = [indices[j], indices[i]];
      }
    }
    return indices;
  }, [filteredCards, shuffled]);

  const currentCard = filteredCards[order[currentIndex]];

  // Reset index when category/shuffled changes (in callback, not effect)
  const handleCategoryChange = (cat: 'all' | keyof typeof FLASHCARD_CATEGORIES) => {
    setActiveCategory(cat);
    setCurrentIndex(0);
    setFlipped(false);
  };

  const toggleShuffle = () => {
    setShuffled(!shuffled);
    setCurrentIndex(0);
    setFlipped(false);
  };

  // Save learned
  useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(learned)));
  }, [learned]);

  const goNext = useCallback(() => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex(prev => Math.min(prev + 1, filteredCards.length - 1));
    }, 150);
  }, [filteredCards.length]);

  const goPrev = useCallback(() => {
    setFlipped(false);
    setTimeout(() => {
      setCurrentIndex(prev => Math.max(prev - 1, 0));
    }, 150);
  }, []);

  const toggleLearned = useCallback(() => {
    if (!currentCard) return;
    setLearned(prev => {
      const newSet = new Set(prev);
      if (newSet.has(currentCard.id)) {
        newSet.delete(currentCard.id);
      } else {
        newSet.add(currentCard.id);
      }
      return newSet;
    });
  }, [currentCard]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === 'ArrowRight') goPrev(); // RTL: right arrow = previous
      else if (e.key === 'ArrowLeft') goNext(); // RTL: left arrow = next
      else if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        setFlipped(f => !f);
      } else if (e.key === 'l' || e.key === 'L') toggleLearned();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [goNext, goPrev, toggleLearned]);

  if (!currentCard) {
    return <div className="text-center py-12 text-muted-foreground">لا توجد بطاقات</div>;
  }

  const cat = FLASHCARD_CATEGORIES[currentCard.category];
  const isLearned = learned.has(currentCard.id);
  const learnedInCategory = filteredCards.filter(c => learned.has(c.id)).length;
  const progress = filteredCards.length > 0 ? Math.round((learnedInCategory / filteredCards.length) * 100) : 0;

  return (
    <div className="space-y-5">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatBox label="إجمالي البطاقات" value={FLASHCARDS.length} />
        <StatBox label="في الفئة الحالية" value={filteredCards.length} />
        <StatBox label="مفهومة" value={learned.size} />
        <StatBox label="التقدم" value={`${progress}%`} />
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2">
        <CategoryButton
          active={activeCategory === 'all'}
          onClick={() => handleCategoryChange('all')}
          label="الكل"
          count={FLASHCARDS.length}
        />
        {Object.entries(FLASHCARD_CATEGORIES).map(([key, info]) => {
          const count = FLASHCARDS.filter(c => c.category === key).length;
          return (
            <CategoryButton
              key={key}
              active={activeCategory === key}
              onClick={() => handleCategoryChange(key as keyof typeof FLASHCARD_CATEGORIES)}
              label={info.label}
              count={count}
              color={info.color}
            />
          );
        })}
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex gap-2">
          <Button
            variant={shuffled ? 'default' : 'outline'}
            size="sm"
            onClick={toggleShuffle}
            className="text-xs"
          >
            <Shuffle className="h-3 w-3 ml-1" />
            {shuffled ? 'مرتب عشوائياً' : 'ترتيب عشوائي'}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => { setLearned(new Set()); localStorage.removeItem(STORAGE_KEY); }}
            className="text-xs"
          >
            <RefreshCw className="h-3 w-3 ml-1" />
            إعادة تعيين
          </Button>
        </div>
        <div className="text-xs text-muted-foreground" dir="ltr">
          {currentIndex + 1} / {filteredCards.length}
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-[#049fd9] to-[#00bceb] transition-all"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Flashcard */}
      <div className="relative" style={{ perspective: '1500px' }}>
        <div
          className={cn(
            'relative w-full transition-transform duration-500 cursor-pointer',
            flipped && 'transform rotate-y-180'
          )}
          style={{
            transformStyle: 'preserve-3d',
            transform: flipped ? 'rotateY(180deg)' : 'rotateY(0)',
            minHeight: '280px',
          }}
          onClick={() => setFlipped(!flipped)}
        >
          {/* Front */}
          <div
            className="absolute inset-0 bg-card border-2 border-border rounded-2xl p-6 flex flex-col items-center justify-center text-center"
            style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}
          >
            <div className="flex items-center gap-2 mb-4">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: cat.color }}
              />
              <Badge variant="outline" className="text-[10px]">{cat.label}</Badge>
              {isLearned && (
                <Badge className="text-[10px] bg-green-500/20 text-green-700 dark:text-green-300">
                  <Check className="h-2.5 w-2.5 ml-1" />
                  مفهومة
                </Badge>
              )}
            </div>
            <div className="text-xs text-muted-foreground mb-3 flex items-center gap-1.5">
              <Brain className="h-3.5 w-3.5" />
              السؤال
            </div>
            <h3 className="text-2xl md:text-3xl font-bold mb-4 text-foreground" dir="ltr">
              {currentCard.front}
            </h3>
            <div className="text-xs text-muted-foreground/70 mt-auto">
              انقر للقلب · أو اضغط مسافة · <kbd className="px-1 py-0.5 bg-muted rounded">Space</kbd>
            </div>
          </div>

          {/* Back */}
          <div
            className="absolute inset-0 bg-gradient-to-br from-[#002b5c] to-[#049fd9] text-white border-2 border-[#049fd9] rounded-2xl p-6 flex flex-col items-center justify-center text-center"
            style={{
              backfaceVisibility: 'hidden',
              WebkitBackfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
            }}
          >
            <div className="text-xs text-cyan-200 mb-3 flex items-center gap-1.5">
              <Eye className="h-3.5 w-3.5" />
              الإجابة
            </div>
            <p className="text-base md:text-lg leading-relaxed mb-3" dir="ltr">
              {currentCard.back}
            </p>
            {currentCard.example && (
              <div className="text-xs text-cyan-100 bg-white/10 rounded px-3 py-1.5 mt-2" dir="ltr">
                {currentCard.example}
              </div>
            )}
            <div className="text-xs text-cyan-200/70 mt-auto">
              انقر للعودة · أو اضغط مسافة
            </div>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex items-center justify-between gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={goPrev}
          disabled={currentIndex === 0}
          className="text-xs"
        >
          <ChevronRight className="h-4 w-4 ml-1" />
          السابق
        </Button>
        <div className="flex gap-2">
          <Button
            variant={isLearned ? 'default' : 'outline'}
            size="sm"
            onClick={toggleLearned}
            className="text-xs"
          >
            <Check className="h-3 w-3 ml-1" />
            {isLearned ? 'مفهومة' : 'علّم كمفهوم'}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setFlipped(!flipped)}
            className="text-xs"
          >
            {flipped ? <EyeOff className="h-3 w-3 ml-1" /> : <Eye className="h-3 w-3 ml-1" />}
            {flipped ? 'إخفاء' : 'اقلب'}
          </Button>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={goNext}
          disabled={currentIndex === filteredCards.length - 1}
          className="text-xs"
        >
          التالي
          <ChevronLeft className="h-4 w-4 mr-1" />
        </Button>
      </div>

      {/* Keyboard hint */}
      <div className="text-center text-xs text-muted-foreground">
        اختصارات: <kbd className="px-1.5 py-0.5 bg-muted rounded font-mono">←</kbd> التالي ·
        <kbd className="px-1.5 py-0.5 bg-muted rounded font-mono ml-1">→</kbd> السابق ·
        <kbd className="px-1.5 py-0.5 bg-muted rounded font-mono ml-1">Space</kbd> اقلب ·
        <kbd className="px-1.5 py-0.5 bg-muted rounded font-mono ml-1">L</kbd> علّم كمفهوم
      </div>
    </div>
  );
}

function StatBox({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-muted/30 rounded-lg p-3 text-center">
      <div className="text-xl md:text-2xl font-black text-[#049fd9]" dir="ltr">{value}</div>
      <div className="text-xs text-muted-foreground">{label}</div>
    </div>
  );
}

function CategoryButton({
  active,
  onClick,
  label,
  count,
  color,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  count: number;
  color?: string;
}) {
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
      {color && <span className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />}
      {label}
      <span className="text-[10px] opacity-70">({count})</span>
    </button>
  );
}
