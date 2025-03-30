from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter(prefix="/scheduling", tags=["scheduling"])


# Models
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


agent_calendars = {}
user_calendars = {}


def is_time_available(user_id: int, time: datetime) -> bool:
    bookings = user_calendars.get(user_id, [])
    # books are assumed to be tuples (start, end)
    for start, end in bookings:
        if start <= time < end:
            return False
    return True


def find_available_slots(user_id: int, time_ranges: List[TimeRange], duration: timedelta, count: int) -> List[datetime]:
    available = []
    for interval in time_ranges:
        current_start = interval.start
        while current_start + duration <= interval.end and len(available) < count:
            if is_time_available(user_id, current_start):
                available.append(current_start)
            current_start += timedelta(minutes=15)  # increment by a step; adjustable
        if len(available) >= count:
            break
    return available


def agent_can_accept_more_work(agent_id: int) -> bool:
    # check if the agent's calendar has > 3 bookings today
    bookings = agent_calendars.get(agent_id, [])
    today = datetime.now().date()
    todays_bookings = [b for b in bookings if b[0].date() == today]
    return len(todays_bookings) < 3


# Endpoints
@router.post("/check", response_model=CheckAvailabilityResponse)
async def check_availability(request: CheckAvailabilityRequest):
    available = is_time_available(request.user_id, request.time)
    return CheckAvailabilityResponse(available=available)


@router.post("/available", response_model=FindAvailableTimesResponse)
async def find_available_times(request: FindAvailableTimesRequest):
    duration = timedelta(minutes=request.duration_minutes)
    available_times = find_available_slots(request.user_id, request.time_ranges, duration, request.count)
    if not available_times:
        raise HTTPException(status_code=404, detail="No available time slots found")
    return FindAvailableTimesResponse(available_times=available_times)


@router.post("/recommend", response_model=RecommendWorkResponse)
async def recommend_work(request: RecommendWorkRequest):
    can_accept = agent_can_accept_more_work(request.agent_id)
    message = "Agent has open time to take additional work." if can_accept else "Agent is fully booked today."
    return RecommendWorkResponse(can_accept_more_work=can_accept, message=message)
