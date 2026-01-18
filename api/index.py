"""
Vercel serverless function entry point.
Exports the FastAPI application for Vercel's Python runtime.
"""

import sys
from pathlib import Path

# Add the project root to Python path so 'backend' module can be imported
# This is necessary because Vercel runs from the api/ directory
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import the FastAPI app after setting up the path
from backend.main import app

# Vercel expects the ASGI app to be named 'app' or 'handler'
# The FastAPI app is already ASGI-compatible
handler = app
