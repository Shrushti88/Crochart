from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from ..core.database import Base

class DBProject(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    raw_pattern = Column(Text, nullable=False)
    terminology = Column(String(10), default="US")
    is_circular = Column(Boolean, default=True)
    ast_data = Column(JSON, nullable=True)
    chart_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DBCorrection(Base):
    __tablename__ = "corrections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=True)
    original_line = Column(Text, nullable=False)
    corrected_line = Column(Text, nullable=False)
    rule_code = Column(String(50), nullable=True)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class DBDatasetSample(Base):
    __tablename__ = "dataset_samples"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), default="synthetic")
    written_pattern = Column(Text, nullable=False)
    normalized_pattern = Column(Text, nullable=False)
    structured_ast = Column(JSON, nullable=False)
    expected_chart = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
