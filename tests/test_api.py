import os

# SQLite is used for isolated unit tests. No external services or corporate datasets.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import PlanRun, Scenario  # noqa: E402, F401


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    def local_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = local_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    engine.dispose()


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok", "database": "ok"}
    assert client.get("/api/meta").json()["engine"] == "illustrative_baseline_v1"


def test_create_and_run(client):
    payload = {
        "name": "Synthetic unit test",
        "level": "tactical",
        "data": {
            "grades": [{"code": "A", "feedstock_kg_per_ton": 1000}],
            "buckets": [{
                "label": "w1", "start": "2026-11-02", "end": "2026-11-08",
                "granularity": "week", "capacity_tons": 100, "demand_tons": {"A": 120}
            }],
        },
    }
    created = client.post("/api/scenarios", json=payload)
    assert created.status_code == 201, created.text
    sid = created.json()["id"]
    assert len(client.get("/api/scenarios").json()) == 1
    assert client.get(f"/api/scenarios/{sid}").json()["name"] == payload["name"]
    run = client.post(f"/api/scenarios/{sid}/runs")
    assert run.status_code == 201, run.text
    result = run.json()["result"]
    assert result["kpis"]["shortage_tons"] == 20
    assert client.get(f"/api/runs/{run.json()['id']}").json()["result"] == result
    assert len(client.get(f"/api/scenarios/{sid}/runs").json()) == 1


def test_not_found_and_validation(client):
    assert client.get("/api/scenarios/missing").status_code == 404
    assert client.get("/api/runs/missing").status_code == 404
    assert client.post("/api/scenarios/missing/runs").status_code == 404
    assert client.post("/api/scenarios", json={"name": "Oops"}).status_code == 422
