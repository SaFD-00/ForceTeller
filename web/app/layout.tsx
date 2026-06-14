import type { Metadata } from 'next';
import { Providers } from './providers';
import { Sidebar } from '@/components/layout/Sidebar';
import './globals.css';

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
    <html lang="ko">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css"
        />
      </head>
      <body className="min-h-screen bg-background text-foreground font-sans">
        <Providers>
          <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 min-w-0 lg:pl-16">{children}</div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
