"""第8天 Flask 强化项目测试 — 覆盖新增的 /api/metrics、/api/categories、/health 接口。"""

import pytest

from app import app


@pytest.fixture
def client():
    """创建 Flask 测试客户端。"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def login(client):
    """辅助函数：使用演示账号登录并获得 session。"""
    return client.post(
        "/login",
        data={"username": "student", "password": "day07"},
        follow_redirects=True,
    )


class TestHealthEndpoint:
    """测试 /health 接口（无需登录）。"""

    def test_health_returns_ok(self, client):
        """健康检查接口应返回 ok=True。"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["ok"] is True
        assert data["service"] == "day08-flask-upgrade"


class TestMetricsAPI:
    """测试 /api/metrics 接口（需要登录）。"""

    def test_metrics_requires_login(self, client):
        """未登录时应被重定向到登录页。"""
        response = client.get("/api/metrics", follow_redirects=False)
        assert response.status_code == 302

    def test_metrics_returns_four_cards(self, client):
        """登录后应返回 4 张指标卡数据。"""
        login(client)
        response = client.get("/api/metrics")
        assert response.status_code == 200
        data = response.get_json()
        assert data["ok"] is True
        assert len(data["metrics"]) == 4
        for metric in data["metrics"]:
            assert "label" in metric
            assert "value" in metric
            assert "note" in metric

    def test_metrics_values_are_strings(self, client):
        """指标卡的 value 和 note 应为可序列化的字符串。"""
        login(client)
        response = client.get("/api/metrics")
        data = response.get_json()
        for metric in data["metrics"]:
            assert isinstance(metric["label"], str)
            assert isinstance(metric["value"], str)
            assert isinstance(metric["note"], str)


class TestCategoriesAPI:
    """测试 /api/categories 接口（需要登录）。"""

    def test_categories_requires_login(self, client):
        """未登录时应被重定向到登录页。"""
        response = client.get("/api/categories", follow_redirects=False)
        assert response.status_code == 302

    def test_categories_returns_all_rows_without_filter(self, client):
        """不带查询参数时应返回全部品类记录。"""
        login(client)
        response = client.get("/api/categories")
        data = response.get_json()
        assert data["ok"] is True
        assert data["category"] == "全部"
        assert len(data["rows"]) >= 5

    def test_categories_filter_by_fashion(self, client):
        """传入 category=Fashion 时应只返回 Fashion 记录。"""
        login(client)
        response = client.get("/api/categories?category=Fashion")
        data = response.get_json()
        assert data["ok"] is True
        assert data["category"] == "Fashion"
        assert len(data["rows"]) == 1
        assert data["rows"][0]["偏好品类"] == "Fashion"

    def test_categories_rows_have_expected_fields(self, client):
        """返回的每一行应包含偏好品类、用户数、流失率、平均订单数字段。"""
        login(client)
        response = client.get("/api/categories")
        data = response.get_json()
        for row in data["rows"]:
            assert "偏好品类" in row
            assert "用户数" in row
            assert "流失率" in row
            assert "平均订单数" in row


class TestErrorHandling:
    """测试错误处理。"""

    def test_400_error_returns_json_structure(self, client):
        """400 错误应返回统一的 JSON 结构，包含 ok 和 error 字段。"""
        login(client)
        response = client.post(
            "/api/ask",
            content_type="application/json",
            data='{"question":""}',
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["ok"] is False
        assert "answer" in data

    def test_404_error_returns_html(self, client):
        """404 错误应返回自定义 HTML 页面。"""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        assert b"404" in response.data

    def test_api_ask_without_login(self, client):
        """未登录时调用 /api/ask 应被拒绝。"""
        response = client.post(
            "/api/ask",
            content_type="application/json",
            data='{"question":"你好"}',
            follow_redirects=False,
        )
        assert response.status_code == 302
