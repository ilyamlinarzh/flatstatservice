from dataclasses import dataclass
from fastapi import Request, Depends

from src.helpers import hash_user_agent

from src.services import IdAgentService


@dataclass
class UserMetadata:
    client_ip: str
    hash_agent: str
    access: bool


async def id_agent(
        request: Request,
        service: IdAgentService = Depends()
) -> UserMetadata:
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    hash_agent = hash_user_agent(user_agent)
    access = await service.can_write_result(client_ip, hash_agent)

    if access:
        await service.add_trace(client_ip, hash_agent)

    return UserMetadata(client_ip, hash_agent, access)
