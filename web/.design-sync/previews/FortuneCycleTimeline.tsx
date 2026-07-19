import { FortuneCycleTimeline } from "forceteller-web";

// 순행(順行) 대운 — 3세 시작, 壬辰부터 천간·지지가 한 칸씩 전진하는 8주기
const forwardCycles = [
  {
    start_age: 3,
    heavenly_stem: { hanja: "壬", korean: "임", element: "수" as const },
    earthly_branch: { hanja: "辰", korean: "진", element: "토" as const },
  },
  {
    start_age: 13,
    heavenly_stem: { hanja: "癸", korean: "계", element: "수" as const },
    earthly_branch: { hanja: "巳", korean: "사", element: "화" as const },
  },
  {
    start_age: 23,
    heavenly_stem: { hanja: "甲", korean: "갑", element: "목" as const },
    earthly_branch: { hanja: "午", korean: "오", element: "화" as const },
  },
  {
    start_age: 33,
    heavenly_stem: { hanja: "乙", korean: "을", element: "목" as const },
    earthly_branch: { hanja: "未", korean: "미", element: "토" as const },
  },
  {
    start_age: 43,
    heavenly_stem: { hanja: "丙", korean: "병", element: "화" as const },
    earthly_branch: { hanja: "申", korean: "신", element: "금" as const },
  },
  {
    start_age: 53,
    heavenly_stem: { hanja: "丁", korean: "정", element: "화" as const },
    earthly_branch: { hanja: "酉", korean: "유", element: "금" as const },
  },
  {
    start_age: 63,
    heavenly_stem: { hanja: "戊", korean: "무", element: "토" as const },
    earthly_branch: { hanja: "戌", korean: "술", element: "토" as const },
  },
  {
    start_age: 73,
    heavenly_stem: { hanja: "己", korean: "기", element: "토" as const },
    earthly_branch: { hanja: "亥", korean: "해", element: "수" as const },
  },
];

/** 대운 10년 주기 타임라인 — 순행 8주기, currentAge 37로 33~42세(乙未) 대운이 현재(★)로 강조. */
export function CurrentHighlighted() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 880 }}>
      <FortuneCycleTimeline cycles={forwardCycles} currentAge={37} />
    </div>
  );
}

/** 역행(逆行) 대운 — 8세 시작, 庚子부터 천간·지지가 한 칸씩 후퇴하는 6주기. currentAge 미지정(현재 강조 없음). */
export function ReverseDirection() {
  const reverseCycles = [
    {
      start_age: 8,
      heavenly_stem: { hanja: "庚", korean: "경", element: "금" as const },
      earthly_branch: { hanja: "子", korean: "자", element: "수" as const },
    },
    {
      start_age: 18,
      heavenly_stem: { hanja: "己", korean: "기", element: "토" as const },
      earthly_branch: { hanja: "亥", korean: "해", element: "수" as const },
    },
    {
      start_age: 28,
      heavenly_stem: { hanja: "戊", korean: "무", element: "토" as const },
      earthly_branch: { hanja: "戌", korean: "술", element: "토" as const },
    },
    {
      start_age: 38,
      heavenly_stem: { hanja: "丁", korean: "정", element: "화" as const },
      earthly_branch: { hanja: "酉", korean: "유", element: "금" as const },
    },
    {
      start_age: 48,
      heavenly_stem: { hanja: "丙", korean: "병", element: "화" as const },
      earthly_branch: { hanja: "申", korean: "신", element: "금" as const },
    },
    {
      start_age: 58,
      heavenly_stem: { hanja: "乙", korean: "을", element: "목" as const },
      earthly_branch: { hanja: "未", korean: "미", element: "토" as const },
    },
  ];
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 720 }}>
      <FortuneCycleTimeline cycles={reverseCycles} />
    </div>
  );
}

/** 첫 대운 강조 — currentAge 5로 3~12세(壬辰) 첫 주기가 현재로 표시되는 순행 흐름. */
export function FirstCycleCurrent() {
  return (
    <div style={{ padding: 16, background: "#ffffff", width: 880 }}>
      <FortuneCycleTimeline cycles={forwardCycles} currentAge={5} />
    </div>
  );
}
