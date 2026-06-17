"""
autourgos-local-memory — Disk-backed memory for Autourgos agents (JSON and SQLite).

    from autourgos_local_memory import LocalShortTermMemory, SQLiteMemory
"""
from .memory import LocalShortTermMemory, SQLiteMemory

try:
    from importlib.metadata import version as _v
    __version__ = _v("autourgos-local-memory")
except Exception:
    __version__ = "1.0.1"

__all__ = ["LocalShortTermMemory", "SQLiteMemory"]
