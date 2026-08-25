from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum

class StitchType(str, Enum):
    # Basic stitches
    CH = "ch"              # Chain
    SL_ST = "sl_st"        # Slip Stitch
    SC = "sc"              # Single Crochet (US) / Double Crochet (UK)
    HDC = "hdc"            # Half Double Crochet (US) / Half Treble (UK)
    DC = "dc"              # Double Crochet (US) / Treble (UK)
    TR = "tr"              # Treble / Triple Crochet (US) / Double Treble (UK)
    DTR = "dtr"            # Double Treble (US) / Triple Treble (UK)
    
    # Starting elements
    MAGIC_RING = "magic_ring"  # Magic Ring / Magic Circle
    FOUNDATION_CH = "foundation_ch"
    
    # Modifications & Compound
    INC = "inc"            # 2 sc in next st
    DC_INC = "dc_inc"      # 2 dc in next st
    HDC_INC = "hdc_inc"    # 2 hdc in next st
    DEC = "dec"            # sc2tog / decrease
    DC_DEC = "dc_dec"      # dc2tog
    HDC_DEC = "hdc_dec"    # hdc2tog
    INV_DEC = "inv_dec"    # Invisible decrease
    
    # Decorative / Textured
    PUFF = "puff"
    POPCORN = "popcorn"
    BOBBLE = "bobble"
    CLUSTER = "cluster"
    PICOT = "picot"
    
    # Structural
    SKIP = "skip"          # Skip stitch
    SPACE = "space"        # Chain space
    JOIN = "join"          # Join round with slip stitch
    TURN = "turn"          # Turn work

class LoopTarget(str, Enum):
    BOTH = "both"
    BLO = "blo"  # Back Loop Only
    FLO = "flo"  # Front Loop Only
    SPACE = "space" # Into chain space
    POST_FRONT = "post_front" # Front post
    POST_BACK = "post_back"   # Back post

class StitchInstruction(BaseModel):
    id: str = Field(description="Unique stitch operation ID within pattern")
    stitch_type: StitchType = Field(description="Type of stitch")
    count: int = Field(default=1, description="Number of times this stitch is executed sequentially")
    target_loop: LoopTarget = Field(default=LoopTarget.BOTH)
    in_same_stitch: bool = Field(default=False, description="Whether multiple stitches are worked into the exact same base stitch")
    target_stitch_count: int = Field(default=1, description="Number of base stitches consumed (e.g., 2 for dec, 0 for ch, 1 for sc)")
    produced_stitch_count: int = Field(default=1, description="Number of stitches created by this operation (e.g., 2 for inc, 1 for sc, 0 for sl st join)")
    chain_space_size: Optional[int] = Field(default=None, description="Size of chain if ch-sp")
    raw_text: str = Field(default="", description="Original substring for this operation")
    line_number: int = Field(default=1)

class RepeatGroup(BaseModel):
    id: str
    instructions: List[Union[StitchInstruction, "RepeatGroup"]] = Field(default_factory=list)
    repeat_count: int = Field(default=1, description="Multiplier for this repeat group")
    raw_text: str = Field(default="")
    line_number: int = Field(default=1)

class UnitType(str, Enum):
    ROUND = "round"
    ROW = "row"

class PatternUnit(BaseModel):
    unit_type: UnitType = Field(default=UnitType.ROUND)
    index: int = Field(description="1-based index (e.g. Round 1, Row 2)")
    raw_header: str = Field(default="")
    raw_text: str = Field(default="")
    instructions: List[Union[StitchInstruction, RepeatGroup]] = Field(default_factory=list)
    stated_stitch_count: Optional[int] = Field(default=None, description="Explicit stitch count at end of line (e.g., (12))")
    computed_produced_count: int = Field(default=0, description="Calculated total stitches produced in this unit")
    computed_consumed_count: int = Field(default=0, description="Calculated total base stitches consumed from previous unit")
    is_joined: bool = Field(default=False, description="Whether round is joined with slip stitch")
    is_turned: bool = Field(default=False, description="Whether work is turned at end of row/round")
    line_number: int = Field(default=1)

class TerminologyStandard(str, Enum):
    US = "US"
    UK = "UK"

class CrochetPatternAST(BaseModel):
    title: str = Field(default="Crochet Pattern")
    terminology: TerminologyStandard = Field(default=TerminologyStandard.US)
    is_circular: bool = Field(default=True, description="True if predominantly rounds, False if rows")
    units: List[PatternUnit] = Field(default_factory=list)
    total_units: int = Field(default=0)
    raw_text: str = Field(default="")
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Visual Chart Graph Types
class ChartNode(BaseModel):
    id: str
    unit_type: UnitType
    unit_index: int
    stitch_index: int
    stitch_type: StitchType
    symbol_name: str
    x: float
    y: float
    rotation: float = 0.0  # In degrees
    target_loop: LoopTarget = LoopTarget.BOTH
    color: Optional[str] = None
    label: Optional[str] = None
    parent_ids: List[str] = Field(default_factory=list, description="IDs of base stitches worked into")
    line_number: int = 1

class ChartLink(BaseModel):
    id: str
    source_id: str
    target_id: str
    link_type: str = "base"  # "base" (into previous round/row), "chain" (horizontal link), "join" (sl st)

class ChartGraph(BaseModel):
    pattern_title: str
    is_circular: bool
    nodes: List[ChartNode] = Field(default_factory=list)
    links: List[ChartLink] = Field(default_factory=list)
    bounds: Dict[str, float] = Field(default_factory=lambda: {"min_x": -100, "max_x": 100, "min_y": -100, "max_y": 100, "width": 200, "height": 200})
    total_stitches: int = 0
    units_count: int = 0
    legend: List[Dict[str, str]] = Field(default_factory=list)
