from abc import ABC, abstractmethod
from typing import Any

from loguru import logger


class Agent(ABC):
    auth: dict[str, str | int | None]
    client: Any
    agent_type: str
    is_builtin: bool

    def __init__(self) -> None:
        self.auth = {}

    @abstractmethod
    def authenticate(self, auth: dict[str, str | int | None]) -> None:
        logger.warning("`authenticate` should be properly initialized!")

    @abstractmethod
    def copy_files(self, files: list[tuple[str, str]], dest_folder: str, remote_machine: str) -> bool:
        logger.warning("`copy_files` should be properly initialized")

    @abstractmethod
    def create_backup(self, source_folder: str, dest_folder: str) -> bool:
        logger.warning("`create_backup` should be properly initialized")

    @abstractmethod
    def move_final(self, source_folder: str, dest_folder: str) -> bool:
        logger.warning("`move_final` should be properly initialized")

    @abstractmethod
    def run_commands(self, commands: list[str]) -> None:
        logger.warning("`run_before` should be properly initialized")

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        logger.warning("`get_name` should be properly initialized")
