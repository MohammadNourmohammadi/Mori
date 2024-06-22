from abc import abstractmethod, ABC

class Crawler(ABC):

    @abstractmethod
    def obtain_data(self):
        return NotImplemented
    
    @abstractmethod
    def get_data(self):
        return NotImplemented
    
