FROM python:3.11-slim

# uv 설치 (공식 이미지에서 정적 바이너리 복사, 재현성을 위해 버전 고정)
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

WORKDIR /app

# 시스템 의존성 설치 (ephem 빌드에 필요)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 의존성 메타데이터 먼저 복사 (레이어 캐시 최적화)
COPY pyproject.toml uv.lock ./

# 프로덕션 의존성만 설치 (dev 그룹 제외, 잠금 파일 그대로 사용)
RUN uv sync --frozen --no-dev

# 소스 코드 복사
COPY . .

# .venv 실행 파일을 PATH 앞에 추가
ENV PATH="/app/.venv/bin:$PATH"

# 포트 노출
EXPOSE 8000

# 서버 실행: 먼저 DB 마이그레이션(alembic) 적용 후 uvicorn 기동
# (DATABASE_URL 미설정 시 로컬 SQLite, 배포 시 PostgreSQL을 환경변수로 주입)
CMD ["sh", "-c", "alembic upgrade head && uvicorn api.server:app --host 0.0.0.0 --port 8000"]
