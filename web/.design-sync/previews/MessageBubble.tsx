import { MessageBubble } from "forceteller-web";

const noop = () => {};

/** 사용자 질문 + AI 답변 — 에이전트 출처·신뢰도 배지와 추천 질문 포함. */
export function Conversation() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, width: 560, padding: 16, background: "#f7f8fa" }}>
      <MessageBubble message={{ role: "user", content: "제 사주에서 직업운은 어떤가요?" }} />
      <MessageBubble
        message={{
          role: "assistant",
          content:
            "일간이 **갑목(甲木)** 으로 뿌리가 단단해, 주도적으로 일을 이끄는 직업이 잘 맞습니다.\n\n- 기획·교육·법률처럼 곧게 뻗는 분야\n- 월지 **정관**이 안정적인 조직 생활을 뒷받침",
          agent_display_name: "직업·재물",
          confidence: 0.88,
          suggested_questions: ["재물운은 어떤가요?", "이직하기 좋은 시기는?"],
          timestamp: "2026-06-23T01:30:00",
        }}
        onSuggestedQuestionClick={noop}
      />
    </div>
  );
}

/** 짧은 단일 답변(출처 배지 없음). */
export function AssistantOnly() {
  return (
    <div style={{ width: 560, padding: 16, background: "#f7f8fa" }}>
      <MessageBubble
        message={{ role: "assistant", content: "네, 용신(用神)은 **수(水)** 로 보는 것이 타당합니다." }}
      />
    </div>
  );
}
