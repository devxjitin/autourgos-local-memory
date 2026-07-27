"""
base.py — Re-exports BaseMemory, BaseRetriever, Document, and MemoryMessage
from autourgos-memory, the package that owns these interfaces, to avoid
divergent duplicate copies across the memory-family packages.
"""
from autourgos_memory import BaseMemory, BaseRetriever, Document, MemoryMessage

__all__ = ["BaseMemory", "BaseRetriever", "Document", "MemoryMessage"]
