'use client';

import { forwardRef, useId } from 'react';
import { cn } from '@/lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, type = 'text', id, ...props }, ref) => {
    const generatedId = useId();
    const inputId = id ?? generatedId;
    const errorId = error ? `${inputId}-error` : undefined;
    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-foreground mb-2"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          ref={ref}
          aria-invalid={error ? true : undefined}
          aria-describedby={errorId}
          className={cn(
            'w-full px-4 py-3 rounded-lg',
            'bg-surface border-[1.5px] border-border',
            'text-foreground placeholder:text-muted-foreground',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus:border-accent',
            'transition-all duration-200',
            error && 'border-danger focus-visible:ring-danger',
            className
          )}
          {...props}
        />
        {error && (
          <p id={errorId} className="mt-1 text-sm text-danger-ink">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
