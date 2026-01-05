# Refined Plan: Fortune-Teller 전체 리팩토링

**Status**: Refined
**Original Plan**: [PLAN_fortune-teller-refactoring.md](PLAN_fortune-teller-refactoring.md)
**Interview Date**: 2026-01-05
**Last Updated**: 2026-01-05

---

## Interview Summary

### Categories Covered
- [x] Technical Implementation
- [ ] UI/UX
- [x] Concerns & Risks
- [x] Tradeoffs
- [x] Edge Cases
- [ ] Integration

### Interview Scope
Medium - 8 questions, approximately 15 minutes

---

## Key Decisions

인터뷰를 통해 확정된 핵심 결정 사항:

| # | Decision | Rationale | Impact Scope |
|---|----------|-----------|--------------|
| 1 | **하이브리드 인터페이스** (Protocol + ABC) | Protocol은 타입 힌팅용, ABC는 핵심 클래스용으로 역할 분리 | `utils/protocols.py`, `agents/base_agent.py` |
| 2 | **FastAPI Depends로 SessionManager 주입** | 테스트 시 오버라이드 용이, 표준 패턴 | `api/routes/*.py`, `api/dependencies.py` |
| 3 | **표준 logging 사용** | 추가 의존성 없음, Python 기본 제공 | `config/logging_config.py` |
| 4 | **기존 에이전트 파일 삭제** | Factory 패턴 완전 전환, 코드 중복 제거 | `agents/interpreters/*.py` 삭제 |
| 5 | **전체 서비스 계층에 DI 적용** | 테스트 가능성 극대화, 일관된 아키텍처 | 전체 모듈 |
| 6 | **설정 오류 시 시작 실패 (Fast-fail)** | 런타임 오류 방지, 문제 조기 발견 | `config/settings.py` |
| 7 | **80% 테스트 커버리지 유지** | 비즈니스 로직 안정성 확보 | `tests/` |
| 8 | **에이전트 확장은 설정만으로** | 코드 수정 없이 새 에이전트 추가 가능 | `agents/agent_configs.py` |

---

## Technical Specifications

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          API Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ chat.py     │  │ analysis.py │  │ manseol.py              │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
│         │                │                      │                │
│         └────────────────┼──────────────────────┘                │
│                          │                                       │
│              ┌───────────▼───────────┐                          │
│              │   api/dependencies.py  │ ◄── FastAPI Depends     │
│              │   - get_session_manager│                          │
│              │   - get_orchestrator   │                          │
│              │   - get_llm_client     │                          │
│              └───────────┬───────────┘                          │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       Service Layer                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Orchestrator                          │    │
│  │  - AgentFactory 사용                                     │    │
│  │  - 키워드 기반 에이전트 선택                              │    │
│  │  - 병렬 에이전트 실행                                    │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                     │
│  ┌─────────────────────────▼───────────────────────────────┐    │
│  │                   AgentFactory                           │    │
│  │  - AgentConfig 기반 에이전트 생성                        │    │
│  │  - 8개 에이전트 타입 지원                                │    │
│  │  - LLMClient 주입                                        │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                     │
│  ┌─────────────────────────▼───────────────────────────────┐    │
│  │                    BaseAgent                             │    │
│  │  - ABC 기반 추상 클래스                                  │    │
│  │  - interpret(), answer_question()                        │    │
│  │  - LLMClientProtocol 의존성 주입                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Infrastructure Layer                         │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │  SessionManager   │  │    LLMClient      │                   │
│  │  (싱글톤 via DI)  │  │  (OpenAI/Gemini)  │                   │
│  └───────────────────┘  └───────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Protocol & ABC 하이브리드 설계

```python
# utils/protocols.py - 타입 힌팅용 Protocol
from typing import Protocol, Dict, List, Optional

class LLMClientProtocol(Protocol):
    async def chat(
        self,
        messages: List[Dict],
        response_schema: Optional[Dict] = None
    ) -> Dict: ...

    async def chat_stream(
        self,
        messages: List[Dict]
    ) -> AsyncGenerator[str, None]: ...

class SessionManagerProtocol(Protocol):
    def create_session(self, saju_data: Dict) -> "Session": ...
    def get_session(self, session_id: str) -> Optional["Session"]: ...
    def delete_session(self, session_id: str) -> bool: ...


# agents/base_agent.py - 핵심 로직용 ABC
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm_client: Optional[LLMClientProtocol] = None,  # DI
        **kwargs
    ):
        self.name = name
        self.system_prompt = system_prompt
        self._llm_client = llm_client or LLMClient()

    @abstractmethod
    def get_interpretation_focus(self) -> str:
        """각 에이전트의 해석 초점 반환"""
        pass

    async def interpret(self, saju_data: Dict, question: str) -> AgentResponse:
        """공통 해석 로직"""
        # 구현...
```

### AgentConfig 데이터 모델

```python
# agents/config.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentConfig:
    """에이전트 설정 데이터 클래스"""
    name: str                      # 내부 식별자 (예: "personality")
    display_name: str              # 표시 이름 (예: "성격 분석")
    system_prompt: str             # 시스템 프롬프트
    interpretation_focus: str      # 해석 초점 설명
    keywords: List[str] = field(default_factory=list)  # 라우팅 키워드


# agents/agent_configs.py
from agents.prompts.system_prompts import (
    PERSONALITY_SYSTEM_PROMPT,
    CAREER_SYSTEM_PROMPT,
    # ...
)

AGENT_CONFIGS: Dict[str, AgentConfig] = {
    "personality": AgentConfig(
        name="personality",
        display_name="성격 분석",
        system_prompt=PERSONALITY_SYSTEM_PROMPT,
        interpretation_focus="성격, 기질, 성향, 특성 분석",
        keywords=["성격", "기질", "성향", "특성", "장점", "단점"]
    ),
    "career": AgentConfig(
        name="career",
        display_name="직업/재물 분석",
        system_prompt=CAREER_SYSTEM_PROMPT,
        interpretation_focus="직업 적성, 재물운, 사업운 분석",
        keywords=["직업", "일", "직장", "취업", "돈", "재물", "투자"]
    ),
    # ... 나머지 6개 에이전트
}
```

### Technology Stack

- **인터페이스**: `typing.Protocol` - 타입 힌팅 및 구조적 서브타이핑
- **추상 클래스**: `abc.ABC` - 핵심 클래스 계약 강제
- **의존성 주입**: `FastAPI Depends()` - 테스트 시 오버라이드 용이
- **로깅**: `logging` (표준 라이브러리) - 추가 의존성 없음
- **설정 관리**: `pydantic-settings` - 타입 안전한 환경 변수

---

## Concerns Addressed

### LLM API 테스트 비용

- **Concern**: 테스트 실행 시마다 LLM API 호출 비용 발생
- **Resolution**:
  - 단위 테스트: 모든 LLM 호출을 Mock으로 대체
  - 통합 테스트: 실제 API 허용 (선별적으로 실행)
  - `@pytest.mark.integration` 마커로 통합 테스트 분리

### 프론트엔드 호환성

- **Concern**: 백엔드 API 변경 시 프론트엔드 영향
- **Resolution**:
  - API 응답 스키마는 변경하지 않음 (내부 리팩토링만)
  - 필요시 프론트엔드도 함께 수정 가능
  - 현재 프로덕션 배포 없으므로 유연하게 대응

### 설정 오류 처리

- **Concern**: 런타임에 설정 오류 발생 시 예측 불가능한 동작
- **Resolution**:
  - Fast-fail 정책: 시작 시 모든 설정 검증
  - Pydantic 모델로 설정 값 타입/범위 검증
  - 검증 실패 시 명확한 에러 메시지와 함께 시작 거부

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior | Error Message |
|----------|-------------------|---------------|
| 존재하지 않는 에이전트 타입 요청 | `AgentNotFoundError` 발생 | "Unknown agent type: {type}. Available: personality, career, ..." |
| 필수 설정 값 누락 | 애플리케이션 시작 실패 | "Missing required setting: {setting_name}" |
| LLM API 호출 실패 | 재시도 후 에러 응답 반환 | "AI 해석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요." |
| 세션 만료/미존재 | `SessionNotFoundError` 발생 | "Session not found: {session_id}" |
| AgentConfig 키워드 중복 | 첫 번째 매칭 에이전트 선택 | 경고 로그: "Duplicate keyword '{keyword}' in agents: {agents}" |
| 빈 질문 입력 | 기본 종합 분석 수행 | - |

---

## Tradeoff Analysis

### 1. Protocol vs ABC 선택

- **Choice**: 하이브리드 (Protocol + ABC)
- **Alternative**: Protocol만 사용 또는 ABC만 사용
- **Rationale**:
  - Protocol: 외부 의존성(LLMClient)에 대한 유연한 타입 힌팅
  - ABC: 핵심 클래스(BaseAgent)의 계약 강제 및 공통 로직 구현
- **Accepted Drawbacks**: 두 가지 패턴을 이해해야 하는 학습 곡선

### 2. 기존 에이전트 파일 삭제 vs 유지

- **Choice**: 완전 삭제
- **Alternative**: deprecated 표시 후 유지
- **Rationale**:
  - Factory 패턴으로 완전 전환
  - 코드 중복 완전 제거
  - 유지보수 포인트 단일화
- **Accepted Drawbacks**: 기존 직접 import 코드 호환성 깨짐 (내부 사용만이므로 영향 없음)

### 3. DI 적용 범위

- **Choice**: 전체 서비스 계층
- **Alternative**: 핵심 컴포넌트만 (LLMClient, SessionManager)
- **Rationale**:
  - 일관된 아키텍처
  - 모든 컴포넌트 독립적 테스트 가능
  - 향후 확장 시 유연성
- **Accepted Drawbacks**: 초기 구현 복잡도 증가, 보일러플레이트 코드 증가

### 4. 테스트 커버리지 80%

- **Choice**: 80% 유지
- **Alternative**: 60-70%로 낮춤
- **Rationale**:
  - 비즈니스 로직(만세력 계산, 에이전트 해석)의 정확성이 중요
  - 리팩토링 안전망으로서 높은 커버리지 필요
- **Accepted Drawbacks**: 테스트 작성 시간 증가, 일부 유틸리티 코드도 테스트 필요

---

## Updated Implementation Plan

### Changes

| Original | Updated | Reason for Change |
|----------|---------|-------------------|
| Protocol만 사용 | Protocol + ABC 하이브리드 | 핵심 클래스에 계약 강제 필요 |
| structlog 고려 | 표준 logging 확정 | 추가 의존성 제거, 단순화 |
| 기존 에이전트 deprecated | 완전 삭제 | 코드 중복 완전 제거 |
| 핵심 컴포넌트만 DI | 전체 서비스 계층 DI | 일관된 아키텍처, 테스트 용이성 |

### Added Tasks

- [ ] **Task 2.8**: 설정 검증 로직 추가 (Fast-fail)
  - File: `config/settings.py`
  - 시작 시 모든 설정 값 검증, 실패 시 명확한 에러

- [ ] **Task 3.9**: AgentConfig 키워드 중복 검사
  - File: `agents/factory.py`
  - 동일 키워드가 여러 에이전트에 있으면 경고 로그

- [ ] **Task 4.9**: API 엔드포인트 응답 스키마 문서화
  - File: `api/schemas.py`
  - 기존 응답 스키마 명시적 정의로 호환성 보장

### Removed Tasks

- ~~deprecated 표시 유지~~ - Reason: Factory 완전 전환으로 불필요

### Priority Adjustments

1. **High**: Phase 1 (테스트 인프라) - 리팩토링 안전망
2. **High**: Phase 2 (DI 패턴) - 테스트 가능한 구조
3. **Medium**: Phase 3 (에이전트 팩토리) - 중복 제거
4. **Medium**: Phase 4 (API 중복 제거) - 코드 정리
5. **Low**: Phase 5 (로깅 개선) - 운영 편의성
6. **Low**: Phase 6 (타입 안전성) - 품질 향상

---

## Interview Notes

### Key Insights

- 현재 프로덕션 배포가 없으므로 리팩토링에 유연하게 대응 가능
- 프론트엔드(web/)도 필요시 함께 수정 가능하여 API 호환성 부담 감소
- LLM 테스트 비용보다 테스트 품질이 우선 (통합 테스트 허용)
- 새 에이전트 추가는 설정만으로 가능해야 함 (개발자 경험)

### Follow-up Actions

- [ ] Phase 1 시작 전 현재 코드 수동 테스트로 기준선 확보
- [ ] pytest-asyncio 설정 확인 (비동기 테스트 지원)
- [ ] 기존 8개 에이전트의 system_prompt 백업

---

## Appendix

### Q&A Log
<details>
<summary>Interview Q&A Record</summary>

**Q1**: Protocol 기반 인터페이스 vs ABC(Abstract Base Class) 중 어떤 것을 선호하시나요?
**A1**: 하이브리드 - Protocol은 타입 힌트용, ABC는 핵심 클래스용

**Q2**: SessionManager를 어떻게 관리할까요?
**A2**: FastAPI 의존성 주입 (Depends() 패턴)

**Q3**: 로깅 라이브러리로 어떤 것을 사용할까요?
**A3**: 표준 logging (추가 의존성 없음)

**Q4**: 기존 에이전트 파일 8개를 어떻게 처리할까요?
**A4**: 삭제 (Factory로 완전 대체)

**Q5**: 리팩토링 중 프로덕션 배포를 어떻게 할 계획인가요?
**A5**: 현재 배포 없음 (로컬/개발 환경만)

**Q6**: 성능 벤치마크 기준이 있나요?
**A6**: 특별한 기준 없음 (기존 성능 유지만 확인)

**Q7**: LLM API 호출 비용이 테스트 시 가장 큰 관심사인가요?
**A7**: 아니오, 단위 테스트는 모킹, 통합 테스트는 실제 API 허용

**Q8**: web/ 프론트엔드에 백엔드 변경이 영향을 미칠 수 있는데, 호환성 검증이 필요한가요?
**A8**: 아니오, 프론트엔드도 함께 수정 가능

**Q9**: DI(의존성 주입) 적용 범위를 어디까지 할까요?
**A9**: 전체 서비스 계층

**Q10**: 80% 테스트 커버리지 목표가 너무 높다고 느껴지시나요?
**A10**: 80% 유지

**Q11**: 새로운 에이전트 타입을 추가할 때 어떤 방식을 선호하시나요?
**A11**: 설정 파일만 수정 (코드 변경 없이)

**Q12**: 설정 파일 오류(누락, 잘못된 값) 시 어떻게 처리할까요?
**A12**: 시작 시 실패 (Fast-fail)

</details>

### References

- [PLAN_fortune-teller-refactoring.md](PLAN_fortune-teller-refactoring.md) - 원본 계획 문서
- [.claude/knowledge/fortuneteller/CLAUDE.md](../../.claude/knowledge/fortuneteller/CLAUDE.md) - 관련 MCP 서버 아키텍처 참조
- [Python typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) - Protocol 공식 문서
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) - FastAPI DI 패턴

---

**Next Steps**:
1. 이 REFINED 문서를 기반으로 Phase 1 구현 시작
2. `/coder` 스킬로 코딩 가이드라인 참조하며 구현
3. 각 Phase 완료 시 PLAN 문서의 체크박스 업데이트
