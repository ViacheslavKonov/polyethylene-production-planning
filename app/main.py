"""Planning starter API. No authentication yet: localhost only until RBAC is implemented."""
from pathlib import Path
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import PlanRun, Scenario
from app.planning import calculate_baseline
from app.schemas import ScenarioCreate

app = FastAPI(title='Планирование производства полиэтилена', version='0.1.0')
WEB_DIR = Path(__file__).resolve().parent / 'static'
app.mount('/static', StaticFiles(directory=WEB_DIR), name='static')

@app.get('/')
def home():
    return FileResponse(WEB_DIR / 'index.html')

@app.get('/api/health')
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
    except Exception:
        raise HTTPException(status_code=503, detail='Database is unavailable') from None
    return {'status': 'ok', 'database': 'ok'}

@app.get('/api/meta')
def meta():
    return {'version': '0.1.0', 'status': 'starter', 'engine': 'illustrative_baseline_v1',
            'limitations': ['no_auth', 'no_optimization', 'no_MES_integration'],
            'levels': {'annual': 'до 18 месяцев', 'tactical': 'до 3 месяцев', 'operational': 'до 4 недель'}}

@app.post('/api/scenarios', status_code=201)
def create_scenario(body: ScenarioCreate, db: Session = Depends(get_db)):
    scenario = Scenario(id=str(uuid4()), name=body.name, level=body.level.value,
                        payload=body.model_dump(mode='json'))
    db.add(scenario)
    db.commit()
    db.refresh(scenario)
    return serialize_scenario(scenario)

def serialize_scenario(item: Scenario):
    return {'id': item.id, 'name': item.name, 'level': item.level,
            'data': item.payload['data'], 'created_at': item.created_at.isoformat()}

@app.get('/api/scenarios')
def list_scenarios(db: Session = Depends(get_db)):
    items = db.scalars(select(Scenario).order_by(Scenario.created_at.desc())).all()
    return [serialize_scenario(x) for x in items]

@app.get('/api/scenarios/{scenario_id}')
def get_scenario(scenario_id: str, db: Session = Depends(get_db)):
    item = db.get(Scenario, scenario_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Scenario not found')
    return serialize_scenario(item)

@app.post('/api/scenarios/{scenario_id}/runs', status_code=201)
def run_scenario(scenario_id: str, db: Session = Depends(get_db)):
    scenario = db.get(Scenario, scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail='Scenario not found')
    definition = ScenarioCreate.model_validate(scenario.payload)
    result = calculate_baseline(definition)
    run = PlanRun(id=str(uuid4()), scenario_id=scenario_id,
                  engine=result['engine'], result=result)
    db.add(run)
    db.commit()
    db.refresh(run)
    return serialize_run(run)

def serialize_run(item: PlanRun):
    return {'id': item.id, 'scenario_id': item.scenario_id,
            'created_at': item.created_at.isoformat(), 'result': item.result}

@app.get('/api/scenarios/{scenario_id}/runs')
def list_runs(scenario_id: str, db: Session = Depends(get_db)):
    if db.get(Scenario, scenario_id) is None:
        raise HTTPException(status_code=404, detail='Scenario not found')
    items = db.scalars(select(PlanRun).where(PlanRun.scenario_id == scenario_id).order_by(PlanRun.created_at.desc())).all()
    return [serialize_run(x) for x in items]

@app.get('/api/runs/{run_id}')
def get_run(run_id: str, db: Session = Depends(get_db)):
    item = db.get(PlanRun, run_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Run not found')
    return serialize_run(item)
