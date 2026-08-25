from io import BytesIO
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from pypdf import PdfReader
from ...ontology.schema import CrochetPatternAST, TerminologyStandard
from ...parser.ast_parser import ASTParser
from ...validator.rules import PatternValidator
from ...validator.diagnostics import ValidationReport

router = APIRouter()

class ParseRequest(BaseModel):
    pattern_text: str
    title: Optional[str] = "Crochet Pattern"
    terminology: Optional[TerminologyStandard] = TerminologyStandard.US

class ParseResponse(BaseModel):
    ast: CrochetPatternAST
    validation: ValidationReport

@router.post("/text", response_model=ParseResponse)
async def parse_text_pattern(request: ParseRequest):
    if not request.pattern_text or not request.pattern_text.strip():
        raise HTTPException(status_code=400, detail="Pattern text cannot be empty.")
    
    parser = ASTParser(terminology=request.terminology or TerminologyStandard.US)
    ast = parser.parse(request.pattern_text, title=request.title or "Crochet Pattern")
    validation = PatternValidator.validate(ast)
    
    return ParseResponse(ast=ast, validation=validation)

@router.post("/file", response_model=ParseResponse)
async def parse_file_upload(
    file: UploadFile = File(...),
    title: Optional[str] = Form("Uploaded Pattern"),
    terminology: Optional[str] = Form("US")
):
    contents = await file.read()
    filename = file.filename.lower() if file.filename else ""
    extracted_text = ""

    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(contents))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")
    else:
        # Default to UTF-8 text
        try:
            extracted_text = contents.decode("utf-8")
        except UnicodeDecodeError:
            try:
                extracted_text = contents.decode("latin-1")
            except Exception as e:
                raise HTTPException(status_code=400, detail="Unable to decode uploaded file as text.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the uploaded file.")

    term_enum = TerminologyStandard.UK if terminology == "UK" else TerminologyStandard.US
    parser = ASTParser(terminology=term_enum)
    ast = parser.parse(extracted_text, title=title or file.filename or "Uploaded Pattern")
    validation = PatternValidator.validate(ast)

    return ParseResponse(ast=ast, validation=validation)
