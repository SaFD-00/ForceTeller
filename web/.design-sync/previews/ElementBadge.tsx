import { ElementBadge } from "forceteller-web";

/** 오행(五行) 배지 — 한자 + 한글, 목·화·토·금·수 전체. */
export function AllElements() {
  return (
    <div style={{ display: "flex", gap: 8, padding: 16, background: "#ffffff", flexWrap: "wrap" }}>
      <ElementBadge element="목" />
      <ElementBadge element="화" />
      <ElementBadge element="토" />
      <ElementBadge element="금" />
      <ElementBadge element="수" />
    </div>
  );
}

/** 크기 변형 — sm / md / lg. */
export function Sizes() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8, padding: 16, background: "#ffffff" }}>
      <ElementBadge element="수" size="sm" />
      <ElementBadge element="수" size="md" />
      <ElementBadge element="수" size="lg" />
    </div>
  );
}

/** 한자만 표시(이름 숨김) — 표·차트 라벨용. */
export function HanjaOnly() {
  return (
    <div style={{ display: "flex", gap: 8, padding: 16, background: "#ffffff" }}>
      <ElementBadge element="목" showName={false} />
      <ElementBadge element="화" showName={false} />
      <ElementBadge element="토" showName={false} />
      <ElementBadge element="금" showName={false} />
      <ElementBadge element="수" showName={false} />
    </div>
  );
}
