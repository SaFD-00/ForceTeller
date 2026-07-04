import { defineConfig } from 'vitest/config';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// tsconfig의 "@/*" 경로 별칭을 vitest에도 동일하게 매핑(transforms.ts 등이 @/ import 사용).
const root = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      '@': root,
    },
  },
  test: {
    // lib의 순수 함수 단위 테스트만 대상. 컴포넌트/DOM 테스트 없음 → node 환경.
    include: ['lib/**/*.test.ts'],
    environment: 'node',
  },
});
