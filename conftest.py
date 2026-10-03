"""
Pytest root configuration file.
Adds project directory to sys.path for seamless import resolution across environments.
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
