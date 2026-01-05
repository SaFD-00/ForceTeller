'use client';

import { useState, useEffect, useCallback } from 'react';
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
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Debounce search query
  const debouncedQuery = useDebounce(cityQuery, 300);

  // 도시 검색
  const handleCitySearch = useCallback(async (query: string) => {
    setIsSearching(true);
    try {
      const results = await searchCities(query, 15);
      setCities(results);
    } catch (err) {
      console.error('Failed to search cities:', err);
      setCities([]);
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

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = '이름을 입력해주세요';
    }

    if (!formData.birth_date) {
      newErrors.birth_date = '생년월일을 입력해주세요';
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

    setLoading(true);
    setError(null);

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
    setErrors((prev) => ({ ...prev, city: '' }));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      <GlassCard className="w-full max-w-md mx-auto p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            사주명리
          </h1>
          <p className="text-white/60">
            정확한 사주팔자 분석을 시작하세요
          </p>
        </div>

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
          <Input
            label="출생시간"
            type="time"
            value={formData.birth_time}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, birth_time: e.target.value }))
            }
          />

          {/* City Autocomplete */}
          <div className="relative">
            <Input
              label="출생 도시"
              placeholder="서울, 도쿄, 뉴욕..."
              value={cityQuery}
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
                // 드롭다운 클릭을 위해 약간의 지연
                setTimeout(() => setShowCityDropdown(false), 200);
              }}
              error={errors.city}
            />
            {showCityDropdown && (
              <div className="absolute z-50 w-full mt-1 bg-black/95 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden max-h-60 overflow-y-auto">
                {isSearching ? (
                  <div className="px-4 py-3 text-white/50 text-center">
                    <Icon name="solar:refresh-bold" size={16} className="animate-spin inline mr-2" />
                    검색 중...
                  </div>
                ) : cities.length > 0 ? (
                  cities.map((city) => (
                    <button
                      key={`${city.name}-${city.country}`}
                      type="button"
                      className="w-full px-4 py-2 text-left text-white/80 hover:bg-white/10 transition-colors"
                      onClick={() => handleCitySelect(city)}
                    >
                      {city.name_ko || city.name}, {city.country_ko || city.country}
                    </button>
                  ))
                ) : cityQuery.length > 0 ? (
                  <div className="px-4 py-3 text-white/50 text-center">
                    검색 결과가 없습니다
                  </div>
                ) : null}
              </div>
            )}
          </div>

          {/* Gender */}
          <div>
            <label className="block text-sm font-medium text-white/70 mb-3">
              성별
            </label>
            <div className="flex gap-4">
              {(['male', 'female'] as const).map((gender) => (
                <button
                  key={gender}
                  type="button"
                  className={`flex-1 py-3 rounded-xl border transition-all duration-300 ${
                    formData.gender === gender
                      ? 'bg-primary/20 border-primary text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:bg-white/10'
                  }`}
                  onClick={() =>
                    setFormData((prev) => ({ ...prev, gender }))
                  }
                >
                  <Icon
                    name={gender === 'male' ? 'solar:men-bold' : 'solar:women-bold'}
                    size={20}
                    className="inline mr-2"
                  />
                  {gender === 'male' ? '남성' : '여성'}
                </button>
              ))}
            </div>
          </div>

          {/* Calendar Type */}
          <div>
            <label className="block text-sm font-medium text-white/70 mb-3">
              달력 유형
            </label>
            <div className="flex gap-2">
              {(['solar', 'lunar', 'leap_lunar'] as const).map((type) => (
                <button
                  key={type}
                  type="button"
                  className={`flex-1 py-2 rounded-lg text-sm border transition-all duration-300 ${
                    formData.calendar === type
                      ? 'bg-primary/20 border-primary text-white'
                      : 'bg-white/5 border-white/10 text-white/60 hover:bg-white/10'
                  }`}
                  onClick={() =>
                    setFormData((prev) => ({ ...prev, calendar: type }))
                  }
                >
                  {type === 'solar' ? '양력' : type === 'lunar' ? '음력' : '윤달'}
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            className="w-full mt-6"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Icon name="solar:refresh-bold" size={20} className="animate-spin mr-2" />
                분석 중...
              </>
            ) : (
              <>
                <Icon name="solar:stars-bold" size={20} className="mr-2" />
                사주 분석하기
              </>
            )}
          </Button>
        </form>
      </GlassCard>
    </motion.div>
  );
}
