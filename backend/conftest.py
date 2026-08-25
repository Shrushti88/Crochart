import sys
from pathlib import Path

# Add backend root to sys.path
backend_root = Path(__file__).resolve().parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))
