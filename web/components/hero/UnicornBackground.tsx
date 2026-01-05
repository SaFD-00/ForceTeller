'use client';

import { useEffect, useRef } from 'react';

export function UnicornBackground() {
  const containerRef = useRef<HTMLDivElement>(null);
  const scriptLoaded = useRef(false);

  useEffect(() => {
    if (scriptLoaded.current) return;

    // Load Unicorn Studio embed script
    const script = document.createElement('script');
    script.src = 'https://cdn.unicorn.studio/v1.3.2/unicornStudio.umd.js';
    script.async = true;
    script.onload = () => {
      // @ts-expect-error - Unicorn Studio global
      if (window.UnicornStudio) {
        // @ts-expect-error - Unicorn Studio global
        window.UnicornStudio.init();
      }
    };
    document.body.appendChild(script);
    scriptLoaded.current = true;

    return () => {
      // Cleanup on unmount
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 -z-10"
      aria-hidden="true"
    >
      <div
        data-us-project="VfhA3y0V4ziDEqnIULCi"
        className="w-full h-full"
        style={{
          width: '100%',
          height: '100%',
        }}
      />
      {/* Gradient overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/20 to-black/60" />
    </div>
  );
}
