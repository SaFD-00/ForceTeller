import { FortuneScoreDashboard } from "forceteller-web";

/** 종합운/직업운/재물운/건강운/애정운 5개 운세 점수가 모두 채워진 전체 대시보드 (첫 항목 펼침) */
export function AllFortunes() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 560 }}>
      <FortuneScoreDashboard
        scores={{
          general: {
            score: 78,
            summary:
              "병화(丙火) 일간이 인목(寅木) 정인의 생을 받아 기운이 안정적입니다. 올해는 식신이 발현되어 새로운 시도가 결실을 맺는 흐름입니다.",
            positive: ["정인의 후원이 두텁다", "식신 발현으로 표현력이 좋다"],
            negative: ["편관의 압박으로 조급해질 수 있다"],
            advice: ["서두르지 말고 단계적으로 추진하세요", "주변의 조언을 경청하면 길합니다"],
            lucky_colors: ["적색", "녹색"],
            lucky_numbers: [3, 8],
            lucky_directions: ["남", "동"],
          },
          career: {
            score: 64,
            summary: "정관이 뚜렷해 조직 내 신뢰가 쌓이는 시기이나, 상관의 견제로 윗사람과 마찰이 생길 수 있습니다.",
            positive: ["정관으로 책임 있는 자리를 맡는다"],
            negative: ["상관이 정관을 극해 구설이 따른다"],
            advice: ["말을 아끼고 실적으로 증명하세요"],
            lucky_colors: ["청색"],
            lucky_numbers: [1, 6],
            lucky_directions: ["북"],
          },
          wealth: {
            score: 52,
            summary: "정재가 자리해 안정적인 수입이 유지되나, 편재의 변동성으로 투기성 지출은 삼가야 합니다.",
            positive: ["정재로 꾸준한 재물운"],
            negative: ["겁재가 재물을 분탈할 우려"],
            advice: ["보수적인 자산 운용이 유리합니다"],
            lucky_colors: ["황색", "백색"],
            lucky_numbers: [5, 0],
            lucky_directions: ["중앙", "서"],
          },
          health: {
            score: 41,
            summary: "화(火) 기운이 왕성하고 수(水)가 부족해 심혈관과 수분 대사에 유의가 필요한 해입니다.",
            positive: ["기본 체력은 양호하다"],
            negative: ["화기 과다로 염증·과열 주의"],
            advice: ["충분한 수분 섭취와 휴식을 권합니다"],
            lucky_colors: ["흑색"],
            lucky_numbers: [1, 6],
            lucky_directions: ["북"],
          },
          love: {
            score: 70,
            summary: "정재(여명은 정관)가 일지와 합을 이뤄 인연이 무르익습니다. 진실한 만남이 기대되는 흐름입니다.",
            positive: ["일지 합으로 좋은 인연이 든다"],
            negative: ["편인의 간섭으로 오해가 생길 수 있다"],
            advice: ["솔직한 대화로 신뢰를 쌓으세요"],
            lucky_colors: ["분홍색", "적색"],
            lucky_numbers: [2, 7],
            lucky_directions: ["남"],
          },
        }}
      />
    </div>
  );
}

/** 종합운 단일 항목 + 낮은 점수(흉) 케이스 — 점수바 색상이 위험 구간(rose)으로 표시되는 모습 */
export function LowScoreSingle() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480 }}>
      <FortuneScoreDashboard
        scores={{
          general: {
            score: 28,
            summary:
              "경금(庚金) 일간이 화(火) 편관의 극을 강하게 받아 부담이 큰 시기입니다. 무리한 확장보다 내실을 다질 때입니다.",
            positive: ["겁재의 도움으로 위기 시 조력자가 있다"],
            negative: ["편관 과다로 스트레스·압박이 심하다", "정인이 약해 회복이 더디다"],
            advice: ["큰 결정을 미루고 휴식을 우선하세요", "건강 관리에 특히 신경 쓰세요"],
            lucky_colors: ["황색", "백색"],
            lucky_numbers: [5, 10],
            lucky_directions: ["중앙", "서"],
          },
        }}
      />
    </div>
  );
}

/** 재물운·애정운 2개 항목만 제공된 부분 케이스 — advice/행운색/방위 부가 정보 렌더 확인 */
export function PartialFortunes() {
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 520 }}>
      <FortuneScoreDashboard
        scores={{
          wealth: {
            score: 85,
            summary: "정재와 편재가 균형을 이루고 식신이 재성을 생하니, 노력한 만큼 재물이 쌓이는 풍요로운 해입니다.",
            positive: ["식신생재로 재원이 풍부하다", "정재로 안정적 수입"],
            negative: ["편재 욕심으로 과욕은 금물"],
            advice: ["꾸준한 저축이 더 큰 결실로 돌아옵니다", "신뢰 기반의 거래를 우선하세요"],
            lucky_colors: ["황색", "금색"],
            lucky_numbers: [5, 9],
            lucky_directions: ["중앙", "서"],
          },
          love: {
            score: 58,
            summary: "일지 인성(印星)이 자리해 정서적 안정이 깊으나, 표현이 서툴러 인연을 놓칠 수 있습니다.",
            positive: ["인성으로 따뜻하고 배려심이 깊다"],
            negative: ["상관의 변덕으로 마음이 자주 흔들린다"],
            advice: ["마음을 적극적으로 표현해 보세요"],
            lucky_colors: ["녹색", "청색"],
            lucky_numbers: [3, 8],
            lucky_directions: ["동", "남동"],
          },
        }}
      />
    </div>
  );
}
