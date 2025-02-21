import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from project_muse.db import init_db

@pytest.fixture(autouse=True)
def setup_test_db():
    """Setup test database connection"""
    init_db() 