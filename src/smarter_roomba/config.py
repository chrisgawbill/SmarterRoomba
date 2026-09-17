import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 8080

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "ServerConfig":
        env = os.environ if env is None else env
        raw_port = env.get("SMARTER_ROOMBA_PORT", str(cls.port))
        try:
            port = int(raw_port)
        except ValueError as error:
            raise ValueError("SMARTER_ROOMBA_PORT must be an integer") from error
        if not 1 <= port <= 65535:
            raise ValueError("SMARTER_ROOMBA_PORT must be between 1 and 65535")
        return cls(host=env.get("SMARTER_ROOMBA_HOST", cls.host), port=port)
