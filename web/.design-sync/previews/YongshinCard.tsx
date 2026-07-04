import { YongshinCard } from "forceteller-web";

/** 억부용신 — 신약한 일간을 돕는 인성(印星) 오행으로 수(水)를 용신으로 잡은 경우 */
export function EokbuYongshin() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 520 }}>
      <YongshinCard
        type="억부용신"
        element="수"
        hanja="水"
        description="일간 갑목(甲木)이 신약하여 일간을 생조하는 인성 오행인 수(水)를 용신으로 삼습니다. 수는 목을 자양하여 뿌리를 튼튼하게 하고, 정인(正印)의 기운으로 학업과 명예를 북돋습니다."
      />
    </div>
  );
}

/** 조후용신 — 한겨울 출생으로 기후를 조절하는 화(火) 오행을 용신으로 잡은 경우 */
export function JohuYongshin() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 520 }}>
      <YongshinCard
        type="조후용신"
        element="화"
        hanja="火"
        description="자월(子月) 엄동에 태어나 사주가 한랭하므로 따뜻한 화(火) 오행으로 기후를 조절합니다. 병화(丙火)의 온기가 얼어붙은 임수(壬水)를 녹여 생기를 불어넣습니다."
      />
    </div>
  );
}

/** 통관용신 — 상충하는 금(金)과 목(木) 사이를 소통시키는 수(水)를 용신으로 잡은 경우 */
export function TonggwanYongshin() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 520 }}>
      <YongshinCard
        type="통관용신"
        element="수"
        hanja="水"
        description="경금(庚金)과 갑목(甲木)이 금극목(金剋木)으로 대치하는 형국에서, 두 기운을 이어주는 수(水)를 통관용신으로 삼습니다. 수가 금생수·수생목으로 흐름을 만들어 상극을 상생으로 전환합니다."
      />
    </div>
  );
}

/** 설명 없는 간결형 — hanja·description 생략 시 오행 기본 한자(土)로 폴백되는 모습 */
export function YongshinCompact() {
  return (
    <div style={{ padding: 16, background: "#dfe7ff", width: 320 }}>
      <YongshinCard type="병약용신" element="토" />
    </div>
  );
}
