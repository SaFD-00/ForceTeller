// S-3 검증: 모바일 채팅 오버레이(390x844) + LoadingOverlay(/) 접근성 계약 실측.
import { BASE, launchBrowser, loadMock } from './lib/harness.mjs';

const MOCK = loadMock();
const fails = [];
const oks = [];
const ok = (m) => oks.push(m);
const fail = (m) => fails.push(m);

const browser = await launchBrowser();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
const page = await ctx.newPage();
const errs = [];
page.on('pageerror', (e) => errs.push(e.message.slice(0, 200)));
page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });

await page.addInitScript((m) => {
  localStorage.setItem('saju-storage', JSON.stringify({ state: { result: m }, version: 0 }));
}, MOCK);

// ───────────────────────── A. 모바일 채팅 오버레이 ─────────────────────────
await page.goto(BASE + '/result', { waitUntil: 'networkidle', timeout: 90000 });
await page.waitForTimeout(2000);

const trigger = page.getByRole('button', { name: 'AI 상담 열기' });
if ((await trigger.count()) !== 1) fail(`M0: "AI 상담 열기" 버튼 ${await trigger.count()}개 (기대 1)`);
else ok('M0: 모바일 뷰포트에서 "AI 상담 열기" 트리거 존재');

const beforeOverflow = await page.evaluate(() => document.body.style.overflow || '(빈 문자열)');
await trigger.scrollIntoViewIfNeeded();
await trigger.focus();
const triggerText = await page.evaluate(() => document.activeElement?.textContent?.trim() ?? null);
await trigger.click();
await page.waitForTimeout(900);

// (0) portal 위치 + AnimatePresence가 portal 안쪽
const portalInfo = await page.evaluate(() => {
  const c = document.querySelector('[data-chat-portal]');
  if (!c) return { exists: false };
  return {
    exists: true,
    isBodyChild: c.parentElement === document.body,
    dialogsInside: c.querySelectorAll('[role="dialog"]').length,
    dialogsOutside: document.querySelectorAll('[role="dialog"]').length - c.querySelectorAll('[role="dialog"]').length,
  };
});
if (!portalInfo.exists) fail('M1: [data-chat-portal] 컨테이너 없음');
else if (!portalInfo.isBodyChild) fail('M1: 포탈 컨테이너가 body 직계가 아님');
else if (portalInfo.dialogsInside !== 1 || portalInfo.dialogsOutside !== 0)
  fail(`M1: dialog 위치 이상 inside=${portalInfo.dialogsInside} outside=${portalInfo.dialogsOutside}`);
else ok('M1-PORTAL OK: body 직계 [data-chat-portal] 안에 role=dialog 1개 (밖 0개)');

// (1) ARIA
const aria = await page.evaluate(() => {
  const d = document.querySelector('[data-chat-portal] [role="dialog"]');
  if (!d) return null;
  const id = d.getAttribute('aria-labelledby');
  const label = id ? document.getElementById(id) : null;
  const close = d.querySelector('button[aria-label]');
  return {
    ariaModal: d.getAttribute('aria-modal'),
    labelledby: id,
    labelText: label ? label.textContent.trim() : null,
    labelInsideDialog: label ? d.contains(label) : false,
    closeLabel: close ? close.getAttribute('aria-label') : null,
    tabIndex: d.getAttribute('tabindex'),
  };
});
if (!aria) fail('M2: dialog 미검출');
else if (aria.ariaModal !== 'true') fail(`M2: aria-modal=${aria.ariaModal}`);
else if (!aria.labelText || !aria.labelInsideDialog) fail(`M2: aria-labelledby 해석 실패 (${aria.labelledby} → ${aria.labelText})`);
else if (aria.closeLabel !== 'AI 상담 닫기') fail(`M2: 닫기 버튼 aria-label=${aria.closeLabel}`);
else ok(`M2-ARIA OK: role=dialog aria-modal=true aria-labelledby→"${aria.labelText}" tabindex=${aria.tabIndex} / 닫기 aria-label="${aria.closeLabel}"`);

// (2) body 직계 inert
const inert = await page.evaluate(() => {
  const c = document.querySelector('[data-chat-portal]');
  const kids = Array.from(document.body.children);
  return {
    total: kids.length,
    notInert: kids.filter((k) => k !== c && !k.hasAttribute('inert')).map((k) => k.tagName.toLowerCase() + (k.className && typeof k.className === 'string' ? '.' + k.className.split(' ').slice(0, 2).join('.') : '')),
    containerHasInert: c?.hasAttribute('inert') ?? null,
    names: kids.filter((k) => k !== c).map((k) => k.tagName.toLowerCase()),
  };
});
if (inert.notInert.length > 0) fail(`M3: inert 누락 ${inert.notInert.length}개 [${inert.notInert.join(', ')}]`);
else if (inert.containerHasInert) fail('M3: 포탈 컨테이너 자신에 inert가 걸림');
else ok(`M3-INERT OK: body 직계 ${inert.total}개 중 컨테이너 제외 ${inert.total - 1}개 전부 inert [${inert.names.join(', ')}]`);

// (3) overflow 잠금
const duringOverflow = await page.evaluate(() => document.body.style.overflow);
if (duringOverflow !== 'hidden') fail(`M4: 열림 중 body overflow=${duringOverflow} (기대 hidden)`);
else ok(`M4-OVERFLOW(열림) OK: ${beforeOverflow} → hidden`);

// (4) 포커스가 오버레이 내부인가
const focusIn = await page.evaluate(() => {
  const d = document.querySelector('[data-chat-portal] [role="dialog"]');
  const a = document.activeElement;
  return { inside: !!(d && a && d.contains(a)), isDialogItself: d === a, tag: a?.tagName.toLowerCase(), cls: (a?.className || '').toString().slice(0, 40) };
});
if (!focusIn.inside) fail(`M5: 오픈 직후 포커스가 오버레이 밖 (<${focusIn.tag}>)`);
else ok(`M5-FOCUS OK: 오픈 직후 포커스가 오버레이 내부 (다이얼로그 컨테이너 자신=${focusIn.isDialogItself}, <${focusIn.tag}>)`);

// (5) Tab 트랩
let trapBreak = null;
for (let i = 0; i < 8; i++) {
  await page.keyboard.press('Tab');
  const r = await page.evaluate(() => {
    const d = document.querySelector('[data-chat-portal] [role="dialog"]');
    const a = document.activeElement;
    return { inside: !!(d && a && d.contains(a)), tag: a?.tagName.toLowerCase(), label: (a?.getAttribute?.('aria-label') || a?.textContent || '').trim().slice(0, 24) };
  });
  if (!r.inside) { trapBreak = `Tab×${i + 1} 후 <${r.tag}> "${r.label}"`; break; }
}
if (!trapBreak) {
  for (let i = 0; i < 3; i++) {
    await page.keyboard.press('Shift+Tab');
    const r = await page.evaluate(() => {
      const d = document.querySelector('[data-chat-portal] [role="dialog"]');
      const a = document.activeElement;
      return { inside: !!(d && a && d.contains(a)), tag: a?.tagName.toLowerCase() };
    });
    if (!r.inside) { trapBreak = `Shift+Tab×${i + 1} 후 <${r.tag}>`; break; }
  }
}
if (trapBreak) fail(`M6: 포커스 트랩 탈출 — ${trapBreak}`);
else ok('M6-TRAP OK: Tab×8 · Shift+Tab×3 전부 오버레이 내부 유지');

// (6) Escape로 닫힘 + 포커스 복귀 + inert/overflow 복원
await page.keyboard.press('Escape');
await page.waitForTimeout(1200);
const after = await page.evaluate(() => {
  const c = document.querySelector('[data-chat-portal]');
  const a = document.activeElement;
  return {
    dialogGone: document.querySelectorAll('[role="dialog"]').length === 0,
    inertLeft: Array.from(document.body.children).filter((k) => k.hasAttribute('inert')).length,
    overflow: document.body.style.overflow || '(빈 문자열)',
    focusTag: a?.tagName.toLowerCase(),
    focusText: a?.textContent?.trim().slice(0, 30) ?? null,
    portalStillThere: !!c,
  };
});
if (!after.dialogGone) fail('M7: Escape 후에도 dialog 잔존');
else ok('M7-ESC OK: Escape로 오버레이 닫힘 (exit 애니메이션 후 dialog 0개)');
if (after.inertLeft !== 0) fail(`M8: 닫힘 후 inert 잔존 ${after.inertLeft}개`);
else ok('M8-INERT-RESTORE OK: 닫힘 후 body 직계 inert 보유 0개');
if (after.overflow !== beforeOverflow) fail(`M9: overflow 미복원 (${beforeOverflow} → ${after.overflow})`);
else ok(`M9-OVERFLOW-RESTORE OK: 닫힘 후 ${after.overflow} 로 복원 (열기 전과 동일)`);
if (after.focusTag !== 'button' || !after.focusText?.includes('AI 상담')) fail(`M10: 포커스 복귀 실패 — <${after.focusTag}> "${after.focusText}" (트리거는 "${triggerText}")`);
else ok(`M10-FOCUS-RETURN OK: Escape 후 포커스가 트리거 버튼("${after.focusText}")으로 복귀`);

// (7) 닫기 버튼 경로도 확인
await page.getByRole('button', { name: 'AI 상담 열기' }).click();
await page.waitForTimeout(700);
await page.evaluate(() => document.querySelector('[data-chat-portal] [role="dialog"] button[aria-label="AI 상담 닫기"]')?.click());
await page.waitForTimeout(1200);
const afterBtn = await page.evaluate(() => ({
  gone: document.querySelectorAll('[role="dialog"]').length === 0,
  inertLeft: Array.from(document.body.children).filter((k) => k.hasAttribute('inert')).length,
  focusText: document.activeElement?.textContent?.trim().slice(0, 30) ?? null,
}));
if (!afterBtn.gone || afterBtn.inertLeft !== 0) fail(`M11: 닫기 버튼 경로 — gone=${afterBtn.gone} inertLeft=${afterBtn.inertLeft}`);
else ok(`M11-CLOSE-BTN OK: 닫기 버튼으로도 닫힘 · inert 0 · 포커스="${afterBtn.focusText}"`);

// (B. LoadingOverlay 는 s3-loading.mjs 로 분리 — 실제 폼 제출 경로가 필요해 별도 스크립트로 실측)

console.log('=== S-3 실측 ===');
oks.forEach((m) => console.log('  ' + m));
if (errs.length) console.log('\n콘솔/페이지 에러:', errs.slice(0, 6));
if (fails.length) {
  console.log('\n=== VERDICT ===\nVERDICT: FAIL (' + fails.length + '건)');
  fails.forEach((m, i) => console.log(`  ${i + 1}. ${m}`));
} else {
  console.log('\n=== VERDICT ===\nVERDICT: PASS');
}
await browser.close();
process.exit(fails.length ? 1 : 0);
