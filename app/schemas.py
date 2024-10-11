from pydantic import BaseModel
from typing import List, Optional

class UpdateCampaignRequest(BaseModel):
    name: str

class TimeSeriesQueryParams(BaseModel):
    aggregate_by: str
    campaigns: Optional[List[int]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
