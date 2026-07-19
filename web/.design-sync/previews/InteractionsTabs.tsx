import { InteractionsTabs } from "forceteller-web";

// 庚午 · 辛巳 · 甲寅 · 己巳 사주의 천간/지지 작용 — 합·충·형·파·해·공망
// branch 인덱스: 자0 축1 인2 묘3 진4 사5 오6 미7 신8 유9 술10 해11
const fullInteractions = {
  천간합: [
    {
      type: "천간합",
      positions: ["day", "hour"],
      stems: [0, 5],
      result: "토",
      description: "갑기합(甲己合) — 일간 갑목과 시간 기토가 만나 토(土)로 화한다.",
    },
  ],
  지지육합: [
    {
      type: "지지육합",
      positions: ["year", "day"],
      branches: [6, 2],
      result: "화",
      description: "인오합(寅午合) — 일지 인목과 년지 오화가 어우러진다.",
    },
  ],
  지지삼합: [
    {
      type: "지지삼합",
      positions: ["year", "month", "hour"],
      branches: [6, 5, 5],
      result: "화",
      name: "사오미 화국(巳午未 火局)",
      description: "지지에 화(火) 기운이 강하게 모여 삼합국을 이룬다.",
    },
  ],
  천간충극: [
    {
      type: "천간충극",
      positions: ["month", "day"],
      stems: [7, 0],
      description: "갑경충(甲庚沖) — 경금이 일간 갑목을 극하여 충돌한다.",
    },
  ],
  지지충: [
    {
      type: "지지충",
      positions: ["day", "hour"],
      branches: [2, 8],
      description: "인신충(寅申沖) — 일지 인목과 신금이 정면으로 부딪친다.",
    },
  ],
  지지형: [
    {
      type: "지지형",
      positions: ["year", "month"],
      branches: [2, 5],
      name: "인사형(寅巳刑)",
      description: "은혜를 저버리는 무은지형(無恩之刑)에 해당한다.",
    },
  ],
  공망: [
    {
      type: "공망",
      position: "hour",
      branch: 9,
      description: "시주가 공망(空亡)에 들어 해당 자리의 작용이 약해진다.",
    },
  ],
} as const;

// 충·형·파·해 위주의 단일 탭 케이스
const conflictOnly = {
  지지충: [
    {
      type: "지지충",
      positions: ["year", "day"],
      branches: [0, 6],
      description: "자오충(子午沖) — 년지 자수와 일지 오화가 상충한다.",
    },
    {
      type: "지지충",
      positions: ["month", "hour"],
      branches: [3, 9],
      description: "묘유충(卯酉沖) — 월지 묘목과 시지 유금이 상충한다.",
    },
  ],
} as const;

/** 전체 작용 — 합·충·형·공망 등 여러 탭이 모두 채워진 상태. */
export function AllInteractions() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 720 }}>
      <InteractionsTabs interactions={fullInteractions} />
    </div>
  );
}

/** 충 단일 탭 — 자오충·묘유충 두 건만 존재하는 케이스. */
export function ConflictOnly() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 720 }}>
      <InteractionsTabs interactions={conflictOnly} />
    </div>
  );
}
