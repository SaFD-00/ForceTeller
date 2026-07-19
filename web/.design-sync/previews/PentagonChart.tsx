import { PentagonChart } from "forceteller-web";

/** 일간 경금(庚金) — 오행이 비교적 고른 사주, 십성 매핑 명시. */
export function GeumDayMaster() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 360 }}>
      <PentagonChart
        dayMaster={"금" as const}
        distribution={{ 목: 1, 화: 2, 토: 1, 금: 3, 수: 1 }}
        tenGodMapping={{
          금: "비겁",
          수: "식상",
          목: "재성",
          화: "관성",
          토: "인성",
        }}
        dayStemKorean="경"
      />
    </div>
  );
}

/** 일간 갑목(甲木) — 화(火)가 강하고 금(金)이 부족한 신약 사주. */
export function MokDayMaster() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 360 }}>
      <PentagonChart
        dayMaster={"목" as const}
        distribution={{ 목: 2, 화: 4, 토: 1, 금: 0, 수: 1 }}
        dayStemKorean="갑"
      />
    </div>
  );
}

/** 일간 임수(壬水) — 십성 매핑/일간 한글 생략, 기본 표시로 폴백되는 경우. */
export function SuDayMasterDefault() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 360 }}>
      <PentagonChart
        dayMaster={"수" as const}
        distribution={{ 목: 2, 화: 1, 토: 2, 금: 2, 수: 1 }}
      />
    </div>
  );
}
