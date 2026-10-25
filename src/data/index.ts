// Index file - combines all section data
import { SECTIONS } from './cisco-data';
import { SECTIONS_5_TO_9 } from './cisco-data-part2';
import { SECTIONS_10_TO_15 } from './cisco-data-part3';
import { SECTIONS_16_TO_22 } from './cisco-data-part4';
import { SECTIONS_23_TO_27 } from './cisco-data-part5';

export type { Section, SubSection, Command } from './cisco-data';

export const ALL_SECTIONS = [
  ...SECTIONS,
  ...SECTIONS_5_TO_9,
  ...SECTIONS_10_TO_15,
  ...SECTIONS_16_TO_22,
  ...SECTIONS_23_TO_27,
];

// Build searchable index of all commands
export interface SearchIndexEntry {
  sectionId: number;
  sectionTitle: string;
  command: string;
  mode: string;
  explanation: string;
}

export const SEARCH_INDEX: SearchIndexEntry[] = ALL_SECTIONS.flatMap(section => {
  const entries: SearchIndexEntry[] = [];
  section.subsections.forEach(sub => {
    if (sub.commands) {
      sub.commands.forEach(cmd => {
        entries.push({
          sectionId: section.id,
          sectionTitle: section.titleAr,
          command: cmd.command,
          mode: cmd.mode,
          explanation: cmd.explanation,
        });
      });
    }
  });
  return entries;
});

export const SECTIONS_BY_ID = ALL_SECTIONS.reduce((acc, s) => {
  acc[s.id] = s;
  return acc;
}, {} as Record<number, typeof ALL_SECTIONS[0]>);
