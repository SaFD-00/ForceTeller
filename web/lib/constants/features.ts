// 기능 그리드 데이터

export const FEATURES = [
  {
    icon: 'solar:calculator-bold',
    title: '사주계산',
    description: '정확한 사주팔자 산출',
    detail: '생년월일시를 기반으로 정확한 사주 4주를 계산합니다.',
    color: 'from-accent to-primary',
  },
  {
    icon: 'solar:user-heart-bold',
    title: '성격분석',
    description: 'AI 기반 성격 해석',
    detail: '일간과 십성 분포를 분석하여 당신의 성격을 해석합니다.',
    color: 'from-pink-500 to-rose-500',
  },
  {
    icon: 'solar:wallet-money-bold',
    title: '직업운',
    description: '적성 및 재물운',
    detail: '용신과 재성을 분석하여 적합한 직업과 재물운을 알려드립니다.',
    color: 'from-amber-500 to-orange-500',
  },
  {
    icon: 'solar:hearts-bold',
    title: '연애운',
    description: '인연 및 결혼운',
    detail: '일지와 배우자 궁을 분석하여 연애와 결혼운을 해석합니다.',
    color: 'from-red-500 to-pink-500',
  },
  {
    icon: 'solar:health-bold',
    title: '건강운',
    description: '체질 및 건강 조언',
    detail: '오행 균형을 분석하여 건강 취약점과 관리법을 안내합니다.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: 'solar:chart-2-bold',
    title: '대운분석',
    description: '10년 주기 운세',
    detail: '대운 흐름을 분석하여 인생의 큰 흐름을 파악합니다.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: 'solar:stars-bold',
    title: '신살',
    description: '길신/흉신 분석',
    detail: '천을귀인, 역마, 도화 등 특별한 기운을 분석합니다.',
    color: 'from-yellow-500 to-amber-500',
  },
  {
    icon: 'solar:pie-chart-2-bold',
    title: '오행분포',
    description: '오행 균형 분석',
    detail: '목화토금수의 분포를 시각화하여 균형을 파악합니다.',
    color: 'from-teal-500 to-green-500',
  },
  {
    icon: 'solar:chat-round-dots-bold',
    title: 'AI 대화',
    description: '전문 에이전트 상담',
    detail: '다양한 전문 AI 에이전트와 자유롭게 대화하세요.',
    color: 'from-accent to-primary',
  },
] as const;

export const AGENTS = [
  {
    id: 'personality',
    name: '성격 분석',
    icon: 'solar:user-heart-bold',
    description: '성격, 기질, 성향 분석',
  },
  {
    id: 'career',
    name: '직업 분석',
    icon: 'solar:wallet-money-bold',
    description: '직업 적성, 재물운, 사업운',
  },
  {
    id: 'relationship',
    name: '관계 분석',
    icon: 'solar:hearts-bold',
    description: '연애, 결혼, 대인관계',
  },
  {
    id: 'health',
    name: '건강 분석',
    icon: 'solar:health-bold',
    description: '건강 체질, 취약 부위',
  },
  {
    id: 'fortune',
    name: '운세 분석',
    icon: 'solar:chart-2-bold',
    description: '대운, 세운, 시기별 운세',
  },
] as const;
