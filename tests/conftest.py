"""Pytest fixtures for the file-janitor test suite.

The tests cover the pure scanning/deletion logic only, never the tkinter
GUI. tkinter is stubbed out so the suite runs headless (e.g. in CI).
"""

import sys
from unittest.mock import MagicMock

_tk = MagicMock(name="tkinter")
_tk.filedialog = MagicMock(name="tkinter.filedialog")
sys.modules.setdefault("tkinter", _tk)
sys.modules.setdefault("tkinter.filedialog", _tk.filedialog)
