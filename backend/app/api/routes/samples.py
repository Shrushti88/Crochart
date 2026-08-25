from typing import List, Dict, Any
from fastapi import APIRouter
from ...samples.sample_library import SAMPLE_PATTERNS

router = APIRouter()

@router.get("", response_model=List[Dict[str, Any]])
async def get_sample_patterns():
    return SAMPLE_PATTERNS

@router.get("/{sample_id}")
async def get_single_sample(sample_id: str):
    for s in SAMPLE_PATTERNS:
        if s["id"] == sample_id:
            return s
    return {"error": "Sample pattern not found"}
