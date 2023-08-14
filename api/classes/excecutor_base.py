from abc import ABC, abstractmethod


class ExecutorBase(ABC):
    @abstractmethod
    def start_process(self):
        pass
