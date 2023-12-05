from abc import ABC, abstractmethod
from brel import QName, BrelLabel

class IReportElement(ABC):

    @abstractmethod
    def get_name(self) -> QName:
        raise NotImplementedError
    
    @abstractmethod
    def get_labels(self) -> list[BrelLabel]:
        raise NotImplementedError
    
    @abstractmethod
    def _add_label(self, label: BrelLabel):
        raise NotImplementedError