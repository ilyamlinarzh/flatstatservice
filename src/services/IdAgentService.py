from fastapi import Depends

from src.repositories import IdAgentRepository

from src.services import BaseService


class IdAgentService(BaseService):
    def __init__(
            self,
            repo: IdAgentRepository = Depends()
    ):
        self.repo = repo

    async def can_write_result(self, ip: str, trace: str):
        ip_has_traces = await self.repo.ip_has_traces(ip)
        if not ip_has_traces:
            return True

        ip_has_this_trace = await self.repo.ip_has_this_trace(ip, trace)
        if not ip_has_this_trace:
            return True

        return False

    async def add_trace(self, ip: str, trace: str):
        traces_count = await self.repo.ip_traces_count(ip)
        await self.repo.add_ip_trace(ip, trace)
        if traces_count == 0:
            await self.repo.set_ip_expire(ip)