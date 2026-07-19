'use client';

/**
 * 저장소의 다이얼로그 포커스 표준 패턴.
 *
 * 열림 시 이전 포커스를 저장하고 컨테이너 자체에 포커스를 준 뒤(닫기 버튼이 아니라 —
 * 스크린리더가 `aria-labelledby` 제목부터 읽게 하려는 의도) Tab/Shift+Tab을 컨테이너 안에
 * 가둔다. 닫힐 때는 저장해 둔 요소로 포커스를 되돌린다.
 *
 * `focus-trap-react` 같은 라이브러리를 쓰지 않는 이유: 필요한 계약이 "순환 + 복귀" 두 가지뿐이라
 * 수십 KB의 의존성과 별도 wrapper 컴포넌트를 들일 만한 근거가 없고, 이 훅은 ref 하나만 받아
 * 기존 마크업을 그대로 둔 채 적용된다.
 */

import { useEffect } from 'react';

const FOCUSABLE_SELECTOR = [
  'a[href]',
  'button:not([disabled])',
  'textarea',
  'input',
  'select',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

function getFocusable(container: HTMLElement): HTMLElement[] {
  return Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
    // 숨겨진 요소 제외 (display:none / visibility:hidden 이면 offsetParent가 없거나 rect가 0)
    (el) => el.offsetParent !== null || el.getClientRects().length > 0
  );
}

export function useFocusTrap<T extends HTMLElement>(
  ref: React.RefObject<T>,
  active: boolean
): void {
  useEffect(() => {
    if (!active) return;

    const container = ref.current;
    if (!container) return;

    const previouslyFocused = document.activeElement as HTMLElement | null;
    container.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      const focusable = getFocusable(container);
      if (focusable.length === 0) {
        // 가둘 대상이 없으면 포커스가 밖으로 새지 않도록 이동 자체를 막는다.
        e.preventDefault();
        return;
      }

      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      const activeEl = document.activeElement;

      if (e.shiftKey) {
        // 컨테이너 자신에 포커스가 있는 초기 상태에서 Shift+Tab 하면 마지막으로 감는다.
        if (activeEl === first || activeEl === container) {
          e.preventDefault();
          last.focus();
        }
      } else if (activeEl === last) {
        e.preventDefault();
        first.focus();
      }
    };

    container.addEventListener('keydown', handleKeyDown);

    return () => {
      container.removeEventListener('keydown', handleKeyDown);
      // 저장 요소가 DOM에서 사라지면 복원을 생략한다(포커스는 body로 낙하) — 현재 모든
      // 호출부의 previouslyFocused는 존속하는 헤딩 버튼이라 실경로 없음. 소멸 가능한
      // 트리거를 도입하면 폴백 설계가 필요하다.
      if (previouslyFocused && document.contains(previouslyFocused)) {
        previouslyFocused.focus();
      }
    };
  }, [ref, active]);
}

export default useFocusTrap;
