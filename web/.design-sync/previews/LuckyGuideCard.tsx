import { LuckyGuideCard } from "forceteller-web";

/** 수(水) 용신 개운법 — 색·방위·직업·활동 칩과 생활 팁/주의, 추천 알고리즘 배지까지 모두 채워진 기본 카드 */
export function WaterFull() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 560 }}>
      <LuckyGuideCard
        recommendations={{
          summary:
            "일간 갑목(甲木)이 약하지 않아 설기와 균형이 필요합니다. 수(水) 기운을 보강하면 정인의 흐름이 살아나 학문과 직관이 트입니다.",
          primary_element: {
            element: "수",
            colors: ["검정", "남색", "짙은 파랑"],
            directions: ["북", "북동"],
            main_careers: ["연구원", "교육자", "무역업", "유통"],
            recommended_activities: ["명상", "수영", "독서", "여행"],
          },
          lifestyle_tips: [
            "아침에 물 한 잔으로 하루를 시작해 수 기운을 채우세요.",
            "북쪽 창가나 책상 배치로 집중력을 높이는 것이 좋습니다.",
            "검정·남색 계열 소품을 가까이 두면 마음이 안정됩니다.",
          ],
          cautions: [
            "화(火)가 강한 한낮의 과도한 활동은 기운을 소진시킵니다.",
            "붉은색 위주의 인테리어는 정인의 흐름을 막을 수 있습니다.",
          ],
        }}
        comparison={{
          results: {},
          applicabilities: { strength: 0.82, johu: 0.41 },
          recommendation: {
            method: "strength",
            algorithm_name: "강약용신",
            result: {},
          },
        }}
      />
    </div>
  );
}

/** 화(火) 용신 — comparison 미제공으로 추천 배지 없이, 조후 보강 위주의 간결한 칩 구성 */
export function FireMinimal() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 560 }}>
      <LuckyGuideCard
        recommendations={{
          summary:
            "겨울에 태어난 임수(壬水) 일간이라 한기가 강합니다. 화(火) 기운으로 따뜻함을 더하면 식신의 표현력이 살아납니다.",
          primary_element: {
            element: "화",
            colors: ["빨강", "주황", "분홍"],
            directions: ["남"],
            main_careers: ["방송인", "요리사", "디자이너"],
            recommended_activities: ["햇볕 산책", "요가"],
          },
        }}
      />
    </div>
  );
}

/** 목(木) 용신 — 생활 팁만 있고 주의 항목이 없는 케이스(조건부 섹션 검증용) */
export function WoodTipsOnly() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 560 }}>
      <LuckyGuideCard
        recommendations={{
          summary:
            "토(土)가 두터운 사주로 무기(戊己) 기운이 강합니다. 목(木) 기운으로 통관하면 정관의 흐름이 부드러워집니다.",
          primary_element: {
            element: "목",
            colors: ["초록", "연두", "청록"],
            directions: ["동", "남동"],
            main_careers: ["교사", "출판", "기획"],
            recommended_activities: ["등산", "원예", "글쓰기"],
          },
          lifestyle_tips: [
            "동쪽 방향에 화분이나 나무 소품을 두면 목 기운이 강해집니다.",
            "초록 계열 의복으로 정관의 안정감을 더하세요.",
          ],
        }}
        comparison={{
          results: {},
          applicabilities: { tonggwan: 0.76 },
          recommendation: {
            method: "tonggwan",
            algorithm_name: "통관용신",
            result: {},
          },
        }}
      />
    </div>
  );
}

/** 금(金) 용신 — 색·방위만 채우고 직업/활동을 비워 칩 행 누락(빈 배열 미렌더) 동작 확인 */
export function MetalSparse() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 560 }}>
      <LuckyGuideCard
        recommendations={{
          summary:
            "병정(丙丁) 화 기운이 치열한 사주입니다. 금(金) 기운으로 열기를 식히면 편재의 균형이 잡힙니다.",
          primary_element: {
            element: "금",
            colors: ["흰색", "은색", "회색"],
            directions: ["서", "북서"],
            main_careers: [],
            recommended_activities: [],
          },
          cautions: ["여름철 과로와 붉은 조명은 화 기운을 더해 역효과를 냅니다."],
        }}
        comparison={{
          results: {},
          applicabilities: { johu: 0.69, byungyak: 0.5 },
          recommendation: {
            method: "byungyak",
            algorithm_name: "병약용신",
            result: {},
          },
        }}
      />
    </div>
  );
}
