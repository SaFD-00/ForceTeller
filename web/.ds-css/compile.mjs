// Tailwind v3 → 정적 CSS 컴파일 (design-sync cfg.cssEntry 생성).
// PaperLight 는 v4(@tailwindcss/postcss + @theme inline)였지만 ForceTeller 는 v3 이므로
// tailwindcss(postcss 플러그인) + content 스캔 방식이다.
//
// 입력은 app/globals.css 를 직접 읽는다(별도 input.css 미러를 두지 않아 드리프트 제거).
// globals.css 의 @tailwind/@layer(.glass-card·.element-*·gradient-text 등)와
// tailwind.ds.config.cjs 의 content 가 함께 컴파일된다.
//
// 실행: cwd=web 에서  node .ds-css/compile.mjs
// (content 글롭이 cwd 기준이라 web/ 에서 실행해야 components/** 가 잡힌다.)
import postcss from 'postcss';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const inPath = fileURLToPath(new URL('../app/globals.css', import.meta.url));
const outPath = fileURLToPath(new URL('./ds-compiled.css', import.meta.url));
const cfgPath = fileURLToPath(new URL('./tailwind.ds.config.cjs', import.meta.url));

const css = readFileSync(inPath, 'utf8');
const result = await postcss([tailwindcss(cfgPath), autoprefixer]).process(css, {
  from: inPath,
  to: outPath,
});
writeFileSync(outPath, result.css);
console.error(`[tailwind v3] wrote ${outPath} (${result.css.length} bytes)`);
