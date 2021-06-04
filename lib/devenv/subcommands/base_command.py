from abc import *
from typing import List, Dict

class Command(ABC):
    def __init__(self, args: List[str], config: Dict[str, str]):
        self.args = args
        self.config = config

    @abstractmethod
    def run(self):
        ...
