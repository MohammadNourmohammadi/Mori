from abc import ABC, abstractmethod
from typing import Union, List
from PIL import Image
import PIL

class Encoder(ABC):

    @abstractmethod
    def encode_image(self, images: str):
        return NotImplemented
    
    @abstractmethod
    def encode_text(self, text: str):
        return NotImplemented


