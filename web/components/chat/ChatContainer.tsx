'use client';

import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { AgentSelector } from './AgentSelector';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { SuggestedQuestions } from './SuggestedQuestions';
import { GlassCard } from '@/components/ui';
import { sendChatMessage, streamChatMessage } from '@/lib/api/chat';
import { useSajuStore, useChatStore } from '@/stores/sajuStore';
import type { AgentType, ChatMessage, Element } from '@/types/saju';

// 천간/지지 데이터
const STEMS = [
  { korean: '갑', hanja: '甲', element: '목' as Element },
  { korean: '을', hanja: '乙', element: '목' as Element },
  { korean: '병', hanja: '丙', element: '화' as Element },
  { korean: '정', hanja: '丁', element: '화' as Element },
  { korean: '무', hanja: '戊', element: '토' as Element },
  { korean: '기', hanja: '己', element: '토' as Element },
  { korean: '경', hanja: '庚', element: '금' as Element },
  { korean: '신', hanja: '辛', element: '금' as Element },
  { korean: '임', hanja: '壬', element: '수' as Element },
  { korean: '계', hanja: '癸', element: '수' as Element },
];

const BRANCHES = [
  { korean: '자', hanja: '子', element: '수' as Element },
  { korean: '축', hanja: '丑', element: '토' as Element },
  { korean: '인', hanja: '寅', element: '목' as Element },
  { korean: '묘', hanja: '卯', element: '목' as Element },
  { korean: '진', hanja: '辰', element: '토' as Element },
  { korean: '사', hanja: '巳', element: '화' as Element },
  { korean: '오', hanja: '午', element: '화' as Element },
  { korean: '미', hanja: '未', element: '토' as Element },
  { korean: '신', hanja: '申', element: '금' as Element },
  { korean: '유', hanja: '酉', element: '금' as Element },
  { korean: '술', hanja: '戌', element: '토' as Element },
  { korean: '해', hanja: '亥', element: '수' as Element },
];

// 십성 계산 함수
function calculateTenGod(dayMasterElement: Element, stemElement: Element): string {
  const relations: Record<Element, Record<Element, string>> = {
    '목': { '목': '비겁', '화': '식상', '토': '재성', '금': '관성', '수': '인성' },
    '화': { '목': '인성', '화': '비겁', '토': '식상', '금': '재성', '수': '관성' },
    '토': { '목': '관성', '화': '인성', '토': '비겁', '금': '식상', '수': '재성' },
    '금': { '목': '재성', '화': '관성', '토': '인성', '금': '비겁', '수': '식상' },
    '수': { '목': '식상', '화': '재성', '토': '관성', '금': '인성', '수': '비겁' },
  };
  return relations[dayMasterElement]?.[stemElement] || '-';
}

// 연도로부터 간지 계산
function getYearGanji(year: number) {
  const stemIndex = (year - 4) % 10;
  const branchIndex = (year - 4) % 12;
  return {
    stem: STEMS[stemIndex >= 0 ? stemIndex : stemIndex + 10],
    branch: BRANCHES[branchIndex >= 0 ? branchIndex : branchIndex + 12],
  };
}

// 월로부터 간지 계산
function getMonthGanji(year: number, month: number) {
  const yearStemIndex = (year - 4) % 10;
  const monthStemBase = (yearStemIndex % 5) * 2;
  const monthStemIndex = (monthStemBase + month - 1) % 10;
  const monthBranchIndex = (month + 1) % 12;
  return {
    stem: STEMS[monthStemIndex],
    branch: BRANCHES[monthBranchIndex],
  };
}

// 일주 간지 계산
function getDayGanji(date: Date) {
  const baseDate = new Date(1900, 0, 31);
  const diffTime = date.getTime() - baseDate.getTime();
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  const stemIndex = ((diffDays % 10) + 10) % 10;
  const branchIndex = ((diffDays % 12) + 12) % 12;
  return {
    stem: STEMS[stemIndex],
    branch: BRANCHES[branchIndex],
  };
}

// 현재 운세 데이터 생성
function getCurrentFortuneData(dayMasterElement: Element) {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1;

  // 연운
  const yearGanji = getYearGanji(currentYear);
  const yearlyFortune = {
    year: currentYear,
    stem: yearGanji.stem.korean,
    branch: yearGanji.branch.korean,
    ten_god: calculateTenGod(dayMasterElement, yearGanji.stem.element),
    element: yearGanji.stem.element,
  };

  // 월운
  const monthGanji = getMonthGanji(currentYear, currentMonth);
  const monthlyFortune = {
    year: currentYear,
    month: currentMonth,
    stem: monthGanji.stem.korean,
    branch: monthGanji.branch.korean,
    ten_god: calculateTenGod(dayMasterElement, monthGanji.stem.element),
    element: monthGanji.stem.element,
  };

  // 일운
  const dayGanji = getDayGanji(now);
  const dailyFortune = {
    date: now.toISOString().split('T')[0],
    stem: dayGanji.stem.korean,
    branch: dayGanji.branch.korean,
    ten_god: calculateTenGod(dayMasterElement, dayGanji.stem.element),
    element: dayGanji.stem.element,
  };

  return {
    yearly: yearlyFortune,
    monthly: monthlyFortune,
    daily: dailyFortune,
  };
}

// 상담 분야별 첫 질문 (종합 상담 제외)
const INITIAL_QUESTIONS: Record<Exclude<AgentType, 'general'>, string> = {
  personality: '제 사주로 본 성격과 기질을 분석해주세요.',
  career: '제 사주에 맞는 직업 적성과 재물운을 알려주세요.',
  relationship: '제 사주로 본 연애운과 인연을 분석해주세요.',
  health: '제 사주로 본 건강 체질과 주의해야 할 점을 알려주세요.',
  fortune: '올해 운세와 앞으로의 운세 흐름을 알려주세요.',
  yongsin: '제 사주의 용신과 기신을 분석해주세요.',
  school_compare: '제 사주를 5개 유파로 비교 분석해주세요.',
};

export function ChatContainer() {
  const { result } = useSajuStore();
  const { messages, addMessage, sessionId, setSessionId } = useChatStore();
  const [selectedAgent, setSelectedAgent] = useState<AgentType>('general');
  const [isLoading, setIsLoading] = useState(false);
  const [reasoning, setReasoning] = useState('');
  const [streamingOutput, setStreamingOutput] = useState('');
  const [isReasoningComplete, setIsReasoningComplete] = useState(false);
  const askedAgentsRef = useRef(new Set<AgentType>(['general' as AgentType]));
  const isFirstMount = useRef(true);

  // 마지막 메시지에서 추천 질문 가져오기
  const lastSuggestedQuestions = useMemo(() => {
    if (messages.length === 0) return [];
    const lastAssistantMsg = [...messages].reverse().find(m => m.role === 'assistant');
    return lastAssistantMsg?.suggested_questions || [];
  }, [messages]);

  // 메시지 전송 함수 (스트리밍 지원)
  const sendMessage = useCallback(
    async (content: string, agentType: AgentType) => {
      if (!result) return;

      // Add user message
      const userMessage: ChatMessage = {
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      addMessage(userMessage);

      setIsLoading(true);
      setReasoning('');
      setStreamingOutput('');
      setIsReasoningComplete(false);

      try {
        // 현재 운세 데이터 계산
        const dayMasterElement = result.four_pillars.day.heavenly_stem.element;
        const currentFortunes = getCurrentFortuneData(dayMasterElement);

        // 현재 대운 찾기
        const birthYear = new Date(result.birth_info.birth_date).getFullYear();
        const currentAge = new Date().getFullYear() - birthYear;
        const currentDaewun = result.fortune_cycles?.find(
          (cycle) => currentAge >= cycle.start_age && currentAge < (cycle.start_age + 10)
        );

        const sajuContext = {
          four_pillars: result.four_pillars,
          five_elements: result.five_elements,
          ten_gods: result.ten_gods,
          strength: result.strength,
          birth_info: result.birth_info,
          fortune_cycles: {
            current_daewun: currentDaewun ? {
              start_age: currentDaewun.start_age,
              stem: currentDaewun.heavenly_stem.korean,
              branch: currentDaewun.earthly_branch.korean,
              ten_god: calculateTenGod(dayMasterElement, currentDaewun.heavenly_stem.element),
            } : undefined,
            yearly: currentFortunes.yearly,
            monthly: currentFortunes.monthly,
            daily: currentFortunes.daily,
          },
        };

        let fullOutput = '';
        let newSessionId = sessionId;
        let suggestedQuestions: string[] = [];
        let respondingAgent: string | undefined;
        let respondingAgentName: string | undefined;
        let respondingConfidence: number | undefined;

        // 스트리밍으로 메시지 수신
        for await (const chunk of streamChatMessage({
          message: content,
          agent_type: agentType,
          session_id: sessionId || undefined,
          saju_context: sajuContext,
        })) {
          switch (chunk.type) {
            case 'session':
              // 새 세션 ID 수신
              if (chunk.content && !sessionId) {
                newSessionId = chunk.content as string;
                setSessionId(chunk.content as string);
              }
              break;
            case 'agent_selected':
              // 응답을 담당한 에이전트 출처·신뢰도
              respondingAgent = chunk.agent;
              respondingAgentName = chunk.display_name;
              respondingConfidence = chunk.confidence;
              break;
            case 'reasoning':
              // AI 사고 과정 스트리밍
              setReasoning(prev => prev + (chunk.content as string));
              break;
            case 'reasoning_done':
              // 사고 과정 완료
              setIsReasoningComplete(true);
              break;
            case 'output':
              // 최종 응답 스트리밍
              fullOutput += chunk.content as string;
              setStreamingOutput(fullOutput);
              break;
            case 'error':
              throw new Error(chunk.content as string);
            case 'suggested_questions':
              // 추천 질문 수신
              suggestedQuestions = chunk.content as string[];
              break;
            case 'done':
              // 스트리밍 완료
              break;
          }
        }

        // 완료 후 메시지로 저장
        if (fullOutput) {
          const assistantMessage: ChatMessage = {
            role: 'assistant',
            content: fullOutput,
            timestamp: new Date().toISOString(),
            suggested_questions: suggestedQuestions.length > 0 ? suggestedQuestions : undefined,
            agent: respondingAgent,
            agent_display_name: respondingAgentName,
            confidence: respondingConfidence,
          };
          addMessage(assistantMessage);
        }

        // 스트리밍 상태 초기화
        setReasoning('');
        setStreamingOutput('');
        setIsReasoningComplete(false);

      } catch (error) {
        console.error('Chat error:', error);
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: '죄송합니다. 응답을 생성하는 중 오류가 발생했습니다. 다시 시도해주세요.',
          timestamp: new Date().toISOString(),
        };
        addMessage(errorMessage);
        // 에러 시 상태 초기화
        setReasoning('');
        setStreamingOutput('');
        setIsReasoningComplete(false);
      } finally {
        setIsLoading(false);
      }
    },
    [result, sessionId, addMessage, setSessionId]
  );

  // 상담 분야 변경 시 자동 첫 질문 전송
  useEffect(() => {
    // 첫 마운트 시에는 실행하지 않음
    if (isFirstMount.current) {
      isFirstMount.current = false;
      return;
    }

    // 종합 상담이 아니고, 아직 질문하지 않은 분야인 경우
    if (
      selectedAgent !== 'general' &&
      !askedAgentsRef.current.has(selectedAgent) &&
      result &&
      !isLoading
    ) {
      const initialQuestion = INITIAL_QUESTIONS[selectedAgent];
      askedAgentsRef.current.add(selectedAgent);
      sendMessage(initialQuestion, selectedAgent);
    }
  }, [selectedAgent, result, isLoading, sendMessage]);

  // 사용자 입력 메시지 전송
  const handleSendMessage = useCallback(
    (content: string) => {
      sendMessage(content, selectedAgent);
    },
    [sendMessage, selectedAgent]
  );

  // 추천 질문 클릭 핸들러
  const handleSuggestedQuestionClick = useCallback(
    (question: string) => {
      sendMessage(question, selectedAgent);
    },
    [sendMessage, selectedAgent]
  );

  return (
    <GlassCard className="flex flex-col h-full overflow-hidden p-0">
      <AgentSelector selected={selectedAgent} onSelect={setSelectedAgent} />
      <MessageList
        messages={messages}
        isLoading={isLoading}
        reasoning={reasoning}
        streamingOutput={streamingOutput}
        isReasoningComplete={isReasoningComplete}
        onSuggestedQuestionClick={handleSuggestedQuestionClick}
      />
      <SuggestedQuestions
        questions={lastSuggestedQuestions}
        onQuestionClick={handleSuggestedQuestionClick}
        disabled={isLoading || !result}
      />
      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading || !result}
        placeholder={result ? '사주에 대해 질문하세요...' : '먼저 사주 분석을 진행해주세요'}
      />
    </GlassCard>
  );
}
