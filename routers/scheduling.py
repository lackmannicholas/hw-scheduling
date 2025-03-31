from fastapi import APIRouter, HTTPException
from datetime import timedelta

from scheduling.scheduling import (
    is_time_available,
    find_available_slots,
    agent_can_accept_more_work,
)
from models import (
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
    FindAvailableTimesRequest,
    FindAvailableTimesResponse,
    RecommendWorkRequest,
    RecommendWorkResponse,
)

router = APIRouter(prefix="/scheduling", tags=["scheduling"])


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
