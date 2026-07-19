'use client';

/**
 * 저장소의 오버레이 "배경 봉쇄" 표준 패턴 — portal + inert + 스크롤 잠금.
 *
 * body 직계에 전용 컨테이너를 하나 만들어 돌려준다. 호출부는 그 안으로 `createPortal` 한다.
 * body 직계에 붙여야 "배경 = body의 나머지 직계 자식"이라는 단순한 규칙으로 `inert`를 걸 수 있다
 * (레이아웃 래퍼 + BottomNav). `active` 동안:
 *
 * - 컨테이너를 제외한 body 직계 자식 전부에 `inert` 부여 → 배경의 포인터·Tab·스크린리더 접근 차단.
 *   이미 `inert`를 갖고 있던 요소는 Map에 원래 값을 저장했다가 그 값으로 되돌린다
 *   (일괄 `removeAttribute`는 남의 inert를 지운다).
 * - `document.body.style.overflow`의 **인라인 값을 저장**했다가 그대로 복원한다.
 *   `'unset'`으로 리셋하지 않는다 — 열리기 전에 다른 코드가 걸어 둔 값을 조용히 지우기 때문.
 *
 * ⚠ **호출 순서 계약**: 포커스 트랩을 함께 쓰는 오버레이라면 이 훅을 반드시 `useFocusTrap`보다
 * **앞에서** 호출해야 한다. React는 한 컴포넌트의 cleanup을 effect 등록 순서대로 실행하고,
 * 커스텀 훅의 effect는 그 훅을 호출한 지점의 순서로 등록된다. inert 해제가 `useFocusTrap`의
 * 포커스 복원보다 먼저 돌아야 복원 대상(오버레이를 연 버튼)이 그 시점에 focusable하다.
 * 순서가 뒤집히면 아직 inert인 서브트리 안의 요소에 `focus()`를 거는 셈이라 no-op이 되고
 * 포커스가 body로 낙하한다.
 *
 * 포커스 트랩을 **포함하지 않는** 이유: 트랩이 필요 없는 오버레이(사용자가 조작할 수 없는
 * 로딩 대기 화면 등)가 있다. focusable 요소가 하나도 없는 컨테이너에 트랩을 걸면 포커스가
 * 갇힌 채 아무데도 못 가므로, 봉쇄와 트랩은 분리된 선택지로 남긴다.
 *
 * @param attribute 컨테이너를 식별할 data 속성 이름 (예: `'data-chat-portal'`). 디버깅·검증용.
 * @param active 오버레이가 열려 있는가. false면 컨테이너는 남되 inert·스크롤 잠금은 해제된다.
 * @returns 포탈 컨테이너. 첫 렌더에서는 아직 `null`이다(마운트 effect에서 생성).
 */

import { useEffect, useState } from 'react';

export function useOverlayPortal(attribute: string, active: boolean): HTMLDivElement | null {
  const [container, setContainer] = useState<HTMLDivElement | null>(null);

  useEffect(() => {
    const el = document.createElement('div');
    el.setAttribute(attribute, '');
    document.body.appendChild(el);
    setContainer(el);
    return () => {
      el.remove();
    };
  }, [attribute]);

  useEffect(() => {
    if (!active || !container) return;

    const previousInert = new Map<Element, string | null>();
    Array.from(document.body.children).forEach((child) => {
      if (child === container) return;
      previousInert.set(child, child.getAttribute('inert'));
      child.setAttribute('inert', '');
    });

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      previousInert.forEach((prev, child) => {
        if (prev === null) child.removeAttribute('inert');
        else child.setAttribute('inert', prev);
      });
      document.body.style.overflow = previousOverflow;
    };
  }, [active, container]);

  return container;
}

export default useOverlayPortal;
