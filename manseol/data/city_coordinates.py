"""
도시별 경위도 데이터
geonamescache를 사용한 전세계 도시 지원 + 한글 지원
"""

import re

from geonamescache import GeonamesCache

from .korean_names import get_korean_city_name, get_korean_country_name

# GeonamesCache 인스턴스 (싱글톤)
_gc = GeonamesCache()
_cities_cache: dict | None = None
_countries_cache: dict | None = None
_korean_search_index: dict[str, list[str]] | None = None

# 한글 문자 패턴 (가-힣)
_korean_pattern = re.compile(r"[\uAC00-\uD7A3]+")


def _get_cities() -> dict:
    """도시 데이터 캐시 반환"""
    global _cities_cache
    if _cities_cache is None:
        _cities_cache = _gc.get_cities()
    return _cities_cache


def _get_countries() -> dict:
    """국가 데이터 캐시 반환"""
    global _countries_cache
    if _countries_cache is None:
        _countries_cache = _gc.get_countries()
    return _countries_cache


def _get_country_name(country_code: str) -> str:
    """국가 코드로 영어 국가명 반환"""
    countries = _get_countries()
    country = countries.get(country_code, {})
    return country.get("name", country_code)


def _build_korean_search_index() -> dict[str, list[str]]:
    """
    한글 이름 → geonameid 매핑 인덱스 구축
    alternatenames에서 한글 이름을 추출하여 검색 인덱스 생성
    """
    global _korean_search_index
    if _korean_search_index is not None:
        return _korean_search_index

    _korean_search_index = {}
    cities = _get_cities()

    for geonameid, city in cities.items():
        alt_names = city.get("alternatenames", [])
        if isinstance(alt_names, str):
            alt_names = [alt_names]

        for name in alt_names:
            if _korean_pattern.search(name):
                normalized = name.lower()
                if normalized not in _korean_search_index:
                    _korean_search_index[normalized] = []
                if geonameid not in _korean_search_index[normalized]:
                    _korean_search_index[normalized].append(geonameid)

    return _korean_search_index


def _get_korean_city_name_from_alt(city: dict) -> str | None:
    """
    도시의 한글 이름 추출 (주요 도시 매핑 → alternatenames 순)

    선택 우선순위:
    1. 주요 도시 매핑 테이블 (korean_names.py)
    2. alternatenames에서 적절한 한글 이름 선택

    Args:
        city: geonamescache 도시 데이터

    Returns:
        한글 도시명 또는 None
    """
    city_name = city.get("name", "")

    # 1. 주요 도시 매핑 확인 (우선순위 최상)
    mapped_name = get_korean_city_name(city_name)
    if mapped_name:
        return mapped_name

    # 2. alternatenames에서 한글 이름 추출
    alt_names = city.get("alternatenames", [])
    if isinstance(alt_names, str):
        alt_names = [alt_names]

    korean_names = []
    for name in alt_names:
        if _korean_pattern.search(name):
            korean_names.append(name)

    if not korean_names:
        return None

    # 행정구역 접미사 (우선순위 낮음)
    suffixes = ("특별시", "광역시", "특별자치시", "특별자치도", "시", "군", "구", "도", "현")

    # 점수 계산: 짧을수록, 접미사 없을수록 높은 점수
    def score(name: str) -> tuple:
        has_suffix = any(name.endswith(s) for s in suffixes)
        # (접미사 없음 우선, 길이 짧은 것 우선)
        return (0 if has_suffix else 1, -len(name))

    korean_names.sort(key=score, reverse=True)
    return korean_names[0]


class CityCoordinates:
    """도시 좌표 데이터 접근 클래스 (geonamescache 기반, 한글 지원)"""

    @staticmethod
    def get_coordinates(city_name: str) -> tuple[float, float] | None:
        """도시의 (위도, 경도) 반환.

        한글/영어 입력을 모두 지원하며, 동명(同名) 도시가 여러 개일 때는
        인구가 가장 많은 도시(통상 광역시)를 우선한다.
        예) "광주"/"Gwangju" -> 광주광역시(126.85°E)이며, 경기도 광주시가 아님.
        """
        if not city_name:
            return None

        # search_city의 매칭 로직(한글 인덱스 + 정확>시작>포함 + 인구순 정렬)을 재사용한다.
        matches = CityCoordinates.search_city(city_name, limit=1)
        if matches:
            return (matches[0]["latitude"], matches[0]["longitude"])

        return None

    @staticmethod
    def get_longitude(city_name: str, default: float = 126.9780) -> float:
        """도시의 경도 반환 (기본값: 서울)"""
        coords = CityCoordinates.get_coordinates(city_name)
        if coords:
            return coords[1]
        return default

    @staticmethod
    def get_latitude(city_name: str, default: float = 37.5665) -> float:
        """도시의 위도 반환 (기본값: 서울)"""
        coords = CityCoordinates.get_coordinates(city_name)
        if coords:
            return coords[0]
        return default

    @staticmethod
    def list_cities(limit: int = 100) -> list[dict]:
        """
        등록된 도시 목록 반환 (인구 기준 상위)

        Returns:
            도시 정보 리스트 [{name, name_ko, country, country_ko, ...}, ...]
        """
        cities = _get_cities()
        sorted_cities = sorted(cities.values(), key=lambda x: x.get("population", 0), reverse=True)[
            :limit
        ]

        result = []
        for city in sorted_cities:
            country_code = city["countrycode"]
            country_name_en = _get_country_name(country_code)
            country_name_ko = get_korean_country_name(country_code, country_name_en)
            korean_name = _get_korean_city_name_from_alt(city)

            result.append(
                {
                    "name": city["name"],
                    "name_ko": korean_name,
                    "country": country_name_en,
                    "country_ko": country_name_ko,
                    "countrycode": country_code,
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "population": city.get("population", 0),
                }
            )

        return result

    @staticmethod
    def search_city(keyword: str, limit: int = 20) -> list[dict]:
        """
        키워드로 도시 검색 (한글 검색 지원)

        Args:
            keyword: 검색 키워드 (한글 또는 영어)
            limit: 최대 결과 수

        Returns:
            도시 정보 리스트 [{
                name: str,           # 영어 이름
                name_ko: str | None, # 한글 이름
                country: str,        # 영어 국가명
                country_ko: str,     # 한글 국가명
                latitude, longitude, population
            }, ...]
        """
        if not keyword or len(keyword) < 1:
            return []

        cities = _get_cities()
        keyword_lower = keyword.lower()

        # 검색어가 한글인지 확인
        is_korean_query = bool(_korean_pattern.search(keyword))

        seen_ids = set()
        exact_matches = []
        starts_with = []
        contains = []

        if is_korean_query:
            # 한글 검색: 한글 검색 인덱스 사용
            korean_index = _build_korean_search_index()

            for korean_name, geoname_ids in korean_index.items():
                match_type = None
                if korean_name == keyword_lower:
                    match_type = "exact"
                elif korean_name.startswith(keyword_lower):
                    match_type = "starts"
                elif keyword_lower in korean_name:
                    match_type = "contains"

                if match_type:
                    for gid in geoname_ids:
                        if gid in seen_ids:
                            continue
                        city = cities.get(gid)
                        if city:
                            if match_type == "exact":
                                exact_matches.append(city)
                            elif match_type == "starts":
                                starts_with.append(city)
                            else:
                                contains.append(city)
                            seen_ids.add(gid)
        else:
            # 영어 검색: 기존 로직 사용
            for gid, city in cities.items():
                city_name = city["name"]
                city_lower = city_name.lower()

                if city_lower == keyword_lower:
                    exact_matches.append(city)
                    seen_ids.add(gid)
                elif city_lower.startswith(keyword_lower):
                    starts_with.append(city)
                    seen_ids.add(gid)
                elif keyword_lower in city_lower:
                    contains.append(city)
                    seen_ids.add(gid)

        # 정확한 매칭 > 시작 매칭 > 포함 매칭 순서로 정렬
        # 각 그룹 내에서는 인구 기준 정렬
        results = []
        for group in [exact_matches, starts_with, contains]:
            group.sort(key=lambda x: x.get("population", 0), reverse=True)
            for city in group:
                if len(results) >= limit:
                    break

                country_code = city["countrycode"]
                country_name_en = _get_country_name(country_code)
                country_name_ko = get_korean_country_name(country_code, country_name_en)
                korean_name = _get_korean_city_name_from_alt(city)

                results.append(
                    {
                        "name": city["name"],
                        "name_ko": korean_name,
                        "country": country_name_en,
                        "country_ko": country_name_ko,
                        "countrycode": country_code,
                        "latitude": city["latitude"],
                        "longitude": city["longitude"],
                        "population": city.get("population", 0),
                    }
                )
            if len(results) >= limit:
                break

        return results

    @staticmethod
    def get_city_by_name(city_name: str) -> dict | None:
        """
        도시명으로 상세 정보 조회

        Args:
            city_name: 도시명 (영어)

        Returns:
            도시 정보 {name, name_ko, country, country_ko, latitude, longitude} 또는 None
        """
        cities = _get_cities()
        city_lower = city_name.lower()

        # 정확한 매칭 우선
        for city in cities.values():
            if city["name"].lower() == city_lower:
                country_code = city["countrycode"]
                country_name_en = _get_country_name(country_code)
                country_name_ko = get_korean_country_name(country_code, country_name_en)
                korean_name = _get_korean_city_name_from_alt(city)

                return {
                    "name": city["name"],
                    "name_ko": korean_name,
                    "country": country_name_en,
                    "country_ko": country_name_ko,
                    "countrycode": country_code,
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                }

        # 부분 매칭 (인구 기준 상위)
        matches = []
        for city in cities.values():
            if city_lower in city["name"].lower():
                matches.append(city)

        if matches:
            matches.sort(key=lambda x: x.get("population", 0), reverse=True)
            city = matches[0]
            country_code = city["countrycode"]
            country_name_en = _get_country_name(country_code)
            country_name_ko = get_korean_country_name(country_code, country_name_en)
            korean_name = _get_korean_city_name_from_alt(city)

            return {
                "name": city["name"],
                "name_ko": korean_name,
                "country": country_name_en,
                "country_ko": country_name_ko,
                "countrycode": country_code,
                "latitude": city["latitude"],
                "longitude": city["longitude"],
            }

        return None


def get_city_longitude(city_name: str, default: float = 126.9780) -> float:
    """편의 함수: 도시 경도 반환"""
    return CityCoordinates.get_longitude(city_name, default)
