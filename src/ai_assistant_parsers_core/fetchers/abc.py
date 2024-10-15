import abc


class ABCFetcher(abc.ABC):
    @abc.abstractmethod
    async def fetch(self, url: str) -> str:
        pass
