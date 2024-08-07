from dataclasses import dataclass

from src.application.exceptions.base import ApplicationException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(ApplicationException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для события: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(ApplicationException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды: {self.command_type}"
