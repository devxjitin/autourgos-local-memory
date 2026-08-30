# autourgos-local-memory

Disk-backed memory for [Autourgos](https://github.com/devxjitin) agents.

Two classes — a JSON file store and a SQLite store. Memory survives process restarts and can be shared across sessions.

---

## Install

```bash
pip install autourgos-local-memory
```

---

## Quick Start

`my_llm` below is any chat-model instance, e.g. `OpenAIChatModel` from `autourgos-openaichat` (`pip install autourgos-openaichat`, needs `OPENAI_API_KEY` set).

## Classes

### LocalShortTermMemory — JSON file

Persists messages as a JSON array. Safe for multiple threads. Uses atomic write (tmp → replace) and a file-level lock to prevent corruption.

```python
from autourgos_local_memory import LocalShortTermMemory
from autourgos_agent import Agent
from autourgos_openaichat import OpenAIChatModel

my_llm = OpenAIChatModel(model="gpt-4o-mini")
memory = LocalShortTermMemory(
    file_path="./data/session.json",
    max_messages=50,
)
agent = Agent(llm=my_llm, memory=memory)
agent.invoke("Remember: my project deadline is Friday")

# Next session — history is loaded from disk automatically
agent2 = Agent(llm=my_llm, memory=LocalShortTermMemory(file_path="./data/session.json"))
agent2.invoke("When is my deadline?")
# → "Your project deadline is Friday."
```

### SQLiteMemory — SQLite database

WAL-mode SQLite. Safer than JSON for concurrent writes — no external lock file needed. Efficient for large histories.

```python
from autourgos_local_memory import SQLiteMemory

memory = SQLiteMemory(
    db_path="./data/agent.db",
    max_messages=500,  # None for unlimited
)
agent = Agent(llm=my_llm, memory=memory)
```

Use `":memory:"` for an ephemeral in-process database (useful for tests):

```python
memory = SQLiteMemory(db_path=":memory:")
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

## Known limitations

`LocalShortTermMemory`'s file lock is timeout-based (a lock file plus a wait deadline), not an OS-level advisory lock. If one process holds the lock longer than `lock_timeout_seconds` (e.g. due to slow disk I/O), a second process can end up believing the lock is stale and write concurrently, risking corruption. For high-concurrency multi-process use, prefer `SQLiteMemory` instead — it uses WAL-mode SQLite, which handles concurrent writers safely without relying on a timeout.

---

## Links

- PyPI: https://pypi.org/project/autourgos-local-memory/
- GitHub: https://github.com/devxjitin/autourgos-local-memory
- Issues: https://github.com/devxjitin/autourgos-local-memory/issues

---

## License

MIT — see [LICENSE](LICENSE)
