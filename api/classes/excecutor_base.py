from abc import ABC, abstractmethod


class ExecutorBase(ABC):
    """Clase con propósito de ejecutar de obligar la implementacion de un proceso"""
    @abstractmethod
    def start_process(self):
        pass
