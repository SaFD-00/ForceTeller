import { ElementDistribution } from "forceteller-web";

// 일간 갑목(甲木) 예시 — 목 신강 사주의 오행/십성 분포
const distribution = { 목: 3, 화: 2, 토: 1, 금: 1, 수: 1 } as const;

const tenGods = {
  비견: 2,
  겁재: 1,
  식신: 1,
  상관: 1,
  편재: 1,
  정재: 1,
  편관: 1,
  정관: 1,
  편인: 0,
  정인: 1,
} as const;

/** 오행/십성 분포 상세 — 목 우세(발달) 사주, 도넛 차트 + 음양 쌍 십성 비율. */
export function MokDominant() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 760 }}>
      <ElementDistribution distribution={distribution} tenGods={tenGods} dominant={"목"} />
    </div>
  );
}

/** 일부 오행 부족(수=0) 사례 — 부족 라벨 및 빈 비율(-) 표시 확인. */
export function WithLackingElement() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 760 }}>
      <ElementDistribution
        distribution={{ 목: 1, 화: 4, 토: 2, 금: 1, 수: 0 }}
        tenGods={{
          비견: 1,
          겁재: 0,
          식신: 2,
          상관: 1,
          편재: 1,
          정재: 1,
          편관: 1,
          정관: 1,
          편인: 0,
          정인: 0,
        }}
        dominant={"화"}
      />
    </div>
  );
}

/** dominant 미정(null) — 균형 잡힌 분포에서 중앙 라벨이 '-'로 표시되는 케이스. */
export function NoDominant() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 760 }}>
      <ElementDistribution
        distribution={{ 목: 2, 화: 2, 토: 1, 금: 2, 수: 1 }}
        tenGods={{
          비견: 1,
          겁재: 1,
          식신: 1,
          상관: 1,
          편재: 1,
          정재: 1,
          편관: 1,
          정관: 1,
          편인: 1,
          정인: 1,
        }}
        dominant={null}
      />
    </div>
  );
}
