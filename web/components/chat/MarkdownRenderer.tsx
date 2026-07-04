'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const components: Components = {
    // 제목
    h1: ({ children }) => (
      <h1 className="text-xl font-bold mt-4 mb-2 text-foreground">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-lg font-bold mt-4 mb-2 text-foreground">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-base font-semibold mt-3 mb-1.5 text-foreground">{children}</h3>
    ),
    h4: ({ children }) => (
      <h4 className="text-sm font-semibold mt-2 mb-1 text-foreground">{children}</h4>
    ),

    // 단락
    p: ({ children }) => (
      <p className="mb-2 leading-relaxed text-foreground">{children}</p>
    ),

    // 목록
    ul: ({ children }) => (
      <ul className="list-disc list-outside ml-5 mb-3 space-y-1 text-foreground">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-outside ml-5 mb-3 space-y-1 text-foreground">{children}</ol>
    ),
    li: ({ children }) => (
      <li className="leading-relaxed">{children}</li>
    ),

    // 코드
    code: ({ className, children, ...props }) => {
      const isInline = !className;
      if (isInline) {
        return (
          <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono text-accent" {...props}>
            {children}
          </code>
        );
      }
      return (
        <code className="block bg-muted p-3 rounded-lg my-2 overflow-x-auto font-mono text-sm text-foreground" {...props}>
          {children}
        </code>
      );
    },
    pre: ({ children }) => (
      <pre className="my-2">{children}</pre>
    ),

    // 인용구
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-accent/50 pl-4 my-3 italic text-muted-foreground">
        {children}
      </blockquote>
    ),

    // 굵게/기울임
    strong: ({ children }) => (
      <strong className="font-bold text-foreground">{children}</strong>
    ),
    em: ({ children }) => (
      <em className="italic text-foreground">{children}</em>
    ),

    // 구분선
    hr: () => (
      <hr className="my-4 border-border" />
    ),

    // 링크
    a: ({ href, children }) => (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-accent hover:text-accent/80 underline underline-offset-2"
      >
        {children}
      </a>
    ),

    // 테이블
    table: ({ children }) => (
      <div className="overflow-x-auto my-3">
        <table className="min-w-full border border-border rounded-lg overflow-hidden">
          {children}
        </table>
      </div>
    ),
    thead: ({ children }) => (
      <thead className="bg-muted">{children}</thead>
    ),
    tbody: ({ children }) => (
      <tbody className="divide-y divide-border">{children}</tbody>
    ),
    tr: ({ children }) => (
      <tr className="divide-x divide-border">{children}</tr>
    ),
    th: ({ children }) => (
      <th className="px-3 py-2 text-left text-sm font-semibold text-foreground">{children}</th>
    ),
    td: ({ children }) => (
      <td className="px-3 py-2 text-sm text-foreground">{children}</td>
    ),
  };

  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
