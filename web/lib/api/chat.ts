// 채팅 API 함수

import { apiClient } from './client';
import type { ChatResponse, AgentType } from '@/types/saju';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

interface ChatMessageRequest {
  message: string;
  agent_type?: AgentType;
  session_id?: string;
  saju_context?: Record<string, unknown>;
}

// 스트리밍 청크 타입
export interface StreamChunk {
  type: 'reasoning' | 'output' | 'reasoning_done' | 'done' | 'error' | 'session' | 'suggested_questions';
  content: string | string[];
}

export async function sendChatMessage(data: ChatMessageRequest): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>('/api/chat', {
    message: data.message,
    saju_data: data.saju_context,
    session_id: data.session_id,
    focus: data.agent_type,
  });

  return response;
}

export interface SessionInfo {
  session_id: string;
  created_at: string;
  last_activity: string;
  message_count: number;
  name: string;
}

export async function getSessions(): Promise<{
  success: boolean;
  sessions: SessionInfo[];
  total: number;
}> {
  return apiClient.get('/api/chat/sessions');
}

export async function getSession(sessionId: string): Promise<{
  success: boolean;
  session: Record<string, unknown>;
}> {
  return apiClient.get(`/api/chat/sessions/${sessionId}`);
}

export async function deleteSession(sessionId: string): Promise<{
  success: boolean;
  message: string;
}> {
  return apiClient.delete(`/api/chat/sessions/${sessionId}`);
}

export async function clearSessionHistory(sessionId: string): Promise<{
  success: boolean;
  message: string;
}> {
  return apiClient.post(`/api/chat/sessions/${sessionId}/clear`, {});
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
