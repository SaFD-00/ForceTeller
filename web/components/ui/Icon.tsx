'use client';

import { Icon as IconifyIcon } from '@iconify/react';
import { cn } from '@/lib/utils';

interface IconProps {
  name: string;
  size?: number;
  className?: string;
}

export function Icon({ name, size = 24, className }: IconProps) {
  return (
    <IconifyIcon
      icon={name}
      width={size}
      height={size}
      className={cn('inline-block', className)}
    />
  );
}
