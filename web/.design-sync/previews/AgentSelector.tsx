import { AgentSelector } from "forceteller-web";

/** 종합 상담 탭이 선택된 기본 상태 — 갑목 일간 명식 전반 분석 */
export function GeneralSelected() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <AgentSelector
        selected={"general" as const}
        onSelect={(agent) => console.log("선택된 에이전트:", agent)}
      />
    </div>
  );
}

/** 용신 분석 탭 선택 — 신금 일간의 용신·기신 오행 해석 */
export function YongsinSelected() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <AgentSelector
        selected={"yongsin" as const}
        onSelect={(agent) => console.log("선택된 에이전트:", agent)}
      />
    </div>
  );
}

/** 인연·궁합 탭 선택 — 정관·편관 십성 기반 인간관계 상담 */
export function RelationshipSelected() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <AgentSelector
        selected={"relationship" as const}
        onSelect={(agent) => console.log("선택된 에이전트:", agent)}
      />
    </div>
  );
}

/** 유파 비교 탭 선택 — 5대 유파별 임수 일간 해석 대조 */
export function SchoolCompareSelected() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <AgentSelector
        selected={"school_compare" as const}
        onSelect={(agent) => console.log("선택된 에이전트:", agent)}
      />
    </div>
  );
}
