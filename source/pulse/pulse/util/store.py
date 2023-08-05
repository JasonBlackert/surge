from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Protocol


class Store(Protocol):
    def list_curr_solarleafs(self) -> list[str]:
        ...

    def select_telemetry(self, measure: str) -> dict[str, Any]:
        ...


_store_ctxvar = ContextVar[Store]("current_store")


def use_store():
    return _store_ctxvar.get()


@contextmanager
def store_context(store: Store):
    t = _store_ctxvar.set(store)

    try:
        yield
    finally:
        _store_ctxvar.reset(t)
