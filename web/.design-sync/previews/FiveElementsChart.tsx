import { FiveElementsChart } from "forceteller-web";
import type { FiveElementsDisplay } from "@/types/saju";

/** 균형 잡힌 사주: 화 주도·금 부족, 용신 수·기신 화 */
export const Balanced = () => {
  const analysis: FiveElementsDisplay = {
    distribution: { 목: 2, 화: 4, 토: 2, 금: 1, 수: 3 },
    dominant: "화",
    lacking: "금",
    yongshin: "수",
    gishin: "화",
  };
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480, height: 360 }}>
      <FiveElementsChart analysis={analysis} />
    </div>
  );
};

/** 목 편중 사주: 목 과다·금 전무, 용신 금·기신 목 */
export const WoodHeavy = () => {
  const analysis: FiveElementsDisplay = {
    distribution: { 목: 6, 화: 3, 토: 1, 금: 0, 수: 2 },
    dominant: "목",
    lacking: "금",
    yongshin: "금",
    gishin: "목",
  };
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480, height: 360 }}>
      <FiveElementsChart analysis={analysis} />
    </div>
  );
};

/** 수 편중 사주: 수 왕성·토 부족, 용신 토·기신 수 */
export const WaterHeavy = () => {
  const analysis: FiveElementsDisplay = {
    distribution: { 목: 3, 화: 1, 토: 1, 금: 2, 수: 5 },
    dominant: "수",
    lacking: "토",
    yongshin: "토",
    gishin: "수",
  };
  return (
    <div style={{ padding: 16, background: "#f7f8fa", width: 480, height: 360 }}>
      <FiveElementsChart analysis={analysis} />
    </div>
  );
};
