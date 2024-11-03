from dataclasses import dataclass

"""
След (у ip) - захешированный User-Agent
"""


@dataclass
class RateLimits:
    max_traces = 5  # максимальное количество "следов" у IP-адреса
    ip_expire = 12 * 60 * 60 # время хранения ip-адреса
