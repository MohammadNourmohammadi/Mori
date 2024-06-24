from abc import ABC, abstractmethod
from typing import Union, List
import PIL
from encoder import Encoder

class VectorDatabase(ABC):

    def __init__(self, encoder: Encoder) -> None:
        super().__init__()
        self.encoder = encoder

    def set(self, product: dict):
        raise NotImplemented
    
    def get(self, text: str):
        raise NotImplemented
    
class TextDatabase(ABC):

    def set(self, product: dict):
        raise NotImplemented
    
    def get(self, text: str):
        raise NotImplemented