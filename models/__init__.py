from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class CheckAvailabilityRequest(BaseModel):
    user_id: int
    time: datetime


class CheckAvailabilityResponse(BaseModel):
    available: bool


class TimeRange(BaseModel):
    start: datetime
    end: datetime


class FindAvailableTimesRequest(BaseModel):
    user_id: int
    time_ranges: List[TimeRange]
    duration_minutes: int = Field(gt=0)
    count: int = Field(gt=0)


class FindAvailableTimesResponse(BaseModel):
    available_times: List[datetime]


class RecommendWorkRequest(BaseModel):
    agent_id: int


class RecommendWorkResponse(BaseModel):
    can_accept_more_work: bool
    message: Optional[str] = None


class ICSEvent(BaseModel):
    uid: str
    dtstamp: datetime
    dtstart: datetime
    dtend: datetime
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None
