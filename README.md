# autourgos-local-memory

[![Framework: Autourgos](https://img.shields.io/badge/Framework-Autourgos-orange.svg)](https://github.com/devxjitin)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/autourgos-local-memory/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/devxjitin/autourgos-local-memory/blob/main/LICENSE)
[![Author](https://img.shields.io/badge/Author-Jitin%20Kumar%20Sengar-blue.svg)](https://github.com/devxjitin)
[![Contributor](https://img.shields.io/badge/Contributor-Sonia-blueviolet.svg)](https://github.com/dahiyasonia)
[![Contributor](https://img.shields.io/badge/Contributor-Vishwanil%20Suman-blueviolet.svg)]()

Disk-backed memory for [Autourgos](https://github.com/devxjitin) agents. Two classes — a JSON file store and
a SQLite store. Memory survives process restarts and can be shared across sessions.

```python
from autourgos_local_memory import SQLiteMemory
from autourgos_agent import Agent
from autourgos_openaichat import OpenAIChatModel

my_llm = OpenAIChatModel(model="gpt-4o-mini")
memory = SQLiteMemory(db_path="./data/agent.db", max_messages=500)
agent  = Agent(llm=my_llm, memory=memory)
```

---

## Features

- **`LocalShortTermMemory`** — JSON file, atomic write (tmp → replace), file-level lock
- **`SQLiteMemory`** — WAL-mode SQLite, safer than JSON under concurrent writes, efficient for large histories
- Both implement `autourgos_memory.BaseMemory` — drop-in for `Agent(memory=...)`
- `":memory:"` for an ephemeral in-process SQLite database (useful for tests)

---

## Table of Contents

- [Install](#install)
- [Classes](#classes)
- [Parameters](#parameters)
- [Known Limitations](#known-limitations)
- [License](#license)

---

## Install

```bash
pip install autourgos-local-memory
```

---

## Classes

### LocalShortTermMemory — JSON file

Persists messages as a JSON array. Safe for multiple threads. Uses atomic write (tmp → replace) and a
file-level lock to prevent corruption.

```python
from autourgos_local_memory import LocalShortTermMemory
from autourgos_agent import Agent
from autourgos_openaichat import OpenAIChatModel

my_llm = OpenAIChatModel(model="gpt-4o-mini")
memory = LocalShortTermMemory(file_path="./data/session.json", max_messages=50)
agent = Agent(llm=my_llm, memory=memory)
agent.invoke("Remember: my project deadline is Friday")

# Next session — history is loaded from disk automatically
agent2 = Agent(llm=my_llm, memory=LocalShortTermMemory(file_path="./data/session.json"))
agent2.invoke("When is my deadline?")
# → "Your project deadline is Friday."
```

### SQLiteMemory — SQLite database

WAL-mode SQLite. Safer than JSON for concurrent writes — no external lock file needed. Efficient for large
histories.

```python
from autourgos_local_memory import SQLiteMemory

memory = SQLiteMemory(db_path="./data/agent.db", max_messages=500)  # None for unlimited
agent = Agent(llm=my_llm, memory=memory)
```

Use `":memory:"` for an ephemeral in-process database:

```python
memory = SQLiteMemory(db_path=":memory:")
```

`SQLiteMemory` supports the context-manager protocol, closing its connection automatically:

```python
with SQLiteMemory(db_path="./data/agent.db") as memory:
    agent = Agent(llm=my_llm, memory=memory)
    agent.invoke("Hello!")
# connection is closed here automatically
```

---

## Parameters

### LocalShortTermMemory

| Parameter | Type | Default | Description |
|---|---|---|---|
| `file_path` | str | `"./data/local_memory.json"` | Path to JSON file. Created if missing. |
| `max_messages` | int | `20` | Rolling cap — oldest pruned on each write. |
| `name` | str | `"local"` | Human-readable identifier. |
| `lock_timeout_seconds` | float | `10.0` | Seconds to wait for file lock. |

### SQLiteMemory

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_path` | str | `"./data/autourgos_memory.db"` | Path to `.db` file. `":memory:"` for ephemeral. |
| `max_messages` | int or None | `500` | Rolling cap. `None` = unlimited. |
| `name` | str | `"sqlite"` | Human-readable identifier. |

---

## Known Limitations

`LocalShortTermMemory`'s file lock is timeout-based (a lock file plus a wait deadline), not an OS-level
advisory lock. If one process holds the lock longer than `lock_timeout_seconds` (e.g. due to slow disk I/O),
a second process can end up believing the lock is stale and write concurrently, risking corruption. For
high-concurrency multi-process use, prefer `SQLiteMemory` instead — it uses WAL-mode SQLite, which handles
concurrent writers safely without relying on a timeout.

---

## License

Apache License 2.0, Copyright (c) 2026 Jitin Kumar Sengar
