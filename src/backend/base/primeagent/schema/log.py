from typing import Any, Literal, TypeAlias

from primeagent.schema.message import ContentBlock, Message
from primeagent.schema.playground_events import PlaygroundEvent
from pydantic import BaseModel
from typing_extensions import Protocol

LoggableType: TypeAlias = str | dict | list | int | float | bool | BaseModel | PlaygroundEvent | None


class LogFunctionType(Protocol):
    def __call__(self, message: LoggableType | list[LoggableType], *, name: str | None = None) -> None: ...


class SendMessageFunctionType(Protocol):
    async def __call__(
        self,
        message: Message | None = None,
        text: str | None = None,
        background_color: str | None = None,
        text_color: str | None = None,
        icon: str | None = None,
        content_blocks: list[ContentBlock] | None = None,
        format_type: Literal["default", "error", "warning", "info"] = "default",
        id_: str | None = None,
        *,
        allow_markdown: bool = True,
    ) -> Message: ...


class OnTokenFunctionType(Protocol):
    def __call__(self, data: dict[str, Any]) -> None: ...
