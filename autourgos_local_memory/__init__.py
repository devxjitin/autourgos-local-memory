"""
autourgos-local-memory — Disk-backed memory for Autourgos agents (JSON and SQLite).

    from autourgos_local_memory import LocalShortTermMemory, SQLiteMemory
"""
import logging

from .memory import LocalShortTermMemory, SQLiteMemory

logger = logging.getLogger(__name__)

try:
    from importlib.metadata import version as _v
    __version__ = _v("autourgos-local-memory")
except Exception:
    logger.debug("could not resolve installed version for autourgos-local-memory", exc_info=True)
    __version__ = "2.1.1"

__all__ = ["LocalShortTermMemory", "SQLiteMemory"]
