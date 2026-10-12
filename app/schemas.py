"""Deliberately limited starter contract; see docs/DATA_MODEL.md for expansion."""
from datetime import date
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field, model_validator

NonNegative = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Positive = Annotated[float, Field(gt=0, allow_inf_nan=False)]

class PlanningLevel(str, Enum):
    annual = 'annual'
    tactical = 'tactical'
    operational = 'operational'

class Grade(BaseModel):
    code: str = Field(min_length=1, max_length=40, pattern=r'^[A-Za-z0-9_-]+$')
    feedstock_kg_per_ton: NonNegative = 0
    materials_kg_per_ton: NonNegative = 0
    water_m3_per_ton: NonNegative = 0
    air_nm3_per_ton: NonNegative = 0
    nitrogen_nm3_per_ton: NonNegative = 0
    byproduct_tons_per_ton: NonNegative = 0

class Bucket(BaseModel):
    label: str = Field(min_length=1, max_length=60)
    start: date
    end: date
    granularity: str = Field(pattern=r'^(day|week|month)$')
    capacity_tons: NonNegative
    demand_tons: dict[str, NonNegative]

    @model_validator(mode='after')
    def dates_ok(self):
        if self.end < self.start:
            raise ValueError('Bucket end must be >= start')
        return self

class PlanningInput(BaseModel):
    grades: list[Grade] = Field(min_length=1)
    buckets: list[Bucket] = Field(min_length=1)
    initial_inventory_tons: dict[str, NonNegative] = Field(default_factory=dict)
    changeover_loss_tons: NonNegative = 0

    @model_validator(mode='after')
    def consistent(self):
        codes = [grade.code for grade in self.grades]
        if len(codes) != len(set(codes)):
            raise ValueError('Duplicate grade codes')
        if len({b.label for b in self.buckets}) != len(self.buckets):
            raise ValueError('Duplicate bucket labels')
        unknown = (set(self.initial_inventory_tons) | {k for b in self.buckets for k in b.demand_tons}) - set(codes)
        if unknown:
            raise ValueError(f'Unknown grades: {sorted(unknown)}')
        ordered = sorted(self.buckets, key=lambda b: b.start)
        if ordered != self.buckets:
            raise ValueError('Buckets must be ordered by start date')
        if any(a.end >= b.start for a, b in zip(ordered, ordered[1:])):
            raise ValueError('Buckets must not overlap')
        return self

class ScenarioCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    level: PlanningLevel
    data: PlanningInput

    @model_validator(mode='after')
    def level_rules(self):
        allowed = {'annual': {'week','month'}, 'tactical': {'week','month'}, 'operational': {'day','week'}}
        max_days = {'annual': 550, 'tactical': 93, 'operational': 28}
        if any(b.granularity not in allowed[self.level.value] for b in self.data.buckets):
            raise ValueError('Unsupported bucket granularity for planning level')
        first, last = self.data.buckets[0], self.data.buckets[-1]
        if (last.end - first.start).days + 1 > max_days[self.level.value]:
            raise ValueError('Planning horizon exceeds this level maximum')
        return self
