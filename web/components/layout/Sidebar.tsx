'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon } from '@/components/ui';
import { cn } from '@/lib/utils';

const NAV_ITEMS = [
  { href: '/', icon: 'solar:home-2-linear', label: '홈' },
  { href: '/result', icon: 'solar:chart-square-linear', label: '결과' },
  { href: '/chat', icon: 'solar:chat-round-line-linear', label: 'AI 상담' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-16 flex-col items-center border-r border-border bg-surface py-4 lg:flex">
      {/* 로고 */}
      <Link
        href="/"
        className="mb-6 flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white"
        aria-label="ForceTeller 홈"
      >
        <Icon name="solar:magic-stick-3-bold" size={22} />
      </Link>

      {/* 내비게이션 */}
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map((item) => {
          const active = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              title={item.label}
              className={cn(
                'flex h-11 w-11 items-center justify-center rounded-xl transition-colors',
                active
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              )}
            >
              <Icon name={item.icon} size={22} />
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
