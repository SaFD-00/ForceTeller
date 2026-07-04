import type { Metadata } from 'next';
import { Bangers, JetBrains_Mono } from 'next/font/google';
import { Sidebar } from '@/components/layout/Sidebar';
import './globals.css';

// Tetris 디자인 시스템 디스플레이/모노 폰트.
// Bangers = 라틴/숫자 디스플레이(단일 weight라 weight 명시 필수),
// JetBrains Mono = 간지 한자·수치 모노. 둘 다 next/font로 번들.
// 한글 디스플레이(Black Han Sans)는 latin subset만 노출하는 next/font로는
// 한글 글리프를 번들할 수 없어 <head>의 Google Fonts <link>로 로드한다
// (Pretendard와 동일한 CDN link 방식). 본문은 Pretendard 유지.
const bangers = Bangers({
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
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="ko"
      className={`${bangers.variable} ${jetbrainsMono.variable}`}
    >
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css"
        />
        {/* 한글 디스플레이 서체 (Tetris) — Google Fonts. 실패 시 Pretendard 폴백 */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&display=swap"
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
