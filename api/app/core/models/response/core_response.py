from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, TypeVar


class CoreStatus(Enum):
    # can be filled with different cases that all
    # eventually get mapped to http status codes
    SUCCESSFUL_GET = auto()
    SUCCESSFUL_POST = auto()
    UNSUCCESSFUL_GET = auto()
    UNSUCCESSFUL_POST = auto()
    INVALID_REQUEST = auto()


T = TypeVar("T")


@dataclass
class CoreResponse(Generic[T]):
    response_content: T
    status: CoreStatus = CoreStatus.SUCCESSFUL_GET
    message: str = ""
