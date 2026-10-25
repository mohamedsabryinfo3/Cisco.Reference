// Question Bank Index - combines all questions
import type { Question } from './questions-ccna';
import { CCNA_QUESTIONS } from './questions-ccna';
import { CCNP_QUESTIONS } from './questions-ccnp';
import { INTERVIEW_QUESTIONS } from './questions-interview';

export type { Question } from './questions-ccna';

export const ALL_QUESTIONS: Question[] = [
  ...CCNA_QUESTIONS,
  ...CCNP_QUESTIONS,
  ...INTERVIEW_QUESTIONS,
];

export const QUESTIONS_BY_CATEGORY = {
  ccna: CCNA_QUESTIONS,
  ccnp: CCNP_QUESTIONS,
  interview: INTERVIEW_QUESTIONS,
};

export const CATEGORY_INFO = {
  ccna: {
    label: 'CCNA 200-301',
    labelAr: 'امتحان CCNA',
    description: 'أسئلة امتحان CCNA - شهادة Cisco Certified Network Associate',
    color: '#049fd9',
    icon: 'GraduationCap',
  },
  ccnp: {
    label: 'CCNP ENARSI',
    labelAr: 'امتحان CCNP',
    description: 'أسئلة امتحان CCNP ENARSI - شهادة Cisco Certified Network Professional',
    color: '#002b5c',
    icon: 'Briefcase',
  },
  interview: {
    label: 'Interview Questions',
    labelAr: 'أسئلة المقابلات',
    description: 'أسئلة مقابلات مهندسي الشبكات - شاملة لكل المواضيع',
    color: '#00bceb',
    icon: 'Users',
  },
};

// Get all unique topics
export const ALL_TOPICS = Array.from(
  new Set(ALL_QUESTIONS.map(q => q.topic))
).sort();

// Get topics by category
export const TOPICS_BY_CATEGORY: Record<string, string[]> = {
  ccna: Array.from(new Set(CCNA_QUESTIONS.map(q => q.topic))).sort(),
  ccnp: Array.from(new Set(CCNP_QUESTIONS.map(q => q.topic))).sort(),
  interview: Array.from(new Set(INTERVIEW_QUESTIONS.map(q => q.topic))).sort(),
};

// Stats
export const QUESTION_STATS = {
  total: ALL_QUESTIONS.length,
  ccna: CCNA_QUESTIONS.length,
  ccnp: CCNP_QUESTIONS.length,
  interview: INTERVIEW_QUESTIONS.length,
  topics: ALL_TOPICS.length,
};
