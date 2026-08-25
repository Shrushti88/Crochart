from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ...core.database import get_db
from ...models.db_models import DBDatasetSample
from ...ml.synthetic_generator import SyntheticPatternGenerator
from ...ml.eval_pipeline import PatternEvaluator

router = APIRouter()

class GenerateSyntheticRequest(BaseModel):
    count: int = 10
    category: Optional[str] = "all"  # "all", "amigurumi", "flat_circle", "row_fabric"
    save_to_db: Optional[bool] = True

class EvalRequest(BaseModel):
    samples: Optional[List[Dict[str, Any]]] = None
    use_db_samples: Optional[bool] = False

@router.post("/generate-synthetic")
async def generate_synthetic_dataset(req: GenerateSyntheticRequest, db: AsyncSession = Depends(get_db)):
    samples = []
    for _ in range(req.count):
        if req.category == "amigurumi":
            samples.append(SyntheticPatternGenerator.generate_amigurumi_sphere())
        elif req.category == "flat_circle":
            samples.append(SyntheticPatternGenerator.generate_flat_circle())
        elif req.category == "row_fabric":
            samples.append(SyntheticPatternGenerator.generate_row_fabric())
        else:
            batch = SyntheticPatternGenerator.generate_batch(1)
            samples.extend(batch)

    if req.save_to_db:
        for s in samples:
            db_sample = DBDatasetSample(
                category=req.category or "synthetic",
                written_pattern=s["written_pattern"],
                normalized_pattern=s["normalized_pattern"],
                structured_ast=s["structured_ast"],
                expected_chart=s["expected_chart"]
            )
            db.add(db_sample)
        await db.commit()

    return {
        "count": len(samples),
        "samples": samples
    }

@router.post("/evaluate")
async def evaluate_parsing_model(req: EvalRequest, db: AsyncSession = Depends(get_db)):
    samples_to_eval = []
    if req.use_db_samples:
        result = await db.execute(select(DBDatasetSample).order_by(desc(DBDatasetSample.created_at)).limit(50))
        db_items = result.scalars().all()
        for item in db_items:
            samples_to_eval.append({
                "written_pattern": item.written_pattern,
                "normalized_pattern": item.normalized_pattern,
                "structured_ast": item.structured_ast,
                "expected_chart": item.expected_chart
            })
    elif req.samples:
        samples_to_eval = req.samples
    else:
        # Generate on the fly
        samples_to_eval = SyntheticPatternGenerator.generate_batch(15)

    report = PatternEvaluator.evaluate_dataset(samples_to_eval)
    return report

@router.get("/samples")
async def get_dataset_samples(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBDatasetSample).order_by(desc(DBDatasetSample.created_at)).limit(limit))
    samples = result.scalars().all()
    return samples
