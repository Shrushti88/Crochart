"""
Comprehensive library of 20+ crochet patterns across amigurumi, flat circles, granny squares, motifs, and row fabrics.
"""

from typing import List, Dict, Any

SAMPLE_PATTERNS: List[Dict[str, Any]] = [
    {
        "id": "traditional-circle-stacked",
        "title": "Traditional Crochet Circle (Stacked Increases)",
        "category": "Circular",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "10-round traditional flat crochet circle with 6 stacked increase spokes radiating outward in a pinwheel spiral.",
        "pattern": """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [inc, sc] * 6 (18)
Round 4: [inc, 2 sc] * 6 (24)
Round 5: [inc, 3 sc] * 6 (30)
Round 6: [inc, 4 sc] * 6 (36)
Round 7: [inc, 5 sc] * 6 (42)
Round 8: [inc, 6 sc] * 6 (48)
Round 9: [inc, 7 sc] * 6 (54)
Round 10: [inc, 8 sc] * 6 (60)"""
    },
    {
        "id": "amigurumi-sphere",
        "title": "Classic Amigurumi Sphere",
        "category": "Amigurumi",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "Standard 6-stitch amigurumi ball with increases, even rounds, and decreases.",
        "pattern": """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [sc, inc] * 6 (18)
Round 4: [2 sc, inc] * 6 (24)
Round 5: [3 sc, inc] * 6 (30)
Round 6: 30 sc (30)
Round 7: 30 sc (30)
Round 8: [3 sc, dec] * 6 (24)
Round 9: [2 sc, dec] * 6 (18)
Round 10: [sc, dec] * 6 (12)
Round 11: [dec] * 6 (6)"""
    },
    {
        "id": "flat-circle-dc",
        "title": "Flat Double Crochet Circle",
        "category": "Circular",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "12-stitch double crochet flat circle with joined rounds.",
        "pattern": """Round 1: Magic ring, 12 dc, sl st to first st to join (12)
Round 2: [dc inc] * 12, sl st to join (24)
Round 3: [dc, dc inc] * 12, sl st to join (36)
Round 4: [2 dc, dc inc] * 12, sl st to join (48)
Round 5: [3 dc, dc inc] * 12, sl st to join (60)"""
    },
    {
        "id": "classic-granny-square",
        "title": "Classic 4-Round Granny Square",
        "category": "Granny Squares & Motifs",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Traditional 3-dc granny clusters with corner chains.",
        "pattern": """Round 1: Magic ring, [3 dc, ch 2] * 4, sl st to join (12 dc, 4 ch-2 sp)
Round 2: [3 dc, ch 2, 3 dc, ch 1] * 4, sl st to join (24)
Round 3: [3 dc, ch 2, 3 dc, ch 1, 3 dc, ch 1] * 4, sl st to join (36)
Round 4: [3 dc, ch 2, 3 dc, ch 1, 3 dc, ch 1, 3 dc, ch 1] * 4, sl st to join (48)"""
    },
    {
        "id": "sunburst-granny-square",
        "title": "Sunburst Sunflower Motif",
        "category": "Granny Squares & Motifs",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Puff stitches and cluster petals expanding from a center circle into a square.",
        "pattern": """Round 1: Magic ring, 16 dc, sl st to join (16)
Round 2: [puff, ch 1] * 16, sl st to join (16)
Round 3: [cluster, ch 2] * 16, sl st to join (16)
Round 4: [3 tr, ch 3, 3 tr, 3 dc, 3 hdc, 3 dc] * 4, sl st to join (48)"""
    },
    {
        "id": "ripple-chevron-blanket",
        "title": "Chevron Ripple Wave Row",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Intermediate",
        "description": "Classic zig-zag chevron wave blanket row pattern with peaks and valleys.",
        "pattern": """Row 1: Ch 26, turn (26)
Row 2: 2 sc in 2nd ch from hook, [4 sc, dec, 4 sc, inc] * 2, sc in last ch, turn (25)
Row 3: Ch 1, 2 sc in first st, [4 sc in BLO, dec, 4 sc in BLO, inc] * 2, sc in last st, turn (25)
Row 4: Ch 1, 2 sc in first st, [4 sc in BLO, dec, 4 sc in BLO, inc] * 2, sc in last st, turn (25)"""
    },
    {
        "id": "heart-applique",
        "title": "Sweetheart Motif Applique",
        "category": "Appliques",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Single-round shaped crochet heart worked into a magic ring.",
        "pattern": """Round 1: Magic ring, ch 3, 3 tr, 3 dc, ch 1, 1 tr, ch 1, 3 dc, 3 tr, ch 3, sl st in ring (18)
Round 2: Sc 1, 2 hdc in next st, 3 dc in next st, 2 dc in next st, 3 sc, ch 1, dc in point, ch 1, 3 sc, 2 dc in next st, 3 dc in next st, 2 hdc in next st, sl st to join (28)"""
    },
    {
        "id": "hexagon-motif",
        "title": "Geometric Hexagon Motif",
        "category": "Granny Squares & Motifs",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Six-sided expanding crochet medallion with corner increases.",
        "pattern": """Round 1: Magic ring, [2 dc, ch 2] * 6, sl st to join (12)
Round 2: [2 dc, 2 dc in ch-sp, ch 2] * 6, sl st to join (24)
Round 3: [4 dc, 2 dc in ch-sp, ch 2] * 6, sl st to join (36)
Round 4: [6 dc, 2 dc in ch-sp, ch 2] * 6, sl st to join (48)"""
    },
    {
        "id": "star-ornament",
        "title": "5-Point Christmas Star Ornament",
        "category": "Appliques",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "5-pointed star motif with picot tips and double crochets.",
        "pattern": """Round 1: Magic ring, 10 sc, sl st to join (10)
Round 2: [inc] * 10, sl st to join (20)
Round 3: [sl st, sc, hdc, dc, tr, picot, tr, dc, hdc, sc] * 5, sl st to join (45)"""
    },
    {
        "id": "ribbed-beanie-row",
        "title": "Thermal Ribbed Beanie Swatch",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Beginner",
        "description": "Back Loop Only single crochet ribbed fabric for beanies and cuffs.",
        "pattern": """Row 1: Ch 20, turn (20)
Row 2: 19 sc in BLO, ch 1, turn (19)
Row 3: 19 sc in BLO, ch 1, turn (19)
Row 4: 19 sc in BLO, ch 1, turn (19)
Row 5: 19 sc in BLO, ch 1, turn (19)
Row 6: 19 sc in BLO, ch 1, turn (19)"""
    },
    {
        "id": "oval-shoe-sole",
        "title": "Oval Bootie Sole",
        "category": "Amigurumi",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Classic shoe sole worked in rounds around both sides of a foundation chain.",
        "pattern": """Round 1: Ch 10, 8 sc along chain, 3 sc in end ch, 7 sc along other side, inc in last ch (20)
Round 2: Inc, 7 sc, [inc] * 3, 7 sc, [inc] * 2 (26)
Round 3: 1 sc, inc, 7 sc, [sc, inc] * 3, 7 sc, [sc, inc] * 2 (32)
Round 4: 2 sc, inc, 7 sc, [2 sc, inc] * 3, 7 sc, [2 sc, inc] * 2 (38)"""
    },
    {
        "id": "flower-petal-coaster",
        "title": "8-Petal Blossom Coaster",
        "category": "Circular",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "Decorative drink coaster with curved 8-petal shell edge.",
        "pattern": """Round 1: Magic ring, 8 sc, sl st to join (8)
Round 2: [inc] * 8, sl st to join (16)
Round 3: [sc, inc] * 8, sl st to join (24)
Round 4: [2 sc, inc] * 8, sl st to join (32)
Round 5: [sk 1 st, 5 dc in next st, sk 1 st, sl st in next st] * 8 (48)"""
    },
    {
        "id": "beanie-crown-rounds",
        "title": "Top-Down Beanie Crown",
        "category": "Circular",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "Concentric Half Double Crochet crown for hats and beanies.",
        "pattern": """Round 1: Magic ring, 10 hdc, sl st to join (10)
Round 2: [hdc inc] * 10, sl st to join (20)
Round 3: [hdc, hdc inc] * 10, sl st to join (30)
Round 4: [2 hdc, hdc inc] * 10, sl st to join (40)
Round 5: [3 hdc, hdc inc] * 10, sl st to join (50)
Round 6: [4 hdc, hdc inc] * 10, sl st to join (60)"""
    },
    {
        "id": "shell-stitch-swatch",
        "title": "Classic Shell Stitch Row",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Intermediate",
        "description": "5-dc decorative shell stitch worked in alternating rows.",
        "pattern": """Row 1: Ch 21, turn (21)
Row 2: Sc in 2nd ch, [sk 2 ch, 5 dc in next ch, sk 2 ch, sc in next ch] * 3, turn (19)
Row 3: Ch 3, 2 dc in first st, [sk 2 sts, sc in next st, sk 2 sts, 5 dc in next st] * 2, sk 2 sts, sc in next st, sk 2 sts, 3 dc in last st, turn (19)
Row 4: Ch 1, sc in first st, [sk 2 sts, 5 dc in next st, sk 2 sts, sc in next st] * 3, turn (19)"""
    },
    {
        "id": "african-flower-motif",
        "title": "African Flower 6-Petal Hexagon",
        "category": "Granny Squares & Motifs",
        "is_circular": True,
        "difficulty": "Advanced",
        "description": "Rich 6-petal African flower motif with spike stitches and borders.",
        "pattern": """Round 1: Magic ring, [2 dc, ch 1] * 6, sl st to join (12)
Round 2: [2 dc in ch-sp, ch 1, 2 dc in same ch-sp] * 6, sl st to join (24)
Round 3: [7 dc in ch-sp] * 6, sl st to join (42)
Round 4: [7 sc in BLO, dc in round below] * 6, sl st to join (48)"""
    },
    {
        "id": "amigurumi-cone",
        "title": "Amigurumi Party Hat / Cone",
        "category": "Amigurumi",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "Gradual conical increase for amigurumi horns, hats, and limbs.",
        "pattern": """Round 1: Magic ring, 4 sc (4)
Round 2: [sc, inc] * 2 (6)
Round 3: 6 sc (6)
Round 4: [2 sc, inc] * 2 (8)
Round 5: 8 sc (8)
Round 6: [3 sc, inc] * 2 (10)
Round 7: 10 sc (10)
Round 8: [4 sc, inc] * 2 (12)"""
    },
    {
        "id": "v-stitch-mesh",
        "title": "V-Stitch Mesh Blanket Rows",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Beginner",
        "description": "(dc, ch 1, dc) V-stitches for lightweight blankets and summer wraps.",
        "pattern": """Row 1: Ch 20, turn (20)
Row 2: Dc in 4th ch from hook, [sk 1 ch, (dc, ch 1, dc) in next ch] * 7, sk 1 ch, dc in last ch, turn (18)
Row 3: Ch 3, [(dc, ch 1, dc) in ch-1 sp] * 7, dc in top of turning chain, turn (18)
Row 4: Ch 3, [(dc, ch 1, dc) in ch-1 sp] * 7, dc in top of turning chain, turn (18)"""
    },
    {
        "id": "picot-lace-edging",
        "title": "Picot Scalloped Lace Edging",
        "category": "Borders & Edgings",
        "is_circular": False,
        "difficulty": "Intermediate",
        "description": "Delicate picot lace border for blankets, towels, and shawls.",
        "pattern": """Row 1: Ch 24, turn (24)
Row 2: 23 sc, turn (23)
Row 3: [sc, sk 1 st, (2 dc, picot, 2 dc) in next st, sk 1 st] * 5, 3 sc (28)"""
    },
    {
        "id": "spiral-disk-coaster",
        "title": "Continuous Spiral Coaster (No Join)",
        "category": "Circular",
        "is_circular": True,
        "difficulty": "Beginner",
        "description": "Continuous spiral worked without slip-stitch joins.",
        "pattern": """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [sc, inc] * 6 (18)
Round 4: [2 sc, inc] * 6 (24)
Round 5: [3 sc, inc] * 6 (30)
Round 6: [4 sc, inc] * 6 (36)
Round 7: [5 sc, inc] * 6 (42)"""
    },
    {
        "id": "bobble-texture-row",
        "title": "Textured Bobble Accent Row",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Intermediate",
        "description": "Pop-out 3D bobble stitches spaced with single crochets.",
        "pattern": """Row 1: Ch 18, turn (18)
Row 2: 17 sc, turn (17)
Row 3: 2 sc, [bobble, 3 sc] * 3, bobble, 2 sc, turn (17)
Row 4: 17 sc, turn (17)
Row 5: 4 sc, [bobble, 3 sc] * 2, bobble, 4 sc, turn (17)
Row 6: 17 sc (17)"""
    },
    {
        "id": "leaf-applique",
        "title": "Botanical Leaf Applique",
        "category": "Appliques",
        "is_circular": True,
        "difficulty": "Intermediate",
        "description": "Tapered leaf shape with gradient stitches (sc -> hdc -> dc -> tr -> picot tip).",
        "pattern": """Round 1: Ch 12, sl st in 2nd ch, sc, hdc, 2 dc, 2 tr, 2 dc, hdc, (sc, picot, sc) in point, and work along other side: hdc, 2 dc, 2 tr, 2 dc, hdc, sc, sl st (24)"""
    },
    {
        "id": "corner-to-corner-c2c",
        "title": "Corner-to-Corner (C2C) Swatch",
        "category": "Rows & Blankets",
        "is_circular": False,
        "difficulty": "Advanced",
        "description": "Diagonal block expansion for pixel art graphghans and diagonal blankets.",
        "pattern": """Row 1: Ch 6, dc in 4th ch from hook, 2 dc in remaining chs, turn (3 dc)
Row 2: Ch 6, dc in 4th ch, 2 dc, sl st in ch-3 sp of row 1, ch 3, 3 dc in ch-3 sp, turn (6 dc)
Row 3: Ch 6, dc in 4th ch, 2 dc, [sl st in ch-3 sp, ch 3, 3 dc in same sp] * 2, turn (9 dc)
Row 4: Ch 6, dc in 4th ch, 2 dc, [sl st in ch-3 sp, ch 3, 3 dc in same sp] * 3, turn (12 dc)"""
    }
]
