"""
채팅 API 라우트
사주 해석 대화 엔드포인트
"""

import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from agents.agent_configs import AGENT_CONFIGS, get_agent_config
from agents.nodes import route_question
from api.dependencies import get_orchestrator, get_session_manager
from api.formatters import SuggestedQuestionsGenerator
from api.schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    SessionDetailResponse,
    SessionListResponse,
)
from config.settings import get_allowed_models, settings
from manseol.calculator.current_fortune import calculate_current_fortune
from manseol.data.stems_branches import StemBranchData
from utils.llm_client import get_llm_client
from utils.protocols import SessionManagerProtocol

router = APIRouter(prefix="/api/chat", tags=["chat"])


def _resolve_model(model_value: str | None) -> str | None:
    """요청 모델을 화이트리스트로 검증. None이면 서버 기본값 사용."""
    if model_value is None:
        return None
    if model_value not in get_allowed_models():
        raise HTTPException(status_code=400, detail=f"허용되지 않은 모델: {model_value}")
    return model_value


def _build_current_fortune_from_saju(saju: dict) -> dict | None:
    """세션 saju_data(display 형식)의 일간으로 현재 연운·월운·일운을 서버 재계산.

    세션 저장값은 생성 시점 스냅샷이라 일운이 낡는다. 저장된
    four_pillars.day.heavenly_stem.korean(한글 천간 1글자)에서 일간 인덱스를
    복원해 매 메시지 시점(KST) 기준으로 다시 계산한다. 구조 불일치·미등록
    천간 등 복원 실패 시 None을 반환해 호출부가 저장값으로 폴백하도록 한다.
    """
    four_pillars = saju.get("four_pillars", {})
    day_pillar = four_pillars.get("day", {}) if isinstance(four_pillars, dict) else {}
    stem = day_pillar.get("heavenly_stem", {}) if isinstance(day_pillar, dict) else {}
    korean = stem.get("korean") if isinstance(stem, dict) else None
    if not korean:
        return None

    day_stem_index = StemBranchData.stem_index_by_korean(korean)
    if day_stem_index is None:
        return None

    return calculate_current_fortune(day_stem_index)


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="대화 요청",
    description="사주 해석 대화를 수행합니다.",
)
async def chat(
    request: ChatRequest, sm: SessionManagerProtocol = Depends(get_session_manager)
) -> ChatResponse:
    """
    대화 엔드포인트

    - 새 세션 생성 또는 기존 세션 사용
    - 질문에 따라 적절한 에이전트 선택
    - Multi-turn 대화 지원
    """
    try:
        # 세션 처리
        if request.session_id:
            # 기존 세션 사용
            session = await sm.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404, detail=f"세션 '{request.session_id}'을 찾을 수 없습니다."
                )
        else:
            # 새 세션 생성
            if not request.saju_data:
                raise HTTPException(
                    status_code=400, detail="새 세션 생성시 saju_data가 필요합니다."
                )
            session = await sm.create_session(request.saju_data)

        # 사용자 메시지 기록
        session.add_user_message(request.message)

        # 모델 검증 후 오케스트레이터 생성
        model = _resolve_model(request.model.value if request.model else None)
        orchestrator = get_orchestrator(model=model)

        # 대화 이력 가져오기
        history = session.get_messages_for_llm(limit=10)

        # 전체 해석 (Supervisor 패턴 동적 라우팅)
        suggested_questions: list[str] = []
        result = await orchestrator.route_and_interpret(
            saju_data=session.saju_data,
            question=request.message,
            conversation_history=history,
            include_synthesis=True,
        )

        # 응답 메시지 구성 및 suggested_questions 추출
        if result.get("synthesis"):
            result_message = result["synthesis"]["interpretation"]
            suggested_questions = result["synthesis"].get("suggested_questions", [])
        elif result.get("interpretations"):
            first_interp = list(result["interpretations"].values())[0]
            result_message = first_interp.get("interpretation", "해석을 생성할 수 없습니다.")
            suggested_questions = first_interp.get("suggested_questions", [])
        else:
            result_message = "해석을 생성할 수 없습니다. 다시 시도해 주세요."

        agents_used = result.get("agents_used", [])
        interpretations = result.get("interpretations") or {}

        # 해석 결과 캐시
        for agent_name, interp in interpretations.items():
            session.cache_interpretation(agent_name, interp)

        # 어시스턴트 메시지 기록
        session.add_assistant_message(result_message)

        # 변형된 세션 영속 (명시적 flush)
        await sm.save_session(session)

        return ChatResponse(
            success=True,
            session_id=session.session_id,
            message=result_message,
            suggested_questions=suggested_questions,
            interpretations=interpretations,
            agents_used=agents_used,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 처리 중 오류: {str(e)}")


@router.get(
    "/sessions",
    response_model=SessionListResponse,
    summary="세션 목록",
    description="활성 세션 목록을 반환합니다.",
)
async def list_sessions(
    sm: SessionManagerProtocol = Depends(get_session_manager),
) -> SessionListResponse:
    """세션 목록 조회"""
    sessions = await sm.list_sessions()

    return SessionListResponse(success=True, sessions=sessions, total=len(sessions))


@router.get(
    "/sessions/{session_id}",
    response_model=SessionDetailResponse,
    summary="세션 상세",
    description="특정 세션의 상세 정보를 반환합니다.",
)
async def get_session(
    session_id: str, sm: SessionManagerProtocol = Depends(get_session_manager)
) -> SessionDetailResponse:
    """세션 상세 조회"""
    session_data = await sm.export_session(session_id)

    if not session_data:
        raise HTTPException(status_code=404, detail=f"세션 '{session_id}'을 찾을 수 없습니다.")

    return SessionDetailResponse(success=True, session=session_data)


@router.delete("/sessions/{session_id}", summary="세션 삭제", description="특정 세션을 삭제합니다.")
async def delete_session(
    session_id: str, sm: SessionManagerProtocol = Depends(get_session_manager)
):
    """세션 삭제"""
    success = await sm.delete_session(session_id)

    if not success:
        raise HTTPException(status_code=404, detail=f"세션 '{session_id}'을 찾을 수 없습니다.")

    return {"success": True, "message": "세션이 삭제되었습니다."}


@router.post(
    "/sessions/{session_id}/clear",
    summary="대화 기록 초기화",
    description="세션의 대화 기록을 초기화합니다.",
)
async def clear_session_history(
    session_id: str, sm: SessionManagerProtocol = Depends(get_session_manager)
):
    """세션 대화 기록 초기화"""
    session = await sm.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail=f"세션 '{session_id}'을 찾을 수 없습니다.")

    session.messages.clear()
    session.interpretation_cache.clear()

    # 초기화된 상태 영속 (명시적 flush)
    await sm.save_session(session)

    return {"success": True, "message": "대화 기록이 초기화되었습니다."}


@router.post(
    "/stream",
    summary="스트리밍 대화 (Reasoning 포함)",
    description="AI 사고 과정(reasoning)과 응답을 실시간 스트리밍합니다.",
)
async def chat_stream(
    request: ChatRequest, sm: SessionManagerProtocol = Depends(get_session_manager)
):
    """
    스트리밍 대화 엔드포인트 (Server-Sent Events)

    - reasoning: AI 사고 과정 스트리밍
    - output: 최종 응답 스트리밍
    - reasoning_done: reasoning 완료 신호
    - done: 전체 완료 신호
    """

    async def generate() -> AsyncGenerator[str, None]:
        try:
            # 세션 처리
            if request.session_id:
                session = await sm.get_session(request.session_id)
                if not session:
                    yield f"data: {json.dumps({'type': 'error', 'content': '세션을 찾을 수 없습니다.'})}\n\n"
                    return
            else:
                if not request.saju_data:
                    yield f"data: {json.dumps({'type': 'error', 'content': '새 세션 생성시 saju_data가 필요합니다.'})}\n\n"
                    return
                session = await sm.create_session(request.saju_data)

            # 세션 ID 먼저 전송
            yield f"data: {json.dumps({'type': 'session', 'content': session.session_id})}\n\n"

            # 사주 컨텍스트 구성 (프론트엔드 데이터 구조에 맞춤)
            saju = session.saju_data

            # 생년월일 정보
            birth_info = saju.get("birth_info", {})
            birth_date = birth_info.get("birth_date", "")
            birth_time = birth_info.get("birth_time", "")
            gender = birth_info.get("gender", "")
            name = birth_info.get("name", "미상")

            # 사주팔자
            four_pillars = saju.get("four_pillars", {})

            # 오행 분석
            five_elements = saju.get("five_elements", {})

            # 십성
            ten_gods = saju.get("ten_gods", {})

            # 신강/신약
            strength = saju.get("strength", {})

            # 운세 흐름
            fortune_cycles = saju.get("fortune_cycles", {})
            current_daewun = fortune_cycles.get("current_daewun", {})
            yearly = fortune_cycles.get("yearly", {})
            monthly = fortune_cycles.get("monthly", {})
            daily = fortune_cycles.get("daily", {})

            # 서버 단일 진실 공급원: 저장 스냅샷(프론트 근사)을 매 메시지 시점
            # 서버 재계산으로 대체한다. 복원 실패 시에만 저장값 폴백(구 세션 호환).
            # 대운(current_daewun)은 출생 기준 고정값이라 저장값을 그대로 쓴다.
            server_fortune = _build_current_fortune_from_saju(saju)
            monthly_label = ""
            if server_fortune is not None:
                yearly = server_fortune["yearly"]
                monthly = server_fortune["monthly"]
                daily = server_fortune["daily"]
                monthly_label = ", 절기월"

            saju_context = f"""
## 사주 정보
- 이름: {name}
- 생년월일: {birth_date} {birth_time}
- 성별: {gender}

## 사주팔자 (四柱八字)
{json.dumps(four_pillars, ensure_ascii=False, indent=2) if four_pillars else "정보 없음"}

## 오행 분석 (五行)
{json.dumps(five_elements, ensure_ascii=False, indent=2) if five_elements else "정보 없음"}

## 십성 (十星)
{json.dumps(ten_gods, ensure_ascii=False, indent=2) if ten_gods else "정보 없음"}

## 신강/신약 분석
{json.dumps(strength, ensure_ascii=False, indent=2) if strength else "정보 없음"}

## 현재 운세 흐름
- 현재 대운: {json.dumps(current_daewun, ensure_ascii=False) if current_daewun else "정보 없음"}
- 연운 ({yearly.get("year", "")}년): {yearly.get("stem", "")}{yearly.get("branch", "")} - {yearly.get("ten_god", "")}
- 월운 ({monthly.get("month", "")}월{monthly_label}): {monthly.get("stem", "")}{monthly.get("branch", "")} - {monthly.get("ten_god", "")}
- 일운: {daily.get("stem", "")}{daily.get("branch", "")} - {daily.get("ten_god", "")}
"""

            # 에이전트 선택: focus 명시 시 해당 전문 에이전트, 아니면 경량 라우팅
            focus = request.focus
            agent_name = (
                focus if (focus and focus in AGENT_CONFIGS and focus != "synthesis") else None
            )
            user_selected = agent_name is not None
            if agent_name is None:
                agent_name = await route_question(
                    request.message, model=settings.OPENROUTER_ROUTING_MODEL
                )

            agent_config = get_agent_config(agent_name)
            if agent_config:
                base_prompt = agent_config.system_prompt
                display_name = agent_config.display_name
            else:
                agent_name = "general"
                base_prompt = (
                    "당신은 전문 사주명리학 상담사입니다.\n"
                    "사용자의 사주팔자를 바탕으로 정확하고 통찰력 있는 해석을 제공합니다."
                )
                display_name = "종합 상담"

            # 신뢰도: 사용자가 직접 선택하면 높음, 자동 라우팅이면 보통 상향
            confidence = 0.9 if user_selected else 0.8

            # 선택된 에이전트 정보 전송 (출처·신뢰도 배지용)
            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "agent_selected",
                        "agent": agent_name,
                        "display_name": display_name,
                        "confidence": confidence,
                    },
                    ensure_ascii=False,
                )
                + "\n\n"
            )

            # 시스템 프롬프트 (에이전트별 전문 프롬프트 + 사주 컨텍스트)
            system_prompt = f"""{base_prompt}

아래는 상담 대상자의 사주 정보입니다. 이 정보에 근거하여 답변하세요.
{saju_context}

한국어로 답변하며, 전문적이면서도 이해하기 쉽게 설명해주세요."""

            # 대화 이력
            history = session.get_messages_for_llm(limit=10)
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": request.message})

            # LLM 클라이언트로 스트리밍 (모델 검증)
            model = _resolve_model(request.model.value if request.model else None)
            llm = get_llm_client(model=model)

            full_output = ""
            async for chunk in llm.chat_stream_with_reasoning(messages):
                chunk_type = chunk.get("type", "output")
                content = chunk.get("content", "")

                if chunk_type == "output" and content:
                    full_output += content

                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

            # 완료 후 메시지 기록
            if full_output:
                session.add_user_message(request.message)
                session.add_assistant_message(full_output)

                # 변형된 세션 영속 (명시적 flush)
                await sm.save_session(session)

                # 추천 질문 생성 및 전송
                suggested_questions = SuggestedQuestionsGenerator.from_context(
                    request.message, full_output
                )
                yield f"data: {json.dumps({'type': 'suggested_questions', 'content': suggested_questions}, ensure_ascii=False)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
