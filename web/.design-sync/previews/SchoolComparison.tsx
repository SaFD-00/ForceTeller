import { SchoolComparison } from "forceteller-web";
import type { SchoolComparisonResult } from "@/types/saju";

const fullComparison: SchoolComparisonResult = {
  schools: ["ziping", "dts", "qtbj", "modern", "shensha"],
  interpretations: [
    {
      school: "ziping",
      school_name: "자평명리",
      yong_sin: "금(金)",
      geok_guk: "정관격",
      overall:
        "병화(丙火) 일간이 신월(申月)에 태어나 인성과 비겁이 적절히 받쳐주는 사주입니다. 정관이 투출해 격이 맑습니다.",
      health: "폐와 대장 계통이 무난하나 가을·겨울 환절기 호흡기 관리가 필요합니다.",
      wealth: "정재가 자리를 지켜 안정적 축재가 가능하며 무리한 투기는 삼가야 합니다.",
      career: "정관격 특성상 조직 내 관리·행정·공직 계열에서 두각을 나타냅니다.",
      relationship: "정관·정인이 조화로워 신뢰 기반의 인연을 오래 이어갑니다.",
      fame: "원칙을 지키는 처신으로 중년 이후 사회적 신망이 두터워집니다.",
      confidence: 0.86,
      key_features: ["정관격", "신약", "금 용신", "병화 일간"],
    },
    {
      school: "dts",
      school_name: "적천수",
      yong_sin: "수(水)",
      geok_guk: "종관격 경향",
      overall:
        "적천수 관점에서는 일간의 기세보다 전체 기운의 흐름을 중시합니다. 임수(壬水)가 조후를 잡아 청기를 띱니다.",
      health: "수기(水氣)가 부족하지 않아 신장·방광이 견실한 편입니다.",
      wealth: "통관 기운이 재성으로 흘러 재물의 출입이 활발합니다.",
      career: "유통·중개·물류 등 흐름을 다루는 직군과 합이 좋습니다.",
      relationship: "감정의 기복이 있으나 수기가 윤활해 관계 회복이 빠릅니다.",
      fame: "기세를 따르는 처신으로 시류에 맞는 평판을 얻습니다.",
      confidence: 0.74,
      key_features: ["조후 중시", "수 용신", "청기", "기세론"],
    },
    {
      school: "qtbj",
      school_name: "궁통보감",
      yong_sin: "수(水)",
      geok_guk: "조후용신격",
      overall:
        "신월(申月) 병화는 화기가 쇠하는 시기이므로 조후로 임수(壬水)를 우선하고 경금(庚金)으로 보좌합니다.",
      health: "조열을 식히는 수기 보강으로 심혈관·순환계가 안정됩니다.",
      wealth: "계절 조후가 맞아 재물운이 시기적으로 무르익습니다.",
      career: "절기의 균형을 읽는 기획·연구 직무에 적합합니다.",
      relationship: "조후가 맞는 배우자를 만나면 가정이 윤택해집니다.",
      fame: "때를 아는 처신으로 적절한 시점에 명예가 따릅니다.",
      confidence: 0.7,
      key_features: ["조후론", "임수 우선", "경금 보좌", "신월 병화"],
    },
  ],
  consensus: [
    {
      category: "yongsin",
      agreement: "신약한 병화 일간을 돕고 조후를 잡는 수(水)·금(金) 기운이 핵심 용신이라는 데 의견이 모입니다.",
      schools: ["ziping", "dts", "qtbj"],
    },
    {
      category: "career",
      agreement: "원칙과 흐름을 함께 다루는 행정·관리·기획 계열 직업이 길하다고 봅니다.",
      schools: ["ziping", "dts"],
    },
    {
      category: "health",
      agreement: "환절기 호흡기와 순환계 관리에 유의해야 한다는 점에 동의합니다.",
      schools: ["ziping", "qtbj"],
    },
  ],
  differences: [
    {
      category: "yongsin",
      interpretations: [
        {
          school: "ziping",
          school_name: "자평명리",
          interpretation: "격국을 맑게 하는 금(金) 재성을 용신으로 우선합니다.",
        },
        {
          school: "qtbj",
          school_name: "궁통보감",
          interpretation: "신월의 조열을 식히는 수(水) 조후를 용신으로 우선합니다.",
        },
      ],
    },
  ],
  recommendation:
    "세 학파 모두 신약한 병화 일간을 돕는 수·금 기운을 권합니다. 직업은 행정·기획 계열, 거주·활동 방향은 북·서가 길합니다.",
  confidence: 0.82,
};

const dividedComparison: SchoolComparisonResult = {
  schools: ["modern", "shensha"],
  interpretations: [
    {
      school: "modern",
      school_name: "현대명리",
      yong_sin: "토(土)",
      overall:
        "통계와 심리 모델을 결합한 현대명리는 무토(戊土) 식상이 강한 표현·실행형 기질을 강조합니다.",
      health: "위장·소화기 부담을 관리하면 활동성을 길게 유지할 수 있습니다.",
      wealth: "식상생재 구조로 콘텐츠·창작 기반 수익 가능성이 높습니다.",
      career: "기획·마케팅·1인 미디어 등 표현 기반 직군이 강점입니다.",
      relationship: "솔직한 표현이 강점이자 갈등 요인이 될 수 있습니다.",
      fame: "대중성과 개인 브랜딩으로 빠른 인지도 상승이 가능합니다.",
      confidence: 0.58,
      key_features: ["식상 발달", "토 용신", "표현형", "통계 기반"],
    },
    {
      school: "shensha",
      school_name: "신살중심",
      yong_sin: "화(火)",
      geok_guk: "역마·문창 동궁",
      overall:
        "신살중심 해석은 역마(驛馬)와 문창(文昌)이 동궁하여 이동과 학문·문서 운이 두드러진다고 봅니다.",
      health: "역마가 동하므로 이동 중 안전과 과로 누적을 경계해야 합니다.",
      wealth: "타지·해외에서의 재물 기회가 열리는 구조입니다.",
      career: "출장·해외·교육·집필 등 이동과 문서가 결합된 직군이 길합니다.",
      relationship: "도화(桃花)가 약하게 비쳐 인연의 변동 폭이 큽니다.",
      fame: "문창의 힘으로 글·자격·시험을 통한 명예 상승이 기대됩니다.",
      confidence: 0.41,
      key_features: ["역마", "문창", "도화", "화 용신"],
    },
  ],
  consensus: [],
  differences: [
    {
      category: "yongsin",
      interpretations: [
        {
          school: "modern",
          school_name: "현대명리",
          interpretation: "식상을 설기·조율하는 토(土)를 핵심으로 봅니다.",
        },
        {
          school: "shensha",
          school_name: "신살중심",
          interpretation: "신살의 활성을 돕는 화(火) 기운을 우선합니다.",
        },
      ],
    },
  ],
  recommendation:
    "두 학파의 용신과 직업 해석이 엇갈립니다. 현대명리는 토 기반 표현 직군을, 신살중심은 화 기반 이동·문서 직군을 권하므로 본인의 성향을 함께 고려하세요.",
  confidence: 0.45,
};

/** 3개 학파(자평명리·적천수·궁통보감)가 폭넓게 합의하는 고신뢰 비교 해석 — 종합 권장·공통 견해·학파별 탭 전체 노출. */
export function ConsensusHigh() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 760 }}>
      <SchoolComparison comparison={fullComparison} />
    </div>
  );
}

/** 현대명리·신살중심 2개 학파의 용신·직업 해석이 엇갈리는 저신뢰('해석 분분') 케이스 — 공통 견해 없이 차이 위주. */
export function ConsensusDivided() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 760 }}>
      <SchoolComparison comparison={dividedComparison} />
    </div>
  );
}
