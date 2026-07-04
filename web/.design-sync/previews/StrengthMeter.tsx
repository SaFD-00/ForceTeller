import { StrengthMeter } from "forceteller-web";

/** 신강 사주: 일간이 강한 케이스(score 72, is_strong true) */
export const StrongDay = () => (
  <div style={{ padding: 16, background: "#dfe7ff", width: 720 }}>
    <StrengthMeter
      analysis={{
        score: 72,
        is_strong: true,
        type: "신강",
        description:
          "일간 갑목(甲木)이 인묘진(寅卯辰) 목국과 정인의 생조를 받아 뿌리가 깊습니다. 비견과 정인의 기운이 왕성하여 자립심이 강하고 주체성이 뚜렷한 신강 사주입니다.",
      }}
    />
  </div>
);

/** 신약 사주: 일간이 약한 케이스(score 34, is_strong false) */
export const WeakDay = () => (
  <div style={{ padding: 16, background: "#dfe7ff", width: 720 }}>
    <StrengthMeter
      analysis={{
        score: 34,
        is_strong: false,
        type: "신약",
        description:
          "일간 정화(丁火)가 신유술(申酉戌) 금국에 둘러싸여 편관과 정재의 설기가 심합니다. 인성의 생조가 부족하여 의지처가 약한 신약 사주로, 식신·상관의 활용에 주의가 필요합니다.",
      }}
    />
  </div>
);

/** 균형에 가까운 사주: score 50 부근, type/description 생략(옵셔널 필드 미지정) */
export const Balanced = () => (
  <div style={{ padding: 16, background: "#dfe7ff", width: 720 }}>
    <StrengthMeter
      analysis={{
        score: 51,
        is_strong: true,
      }}
    />
  </div>
);
