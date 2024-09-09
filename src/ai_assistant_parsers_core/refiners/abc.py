import abc


class ABCParsingRefiner(abc.ABC):
    @abc.abstractmethod
    def refine(self, html: str) -> str:
        pass
