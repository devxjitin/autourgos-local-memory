# Changelog

## [2.1.1] - 2026-09-01

- Metadata: added `maintainers` (Sonia, Vishwanil Suman) to `pyproject.toml`,
  and linked the README's existing Sonia contributor badge to her GitHub
  profile (https://github.com/dahiyasonia). No code changes.

## [2.1.0] - 2026-09-01

- Fixed: `_load()` (used by `get_messages()`/`format_for_llm()`) raised
  uncaught on a corrupted JSON file, while `add_message()` silently
  recovered by resetting to an empty list — inconsistent handling of the
  same corruption depending on which method touched the file first.
  `_load()` now recovers the same way.
- Added: `SQLiteMemory` supports the context-manager protocol
  (`with SQLiteMemory(...) as mem:`), closing its connection automatically.

## [2.0.1] - 2026-07-27

- Added: module logger, used to warn on corrupted memory-file JSON. Docs: added explicit Quick Start heading, fixed the undefined my_llm placeholder, and documented the timeout-based file lock's known concurrency limitation.

All notable changes to `autourgos-local-memory` are documented here.

---

## [2.0.0] - 2026-07-27

### Changed
- BREAKING: this package now depends on `autourgos-memory>=1.0.1` (previously zero-dependency). `BaseMemory`/`BaseRetriever`/`Document`/`MemoryMessage` are now re-exported from `autourgos-memory` instead of duplicated locally. No public API/behavior change for typical usage.

## [1.0.1] - 2026-07-27

### Fixed
- `__version__` fallback in `__init__.py` now matches `pyproject.toml` (was incorrectly `1.0.2`, now `1.0.0`).
- Wording correction: CHANGELOG previously referenced a non-existent `autourgos-core` package; now correctly states there is no dependency on `autourgos-memory` or any other Autourgos package.

## [1.0.0] - 2026-06-17

### Added
- Initial release.
- File-backed (JSON) and SQLite memory implementations.
- Self-contained package — no dependency on `autourgos-memory` or any other Autourgos package.
- All base interfaces (`BaseMemory`, `BaseRetriever`, `MemoryMessage`, `Document`) inlined.
- Thread-safe implementation using `threading.RLock`.
- Full type annotations and `py.typed` marker.

