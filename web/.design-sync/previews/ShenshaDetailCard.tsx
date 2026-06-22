import { ShenshaDetailCard } from "forceteller-web";

// 庚午 · 辛巳 · 甲寅 · 己巳 — 일간 갑목(甲木) 예시 사주
const pillars = {
  year: {
    heavenly_stem: { hanja: "庚", korean: "경", element: "금" as const },
    earthly_branch: { hanja: "午", korean: "오", element: "화" as const },
    ten_god: "편관",
    branch_ten_god: "상관",
  },
  month: {
    heavenly_stem: { hanja: "辛", korean: "신", element: "금" as const },
    earthly_branch: { hanja: "巳", korean: "사", element: "화" as const },
    ten_god: "정관",
    branch_ten_god: "식신",
  },
  day: {
    heavenly_stem: { hanja: "甲", korean: "갑", element: "목" as const },
    earthly_branch: { hanja: "寅", korean: "인", element: "목" as const },
    ten_god: "일원",
    branch_ten_god: "비견",
  },
  hour: {
    heavenly_stem: { hanja: "己", korean: "기", element: "토" as const },
    earthly_branch: { hanja: "巳", korean: "사", element: "화" as const },
    ten_god: "정재",
    branch_ten_god: "식신",
  },
};

// position 은 영문 키(year·month·day·hour)로 주별 그룹화에 사용된다.
const shensha = [
  {
    name: "천을귀인",
    hanja: "天乙貴人",
    type: "길신" as const,
    position: "day",
    description: "가장 으뜸가는 길신으로, 어려움에 처했을 때 귀인의 도움을 받아 위기를 넘긴다.",
  },
  {
    name: "문창귀인",
    hanja: "文昌貴人",
    type: "길신" as const,
    position: "hour",
    description: "학문과 글재주를 관장하는 길신으로, 총명함과 시험운을 높여 준다.",
  },
  {
    name: "역마살",
    hanja: "驛馬殺",
    type: "중성" as const,
    position: "month",
    description: "이동과 변화를 상징하며, 활동성이 강하고 해외나 타향과 인연이 깊다.",
  },
  {
    name: "도화살",
    hanja: "桃花殺",
    type: "흉신" as const,
    position: "year",
    description: "이성에게 매력을 끄는 기운으로, 인기와 끼가 많으나 구설수를 조심해야 한다.",
  },
];

/** 주별 보기(기본) — 사주팔자 표 위에 년·월·일·시주별 신살을 색상 배지로 배치. */
export function PillarView() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 640 }}>
      <ShenshaDetailCard shensha={shensha} pillars={pillars} />
    </div>
  );
}

/** 유형별 보기 — pillars 미제공 시 길신·중성·흉신 카테고리별 카드 그리드로 폴백. */
export function TypeView() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 640 }}>
      <ShenshaDetailCard shensha={shensha} />
    </div>
  );
}

/** 길신만 — 천을귀인·문창귀인 등 긍정 신살이 녹색 강조로 표시. */
export function AuspiciousOnly() {
  const auspicious = shensha.filter((s) => s.type === "길신");
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <ShenshaDetailCard shensha={auspicious} />
    </div>
  );
}
