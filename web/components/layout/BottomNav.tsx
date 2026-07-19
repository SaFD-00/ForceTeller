'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon } from '@/components/ui';
import { cn } from '@/lib/utils';
import { NAV_ITEMS, isNavItemActive } from './nav-items';

/**
 * 모바일/태블릿 하단 내비게이션.
 * lg 이상에서는 Sidebar가 같은 역할을 하므로 숨긴다.
 */
export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav
      aria-label="주요 메뉴"
      className="fixed bottom-0 inset-x-0 z-40 h-16 border-t-[1.5px] border-border bg-surface lg:hidden"
    >
      <ul className="flex h-full items-stretch">
        {NAV_ITEMS.map((item) => {
          const active = isNavItemActive(item.href, pathname);
          return (
            <li key={item.href} className="flex-1">
              <Link
                href={item.href}
                aria-current={active ? 'page' : undefined}
                className={cn(
                  'focus-ring flex h-full min-h-11 w-full flex-col items-center justify-center gap-0.5 transition-colors',
                  active ? 'text-accent' : 'text-muted-foreground'
                )}
              >
                <Icon name={item.icon} size={22} />
                <span className={cn('text-xs', active && 'font-semibold')}>
                  {item.label}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

export default BottomNav;
