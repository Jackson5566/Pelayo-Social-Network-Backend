from abc import abstractmethod, ABC


class CreateUpdate(ABC):
    """Clase que es de ayuda en cuanto a procesos de creacion y actualizacion"""

    @abstractmethod
    def create_or_update_process(self) -> None:
        pass
