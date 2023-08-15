from abc import ABC, abstractmethod


class CreateUpdateProcessor(ABC):
    """Clase que es de ayuda en cuanto a procesos de creacion y actualizacion"""

    @abstractmethod
    def create_or_update_process(self) -> None:
        pass
