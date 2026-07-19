// /chat 의 populated 상태를 실제로 렌더해 분석의 코드-읽기 주장을 실측으로 확정한다.
// 아무도 이 상태를 브라우저로 본 적이 없다 — 고치기 전에 먼저 본다.
import { BASE, artifact, launchBrowser, loadMock } from './lib/harness.mjs';

const MOCK = loadMock();

const browser = await launchBrowser();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
const page = await ctx.newPage();

// 스트리밍 응답을 "영원히 대기" 상태로 묶어 로딩 말풍선을 노출시킨다.
await page.route('**/api/**', async (route) => {
  if (/chat|stream/i.test(route.request().url())) return; // 응답 안 줌 = 대기 지속
  route.continue();
});

await page.addInitScript((m) => {
  localStorage.setItem('saju-storage', JSON.stringify({ state: { result: m }, version: 0 }));
}, MOCK);

await page.goto(BASE + '/chat', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2500);

const out = { fails: [], oks: [] };

// --- 렌더 가드 ---
const guard = await page.evaluate(() => ({
  els: document.querySelectorAll('span,p,div,button,textarea').length,
  body: document.body.innerText.replace(/\s+/g, ' ').slice(0, 80),
  hasTextarea: !!document.querySelector('textarea'),
}));
console.log(`렌더 가드: 요소 ${guard.els}개, textarea ${guard.hasTextarea ? 'O' : 'X'}`);
console.log(`본문: ${guard.body}\n`);
// /chat 은 /result(531개)보다 훨씬 단순하다 — 개수 임계값 대신 이 페이지의
// 고유 계약(입력창 + 사주 컨텍스트 렌더)으로 판정한다. 임계값을 페이지 간에
// 재사용하면 렌더된 페이지를 미렌더로 오판한다(실제로 43개에서 한 번 겪었다).
if (!guard.hasTextarea || !/상담|사주/.test(guard.body)) {
  console.error('!!! 렌더 가드 실패 — 측정 무효, PASS로 읽지 마라 !!!');
  console.error(`  textarea=${guard.hasTextarea}, 본문="${guard.body}"`);
  await browser.close();
  process.exit(1);
}

// --- C1: textarea 접근 가능한 이름 ---
const ta = await page.evaluate(() => {
  const t = document.querySelector('textarea');
  if (!t) return null;
  const id = t.getAttribute('id');
  return {
    ariaLabel: t.getAttribute('aria-label'),
    ariaLabelledby: t.getAttribute('aria-labelledby'),
    placeholder: t.getAttribute('placeholder'),
    hasLabelFor: id ? !!document.querySelector(`label[for="${CSS.escape(id)}"]`) : false,
    wrappedInLabel: !!t.closest('label'),
  };
});
if (!ta) out.fails.push('C1: textarea 자체가 없음');
else if (!ta.ariaLabel && !ta.ariaLabelledby && !ta.hasLabelFor && !ta.wrappedInLabel) {
  out.fails.push(`C1-NAME: textarea 접근 가능한 이름 없음 (placeholder="${ta.placeholder}" 뿐 — placeholder는 이름이 아니다)`);
} else out.oks.push(`C1-NAME OK: ${ta.ariaLabel || ta.ariaLabelledby || 'label 연결'}`);

// --- C2: aria-live 라이브 리전 ---
const live = await page.evaluate(() => ({
  ariaLive: document.querySelectorAll('[aria-live]').length,
  status: document.querySelectorAll('[role="status"],[role="alert"],[role="log"]').length,
}));
if (live.ariaLive === 0 && live.status === 0) {
  out.fails.push('C2-LIVE: aria-live / role=status|alert|log 가 0건 — 스트리밍 답변이 SR 에 전달되지 않는다');
} else out.oks.push(`C2-LIVE OK: aria-live ${live.ariaLive}, status/alert ${live.status}`);

// --- C3: 로딩 점 가시성 (분석의 핵심 주장) ---
await page.evaluate(() => {
  const ta = document.querySelector('textarea');
  if (ta) {
    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    setter.call(ta, '테스트 질문');
    ta.dispatchEvent(new Event('input', { bubbles: true }));
  }
});
await page.waitForTimeout(400);
const sendBtn = page.locator('form button[type="submit"], button[type="submit"]').first();
if (await sendBtn.count()) {
  await sendBtn.click({ force: true }).catch(() => {});
  await page.waitForTimeout(1800);
}

const dots = await page.evaluate(() => {
  const srgb = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const lum = ([r, g, b]) => 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b);
  const parse = (s) => (s.match(/[\d.]+/g) || []).slice(0, 4).map(Number);
  const ratio = (f, b) => { const x = lum(f) + 0.05, y = lum(b) + 0.05; return +(Math.max(x, y) / Math.min(x, y)).toFixed(2); };

  const found = [...document.querySelectorAll('.animate-bounce')];
  return found.slice(0, 3).map((d) => {
    const cs = getComputedStyle(d);
    const fg = parse(cs.backgroundColor);
    let p = d.parentElement, bg = null;
    while (p && !bg) {
      const b = parse(getComputedStyle(p).backgroundColor);
      if (b.length >= 3 && (b[3] === undefined || b[3] > 0.5)) bg = b.slice(0, 3);
      p = p.parentElement;
    }
    return { dot: cs.backgroundColor, bg: `rgb(${(bg || [255, 255, 255]).join(',')})`, ratio: ratio(fg, bg || [255, 255, 255]) };
  });
});

if (!dots.length) {
  out.fails.push('C3-DOTS: 로딩 점(.animate-bounce)을 못 찾음 — 스트림 대기 상태 재현 실패, 이 항목 미검증');
} else {
  const worst = Math.min(...dots.map((d) => d.ratio));
  console.log('로딩 점 실측:');
  dots.forEach((d) => console.log(`  점=${d.dot} 배경=${d.bg} → ${d.ratio}:1`));
  if (worst < 3) out.fails.push(`C3-DOTS: 로딩 점 대비 ${worst}:1 (비텍스트 3:1 미달) — 사용자에게 빈 말풍선으로 보인다`);
  else out.oks.push(`C3-DOTS OK: 최저 ${worst}:1`);
}

await page.screenshot({ path: artifact('chat-populated.png'), fullPage: true });

console.log('\n=== 실행된 단언 ===');
out.oks.forEach((o) => console.log('  ' + o));
console.log('\n=== VERDICT ===');
if (out.fails.length) {
  console.log(`VERDICT: FAIL (${out.fails.length}건)`);
  out.fails.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
} else console.log('VERDICT: PASS');

await browser.close();
process.exit(out.fails.length ? 1 : 0);
