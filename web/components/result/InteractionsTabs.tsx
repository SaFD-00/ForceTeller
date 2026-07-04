'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon, GlassCard } from '@/components/ui';
import type { InteractionsData } from '@/types/saju';

interface InteractionsTabsProps {
  interactions: InteractionsData;
}

// 탭 정보 정의
const TAB_INFO = [
  { key: '천간합', label: '천간합', icon: 'solar:link-round-bold', color: 'text-green-600' },
  { key: '지지육합', label: '지지육합', icon: 'solar:link-round-bold', color: 'text-blue-600' },
  { key: '지지삼합', label: '지지삼합', icon: 'solar:link-minimalistic-2-bold', color: 'text-accent' },
  { key: '지지방합', label: '지지방합', icon: 'solar:link-square-bold', color: 'text-cyan-600' },
  { key: '지지반합', label: '지지반합', icon: 'solar:link-broken-bold', color: 'text-teal-600' },
  { key: '천간충극', label: '천간충극', icon: 'solar:bolt-bold', color: 'text-orange-600' },
  { key: '지지충', label: '지지충', icon: 'solar:bolt-circle-bold', color: 'text-red-600' },
  { key: '지지형', label: '지지형', icon: 'solar:danger-triangle-bold', color: 'text-amber-600' },
  { key: '지지파', label: '지지파', icon: 'solar:shield-cross-bold', color: 'text-rose-600' },
  { key: '지지해', label: '지지해', icon: 'solar:shield-warning-bold', color: 'text-pink-600' },
  { key: '공망', label: '공망', icon: 'solar:ghost-bold', color: 'text-muted-foreground' },
] as const;

// 위치 한글 표시
const positionNames: Record<string, string> = {
  year: '년주',
  month: '월주',
  day: '일주',
  hour: '시주',
};

// 지지 이름
const branchNames = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'];

export function InteractionsTabs({ interactions }: InteractionsTabsProps) {
  // 데이터가 있는 탭만 필터링
  const availableTabs = TAB_INFO.filter(tab => {
    const items = interactions[tab.key as keyof InteractionsData];
    return items && items.length > 0;
  });

  const [activeTab, setActiveTab] = useState(availableTabs[0]?.key || '');

  if (availableTabs.length === 0) {
    return null;
  }

  const activeTabInfo = TAB_INFO.find(t => t.key === activeTab);
  const activeItems = interactions[activeTab as keyof InteractionsData] || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="mb-8"
    >
      <div className="flex items-center gap-2 mb-4">
        <Icon name="solar:widget-2-bold" size={24} className="text-primary" />
        <h2 className="text-xl font-bold text-foreground">천간 지지 작용</h2>
      </div>

      <GlassCard className="p-4 md:p-6">
        {/* 탭 버튼들 */}
        <div className="flex flex-wrap gap-2 mb-6 pb-4 border-b border-border">
          {availableTabs.map(tab => {
            const count = (interactions[tab.key as keyof InteractionsData] || []).length;
            const isActive = activeTab === tab.key;

            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all
                  ${isActive
                    ? 'bg-primary/20 text-primary border border-primary/30'
                    : 'bg-muted text-muted-foreground hover:bg-muted hover:text-foreground'
                  }`}
              >
                <Icon name={tab.icon} size={16} className={isActive ? 'text-primary' : tab.color} />
                <span className="text-sm font-medium">{tab.label}</span>
                <span className={`text-xs px-1.5 py-0.5 rounded-full
                  ${isActive ? 'bg-primary/30 text-primary' : 'bg-muted text-muted-foreground'}`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* 탭 컨텐츠 */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            {activeItems.length === 0 ? (
              <p className="text-center text-muted-foreground py-8">
                해당하는 {activeTabInfo?.label}이(가) 없습니다.
              </p>
            ) : (
              <div className="space-y-4">
                {activeItems.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-lg bg-muted border border-border"
                  >
                    {/* 설명 */}
                    <div className="flex items-center gap-2 mb-2">
                      <Icon
                        name={activeTabInfo?.icon || 'solar:info-circle-bold'}
                        size={20}
                        className={activeTabInfo?.color || 'text-primary'}
                      />
                      <span className="font-medium text-foreground">
                        {item.description}
                      </span>
                    </div>

                    {/* 위치 정보 */}
                    {item.positions && (
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <span>위치:</span>
                        {item.positions.map((pos, i) => (
                          <span key={i} className="px-2 py-0.5 bg-muted rounded">
                            {positionNames[pos] || pos}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* 공망의 경우 */}
                    {item.position && item.branch !== undefined && (
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <span>위치:</span>
                        <span className="px-2 py-0.5 bg-muted rounded">
                          {positionNames[item.position] || item.position}
                        </span>
                        <span className="px-2 py-0.5 bg-muted text-muted-foreground rounded">
                          {branchNames[item.branch]}
                        </span>
                      </div>
                    )}

                    {/* 합화 결과 */}
                    {item.result && (
                      <div className="mt-2 text-sm">
                        <span className="text-muted-foreground">합화 결과: </span>
                        <span className="text-primary font-medium">{item.result}</span>
                      </div>
                    )}

                    {/* 삼합/방합 이름 */}
                    {item.name && (
                      <div className="mt-1 text-xs text-muted-foreground">
                        {item.name}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </GlassCard>
    </motion.div>
  );
}

export default InteractionsTabs;
