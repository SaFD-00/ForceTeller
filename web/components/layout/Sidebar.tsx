'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon, Mascot } from '@/components/ui';
import { cn } from '@/lib/utils';

const NAV_ITEMS = [
  { href: '/', icon: 'solar:home-2-linear', label: '홈' },
  { href: '/result', icon: 'solar:chart-square-linear', label: '결과' },
  { href: '/chat', icon: 'solar:chat-round-line-linear', label: 'AI 상담' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-16 flex-col items-center border-r-[1.5px] border-border bg-surface py-4 lg:flex">
      {/* 로고 (마스코트 별이) */}
      <Link
        href="/"
        className="mb-6 flex h-11 w-11 items-center justify-center"
        aria-label="ForceTeller 홈"
      >
        <Mascot mood="idle" size="sm" />
      </Link>

      {/* 내비게이션 */}
      <nav className="flex flex-col gap-2">
        {NAV_ITEMS.map((item) => {
          const active = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              title={item.label}
              className={cn(
                'flex h-11 w-11 items-center justify-center rounded-lg transition-all',
                active
                  ? 'border-[1.5px] border-border bg-primary/15 text-primary shadow-block-sm'
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
