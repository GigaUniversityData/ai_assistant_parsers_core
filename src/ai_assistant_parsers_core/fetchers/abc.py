import abc


class ABCFetcher(abc.ABC):
    @abc.abstractmethod
    async def fetch(self, url: str) -> str:
        pass

    @abc.abstractmethod
    async def open(self) -> None:
        pass

    @abc.abstractmethod
    async def close(self) -> None:
        pass

    @abc.abstractmethod
    def is_open(self) -> bool:
        pass
