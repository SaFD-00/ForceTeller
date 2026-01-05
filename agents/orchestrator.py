"""
오케스트레이터
에이전트 선택 및 조율을 담당
"""

import json
import asyncio
from typing import Dict, List, Optional, Any

from utils.llm_client import LLMClient
from agents.base_agent import AgentResponse
from agents.prompts.system_prompts import ORCHESTRATOR_SYSTEM_PROMPT
from agents.interpreters import (
    PersonalityAgent,
    CareerAgent,
    RelationshipAgent,
    HealthAgent,
    FortuneAgent,
    SynthesisAgent,
    YongsinAgent,
    SchoolCompareAgent,
)


class Orchestrator:
    """에이전트 오케스트레이터"""

    # 에이전트 매핑
    AGENT_CLASSES = {
        "personality": PersonalityAgent,
        "career": CareerAgent,
        "relationship": RelationshipAgent,
        "health": HealthAgent,
        "fortune": FortuneAgent,
        "synthesis": SynthesisAgent,
        "yongsin": YongsinAgent,
        "school_compare": SchoolCompareAgent,
    }

    # 키워드 기반 에이전트 매핑 (간단한 규칙 기반)
    KEYWORD_MAPPING = {
        "personality": ["성격", "기질", "성향", "특성", "장단점", "강점", "약점"],
        "career": ["직업", "일", "직장", "취업", "사업", "재물", "돈", "부", "투자", "경력"],
        "relationship": ["연애", "결혼", "배우자", "인연", "이성", "사랑", "대인관계", "친구", "가족"],
        "health": ["건강", "질병", "아픈", "체질", "몸", "운동", "음식"],
        "fortune": ["운세", "대운", "올해", "내년", "언제", "시기", "때", "미래", "앞으로"],
        "yongsin": ["용신", "희신", "기신", "개운", "강약", "신강", "신약"],
        "school_compare": ["유파", "비교", "자평", "적천수", "궁통보감", "현대명리", "신살"],
    }

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = None,
        use_llm_routing: bool = False
    ):
        """
        Args:
            llm_provider: LLM 제공자
            model: 모델명
            use_llm_routing: LLM 기반 라우팅 사용 여부 (False면 키워드 기반)
        """
        self.llm_provider = llm_provider
        self.model = model
        self.use_llm_routing = use_llm_routing

        if use_llm_routing:
            self.llm_client = LLMClient(provider=llm_provider)

        # 에이전트 인스턴스 캐시
        self._agents: Dict[str, Any] = {}

    def _get_agent(self, agent_name: str) -> Any:
        """에이전트 인스턴스 가져오기 (캐시 사용)"""
        if agent_name not in self._agents:
            agent_class = self.AGENT_CLASSES.get(agent_name)
            if agent_class:
                self._agents[agent_name] = agent_class(
                    llm_provider=self.llm_provider,
                    model=self.model
                )
        return self._agents.get(agent_name)

    def _select_agents_by_keyword(self, question: str) -> List[str]:
        """키워드 기반 에이전트 선택"""
        selected = []

        question_lower = question.lower()

        for agent_name, keywords in self.KEYWORD_MAPPING.items():
            for keyword in keywords:
                if keyword in question_lower:
                    if agent_name not in selected:
                        selected.append(agent_name)
                    break

        # 전체 해석 요청 감지
        full_request_keywords = ["전체", "종합", "다", "모두", "전반", "봐주세요", "알려주세요"]
        if not selected or any(kw in question_lower for kw in full_request_keywords):
            selected = ["personality", "career", "relationship", "fortune"]

        return selected

    async def _select_agents_by_llm(self, question: str) -> Dict:
        """LLM 기반 에이전트 선택"""
        messages = [
            {"role": "system", "content": ORCHESTRATOR_SYSTEM_PROMPT},
            {"role": "user", "content": f"사용자 질문: {question}"}
        ]

        try:
            response = await self.llm_client.chat(
                messages=messages,
                model=self.model
            )

            # LLMClient.chat()은 문자열을 반환
            content = response if isinstance(response, str) else str(response)

            # JSON 파싱 시도
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # JSON 파싱 실패시 기본값
                return {
                    "agents": self._select_agents_by_keyword(question),
                    "reasoning": "LLM 응답 파싱 실패, 키워드 기반 선택"
                }

        except Exception as e:
            return {
                "agents": self._select_agents_by_keyword(question),
                "reasoning": f"LLM 라우팅 실패: {str(e)}"
            }

    async def route_and_interpret(
        self,
        saju_data: Dict,
        question: str,
        conversation_history: Optional[List[Dict]] = None,
        include_synthesis: bool = True
    ) -> Dict[str, Any]:
        """
        질문을 분석하여 적절한 에이전트로 라우팅하고 해석 수행

        Args:
            saju_data: 사주 계산 결과
            question: 사용자 질문
            conversation_history: 대화 이력
            include_synthesis: 종합 해석 포함 여부

        Returns:
            {
                "agents_used": [...],
                "interpretations": {...},
                "synthesis": "...",
                "routing_info": {...}
            }
        """
        # 1. 에이전트 선택
        if self.use_llm_routing:
            routing_result = await self._select_agents_by_llm(question)
            selected_agents = routing_result.get("agents", [])
        else:
            selected_agents = self._select_agents_by_keyword(question)
            routing_result = {
                "agents": selected_agents,
                "reasoning": "키워드 기반 선택"
            }

        # 2. 선택된 에이전트들로 병렬 해석
        interpretation_tasks = []
        agent_names = []

        for agent_name in selected_agents:
            if agent_name == "synthesis":
                continue  # synthesis는 나중에 별도 처리

            agent = self._get_agent(agent_name)
            if agent:
                task = agent.interpret(
                    saju_data=saju_data,
                    user_question=question,
                    conversation_history=conversation_history
                )
                interpretation_tasks.append(task)
                agent_names.append(agent_name)

        # 병렬 실행
        responses = await asyncio.gather(*interpretation_tasks, return_exceptions=True)

        # 결과 정리
        interpretations = {}
        valid_responses = []

        for agent_name, response in zip(agent_names, responses):
            if isinstance(response, Exception):
                interpretations[agent_name] = {
                    "error": str(response),
                    "interpretation": None
                }
            else:
                interpretations[agent_name] = response.to_dict()
                if response.confidence > 0:
                    valid_responses.append(response)

        # 3. 종합 해석 (선택적)
        synthesis_result = None
        if include_synthesis and len(valid_responses) > 1:
            synthesis_agent = self._get_agent("synthesis")
            if synthesis_agent:
                synthesis_response = await synthesis_agent.synthesize(
                    saju_data=saju_data,
                    agent_responses=valid_responses,
                    user_question=question,
                    conversation_history=conversation_history
                )
                synthesis_result = synthesis_response.to_dict()

        return {
            "agents_used": agent_names,
            "interpretations": interpretations,
            "synthesis": synthesis_result,
            "routing_info": routing_result
        }

    async def interpret_full(
        self,
        saju_data: Dict,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        전체 해석 수행 (모든 에이전트 사용)

        Args:
            saju_data: 사주 계산 결과
            conversation_history: 대화 이력

        Returns:
            전체 해석 결과
        """
        return await self.route_and_interpret(
            saju_data=saju_data,
            question="전체적으로 사주를 분석해 주세요.",
            conversation_history=conversation_history,
            include_synthesis=True
        )

    async def quick_interpret(
        self,
        saju_data: Dict,
        focus: str = "personality"
    ) -> AgentResponse:
        """
        빠른 단일 해석

        Args:
            saju_data: 사주 계산 결과
            focus: 해석 초점 (에이전트 이름)

        Returns:
            단일 에이전트 응답
        """
        agent = self._get_agent(focus)
        if not agent:
            return AgentResponse(
                agent_name=focus,
                interpretation=f"'{focus}' 에이전트를 찾을 수 없습니다.",
                confidence=0.0
            )

        return await agent.interpret(saju_data=saju_data)
