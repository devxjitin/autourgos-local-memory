# autourgos-local-memory — Features

Disk-backed short-term conversation memory for Autourgos agents. Two classes — a JSON-file store and a WAL-mode SQLite store — so agent history survives process restarts and can be shared across sessions without standing up an external database.

## Full Feature List

- **`LocalShortTermMemory`** — JSON file persistence, atomic write (write to tmp file, then replace), file-level lock (`lock_timeout_seconds`, default 10s), rolling `max_messages` cap (oldest pruned on each write)
- **`SQLiteMemory`** — WAL-mode SQLite; safer than the JSON store under concurrent writers, no external lock file needed, efficient for large histories; rolling `max_messages` cap (`None` = unlimited)
- `":memory:"` supported as `db_path` for an ephemeral in-process SQLite database — useful for tests, no cleanup needed
- Both implement `autourgos_memory.BaseMemory` — drop-in for `Agent(memory=...)`, same interface as the rest of the memory family
- `SQLiteMemory` supports the context-manager protocol (`with SQLiteMemory(...) as memory:`), closing the connection automatically
- Documented known limitation: `LocalShortTermMemory`'s lock is a timeout-based lock file, not an OS-level advisory lock — under high concurrency across processes a stale-lock race is possible, and the README explicitly recommends `SQLiteMemory` for that case instead

## Competitor Comparison

Landscape research on lightweight local/embedded persistent chat-history stores, current as of the search date.

| Capability | **autourgos-local-memory** | [LangChain `FileChatMessageHistory`](https://python.langchain.com/) | [LangChain `SQLChatMessageHistory`](https://python.langchain.com/) | [LangGraph `SqliteSaver`/`PostgresSaver`](https://langchain-ai.github.io/langgraph/) | [Redis-backed chat history (e.g. `RedisChatMessageHistory`)](https://python.langchain.com/) |
|---|---|---|---|---|---|
| Scope | Standalone library, zero external services | Part of LangChain core | Part of LangChain core, needs a DB connection string | Part of LangGraph's checkpoint system | Part of LangChain core, needs a running Redis server |
| Storage backend | JSON file or SQLite file, both local, no server | Local JSON file | Any SQLAlchemy-supported DB (often external) | SQLite file or Postgres (external for Postgres) | External Redis instance |
| Zero external infrastructure required | Yes, for both classes | Yes | Only if pointed at a local SQLite file | Yes with SQLite, no with Postgres | No — Redis must be running |
| Atomic write safety documented | Yes, explicit tmp→replace + file lock (JSON class), WAL mode (SQLite class) | Not documented as atomic | Delegated to the underlying DB engine | Delegated to the underlying DB engine (Postgres has real ACID guarantees; SQLite WAL is solid) | Delegated to Redis (single-command ops are atomic; multi-key sequences are not by default) |
| Concurrent multi-process write safety | Documented trade-off: JSON class is timeout-lock only (known limitation, SQLite recommended instead); SQLite class uses WAL mode | Not designed for concurrent multi-process writers | Depends on DB engine (generally good) | Good (real DB engines) | Good (Redis is single-threaded per command) |
| In-memory/ephemeral mode for tests | Yes, `db_path=":memory:"` | No direct equivalent (it's file-only) | Yes, via `sqlite:///:memory:` connection string | Yes, `MemorySaver` (a separate class in LangGraph) | No (would need a real or mocked Redis) |
| Rolling message cap built in | Yes, `max_messages` on both classes | No — caller manages pruning | No — caller manages pruning | No — full state snapshots, different model | No — caller manages pruning/expiry (Redis TTL can help) |
| Context manager for cleanup | Yes (`SQLiteMemory`) | N/A (no persistent connection) | N/A (connection managed by SQLAlchemy) | Yes (checkpointer context managers) | Depends on client setup |
| Dependencies | Zero beyond stdlib (`sqlite3`, `json`) | Full LangChain core | Full LangChain core + SQLAlchemy + DB driver | Full LangGraph/LangChain core (+ Postgres driver if used) | Full LangChain core + `redis` client |
| Pricing | Free, open source | Free, open source | Free, open source (DB hosting cost varies) | Free, open source (Postgres hosting cost if used) | Free, open source (Redis hosting cost) |

### How to read this

- **vs. LangChain's file/SQL chat histories**: closest functional match. autourgos-local-memory's edge is being explicit and tested about the failure mode that matters for local files — atomic writes and lock behavior — and documenting its own limitation (timeout-lock races) honestly rather than leaving it implicit.
- **vs. LangGraph's checkpointers**: LangGraph persists full graph/execution state (for resumability and time-travel), not just a chat message list — a heavier, more powerful primitive if you're already on LangGraph, overkill if you just want durable chat history for a single-agent setup.
- **vs. Redis-backed history**: Redis buys you a shared, low-latency, multi-process/multi-host store, but it's infrastructure you have to run; autourgos-local-memory intentionally trades that scalability for "no server, just a file," which is the right call for single-host or single-user agent deployments.
- **Zero-dependency angle**: this package (and the whole Autourgos memory family) treats "no framework, no server, `pip install` and go" as a design constraint, which is real differentiation against every LangChain/LangGraph-based alternative here — they all pull in a large framework even for a simple persisted chat log.

Sources:
- [LangChain Memory Component Deep Dive: Chain Components and Runnable Study](https://dev.to/jamesli/langchain-memory-component-deep-dive-chain-components-and-runnable-study-359p)
- [How to Implement LangChain Memory](https://oneuptime.com/blog/post/2026-01-27-langchain-memory/view)
- [LangGraph Memory vs Mem0: Which Should You Use in 2026?](https://atlan.com/know/ai-agent/ai-agent-memory/langgraph-memory-vs-mem0/)
- [LangGraph vs LangChain: Which to Use for Production AI Agents in 2026](https://www.spheron.network/blog/langgraph-vs-langchain/)
