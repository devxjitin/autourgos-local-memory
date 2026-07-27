"""Smoke tests for LocalShortTermMemory and SQLiteMemory."""
import os
import tempfile

from autourgos_local_memory import LocalShortTermMemory, SQLiteMemory


def test_local_short_term_memory_add_and_get(tmp_path):
    file_path = os.path.join(tmp_path, "mem.json")
    mem = LocalShortTermMemory(file_path=file_path, max_messages=10)
    mem.add_user_message("hello")
    mem.add_agent_message("hi there")
    msgs = mem.get_messages()
    assert [m.content for m in msgs] == ["hello", "hi there"]


def test_local_short_term_memory_rolling_cap(tmp_path):
    file_path = os.path.join(tmp_path, "mem.json")
    mem = LocalShortTermMemory(file_path=file_path, max_messages=2)
    mem.add_user_message("a")
    mem.add_user_message("b")
    mem.add_user_message("c")
    msgs = mem.get_messages()
    assert [m.content for m in msgs] == ["b", "c"]


def test_local_short_term_memory_clear(tmp_path):
    file_path = os.path.join(tmp_path, "mem.json")
    mem = LocalShortTermMemory(file_path=file_path)
    mem.add_user_message("x")
    mem.clear()
    assert mem.get_messages() == []


def test_sqlite_memory_add_get_clear():
    mem = SQLiteMemory(db_path=":memory:", max_messages=None)
    mem.add_user_message("hello")
    mem.add_agent_message("hi there")
    msgs = mem.get_messages()
    assert [m.content for m in msgs] == ["hello", "hi there"]
    mem.clear()
    assert mem.get_messages() == []
    mem.close()
