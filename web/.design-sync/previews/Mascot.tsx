import { Mascot, MascotBubble } from "forceteller-web";

const moods = ["idle", "happy", "thinking", "talking", "curious", "sleeping"] as const;

/** 표정(mood) 6종 — 별·달 점성술사 "별이". */
export function Moods() {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 20, padding: 24, background: "#ffffff" }}>
      {moods.map((m) => (
        <div key={m} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
          <Mascot mood={m} size="lg" />
          <code style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: "#263D5B" }}>{m}</code>
        </div>
      ))}
    </div>
  );
}

/** 크기(size) 5종. */
export function Sizes() {
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 20, padding: 24, background: "#ffffff" }}>
      <Mascot mood="happy" size="xs" />
      <Mascot mood="happy" size="sm" />
      <Mascot mood="happy" size="md" />
      <Mascot mood="happy" size="lg" />
      <Mascot mood="happy" size="xl" />
    </div>
  );
}

/** 말풍선 헬퍼 — 설명봇/빈상태 재사용. */
export function WithBubble() {
  return (
    <div style={{ padding: 24, background: "#ffffff", width: 420 }}>
      <MascotBubble mood="curious">
        일간이 <b>갑목(甲木)</b>이면 곧게 뻗는 기질이에요. 궁금한 점을 물어보세요!
      </MascotBubble>
    </div>
  );
}
