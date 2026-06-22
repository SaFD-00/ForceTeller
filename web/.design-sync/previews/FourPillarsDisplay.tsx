import { FourPillarsDisplay } from "forceteller-web";

// 庚午 · 辛巳 · 甲寅 · 己巳 — 일간 갑목(甲木) 예시 사주 (시주 포함)
const pillars = {
  year: {
    heavenly_stem: { hanja: "庚", korean: "경", element: "금" as const },
    earthly_branch: {
      hanja: "午",
      korean: "오",
      element: "화" as const,
      hidden_stems: [
        { korean: "병", chinese: "丙", element: "화", type: "여기", ratio: 30, ten_god: "식신" },
        { korean: "기", chinese: "己", element: "토", type: "본기", ratio: 70, ten_god: "정재" },
      ],
    },
    ten_god: "편관",
    twelve_phase: "사",
  },
  month: {
    heavenly_stem: { hanja: "辛", korean: "신", element: "금" as const },
    earthly_branch: {
      hanja: "巳",
      korean: "사",
      element: "화" as const,
      hidden_stems: [
        { korean: "병", chinese: "丙", element: "화", type: "본기", ratio: 60, ten_god: "식신" },
        { korean: "무", chinese: "戊", element: "토", type: "중기", ratio: 25, ten_god: "편재" },
        { korean: "경", chinese: "庚", element: "금", type: "여기", ratio: 15, ten_god: "편관" },
      ],
    },
    ten_god: "정관",
    twelve_phase: "병",
  },
  day: {
    heavenly_stem: { hanja: "甲", korean: "갑", element: "목" as const },
    earthly_branch: {
      hanja: "寅",
      korean: "인",
      element: "목" as const,
      hidden_stems: [
        { korean: "갑", chinese: "甲", element: "목", type: "본기", ratio: 60, ten_god: "비견" },
        { korean: "병", chinese: "丙", element: "화", type: "중기", ratio: 30, ten_god: "식신" },
        { korean: "무", chinese: "戊", element: "토", type: "여기", ratio: 10, ten_god: "편재" },
      ],
    },
    ten_god: null,
    twelve_phase: "건록",
  },
  hour: {
    heavenly_stem: { hanja: "己", korean: "기", element: "토" as const },
    earthly_branch: {
      hanja: "巳",
      korean: "사",
      element: "화" as const,
      hidden_stems: [
        { korean: "병", chinese: "丙", element: "화", type: "본기", ratio: 60, ten_god: "식신" },
        { korean: "무", chinese: "戊", element: "토", type: "중기", ratio: 25, ten_god: "정재" },
        { korean: "경", chinese: "庚", element: "금", type: "여기", ratio: 15, ten_god: "정관" },
      ],
    },
    ten_god: "정재",
    twelve_phase: "병",
  },
};

/** 사주팔자(四柱八字) 4기둥 카드 — 년·월·일·시주 천간/지지 + 오행 뱃지·십성. */
export function FullChart() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 720 }}>
      <FourPillarsDisplay pillars={pillars} />
    </div>
  );
}

/** 일간(日干) 무토(戊土) 사주 예시 — 戊子 · 乙卯 · 戊辰 · 壬戌 (수·목 혼재). */
export function EarthDayMaster() {
  const earthPillars = {
    year: {
      heavenly_stem: { hanja: "戊", korean: "무", element: "토" as const },
      earthly_branch: {
        hanja: "子",
        korean: "자",
        element: "수" as const,
        hidden_stems: [
          { korean: "계", chinese: "癸", element: "수", type: "본기", ratio: 100, ten_god: "정재" },
        ],
      },
      ten_god: "비견",
      twelve_phase: "태",
    },
    month: {
      heavenly_stem: { hanja: "乙", korean: "을", element: "목" as const },
      earthly_branch: {
        hanja: "卯",
        korean: "묘",
        element: "목" as const,
        hidden_stems: [
          { korean: "을", chinese: "乙", element: "목", type: "본기", ratio: 100, ten_god: "정관" },
        ],
      },
      ten_god: "정관",
      twelve_phase: "목욕",
    },
    day: {
      heavenly_stem: { hanja: "戊", korean: "무", element: "토" as const },
      earthly_branch: {
        hanja: "辰",
        korean: "진",
        element: "토" as const,
        hidden_stems: [
          { korean: "무", chinese: "戊", element: "토", type: "본기", ratio: 60, ten_god: "비견" },
          { korean: "을", chinese: "乙", element: "목", type: "중기", ratio: 20, ten_god: "정관" },
          { korean: "계", chinese: "癸", element: "수", type: "여기", ratio: 20, ten_god: "정재" },
        ],
      },
      ten_god: null,
      twelve_phase: "관대",
    },
    hour: {
      heavenly_stem: { hanja: "壬", korean: "임", element: "수" as const },
      earthly_branch: {
        hanja: "戌",
        korean: "술",
        element: "토" as const,
        hidden_stems: [
          { korean: "무", chinese: "戊", element: "토", type: "본기", ratio: 60, ten_god: "비견" },
          { korean: "신", chinese: "辛", element: "금", type: "중기", ratio: 20, ten_god: "상관" },
          { korean: "정", chinese: "丁", element: "화", type: "여기", ratio: 20, ten_god: "정인" },
        ],
      },
      ten_god: "편재",
      twelve_phase: "묘",
    },
  };
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 720 }}>
      <FourPillarsDisplay pillars={earthPillars} />
    </div>
  );
}
