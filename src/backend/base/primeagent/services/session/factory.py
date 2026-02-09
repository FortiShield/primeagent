from typing import TYPE_CHECKING

from primeagent.services.factory import ServiceFactory
from primeagent.services.session.service import SessionService
from typing_extensions import override

if TYPE_CHECKING:
    from primeagent.services.cache.service import CacheService


class SessionServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(SessionService)

    @override
    def create(self, cache_service: "CacheService"):
        return SessionService(cache_service)
