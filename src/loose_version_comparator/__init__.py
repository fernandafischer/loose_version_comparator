"""Loose Version Comparator.

Public API:
    Version — parse a version string into a comparable value.
    compare — convenience function returning -1, 0, or +1.
"""

from .core import Version, compare

__all__ = ["Version", "compare"]
