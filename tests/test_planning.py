import copy

import pytest
from pydantic import ValidationError

from app.planning import calculate_baseline
from app.schemas import ScenarioCreate


@pytest.fixture
def payload():
    return {
        "name": "Synthetic",
        "level": "tactical",
        "data": {
            "grades": [
                {"code": "A", "feedstock_kg_per_ton": 1000, "water_m3_per_ton": 2},
                {"code": "B", "feedstock_kg_per_ton": 1100},
            ],
            "buckets": [
                {
                    "label": "w1",
                    "start": "2026-11-02",
                    "end": "2026-11-08",
                    "granularity": "week",
                    "capacity_tons": 100,
                    "demand_tons": {"A": 60, "B": 60},
                },
            ],
            "initial_inventory_tons": {"A": 10},
            "changeover_loss_tons": 5,
        },
    }


def test_capacity_and_changeover(payload):
    plan = calculate_baseline(ScenarioCreate.model_validate(payload))
    row = plan["buckets"][0]
    assert row["production_tons"] == {"A": 50, "B": 45}
    assert row["changeover_loss_tons"] == 5
    assert sum(row["production_tons"].values()) + row["changeover_loss_tons"] <= 100
    assert row["shortage_tons"] == {"A": 0, "B": 15}
    assert plan["kpis"]["served_tons"] == 105
    assert plan["is_optimized"] is False
    assert plan["production_feasibility_verified"] is False


def test_material_and_water_needs(payload):
    result = calculate_baseline(ScenarioCreate.model_validate(payload))
    flows = result["buckets"][0]["derived_flows"]
    assert flows["feedstock_kg"] == 99500
    assert flows["water_m3"] == 100


def test_existing_inventory_and_zero_capacity(payload):
    payload["data"]["buckets"][0]["capacity_tons"] = 0
    result = calculate_baseline(ScenarioCreate.model_validate(payload))
    assert result["kpis"]["produced_tons"] == 0
    assert result["kpis"]["served_tons"] == 10
    assert result["kpis"]["shortage_tons"] == 110


@pytest.mark.parametrize("mutation", [
    lambda d: d["data"]["grades"].append({"code": "A"}),
    lambda d: d["data"]["buckets"][0]["demand_tons"].update({"UNKNOWN": 2}),
    lambda d: d["data"]["buckets"][0].update({"capacity_tons": -3}),
    lambda d: d["data"]["buckets"][0].update({"end": "2026-10-01"}),
    lambda d: d["data"]["buckets"][0].update({"granularity": "day"}),
])
def test_invalid_scenarios_rejected(payload, mutation):
    variant = copy.deepcopy(payload)
    mutation(variant)
    with pytest.raises(ValidationError):
        ScenarioCreate.model_validate(variant)


def test_excessive_operational_horizon_rejected(payload):
    payload["level"] = "operational"
    payload["data"]["buckets"][0]["end"] = "2027-01-01"
    with pytest.raises(ValidationError):
        ScenarioCreate.model_validate(payload)
