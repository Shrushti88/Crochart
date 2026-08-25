from io import BytesIO
from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
from ...ontology.schema import ChartGraph, TerminologyStandard
from ...parser.ast_parser import ASTParser
from ...layout.graph_builder import ChartGraphBuilder
from ...ontology.symbols import CYC_SYMBOLS

router = APIRouter()

class ExportRequest(BaseModel):
    pattern_text: Optional[str] = None
    chart: Optional[ChartGraph] = None
    format: str = "svg" # "svg", "pdf", "json"
    title: Optional[str] = "Crochet Chart"

@router.post("")
async def export_chart_file(req: ExportRequest):
    if req.chart is not None:
        chart = req.chart
    elif req.pattern_text:
        parser = ASTParser()
        ast = parser.parse(req.pattern_text, title=req.title or "Crochet Chart")
        chart = ChartGraphBuilder.build(ast)
    else:
        raise HTTPException(status_code=400, detail="Must provide either pattern_text or chart graph")

    if req.format.lower() == "json":
        return Response(
            content=chart.model_dump_json(indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{req.title}.json"'}
        )

    # Generate standalone SVG
    svg_content = _render_standalone_svg(chart)

    if req.format.lower() == "svg":
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Content-Disposition": f'attachment; filename="{req.title}.svg"'}
        )
    elif req.format.lower() == "pdf":
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(50, 750, f"Crochet Pattern Chart: {chart.pattern_title}")
            p.drawString(50, 730, f"Total Stitches: {chart.total_stitches} | Units: {chart.units_count}")
            p.drawString(50, 700, "Vector SVG diagram exported from Crochet Visualizer.")
            p.showPage()
            p.save()
            pdf_bytes = buffer.getvalue()
            buffer.close()
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": f'attachment; filename="{req.title}.pdf"'}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")
            
    raise HTTPException(status_code=400, detail=f"Unsupported format: {req.format}")

def _render_standalone_svg(chart: ChartGraph) -> str:
    b = chart.bounds
    w = max(b["width"], 200)
    h = max(b["height"], 200)
    vx = b["min_x"]
    vy = b["min_y"]

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {w} {h}" width="100%" height="100%" style="background:#ffffff; font-family:sans-serif;">',
        '<style>',
        '  .chart-link { stroke: #cbd5e1; stroke-width: 1.5; stroke-dasharray: 2 2; fill: none; }',
        '  .chart-join { stroke: #f43f5e; stroke-width: 2; stroke-dasharray: 4 4; fill: none; }',
        '  .stitch-node text { font-size: 8px; fill: #64748b; text-anchor: middle; }',
        '</style>',
        '<g id="links">'
    ]

    # Map node positions
    node_pos = {n.id: n for n in chart.nodes}

    # Render links
    for link in chart.links:
        src = node_pos.get(link.source_id)
        tgt = node_pos.get(link.target_id)
        if src and tgt:
            cls_name = "chart-join" if link.link_type == "join" else "chart-link"
            svg_parts.append(f'<line x1="{src.x}" y1="{src.y}" x2="{tgt.x}" y2="{tgt.y}" class="{cls_name}" />')

    svg_parts.append('</g><g id="nodes">')

    # Render Nodes
    for n in chart.nodes:
        color = n.color or "#3b82f6"
        symbol_def = CYC_SYMBOLS.get(n.symbol_name, CYC_SYMBOLS.get("sc_plus"))
        inner_svg = symbol_def["svg"] if symbol_def else '<circle cx="0" cy="0" r="4" fill="currentColor"/>'

        svg_parts.append(
            f'<g class="stitch-node" transform="translate({n.x}, {n.y}) rotate({n.rotation})" style="color: {color};">'
            f'{inner_svg}'
            f'</g>'
        )

    svg_parts.append('</g></svg>')
    return "\n".join(svg_parts)
