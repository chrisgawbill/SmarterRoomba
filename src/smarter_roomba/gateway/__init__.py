from typing import Protocol


class RobotTransport(Protocol):
    """Hardware-neutral byte transport owned by the gateway layer."""

    def read(self, size: int = -1) -> bytes: ...

    def write(self, data: bytes) -> int: ...
