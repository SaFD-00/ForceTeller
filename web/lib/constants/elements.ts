// 오행 관련 상수

export const ELEMENT_COLORS = {
  목: {
    bg: 'bg-element-wood/20',
    text: 'text-element-wood',
    border: 'border-element-wood/50',
    hex: '#22c55e',
    gradient: 'from-green-500 to-emerald-500',
  },
  화: {
    bg: 'bg-element-fire/20',
    text: 'text-element-fire',
    border: 'border-element-fire/50',
    hex: '#ef4444',
    gradient: 'from-red-500 to-orange-500',
  },
  토: {
    bg: 'bg-element-earth/20',
    text: 'text-element-earth',
    border: 'border-element-earth/50',
    hex: '#eab308',
    gradient: 'from-yellow-500 to-amber-500',
  },
  금: {
    bg: 'bg-element-metal/20',
    text: 'text-element-metal',
    border: 'border-element-metal/50',
    hex: '#a1a1aa',
    gradient: 'from-zinc-400 to-gray-400',
  },
  수: {
    bg: 'bg-element-water/20',
    text: 'text-element-water',
    border: 'border-element-water/50',
    hex: '#3b82f6',
    gradient: 'from-blue-500 to-cyan-500',
  },
} as const;

export const ELEMENT_NAMES = {
  목: { korean: '목', chinese: '木', english: 'Wood' },
  화: { korean: '화', chinese: '火', english: 'Fire' },
  토: { korean: '토', chinese: '土', english: 'Earth' },
  금: { korean: '금', chinese: '金', english: 'Metal' },
  수: { korean: '수', chinese: '水', english: 'Water' },
} as const;

export const TEN_GODS = {
  비견: { group: '비겁', meaning: '같은 기운', icon: 'solar:users-group-rounded-bold' },
  겁재: { group: '비겁', meaning: '경쟁자', icon: 'solar:users-group-two-rounded-bold' },
  식신: { group: '식상', meaning: '표현력', icon: 'solar:chat-square-like-bold' },
  상관: { group: '식상', meaning: '창의력', icon: 'solar:lightbulb-bolt-bold' },
  편재: { group: '재성', meaning: '돈/아버지', icon: 'solar:wallet-money-bold' },
  정재: { group: '재성', meaning: '재물/아내', icon: 'solar:safe-square-bold' },
  편관: { group: '관성', meaning: '직장/압박', icon: 'solar:shield-warning-bold' },
  정관: { group: '관성', meaning: '명예/남편', icon: 'solar:crown-bold' },
  편인: { group: '인성', meaning: '학문/어머니', icon: 'solar:book-bookmark-bold' },
  정인: { group: '인성', meaning: '교육/보호', icon: 'solar:diploma-bold' },
} as const;

export const TWELVE_PHASES = [
  { name: '장생', meaning: '탄생', energy: 8 },
  { name: '목욕', meaning: '성장', energy: 4 },
  { name: '관대', meaning: '성인', energy: 10 },
  { name: '건록', meaning: '왕성', energy: 12 },
  { name: '제왕', meaning: '정점', energy: 12 },
  { name: '쇠', meaning: '쇠퇴', energy: -4 },
  { name: '병', meaning: '아픔', energy: -8 },
  { name: '사', meaning: '죽음', energy: -10 },
  { name: '묘', meaning: '무덤', energy: -12 },
  { name: '절', meaning: '끊김', energy: -8 },
  { name: '태', meaning: '잉태', energy: 2 },
  { name: '양', meaning: '양육', energy: 4 },
] as const;
