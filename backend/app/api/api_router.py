from fastapi import APIRouter
from .routes import parse, chart, projects, datasets, samples, export

api_router = APIRouter()

api_router.include_router(parse.router, prefix="/parse", tags=["Pattern Parsing"])
api_router.include_router(chart.router, prefix="/chart", tags=["Chart Generation"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects & Storage"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["ML & Datasets"])
api_router.include_router(samples.router, prefix="/samples", tags=["Sample Library"])
api_router.include_router(export.router, prefix="/export", tags=["Exports"])
