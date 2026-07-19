'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import { ELEMENT_COLORS, ELEMENT_NAMES } from '@/lib/constants/elements';
import type { Element } from '@/types/saju';

interface YongshinCardProps {
  type: string; // 억부용신, 조후용신, 통관용신 등
  element: Element;
  hanja?: string;
  description?: string;
}

export function YongshinCard({ type, element, hanja, description }: YongshinCardProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleTitleClick = () => {
    const entry = getGlossaryEntry('용신');
    if (entry) {
      setSelectedEntry(entry);
      setIsModalOpen(true);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEntry(null);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35 }}
        className="mb-8"
      >
        <div className="flex items-center gap-2 mb-4">
          <Icon name="solar:star-bold" size={24} className="text-accent" />
          <button
            onClick={handleTitleClick}
            className="font-display text-xl text-foreground underline decoration-border/30 hover:decoration-accent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            용신
          </button>
        </div>

        <GlassCard className="p-4 md:p-6">
          <div className="flex flex-wrap gap-4">
            <div className="bg-surface border-[1.5px] border-border rounded-xl p-4 text-center min-w-[100px] shadow-block-sm">
              <div className="text-xs text-muted-foreground mb-2">{type}</div>
              <div className={`text-2xl font-bold ${ELEMENT_COLORS[element].text}`}>
                {element}({hanja || ELEMENT_NAMES[element].chinese})
              </div>
            </div>

            {description && (
              <div className="flex-1 min-w-[200px]">
                <p className="text-muted-foreground text-sm leading-relaxed">{description}</p>
              </div>
            )}
          </div>
        </GlassCard>
      </motion.div>

      <GlossaryModal
        entry={selectedEntry}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </>
  );
}

export default YongshinCard;
