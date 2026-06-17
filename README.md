# autourgos-local-memory

Disk-backed memory for [Autourgos](https://github.com/devxjitin) agents.

Two classes — a JSON file store and a SQLite store. Memory survives process restarts and can be shared across sessions.

---

## Install

```bash
pip install autourgos-local-memory
```

---

## Classes

### LocalShortTermMemory — JSON file

Persists messages as a JSON array. Safe for multiple threads. Uses atomic write (tmp → replace) and a file-level lock to prevent corruption.

```python
from autourgos_local_memory import LocalShortTermMemory
from autourgos_react_agent import ReactAgent

memory = LocalShortTermMemory(
    file_path="./data/session.json",
    max_messages=50,
)
agent = ReactAgent(llm=my_llm, memory=memory)
agent.invoke("Remember: my project deadline is Friday")

# Next session — history is loaded from disk automatically
agent2 = ReactAgent(llm=my_llm, memory=LocalShortTermMemory(file_path="./data/session.json"))
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
agent = ReactAgent(llm=my_llm, memory=memory)
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

## Links

- PyPI: https://pypi.org/project/autourgos-local-memory/
- GitHub: https://github.com/devxjitin/autourgos-local-memory
- Issues: https://github.com/devxjitin/autourgos-local-memory/issues

---

## License

MIT — see [LICENSE](LICENSE)
