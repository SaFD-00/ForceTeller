// 채팅 API 함수

import type { AgentType } from '@/types/saju';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

interface ChatMessageRequest {
  message: string;
  agent_type?: AgentType;
  session_id?: string;
  saju_context?: Record<string, unknown>;
}

// 스트리밍 청크 타입
export interface StreamChunk {
  type:
    | 'reasoning'
    | 'output'
    | 'reasoning_done'
    | 'done'
    | 'error'
    | 'session'
    | 'suggested_questions'
    | 'agent_selected';
  content?: string | string[];
  // agent_selected 이벤트 필드 (출처·신뢰도 배지)
  agent?: string;
  display_name?: string;
  confidence?: number;
}

/**
 * 스트리밍 채팅 메시지 전송 (Reasoning 포함)
 * Server-Sent Events를 통해 AI 사고 과정과 응답을 실시간으로 수신
 */
export async function* streamChatMessage(
  data: ChatMessageRequest
): AsyncGenerator<StreamChunk, void, unknown> {
  const response = await fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: data.message,
      saju_data: data.saju_context,
      session_id: data.session_id,
      focus: data.agent_type,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('ReadableStream not supported');
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // SSE 이벤트 파싱
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // 마지막 불완전한 라인은 버퍼에 유지

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const jsonStr = line.slice(6).trim();
          if (jsonStr) {
            try {
              const chunk: StreamChunk = JSON.parse(jsonStr);
              yield chunk;

              // error 이벤트면 종료 (done은 suggested_questions가 올 수 있으므로 대기)
              if (chunk.type === 'error') {
                return;
              }
            } catch (e) {
              console.error('Failed to parse SSE chunk:', jsonStr, e);
            }
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}
