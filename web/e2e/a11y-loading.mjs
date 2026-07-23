// S-3 검증 B: LoadingOverlay 축소 계약 실측 (/ 에서 실제 폼 제출).
import { BASE, launchBrowser } from './lib/harness.mjs';

const fails = [];
const oks = [];
const ok = (m) => oks.push(m);
const fail = (m) => fails.push(m);

const browser = await launchBrowser();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
const page = await ctx.newPage();
const errs = [];
page.on('pageerror', (e) => errs.push(e.message.slice(0, 200)));
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });

await page.goto(BASE + '/', { waitUntil: 'networkidle', timeout: 90000 });
await page.waitForTimeout(1200);

const beforeOverflow = await page.evaluate(() => document.body.style.overflow || '(빈 문자열)');
const beforeTabbables = await page.evaluate(() =>
  Array.from(document.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select, textarea')).length
);

// 폼 채우기
await page.fill('input[placeholder="홍길동"]', '홍길동');
await page.fill('input[type="date"]', '1990-05-15');
await page.fill('input[type="time"]', '13:30');
await page.fill('input[placeholder="서울, 도쿄, 뉴욕..."]', '서울');
await page.waitForTimeout(1800);
// 도시 자동완성은 ARIA combobox → 옵션은 role="option"(구 button[type=button]에서 변경)
const cityBtns = page.locator('[role="option"]').filter({ hasText: '서울' });
if ((await cityBtns.count()) === 0) { console.log('도시 드롭다운 항목 없음'); }
await cityBtns.first().click();
await page.waitForTimeout(400);

// /api/manseol 응답을 지연시켜 로딩 오버레이가 떠 있는 창을 확보한다.
await page.route('**/api/manseol', async (route) => {
  await new Promise((r) => setTimeout(r, 10000));
  await route.abort();
});

const submitBtn = page.locator('button[type="submit"]');
const submitText = (await submitBtn.textContent())?.trim();
await submitBtn.click();
await page.waitForTimeout(1500);

const present = await page.locator('[data-loading-portal] [role="status"]').count();
if (present === 0) {
  fail('L0: 제출 후에도 LoadingOverlay 미표시 — 이하 단언 미수행');
} else {
  ok(`L0: 폼 제출("${submitText}") 후 LoadingOverlay 표시됨`);

  const lo = await page.evaluate(() => {
    const c = document.querySelector('[data-loading-portal]');
    const s = c?.querySelector('[role="status"]');
    const kids = Array.from(document.body.children);
    return {
      isBodyChild: c?.parentElement === document.body,
      statusOutsidePortal: document.querySelectorAll('[role="status"]').length - (c?.querySelectorAll('[role="status"]').length ?? 0),
      ariaLive: s?.getAttribute('aria-live'),
      role: s?.getAttribute('role'),
      notInert: kids.filter((k) => k !== c && !k.hasAttribute('inert')).map((k) => k.tagName.toLowerCase()),
      total: kids.length,
      inertNames: kids.filter((k) => k !== c).map((k) => k.tagName.toLowerCase()),
      containerHasInert: c?.hasAttribute('inert'),
      overflow: document.body.style.overflow,
      focusablesInside: s ? s.querySelectorAll('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])').length : -1,
      text: s?.textContent?.trim().replace(/\s+/g, ' ').slice(0, 60),
    };
  });

  if (!lo.isBodyChild) fail('L1: [data-loading-portal]가 body 직계가 아님');
  else if (lo.statusOutsidePortal !== 0) fail(`L1: 포탈 밖 role=status ${lo.statusOutsidePortal}개`);
  else ok('L1-PORTAL OK: body 직계 [data-loading-portal] 안에만 렌더 (밖 0개)');

  if (lo.role !== 'status' || lo.ariaLive !== 'polite') fail(`L2: role=${lo.role} aria-live=${lo.ariaLive}`);
  else ok(`L2-ARIA OK: role="status" + aria-live="polite" (내용 "${lo.text}")`);

  if (lo.notInert.length > 0) fail(`L3: inert 누락 [${lo.notInert.join(', ')}]`);
  else if (lo.containerHasInert) fail('L3: 포탈 컨테이너 자신에 inert');
  else ok(`L3-INERT OK: body 직계 ${lo.total}개 중 컨테이너 제외 ${lo.total - 1}개 전부 inert [${lo.inertNames.join(', ')}]`);

  if (lo.overflow !== 'hidden') fail(`L4: 열림 중 overflow=${lo.overflow}`);
  else ok(`L4-OVERFLOW OK: ${beforeOverflow} → hidden`);

  if (lo.focusablesInside !== 0) fail(`L5: 오버레이 내부 focusable ${lo.focusablesInside}개`);
  else ok('L5-NO-TRAP-RATIONALE OK: 오버레이 내부 focusable 0개 — 트랩을 걸면 포커스가 갇힌다(미적용 근거 실측)');

  // 뒤 폼 Tab 도달 불가
  await page.evaluate(() => document.body.focus());
  let reached = null;
  for (let i = 0; i < 15; i++) {
    await page.keyboard.press('Tab');
    const r = await page.evaluate(() => {
      const c = document.querySelector('[data-loading-portal]');
      const a = document.activeElement;
      if (!a || a === document.body || a.tagName === 'HTML') return { bg: false, name: '(body)' };
      return { bg: !c?.contains(a), name: a.tagName.toLowerCase() + ':' + ((a.getAttribute('placeholder') || a.textContent || '').trim().slice(0, 20)) };
    });
    if (r.bg) { reached = `Tab×${i + 1} → ${r.name}`; break; }
  }
  if (reached) fail(`L6: 배경(폼)에 Tab 도달 — ${reached}`);
  else ok(`L6-TAB OK: Tab×15 동안 배경에 한 번도 도달 못함 (열기 전 tabbable ${beforeTabbables}개)`);

  // Escape 를 눌러도 닫히지 않아야 한다(취소 경로 없음 → 의도적으로 미부착)
  await page.keyboard.press('Escape');
  await page.waitForTimeout(600);
  const stillThere = await page.locator('[data-loading-portal] [role="status"]').count();
  if (stillThere !== 1) fail(`L7: Escape로 로딩 오버레이가 닫힘 (취소 경로가 없어 닫히면 안 됨) count=${stillThere}`);
  else ok('L7-NO-ESC OK: Escape에도 로딩 오버레이 유지 (취소 불가 작업이라 의도적 미부착)');

  // 로딩 종료 후 복원 (요청 abort → catch → setLoading(false))
  await page.waitForTimeout(11000);
  const after = await page.evaluate(() => ({
    statusCount: document.querySelectorAll('[role="status"]').length,
    inertLeft: Array.from(document.body.children).filter((k) => k.hasAttribute('inert')).length,
    overflow: document.body.style.overflow || '(빈 문자열)',
    portalStillThere: !!document.querySelector('[data-loading-portal]'),
  }));
  if (after.statusCount !== 0) fail(`L8: 로딩 종료 후 role=status 잔존 ${after.statusCount}개`);
  else ok('L8-EXIT OK: 로딩 종료 후 오버레이 언마운트');
  if (after.inertLeft !== 0) fail(`L9: 종료 후 inert 잔존 ${after.inertLeft}개`);
  else ok('L9-INERT-RESTORE OK: 종료 후 body 직계 inert 0개');
  if (after.overflow !== beforeOverflow) fail(`L10: overflow 미복원 (${beforeOverflow} → ${after.overflow})`);
  else ok(`L10-OVERFLOW-RESTORE OK: ${after.overflow} 로 복원 (열기 전과 동일)`);
}

console.log('=== S-3 LoadingOverlay 실측 ===');
oks.forEach((m) => console.log('  ' + m));
if (errs.length) console.log('\n콘솔/페이지 에러:', errs.slice(0, 6));
console.log('\n=== VERDICT ===');
if (fails.length) { console.log('VERDICT: FAIL (' + fails.length + '건)'); fails.forEach((m, i) => console.log(`  ${i + 1}. ${m}`)); }
else console.log('VERDICT: PASS');
await browser.close();
process.exit(fails.length ? 1 : 0);
