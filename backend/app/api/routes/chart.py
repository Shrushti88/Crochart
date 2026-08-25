from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ...ontology.schema import CrochetPatternAST, ChartGraph, TerminologyStandard
from ...parser.ast_parser import ASTParser
from ...layout.graph_builder import ChartGraphBuilder

router = APIRouter()

class GenerateChartRequest(BaseModel):
    ast: Optional[CrochetPatternAST] = None
    pattern_text: Optional[str] = None
    title: Optional[str] = "Crochet Chart"
    terminology: Optional[TerminologyStandard] = TerminologyStandard.US

@router.post("/generate", response_model=ChartGraph)
async def generate_chart(request: GenerateChartRequest):
    if request.ast is not None:
        ast = request.ast
    elif request.pattern_text is not None and request.pattern_text.strip():
        parser = ASTParser(terminology=request.terminology or TerminologyStandard.US)
        ast = parser.parse(request.pattern_text, title=request.title or "Crochet Chart")
    else:
        raise HTTPException(status_code=400, detail="Either 'ast' or 'pattern_text' must be provided.")

    chart = ChartGraphBuilder.build(ast)
    return chart
