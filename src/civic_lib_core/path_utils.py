"""Path utilities.

File: civic_lib_core/path_utils.py
"""

import warnings as _w

from .fs_utils import ensure_dir as ensure_dir

_w.warn(
    "civic_lib_core.path_utils is deprecated; use civic_lib_core.fs_utils",
    DeprecationWarning,
    stacklevel=2,
)
