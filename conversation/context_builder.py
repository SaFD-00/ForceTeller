"""
컨텍스트 빌더 모듈
LLM 호출을 위한 컨텍스트 구성
"""

from typing import Dict, List, Optional, Any

from conversation.session_manager import Session
from agents.prompts.system_prompts import format_saju_context


class ContextBuilder:
    """LLM 컨텍스트 빌더"""

    def __init__(
        self,
        max_history_messages: int = 10,
        include_saju_summary: bool = True,
        include_cached_interpretations: bool = True
    ):
        """
        Args:
            max_history_messages: 포함할 최대 대화 이력 수
            include_saju_summary: 사주 요약 포함 여부
            include_cached_interpretations: 캐시된 해석 포함 여부
        """
        self.max_history_messages = max_history_messages
        self.include_saju_summary = include_saju_summary
        self.include_cached_interpretations = include_cached_interpretations

    def build_context(
        self,
        session: Session,
        current_question: str,
        system_prompt: str,
        additional_context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        LLM 호출용 전체 컨텍스트 구성

        Args:
            session: 현재 세션
            current_question: 현재 질문
            system_prompt: 시스템 프롬프트
            additional_context: 추가 컨텍스트

        Returns:
            LLM 메시지 형식의 컨텍스트
        """
        messages = []

        # 1. 시스템 프롬프트
        messages.append({
            "role": "system",
            "content": system_prompt
        })

        # 2. 사주 데이터 요약 (첫 번째 사용자 메시지로)
        if self.include_saju_summary:
            saju_context = self._build_saju_context(session)
            messages.append({
                "role": "user",
                "content": f"다음은 분석할 사주 정보입니다:\n\n{saju_context}"
            })
            messages.append({
                "role": "assistant",
                "content": "네, 사주 정보를 확인했습니다. 질문해 주세요."
            })

        # 3. 캐시된 해석 정보 (있다면)
        if self.include_cached_interpretations and session.interpretation_cache:
            cached_summary = self._build_cached_summary(session)
            if cached_summary:
                messages.append({
                    "role": "user",
                    "content": "이전에 받은 해석을 참고해 주세요."
                })
                messages.append({
                    "role": "assistant",
                    "content": cached_summary
                })

        # 4. 대화 이력
        history = session.get_messages_for_llm(self.max_history_messages)
        messages.extend(history)

        # 5. 추가 컨텍스트 (있다면)
        if additional_context:
            messages.append({
                "role": "system",
                "content": f"추가 참고 정보:\n{additional_context}"
            })

        # 6. 현재 질문
        messages.append({
            "role": "user",
            "content": current_question
        })

        return messages

    def _build_saju_context(self, session: Session) -> str:
        """사주 컨텍스트 문자열 생성"""
        return format_saju_context(session.saju_data)

    def _build_cached_summary(self, session: Session) -> Optional[str]:
        """캐시된 해석 요약"""
        if not session.interpretation_cache:
            return None

        summaries = []
        for agent_name, cache_data in session.interpretation_cache.items():
            interpretation = cache_data.get("interpretation")
            if interpretation:
                # 해석 내용 요약 (첫 500자)
                content = interpretation.get("interpretation", "")[:500]
                if content:
                    summaries.append(f"**{agent_name} 해석 요약:**\n{content}...")

        if summaries:
            return "\n\n".join(summaries)
        return None

    def build_quick_context(
        self,
        saju_data: Dict,
        question: str,
        system_prompt: str
    ) -> List[Dict[str, str]]:
        """
        세션 없이 빠른 컨텍스트 구성

        Args:
            saju_data: 사주 데이터
            question: 질문
            system_prompt: 시스템 프롬프트

        Returns:
            LLM 메시지 형식
        """
        saju_context = format_saju_context(saju_data)

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{saju_context}\n\n## 질문\n{question}"}
        ]

    def summarize_conversation(
        self,
        session: Session,
        max_messages: int = 20
    ) -> str:
        """
        대화 요약 생성 (긴 대화용)

        Args:
            session: 세션
            max_messages: 요약할 최대 메시지 수

        Returns:
            대화 요약 문자열
        """
        messages = session.messages[-max_messages:]

        summary_parts = []

        for msg in messages:
            role_label = "사용자" if msg.role == "user" else "어시스턴트"
            # 긴 메시지는 요약
            content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
            summary_parts.append(f"[{role_label}] {content}")

        return "\n".join(summary_parts)

    def extract_key_topics(self, session: Session) -> List[str]:
        """
        대화에서 주요 토픽 추출

        Args:
            session: 세션

        Returns:
            토픽 키워드 목록
        """
        topics = set()

        # 간단한 키워드 추출 (실제로는 더 정교한 NLP 필요)
        keywords = {
            "성격": ["성격", "기질", "성향", "특성"],
            "직업": ["직업", "일", "취업", "사업", "재물"],
            "연애": ["연애", "결혼", "배우자", "이성"],
            "건강": ["건강", "몸", "질병"],
            "운세": ["운세", "대운", "올해", "내년", "시기"],
        }

        for msg in session.messages:
            if msg.role == "user":
                content = msg.content.lower()
                for topic, kws in keywords.items():
                    if any(kw in content for kw in kws):
                        topics.add(topic)

        return list(topics)
