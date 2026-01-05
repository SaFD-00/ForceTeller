"""
만세력 API 라우트
사주 계산 엔드포인트
"""

from datetime import datetime, time
from fastapi import APIRouter, HTTPException

from api.schemas import ManseolRequest, ManseolResponse, ErrorResponse
from manseol.models.input_model import SajuInput, CalendarType, Gender
from manseol.output.json_exporter import JsonExporter


router = APIRouter(prefix="/api/manseol", tags=["manseol"])


@router.post(
    "",
    response_model=ManseolResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="사주 계산",
    description="생년월일시를 입력받아 사주팔자를 계산합니다."
)
async def calculate_saju(request: ManseolRequest) -> ManseolResponse:
    """
    사주 계산 엔드포인트

    - 양력/음력/윤달 지원
    - 시간 보정 (경도, 균시차, DST) 적용
    - 사주 4주 및 분석 결과 반환
    """
    try:
        # 출생시간 파싱
        birth_time = None
        if request.birth_time:
            try:
                birth_time = datetime.strptime(request.birth_time, "%H:%M").time()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="시간 형식이 잘못되었습니다. HH:MM 형식으로 입력하세요."
                )

        # 입력 데이터 생성
        saju_input = SajuInput(
            name=request.name,
            birth_date=request.birth_date,
            birth_time=birth_time,
            calendar=CalendarType(request.calendar.value),
            city=request.city,
            gender=Gender(request.gender.value),
            jajasi=request.jajasi,
            longitude=request.longitude,
            apply_time_correction=request.apply_time_correction
        )

        # 사주 계산
        exporter = JsonExporter(saju_input)
        result = exporter.generate_result()

        return ManseolResponse(
            success=True,
            data=result.to_dict()
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"계산 중 오류 발생: {str(e)}")


@router.post(
    "/quick",
    response_model=ManseolResponse,
    summary="빠른 사주 계산",
    description="최소 정보로 빠르게 사주를 계산합니다."
)
async def quick_calculate(
    name: str,
    birth_date: str,
    gender: str,
    birth_time: str = None
) -> ManseolResponse:
    """
    빠른 사주 계산 (쿼리 파라미터)

    간단한 파라미터로 빠르게 사주 계산
    """
    try:
        # 날짜 파싱
        parsed_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

        # 시간 파싱
        parsed_time = None
        if birth_time:
            parsed_time = datetime.strptime(birth_time, "%H:%M").time()

        # 입력 데이터
        saju_input = SajuInput(
            name=name,
            birth_date=parsed_date,
            birth_time=parsed_time,
            gender=Gender(gender)
        )

        # 계산
        exporter = JsonExporter(saju_input)
        result = exporter.generate_result()

        return ManseolResponse(
            success=True,
            data=result.to_dict()
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/cities",
    summary="도시 검색",
    description="전세계 도시를 검색합니다. 한글/영어 모두 지원합니다."
)
async def search_cities(q: str = "", limit: int = 20):
    """
    도시 검색 엔드포인트 (한글 검색 지원)

    - q: 검색어 (도시명, 한글/영어 모두 지원)
    - limit: 최대 결과 수 (기본 20)

    응답 필드:
    - name: 영어 도시명 (API 전송용)
    - name_ko: 한글 도시명 (표시용, 없으면 null)
    - country: 영어 국가명
    - country_ko: 한글 국가명
    """
    from manseol.data.city_coordinates import CityCoordinates

    if not q:
        # 검색어가 없으면 인구 기준 상위 도시 반환
        cities = CityCoordinates.list_cities(limit=limit)
        return {
            "success": True,
            "cities": cities,
            "total": len(cities)
        }

    # 검색어로 도시 검색 (한글/영어 모두 지원)
    results = CityCoordinates.search_city(q, limit=limit)

    return {
        "success": True,
        "cities": results,
        "total": len(results)
    }


@router.get(
    "/city/{city_name}",
    summary="도시 정보",
    description="특정 도시의 좌표 정보를 반환합니다."
)
async def get_city_info(city_name: str):
    """도시 좌표 정보 반환"""
    from manseol.data.city_coordinates import CityCoordinates

    city_info = CityCoordinates.get_city_by_name(city_name)

    if not city_info:
        raise HTTPException(status_code=404, detail=f"도시 '{city_name}'을 찾을 수 없습니다.")

    return {
        "success": True,
        "city": city_info['name'],
        "country": city_info['country'],
        "latitude": city_info['latitude'],
        "longitude": city_info['longitude']
    }
