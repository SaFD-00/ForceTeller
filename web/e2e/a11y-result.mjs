// 잔여 접근성 수정의 렌더 결과를 실측한다.
// 코드 리뷰가 아니라 getComputedStyle 로 실제 대비를 계산해 판정한다.
import { BASE, artifact, launchBrowser, loadMock } from './lib/harness.mjs';

const MOCK = loadMock();
const TEN_GOD_RAMP = ['#748BAF', '#637DA6', '#43587B', '#3A4D6C', '#1E293B', '#131A25', '#57709A', '#4D648B', '#31425C', '#28364C'];
const SELFTEST = process.env.A11Y_SELFTEST === '1';

// ============================================================================
// 기대값 빌더 — 렌더 결과를 "무엇과" 대조할지 mock 으로부터 계산한다.
// 여기 공식은 컴포넌트 공식의 미러다. SSOT 는 각 주석의 코드 위치.
// ============================================================================
// SSOT: web/components/result/ElementDistribution.tsx:49
const TEN_GOD_ORDER = ['비견', '겁재', '식신', '상관', '편재', '정재', '편관', '정관', '편인', '정인'];
// SSOT: web/components/result/ElementDistribution.tsx:100
const ELEMENT_ORDER = ['목', '화', '토', '금', '수'];
// SSOT: ElementDistribution.tsx:102-105 getPercentage (소수 첫째자리)
const pct1 = (v, t) => (t === 0 ? 0 : Math.round((v / t) * 1000) / 10);
// SSOT: PentagonChart.tsx:185 (정수 반올림)
const pct0 = (v, t) => (t > 0 ? Math.round((v / t) * 100) : 0);

const DIST = MOCK.five_elements.distribution;
const TENGODS = MOCK.ten_gods.counts;
// 컴포넌트는 Object.values 전체 합을 total 로 쓴다 (ElementDistribution.tsx:63-64, PentagonChart.tsx:71)
const DIST_TOTAL = Object.values(DIST).reduce((s, v) => s + (v || 0), 0);
const TENGOD_TOTAL = Object.values(TENGODS).reduce((s, v) => s + (v || 0), 0);

// SSOT: ElementDistribution.tsx:114-118 — 오행은 0% 항목도 포함
const EXPECT_ARIA_OHENG =
  '오행 분포: ' + ELEMENT_ORDER.map((e) => `${e} ${pct1(DIST[e] || 0, DIST_TOTAL)}%`).join(', ');
// SSOT: ElementDistribution.tsx:119-124 — 오행과 동일하게 0% 항목도 포함한다.
// aria 는 시각 범례의 대체 채널이라 정보 집합이 같아야 한다(범례도 10개 전부 렌더).
const TENGOD_ARIA_INCLUDE = () => true;
const EXPECT_ARIA_TENGOD =
  '십성 분포: ' +
  TEN_GOD_ORDER.map((god) => ({ god, p: pct1(TENGODS[god] || 0, TENGOD_TOTAL) }))
    .filter(({ p }) => TENGOD_ARIA_INCLUDE(p))
    .map(({ god, p }) => `${god} ${p}%`)
    .join(', ');
// 오각형은 일간 기준으로 배치가 회전하므로 순서가 아니라 multiset 으로 비교한다.
const EXPECT_PENTAGON_PCTS = ELEMENT_ORDER.map((e) => pct0(DIST[e] || 0, DIST_TOTAL)).sort((a, b) => a - b);
// 도넛 세그먼트 수 = 비영 항목 수 (0% 는 null 반환이라 circle 이 안 나온다)
const EXPECT_DONUT_NS = [
  ELEMENT_ORDER.filter((e) => pct1(DIST[e] || 0, DIST_TOTAL) > 0).length,
  TEN_GOD_ORDER.filter((g) => pct1(TENGODS[g] || 0, TENGOD_TOTAL) > 0).length,
].sort((a, b) => a - b);

// 위 기대값은 mock 에서 파생된다 = mock 이 바뀌면 기대값도 조용히 따라 움직인다.
// 아래 sanity 핀이 그 순환 통과를 막는다 (핀과 어긋나면 즉시 FAIL).
const SANITY_FAILS = [];
if (EXPECT_ARIA_OHENG !== '오행 분포: 목 33.3%, 화 22.2%, 토 22.2%, 금 22.2%, 수 0%')
  SANITY_FAILS.push(`SANITY: 오행 aria 기대값이 핀과 다름 — "${EXPECT_ARIA_OHENG}"`);
if (JSON.stringify(EXPECT_PENTAGON_PCTS) !== '[0,22,22,22,33]')
  SANITY_FAILS.push(`SANITY: 오각형 % 기대 multiset 이 핀과 다름 — ${JSON.stringify(EXPECT_PENTAGON_PCTS)}`);
if (JSON.stringify(EXPECT_DONUT_NS) !== '[4,8]')
  SANITY_FAILS.push(`SANITY: 도넛 세그먼트 수 기대가 핀과 다름 — ${JSON.stringify(EXPECT_DONUT_NS)}`);

// 오각형 % 텍스트는 꼭지점 5개 = 정확히 5개여야 한다 (slice 로 잘라 세면 개수 결함을 못 본다).
const EXPECT_PENTAGON_PCT_TEXTS = 5;
// 탭 아이콘 대비 후보 총수 — 현행 HEAD 프로덕션 렌더('유형별 보기' 토글 후) 1회 실측 핀.
// 내역: iconify svg 8 + button 2('주별 보기' + 신살 카드 버튼) + 배지 span 2(일주/년주)
//       + 신살 설명 p 4 = 16.
// 주의: 셀렉터 이름은 "탭 아이콘"이지만 실제로는 button 하위의 모든
//       text-success / text-danger / text-muted-foreground 요소를 잡는다. 개수를 못 박아
//       "후보가 사라져 조용히 0건 통과"와 "새 후보가 늘었는데 캡에 잘려 안 보임"을 둘 다 막는다.
const EXPECT_TAB_CANDIDATES = 16;
// 도넛은 오행/십성 2개 차트다.
const EXPECT_DONUT_CHARTS = 2;

const browser = await launchBrowser();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
const page = await ctx.newPage();
const errs = [];
page.on('pageerror', (e) => errs.push(e.message.slice(0, 160)));
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)); });

await page.addInitScript((m) => {
  localStorage.setItem('saju-storage', JSON.stringify({ state: { result: m }, version: 0 }));
}, MOCK);

await page.goto(BASE + '/result', { waitUntil: 'networkidle', timeout: 90000 });
await page.waitForTimeout(2500);

// --- 셀프테스트: 하네스가 결함을 실제로 잡는지 검증하는 변이 주입 ---
// A11Y_SELFTEST=1 이면 알려진 결함 4종을 DOM 에 심는다. 기대: exit 1 +
// ARROWS: / ARIA: / P3: / GUARD: 계열 fail 이 각각 최소 1건.
// (멱등하게 짜서 React 리렌더로 되돌아가도 재적용할 수 있게 한다.)
async function applySelfTestMutations() {
  if (!SELFTEST) return;
  await page.evaluate(() => {
    // (a) 오각형 화살촉 defs 제거 → markerDefs 0 / dangling 10 → ARROWS:
    document.querySelectorAll('svg[viewBox="0 0 300 300"] defs marker').forEach((m) => m.remove());
    // (b) 오행 도넛 aria-label 변조 → ARIA:
    const oheng = document.querySelector('svg[aria-label^="오행 분포:"]');
    if (oheng) oheng.setAttribute('aria-label', '오행 분포: 목 99%');
    // (c) 십성 범례 아이템 1개 제거 → 10→9 → P3:
    const legend = document.querySelector('[data-legend="ten-gods"]');
    while (legend && legend.children.length > 9) legend.lastElementChild.remove();
    // (d) 오각형 % 텍스트 전부 제거 → 5→0 → GUARD:
    const pent = document.querySelector('svg[viewBox="0 0 300 300"]');
    if (pent) [...pent.querySelectorAll('text')].filter((t) => /%/.test(t.textContent)).forEach((t) => t.remove());
  });
}
if (SELFTEST) {
  console.log('!!! A11Y_SELFTEST=1 — 변이 주입 모드. 이 실행의 FAIL 은 하네스 자체 검증이다 !!!\n');
  await applySelfTestMutations();
}

// --- 렌더 가드 ---
// 빈/깨진 페이지는 "위반 0건"으로 조용히 통과한다. 실제로 결과 페이지가 그려졌는지 먼저 못 박는다.
// (dev 서버의 .next 를 npm run build 가 덮어써서 500이 나는데도 PASS 로 읽힌 적이 있다.)
{
  const probe = await page.evaluate(() => ({
    textNodes: document.querySelectorAll('span, p, div, td, li').length,
    hasPentagon: !!document.querySelector('svg[viewBox="0 0 300 300"]'),
    donuts: [...document.querySelectorAll('circle')].filter((c) => getComputedStyle(c).strokeDasharray !== 'none').length,
    body: document.body.innerText.replace(/\s+/g, ' ').slice(0, 60),
  }));
  const fail = [];
  if (probe.textNodes < 200) fail.push(`요소 ${probe.textNodes}개뿐 (기대 200+)`);
  if (!probe.hasPentagon) fail.push('오각형 차트 미렌더');
  if (probe.donuts < 5) fail.push(`도넛 세그먼트 ${probe.donuts}개 (기대 5+)`);
  if (fail.length) {
    console.error('!!! 렌더 가드 실패 — 측정 무효, PASS로 읽지 마라 !!!');
    fail.forEach((f) => console.error('  - ' + f));
    console.error('  본문: ' + probe.body);
    await browser.close();
    process.exit(1);
  }
  console.log(`렌더 가드 통과: 요소 ${probe.textNodes}개, 오각형 O, 도넛 세그먼트 ${probe.donuts}개\n`);
}

// ShenshaDetailCard "유형별 보기" 토글 — 이 뒤에만 보이는 잠재 위반(중첩 틴트)을 노출시킨다.
const typeViewBtn = page.getByText('유형별 보기', { exact: true });
if (await typeViewBtn.count()) {
  await typeViewBtn.click();
  await page.waitForTimeout(500);
}
// bgAtPoint 는 document.elementsFromPoint = "뷰포트 좌표" 기반이다.
// 오각형 차트는 페이지 한참 아래(y≈1600, 뷰포트 높이 1000)라 스크롤 없이는 스택이 항상 []이고,
// bgAtPoint 가 조용히 기본값 흰색을 돌려줬다 — 그래서 vsActual 이 늘 vsWhite 와 똑같았다.
// 즉 "실제 틴트 배경 기준 판정"이 한 번도 실행된 적이 없다. 측정 전에 뷰포트로 끌어온다.
await page.locator('svg[viewBox="0 0 300 300"]').first().scrollIntoViewIfNeeded();
await page.waitForTimeout(300);

// 토글로 리렌더가 일어나면 변이가 되돌아갈 수 있으므로 측정 직전에 재적용한다(멱등).
await applySelfTestMutations();

// 브라우저 안에 대비 계산기를 심는다 (실제 렌더된 색 기준)
const report = await page.evaluate(() => {
  const srgb = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const lum = ([r, g, b]) => 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b);
  const parse = (s) => (s.match(/[\d.]+/g) || []).slice(0, 4).map(Number);
  const ratio = (fg, bg) => {
    const a = lum(fg) + 0.05, b = lum(bg) + 0.05;
    return +(Math.max(a, b) / Math.min(a, b)).toFixed(2);
  };
  // 알파 합성: 조상 방향으로 배경 레이어를 모은 뒤, 가장 아래(불투명)부터 위로 합성한다.
  // (앞 버전은 첫 레이어를 자기 자신과 합성해 틴트를 불투명색으로 만드는 버그가 있었다.)
  const effectiveBg = (el) => {
    const layers = [];
    let node = el;
    while (node && node.nodeType === 1) {
      const bg = parse(getComputedStyle(node).backgroundColor);
      if (bg.length >= 3) {
        const a = bg.length === 4 ? bg[3] : 1;
        if (a > 0) {
          layers.push({ c: bg.slice(0, 3), a });
          if (a === 1) break; // 불투명 레이어를 만나면 그 아래는 보이지 않는다
        }
      }
      node = node.parentElement;
    }
    let base = [255, 255, 255]; // 불투명 레이어를 못 찾으면 페이지 흰 배경
    if (layers.length && layers[layers.length - 1].a === 1) base = layers.pop().c;
    // 아래에서 위로: base 위에 반투명 레이어를 순서대로 얹는다
    for (let i = layers.length - 1; i >= 0; i--) {
      const { c, a } = layers[i];
      base = base.map((v, k) => c[k] * a + v * (1 - a));
    }
    return base;
  };

  // 특정 화면 좌표(x,y)의 실제 배경을 elementsFromPoint 스택으로 실측한다.
  // (조상 체인만 보는 effectiveBg 는 SVG 안에서 텍스트 "아래 깔린 도형"을 못 본다 —
  // 도형은 조상이 아니라 같은 그림 안의 형제 요소이기 때문이다.)
  function bgAtPoint(x, y, selfEl) {
    const stack = document.elementsFromPoint(x, y);
    const layers = [];
    for (const node of stack) {
      if (!node || node === selfEl || selfEl.contains(node)) continue;
      const tag = node.tagName ? node.tagName.toLowerCase() : '';
      if (node instanceof SVGElement) {
        if (tag === 'svg' || tag === 'g' || tag === 'defs') continue; // 비렌더 컨테이너
        const cs = getComputedStyle(node);
        if (cs.fill === 'none') continue;
        const fill = parse(cs.fill);
        if (fill.length < 3) continue;
        const fillA = fill.length === 4 ? fill[3] : 1;
        const fillOpacity = parseFloat(cs.fillOpacity);
        const opacity = parseFloat(cs.opacity);
        const a = fillA * (isNaN(fillOpacity) ? 1 : fillOpacity) * (isNaN(opacity) ? 1 : opacity);
        if (a <= 0) continue;
        layers.push({ c: fill.slice(0, 3), a });
        if (a >= 0.999) break;
      } else {
        const cs = getComputedStyle(node);
        const bg = parse(cs.backgroundColor);
        if (bg.length < 3) continue;
        const bgA = bg.length === 4 ? bg[3] : 1;
        const opacity = parseFloat(cs.opacity);
        const a = bgA * (isNaN(opacity) ? 1 : opacity);
        if (a <= 0) continue;
        layers.push({ c: bg.slice(0, 3), a });
        if (a >= 0.999) break;
      }
    }
    let base = [255, 255, 255];
    if (layers.length && layers[layers.length - 1].a >= 0.999) base = layers.pop().c;
    for (let i = layers.length - 1; i >= 0; i--) {
      const { c, a } = layers[i];
      base = base.map((v, k) => c[k] * a + v * (1 - a));
    }
    return base;
  }

  const out = { contrast: [], arrows: {}, donut: {}, tabs: [], legend: {}, pentagon: {}, aria: {} };

  // --- 1. 오각형 화살표: stroke / dasharray / opacity 실측 ---
  const svg = document.querySelector('svg[viewBox="0 0 300 300"]');
  if (svg) {
    const lines = [...svg.querySelectorAll('path, line')];
    const seen = new Map();
    lines.forEach((l) => {
      const cs = getComputedStyle(l);
      const key = `${cs.stroke}|${cs.strokeDasharray}|${cs.opacity}`;
      seen.set(key, (seen.get(key) || 0) + 1);
    });
    out.arrows.styles = [...seen.entries()].map(([k, n]) => ({ style: k, count: n }));
    out.arrows.markerDefs = svg.querySelectorAll('defs marker').length;
    out.arrows.markerRefs = lines.filter((l) => getComputedStyle(l).markerEnd !== 'none').length;
    // 실제 화살촉이 그려지는지: marker id 가 defs 에 존재하는지 대조
    const ids = new Set([...svg.querySelectorAll('defs marker')].map((m) => m.id));
    out.arrows.danglingMarkerRefs = lines.filter((l) => {
      const m = (getComputedStyle(l).markerEnd || '').match(/#([^)"']+)/);
      return m && !ids.has(m[1]);
    }).length;
    // % 텍스트 대비 — 실제 배경(20% 틴트 원)과 vs-white 중 나쁜 쪽으로 판정
    // slice(0,5) 로 자르면 "후보가 5개 미만"인 결함을 못 본다. 전수 수집하고 개수는 Node 에서 단언한다.
    const pcts = [...svg.querySelectorAll('text')].filter((t) => /%/.test(t.textContent));
    out.pentagon.pctTextCount = pcts.length;
    out.pentagon.pctTexts = pcts.map((t) => t.textContent.trim());
    out.pentagon.pctValues = pcts
      .map((t) => parseFloat((t.textContent.match(/-?[\d.]+/) || [NaN])[0]))
      .sort((a, b) => a - b);
    pcts.forEach((t) => {
      const fg = parse(getComputedStyle(t).fill);
      const rect = t.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const actualBg = bgAtPoint(cx, cy, t);
      // 히트테스트가 실제로 성립했는지 기록한다. 0이면 bgAtPoint 는 아무것도 못 보고
      // 기본값 흰색을 돌려준 것이고, vsActual 은 측정이 아니라 위장이다.
      const stackLen = document.elementsFromPoint(cx, cy).length;
      const vsWhite = ratio(fg, [255, 255, 255]);
      const vsActual = ratio(fg, actualBg);
      out.contrast.push({
        what: `오각형 % 텍스트 "${t.textContent.trim()}"`,
        fg: getComputedStyle(t).fill,
        bg: `rgb(${actualBg.map((v) => Math.round(v)).join(',')})`,
        stackLen,
        vsWhite,
        vsActual,
        ratio: Math.min(vsWhite, vsActual),
        need: 4.5,
      });
    });
  }

  // --- 2. 범례 스와치 (색 아닌 구분자 존재 여부) ---
  // 앞 버전은 `svg[aria-hidden="true"]` + clientWidth<=40 으로 잡았는데, iconify 아이콘이
  // 전부 aria-hidden 24px svg 라 44개가 걸렸다(범례 2 + 아이콘 42). 개수 단언이 불가능한 측정이었다.
  // → 오각형 차트 카드 안으로 스코프를 좁힌다: 오각형 svg 의 조상을 4단계까지 올라가며
  //   "오각형 자신이 아닌 aria-hidden svg 를 처음 포함하는" 조상을 카드로 본다.
  {
    let card = null;
    let node = svg ? svg.parentElement : null;
    const isSwatch = (s) => s !== svg && (!svg || !svg.contains(s));
    for (let i = 0; i < 4 && node; i++, node = node.parentElement) {
      if ([...node.querySelectorAll('svg[aria-hidden="true"]')].some(isSwatch)) { card = node; break; }
    }
    const legendSvgs = card ? [...card.querySelectorAll('svg[aria-hidden="true"]')].filter(isSwatch) : [];
    out.legend.cardFound = !!card;
    out.legend.miniSwatchCount = legendSvgs.length;
    out.legend.dashedSwatches = legendSvgs.filter((s) =>
      [...s.querySelectorAll('line,path')].some((l) => getComputedStyle(l).strokeDasharray !== 'none')
    ).length;
  }

  // --- 3. 도넛 세그먼트: dasharray/offset 정합 + 색 대비 ---
  const circles = [...document.querySelectorAll('circle')].filter((c) => getComputedStyle(c).strokeDasharray !== 'none' && c.r?.baseVal?.value > 20);
  out.donut.segments = circles.length;
  const bad = [];
  circles.forEach((c) => {
    const cs = getComputedStyle(c);
    const fg = parse(cs.stroke);
    if (fg.length >= 3) {
      const r = ratio(fg, [255, 255, 255]);
      if (r < 3) bad.push({ stroke: cs.stroke, ratio: r });
    }
  });
  out.donut.belowThree = bad;
  // 갭이 실제로 적용됐는지: dasharray 의 visible 합 + 갭*n ≈ 둘레
  // 도넛별로 분리해야 한다 — 두 도넛의 반지름이 같아서 반지름 기준 묶기는 틀린다.
  const svgs = new Map();
  circles.forEach((c) => {
    const owner = c.ownerSVGElement;
    if (!svgs.has(owner)) svgs.set(owner, []);
    svgs.get(owner).push(c);
  });
  out.donut.byChart = [...svgs.values()].map((arr, i) => {
    const r = arr[0].r.baseVal.value;
    const circ = 2 * Math.PI * r;
    const segs = arr.map((c) => {
      const cs = getComputedStyle(c);
      const [vis] = cs.strokeDasharray.split(/[, ]+/).map(parseFloat);
      return { vis, offset: parseFloat(cs.strokeDashoffset), stroke: cs.stroke };
    });
    const visSum = segs.reduce((s, x) => s + x.vis, 0);
    // 오프셋 간격이 갭 미차감 원값으로 누적됐는지: 인접 오프셋 차 - vis == GAP 이어야 한다
    const sorted = [...segs].sort((a, b) => b.offset - a.offset);
    const gaps = [];
    for (let k = 0; k < sorted.length - 1; k++) {
      gaps.push(+(sorted[k].offset - sorted[k + 1].offset - sorted[k].vis).toFixed(2));
    }
    const totalGap = +(circ - visSum).toFixed(2);
    // n개 세그먼트 링에는 갭이 n개다 — 위 루프는 n-1개뿐, 12시 방향 랩어라운드 갭이 빠진다.
    const wrapGap = +(totalGap - gaps.reduce((s, g) => s + g, 0)).toFixed(2);
    gaps.push(wrapGap);
    // Math.max(visible-GAP, 1) 클램프가 걸린 극소 세그먼트는 갭이 2±0.5를 벗어나도 예외다.
    // gaps[k] 는 sorted[k].vis 로 계산되므로(wrap 갭은 sorted[last]) 인덱스가 그대로 대응된다.
    const isClamped = (seg) => Math.abs(seg.vis - 1) < 0.01;
    const exceptions = sorted.map((s) => isClamped(s));
    const gapFails = gaps.map((g, k) => !exceptions[k] && Math.abs(g - 2) > 0.5);
    return {
      chart: i, r: +r.toFixed(1), n: segs.length,
      circumference: +circ.toFixed(1), visibleSum: +visSum.toFixed(1),
      totalGap,
      gaps, exceptions, gapFails,
    };
  });

  // --- 4. 상호작용 탭 아이콘 색 대비 ---
  document.querySelectorAll('[class*="text-success"], [class*="text-danger"], [class*="text-muted-foreground"]').forEach((el) => {
    if (!el.closest('button')) return;
    const cs = getComputedStyle(el);
    const fg = parse(cs.color);
    if (fg.length < 3) return;
    const r = ratio(fg, effectiveBg(el));
    // 12개 캡을 제거한다 — 13번째부터 조용히 버려지면 그 위반은 영원히 안 보인다.
    out.tabs.push({ tag: el.tagName.toLowerCase(), cls: el.className.toString().slice(0, 40), color: cs.color, ratio: r });
  });

  // --- 4b. 도넛 aria-label 원문 (Node 에서 mock 계산값과 완전 일치 대조) ---
  const ohengSvg = document.querySelector('svg[aria-label^="오행 분포:"]');
  const tenGodSvg2 = document.querySelector('svg[aria-label^="십성 분포:"]');
  out.aria.oheng = ohengSvg ? ohengSvg.getAttribute('aria-label') : null;
  out.aria.tenGod = tenGodSvg2 ? tenGodSvg2.getAttribute('aria-label') : null;

  // --- 5. 전역 스윕: 눈에 보이는 텍스트 중 대비 미달 ---
  const violations = [];
  document.querySelectorAll('span, p, div, a, button, h1, h2, h3, td, th, li').forEach((el) => {
    const t = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join('');
    if (!t || t.length < 2) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return;
    const rect = el.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) return;
    const fg = parse(cs.color);
    if (fg.length < 3) return;
    const px = parseFloat(cs.fontSize);
    const w = cs.fontWeight;
    const isLarge = px >= 24 || (px >= 18.66 && (+w >= 700 || w === 'bold'));
    const need = isLarge ? 3 : 4.5;
    const r = ratio(fg, effectiveBg(el));
    if (r < need) violations.push({ text: t.slice(0, 24), color: cs.color, px, ratio: r, need });
  });
  // 중복 제거
  const uniq = new Map();
  violations.forEach((v) => { const k = `${v.color}|${v.px}`; if (!uniq.has(k)) uniq.set(k, { ...v, n: 1 }); else uniq.get(k).n++; });
  out.sweep = [...uniq.values()].sort((a, b) => a.ratio - b.ratio);

  return out;
});

console.log('=== 오각형 화살표 (생=실선 #2563EB / 극=파선 #DC2626, opacity 없어야 함) ===');
console.log(JSON.stringify(report.arrows, null, 2));
console.log('\n=== 범례 스와치 (색각무관 구분자) ===');
console.log(JSON.stringify(report.legend, null, 2));
console.log('\n=== aria-label 원문 (mock 계산값과 대조) ===');
console.log(`  오행 실측: ${JSON.stringify(report.aria.oheng)}`);
console.log(`  오행 기대: ${JSON.stringify(EXPECT_ARIA_OHENG)}`);
console.log(`  십성 실측: ${JSON.stringify(report.aria.tenGod)}`);
console.log(`  십성 기대: ${JSON.stringify(EXPECT_ARIA_TENGOD)}`);
console.log(`  오각형 % 실측: ${JSON.stringify(report.pentagon.pctValues)} (텍스트 ${report.pentagon.pctTextCount}개) / 기대 ${JSON.stringify(EXPECT_PENTAGON_PCTS)}`);
console.log('\n=== 오각형 % 텍스트 대비 (vs-white / vs-실측배경 중 나쁜 쪽) ===');
report.contrast.forEach((c) => console.log(`  ${c.ratio >= c.need ? 'PASS' : 'FAIL'} ${c.ratio}:1 (필요 ${c.need}) ${c.what} fg=${c.fg} bg=${c.bg} [vsWhite=${c.vsWhite} vsActual=${c.vsActual} stack=${c.stackLen}]`));
console.log('\n=== 도넛 ===');
console.log(JSON.stringify(report.donut, null, 2));
console.log('\n=== 탭 아이콘 대비 (비텍스트 3:1) ===');
report.tabs.forEach((t) => console.log(`  ${t.ratio >= 3 ? 'PASS' : 'FAIL'} ${t.ratio}:1  ${t.color}  ${t.cls}`));
console.log('\n=== 전역 텍스트 대비 스윕 (미달만) ===');
if (!report.sweep.length) console.log('  위반 0건');
report.sweep.forEach((v) => console.log(`  ${v.ratio}:1 (필요 ${v.need}) ${v.px}px ${v.color} ×${v.n} "${v.text}"`));

if (errs.length) { console.log('\n=== 콘솔 에러 (WARN, 판정에 영향 없음) ==='); [...new Set(errs)].slice(0, 5).forEach((e) => console.log('  ' + e)); }
else console.log('\n콘솔 에러 0건');

// --- P1: 모달 포커스 트랩 + 배경 봉쇄(inert) + overflow 복원 + exit 애니메이션 ---
// 반환: { fails, oks } — 성공 시에도 양성 라인을 남겨 "대상이 없어 조용히 통과"를 구분한다.
async function probeP1() {
  const fails = [];
  const oks = [];
  const resetOverflow = () => page.evaluate(() => { document.body.style.overflow = ''; });

  const heading = page.getByRole('button', { name: '오행 / 십성 분포', exact: true }).first();
  if (!(await heading.count())) {
    fails.push('P1: "오행 / 십성 분포" 버튼을 찾지 못함');
    return { fails, oks };
  }
  const headingHandle = await heading.elementHandle();

  // overflow 복원 계약을 검사하려면 "열기 전 값"이 빈 문자열이 아니어야 한다.
  // ''였다면 'unset' 리셋 버그와 올바른 복원이 구분되지 않는다.
  await page.evaluate(() => { document.body.style.overflow = 'auto'; });

  await heading.focus();
  await page.keyboard.press('Enter');

  const dialog = page.locator('[role="dialog"][aria-modal="true"]');
  try {
    await dialog.waitFor({ state: 'visible', timeout: 3000 });
  } catch {
    fails.push('P1: Enter 후 [role="dialog"][aria-modal="true"]가 나타나지 않음');
    await resetOverflow();
    return { fails, oks };
  }
  const dialogHandle = await dialog.elementHandle();
  const insideDialog = () => page.evaluate((d) => !!d && d.contains(document.activeElement), dialogHandle);

  if (!(await insideDialog())) fails.push('P1: 다이얼로그 오픈 직후 activeElement가 다이얼로그 내부가 아님');

  // --- 열림 중 상태 실측: overflow 잠금 + 배경 inert 봉쇄 ---
  const openState = await page.evaluate((d) => {
    const children = [...document.body.children];
    const host = children.find((c) => c.contains(d)); // 다이얼로그를 담은 body 직계 자식
    const describe = (c) =>
      c.tagName.toLowerCase() +
      (c.id ? '#' + c.id : '') +
      (typeof c.className === 'string' && c.className ? '.' + c.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
    const others = children.filter((c) => c !== host);
    return {
      overflow: document.body.style.overflow,
      hostFound: !!host,
      hostIsPortal: !!host && host.hasAttribute('data-glossary-portal'),
      hostInert: !!host && host.hasAttribute('inert'),
      total: children.length,
      othersCount: others.length,
      notInert: others.filter((c) => !c.hasAttribute('inert')).map(describe),
      inertList: others.filter((c) => c.hasAttribute('inert')).map(describe),
    };
  }, dialogHandle);

  if (openState.overflow !== 'hidden')
    fails.push(`P1-OVERFLOW: 열림 중 body 인라인 overflow="${openState.overflow}" (기대 hidden)`);

  if (!openState.hostFound)
    fails.push('P1-INERT: 다이얼로그를 담은 body 직계 자식을 찾지 못함 — 포탈이 body 직계가 아니다');
  else if (!openState.hostIsPortal)
    fails.push('P1-INERT: 다이얼로그를 담은 body 직계 자식에 [data-glossary-portal]이 없음');
  if (openState.hostInert)
    fails.push('P1-INERT: 다이얼로그 컨테이너 자신이 inert를 갖고 있음 — 모달까지 봉쇄된다');
  if (openState.othersCount < 2)
    fails.push(`P1-INERT: 봉쇄 대상 body 직계 자식이 ${openState.othersCount}개뿐 — 단언이 공허하다 (total=${openState.total})`);
  if (openState.notInert.length)
    fails.push(`P1-INERT: inert 미적용 배경 요소 ${openState.notInert.length}개 — ${openState.notInert.join(', ')}`);
  if (
    openState.hostFound && openState.hostIsPortal && !openState.hostInert &&
    openState.othersCount >= 2 && !openState.notInert.length
  )
    oks.push(`P1-INERT OK: body 직계 ${openState.total}개 중 포탈 컨테이너 제외 ${openState.othersCount}개 전부 inert [${openState.inertList.join(', ')}], 컨테이너는 미보유`);

  for (let i = 0; i < 6; i++) await page.keyboard.press('Tab');
  if (!(await insideDialog())) fails.push('P1: Tab×6 후 activeElement가 다이얼로그 밖으로 탈출');

  for (let i = 0; i < 2; i++) await page.keyboard.press('Shift+Tab');
  if (!(await insideDialog())) fails.push('P1: Shift+Tab×2 후 activeElement가 다이얼로그 밖으로 탈출');

  // --- exit 애니메이션: Escape 직후에도 아직 붙어 있어야 하고, 2000ms 안에 사라져야 한다 ---
  await page.keyboard.press('Escape');
  const attachedRightAfter = await dialog.count();
  if (attachedRightAfter === 0)
    fails.push('P1-EXITANIM: Escape 직후 다이얼로그가 즉시 detach — exit 애니메이션이 스킵됐다(entry null 처리로 언마운트)');

  let detachMs = -1;
  const t0 = Date.now();
  while (Date.now() - t0 < 2000) {
    if ((await dialog.count()) === 0) { detachMs = Date.now() - t0; break; }
    await page.waitForTimeout(50);
  }
  if (detachMs < 0)
    fails.push('P1-EXITANIM: Escape 후 2000ms 안에 다이얼로그가 detach 되지 않음 — 닫히지 않는다');
  else if (attachedRightAfter > 0)
    oks.push(`P1-EXITANIM OK: Escape 직후 attach 유지(exit 재생 중) → ${detachMs}ms 후 detach`);

  await page.waitForTimeout(500);

  const focusInfo = await page.evaluate((h) => {
    const a = document.activeElement;
    return {
      back: a === h,
      tag: a ? a.tagName.toLowerCase() : 'null',
      text: a && a.textContent ? a.textContent.replace(/\s+/g, ' ').trim().slice(0, 30) : '',
    };
  }, headingHandle);
  if (!focusInfo.back)
    fails.push(`P1-FOCUSRETURN: Escape 후 activeElement가 헤딩 버튼으로 복귀하지 않음 — 현재 <${focusInfo.tag}> "${focusInfo.text}"`);
  else oks.push('P1-FOCUSRETURN OK: Escape 후 포커스가 트리거 헤딩 버튼("오행 / 십성 분포")으로 복귀');

  // --- 닫힘 후 복원: inert 전량 해제 + overflow 원값 ---
  const closedState = await page.evaluate(() => {
    const children = [...document.body.children];
    const inert = children.filter((c) => c.hasAttribute('inert'));
    return {
      overflow: document.body.style.overflow,
      total: children.length,
      inertCount: inert.length,
      inertList: inert.map((c) => c.tagName.toLowerCase()),
    };
  });

  if (closedState.overflow !== 'auto')
    fails.push(`P1-OVERFLOW: 닫힘 후 body 인라인 overflow="${closedState.overflow}" (기대 auto — 열기 전 값 복원)`);
  else if (openState.overflow === 'hidden')
    oks.push('P1-OVERFLOW OK: 열기 전 auto → 열림 중 hidden → 닫힘 후 auto 복원');

  if (closedState.inertCount !== 0)
    fails.push(`P1-INERT-RESTORE: 닫힘 후에도 inert 보유 ${closedState.inertCount}개 — ${closedState.inertList.join(', ')}`);
  else
    oks.push(`P1-INERT-RESTORE OK: 닫힘 후 body 직계 ${closedState.total}개 중 inert 보유 0개`);

  await resetOverflow();
  return { fails, oks };
}

// --- P2: 툴팁 dismissable (WCAG 1.4.13) ---
// P2-KBD-ESC        키보드로 연 툴팁: Escape로 닫히고, 트리거 포커스 유지, 재열림 없음
// P2-NO-DETAIL-BTN  래퍼 안에 button 0개 — 도달 불가였던 "자세히 보기" 제거의 회귀 가드
// P2-HOVER-ESC      hover로 연 툴팁: 포커스가 위젯 밖에 있어도 Escape로 닫히고, 포커스는 불변
// 반환: { fails, oks } — 성공 시에도 양성 라인을 남겨 "대상이 없어 조용히 통과"를 구분한다.
async function probeP2() {
  const fails = [];
  const oks = [];
  const trigger = page.locator('span[role="button"][aria-label$="용어 설명"]').first();
  if (!(await trigger.count())) {
    fails.push('P2: 툴팁 트리거(span[role="button"][aria-label$="용어 설명"])를 찾지 못함');
    return { fails, oks };
  }
  const triggerHandle = await trigger.elementHandle();

  // ================= P2-KBD-ESC + P2-NO-DETAIL-BTN =================
  await trigger.focus();
  await page.waitForTimeout(100);
  let expanded = await trigger.getAttribute('aria-expanded');
  if (expanded !== 'true') {
    fails.push(`P2-KBD-ESC: 포커스 후 aria-expanded="${expanded}" (기대 true)`);
    return { fails, oks };
  }

  // 열린 상태에서 측정한다 — 닫힌 상태로 세면 "버튼 0개"는 공허하게 참이 된다.
  const openProbe = await page.evaluate((el) => {
    const wrapper = el.parentElement;
    const id = el.getAttribute('aria-describedby');
    const panel = id ? document.getElementById(id) : null;
    return {
      wrapperFound: !!wrapper,
      buttons: wrapper ? wrapper.querySelectorAll('button').length : -1,
      buttonTexts: wrapper
        ? [...wrapper.querySelectorAll('button')].map((b) => (b.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 24))
        : [],
      panelFound: !!panel,
      panelInWrapper: !!panel && !!wrapper && wrapper.contains(panel),
      panelText: panel ? (panel.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 50) : '',
    };
  }, triggerHandle);

  {
    const f = [];
    if (!openProbe.wrapperFound) f.push('P2-NO-DETAIL-BTN: 트리거의 부모(래퍼)를 찾지 못함');
    // 툴팁 패널이 실제로 열려 있어야 "버튼 0개" 단언이 의미를 갖는다.
    if (!openProbe.panelFound)
      f.push('P2-NO-DETAIL-BTN: aria-describedby가 가리키는 툴팁 패널이 DOM에 없음 — 버튼 0개 단언이 공허하다');
    else if (!openProbe.panelInWrapper)
      f.push('P2-NO-DETAIL-BTN: 툴팁 패널이 래퍼 하위가 아님 — 래퍼 스코프 카운트가 패널을 못 본다');
    if (openProbe.buttons !== 0)
      f.push(`P2-NO-DETAIL-BTN: 래퍼 하위 button ${openProbe.buttons}개 (기대 0) — ${JSON.stringify(openProbe.buttonTexts)}`);
    fails.push(...f);
    if (!f.length)
      oks.push(`P2-NO-DETAIL-BTN OK: 툴팁 열린 상태(패널 "${openProbe.panelText}")에서 래퍼 하위 button 0개`);
  }

  {
    const f = [];
    await trigger.press('Escape');
    await page.waitForTimeout(100);
    expanded = await trigger.getAttribute('aria-expanded');
    let triggerActive = await page.evaluate((el) => document.activeElement === el, triggerHandle);
    if (expanded !== 'false' || !triggerActive)
      f.push(`P2-KBD-ESC: Escape 직후 aria-expanded="${expanded}", activeElement===트리거? ${triggerActive}`);

    // 300ms 대기 후 재확인 — 트리거에 남은 포커스가 focus 핸들러를 다시 태워
    // 툴팁이 즉시 재열리는 회귀를 여기서 잡는다.
    await page.waitForTimeout(300);
    const expandedAfterWait = await trigger.getAttribute('aria-expanded');
    triggerActive = await page.evaluate((el) => document.activeElement === el, triggerHandle);
    if (expandedAfterWait !== 'false')
      f.push(`P2-KBD-ESC: 300ms 후 재확인 — aria-expanded="${expandedAfterWait}" (툴팁 재열림)`);
    if (!triggerActive) f.push('P2-KBD-ESC: 300ms 후 activeElement가 트리거에서 벗어남');
    fails.push(...f);
    if (!f.length)
      oks.push('P2-KBD-ESC OK: 포커스로 열림 → Escape로 닫힘(aria-expanded=false) → 트리거 포커스 유지 → 300ms 후 재열림 없음');
  }

  // ================= P2-HOVER-ESC (1.4.13 dismissable) =================
  // 포커스를 위젯 밖으로 뺀 뒤 마우스로만 연다. Escape가 닫아야 하고, 포커스는 건드리면 안 된다.
  {
    const f = [];
    await page.evaluate(() => document.activeElement instanceof HTMLElement && document.activeElement.blur());
    await page.waitForTimeout(150);
    const beforeHandle = await page.evaluateHandle(() => document.activeElement);
    const beforeDesc = await page.evaluate(() => {
      const a = document.activeElement;
      return a ? a.tagName.toLowerCase() + (a.id ? '#' + a.id : '') : 'null';
    });

    await trigger.hover();
    await page.waitForTimeout(500); // hover 열기 지연 300ms + 여유

    const hoverState = await page.evaluate(
      ([el, before]) => ({
        expanded: el.getAttribute('aria-expanded'),
        activeOutsideWrapper: !(el.parentElement && el.parentElement.contains(document.activeElement)),
        activeUnchanged: document.activeElement === before,
        activeTag: document.activeElement ? document.activeElement.tagName.toLowerCase() : 'null',
      }),
      [triggerHandle, beforeHandle]
    );

    if (hoverState.expanded !== 'true')
      f.push(`P2-HOVER-ESC: hover 후 aria-expanded="${hoverState.expanded}" (기대 true — 마우스로 열리지 않았다)`);
    if (!hoverState.activeOutsideWrapper)
      f.push(`P2-HOVER-ESC: hover 시점 activeElement가 위젯 안에 있음(<${hoverState.activeTag}>) — "포커스 밖" 전제가 성립하지 않아 단언이 공허하다`);
    if (!hoverState.activeUnchanged)
      f.push(`P2-HOVER-ESC: hover만으로 activeElement가 바뀜(<${hoverState.activeTag}>) — 기준선이 무너졌다`);

    if (!f.length) {
      await page.keyboard.press('Escape');
      let closedMs = -1;
      const t0 = Date.now();
      while (Date.now() - t0 < 200) {
        if ((await trigger.getAttribute('aria-expanded')) === 'false') { closedMs = Date.now() - t0; break; }
        await page.waitForTimeout(20);
      }
      const after = await page.evaluate(
        (before) => ({
          same: document.activeElement === before,
          tag: document.activeElement ? document.activeElement.tagName.toLowerCase() : 'null',
        }),
        beforeHandle
      );
      if (closedMs < 0)
        f.push(`P2-HOVER-ESC: Escape 후 200ms 안에 닫히지 않음 — aria-expanded="${await trigger.getAttribute('aria-expanded')}" (hover로 연 툴팁이 키보드로 해제 불가)`);
      if (!after.same)
        f.push(`P2-HOVER-ESC: Escape가 포커스를 이동시킴 — <${beforeDesc}> → <${after.tag}> (1.4.13 위반: 포커스 강탈)`);
      if (!f.length)
        oks.push(`P2-HOVER-ESC OK: 포커스 밖(<${beforeDesc}>)에서 hover로 열림 → Escape ${closedMs}ms 만에 닫힘 → activeElement 불변`);
    }
    fails.push(...f);
    await beforeHandle.dispose();
  }

  // 마우스를 트리거에서 떼어 뒤 단계(P3)에 hover 상태가 새지 않게 한다.
  await page.mouse.move(0, 0);
  await page.waitForTimeout(300);

  return { fails, oks };
}

// --- P3: 십성 범례 / aria 계약 ---
async function probeP3(rampHexes) {
  return page.evaluate((ramp) => {
    const fails = [];
    const rampSet = new Set(ramp.map((h) => h.toLowerCase()));
    const toHex = (rgbStr) => {
      const m = rgbStr.match(/[\d.]+/g);
      if (!m) return null;
      const [r, g, b] = m.map(Number);
      return '#' + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
    };
    const srgb = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const lum = ([r, g, b]) => 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b);
    const parse = (s) => (s.match(/[\d.]+/g) || []).slice(0, 4).map(Number);
    const ratio = (fg, bg) => {
      const a = lum(fg) + 0.05, b = lum(bg) + 0.05;
      return +(Math.max(a, b) / Math.min(a, b)).toFixed(2);
    };

    const elementSvg = document.querySelector('svg[role="img"][aria-label^="오행 분포:"]');
    if (!elementSvg) fails.push('P3: svg[role="img"][aria-label^="오행 분포:"] 없음');
    const tenGodSvg = document.querySelector('svg[role="img"][aria-label^="십성 분포:"]');
    if (!tenGodSvg) fails.push('P3: svg[role="img"][aria-label^="십성 분포:"] 없음');

    const legendItems = [...document.querySelectorAll('[data-legend="ten-gods"] > div')];
    if (legendItems.length !== 10) fails.push(`P3: [data-legend="ten-gods"] > div 개수 ${legendItems.length} (기대 10)`);

    const swatchMismatches = [];
    legendItems.forEach((item, i) => {
      const swatch = item.querySelector(':scope > div');
      if (!swatch) { swatchMismatches.push(`#${i} 스와치 요소 없음`); return; }
      const hex = toHex(getComputedStyle(swatch).backgroundColor);
      if (!hex || !rampSet.has(hex.toLowerCase())) swatchMismatches.push(`#${i} ${hex}`);
    });
    if (swatchMismatches.length) fails.push(`P3: 십성 스와치 색이 신 램프 밖 — ${swatchMismatches.join(', ')}`);

    if (tenGodSvg) {
      const circles = [...tenGodSvg.querySelectorAll('circle')].filter((c) => getComputedStyle(c).strokeDasharray !== 'none');
      const notInRamp = [];
      const belowMin = [];
      circles.forEach((c) => {
        const strokeHex = toHex(getComputedStyle(c).stroke);
        if (!strokeHex || !rampSet.has(strokeHex.toLowerCase())) notInRamp.push(strokeHex);
        const fg = parse(getComputedStyle(c).stroke).slice(0, 3);
        const r = ratio(fg, [255, 255, 255]);
        if (r < 3.4) belowMin.push({ stroke: strokeHex, ratio: r });
      });
      if (notInRamp.length) fails.push(`P3: 십성 도넛 stroke가 신 램프 밖 — ${notInRamp.join(', ')}`);
      if (belowMin.length) fails.push(`P3: 십성 도넛 세그먼트 백색 대비 <3.4 — ${JSON.stringify(belowMin)}`);
    }

    return fails;
  }, rampHexes);
}

console.log('\n=== P1: 모달 포커스 트랩 / inert 봉쇄 / overflow 복원 / exit 애니메이션 ===');
// 양성 라인(p1Oks)은 아래 "실행된 단언" 섹션에서 한 번만 출력한다(중복 집계 방지).
const { fails: p1Fails, oks: p1Oks } = await probeP1();
if (!p1Fails.length) console.log('  PASS');
else p1Fails.forEach((f) => console.log('  FAIL ' + f));

console.log('\n=== P2: 툴팁 dismissable (키보드 Escape / hover Escape / 죽은 버튼 제거) ===');
// 양성 라인(p2Oks)은 아래 "실행된 단언" 섹션에서 한 번만 출력한다(중복 집계 방지).
const { fails: p2Fails, oks: p2Oks } = await probeP2();
if (!p2Fails.length) console.log('  PASS');
else p2Fails.forEach((f) => console.log('  FAIL ' + f));

console.log('\n=== P3: 십성 범례 / aria 계약 ===');
// P1/P2 가 모달·툴팁을 열고 닫으며 리렌더를 유발하므로 변이를 재적용한다(멱등).
await applySelfTestMutations();
const p3Fails = await probeP3(TEN_GOD_RAMP);
if (!p3Fails.length) console.log('  PASS');
else p3Fails.forEach((f) => console.log('  FAIL ' + f));

// ============================================================================
// 판정 집계 — 측정한 것은 전부 여기로 들어와야 한다.
// "계산만 되고 단언되지 않는 값"이 남으면 VERDICT: PASS 는 공허해진다.
// ============================================================================
const allFails = [];
const oks = []; // 양성 라인: "단언이 실행됐다"와 "대상이 없어 조용히 넘어갔다"를 구분하기 위함

allFails.push(...SANITY_FAILS);

// --- ARROWS: 오각형 생/극 화살표 ---
{
  const a = report.arrows;
  const fails = [];
  if (a.markerDefs !== 2) fails.push(`ARROWS: defs marker ${a.markerDefs}개 (기대 2 — 생/극 화살촉)`);
  if (a.markerRefs !== 10) fails.push(`ARROWS: markerEnd 참조 ${a.markerRefs}개 (기대 10 — 생 5 + 극 5)`);
  if (a.danglingMarkerRefs !== 0) fails.push(`ARROWS: 끊긴 marker 참조 ${a.danglingMarkerRefs}개 (기대 0 — 화살촉이 안 그려진다)`);
  // defs 내부 marker path 는 stroke none 이라 별도 그룹으로 잡힌다 — 무시하고 생/극 그룹만 본다.
  const styles = a.styles || [];
  const find = (pred) => styles.find(pred);
  const sheng = find((s) => {
    const [stroke, dash, op] = s.style.split('|');
    return stroke === 'rgb(37, 99, 235)' && dash === 'none' && parseFloat(op) === 1;
  });
  const ke = find((s) => {
    const [stroke, dash, op] = s.style.split('|');
    return stroke === 'rgb(220, 38, 38)' && dash !== 'none' && parseFloat(op) === 1;
  });
  if (!sheng) fails.push(`ARROWS: 생(生) 그룹 없음 — stroke rgb(37, 99, 235)·dasharray none·opacity 1 을 만족하는 그룹 부재. 실측=${JSON.stringify(styles)}`);
  else if (sheng.count !== 5) fails.push(`ARROWS: 생(生) 실선 ${sheng.count}개 (기대 5)`);
  if (!ke) fails.push(`ARROWS: 극(剋) 그룹 없음 — stroke rgb(220, 38, 38)·dasharray non-none·opacity 1 을 만족하는 그룹 부재. 실측=${JSON.stringify(styles)}`);
  else if (ke.count !== 5) fails.push(`ARROWS: 극(剋) 파선 ${ke.count}개 (기대 5)`);
  allFails.push(...fails);
  if (!fails.length) oks.push(`ARROWS OK: markerDefs=2 markerRefs=10 dangling=0 / 생 실선 ${sheng.count}개 rgb(37, 99, 235) / 극 파선 ${ke.count}개 rgb(220, 38, 38)`);
}

// --- LEGEND: 색각무관 구분자 ---
{
  const l = report.legend;
  const fails = [];
  if (!l.cardFound) fails.push('LEGEND: 오각형 차트 카드를 찾지 못함 — 범례 스와치를 측정할 스코프가 없다');
  if (l.miniSwatchCount !== 2) fails.push(`LEGEND: 미니 스와치 ${l.miniSwatchCount}개 (기대 2 — 생/극)`);
  if (l.dashedSwatches !== 1) fails.push(`LEGEND: 파선 스와치 ${l.dashedSwatches}개 (기대 1 — 극만 파선)`);
  allFails.push(...fails);
  if (!fails.length) oks.push(`LEGEND OK: 미니 스와치 2개(생/극), 그중 파선 1개`);
}

// --- GUARD: 공허 통과 방지 (측정 대상이 실제로 존재했는가) ---
{
  const fails = [];
  if (report.pentagon.pctTextCount !== EXPECT_PENTAGON_PCT_TEXTS)
    fails.push(`GUARD: 오각형 % 텍스트 ${report.pentagon.pctTextCount}개 (기대 ${EXPECT_PENTAGON_PCT_TEXTS} — 꼭지점 5개). 대비 단언이 공허하게 통과할 수 있다`);
  if (report.contrast.length !== EXPECT_PENTAGON_PCT_TEXTS)
    fails.push(`GUARD: 오각형 % 대비 측정 ${report.contrast.length}건 (기대 ${EXPECT_PENTAGON_PCT_TEXTS})`);
  // bgAtPoint 가 뷰포트 밖이라 빈 스택 → 기본값 흰색으로 통과하는 위장을 막는다.
  const noStack = report.contrast.filter((c) => !c.stackLen);
  if (noStack.length)
    fails.push(`GUARD: bgAtPoint 히트테스트 실패 ${noStack.length}건 — elementsFromPoint 가 빈 스택(뷰포트 밖). vsActual 이 실측이 아니라 기본값 흰색이다`);
  if (report.tabs.length !== EXPECT_TAB_CANDIDATES)
    fails.push(`GUARD: 탭 대비 후보 ${report.tabs.length}개 (기대 핀 ${EXPECT_TAB_CANDIDATES}). 후보가 사라졌거나 늘었다 — 핀을 갱신하거나 회귀를 확인해라. 실측 내역=${JSON.stringify(report.tabs.map((t) => t.tag))}`);
  if (report.donut.byChart.length !== EXPECT_DONUT_CHARTS)
    fails.push(`GUARD: 도넛 차트 ${report.donut.byChart.length}개 (기대 ${EXPECT_DONUT_CHARTS} — 오행/십성)`);
  const ns = report.donut.byChart.map((c) => c.n).sort((a, b) => a - b);
  if (JSON.stringify(ns) !== JSON.stringify(EXPECT_DONUT_NS))
    fails.push(`GUARD: 도넛 세그먼트 수 ${JSON.stringify(ns)} (기대 ${JSON.stringify(EXPECT_DONUT_NS)} — mock 의 비영 항목 수)`);
  if (report.donut.segments !== EXPECT_DONUT_NS.reduce((s, n) => s + n, 0))
    fails.push(`GUARD: 도넛 세그먼트 총합 ${report.donut.segments} (기대 ${EXPECT_DONUT_NS.reduce((s, n) => s + n, 0)})`);
  allFails.push(...fails);
  if (!fails.length) oks.push(`GUARD OK: 오각형 %text ${report.pentagon.pctTextCount}개 / 탭 후보 ${report.tabs.length}개 / 도넛 ${report.donut.byChart.length}차트 n=${JSON.stringify(ns)} (총 ${report.donut.segments} 세그먼트)`);
}

// --- ARIA: 렌더된 aria-label ↔ mock 계산값 완전 일치 ---
{
  const fails = [];
  if (report.aria.oheng !== EXPECT_ARIA_OHENG)
    fails.push(`ARIA: 오행 aria-label 불일치\n       실측=${JSON.stringify(report.aria.oheng)}\n       기대=${JSON.stringify(EXPECT_ARIA_OHENG)}`);
  else oks.push(`ARIA-OHENG OK: ${EXPECT_ARIA_OHENG}`);
  if (report.aria.tenGod !== EXPECT_ARIA_TENGOD)
    fails.push(`ARIA: 십성 aria-label 불일치(현행 ">0 필터" 계약 기준)\n       실측=${JSON.stringify(report.aria.tenGod)}\n       기대=${JSON.stringify(EXPECT_ARIA_TENGOD)}`);
  else oks.push(`ARIA-TENGOD OK: ${EXPECT_ARIA_TENGOD}`);
  const got = JSON.stringify(report.pentagon.pctValues);
  const want = JSON.stringify(EXPECT_PENTAGON_PCTS);
  if (got !== want) fails.push(`ARIA: 오각형 % 값 multiset 불일치 — 실측 ${got} / 기대 ${want}`);
  else oks.push(`ARIA-PENTAGON OK: % multiset ${want} (표시 순서 ${JSON.stringify(report.pentagon.pctTexts)})`);
  allFails.push(...fails);
}

report.sweep.forEach((v) => allFails.push(`전역 스윕: ${v.ratio}:1 (필요 ${v.need}) ${v.px}px ${v.color} ×${v.n} "${v.text}"`));
if (!report.sweep.length) oks.push('SWEEP OK: 전역 텍스트 대비 위반 0건');
report.donut.belowThree.forEach((b) => allFails.push(`도넛 대비 <3:1: ${b.stroke} (${b.ratio}:1)`));
report.donut.byChart.forEach((chart) => {
  chart.gaps.forEach((g, k) => {
    if (chart.gapFails[k]) allFails.push(`도넛#${chart.chart} 갭[${k}]=${g} (기대 2.0±0.5, 세그먼트 n=${chart.n})`);
  });
});
report.contrast.forEach((c) => {
  if (c.ratio < c.need) allFails.push(`오각형 % 텍스트 대비 ${c.ratio}:1 (필요 ${c.need}) ${c.what}`);
});
report.tabs.forEach((t) => {
  if (t.ratio < 3) allFails.push(`탭 아이콘 대비 ${t.ratio}:1 (필요 3) ${t.color} ${t.cls}`);
});
allFails.push(...p1Fails, ...p2Fails, ...p3Fails);

// 나머지 계열의 양성 라인
if (!report.donut.belowThree.length && !report.donut.byChart.some((c) => c.gapFails.some(Boolean)))
  oks.push(`DONUT OK: 대비 <3:1 0건, 갭 2.0±0.5 정합 (${report.donut.byChart.map((c) => `#${c.chart} n=${c.n}`).join(', ')})`);
if (report.contrast.length && report.contrast.every((c) => c.ratio >= c.need))
  oks.push(`CONTRAST OK: 오각형 % 텍스트 ${report.contrast.length}건 전부 ≥4.5:1 (최저 ${Math.min(...report.contrast.map((c) => c.ratio))}:1)`);
if (report.tabs.length && report.tabs.every((t) => t.ratio >= 3))
  oks.push(`TABS OK: 후보 ${report.tabs.length}건 전부 ≥3:1 (최저 ${Math.min(...report.tabs.map((t) => t.ratio))}:1)`);
oks.push(...p1Oks);
if (!p1Fails.length) oks.push('P1 트랩 OK: 오픈 직후·Tab×6·Shift+Tab×2 전부 다이얼로그 내부 유지');
oks.push(...p2Oks);
if (!p3Fails.length) oks.push('P3 OK: 십성 범례 10개 · 램프 정합 · 도넛 대비 ≥3.4:1');

// 양성 라인 — "단언이 실제로 실행됐다"의 증거. 여기가 비면 PASS 를 믿지 마라.
console.log('\n=== 실행된 단언 (양성) ===');
if (!oks.length) console.log('  (없음) — 단언이 하나도 성립하지 않았다');
oks.forEach((o) => console.log('  ' + o));

console.log('\n=== VERDICT ===');
if (!allFails.length) {
  console.log('VERDICT: PASS');
} else {
  console.log(`VERDICT: FAIL (${allFails.length}건)`);
  allFails.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
}

await page.screenshot({ path: artifact('a11y-result-full.png'), fullPage: true });
const chart = page.locator('svg[viewBox="0 0 300 300"]').first();
if (await chart.count()) await chart.screenshot({ path: artifact('a11y-pentagon.png') });
await browser.close();

if (allFails.length) process.exit(1);
