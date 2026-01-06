"""
세션 관리 모듈
Multi-turn 대화를 위한 세션 관리
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Message:
    """대화 메시지"""
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Message":
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


@dataclass
class Session:
    """대화 세션"""
    session_id: str
    saju_data: Dict[str, Any]
    messages: List[Message] = field(default_factory=list)
    interpretation_cache: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Message:
        """메시지 추가"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.last_activity = datetime.now()
        return message

    def add_user_message(self, content: str) -> Message:
        """사용자 메시지 추가"""
        return self.add_message("user", content)

    def add_assistant_message(self, content: str, agent_name: Optional[str] = None) -> Message:
        """어시스턴트 메시지 추가"""
        metadata = {"agent": agent_name} if agent_name else {}
        return self.add_message("assistant", content, metadata)

    def get_messages_for_llm(self, limit: int = 10) -> List[Dict]:
        """LLM 호출용 메시지 형식 반환"""
        recent = self.messages[-limit:] if limit else self.messages
        return [{"role": m.role, "content": m.content} for m in recent]

    def cache_interpretation(self, agent_name: str, interpretation: Any):
        """해석 결과 캐시"""
        self.interpretation_cache[agent_name] = {
            "interpretation": interpretation,
            "cached_at": datetime.now().isoformat()
        }

    def get_cached_interpretation(self, agent_name: str) -> Optional[Any]:
        """캐시된 해석 반환"""
        cached = self.interpretation_cache.get(agent_name)
        if cached:
            return cached.get("interpretation")
        return None

    def is_expired(self, max_age_hours: int = 24) -> bool:
        """세션 만료 여부 확인"""
        age = datetime.now() - self.last_activity
        return age > timedelta(hours=max_age_hours)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "saju_data": self.saju_data,
            "messages": [m.to_dict() for m in self.messages],
            "interpretation_cache": self.interpretation_cache,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Session":
        return cls(
            session_id=data["session_id"],
            saju_data=data["saju_data"],
            messages=[Message.from_dict(m) for m in data.get("messages", [])],
            interpretation_cache=data.get("interpretation_cache", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            last_activity=datetime.fromisoformat(data.get("last_activity", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


class SessionManager:
    """세션 관리자"""

    def __init__(self, max_sessions: int = 1000, session_ttl_hours: int = 24):
        """
        Args:
            max_sessions: 최대 세션 수
            session_ttl_hours: 세션 유효 시간 (시간)
        """
        self._sessions: Dict[str, Session] = {}
        self.max_sessions = max_sessions
        self.session_ttl_hours = session_ttl_hours

    def create_session(self, saju_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Session:
        """
        새 세션 생성

        Args:
            saju_data: 사주 계산 결과
            metadata: 추가 메타데이터

        Returns:
            생성된 Session
        """
        # 세션 수 초과시 오래된 세션 정리
        self._cleanup_if_needed()

        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            saju_data=saju_data,
            metadata=metadata or {}
        )

        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        세션 조회

        Args:
            session_id: 세션 ID

        Returns:
            Session 또는 None
        """
        session = self._sessions.get(session_id)

        if session:
            if session.is_expired(self.session_ttl_hours):
                self.delete_session(session_id)
                return None
            session.last_activity = datetime.now()

        return session

    def delete_session(self, session_id: str) -> bool:
        """
        세션 삭제

        Args:
            session_id: 세션 ID

        Returns:
            삭제 성공 여부
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Message]:
        """
        세션에 메시지 추가

        Args:
            session_id: 세션 ID
            role: 역할
            content: 내용
            metadata: 메타데이터

        Returns:
            추가된 Message 또는 None
        """
        session = self.get_session(session_id)
        if session:
            return session.add_message(role, content, metadata)
        return None

    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        대화 이력 조회

        Args:
            session_id: 세션 ID
            limit: 최근 메시지 개수

        Returns:
            메시지 목록
        """
        session = self.get_session(session_id)
        if session:
            return session.get_messages_for_llm(limit)
        return []

    def list_sessions(self) -> List[Dict]:
        """
        모든 세션 목록

        Returns:
            세션 정보 목록
        """
        def get_name(saju_data):
            """사주 데이터에서 이름 추출 (원본/display 형식 모두 지원)"""
            if not isinstance(saju_data, dict):
                return "Unknown"
            # 프론트엔드 display 형식
            if "birth_info" in saju_data:
                birth_info = saju_data.get("birth_info", {})
                if isinstance(birth_info, dict):
                    return birth_info.get("name", "Unknown")
            # 백엔드 원본 형식
            if "input" in saju_data:
                input_data = saju_data.get("input", {})
                if isinstance(input_data, dict):
                    return input_data.get("name", "Unknown")
            return "Unknown"

        return [
            {
                "session_id": s.session_id,
                "created_at": s.created_at.isoformat(),
                "last_activity": s.last_activity.isoformat(),
                "message_count": len(s.messages),
                "name": get_name(s.saju_data)
            }
            for s in self._sessions.values()
            if not s.is_expired(self.session_ttl_hours)
        ]

    def _cleanup_if_needed(self):
        """필요시 오래된 세션 정리"""
        # 만료된 세션 삭제
        expired = [
            sid for sid, session in self._sessions.items()
            if session.is_expired(self.session_ttl_hours)
        ]
        for sid in expired:
            del self._sessions[sid]

        # 최대 세션 수 초과시 오래된 것부터 삭제
        if len(self._sessions) >= self.max_sessions:
            sorted_sessions = sorted(
                self._sessions.items(),
                key=lambda x: x[1].last_activity
            )
            # 20% 정리
            to_remove = len(self._sessions) - int(self.max_sessions * 0.8)
            for sid, _ in sorted_sessions[:to_remove]:
                del self._sessions[sid]

    def get_session_count(self) -> int:
        """활성 세션 수 반환"""
        return len(self._sessions)

    def export_session(self, session_id: str) -> Optional[Dict]:
        """세션 데이터 내보내기"""
        session = self.get_session(session_id)
        if session:
            return session.to_dict()
        return None

    def import_session(self, session_data: Dict) -> Session:
        """세션 데이터 가져오기"""
        session = Session.from_dict(session_data)
        self._sessions[session.session_id] = session
        return session
