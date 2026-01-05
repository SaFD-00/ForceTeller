# Implementation Plan: Fortune-Teller 전체 리팩토링

**Status**: 🔄 In Progress
**Started**: 2026-01-05
**Last Updated**: 2026-01-05
**Scope**: Large (6 Phases)

---

**CRITICAL INSTRUCTIONS**: After completing each phase:
1. Check off completed task checkboxes
2. Run all quality gate validation commands
3. Verify ALL quality gate items pass
4. Update "Last Updated" date above
5. Document learnings in Notes section
6. Only then proceed to next phase

**DO NOT skip quality gates or proceed with failing checks**

**Optional**: Run `/interviewer` on this plan to clarify ambiguous areas before implementation.

---

## Overview

### Feature Description
Fortune-Teller 프로젝트의 전체 리팩토링을 통해 코드 품질, 테스트 가능성, 모듈 결합도를 개선합니다.

### Success Criteria
- [ ] 테스트 커버리지 80% 이상 달성
- [ ] 에이전트 클래스 중복 제거 (8개 → 1개 팩토리 + 설정)
- [ ] 의존성 주입 패턴 적용으로 모킹 가능한 구조
- [ ] API 라우트 중복 로직 추출 및 통합
- [ ] 설정값 중앙 집중화
- [ ] 모든 debug print 문 제거 및 logging 도입

### User Impact
- 버그 수정 및 기능 추가 시간 단축
- 테스트를 통한 안정성 향상
- 새로운 에이전트 추가가 설정만으로 가능

---

## Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| Agent Factory Pattern | 8개 중복 클래스를 1개 팩토리로 통합 | 초기 구현 복잡도 증가, 런타임 설정 의존 |
| Dependency Injection | 테스트 시 모킹 가능, 결합도 감소 | FastAPI Depends 학습 필요 |
| Protocol 기반 인터페이스 | 타입 안전성 + 느슨한 결합 | Python 3.8+ 필요 |
| 중앙 집중식 설정 | 하드코딩 제거, 환경별 설정 용이 | 설정 파일 관리 필요 |

---

## Dependencies

### Required Before Starting
- [ ] Python 3.10+ 확인
- [ ] pytest, pytest-asyncio, pytest-cov 설치
- [ ] 현재 코드가 정상 동작하는지 수동 테스트

### External Dependencies (추가 예정)
- pytest >= 8.0
- pytest-asyncio >= 0.23
- pytest-cov >= 4.0
- pytest-mock >= 3.0

---

## Test Strategy

### Testing Approach
**TDD Principle**: 리팩토링 전 기존 동작을 보장하는 테스트 작성 → 리팩토링 → 테스트 통과 확인

### Test Pyramid for This Feature
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Unit Tests** | ≥80% | 개별 클래스/함수 동작 검증 |
| **Integration Tests** | Critical paths | API 엔드포인트, 에이전트-LLM 연동 |
| **E2E Tests** | Key flows | CLI/서버 전체 흐름 |

### Test File Organization
```
tests/
├── conftest.py              # 공통 fixtures
├── unit/
│   ├── agents/              # 에이전트 테스트
│   ├── conversation/        # 세션 관리 테스트
│   ├── manseol/             # 만세력 계산 테스트
│   └── utils/               # 유틸리티 테스트
├── integration/
│   ├── api/                 # API 엔드포인트 테스트
│   └── agents/              # 에이전트 통합 테스트
└── e2e/
    └── cli/                 # CLI 명령 테스트
```

---

## Implementation Phases

### Phase 1: 테스트 인프라 구축
**Goal**: pytest 설정 및 기본 테스트 구조 수립, 핵심 모듈 테스트 작성
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 1.1**: pytest 설정 및 기본 구조 생성
  - Files: `tests/conftest.py`, `pytest.ini`, `pyproject.toml`
  - 공통 fixtures 정의 (mock_llm_client, mock_session, sample_saju_data)

- [ ] **Test 1.2**: SessionManager 단위 테스트 작성
  - File: `tests/unit/conversation/test_session_manager.py`
  - Test cases:
    - 세션 생성/조회/삭제
    - 메시지 추가/조회
    - 세션 만료 처리
    - 최대 세션 수 초과 시 정리

- [ ] **Test 1.3**: BaseAgent 단위 테스트 작성 (mocked LLM)
  - File: `tests/unit/agents/test_base_agent.py`
  - Test cases:
    - interpret() 메서드 정상 동작
    - answer_question() 메서드
    - LLM 호출 실패 시 에러 처리

- [ ] **Test 1.4**: Orchestrator 단위 테스트 작성
  - File: `tests/unit/agents/test_orchestrator.py`
  - Test cases:
    - 키워드 기반 에이전트 선택
    - 다중 에이전트 선택
    - route_and_interpret() 흐름

**GREEN: Run Tests (기존 코드로 통과)**
- [ ] **Task 1.5**: 테스트 실행 및 커버리지 확인
  - 목표: 기존 코드가 테스트를 통과하는지 확인
  - 커버리지 리포트 생성

**REFACTOR: Test Infrastructure**
- [ ] **Task 1.6**: 테스트 유틸리티 및 fixtures 정리
  - Mock 객체 재사용 가능하도록 정리
  - 테스트 데이터 팩토리 함수 작성

#### Quality Gate
- [ ] pytest 설정 완료 및 실행 가능
- [ ] 기존 코드가 모든 테스트 통과
- [ ] 커버리지 리포트 생성 가능
- [ ] CI 파이프라인에서 테스트 실행 가능

```bash
# Validation Commands
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

#### Critical Files
- `tests/conftest.py` (신규)
- `pytest.ini` (신규)
- `conversation/session_manager.py` (기존, 테스트 대상)
- `agents/base_agent.py` (기존, 테스트 대상)
- `agents/orchestrator.py` (기존, 테스트 대상)

---

### Phase 2: 의존성 주입 패턴 적용
**Goal**: LLMClient와 SessionManager에 DI 패턴 적용하여 테스트 가능한 구조로 변경
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 2.1**: Protocol 기반 인터페이스 테스트 작성
  - File: `tests/unit/utils/test_llm_protocols.py`
  - LLMClientProtocol, SessionManagerProtocol 정의 테스트

- [ ] **Test 2.2**: DI 적용된 BaseAgent 테스트
  - File: `tests/unit/agents/test_base_agent_di.py`
  - 외부에서 LLMClient 주입 가능 여부 테스트

**GREEN: Implement to Make Tests Pass**
- [ ] **Task 2.3**: Protocol 인터페이스 정의
  - File: `utils/protocols.py` (신규)
  - LLMClientProtocol, SessionManagerProtocol 정의

- [ ] **Task 2.4**: BaseAgent 생성자에 LLMClient 주입 가능하도록 수정
  - File: `agents/base_agent.py`
  - 변경: `__init__(self, ..., llm_client: Optional[LLMClientProtocol] = None)`

- [ ] **Task 2.5**: API 라우트에 FastAPI Depends로 SessionManager 주입
  - Files: `api/routes/chat.py`, `api/routes/analysis.py`
  - 전역 변수 → Depends() 패턴

- [ ] **Task 2.6**: SessionManager 싱글톤 또는 팩토리 패턴 적용
  - File: `conversation/session_manager.py`
  - 앱 전체에서 단일 인스턴스 공유

**REFACTOR: Clean Up Code**
- [ ] **Task 2.7**: 기존 테스트 업데이트
  - Mock 객체 주입 방식으로 변경
  - 불필요한 의존성 제거

#### Quality Gate
- [ ] LLMClient 없이 BaseAgent 테스트 가능
- [ ] SessionManager mock 주입으로 API 테스트 가능
- [ ] 모든 기존 테스트 통과
- [ ] 기존 기능 수동 테스트 통과

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

#### Critical Files
- `utils/protocols.py` (신규)
- `agents/base_agent.py` (수정)
- `agents/orchestrator.py` (수정)
- `api/routes/chat.py` (수정)
- `api/routes/analysis.py` (수정)
- `api/server.py` (수정)
- `conversation/session_manager.py` (수정)

---

### Phase 3: 에이전트 팩토리 패턴 도입
**Goal**: 8개 에이전트 클래스를 1개 팩토리 + 설정 기반으로 통합
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 3.1**: AgentFactory 테스트 작성
  - File: `tests/unit/agents/test_agent_factory.py`
  - Test cases:
    - 설정으로 에이전트 생성
    - 모든 기존 에이전트 타입 지원
    - 잘못된 타입 에러 처리

- [ ] **Test 3.2**: 에이전트 설정 스키마 테스트
  - File: `tests/unit/agents/test_agent_config.py`
  - AgentConfig 데이터 클래스 검증

**GREEN: Implement to Make Tests Pass**
- [ ] **Task 3.3**: AgentConfig 데이터 클래스 정의
  - File: `agents/config.py` (신규)
  ```python
  @dataclass
  class AgentConfig:
      name: str
      display_name: str
      system_prompt: str
      interpretation_focus: str
      keywords: List[str]
  ```

- [ ] **Task 3.4**: AGENT_CONFIGS 설정 파일 생성
  - File: `agents/agent_configs.py` (신규)
  - 8개 에이전트 설정을 딕셔너리로 정의

- [ ] **Task 3.5**: AgentFactory 클래스 구현
  - File: `agents/factory.py` (신규)
  ```python
  class AgentFactory:
      def create(self, agent_type: str, llm_client: LLMClientProtocol) -> BaseAgent
      def get_all_types(self) -> List[str]
  ```

- [ ] **Task 3.6**: Orchestrator 수정
  - File: `agents/orchestrator.py`
  - 하드코딩된 클래스 참조 → AgentFactory 사용
  - KEYWORD_MAPPING → AgentConfig에서 읽기

**REFACTOR: Clean Up Code**
- [ ] **Task 3.7**: 개별 에이전트 파일 제거 또는 deprecated 표시
  - Files: `agents/interpreters/*.py`
  - 기존 파일은 호환성을 위해 유지하되 내부적으로 Factory 사용

- [ ] **Task 3.8**: 테스트 업데이트
  - Factory 기반 테스트로 전환

#### Quality Gate
- [ ] AgentFactory로 모든 에이전트 타입 생성 가능
- [ ] 새 에이전트 추가가 설정만으로 가능
- [ ] Orchestrator가 Factory 사용
- [ ] 기존 API 동작 변화 없음

```bash
pytest tests/unit/agents/ -v
pytest tests/integration/ -v
```

#### Critical Files
- `agents/config.py` (신규)
- `agents/agent_configs.py` (신규)
- `agents/factory.py` (신규)
- `agents/orchestrator.py` (수정)
- `agents/interpreters/*.py` (검토/수정)

---

### Phase 4: API 라우트 중복 제거
**Goal**: 메시지 생성 함수, 세션 처리 로직, 데이터 변환 함수 통합
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 4.1**: MessageFormatter 테스트 작성
  - File: `tests/unit/api/test_message_formatter.py`
  - 각 분석 타입별 메시지 포맷팅 테스트

- [ ] **Test 4.2**: SessionDependency 테스트 작성
  - File: `tests/unit/api/test_session_dependency.py`
  - 세션 조회/생성 로직 테스트

**GREEN: Implement to Make Tests Pass**
- [ ] **Task 4.3**: MessageFormatter 클래스 추출
  - File: `api/formatters.py` (신규)
  - 전략 패턴으로 각 분석 타입별 포맷터 구현
  ```python
  class MessageFormatter:
      def format_fortune(self, result: Dict) -> str
      def format_yongsin(self, result: Dict) -> str
      def format_school_comparison(self, result: Dict) -> str
  ```

- [ ] **Task 4.4**: SessionDependency 추출
  - File: `api/dependencies.py` (신규)
  - FastAPI Depends로 세션 처리 로직 통합
  ```python
  async def get_or_create_session(
      request: Union[ChatRequest, AnalysisRequest],
      session_manager: SessionManager = Depends(get_session_manager)
  ) -> Session
  ```

- [ ] **Task 4.5**: DataConverter 클래스 추출
  - File: `api/converters.py` (신규)
  - 데이터 형식 변환 로직 통합

- [ ] **Task 4.6**: API 라우트 리팩토링
  - Files: `api/routes/chat.py`, `api/routes/analysis.py`
  - 추출된 클래스 사용하도록 수정

**REFACTOR: Clean Up Code**
- [ ] **Task 4.7**: 중복 코드 제거 확인
  - 동일 로직이 여러 곳에 없는지 확인
- [ ] **Task 4.8**: API 엔드포인트 통합 테스트
  - File: `tests/integration/api/test_endpoints.py`

#### Quality Gate
- [ ] API 라우트 파일 코드량 50% 감소
- [ ] 중복 함수 제거 완료
- [ ] 모든 API 엔드포인트 정상 동작
- [ ] 통합 테스트 통과

```bash
pytest tests/integration/api/ -v
# Manual test: 각 API 엔드포인트 curl 테스트
```

#### Critical Files
- `api/formatters.py` (신규)
- `api/dependencies.py` (신규)
- `api/converters.py` (신규)
- `api/routes/chat.py` (수정)
- `api/routes/analysis.py` (수정)
- `api/routes/manseol.py` (수정)

---

### Phase 5: 설정 통합 및 로깅 개선
**Goal**: 분산된 설정값 중앙 집중화, debug print 제거, logging 모듈 도입
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 5.1**: 통합 설정 테스트
  - File: `tests/unit/config/test_settings.py`
  - 모든 설정값이 Settings 클래스에서 관리되는지 확인

**GREEN: Implement to Make Tests Pass**
- [ ] **Task 5.2**: Settings 클래스 확장
  - File: `config/settings.py`
  - 하드코딩된 값들을 설정으로 이동:
    - `CONVERSATION_HISTORY_LIMIT: int = 10`
    - `SESSION_CLEANUP_PERCENTAGE: float = 0.2`
    - `DEFAULT_REASONING_EFFORT: str = "medium"`

- [ ] **Task 5.3**: 로깅 설정 추가
  - File: `config/logging_config.py` (신규)
  - structlog 또는 표준 logging 설정

- [ ] **Task 5.4**: debug print 문 제거 및 logging 적용
  - Files:
    - `agents/base_agent.py` (라인 122, 138)
    - `agents/interpreters/synthesis_agent.py` (라인 98, 114)
    - `utils/llm_client.py` (라인 117-119, 147-148)
  - `print()` → `logger.debug()`

- [ ] **Task 5.5**: 하드코딩된 값들을 설정 참조로 변경
  - Files: `agents/base_agent.py`, `conversation/session_manager.py`

**REFACTOR: Clean Up Code**
- [ ] **Task 5.6**: 설정 사용처 일관성 확인
  - 모든 설정이 Settings 클래스를 통해 접근되는지 확인

#### Quality Gate
- [ ] 모든 print 문 제거 완료
- [ ] 로깅 레벨별 출력 확인
- [ ] 설정 파일 하나로 모든 값 관리
- [ ] 환경별 설정 오버라이드 가능

```bash
grep -r "print(" --include="*.py" agents/ api/ utils/ conversation/
# 결과가 없어야 함 (또는 의도적인 출력만)
```

#### Critical Files
- `config/settings.py` (수정)
- `config/logging_config.py` (신규)
- `agents/base_agent.py` (수정)
- `agents/interpreters/synthesis_agent.py` (수정)
- `utils/llm_client.py` (수정)
- `conversation/session_manager.py` (수정)

---

### Phase 6: 타입 안전성 및 최종 정리
**Goal**: 타입 힌팅 강화, 불필요 코드 정리, 문서화
**Status**: Pending

#### Tasks

**RED: Write Failing Tests First**
- [ ] **Test 6.1**: mypy 타입 체크 통과
  - `mypy agents/ api/ utils/ conversation/ config/`

**GREEN: Implement to Make Tests Pass**
- [ ] **Task 6.2**: 타입 힌팅 강화
  - Files:
    - `agents/orchestrator.py` (Any → 구체적 타입)
    - `api/routes/analysis.py` (Dict[str, Any] → TypedDict)
  - 반환 타입, 파라미터 타입 명시

- [ ] **Task 6.3**: TypedDict 또는 Pydantic 모델로 Dict 대체
  - Files: `api/schemas.py` 확장
  - 주요 데이터 구조에 대한 타입 정의

- [ ] **Task 6.4**: 사용되지 않는 코드 제거
  - deprecated 함수/클래스 제거
  - 불필요한 import 제거

- [ ] **Task 6.5**: 최종 문서화
  - `README.md` 업데이트
  - 모듈별 docstring 추가

**REFACTOR: Final Cleanup**
- [ ] **Task 6.6**: 전체 코드 포맷팅
  - `black .`
  - `isort .`
  - `ruff check --fix .`

- [ ] **Task 6.7**: 최종 테스트 및 커버리지 확인
  - 목표: 80% 이상 커버리지

#### Quality Gate
- [ ] mypy 타입 체크 통과
- [ ] 테스트 커버리지 80% 이상
- [ ] 모든 linting 통과
- [ ] README 업데이트 완료

```bash
mypy agents/ api/ utils/ conversation/ config/ --ignore-missing-imports
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=80
black --check .
ruff check .
```

#### Critical Files
- `agents/orchestrator.py` (수정)
- `api/schemas.py` (수정)
- `api/routes/analysis.py` (수정)
- `README.md` (수정)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| 리팩토링 중 기존 기능 손상 | Medium | High | 테스트 인프라 먼저 구축, 단계별 검증 |
| LLM API 변경으로 테스트 실패 | Low | Medium | Mock 객체로 API 격리 |
| 성능 저하 | Low | Medium | 각 Phase 후 성능 벤치마크 |
| 팩토리 패턴 복잡도 증가 | Medium | Low | 명확한 문서화, 예제 코드 제공 |

---

## Rollback Strategy

### If Phase 1 Fails
- 테스트 파일 삭제, pytest 설정 제거
- 기존 코드 영향 없음

### If Phase 2 Fails
- Protocol 파일 삭제
- 생성자 변경 원복
- git revert 사용

### If Phase 3 Fails
- Factory 파일 삭제
- Orchestrator의 직접 import 복원
- 개별 에이전트 파일 유지

### If Phase 4-6 Fails
- 해당 Phase의 git commit을 revert
- 이전 Phase 상태로 복원

---

## Progress Tracking

### Completion Status
- **Phase 1**: 0%
- **Phase 2**: 0%
- **Phase 3**: 0%
- **Phase 4**: 0%
- **Phase 5**: 0%
- **Phase 6**: 0%

**Overall Progress**: 0% complete

---

## Notes & Learnings

### Implementation Notes
- (구현 중 발견사항 기록)

### Blockers Encountered
- (차단 요소 기록)

### Improvements for Future Plans
- (향후 개선사항 기록)

---

## Next Steps

1. 이 계획 문서 검토 후 `/interviewer`로 심층 인터뷰 진행
2. 인터뷰 결과를 `REFINED_fortune-teller-refactoring.md`로 문서화
3. Phase 1부터 순차적으로 구현 시작

---

**Plan Status**: Ready for Review
**Next Action**: `/interviewer`로 심층 인터뷰 진행
**Blocked By**: None
