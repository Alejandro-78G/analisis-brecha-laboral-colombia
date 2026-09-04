from abc import ABC, abstractmethod
from typing import Any
from src.transformers.schemas import VacanteSchema


class BaseExtractor(ABC):
    """
    Clase base abstracta para todos los extractores de datos de vacantes.
    """

    @abstractmethod
    async def extract(self, limit: int = 100) -> list[VacanteSchema]:
        """
        Extrae datos de la fuente configurada y retorna objetos validados por VacanteSchema.
        """
        pass
