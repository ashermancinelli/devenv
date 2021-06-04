from abc import *
from typing import List, Dict

class Command(ABC):
    def __init__(self, args: List[str], configs: Dict[str, str]):
        self.args = args
        self.configs = configs

    @abstractmethod
    def run(self):
        ...
