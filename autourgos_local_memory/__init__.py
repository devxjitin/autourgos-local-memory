"""
autourgos-local-memory — Disk-backed memory for Autourgos agents (JSON and SQLite).

    from autourgos_local_memory import LocalShortTermMemory, SQLiteMemory
"""
import logging

from .memory import LocalShortTermMemory, SQLiteMemory

logger = logging.getLogger(__name__)

from autourgos_core import package_version

__version__ = package_version("autourgos-local-memory", fallback="2.1.3", logger=logger)

__all__ = ["LocalShortTermMemory", "SQLiteMemory"]
