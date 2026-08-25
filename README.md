# Crochart Visualizer 🧶✨

> **Interactive Crochet Pattern Visualizer, AST Parser, Diagnostic Engine & 2D Vector Chart Studio**

Crochart Visualizer is a full-stack developer and designer tool designed to parse textual crochet patterns, validate their mathematical and structural consistency, and compile them into interactive 2D vector crochet charts compliant with **Craft Yarn Council (CYC)** standard symbology.

---

## 🌟 Key Features

### 1. 🧠 Intelligent Pattern Lexer & AST Parser
- **Dual Terminology**: Full support for both **US** (`sc`, `hdc`, `dc`, `tr`, etc.) and **UK** (`dc`, `htr`, `tr`, `dtr`, etc.) crochet nomenclature with automated conversion.
- **Repeat Syntax Support**: Recursively parses complex repeats such as `[inc, 2 sc] * 6`, `(sc, inc) 3 times`, `*ch 3, sk 1, sc in next st; rep from * to end`.
- **Structural Units**: Automatically detects working in continuous/joined rounds (magic ring, chain rings) or flat rows with turning chains.

### 2. 🔍 Diagnostic & Validation Engine
- **Stitch Arithmetic Audit**: Verifies stitch count changes round-by-round (e.g., matching claimed stitch counts `(36)` with computed produced stitches).
- **Base Consumption Checking**: Validates that stitches generated in round $N$ consume the exact number of base stitches provided by round $N-1$.
- **Real-Time Issue Reporting**: Categorizes issues by severity (`ERROR`, `WARNING`, `INFO`) with exact line numbers and actionable auto-fix suggestions.

### 3. 🎨 Interactive Vector Chart Canvas (CYC Standards)
- **Radial & Cartesian Layouts**:
  - **Radial / Concentric Circles**: Layout engine for circular patterns (amigurumi, coasters, mandalas) with radial projection and angle distribution.
  - **Cartesian Grid**: Alternating left-to-right / right-to-left rows for blankets, scarves, and flat panels.
- **Standard Symbols**: Rendered using official Craft Yarn Council vector definitions for chains, single crochet, increases, decreases, clusters, picots, and slip stitches.
- **Canvas Interaction**: Smooth zooming, panning, reset controls, and interactive stitch inspection on click/hover.

### 4. ⏱️ Stitch-by-Stitch Playback Animator
- Step through your pattern stitch by stitch or animate progression at adjustable speeds.
- Highlights active rounds, current stitch position, and attachment links to base stitches in real time.

### 5. 🤖 ML Studio & Synthetic Dataset Generator
- **Synthetic Generator**: Generate hundreds of randomized, structurally valid or corrupted crochet patterns with configurable complexity, noise, and error injection.
- **Evaluation Pipeline**: Benchmark parsing engines and ML models against ground-truth ASTs measuring stitch precision, recall, F1 score, and AST exact match accuracy.

### 6. 💾 Project Management & Multi-Format Exporter
- **Project Persistence**: Save, rename, organize, and reload crochet patterns via an embedded SQLite database.
- **Export Options**: Export charts to high-resolution **SVG**, **PNG**, **PDF documents with pattern summaries**, or raw **JSON AST/Graph** data.

---

## 🏗️ Architecture

```
Crochart Visualizer
├── backend/                       # FastAPI Python Backend
│   ├── app/
│   │   ├── api/routes/           # API routes (parse, chart, projects, datasets, samples, export)
│   │   ├── core/                 # App configuration & SQLite database setup
│   │   ├── layout/               # Radial and Cartesian 2D coordinate graph layout engines
│   │   ├── ml/                   # Synthetic dataset generator & parser evaluation pipeline
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── ontology/             # Crochet stitch vocabulary, schema & CYC symbols
│   │   ├── parser/               # Preprocessor, Tokenizer, and AST compiler
│   │   ├── samples/              # Built-in curated pattern library
│   │   └── validator/            # Static analysis, stitch math & diagnostic rules
│   ├── tests/                    # Comprehensive Pytest test suite
│   ├── main.py                   # FastAPI application entrypoint
│   └── requirements.txt          # Python dependencies
│
└── frontend/                      # React 18 + TypeScript + Vite Frontend
    ├── src/
    │   ├── components/
    │   │   ├── Canvas/           # Vector canvas, CYC symbols & playback animator
    │   │   ├── Diagnostics/      # Error & warning diagnostics panel
    │   │   ├── Editor/           # Code editor with syntax highlights & file upload
    │   │   ├── Export/           # Vector & document export modal (SVG/PNG/PDF/JSON)
    │   │   ├── Gallery/          # Built-in sample pattern library modal
    │   │   ├── MLStudio/         # Synthetic generator & evaluation benchmark studio
    │   │   └── Projects/         # Saved projects management modal
    │   ├── services/             # Backend API client
    │   ├── types/                # TypeScript interfaces for AST, Graphs, Diagnostics
    │   ├── App.tsx               # Main layout orchestrator
    │   └── index.css             # Dark/Light responsive glassmorphic design system
    ├── package.json
    └── vite.config.ts
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**

---

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

The backend server will start at `http://localhost:8000`.
- Interactive Swagger API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

---

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Open `http://localhost:5173` in your browser to start visualizing and designing crochet charts.

---

## 🧪 Running Tests

The backend includes a comprehensive unit and integration test suite covering the AST parser, diagnostic rules, layout engines, ML evaluation, and sample presets.

```bash
# Run pytest in the backend directory
cd backend
pytest
```

---

## 📊 Supported Crochet Stitches (Craft Yarn Council)

| Symbol / Abbr (US) | Name (US) | UK Equivalent | Produced Count | Base Consumed |
| :--- | :--- | :--- | :---: | :---: |
| `mr` / `magic ring` | Magic Ring / Circle | Magic Ring | 0 | 0 |
| `ch` | Chain Stitch | Chain Stitch | 1 | 0 |
| `sl st` | Slip Stitch | Slip Stitch | 1 | 1 |
| `sc` | Single Crochet | Double Crochet (`dc`) | 1 | 1 |
| `hdc` | Half Double Crochet | Half Treble Crochet (`htr`) | 1 | 1 |
| `dc` | Double Crochet | Treble Crochet (`tr`) | 1 | 1 |
| `tr` / `tc` | Treble Crochet | Double Treble Crochet (`dtr`)| 1 | 1 |
| `inc` | Increase (2 sc in 1 st)| Increase | 2 | 1 |
| `dec` / `sc2tog` | Decrease (sc 2 together)| Decrease (`dc2tog`) | 1 | 2 |
| `picot` | Picot Stitch | Picot Stitch | 1 | 1 |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
