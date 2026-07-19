'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon, Mascot } from '@/components/ui';
import { cn } from '@/lib/utils';
import { NAV_ITEMS, isNavItemActive } from './nav-items';

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
          const active = isNavItemActive(item.href, pathname);
          return (
            <Link
              key={item.href}
              href={item.href}
              title={item.label}
              aria-current={active ? 'page' : undefined}
              className={cn(
                'focus-ring flex h-11 w-11 items-center justify-center rounded-lg transition-all',
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
