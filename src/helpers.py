import user_agents
import hashlib


def hash_user_agent(user_agent: str) -> str | None:
    user_agent_parsed = user_agents.parse(user_agent)
    key = (f'{user_agent_parsed.device.family}-{user_agent_parsed.os.family}'
           f'-{user_agent_parsed.browser.family}{user_agent_parsed.browser.version}')

    return hashlib.sha256(key.encode()).hexdigest()

