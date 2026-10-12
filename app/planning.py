"""Deterministic, NOT mathematically optimal, illustrative capacity allocator.

This code must not be used to operate industrial equipment or certify production feasibility.
Future solver contract must account for per-equipment constraints, raw material supply,
energy balances, grade wheel and transitions, repairs, silo inventories, operations, etc.
"""
from app.schemas import ScenarioCreate

def calculate_baseline(scenario: ScenarioCreate) -> dict:
    data = scenario.data
    grades = {g.code: g for g in data.grades}
    stocks = {code: data.initial_inventory_tons.get(code, 0.0) for code in grades}
    previous_grade = None
    rows = []
    totals = {'demand_tons': 0.0, 'produced_tons': 0.0, 'served_tons': 0.0,
              'shortage_tons': 0.0, 'changeover_loss_tons': 0.0}
    for bucket in data.buckets:
        available = bucket.capacity_tons
        products = {}
        loss = 0.0
        # Alphabetical fixed order is reproducible but generally suboptimal.
        for code in sorted(grades):
            target = bucket.demand_tons.get(code, 0.0)
            need = max(0.0, target - stocks[code])
            if need > 0 and available > 0:
                setup = data.changeover_loss_tons if previous_grade is not None and previous_grade != code else 0.0
                possible = max(0.0, available - setup)
                produce = min(need, possible)
                if produce > 0:
                    available -= setup + produce
                    loss += setup
                    stocks[code] += produce
                    previous_grade = code
                products[code] = produce
            else:
                products[code] = 0.0
        shortages = {}
        served = {}
        for code in sorted(grades):
            demand = bucket.demand_tons.get(code, 0.0)
            supply = min(demand, stocks[code])
            stocks[code] -= supply
            served[code] = supply
            shortages[code] = demand - supply
        produced = sum(products.values())
        consumption = {
            'feedstock_kg': sum(v * grades[c].feedstock_kg_per_ton for c, v in products.items()),
            'materials_kg': sum(v * grades[c].materials_kg_per_ton for c, v in products.items()),
            'water_m3': sum(v * grades[c].water_m3_per_ton for c, v in products.items()),
            'air_nm3': sum(v * grades[c].air_nm3_per_ton for c, v in products.items()),
            'nitrogen_nm3': sum(v * grades[c].nitrogen_nm3_per_ton for c, v in products.items()),
            'byproduct_tons': sum(v * grades[c].byproduct_tons_per_ton for c, v in products.items()),
        }
        rows.append({'bucket': bucket.label, 'production_tons': products,
                     'served_tons': served, 'shortage_tons': shortages,
                     'ending_inventory_tons': stocks.copy(),
                     'unused_capacity_tons': round(available, 6),
                     'changeover_loss_tons': loss, 'derived_flows': consumption})
        totals['demand_tons'] += sum(bucket.demand_tons.values())
        totals['produced_tons'] += produced
        totals['served_tons'] += sum(served.values())
        totals['shortage_tons'] += sum(shortages.values())
        totals['changeover_loss_tons'] += loss
    totals['demand_coverage_pct'] = round(100 * totals['served_tons'] / totals['demand_tons'], 2) if totals['demand_tons'] else 100.0
    return {'engine': 'illustrative_baseline_v1', 'is_optimized': False,
            'production_feasibility_verified': False,
            'warning': 'Учебный эвристический расчёт; не промышленный оптимизатор и не проверка технологической исполнимости.',
            'level': scenario.level.value, 'buckets': rows, 'kpis': totals}
