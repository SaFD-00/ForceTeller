import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import ssotConfig from '../tailwind.config';

// S-4: 토큰 패리티 테스트.
// SSOT(web/tailwind.config.ts) 와 두 미러(.ds-css/tailwind.ds.config.cjs,
// .design-sync/ds-tokens/tokens.css)의 값이 실제로 일치하는지 기계적으로 단언한다.
// 세 파일 중 하나라도 값이 어긋나면 이 테스트가 FAIL 해야 한다(산문 규칙 → CI 게이트 전환).

const require_ = createRequire(import.meta.url);
const dsConfig = require_('../.ds-css/tailwind.ds.config.cjs');

const tokensCssPath = fileURLToPath(
  new URL('../.design-sync/ds-tokens/tokens.css', import.meta.url)
);
const tokensCss = readFileSync(tokensCssPath, 'utf8');

const ssotColors = ssotConfig.theme!.extend!.colors as Record<string, unknown>;
const ssotRadius = ssotConfig.theme!.extend!.borderRadius as Record<string, string>;
const ssotBorderWidth = ssotConfig.theme!.extend!.borderWidth as Record<string, string>;
const ssotShadow = ssotConfig.theme!.extend!.boxShadow as Record<string, string>;

// ---- 1) tailwind.config.ts (SSOT) ↔ .ds-css/tailwind.ds.config.cjs -------------------
// fontFamily/content/safelist 는 의도된 차이(주석에 문서화됨)이므로 비교 대상에서 제외한다:
//  - fontFamily: 프리뷰엔 next/font 변수가 없어 리터럴 폰트명을 쓴다.
//  - content/safelist: 프리뷰 전용 글롭 + purge 방지 safelist.
describe('tailwind.config.ts (SSOT) ↔ tailwind.ds.config.cjs', () => {
  it('colors 가 완전히 일치한다', () => {
    expect(dsConfig.theme.extend.colors).toEqual(ssotColors);
  });

  it('borderRadius 가 완전히 일치한다', () => {
    expect(dsConfig.theme.extend.borderRadius).toEqual(ssotRadius);
  });

  it('borderWidth 가 완전히 일치한다', () => {
    expect(dsConfig.theme.extend.borderWidth).toEqual(ssotBorderWidth);
  });

  it('boxShadow 가 완전히 일치한다', () => {
    expect(dsConfig.theme.extend.boxShadow).toEqual(ssotShadow);
  });

  it('corePlugins.boxShadowColor 가 동일하게 비활성화돼 있다', () => {
    expect(dsConfig.corePlugins).toEqual(ssotConfig.corePlugins);
  });
});

// ---- 2) tailwind.config.ts (SSOT) ↔ tokens.css --------------------------------------

// colors 는 중첩 구조(문자열 | {DEFAULT, foreground?, ink?} | {하위키: {...}})를
// --ft-color-<경로> 네이밍으로 평탄화한다. DEFAULT 는 접미사 없이 자기 경로에 매핑된다.
function flattenColorTokens(node: unknown, path: string[], out: Record<string, string>) {
  if (typeof node === 'string') {
    out[path.join('-')] = node.toLowerCase();
    return;
  }
  if (typeof node === 'object' && node !== null) {
    for (const [key, value] of Object.entries(node)) {
      const nextPath = key === 'DEFAULT' ? path : [...path, key];
      flattenColorTokens(value, nextPath, out);
    }
  }
}

function parseCssVars(css: string, prefix: string): Record<string, string> {
  const re = new RegExp(`--${prefix}-([a-z0-9-]+):\\s*([^;]+);`, 'g');
  const out: Record<string, string> = {};
  let match: RegExpExecArray | null;
  while ((match = re.exec(css)) !== null) {
    out[match[1]] = match[2].trim().toLowerCase();
  }
  return out;
}

describe('tailwind.config.ts (SSOT) ↔ tokens.css', () => {
  it('color 토큰이 모두 존재하고 값이 일치한다', () => {
    const expected: Record<string, string> = {};
    for (const [key, value] of Object.entries(ssotColors)) {
      flattenColorTokens(value, [key], expected);
    }
    const actual = parseCssVars(tokensCss, 'ft-color');

    for (const [key, expectedValue] of Object.entries(expected)) {
      expect(actual, `--ft-color-${key} 가 tokens.css 에 없다`).toHaveProperty(key);
      expect(actual[key], `--ft-color-${key} 값 불일치`).toBe(expectedValue);
    }
  });

  it('borderRadius 6단계가 모두 존재하고 값이 일치한다', () => {
    const actual = parseCssVars(tokensCss, 'ft-radius');
    for (const [key, expectedValue] of Object.entries(ssotRadius)) {
      expect(actual, `--ft-radius-${key} 가 tokens.css 에 없다`).toHaveProperty(key);
      expect(actual[key], `--ft-radius-${key} 값 불일치`).toBe(expectedValue.toLowerCase());
    }
  });

  it('borderWidth 가 모두 존재하고 값이 일치한다 (1.5=block 시맨틱 별칭, 3=리터럴)', () => {
    // tokens.css 는 borderWidth['1.5']를 손그림 카드의 시맨틱 이름(--ft-border-block)으로
    // 노출한다(리터럴 --ft-border-1.5 는 CSS 커스텀 프로퍼티 이름 관례상 쓰지 않음).
    // borderWidth['3']은 --ft-border-3 로 리터럴 매핑한다.
    const BORDER_WIDTH_CSS_VAR: Record<string, string> = {
      '1.5': 'block',
      '3': '3',
    };
    const actual = parseCssVars(tokensCss, 'ft-border');
    for (const [key, expectedValue] of Object.entries(ssotBorderWidth)) {
      const cssKey = BORDER_WIDTH_CSS_VAR[key];
      expect(cssKey, `borderWidth['${key}']에 대응하는 tokens.css 매핑이 테스트에 없다`).toBeDefined();
      expect(actual, `--ft-border-${cssKey} 가 tokens.css 에 없다`).toHaveProperty(cssKey);
      expect(actual[cssKey], `--ft-border-${cssKey} 값 불일치`).toBe(expectedValue.toLowerCase());
    }
  });

  it('boxShadow 6종이 모두 존재하고 값이 일치한다 (공백 차이는 무시)', () => {
    // rgba(38,61,91,0.12) vs rgba(38, 61, 91, 0.12) 처럼 공백 표기 차이,
    // 0.10 vs 0.1 처럼 소수 트레일링 zero 표기 차이가 있어도 값 자체가 같으면
    // 통과해야 하므로 공백 제거 + 소수 리터럴을 parseFloat 왕복으로 정규화한다.
    const normalize = (s: string) =>
      s.replace(/\s+/g, '').replace(/\d+\.\d+/g, (m) => String(parseFloat(m)));
    const actual = parseCssVars(tokensCss, 'ft-shadow');
    for (const [key, expectedValue] of Object.entries(ssotShadow)) {
      expect(actual, `--ft-shadow-${key} 가 tokens.css 에 없다`).toHaveProperty(key);
      expect(normalize(actual[key]), `--ft-shadow-${key} 값 불일치`).toBe(
        normalize(expectedValue.toLowerCase())
      );
    }
  });
});
