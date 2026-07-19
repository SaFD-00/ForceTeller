// 데스크톱 Sidebar와 모바일 BottomNav가 공유하는 단일 내비게이션 정의.
// 두 곳이 어긋나지 않도록 여기서만 항목을 추가/수정한다.

export interface NavItem {
  href: string;
  icon: string;
  label: string;
}

export const NAV_ITEMS: NavItem[] = [
  { href: '/', icon: 'solar:home-2-linear', label: '홈' },
  { href: '/result', icon: 'solar:chart-square-linear', label: '결과' },
  { href: '/chat', icon: 'solar:chat-round-line-linear', label: 'AI 상담' },
];

// 활성 판정: 홈은 정확히 일치할 때만 (모든 경로가 '/'로 시작하므로).
export function isNavItemActive(href: string, pathname: string): boolean {
  return href === '/' ? pathname === '/' : pathname.startsWith(href);
}
