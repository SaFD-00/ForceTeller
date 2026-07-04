import { PillarTable } from "forceteller-web";

// 庚午 · 辛巳 · 甲寅 · 己巳 — 일간 갑목(甲木) 예시 사주
const pillars = {
  year: {
    heavenly_stem: { hanja: "庚", korean: "경", element: "금" as const, polarity: "양" as const },
    earthly_branch: { hanja: "午", korean: "오", element: "화" as const, polarity: "양" as const },
    ten_god: "편관", branch_ten_god: "상관", hidden_stems: "정·기", twelve_phase: "사", twelve_shensha: "재살",
  },
  month: {
    heavenly_stem: { hanja: "辛", korean: "신", element: "금" as const, polarity: "음" as const },
    earthly_branch: { hanja: "巳", korean: "사", element: "화" as const, polarity: "음" as const },
    ten_god: "정관", branch_ten_god: "식신", hidden_stems: "병·무·경", twelve_phase: "병", twelve_shensha: "역마",
  },
  day: {
    heavenly_stem: { hanja: "甲", korean: "갑", element: "목" as const, polarity: "양" as const },
    earthly_branch: { hanja: "寅", korean: "인", element: "목" as const, polarity: "양" as const },
    ten_god: "일원", branch_ten_god: "비견", hidden_stems: "갑·병·무", twelve_phase: "건록", twelve_shensha: "지살",
  },
  hour: {
    heavenly_stem: { hanja: "己", korean: "기", element: "토" as const, polarity: "음" as const },
    earthly_branch: { hanja: "巳", korean: "사", element: "화" as const, polarity: "음" as const },
    ten_god: "정재", branch_ten_god: "식신", hidden_stems: "병·무·경", twelve_phase: "병", twelve_shensha: "겁살",
  },
};

/** 사주팔자(四柱八字) 표 — 년·월·일·시주 + 지장간·십이운성·십이신살. */
export function FullChart() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff" }}>
      <PillarTable pillars={pillars} />
    </div>
  );
}

/** 간결형 — 지장간·십이운성·신살 숨김. */
export function Compact() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff" }}>
      <PillarTable pillars={pillars} showHiddenStems={false} showTwelvePhase={false} showTwelveShensha={false} />
    </div>
  );
}
