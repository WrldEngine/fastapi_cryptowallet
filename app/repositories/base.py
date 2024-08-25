from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_single(self, **kwargs):
        raise NotImplementedError


class AbsWalletRepository(ABC):

    @abstractmethod
    async def create_from_user(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def recover_wallet_from_mnemonics(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_single_wallet(self, **kwargs):
        raise NotImplementedError
