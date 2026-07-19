// e2e 접근성 하네스 공통 설정.
// 각 하네스는 독립 실행 스크립트다(Playwright Test 러너를 쓰지 않는다) — 하나의 페이지 위에서
// 열기/닫기/리렌더가 순서대로 누적되는 상태 기계라 테스트 격리·병렬화가 오히려 계약을 깬다.
// 여기서는 4개 스크립트가 공유해야 하는 것(브라우저 채널·베이스 URL·fixture·산출물 경로)만 모은다.
import { chromium } from 'playwright';
import { mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const E2E_DIR = join(dirname(fileURLToPath(import.meta.url)), '..');

// 프로덕션 빌드(`npm run build && npm run start`)를 띄운 주소.
// 포트를 바꿔 띄웠다면 E2E_BASE_URL 로 넘긴다.
export const BASE = process.env.E2E_BASE_URL || 'http://localhost:3456';

/**
 * 브라우저 채널 결정.
 * - CI(ubuntu-latest)에는 시스템 Chrome이 없다 → 번들 chromium(채널 미지정)을 쓴다.
 * - 로컬 개발 머신에서는 시스템 Chrome('chrome')이 기본이다.
 * - PW_CHANNEL 로 강제 지정 가능. PW_CHANNEL='' (빈 문자열)이면 로컬에서도 번들 chromium을
 *   쓰게 되어 CI와 동일한 조건을 재현할 수 있다.
 */
export function browserChannel() {
  if (process.env.PW_CHANNEL !== undefined) return process.env.PW_CHANNEL || undefined;
  return process.env.CI ? undefined : 'chrome';
}

export async function launchBrowser(opts = {}) {
  const channel = browserChannel();
  console.log(`[harness] base=${BASE} channel=${channel ?? '(번들 chromium)'}`);
  return chromium.launch({ ...(channel ? { channel } : {}), ...opts });
}

// 결과 페이지 렌더에 주입하는 mock 사주 응답 (localStorage 'saju-storage').
export function loadMock() {
  return JSON.parse(readFileSync(join(E2E_DIR, 'fixtures', 'mock-saju.json'), 'utf8'));
}

// 스크린샷 등 산출물 경로. cwd 와 무관하게 e2e/.artifacts 아래로 모은다(gitignore 대상).
export function artifact(name) {
  const p = join(E2E_DIR, '.artifacts', name);
  mkdirSync(dirname(p), { recursive: true });
  return p;
}
