import { TenGodsDistribution } from "forceteller-web";

/** 재성(편재·정재)이 주를 이루는 균형 잡힌 십성 분포 */
export function WealthDominant() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 960 }}>
      <TenGodsDistribution
        distribution={{
          counts: {
            비견: 1,
            겁재: 1,
            식신: 2,
            상관: 0,
            편재: 3,
            정재: 2,
            편관: 1,
            정관: 1,
            편인: 0,
            정인: 1,
          },
          primary: "편재",
        }}
      />
    </div>
  );
}

/** 인성(편인·정인)이 강하고 주 십성이 정인인 학자형 분포 */
export function ResourceHeavy() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 960 }}>
      <TenGodsDistribution
        distribution={{
          counts: {
            비견: 1,
            겁재: 0,
            식신: 1,
            상관: 1,
            편재: 0,
            정재: 1,
            편관: 0,
            정관: 2,
            편인: 2,
            정인: 4,
          },
          primary: "정인",
        }}
      />
    </div>
  );
}

/** 관성(편관·정관) 위주에 일부 십성이 0인 명예지향형 분포 */
export function PowerFocused() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 960 }}>
      <TenGodsDistribution
        distribution={{
          counts: {
            비견: 0,
            겁재: 1,
            식신: 1,
            상관: 0,
            편재: 1,
            정재: 0,
            편관: 3,
            정관: 3,
            편인: 1,
            정인: 1,
          },
          primary: "정관",
        }}
      />
    </div>
  );
}

/** 주 십성이 없는(primary=null) 고른 분포 — 하단 주 십성 카드 미표시 */
export function NoPrimary() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 960 }}>
      <TenGodsDistribution
        distribution={{
          counts: {
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
          },
          primary: null,
        }}
      />
    </div>
  );
}
