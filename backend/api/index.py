"""
Vercel serverless function entry point.
Exports the FastAPI application for Vercel's Python runtime.
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
# This allows imports like 'from main import app' to work
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from main import app

# Vercel expects 'app' or 'handler'
handler = app
