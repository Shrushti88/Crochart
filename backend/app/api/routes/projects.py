from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ...core.database import get_db
from ...models.db_models import DBProject, DBCorrection

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    raw_pattern: str
    terminology: Optional[str] = "US"
    is_circular: Optional[bool] = True
    ast_data: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    raw_pattern: str
    terminology: str
    is_circular: bool
    ast_data: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class CorrectionCreate(BaseModel):
    project_id: Optional[int] = None
    original_line: str
    corrected_line: str
    rule_code: Optional[str] = None
    notes: Optional[str] = ""

@router.get("", response_model=List[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBProject).order_by(desc(DBProject.updated_at)))
    projects = result.scalars().all()
    return projects

@router.post("", response_model=ProjectResponse)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    db_proj = DBProject(
        title=project_in.title,
        description=project_in.description or "",
        raw_pattern=project_in.raw_pattern,
        terminology=project_in.terminology or "US",
        is_circular=project_in.is_circular if project_in.is_circular is not None else True,
        ast_data=project_in.ast_data,
        chart_data=project_in.chart_data
    )
    db.add(db_proj)
    await db.commit()
    await db.refresh(db_proj)
    return db_proj

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBProject).where(DBProject.id == project_id))
    db_proj = result.scalar_one_or_none()
    if not db_proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_proj

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBProject).where(DBProject.id == project_id))
    db_proj = result.scalar_one_or_none()
    if not db_proj:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(db_proj)
    await db.commit()
    return {"message": "Project deleted successfully"}

@router.post("/corrections")
async def record_correction(corr: CorrectionCreate, db: AsyncSession = Depends(get_db)):
    db_corr = DBCorrection(
        project_id=corr.project_id,
        original_line=corr.original_line,
        corrected_line=corr.corrected_line,
        rule_code=corr.rule_code,
        notes=corr.notes or ""
    )
    db.add(db_corr)
    await db.commit()
    await db.refresh(db_corr)
    return {"id": db_corr.id, "status": "recorded"}
