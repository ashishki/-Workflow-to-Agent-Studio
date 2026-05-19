"""Shared tracing entry point."""

from __future__ import annotations

from contextlib import nullcontext


class NoopTracer:
    def start_as_current_span(self, _name: str) -> nullcontext[None]:
        return nullcontext()


def get_tracer() -> NoopTracer:
    return NoopTracer()
