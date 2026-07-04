'use client';

import { HeroSection } from '@/components/hero';
import { FeatureGrid } from '@/components/features';
import { LoadingOverlay } from '@/components/ui';
import { useSajuStore } from '@/stores/sajuStore';

export default function HomePage() {
  const { isLoading } = useSajuStore();

  return (
    <main className="min-h-screen">
      <LoadingOverlay isVisible={isLoading} />
      <HeroSection />
      <FeatureGrid />

      {/* Footer */}
      <footer className="py-8 px-4 border-t-[1.5px] border-border">
        <div className="max-w-6xl mx-auto text-center text-muted-foreground text-sm">
          <p>© 2026 ForceTeller · AI 기반 사주팔자 분석 서비스</p>
        </div>
      </footer>
    </main>
  );
}
