import { SuggestedQuestions } from "forceteller-web";

/** 기본 상태 — AI가 제안한 후속 질문 칩 3개 (최대 3개까지 노출). */
export function Default() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 420 }}>
      <SuggestedQuestions
        questions={[
          "제 일간 무토(戊土)의 성향이 궁금해요",
          "올해 들어온 정관 대운은 어떤 의미인가요?",
          "신금(辛金) 일간에게 부족한 오행은 무엇인가요?",
        ]}
        onQuestionClick={(q) => console.log(q)}
      />
    </div>
  );
}

/** 질문 1개만 제안된 경우 — 단일 칩 렌더. */
export function SingleQuestion() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 420 }}>
      <SuggestedQuestions
        questions={["병화(丙火) 일간과 임수(壬水) 배우자의 궁합이 어떤가요?"]}
        onQuestionClick={(q) => console.log(q)}
      />
    </div>
  );
}

/** 비활성(disabled) 상태 — 답변 생성 중 칩 클릭이 막힌 모습. */
export function Disabled() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 420 }}>
      <SuggestedQuestions
        questions={[
          "갑목(甲木) 일간에게 식신은 어떤 작용을 하나요?",
          "을묘(乙卯)일주의 십성 구성을 풀어주세요",
          "경금(庚金) 대운에 들어오는 편재 운을 알려주세요",
        ]}
        onQuestionClick={(q) => console.log(q)}
        disabled={true}
      />
    </div>
  );
}

/** 긴 질문 텍스트 — line-clamp로 한 줄 말줄임 처리되는 칩. */
export function LongQuestion() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 360 }}>
      <SuggestedQuestions
        questions={[
          "정묘(丁卯)일주에 인성이 강하게 들어왔을 때 학업과 직장 운에서 정인과 편인이 각각 어떤 영향을 주는지 자세히 설명해주세요",
          "계수(癸水) 일간이 화(火) 기운이 부족할 때 어떤 보완책이 있나요?",
        ]}
        onQuestionClick={(q) => console.log(q)}
      />
    </div>
  );
}
