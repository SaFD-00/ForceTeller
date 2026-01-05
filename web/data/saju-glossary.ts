/**
 * 사주 용어 사전 데이터
 * 사용자가 어려운 사주 용어 위에 hover/click시 설명을 보여주는 기능을 위한 데이터
 */

export interface GlossaryEntry {
  term: string;           // 용어 (한글)
  hanja: string;          // 한자
  hanjaBreakdown: string; // 한자 풀이
  shortDesc: string;      // 짧은 설명 (툴팁용)
  longDesc: string;       // 상세 설명 (모달용)
  category: '천간' | '지지' | '십성' | '12운성' | '신살' | '합충' | '용어';
}

// 천간 (10개)
const CHEONGAN_GLOSSARY: Record<string, GlossaryEntry> = {
  '갑목': {
    term: '갑목',
    hanja: '甲木',
    hanjaBreakdown: '갑옷 갑(甲), 나무 목(木)',
    shortDesc: '양(+)의 에너지를 지닌 목(木)',
    longDesc: '큰 나무, 대들보를 상징합니다. 곧고 뻗어나가려는 성장 욕구가 강하며, 순수하고 리더십이 있습니다. 고집이 세고 융통성이 부족할 수 있습니다.',
    category: '천간'
  },
  '을목': {
    term: '을목',
    hanja: '乙木',
    hanjaBreakdown: '새 을(乙), 나무 목(木)',
    shortDesc: '음(-)의 에너지를 지닌 목(木)',
    longDesc: '덩굴, 화초, 잔디를 상징합니다. 유연하고 환경 적응력이 뛰어나며, 생존력이 강합니다. 부드러우나 질기고, 끈기가 있습니다.',
    category: '천간'
  },
  '병화': {
    term: '병화',
    hanja: '丙火',
    hanjaBreakdown: '밝을 병(丙), 불 화(火)',
    shortDesc: '양(+)의 에너지를 지닌 화(火)',
    longDesc: '태양, 큰 불을 상징합니다. 열정적이고 화려하며, 공명정대합니다. 밝고 따뜻한 에너지로 주변을 환하게 비춥니다.',
    category: '천간'
  },
  '정화': {
    term: '정화',
    hanja: '丁火',
    hanjaBreakdown: '고무래 정(丁), 불 화(火)',
    shortDesc: '음(-)의 에너지를 지닌 화(火)',
    longDesc: '촛불, 달빛, 별빛을 상징합니다. 은은하고 따뜻한 감수성을 지니며, 섬세하고 헌신적입니다. 내면의 열정을 조용히 태웁니다.',
    category: '천간'
  },
  '무토': {
    term: '무토',
    hanja: '戊土',
    hanjaBreakdown: '다섯째 천간 무(戊), 흙 토(土)',
    shortDesc: '양(+)의 에너지를 지닌 토(土)',
    longDesc: '산, 큰 언덕을 상징합니다. 신뢰감이 있고 중후하며, 포용력이 넓습니다. 안정적이고 변함없는 성품을 가집니다.',
    category: '천간'
  },
  '기토': {
    term: '기토',
    hanja: '己土',
    hanjaBreakdown: '몸 기(己), 흙 토(土)',
    shortDesc: '음(-)의 에너지를 지닌 토(土)',
    longDesc: '논밭, 정원의 흙을 상징합니다. 실속있고 다재다능하며, 어머니 같은 따뜻한 마음을 가집니다. 만물을 기르는 포용력이 있습니다.',
    category: '천간'
  },
  '경금': {
    term: '경금',
    hanja: '庚金',
    hanjaBreakdown: '일곱째 천간 경(庚), 쇠 금(金)',
    shortDesc: '양(+)의 에너지를 지닌 금(金)',
    longDesc: '원석, 무쇠, 도끼를 상징합니다. 결단력이 있고 의리를 중시하며, 혁명적인 기질이 있습니다. 강직하고 정의로운 성품입니다.',
    category: '천간'
  },
  '신금': {
    term: '신금',
    hanja: '辛金',
    hanjaBreakdown: '매울 신(辛), 쇠 금(金)',
    shortDesc: '음(-)의 에너지를 지닌 금(金)',
    longDesc: '보석, 가공된 금속을 상징합니다. 예민하고 정확하며, 깔끔합니다. 섬세한 감각과 심미안을 가지며, 완벽주의 성향이 있습니다.',
    category: '천간'
  },
  '임수': {
    term: '임수',
    hanja: '壬水',
    hanjaBreakdown: '아홉째 천간 임(壬), 물 수(水)',
    shortDesc: '양(+)의 에너지를 지닌 수(水)',
    longDesc: '바다, 큰 강을 상징합니다. 유연하고 총명하며, 속을 알 수 없는 깊이가 있습니다. 지혜롭고 포용력이 넓습니다.',
    category: '천간'
  },
  '계수': {
    term: '계수',
    hanja: '癸水',
    hanjaBreakdown: '열째 천간 계(癸), 물 수(水)',
    shortDesc: '음(-)의 에너지를 지닌 수(水)',
    longDesc: '비, 이슬, 샘물을 상징합니다. 지혜롭고 아이디어가 풍부하며, 기획력이 뛰어납니다. 조용히 스며드는 침투력이 있습니다.',
    category: '천간'
  },
};

// 지지 (12개)
const JIJI_GLOSSARY: Record<string, GlossaryEntry> = {
  '자': {
    term: '자',
    hanja: '子',
    hanjaBreakdown: '아들 자(子)',
    shortDesc: '쥐, 겨울의 한가운데, 자정',
    longDesc: '12지지의 첫 번째로, 쥐를 상징합니다. 겨울의 한가운데(음력 11월)이며, 자시(23시-01시)를 나타냅니다. 수(水) 기운이 가장 강한 시기입니다.',
    category: '지지'
  },
  '축': {
    term: '축',
    hanja: '丑',
    hanjaBreakdown: '소 축(丑)',
    shortDesc: '소, 늦겨울, 새벽',
    longDesc: '12지지의 두 번째로, 소를 상징합니다. 겨울이 끝나가는 시기(음력 12월)이며, 축시(01시-03시)를 나타냅니다. 습한 토(土) 기운을 가집니다.',
    category: '지지'
  },
  '인': {
    term: '인',
    hanja: '寅',
    hanjaBreakdown: '범 인(寅)',
    shortDesc: '호랑이, 이른 봄, 새벽',
    longDesc: '12지지의 세 번째로, 호랑이를 상징합니다. 봄의 시작(음력 1월, 입춘)이며, 인시(03시-05시)를 나타냅니다. 목(木) 기운이 시작됩니다.',
    category: '지지'
  },
  '묘': {
    term: '묘',
    hanja: '卯',
    hanjaBreakdown: '토끼 묘(卯)',
    shortDesc: '토끼, 봄의 한가운데, 일출',
    longDesc: '12지지의 네 번째로, 토끼를 상징합니다. 봄의 한가운데(음력 2월)이며, 묘시(05시-07시)를 나타냅니다. 목(木) 기운이 가장 강합니다.',
    category: '지지'
  },
  '진': {
    term: '진',
    hanja: '辰',
    hanjaBreakdown: '용 진(辰)',
    shortDesc: '용, 늦봄, 아침',
    longDesc: '12지지의 다섯 번째로, 용을 상징합니다. 봄이 끝나가는 시기(음력 3월)이며, 진시(07시-09시)를 나타냅니다. 습한 토(土) 기운을 가집니다.',
    category: '지지'
  },
  '사': {
    term: '사',
    hanja: '巳',
    hanjaBreakdown: '뱀 사(巳)',
    shortDesc: '뱀, 이른 여름, 오전',
    longDesc: '12지지의 여섯 번째로, 뱀을 상징합니다. 여름의 시작(음력 4월)이며, 사시(09시-11시)를 나타냅니다. 화(火) 기운이 시작됩니다.',
    category: '지지'
  },
  '오': {
    term: '오',
    hanja: '午',
    hanjaBreakdown: '말 오(午)',
    shortDesc: '말, 여름의 한가운데, 정오',
    longDesc: '12지지의 일곱 번째로, 말을 상징합니다. 여름의 한가운데(음력 5월)이며, 오시(11시-13시)를 나타냅니다. 화(火) 기운이 가장 강합니다.',
    category: '지지'
  },
  '미': {
    term: '미',
    hanja: '未',
    hanjaBreakdown: '양 미(未)',
    shortDesc: '양(염소), 늦여름, 오후',
    longDesc: '12지지의 여덟 번째로, 양을 상징합니다. 여름이 끝나가는 시기(음력 6월)이며, 미시(13시-15시)를 나타냅니다. 건조한 토(土) 기운을 가집니다.',
    category: '지지'
  },
  '신': {
    term: '신',
    hanja: '申',
    hanjaBreakdown: '원숭이 신(申)',
    shortDesc: '원숭이, 이른 가을, 오후',
    longDesc: '12지지의 아홉 번째로, 원숭이를 상징합니다. 가을의 시작(음력 7월)이며, 신시(15시-17시)를 나타냅니다. 금(金) 기운이 시작됩니다.',
    category: '지지'
  },
  '유': {
    term: '유',
    hanja: '酉',
    hanjaBreakdown: '닭 유(酉)',
    shortDesc: '닭, 가을의 한가운데, 일몰',
    longDesc: '12지지의 열 번째로, 닭을 상징합니다. 가을의 한가운데(음력 8월)이며, 유시(17시-19시)를 나타냅니다. 금(金) 기운이 가장 강합니다.',
    category: '지지'
  },
  '술': {
    term: '술',
    hanja: '戌',
    hanjaBreakdown: '개 술(戌)',
    shortDesc: '개, 늦가을, 저녁',
    longDesc: '12지지의 열한 번째로, 개를 상징합니다. 가을이 끝나가는 시기(음력 9월)이며, 술시(19시-21시)를 나타냅니다. 건조한 토(土) 기운을 가집니다.',
    category: '지지'
  },
  '해': {
    term: '해',
    hanja: '亥',
    hanjaBreakdown: '돼지 해(亥)',
    shortDesc: '돼지, 이른 겨울, 밤',
    longDesc: '12지지의 열두 번째로, 돼지를 상징합니다. 겨울의 시작(음력 10월)이며, 해시(21시-23시)를 나타냅니다. 수(水) 기운이 시작됩니다.',
    category: '지지'
  },
};

// 십성 (10개)
const SIPSEONG_GLOSSARY: Record<string, GlossaryEntry> = {
  '비견': {
    term: '비견',
    hanja: '比肩',
    hanjaBreakdown: '견줄 비(比), 어깨 견(肩)',
    shortDesc: '나와 같은 오행, 음양도 같음',
    longDesc: '일간과 같은 오행이면서 음양도 같은 관계입니다. 형제, 친구, 동료, 경쟁자를 의미합니다. 자주성이 강하고 독립심이 있습니다.',
    category: '십성'
  },
  '겁재': {
    term: '겁재',
    hanja: '劫財',
    hanjaBreakdown: '빼앗을 겁(劫), 재물 재(財)',
    shortDesc: '나와 같은 오행, 음양이 다름',
    longDesc: '일간과 같은 오행이지만 음양이 다른 관계입니다. 경쟁자, 라이벌을 의미합니다. 승부욕이 강하고 과감한 결단력이 있습니다.',
    category: '십성'
  },
  '식신': {
    term: '식신',
    hanja: '食神',
    hanjaBreakdown: '밥 식(食), 귀신 신(神)',
    shortDesc: '내가 생하는 오행, 음양이 같음',
    longDesc: '일간이 생하는 오행이면서 음양이 같은 관계입니다. 의식주, 표현력, 재능을 의미합니다. 온화하고 여유로우며 창작력이 있습니다.',
    category: '십성'
  },
  '상관': {
    term: '상관',
    hanja: '傷官',
    hanjaBreakdown: '다칠 상(傷), 벼슬 관(官)',
    shortDesc: '내가 생하는 오행, 음양이 다름',
    longDesc: '일간이 생하는 오행이지만 음양이 다른 관계입니다. 표현력, 언변, 예술성을 의미합니다. 창의적이고 반항적인 기질이 있습니다.',
    category: '십성'
  },
  '편재': {
    term: '편재',
    hanja: '偏財',
    hanjaBreakdown: '치우칠 편(偏), 재물 재(財)',
    shortDesc: '내가 극하는 오행, 음양이 같음',
    longDesc: '일간이 극하는 오행이면서 음양이 같은 관계입니다. 투기적 재물, 아버지(남자의 경우)를 의미합니다. 활동적이고 사교적입니다.',
    category: '십성'
  },
  '정재': {
    term: '정재',
    hanja: '正財',
    hanjaBreakdown: '바를 정(正), 재물 재(財)',
    shortDesc: '내가 극하는 오행, 음양이 다름',
    longDesc: '일간이 극하는 오행이지만 음양이 다른 관계입니다. 정당한 재물, 아내(남자의 경우)를 의미합니다. 성실하고 착실합니다.',
    category: '십성'
  },
  '편관': {
    term: '편관',
    hanja: '偏官',
    hanjaBreakdown: '치우칠 편(偏), 벼슬 관(官)',
    shortDesc: '나를 극하는 오행, 음양이 같음',
    longDesc: '일간을 극하는 오행이면서 음양이 같은 관계입니다. 칠살(七殺)이라고도 합니다. 권위, 압박, 스트레스를 의미하며, 카리스마가 있습니다.',
    category: '십성'
  },
  '정관': {
    term: '정관',
    hanja: '正官',
    hanjaBreakdown: '바를 정(正), 벼슬 관(官)',
    shortDesc: '나를 극하는 오행, 음양이 다름',
    longDesc: '일간을 극하는 오행이지만 음양이 다른 관계입니다. 직장, 명예, 규율, 남편(여자의 경우)을 의미합니다. 책임감이 강합니다.',
    category: '십성'
  },
  '편인': {
    term: '편인',
    hanja: '偏印',
    hanjaBreakdown: '치우칠 편(偏), 도장 인(印)',
    shortDesc: '나를 생하는 오행, 음양이 같음',
    longDesc: '일간을 생하는 오행이면서 음양이 같은 관계입니다. 특수한 학문, 직관력, 눈치를 의미합니다. 독창적이고 마니아적 기질이 있습니다.',
    category: '십성'
  },
  '정인': {
    term: '정인',
    hanja: '正印',
    hanjaBreakdown: '바를 정(正), 도장 인(印)',
    shortDesc: '나를 생하는 오행, 음양이 다름',
    longDesc: '일간을 생하는 오행이지만 음양이 다른 관계입니다. 어머니, 학문, 자격증을 의미합니다. 자애롭고 학구적입니다.',
    category: '십성'
  },
};

// 12운성 (12개)
const SIBIUNSEONG_GLOSSARY: Record<string, GlossaryEntry> = {
  '장생': {
    term: '장생',
    hanja: '長生',
    hanjaBreakdown: '길 장(長), 날 생(生)',
    shortDesc: '새로운 시작, 탄생의 기운',
    longDesc: '아기가 세상에 태어난 상태입니다. 새로운 시작, 생명력, 발전 가능성을 의미합니다. 희망차고 순수한 에너지입니다.',
    category: '12운성'
  },
  '목욕': {
    term: '목욕',
    hanja: '沐浴',
    hanjaBreakdown: '머리 감을 목(沐), 목욕할 욕(浴)',
    shortDesc: '정화와 성장, 도화의 자리',
    longDesc: '아기가 처음 목욕하는 상태입니다. 순수함, 새로움, 그리고 매력을 의미합니다. 도화살의 자리로 이성에게 인기가 있습니다.',
    category: '12운성'
  },
  '관대': {
    term: '관대',
    hanja: '冠帶',
    hanjaBreakdown: '갓 관(冠), 띠 대(帶)',
    shortDesc: '성장과 준비, 관복을 입음',
    longDesc: '성인이 되어 관을 쓰는 상태입니다. 사회 진출 준비, 야망, 자기 표현을 의미합니다. 외향적이고 당당합니다.',
    category: '12운성'
  },
  '건록': {
    term: '건록',
    hanja: '建祿',
    hanjaBreakdown: '세울 건(建), 복 록(祿)',
    shortDesc: '안정과 수입, 녹봉을 받음',
    longDesc: '직장을 얻어 녹봉을 받는 상태입니다. 자수성가, 안정적 수입, 노력의 결실을 의미합니다. 실력이 인정받는 시기입니다.',
    category: '12운성'
  },
  '제왕': {
    term: '제왕',
    hanja: '帝旺',
    hanjaBreakdown: '임금 제(帝), 왕성할 왕(旺)',
    shortDesc: '최고 전성기, 왕의 자리',
    longDesc: '가장 왕성하고 강한 상태입니다. 정점, 성공, 권력을 의미합니다. 하지만 정점 이후는 내려가므로 겸손이 필요합니다.',
    category: '12운성'
  },
  '쇠': {
    term: '쇠',
    hanja: '衰',
    hanjaBreakdown: '쇠할 쇠(衰)',
    shortDesc: '기운이 약해지기 시작',
    longDesc: '전성기를 지나 기운이 줄어드는 상태입니다. 은퇴 준비, 안정 추구를 의미합니다. 무리하지 않고 내실을 다지는 시기입니다.',
    category: '12운성'
  },
  '병': {
    term: '병',
    hanja: '病',
    hanjaBreakdown: '병 병(病)',
    shortDesc: '쇠약해진 상태',
    longDesc: '병에 걸린 듯 기운이 약한 상태입니다. 휴식, 치유, 돌봄이 필요합니다. 이 시기를 잘 넘기면 회복할 수 있습니다.',
    category: '12운성'
  },
  '사': {
    term: '사',
    hanja: '死',
    hanjaBreakdown: '죽을 사(死)',
    shortDesc: '에너지가 다한 상태',
    longDesc: '생명 에너지가 다한 상태입니다. 끝, 마무리, 정리를 의미합니다. 새로운 시작을 위한 종결의 단계입니다.',
    category: '12운성'
  },
  '묘': {
    term: '묘',
    hanja: '墓',
    hanjaBreakdown: '무덤 묘(墓)',
    shortDesc: '저장과 축적, 창고',
    longDesc: '무덤 또는 창고에 들어간 상태입니다. 저장, 보관, 숨은 힘을 의미합니다. 화개살의 자리로 학문, 예술, 종교와 관련됩니다.',
    category: '12운성'
  },
  '절': {
    term: '절',
    hanja: '絶',
    hanjaBreakdown: '끊을 절(絶)',
    shortDesc: '완전히 끊어진 상태',
    longDesc: '모든 것이 끊어진 상태입니다. 공허, 단절, 그러나 새로운 시작 직전을 의미합니다. 겁살의 자리이기도 합니다.',
    category: '12운성'
  },
  '태': {
    term: '태',
    hanja: '胎',
    hanjaBreakdown: '아이 밸 태(胎)',
    shortDesc: '새 생명이 잉태됨',
    longDesc: '새로운 생명이 잉태된 상태입니다. 씨앗, 가능성, 준비를 의미합니다. 조용히 힘을 축적하는 시기입니다.',
    category: '12운성'
  },
  '양': {
    term: '양',
    hanja: '養',
    hanjaBreakdown: '기를 양(養)',
    shortDesc: '태아가 자라는 상태',
    longDesc: '어머니 뱃속에서 자라는 상태입니다. 양육, 보호, 성장을 의미합니다. 장생 직전의 준비 단계입니다.',
    category: '12운성'
  },
};

// 신살 (20개 이상)
const SINSAL_GLOSSARY: Record<string, GlossaryEntry> = {
  '도화살': {
    term: '도화살',
    hanja: '桃花殺',
    hanjaBreakdown: '복숭아 도(桃), 꽃 화(花), 죽일 살(殺)',
    shortDesc: '이성에게 매력을 끼치는 별',
    longDesc: '복숭아꽃처럼 아름다운 매력을 가진 살입니다. 이성에게 인기가 많고 연애 운이 좋습니다. 너무 과하면 색정이나 외도의 우려가 있습니다.',
    category: '신살'
  },
  '역마살': {
    term: '역마살',
    hanja: '驛馬殺',
    hanjaBreakdown: '역참 역(驛), 말 마(馬), 죽일 살(殺)',
    shortDesc: '이동과 변동이 많은 별',
    longDesc: '역참의 말처럼 쉬지 않고 움직이는 살입니다. 출장, 이사, 여행이 많고 변화가 잦습니다. 활동적인 직업에 유리합니다.',
    category: '신살'
  },
  '화개살': {
    term: '화개살',
    hanja: '華蓋殺',
    hanjaBreakdown: '빛날 화(華), 덮을 개(蓋), 죽일 살(殺)',
    shortDesc: '학문, 예술, 종교의 별',
    longDesc: '화려한 덮개로 덮인 살입니다. 학문, 예술, 종교에 심취하기 쉽습니다. 내향적이고 철학적이며, 고독을 즐기는 성향이 있습니다.',
    category: '신살'
  },
  '장성살': {
    term: '장성살',
    hanja: '將星殺',
    hanjaBreakdown: '장수 장(將), 별 성(星), 죽일 살(殺)',
    shortDesc: '왕성한 기운, 리더십의 별',
    longDesc: '장수의 별처럼 권위와 리더십을 가진 살입니다. 조직을 이끄는 능력이 있고 권력 지향적입니다. 군, 경, 관직에 유리합니다.',
    category: '신살'
  },
  '망신살': {
    term: '망신살',
    hanja: '亡身殺',
    hanjaBreakdown: '망할 망(亡), 몸 신(身), 죽일 살(殺)',
    shortDesc: '체면과 명예 관련 구설수',
    longDesc: '몸을 드러내어 망신당할 수 있는 살입니다. 하지만 긍정적으로는 자신의 재능을 세상에 알리는 의미도 있습니다. 연예인, 방송인에게 유리할 수 있습니다.',
    category: '신살'
  },
  '겁살': {
    term: '겁살',
    hanja: '劫殺',
    hanjaBreakdown: '빼앗을 겁(劫), 죽일 살(殺)',
    shortDesc: '경쟁과 시비, 재물 손실',
    longDesc: '빼앗기고 경쟁하는 살입니다. 시비와 갈등이 생길 수 있고 재물 손실을 조심해야 합니다. 승부욕이 강한 특징이 있습니다.',
    category: '신살'
  },
  '괴강살': {
    term: '괴강살',
    hanja: '魁罡殺',
    hanjaBreakdown: '우두머리 괴(魁), 강할 강(罡), 죽일 살(殺)',
    shortDesc: '북두칠성의 우두머리 별',
    longDesc: '북두칠성의 우두머리인 괴성과 강성을 합친 살입니다. 총명하고 카리스마가 강하며, 결단력이 있습니다. 대발하거나 대흉할 수 있는 극단적 운명입니다.',
    category: '신살'
  },
  '천을귀인': {
    term: '천을귀인',
    hanja: '天乙貴人',
    hanjaBreakdown: '하늘 천(天), 새 을(乙), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '귀인의 도움을 받는 별',
    longDesc: '하늘이 내린 귀인이라는 뜻입니다. 어려울 때 귀인의 도움을 받아 위기를 넘깁니다. 가장 좋은 길신 중 하나입니다.',
    category: '신살'
  },
  '문창귀인': {
    term: '문창귀인',
    hanja: '文昌貴人',
    hanjaBreakdown: '글월 문(文), 창성할 창(昌), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '학문과 시험 운이 좋은 별',
    longDesc: '문장이 창성한다는 뜻입니다. 학문, 시험, 글쓰기에 뛰어난 재능이 있습니다. 공부운, 시험운, 자격증운이 좋습니다.',
    category: '신살'
  },
  '홍염살': {
    term: '홍염살',
    hanja: '紅艶殺',
    hanjaBreakdown: '붉을 홍(紅), 고울 염(艶), 죽일 살(殺)',
    shortDesc: '능동적 매력, 유혹의 별',
    longDesc: '붉고 아름다운 매력의 살입니다. 도화살과 달리 능동적으로 매력을 발산합니다. 타겟에게 의도적으로 매력을 어필하는 능력이 있습니다.',
    category: '신살'
  },
  '원진살': {
    term: '원진살',
    hanja: '怨嗔殺',
    hanjaBreakdown: '원망할 원(怨), 성낼 진(嗔), 죽일 살(殺)',
    shortDesc: '서로 원망하고 미워하는 관계',
    longDesc: '서로 원망하고 미워하는 살입니다. 처음에는 좋다가 나중에 원수가 되거나, 가까이 있으면 불편한 관계입니다.',
    category: '신살'
  },
  '귀문관살': {
    term: '귀문관살',
    hanja: '鬼門關殺',
    hanjaBreakdown: '귀신 귀(鬼), 문 문(門), 빗장 관(關), 죽일 살(殺)',
    shortDesc: '정신적 고민, 신비 체험',
    longDesc: '귀신이 드나드는 문이라는 뜻입니다. 정신적 고민이 많고 신비로운 체험을 할 수 있습니다. 감각이 예민하고 직관력이 뛰어납니다.',
    category: '신살'
  },
  // 12신살 추가 (Phase 3)
  '재살': {
    term: '재살',
    hanja: '災殺',
    hanjaBreakdown: '재앙 재(災), 죽일 살(殺)',
    shortDesc: '관재수와 재난의 별',
    longDesc: '일명 수옥살(囚獄殺)이라 하여 감옥에 갇히는 형국입니다. 운이 나쁘면 재난, 질병, 송사, 구속 등이 일어나고, 운이 좋으면 권력기관에서 위명을 떨칩니다.',
    category: '신살'
  },
  '천살': {
    term: '천살',
    hanja: '天殺',
    hanjaBreakdown: '하늘 천(天), 죽일 살(殺)',
    shortDesc: '하늘의 재앙, 천재지변',
    longDesc: '하늘에서 내리는 천재지변 같은 재난을 의미합니다. 홍수, 가뭄, 태풍 등 피하기 힘든 재해를 겪거나 치매, 중풍 등의 질병을 겪을 위험이 있습니다.',
    category: '신살'
  },
  '지살': {
    term: '지살',
    hanja: '地殺',
    hanjaBreakdown: '땅 지(地), 죽일 살(殺)',
    shortDesc: '땅의 변동, 자발적 이동',
    longDesc: '땅에서 일어나는 재난으로, 한곳에 정착하지 못하고 옮겨 다닙니다. 역마와 비슷하지만 역마가 외부요인이라면 지살은 스스로의 의지에 의한 이동입니다.',
    category: '신살'
  },
  '연살': {
    term: '연살',
    hanja: '年殺',
    hanjaBreakdown: '해 연(年), 죽일 살(殺)',
    shortDesc: '매력과 다재다능함 (도화)',
    longDesc: '복숭아꽃으로 매력, 인기, 화려함을 의미합니다. 예전에는 흉살로 봤지만 현대에서는 자기 PR 능력으로 유용하게 평가됩니다. 도화살과 같은 위치입니다.',
    category: '신살'
  },
  '월살': {
    term: '월살',
    hanja: '月殺',
    hanjaBreakdown: '달 월(月), 죽일 살(殺)',
    shortDesc: '고집과 병약함',
    longDesc: '학문궁 또는 고집살이라고도 합니다. 몸이 마르고 고갈된 상태로서 덕이 없어 고통을 겪습니다. 하는 일마다 성과를 얻기 힘들고 건강이 좋지 않습니다.',
    category: '신살'
  },
  '반안살': {
    term: '반안살',
    hanja: '攀鞍殺',
    hanjaBreakdown: '오를 반(攀), 안장 안(鞍), 죽일 살(殺)',
    shortDesc: '합격, 출세, 승진의 길신',
    longDesc: '말 안장 위에 올라탄다는 뜻으로, 장수가 전쟁에서 승리하여 개선하는 형상입니다. 12신살 중 가장 실리적인 성공과 성과를 뜻하며 길신입니다.',
    category: '신살'
  },
  '육해살': {
    term: '육해살',
    hanja: '六害殺',
    hanjaBreakdown: '여섯 육(六), 해할 해(害), 죽일 살(殺)',
    shortDesc: '육친 관련 어려움',
    longDesc: '부모, 형제, 부부, 자녀 등 가족에게 어려움이 생깁니다. 단, 눈치가 빠르고 민첩하며 임기응변과 위기 대처 능력이 뛰어납니다.',
    category: '신살'
  },
  // 추가 귀인/신살 (Phase 3)
  '천덕귀인': {
    term: '천덕귀인',
    hanja: '天德貴人',
    hanjaBreakdown: '하늘 천(天), 덕 덕(德), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '하늘의 은덕을 받는 귀인',
    longDesc: '하늘이 내려주는 은덕(隱德)의 성분입니다. 성정이 밝고 성실하며 관운이 좋고 무병장수합니다. 사흉신과 흉살을 감소시키는 귀인입니다.',
    category: '신살'
  },
  '월덕귀인': {
    term: '월덕귀인',
    hanja: '月德貴人',
    hanjaBreakdown: '달 월(月), 덕 덕(德), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '달의 덕을 받는 귀인',
    longDesc: '달의 덕을 입음으로써 명예, 품성과 관련된 귀인입니다. 천을귀인, 천덕귀인과 함께 명리학의 3대 귀인으로 불립니다.',
    category: '신살'
  },
  '양인살': {
    term: '양인살',
    hanja: '羊刃殺',
    hanjaBreakdown: '양 양(羊), 칼날 인(刃), 죽일 살(殺)',
    shortDesc: '날카로운 결단력의 별',
    longDesc: '칼날로 양털을 자르듯 가혹한 결단의 힘을 가집니다. 양간(陽干)일 경우에만 적용됩니다. 강한 결단력이 있지만 주변과 갈등이 생길 수 있습니다.',
    category: '신살'
  },
  '학당귀인': {
    term: '학당귀인',
    hanja: '學堂貴人',
    hanjaBreakdown: '배울 학(學), 집 당(堂), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '학문에 뛰어난 재능',
    longDesc: '학문에 재능이 있어 교육자나 교수 같은 직업에 적합합니다. 지혜와 총명함을 상징하며 연구, 교육 분야에서 두각을 나타냅니다.',
    category: '신살'
  },
  '금여록': {
    term: '금여록',
    hanja: '金輿祿',
    hanjaBreakdown: '쇠 금(金), 수레 여(輿), 복 록(祿)',
    shortDesc: '귀인의 수레, 배우자복',
    longDesc: '귀인의 수레를 의미하며 배우자복이나 이성운과 관련된 길신입니다. 명예와 부귀를 누리며 귀한 배우자를 만날 수 있습니다.',
    category: '신살'
  },
  '백호살': {
    term: '백호살',
    hanja: '白虎殺',
    hanjaBreakdown: '흰 백(白), 범 호(虎), 죽일 살(殺)',
    shortDesc: '예측 불가한 강한 살',
    longDesc: '부정적으로는 교통사고, 산업재해, 비명횡사를 의미하고, 긍정적으로는 특수한 재능, 전문적 능력, 강한 집중력과 끈기를 상징합니다.',
    category: '신살'
  },
  // 추가 신살 (24개)
  '공망살': {
    term: '공망살',
    hanja: '空亡殺',
    hanjaBreakdown: '빌 공(空), 없을 망(亡), 죽일 살(殺)',
    shortDesc: '빈 것, 허무, 노력이 물거품',
    longDesc: '60갑자 중 10일 단위(순)에서 빠진 두 지지가 공망입니다. 공망에 해당하는 지지는 힘이 약해지거나 없는 것처럼 작용합니다. 노력이 물거품이 될 수 있으나, 수행이나 종교적 깨달음에는 도움이 됩니다.',
    category: '신살'
  },
  '건록': {
    term: '건록',
    hanja: '建祿',
    hanjaBreakdown: '세울 건(建), 복 록(祿)',
    shortDesc: '녹을 세움, 안정적 기반',
    longDesc: '일간이 지지에서 녹을 만나는 것으로, 안정적인 수입과 기반을 의미합니다. 자수성가 타입으로 스스로의 능력으로 성공합니다. 직장운, 사업운이 좋습니다.',
    category: '신살'
  },
  '협록': {
    term: '협록',
    hanja: '挾祿',
    hanjaBreakdown: '끼일 협(挾), 복 록(祿)',
    shortDesc: '녹을 끼고 있음, 재물 도움',
    longDesc: '녹을 양옆에서 끼고 있는 형상으로, 재물이나 도움이 주변에서 옵니다. 협력자의 도움으로 재물을 얻거나 사업이 발전합니다.',
    category: '신살'
  },
  '천의귀인': {
    term: '천의귀인',
    hanja: '天醫貴人',
    hanjaBreakdown: '하늘 천(天), 의원 의(醫), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '의약/치료 재능, 건강 운',
    longDesc: '하늘의 의사라는 뜻으로, 의약, 치료, 건강과 관련된 재능이 있습니다. 의사, 간호사, 약사, 한의사 등 의료 관련 직업에 적합하며, 본인의 건강 운도 좋습니다.',
    category: '신살'
  },
  '암록귀인': {
    term: '암록귀인',
    hanja: '暗祿貴人',
    hanjaBreakdown: '어두울 암(暗), 복 록(祿), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '숨겨진 재물, 은밀한 도움',
    longDesc: '숨겨진 녹이라는 뜻으로, 겉으로 드러나지 않는 재물이나 은밀한 도움을 받습니다. 뜻밖의 재물이 생기거나 숨은 귀인이 나타납니다.',
    category: '신살'
  },
  '태극귀인': {
    term: '태극귀인',
    hanja: '太極貴人',
    hanjaBreakdown: '클 태(太), 다할 극(極), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '시작과 끝의 별, 리더십',
    longDesc: '태극은 만물의 시작과 끝을 주관합니다. 일의 시작과 마무리를 잘하며, 리더십이 있습니다. 조직의 수장이 되거나 창업에 유리합니다.',
    category: '신살'
  },
  '복성귀인': {
    term: '복성귀인',
    hanja: '福星貴人',
    hanjaBreakdown: '복 복(福), 별 성(星), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '복과 행운을 가져옴',
    longDesc: '복의 별이라는 뜻으로, 자연스럽게 복과 행운이 따릅니다. 어려운 상황에서도 운 좋게 빠져나가고, 좋은 기회가 찾아옵니다.',
    category: '신살'
  },
  '문곡귀인': {
    term: '문곡귀인',
    hanja: '文曲貴人',
    hanjaBreakdown: '글월 문(文), 곡조 곡(曲), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '문장력, 예술적 감각',
    longDesc: '문장과 음악의 별입니다. 글쓰기, 작곡, 예술적 표현에 뛰어난 재능이 있습니다. 작가, 음악가, 예술가에게 좋은 귀인입니다.',
    category: '신살'
  },
  '황은대사': {
    term: '황은대사',
    hanja: '皇恩大赦',
    hanjaBreakdown: '임금 황(皇), 은혜 은(恩), 클 대(大), 용서할 사(赦)',
    shortDesc: '황제의 은혜, 높은 지위',
    longDesc: '황제의 은혜로 대사면을 받는다는 뜻입니다. 높은 지위에 오르거나, 큰 어려움에서 벗어나게 됩니다. 권력자의 도움을 받습니다.',
    category: '신살'
  },
  '월공귀인': {
    term: '월공귀인',
    hanja: '月空貴人',
    hanjaBreakdown: '달 월(月), 빌 공(空), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '월의 공덕, 험난함을 피함',
    longDesc: '달의 빈자리가 귀인이 된다는 뜻으로, 위험이나 험난한 상황을 피해갑니다. 소송, 재난, 질병 등 흉한 일을 모면하는 데 도움이 됩니다.',
    category: '신살'
  },
  '재고귀인': {
    term: '재고귀인',
    hanja: '財庫貴人',
    hanjaBreakdown: '재물 재(財), 창고 고(庫), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '재물 창고, 부의 축적',
    longDesc: '재물의 창고가 있다는 뜻으로, 재물을 축적하는 능력이 뛰어납니다. 저축, 투자, 부동산 등에서 재물이 쌓입니다.',
    category: '신살'
  },
  '삼기귀인': {
    term: '삼기귀인',
    hanja: '三奇貴人',
    hanjaBreakdown: '석 삼(三), 기이할 기(奇), 귀할 귀(貴), 사람 인(人)',
    shortDesc: '세 개의 기이한 별, 특별한 재능',
    longDesc: '을병정(乙丙丁), 갑무경(甲戊庚), 임계기(壬癸己) 세 천간이 연속으로 나타나면 삼기귀인입니다. 특별한 재능과 기회를 의미하며, 매우 드문 귀인입니다.',
    category: '신살'
  },
  '천라지망살': {
    term: '천라지망살',
    hanja: '天羅地網殺',
    hanjaBreakdown: '하늘 천(天), 그물 라(羅), 땅 지(地), 그물 망(網), 죽일 살(殺)',
    shortDesc: '하늘/땅의 그물, 구속/제약',
    longDesc: '천라(天羅)는 술해(戌亥), 지망(地網)은 진사(辰巳)를 가리킵니다. 하늘과 땅의 그물에 걸린 형상으로, 구속되거나 제약을 받습니다. 법적 문제나 감옥과 관련될 수 있습니다.',
    category: '신살'
  },
  '현침살': {
    term: '현침살',
    hanja: '懸針殺',
    hanjaBreakdown: '매달 현(懸), 바늘 침(針), 죽일 살(殺)',
    shortDesc: '바늘에 걸림, 의료/기술직',
    longDesc: '바늘에 매달린다는 뜻으로, 정밀한 기술을 요하는 일과 관련됩니다. 의료(수술), 침술, 재봉, 미용 등 정밀 기술직에 재능이 있습니다.',
    category: '신살'
  },
  '효신살': {
    term: '효신살',
    hanja: '梟神殺',
    hanjaBreakdown: '올빼미 효(梟), 귀신 신(神), 죽일 살(殺)',
    shortDesc: '부모 상 또는 효도 문제',
    longDesc: '올빼미가 어미를 잡아먹는다는 옛 이야기에서 유래했습니다. 부모와의 인연이 박하거나 이른 이별이 있을 수 있습니다. 효도에 더 신경 써야 합니다.',
    category: '신살'
  },
  '십악대패살': {
    term: '십악대패살',
    hanja: '十惡大敗殺',
    hanjaBreakdown: '열 십(十), 악할 악(惡), 클 대(大), 패할 패(敗), 죽일 살(殺)',
    shortDesc: '10개 흉일주, 큰 재앙',
    longDesc: '갑진, 을사, 임신, 병신, 정해, 무술, 무진, 계해, 경진, 신사 일주가 해당됩니다. 큰 실패나 재앙을 의미하지만, 오히려 극적인 성공을 이루는 경우도 있습니다.',
    category: '신살'
  },
  '급각살': {
    term: '급각살',
    hanja: '急脚殺',
    hanjaBreakdown: '급할 급(急), 다리 각(脚), 죽일 살(殺)',
    shortDesc: '다리 부상, 이동 장애',
    longDesc: '급하게 다리를 다친다는 뜻으로, 하지(下肢) 부상이나 이동에 장애가 생길 수 있습니다. 교통사고, 낙상 등에 주의해야 합니다.',
    category: '신살'
  },
  '탕화살': {
    term: '탕화살',
    hanja: '湯火殺',
    hanjaBreakdown: '끓는물 탕(湯), 불 화(火), 죽일 살(殺)',
    shortDesc: '뜨거운 물/불 관련 사고',
    longDesc: '끓는 물이나 불과 관련된 사고를 의미합니다. 화상, 폭발, 화재 등에 주의해야 합니다. 요리, 용접 등 불을 다루는 직업에서는 특히 조심해야 합니다.',
    category: '신살'
  },
  '낙정관살': {
    term: '낙정관살',
    hanja: '落井關殺',
    hanjaBreakdown: '떨어질 낙(落), 우물 정(井), 빗장 관(關), 죽일 살(殺)',
    shortDesc: '우물에 빠짐, 물 관련 사고',
    longDesc: '우물에 빠지는 것처럼 물과 관련된 사고를 의미합니다. 익사, 침수, 수해 등에 주의해야 합니다. 수영, 낚시 등 물과 관련된 활동에서 조심해야 합니다.',
    category: '신살'
  },
  '고란살': {
    term: '고란살',
    hanja: '孤鸞殺',
    hanjaBreakdown: '외로울 고(孤), 난새 란(鸞), 죽일 살(殺)',
    shortDesc: '외로움, 배우자 복 약함',
    longDesc: '외로운 난새라는 뜻으로, 배우자를 만나기 어렵거나 만나더라도 인연이 박할 수 있습니다. 결혼 후에도 외로움을 느끼기 쉽습니다.',
    category: '신살'
  },
  '고신살': {
    term: '고신살',
    hanja: '孤辰殺',
    hanjaBreakdown: '외로울 고(孤), 별 신(辰), 죽일 살(殺)',
    shortDesc: '남자 고독, 배우자 이별',
    longDesc: '외로운 별이라는 뜻으로, 주로 남자에게 적용됩니다. 배우자와의 이별이나 만혼, 독신의 운명이 있을 수 있습니다. 과숙살과 함께 고과살로 불립니다.',
    category: '신살'
  },
  '과숙살': {
    term: '과숙살',
    hanja: '寡宿殺',
    hanjaBreakdown: '홀로 과(寡), 잘 숙(宿), 죽일 살(殺)',
    shortDesc: '여자 고독, 배우자 이별',
    longDesc: '홀로 사는 별이라는 뜻으로, 주로 여자에게 적용됩니다. 배우자와의 이별이나 만혼, 독신의 운명이 있을 수 있습니다. 고신살과 함께 고과살로 불립니다.',
    category: '신살'
  },
  '상문살': {
    term: '상문살',
    hanja: '喪門殺',
    hanjaBreakdown: '초상 상(喪), 문 문(門), 죽일 살(殺)',
    shortDesc: '상복, 장례 관련',
    longDesc: '상을 치르는 문이라는 뜻으로, 가까운 사람의 죽음이나 장례와 관련됩니다. 슬픈 일이 생기거나 조문을 가게 됩니다.',
    category: '신살'
  },
  '조객살': {
    term: '조객살',
    hanja: '弔客殺',
    hanjaBreakdown: '조문할 조(弔), 손님 객(客), 죽일 살(殺)',
    shortDesc: '조문객, 조의금',
    longDesc: '조문하러 오는 손님이라는 뜻으로, 상문과 반대 방향에서 작용합니다. 조문을 가거나 조의금을 쓸 일이 생깁니다. 슬픈 소식을 접하게 됩니다.',
    category: '신살'
  },
};

// 합충 관련 용어
const HAPCHUNG_GLOSSARY: Record<string, GlossaryEntry> = {
  '천간합': {
    term: '천간합',
    hanja: '天干合',
    hanjaBreakdown: '하늘 천(天), 줄기 간(干), 합할 합(合)',
    shortDesc: '두 천간이 합쳐져 새로운 오행 생성',
    longDesc: '두 천간이 만나 새로운 오행으로 변하는 것입니다. 갑기합토, 을경합금, 병신합수, 정임합목, 무계합화가 있습니다.',
    category: '합충'
  },
  '지지육합': {
    term: '지지육합',
    hanja: '地支六合',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 여섯 육(六), 합할 합(合)',
    shortDesc: '두 지지가 합쳐져 새로운 오행 생성',
    longDesc: '두 지지가 만나 새로운 오행으로 변하는 것입니다. 자축합토, 인해합목, 묘술합화, 진유합금, 사신합수, 오미합화가 있습니다.',
    category: '합충'
  },
  '지지삼합': {
    term: '지지삼합',
    hanja: '地支三合',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 석 삼(三), 합할 합(合)',
    shortDesc: '세 지지가 합쳐져 오행국 형성',
    longDesc: '세 지지가 만나 완전한 오행국을 이루는 것입니다. 신자진 수국, 인오술 화국, 사유축 금국, 해묘미 목국이 있습니다.',
    category: '합충'
  },
  '지지방합': {
    term: '지지방합',
    hanja: '地支方合',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 모 방(方), 합할 합(合)',
    shortDesc: '같은 계절(방위)의 세 지지가 합함',
    longDesc: '같은 계절의 세 지지가 만나 합을 이루는 것입니다. 인묘진 동방목국, 사오미 남방화국, 신유술 서방금국, 해자축 북방수국이 있습니다.',
    category: '합충'
  },
  '지지충': {
    term: '지지충',
    hanja: '地支沖',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 부딪칠 충(沖)',
    shortDesc: '서로 마주보는 두 지지가 충돌',
    longDesc: '12지지 원에서 서로 마주보는 두 지지가 충돌하는 것입니다. 자오충, 축미충, 인신충, 묘유충, 진술충, 사해충이 있습니다.',
    category: '합충'
  },
  '지지형': {
    term: '지지형',
    hanja: '地支刑',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 형벌 형(刑)',
    shortDesc: '지지 간 형벌 관계',
    longDesc: '지지 간에 형벌이 되는 관계입니다. 인사신 삼형(무은지형), 축술미 삼형(무례지형), 자묘형(무례지형), 자형(진진, 오오, 유유, 해해)이 있습니다.',
    category: '합충'
  },
  '지지파': {
    term: '지지파',
    hanja: '地支破',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 깨뜨릴 파(破)',
    shortDesc: '지지 간 깨뜨리는 관계',
    longDesc: '지지 간에 서로 깨뜨리는 관계입니다. 자유파, 축진파, 인해파, 묘오파, 사신파, 미술파가 있습니다.',
    category: '합충'
  },
  '지지해': {
    term: '지지해',
    hanja: '地支害',
    hanjaBreakdown: '땅 지(地), 가지 지(支), 해할 해(害)',
    shortDesc: '지지 간 해치는 관계',
    longDesc: '지지 간에 서로 해치는 관계입니다. 자미해, 축오해, 인사해, 묘진해, 신해해, 유술해가 있습니다. 육해(六害)라고도 합니다.',
    category: '합충'
  },
  '공망': {
    term: '공망',
    hanja: '空亡',
    hanjaBreakdown: '빌 공(空), 없을 망(亡)',
    shortDesc: '비어서 없음, 순에서 빠진 지지',
    longDesc: '60갑자 중 10일 단위(순)에서 빠진 두 지지입니다. 공망에 든 지지는 힘이 약해지거나 없는 것처럼 작용합니다.',
    category: '합충'
  },
};

// 일반 용어
const GENERAL_GLOSSARY: Record<string, GlossaryEntry> = {
  '용신': {
    term: '용신',
    hanja: '用神',
    hanjaBreakdown: '쓸 용(用), 귀신 신(神)',
    shortDesc: '내 인생에 도움을 주는 기운',
    longDesc: '용신은 내가 사용하는 신, 혹은 기운이라는 뜻으로 내 인생에 도움을 주는 기운을 뜻합니다. 억부용신, 조후용신, 통관용신 등이 있습니다.',
    category: '용어'
  },
  '희신': {
    term: '희신',
    hanja: '喜神',
    hanjaBreakdown: '기쁠 희(喜), 귀신 신(神)',
    shortDesc: '용신을 도와주는 기운',
    longDesc: '용신을 생해주거나 보조하는 기운입니다. 용신 다음으로 좋은 기운이며, 용신과 함께 작용할 때 더 좋은 효과를 냅니다.',
    category: '용어'
  },
  '기신': {
    term: '기신',
    hanja: '忌神',
    hanjaBreakdown: '꺼릴 기(忌), 귀신 신(神)',
    shortDesc: '내 인생에 해가 되는 기운',
    longDesc: '용신을 극하거나 방해하는 기운입니다. 기신이 오는 시기에는 어려움이 있을 수 있으므로 조심해야 합니다.',
    category: '용어'
  },
  '신강': {
    term: '신강',
    hanja: '身强',
    hanjaBreakdown: '몸 신(身), 강할 강(强)',
    shortDesc: '일간의 힘이 강한 상태',
    longDesc: '사주에서 일간(나)을 돕는 기운(비겁, 인성)이 많아 일간이 강한 상태입니다. 주체성이 강하고 남의 말을 잘 듣지 않습니다.',
    category: '용어'
  },
  '신약': {
    term: '신약',
    hanja: '身弱',
    hanjaBreakdown: '몸 신(身), 약할 약(弱)',
    shortDesc: '일간의 힘이 약한 상태',
    longDesc: '사주에서 일간(나)을 극하는 기운(관살, 재성, 식상)이 많아 일간이 약한 상태입니다. 타인의 영향을 많이 받습니다.',
    category: '용어'
  },
  '중화': {
    term: '중화',
    hanja: '中和',
    hanjaBreakdown: '가운데 중(中), 화할 화(和)',
    shortDesc: '균형잡힌 상태',
    longDesc: '오행이 균형을 이루어 한쪽으로 치우치지 않은 상태입니다. 가장 이상적인 사주 구성으로 여겨집니다.',
    category: '용어'
  },
  '대운': {
    term: '대운',
    hanja: '大運',
    hanjaBreakdown: '클 대(大), 움직일 운(運)',
    shortDesc: '10년 단위의 운의 흐름',
    longDesc: '10년 단위로 바뀌는 큰 운의 흐름입니다. 대운의 천간과 지지가 사주 원국과 어떤 관계인지에 따라 운의 길흉이 결정됩니다.',
    category: '용어'
  },
  '세운': {
    term: '세운',
    hanja: '歲運',
    hanjaBreakdown: '해 세(歲), 움직일 운(運)',
    shortDesc: '매년의 운의 흐름',
    longDesc: '한 해 한 해의 운입니다. 그 해의 간지가 사주 원국 및 대운과 어떤 관계인지에 따라 그 해의 운이 결정됩니다.',
    category: '용어'
  },
  '지장간': {
    term: '지장간',
    hanja: '地藏干',
    hanjaBreakdown: '땅 지(地), 감출 장(藏), 줄기 간(干)',
    shortDesc: '지지 속에 숨겨진 천간',
    longDesc: '12지지 각각 안에 숨어 있는 천간들입니다. 초기, 중기, 본기(정기)로 나뉘며, 사주 해석에서 숨은 요소를 보는 데 사용됩니다.',
    category: '용어'
  },
  '물상': {
    term: '물상',
    hanja: '物象',
    hanjaBreakdown: '물건 물(物), 모양 상(象)',
    shortDesc: '오행이 상징하는 구체적 사물',
    longDesc: '오행이나 십성이 실제로 상징하는 구체적인 사물이나 이미지입니다. 예를 들어 갑목은 큰 나무, 정화는 촛불을 물상으로 합니다.',
    category: '용어'
  },
  '일간': {
    term: '일간',
    hanja: '日干',
    hanjaBreakdown: '날 일(日), 줄기 간(干)',
    shortDesc: '일주의 천간, 나 자신',
    longDesc: '태어난 날의 천간으로, 사주에서 나 자신을 의미합니다. 모든 사주 해석의 기준점이 됩니다.',
    category: '용어'
  },
  '월령': {
    term: '월령',
    hanja: '月令',
    hanjaBreakdown: '달 월(月), 명령 령(令)',
    shortDesc: '태어난 달의 계절 기운',
    longDesc: '태어난 달(월지)이 나타내는 계절의 기운입니다. 일간이 월령을 얻었는지(득령) 여부가 신강/신약 판단에 중요합니다.',
    category: '용어'
  },
};

// 섹션 제목 용어 (모달 설명용)
const SECTION_GLOSSARY: Record<string, GlossaryEntry> = {
  '신살': {
    term: '신살',
    hanja: '神殺',
    hanjaBreakdown: '귀신 신(神), 죽일 살(殺)',
    shortDesc: '사주에 영향을 미치는 특별한 별',
    longDesc: '신살은 사주의 특정 조합에서 나타나는 길흉의 작용입니다. 천을귀인처럼 좋은 귀인도 있고, 도화살처럼 이중적 성격의 살도 있습니다. 신살은 사주 해석의 보조 도구로 활용되며, 원국의 오행 균형이 더 중요합니다.',
    category: '용어'
  },
  '오행분포': {
    term: '오행분포',
    hanja: '五行分布',
    hanjaBreakdown: '다섯 오(五), 다닐 행(行), 나눌 분(分), 펼 포(布)',
    shortDesc: '목화토금수 다섯 기운의 분포',
    longDesc: '오행분포는 사주팔자에서 목(木), 화(火), 토(土), 금(金), 수(水) 다섯 가지 기운이 어떻게 분포되어 있는지를 보여줍니다. 균형 잡힌 오행이 좋으나, 치우침이 있더라도 그것이 곧 나쁜 것은 아닙니다. 용신을 통해 부족한 오행을 보완할 수 있습니다.',
    category: '용어'
  },
  '십성분포': {
    term: '십성분포',
    hanja: '十星分布',
    hanjaBreakdown: '열 십(十), 별 성(星), 나눌 분(分), 펼 포(布)',
    shortDesc: '열 가지 십성의 분포',
    longDesc: '십성은 일간을 기준으로 다른 천간/지지와의 관계를 나타냅니다. 비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인의 10가지가 있으며, 각 십성의 분포를 통해 성격과 운명의 경향을 파악합니다.',
    category: '용어'
  },
  '신강신약': {
    term: '신강신약',
    hanja: '身强身弱',
    hanjaBreakdown: '몸 신(身), 강할 강(强), 몸 신(身), 약할 약(弱)',
    shortDesc: '일간의 힘이 강한지 약한지',
    longDesc: '신강/신약 지수는 사주에서 일간(나)의 힘이 얼마나 강한지를 수치화한 것입니다. 일간을 돕는 비겁과 인성이 많으면 신강, 일간을 극하거나 빼앗는 관살과 재성, 식상이 많으면 신약입니다. 신강은 주체적이고 독립적인 성향, 신약은 협력적이고 유연한 성향을 보입니다.',
    category: '용어'
  },
  '대운': {
    term: '대운',
    hanja: '大運',
    hanjaBreakdown: '클 대(大), 움직일 운(運)',
    shortDesc: '10년 단위의 운의 흐름',
    longDesc: '대운은 10년 단위로 바뀌는 큰 운의 흐름입니다. 월주를 기준으로 순행 또는 역행하며, 각 대운의 천간과 지지가 사주 원국과 어떤 관계를 맺는지에 따라 그 10년간의 운세가 결정됩니다. 대운은 인생의 큰 방향을 좌우합니다.',
    category: '용어'
  },
  '연운': {
    term: '연운',
    hanja: '年運',
    hanjaBreakdown: '해 년(年), 움직일 운(運)',
    shortDesc: '매년의 운의 흐름',
    longDesc: '연운(세운)은 매년 바뀌는 운입니다. 그 해의 간지(예: 2024년 갑진)가 사주 원국 및 대운과 어떤 관계를 맺는지에 따라 한 해의 운세가 결정됩니다. 대운 안에서의 세부적인 길흉을 파악할 수 있습니다.',
    category: '용어'
  },
  '월운': {
    term: '월운',
    hanja: '月運',
    hanjaBreakdown: '달 월(月), 움직일 운(運)',
    shortDesc: '매월의 운의 흐름',
    longDesc: '월운은 매월 바뀌는 운입니다. 절기를 기준으로 월이 바뀌며, 해당 월의 간지가 사주와 어떤 관계를 맺는지에 따라 그 달의 운세가 결정됩니다. 더 세밀한 시점의 길흉을 파악하는 데 사용됩니다.',
    category: '용어'
  },
  '일운': {
    term: '일운',
    hanja: '日運',
    hanjaBreakdown: '날 일(日), 움직일 운(運)',
    shortDesc: '매일의 운의 흐름',
    longDesc: '일운은 매일 바뀌는 운입니다. 그날의 일진(간지)이 사주 원국과 어떤 관계를 맺는지에 따라 하루의 운세가 결정됩니다. 가장 세밀한 시점의 길흉을 파악하는 데 사용되며, 중요한 일정을 잡을 때 참고합니다.',
    category: '용어'
  },
};

// 전체 용어 사전 통합
export const SAJU_GLOSSARY: Record<string, GlossaryEntry> = {
  ...CHEONGAN_GLOSSARY,
  ...JIJI_GLOSSARY,
  ...SIPSEONG_GLOSSARY,
  ...SIBIUNSEONG_GLOSSARY,
  ...SINSAL_GLOSSARY,
  ...HAPCHUNG_GLOSSARY,
  ...GENERAL_GLOSSARY,
  ...SECTION_GLOSSARY,
};

// 카테고리별 용어 목록 조회
export const getGlossaryByCategory = (category: GlossaryEntry['category']): GlossaryEntry[] => {
  return Object.values(SAJU_GLOSSARY).filter(entry => entry.category === category);
};

// 용어 검색
export const searchGlossary = (query: string): GlossaryEntry[] => {
  const lowerQuery = query.toLowerCase();
  return Object.values(SAJU_GLOSSARY).filter(
    entry =>
      entry.term.toLowerCase().includes(lowerQuery) ||
      entry.hanja.includes(query) ||
      entry.shortDesc.toLowerCase().includes(lowerQuery)
  );
};

// 용어 조회
export const getGlossaryEntry = (term: string): GlossaryEntry | undefined => {
  return SAJU_GLOSSARY[term];
};

export default SAJU_GLOSSARY;
