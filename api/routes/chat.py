"""
채팅 API 라우트
사주 해석 대화 엔드포인트
"""

import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Optional, List, AsyncGenerator

from api.schemas import (
    ChatRequest, ChatResponse,
    SessionListResponse, SessionDetailResponse,
    ErrorResponse, InterpretationType
)
from conversation.session_manager import SessionManager
from agents.orchestrator import Orchestrator
from utils.llm_client import get_llm_client


router = APIRouter(prefix="/api/chat", tags=["chat"])

# 전역 세션 매니저 (실제 환경에서는 의존성 주입 사용)
session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """세션 매니저 의존성"""
    return session_manager


def get_orchestrator(provider: str = "openai") -> Orchestrator:
    """오케스트레이터 의존성"""
    return Orchestrator(llm_provider=provider)


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="대화 요청",
    description="사주 해석 대화를 수행합니다."
)
async def chat(
    request: ChatRequest,
    sm: SessionManager = Depends(get_session_manager)
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
            session = sm.get_session(request.session_id)
            if not session:
                raise HTTPException(
                    status_code=404,
                    detail=f"세션 '{request.session_id}'을 찾을 수 없습니다."
                )
        else:
            # 새 세션 생성
            if not request.saju_data:
                raise HTTPException(
                    status_code=400,
                    detail="새 세션 생성시 saju_data가 필요합니다."
                )
            session = sm.create_session(request.saju_data)

        # 사용자 메시지 기록
        session.add_user_message(request.message)

        # 오케스트레이터 생성
        orchestrator = get_orchestrator(request.llm_provider.value)

        # 대화 이력 가져오기
        history = session.get_messages_for_llm(limit=10)

        # 해석 유형에 따른 처리
        suggested_questions: List[str] = []

        if request.interpretation_type == InterpretationType.QUICK:
            # 빠른 단일 해석
            focus = request.focus or "personality"
            response = await orchestrator.quick_interpret(
                saju_data=session.saju_data,
                focus=focus
            )
            result_message = response.interpretation
            suggested_questions = response.suggested_questions or []
            agents_used = [response.agent_name]
            interpretations = {response.agent_name: response.to_dict()}

        elif request.interpretation_type == InterpretationType.SPECIFIC:
            # 특정 분야 해석
            if not request.focus:
                raise HTTPException(
                    status_code=400,
                    detail="specific 해석 유형에는 focus 파라미터가 필요합니다."
                )
            response = await orchestrator.quick_interpret(
                saju_data=session.saju_data,
                focus=request.focus
            )
            result_message = response.interpretation
            suggested_questions = response.suggested_questions or []
            agents_used = [response.agent_name]
            interpretations = {response.agent_name: response.to_dict()}

        else:
            # 전체 해석 (기본)
            result = await orchestrator.route_and_interpret(
                saju_data=session.saju_data,
                question=request.message,
                conversation_history=history,
                include_synthesis=True
            )

            # 응답 메시지 구성 및 suggested_questions 추출
            if result.get("synthesis"):
                result_message = result["synthesis"]["interpretation"]
                suggested_questions = result["synthesis"].get("suggested_questions", [])
            else:
                # synthesis가 없으면 첫 번째 해석 사용
                first_interp = list(result["interpretations"].values())[0]
                result_message = first_interp.get("interpretation", "해석을 생성할 수 없습니다.")
                suggested_questions = first_interp.get("suggested_questions", [])

            agents_used = result.get("agents_used", [])
            interpretations = result.get("interpretations")

            # 해석 결과 캐시
            for agent_name, interp in interpretations.items():
                session.cache_interpretation(agent_name, interp)

        # 어시스턴트 메시지 기록
        session.add_assistant_message(result_message)

        return ChatResponse(
            success=True,
            session_id=session.session_id,
            message=result_message,
            suggested_questions=suggested_questions,
            interpretations=interpretations,
            agents_used=agents_used
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 처리 중 오류: {str(e)}")


@router.get(
    "/sessions",
    response_model=SessionListResponse,
    summary="세션 목록",
    description="활성 세션 목록을 반환합니다."
)
async def list_sessions(
    sm: SessionManager = Depends(get_session_manager)
) -> SessionListResponse:
    """세션 목록 조회"""
    sessions = sm.list_sessions()

    return SessionListResponse(
        success=True,
        sessions=sessions,
        total=len(sessions)
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionDetailResponse,
    summary="세션 상세",
    description="특정 세션의 상세 정보를 반환합니다."
)
async def get_session(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
) -> SessionDetailResponse:
    """세션 상세 조회"""
    session_data = sm.export_session(session_id)

    if not session_data:
        raise HTTPException(
            status_code=404,
            detail=f"세션 '{session_id}'을 찾을 수 없습니다."
        )

    return SessionDetailResponse(
        success=True,
        session=session_data
    )


@router.delete(
    "/sessions/{session_id}",
    summary="세션 삭제",
    description="특정 세션을 삭제합니다."
)
async def delete_session(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
):
    """세션 삭제"""
    success = sm.delete_session(session_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"세션 '{session_id}'을 찾을 수 없습니다."
        )

    return {"success": True, "message": "세션이 삭제되었습니다."}


@router.post(
    "/sessions/{session_id}/clear",
    summary="대화 기록 초기화",
    description="세션의 대화 기록을 초기화합니다."
)
async def clear_session_history(
    session_id: str,
    sm: SessionManager = Depends(get_session_manager)
):
    """세션 대화 기록 초기화"""
    session = sm.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"세션 '{session_id}'을 찾을 수 없습니다."
        )

    session.messages.clear()
    session.interpretation_cache.clear()

    return {"success": True, "message": "대화 기록이 초기화되었습니다."}


def _generate_suggested_questions(user_question: str, ai_response: str) -> List[str]:
    """
    사용자 질문과 AI 응답을 기반으로 후속 질문을 생성합니다.
    """
    # 응답 내용에서 주제 추출 (첫 50자 내외)
    topic_hint = ai_response[:50].replace('\n', ' ').strip()
    if len(topic_hint) > 30:
        topic_hint = topic_hint[:30] + "..."

    # 기본 추천 질문 템플릿
    questions = [
        "이 내용에 대해 더 자세히 설명해주세요.",
        "다른 관점에서도 분석해주실 수 있나요?",
        "실생활에서 어떻게 활용할 수 있을까요?",
    ]

    # 사용자 질문에 따라 맞춤형 질문 추가
    if "성격" in user_question or "기질" in user_question:
        questions = [
            "제 성격의 장점을 극대화하려면 어떻게 해야 할까요?",
            "대인관계에서 주의할 점은 무엇인가요?",
            "성격적으로 맞는 직업은 무엇인가요?",
        ]
    elif "직업" in user_question or "재물" in user_question or "사업" in user_question:
        questions = [
            "올해 재물운은 어떤가요?",
            "사업을 시작하기 좋은 시기는 언제인가요?",
            "투자에 유리한 방향은 무엇인가요?",
        ]
    elif "연애" in user_question or "결혼" in user_question or "인연" in user_question:
        questions = [
            "좋은 인연을 만나는 시기는 언제인가요?",
            "어떤 스타일의 사람과 잘 맞나요?",
            "연애운을 높이려면 어떻게 해야 할까요?",
        ]
    elif "건강" in user_question or "체질" in user_question:
        questions = [
            "건강을 위해 특별히 주의해야 할 점은요?",
            "저에게 맞는 운동이나 식이요법이 있나요?",
            "건강운이 좋아지는 시기는 언제인가요?",
        ]
    elif "운세" in user_question or "올해" in user_question or "내년" in user_question:
        questions = [
            "이번 달 특별히 주의할 점은 무엇인가요?",
            "행운을 높이기 위한 방법이 있을까요?",
            "중요한 결정을 하기 좋은 시기는 언제인가요?",
        ]
    elif "용신" in user_question or "기신" in user_question:
        questions = [
            "용신을 강화하는 방법은 무엇인가요?",
            "일상에서 용신을 활용하는 법을 알려주세요.",
            "기신을 피하는 방법이 있나요?",
        ]

    return questions[:3]


@router.post(
    "/stream",
    summary="스트리밍 대화 (Reasoning 포함)",
    description="AI 사고 과정(reasoning)과 응답을 실시간 스트리밍합니다."
)
async def chat_stream(
    request: ChatRequest,
    sm: SessionManager = Depends(get_session_manager)
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
                session = sm.get_session(request.session_id)
                if not session:
                    yield f"data: {json.dumps({'type': 'error', 'content': '세션을 찾을 수 없습니다.'})}\n\n"
                    return
            else:
                if not request.saju_data:
                    yield f"data: {json.dumps({'type': 'error', 'content': '새 세션 생성시 saju_data가 필요합니다.'})}\n\n"
                    return
                session = sm.create_session(request.saju_data)

            # 세션 ID 먼저 전송
            yield f"data: {json.dumps({'type': 'session', 'content': session.session_id})}\n\n"

            # 사주 컨텍스트 구성 (프론트엔드 데이터 구조에 맞춤)
            saju = session.saju_data

            # 생년월일 정보
            birth_info = saju.get('birth_info', {})
            birth_date = birth_info.get('birth_date', '')
            birth_time = birth_info.get('birth_time', '')
            gender = birth_info.get('gender', '')
            name = birth_info.get('name', '미상')

            # 사주팔자
            four_pillars = saju.get('four_pillars', {})

            # 오행 분석
            five_elements = saju.get('five_elements', {})

            # 십성
            ten_gods = saju.get('ten_gods', {})

            # 신강/신약
            strength = saju.get('strength', {})

            # 운세 흐름
            fortune_cycles = saju.get('fortune_cycles', {})
            current_daewun = fortune_cycles.get('current_daewun', {})
            yearly = fortune_cycles.get('yearly', {})
            monthly = fortune_cycles.get('monthly', {})
            daily = fortune_cycles.get('daily', {})

            saju_context = f"""
## 사주 정보
- 이름: {name}
- 생년월일: {birth_date} {birth_time}
- 성별: {gender}

## 사주팔자 (四柱八字)
{json.dumps(four_pillars, ensure_ascii=False, indent=2) if four_pillars else '정보 없음'}

## 오행 분석 (五行)
{json.dumps(five_elements, ensure_ascii=False, indent=2) if five_elements else '정보 없음'}

## 십성 (十星)
{json.dumps(ten_gods, ensure_ascii=False, indent=2) if ten_gods else '정보 없음'}

## 신강/신약 분석
{json.dumps(strength, ensure_ascii=False, indent=2) if strength else '정보 없음'}

## 현재 운세 흐름
- 현재 대운: {json.dumps(current_daewun, ensure_ascii=False) if current_daewun else '정보 없음'}
- 연운 ({yearly.get('year', '')}년): {yearly.get('stem', '')}{yearly.get('branch', '')} - {yearly.get('ten_god', '')}
- 월운 ({monthly.get('month', '')}월): {monthly.get('stem', '')}{monthly.get('branch', '')} - {monthly.get('ten_god', '')}
- 일운: {daily.get('stem', '')}{daily.get('branch', '')} - {daily.get('ten_god', '')}
"""

            # 시스템 프롬프트
            system_prompt = f"""당신은 전문 사주명리학 상담사입니다.
사용자의 사주팔자를 바탕으로 정확하고 통찰력 있는 해석을 제공합니다.

{saju_context}

위 사주 정보를 바탕으로 사용자의 질문에 친절하고 상세하게 답변해주세요.
한국어로 답변하며, 전문적이면서도 이해하기 쉽게 설명해주세요.
사주 분석 시 오행의 균형, 십성의 배치, 현재 운세 흐름을 종합적으로 고려하세요."""

            # 대화 이력
            history = session.get_messages_for_llm(limit=10)
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": request.message})

            # LLM 클라이언트로 스트리밍
            llm = get_llm_client(provider=request.llm_provider.value)

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

                # 추천 질문 생성 및 전송
                suggested_questions = _generate_suggested_questions(request.message, full_output)
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
        }
    )
