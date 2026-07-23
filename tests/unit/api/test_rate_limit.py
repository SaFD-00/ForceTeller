"""api.rate_limit 단위 테스트 — 슬라이딩 윈도우 리미터·클라이언트 키 결정."""

from unittest.mock import MagicMock

import pytest

from api.rate_limit import SlidingWindowRateLimiter, client_key

pytestmark = pytest.mark.unit


class TestSlidingWindowRateLimiter:
    def test_allows_up_to_limit_then_blocks(self):
        limiter = SlidingWindowRateLimiter(limit=3, window_seconds=60)
        # 창 시작 시각을 고정 주입해 결정론적으로 검증
        assert limiter.check("ip", now=1000.0) == (True, 0.0)
        assert limiter.check("ip", now=1000.1)[0] is True
        assert limiter.check("ip", now=1000.2)[0] is True
        allowed, retry = limiter.check("ip", now=1000.3)
        assert allowed is False
        # 첫 요청(1000.0)이 창(60s) 밖으로 나가는 1060.0까지 대기 → 약 59.7초
        assert retry == pytest.approx(59.7, abs=0.01)

    def test_window_slides_and_frees_capacity(self):
        limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10)
        assert limiter.check("ip", now=0.0)[0] is True
        assert limiter.check("ip", now=1.0)[0] is True
        assert limiter.check("ip", now=2.0)[0] is False
        # 첫 요청(0.0)이 창 밖으로 나가면(>10) 자리 하나가 회복된다
        assert limiter.check("ip", now=10.5)[0] is True

    def test_keys_are_isolated(self):
        limiter = SlidingWindowRateLimiter(limit=1, window_seconds=60)
        assert limiter.check("a", now=0.0)[0] is True
        assert limiter.check("a", now=0.1)[0] is False
        # 다른 키는 독립 카운터
        assert limiter.check("b", now=0.2)[0] is True

    def test_boundary_expiry_is_inclusive(self):
        # cutoff = now - window; dq[0] <= cutoff 이면 제거. 정확히 window 경과 시 회복.
        limiter = SlidingWindowRateLimiter(limit=1, window_seconds=10)
        assert limiter.check("ip", now=100.0)[0] is True
        assert limiter.check("ip", now=110.0)[0] is True  # 100.0 <= 110-10 이므로 만료

    def test_reset_clears_state(self):
        limiter = SlidingWindowRateLimiter(limit=1, window_seconds=60)
        assert limiter.check("ip", now=0.0)[0] is True
        assert limiter.check("ip", now=0.1)[0] is False
        limiter.reset()
        assert limiter.check("ip", now=0.2)[0] is True

    def test_max_keys_guard_bounds_memory(self):
        limiter = SlidingWindowRateLimiter(limit=1, window_seconds=60, max_keys=2)
        limiter.check("a", now=0.0)
        limiter.check("b", now=0.0)
        # 3번째 신규 키 진입 시 상한 도달로 전체 리셋 → 새 키만 남는다
        limiter.check("c", now=0.0)
        assert limiter.check("c", now=0.1)[0] is False  # c는 방금 계상됨
        assert limiter.check("a", now=0.2)[0] is True  # a는 리셋되어 회복

    @pytest.mark.parametrize("bad", [0, -1])
    def test_invalid_limit_rejected(self, bad):
        with pytest.raises(ValueError):
            SlidingWindowRateLimiter(limit=bad, window_seconds=60)

    def test_invalid_window_rejected(self):
        with pytest.raises(ValueError):
            SlidingWindowRateLimiter(limit=1, window_seconds=0)


class TestClientKey:
    def _request(self, *, forwarded=None, host="1.2.3.4"):
        req = MagicMock()
        req.headers = {}
        if forwarded is not None:
            req.headers["x-forwarded-for"] = forwarded
        req.client = MagicMock()
        req.client.host = host
        return req

    def test_trusts_forwarded_leftmost_ip(self):
        req = self._request(forwarded="9.9.9.9, 10.0.0.1, 172.16.0.1")
        assert client_key(req, trust_forwarded=True) == "9.9.9.9"

    def test_ignores_forwarded_when_untrusted(self):
        req = self._request(forwarded="9.9.9.9", host="1.2.3.4")
        assert client_key(req, trust_forwarded=False) == "1.2.3.4"

    def test_falls_back_to_socket_when_no_header(self):
        req = self._request(forwarded=None, host="1.2.3.4")
        assert client_key(req, trust_forwarded=True) == "1.2.3.4"

    def test_unknown_when_no_client(self):
        req = MagicMock()
        req.headers = {}
        req.client = None
        assert client_key(req, trust_forwarded=True) == "unknown"
