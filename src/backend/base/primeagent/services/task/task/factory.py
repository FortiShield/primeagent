from primeagent.services.factory import ServiceFactory
from primeagent.services.task.service import TaskService
from typing_extensions import override
from wfx.services.settings.service import SettingsService


class TaskServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(TaskService)

    @override
    def create(self, settings_service: SettingsService):
        return TaskService(settings_service)
