from typing import Optional
from pydantic import BaseModel


class GetStatResponse(BaseModel):
    results_stat: list[tuple[str, int]]
    result_in_city: Optional[int]
