import type { Metadata } from 'next';
import { Delius_Swash_Caps, JetBrains_Mono } from 'next/font/google';
import { Sidebar } from '@/components/layout/Sidebar';
import './globals.css';

// Doodle 디자인 시스템 디스플레이/모노 폰트.
// Delius Swash Caps = 라틴/숫자 손글씨 디스플레이(단일 weight라 weight 명시 필수),
// JetBrains Mono = 간지 한자·수치 모노(Doodle label-caps). 둘 다 next/font로 번들.
// 한글 디스플레이(Gaegu)는 latin subset만 노출하는 next/font로는 한글 글리프를
// 번들할 수 없어 <head>의 Google Fonts <link>로 로드한다
// (Pretendard와 동일한 CDN link 방식). 본문은 Pretendard 유지.
const deliusSwashCaps = Delius_Swash_Caps({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-display-latin',
  display: 'swap',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'ForceTeller | 사주명리 AI',
  description: '사주팔자 계산 및 AI 해석 서비스',
  // 파비콘은 App Router 규약(app/icon.svg)으로 자동 주입됩니다.
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="ko"
      className={`${deliusSwashCaps.variable} ${jetbrainsMono.variable}`}
    >
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css"
        />
        {/* 한글 디스플레이 서체(Gaegu, 손글씨) — Google Fonts. 실패 시 Pretendard 폴백.
            Delius Swash Caps(라틴)·JetBrains Mono는 next/font로 번들되므로 여기서 로드하지 않는다. */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        {/* App Router에는 pages/_document.js가 없고, 한글 글리프는 next/font(latin subset)로
            번들할 수 없어 <head> <link>가 유일한 로드 경로다. 규칙이 가정하는 상황과 달라 비활성화한다. */}
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Gaegu&display=swap"
        />
      </head>
      <body className="min-h-screen bg-background text-foreground font-sans">
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1 min-w-0 lg:pl-16">{children}</div>
        </div>
      </body>
    </html>
  );
}
