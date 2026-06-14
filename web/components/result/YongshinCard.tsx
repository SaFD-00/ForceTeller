'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard, Icon, GlossaryModal } from '@/components/ui';
import { getGlossaryEntry, type GlossaryEntry } from '@/data/saju-glossary';
import type { Element } from '@/types/saju';

interface YongshinCardProps {
  type: string; // 억부용신, 조후용신, 통관용신 등
  element: Element;
  hanja?: string;
  description?: string;
}

// 오행별 색상 및 한자
const ELEMENT_INFO: Record<Element, { hanja: string; bg: string; text: string }> = {
  '목': { hanja: '木', bg: 'bg-green-500/20', text: 'text-green-400' },
  '화': { hanja: '火', bg: 'bg-red-500/20', text: 'text-red-400' },
  '토': { hanja: '土', bg: 'bg-yellow-500/20', text: 'text-yellow-400' },
  '금': { hanja: '金', bg: 'bg-gray-300/20', text: 'text-gray-300' },
  '수': { hanja: '水', bg: 'bg-blue-500/20', text: 'text-blue-400' },
};

export function YongshinCard({ type, element, hanja, description }: YongshinCardProps) {
  const [selectedEntry, setSelectedEntry] = useState<GlossaryEntry | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const info = ELEMENT_INFO[element];

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
          <Icon name="solar:star-bold" size={24} className="text-primary" />
          <button
            onClick={handleTitleClick}
            className="text-xl font-bold text-foreground underline decoration-white/30 hover:decoration-primary transition-colors"
          >
            용신
          </button>
        </div>

        <GlassCard className="p-4 md:p-6">
          <div className="flex flex-wrap gap-4">
            <div className={`${info.bg} rounded-xl p-4 text-center min-w-[100px]`}>
              <div className="text-xs text-muted-foreground mb-2">{type}</div>
              <div className={`text-2xl font-bold ${info.text}`}>
                {element}({hanja || info.hanja})
              </div>
            </div>

            {description && (
              <div className="flex-1 min-w-[200px]">
                <p className="text-gray-600 text-sm leading-relaxed">{description}</p>
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
