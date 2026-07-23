'use client';

import { useState, useEffect, useCallback, useRef, useId } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Button, Input, Icon, GlassCard } from '@/components/ui';
import { calculateManseol, searchCities, type City } from '@/lib/api/manseol';
import { useSajuStore } from '@/stores/sajuStore';
import type { ManseolRequest } from '@/types/saju';

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

export function BirthInfoForm() {
  const router = useRouter();
  const { setResult, setLoading, setError, isLoading } = useSajuStore();

  const [formData, setFormData] = useState<ManseolRequest>({
    name: '',
    birth_date: '',
    birth_time: '',
    city: '',
    gender: 'male',
    calendar: 'solar',
  });

  const [cities, setCities] = useState<City[]>([]);
  const [cityQuery, setCityQuery] = useState('');
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  // 키보드 활성 옵션 인덱스(-1 = 없음). ARIA combobox의 aria-activedescendant를 구동한다.
  const [activeIndex, setActiveIndex] = useState(-1);
  const cityListboxId = useId();
  const cityListRef = useRef<HTMLUListElement>(null);
  const optionId = (index: number) => `${cityListboxId}-opt-${index}`;
  // 도시 목록이 백엔드가 아닌 오프라인 폴백에서 온 경우 표시(주요 도시만 제공됨을 안내)
  const [citiesFallback, setCitiesFallback] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [timeUnknown, setTimeUnknown] = useState(false);

  // Debounce search query
  const debouncedQuery = useDebounce(cityQuery, 300);

  // 도시 검색
  const handleCitySearch = useCallback(async (query: string) => {
    setIsSearching(true);
    try {
      const { cities: results, isFallback } = await searchCities(query, 15);
      setCities(results);
      setCitiesFallback(isFallback);
    } catch (err) {
      console.error('Failed to search cities:', err);
      setCities([]);
      setCitiesFallback(false);
    } finally {
      setIsSearching(false);
    }
  }, []);

  // debounced query가 변경될 때 검색 수행
  useEffect(() => {
    if (debouncedQuery.length >= 1) {
      handleCitySearch(debouncedQuery);
    } else if (debouncedQuery.length === 0 && showCityDropdown) {
      // 빈 검색어일 때 인기 도시 표시
      handleCitySearch('');
    }
  }, [debouncedQuery, showCityDropdown, handleCitySearch]);

  // 결과 집합이 바뀌면 키보드 활성 항목을 초기화(엉뚱한 옵션이 강조된 채 남지 않게)
  useEffect(() => {
    setActiveIndex(-1);
  }, [cities]);

  // 키보드로 이동한 활성 옵션을 항상 보이도록 스크롤
  useEffect(() => {
    if (activeIndex < 0 || !cityListRef.current) return;
    const el = cityListRef.current.querySelector<HTMLElement>(`#${CSS.escape(optionId(activeIndex))}`);
    el?.scrollIntoView({ block: 'nearest' });
    // optionId는 cityListboxId만 의존하는 안정 함수라 deps에 넣지 않는다
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex]);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = '이름을 입력해주세요';
    }

    if (!formData.birth_date) {
      newErrors.birth_date = '생년월일을 입력해주세요';
    } else {
      // 생년월일 범위 가드 (미래/과도하게 과거 차단)
      const birth = new Date(formData.birth_date);
      const today = new Date();
      const minDate = new Date('1900-01-01');
      if (birth > today) {
        newErrors.birth_date = '미래 날짜는 입력할 수 없습니다';
      } else if (birth < minDate) {
        newErrors.birth_date = '1900년 이후 날짜를 입력해주세요';
      }
    }

    if (!formData.city) {
      newErrors.city = '출생 도시를 선택해주세요';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    // setError 는 isLoading:false 를 함께 세팅한다(sajuStore.ts) — 순서가 뒤집히면
    // 방금 켠 로딩 플래그를 즉시 꺼서 LoadingOverlay 가 영영 뜨지 않는다.
    setError(null);
    setLoading(true);

    try {
      const result = await calculateManseol(formData);
      setResult(result);
      router.push('/result');
    } catch (err) {
      setError(err instanceof Error ? err.message : '계산 중 오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  const handleCitySelect = (city: City) => {
    setFormData((prev) => ({ ...prev, city: city.name })); // 영어 이름으로 API 전송
    // 한글 이름 우선 표시 (없으면 영어)
    const displayCity = city.name_ko || city.name;
    const displayCountry = city.country_ko || city.country;
    setCityQuery(`${displayCity}, ${displayCountry}`);
    setShowCityDropdown(false);
    setActiveIndex(-1);
    setErrors((prev) => ({ ...prev, city: '' }));
  };

  // ARIA combobox 키보드 인터랙션: 방향키로 활성 옵션 이동, Enter 선택, Escape 닫기.
  // 활성 옵션은 aria-activedescendant로 가리키므로 DOM 포커스는 입력에 머문다 —
  // 옵션 버튼으로 Tab 이동하면서 onBlur 타이머가 옵션을 언마운트하던 결함을 제거한다.
  const handleCityKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (!showCityDropdown) {
        setShowCityDropdown(true);
        if (cities.length === 0) handleCitySearch('');
        return;
      }
      if (cities.length > 0) {
        setActiveIndex((prev) => (prev + 1) % cities.length);
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (cities.length > 0) {
        setActiveIndex((prev) => (prev <= 0 ? cities.length - 1 : prev - 1));
      }
    } else if (e.key === 'Enter') {
      // 드롭다운이 열려 있으면 폼 제출 대신 옵션 선택으로 가로챈다.
      if (showCityDropdown && cities.length > 0) {
        e.preventDefault();
        if (activeIndex >= 0) handleCitySelect(cities[activeIndex]);
      }
    } else if (e.key === 'Escape') {
      if (showCityDropdown) {
        e.preventDefault();
        setShowCityDropdown(false);
        setActiveIndex(-1);
      }
    } else if (e.key === 'Home' && showCityDropdown && cities.length > 0) {
      e.preventDefault();
      setActiveIndex(0);
    } else if (e.key === 'End' && showCityDropdown && cities.length > 0) {
      e.preventDefault();
      setActiveIndex(cities.length - 1);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      <GlassCard className="w-full max-w-xl mx-auto p-6 md:p-8">
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Name */}
          <Input
            label="이름"
            placeholder="홍길동"
            value={formData.name}
            onChange={(e) => {
              setFormData((prev) => ({ ...prev, name: e.target.value }));
              setErrors((prev) => ({ ...prev, name: '' }));
            }}
            error={errors.name}
          />

          {/* Birth Date */}
          <Input
            label="생년월일"
            type="date"
            value={formData.birth_date}
            onChange={(e) => {
              setFormData((prev) => ({ ...prev, birth_date: e.target.value }));
              setErrors((prev) => ({ ...prev, birth_date: '' }));
            }}
            error={errors.birth_date}
          />

          {/* Birth Time (Optional) */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-sm font-medium text-foreground">출생시간</label>
              <label className="flex items-center gap-1.5 text-sm text-muted-foreground cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={timeUnknown}
                  onChange={(e) => {
                    const checked = e.target.checked;
                    setTimeUnknown(checked);
                    if (checked) {
                      setFormData((prev) => ({ ...prev, birth_time: '' }));
                    }
                  }}
                  className="accent-primary"
                />
                시간 모름 (時不知)
              </label>
            </div>
            <Input
              type="time"
              value={formData.birth_time}
              disabled={timeUnknown}
              className={timeUnknown ? 'opacity-50 cursor-not-allowed' : ''}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, birth_time: e.target.value }))
              }
            />
            <p className="mt-1 text-xs text-muted-foreground">
              {timeUnknown
                ? '시주(時柱) 없이 분석합니다. 시간 관련 해석의 정확도는 낮아질 수 있어요.'
                : '정확한 출생시각은 사주 정확도를 크게 높입니다. 해외 출생·서머타임은 도시 기준으로 자동 보정됩니다.'}
            </p>
          </div>

          {/* City Autocomplete (ARIA combobox + listbox) */}
          <div className="relative">
            <Input
              label="출생 도시"
              placeholder="서울, 도쿄, 뉴욕..."
              value={cityQuery}
              role="combobox"
              aria-expanded={showCityDropdown}
              aria-controls={showCityDropdown ? cityListboxId : undefined}
              aria-autocomplete="list"
              aria-activedescendant={
                showCityDropdown && activeIndex >= 0 ? optionId(activeIndex) : undefined
              }
              autoComplete="off"
              onKeyDown={handleCityKeyDown}
              onChange={(e) => {
                setCityQuery(e.target.value);
                setShowCityDropdown(true);
                setFormData((prev) => ({ ...prev, city: '' }));
              }}
              onFocus={() => {
                setShowCityDropdown(true);
                if (cities.length === 0) {
                  handleCitySearch('');
                }
              }}
              onBlur={() => {
                // 포인터가 옵션을 클릭할 틈을 주려 약간 지연(옵션은 onMouseDown에서
                // preventDefault로 blur 자체를 막지만, 그 밖으로 blur될 때의 폴백)
                setTimeout(() => {
                  setShowCityDropdown(false);
                  setActiveIndex(-1);
                }, 200);
              }}
              error={errors.city}
            />
            {showCityDropdown && (
              <div className="absolute z-50 w-full mt-1 bg-surface border border-border rounded-xl shadow-card-hover overflow-hidden max-h-60 overflow-y-auto">
                {isSearching ? (
                  <div className="px-4 py-3 text-muted-foreground text-center" role="status">
                    <Icon name="solar:refresh-linear" size={16} className="animate-spin inline mr-2" />
                    검색 중...
                  </div>
                ) : cities.length > 0 ? (
                  <>
                    {citiesFallback && (
                      <div className="px-4 py-2 text-xs text-muted-foreground border-b border-border">
                        오프라인 기본 도시 목록입니다 (주요 도시만 제공)
                      </div>
                    )}
                    <ul
                      ref={cityListRef}
                      id={cityListboxId}
                      role="listbox"
                      aria-label="출생 도시 검색 결과"
                    >
                      {cities.map((city, index) => {
                        const active = index === activeIndex;
                        return (
                          <li
                            key={`${city.name}-${city.country}`}
                            id={optionId(index)}
                            role="option"
                            aria-selected={active}
                            data-active={active}
                            // onMouseDown preventDefault: 클릭 시 입력의 blur(→드롭다운 닫힘)보다
                            // 먼저 선택이 확정되게 한다
                            onMouseDown={(e) => e.preventDefault()}
                            onClick={() => handleCitySelect(city)}
                            onMouseEnter={() => setActiveIndex(index)}
                            className={`px-4 py-2 text-left cursor-pointer transition-colors ${
                              active ? 'bg-muted text-accent font-medium' : 'text-foreground'
                            }`}
                          >
                            {city.name_ko || city.name}, {city.country_ko || city.country}
                          </li>
                        );
                      })}
                    </ul>
                  </>
                ) : cityQuery.length > 0 ? (
                  <div className="px-4 py-3 text-muted-foreground text-center" role="status">
                    검색 결과가 없습니다
                  </div>
                ) : null}
              </div>
            )}
          </div>

          {/* Inline option pills: gender + calendar */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-sm font-medium text-muted-foreground mr-1">성별</span>
            {(['male', 'female'] as const).map((gender) => {
              const selected = formData.gender === gender;
              return (
                <button
                  key={gender}
                  type="button"
                  aria-pressed={selected}
                  className={`focus-ring inline-flex min-h-11 items-center gap-1.5 px-4 rounded-full text-sm border transition-all ${
                    selected
                      ? 'bg-primary/10 border-accent text-accent font-semibold'
                      : 'bg-surface border-border text-muted-foreground hover:bg-muted'
                  }`}
                  onClick={() => setFormData((prev) => ({ ...prev, gender }))}
                >
                  <Icon
                    name={gender === 'male' ? 'solar:men-linear' : 'solar:women-linear'}
                    size={15}
                  />
                  {gender === 'male' ? '남성' : '여성'}
                  {/* 색 외 선택 신호 (색각 이상·저대비 환경 대비) */}
                  {selected && <Icon name="solar:check-circle-linear" size={14} />}
                </button>
              );
            })}

            <span className="text-sm font-medium text-muted-foreground mx-1">달력</span>
            {(['solar', 'lunar', 'leap_lunar'] as const).map((type) => {
              const selected = formData.calendar === type;
              return (
                <button
                  key={type}
                  type="button"
                  aria-pressed={selected}
                  className={`focus-ring inline-flex min-h-11 items-center gap-1.5 px-4 rounded-full text-sm border transition-all ${
                    selected
                      ? 'bg-primary/10 border-accent text-accent font-semibold'
                      : 'bg-surface border-border text-muted-foreground hover:bg-muted'
                  }`}
                  onClick={() => setFormData((prev) => ({ ...prev, calendar: type }))}
                >
                  {type === 'solar' ? '양력' : type === 'lunar' ? '음력' : '윤달'}
                  {selected && <Icon name="solar:check-circle-linear" size={14} />}
                </button>
              );
            })}
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            className="w-full mt-2"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Icon name="solar:refresh-linear" size={20} className="animate-spin mr-2" />
                분석 중...
              </>
            ) : (
              <>
                <Icon name="solar:stars-linear" size={20} className="mr-2" />
                사주 분석하기
              </>
            )}
          </Button>
        </form>
      </GlassCard>
    </motion.div>
  );
}
