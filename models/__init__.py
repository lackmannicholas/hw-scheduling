from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List, Optional


class CheckAvailabilityRequest(BaseModel):
    client_id: int
    agent_id: int
    start_date_time: datetime
    end_date_time: datetime


class CheckAvailabilityResponse(BaseModel):
    available: bool


class TimeRange(BaseModel):
    start: datetime
    end: datetime


class FindAvailableTimesRequest(BaseModel):
    client_id: int
    agent_id: int
    time_ranges: List[TimeRange]
    duration_minutes: int = Field(gt=0)
    count: int = Field(gt=0)


class FindAvailableTimesResponse(BaseModel):
    available_times: List[datetime]


class RecommendWorkRequest(BaseModel):
    client_id: int
    agent_id: int


class RecommendWorkResponse(BaseModel):
    can_accept_more_work: bool
    message: Optional[str] = None


class WorkingHours(BaseModel):
    start: time
    end: time


class AgentCalendarSettings(BaseModel):
    client_id: int
    agent_id: int
    calendar_type: str
    working_hours: WorkingHours
    availability_increment: int = Field(default=15)
    max_bookings_per_day: int = Field(default=3)


class AgentCalendarEvent(BaseModel):
    uid: str
    dtstamp: datetime
    dtstart: datetime
    dtend: datetime
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None


class ICSEvent(BaseModel):
    uid: str
    client_id: int
    agent_id: int
    dtstamp: datetime
    dtstart: datetime
    dtend: datetime
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None
