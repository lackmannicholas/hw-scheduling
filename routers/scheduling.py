import logging

from fastapi import APIRouter, HTTPException
from datetime import timedelta

from agent_calendar.agent_calendar_factory import AgentCalendarFactory
from models import (
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
    FindAvailableTimesRequest,
    FindAvailableTimesResponse,
    RecommendWorkRequest,
    RecommendWorkResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scheduling", tags=["scheduling"])


@router.post("/check", response_model=CheckAvailabilityResponse)
async def check_availability(request: CheckAvailabilityRequest):
    try:
        agent_calendar = AgentCalendarFactory.create_calendar(client_id=request.client_id, agent_id=request.agent_id)
        if not agent_calendar:
            raise HTTPException(status_code=404, detail="Agent calendar not found")
        available = agent_calendar.is_time_available(start_time=request.start_date_time, end_time=request.end_date_time)
        return CheckAvailabilityResponse(available=available)
    except ValueError as e:
        logger.error(f"Error checking availability: {e}")
        raise HTTPException(status_code=404, detail="Agent calendar not found")
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/available", response_model=FindAvailableTimesResponse)
async def find_available_times(request: FindAvailableTimesRequest):
    try:
        agent_calendar = AgentCalendarFactory.create_calendar(client_id=request.client_id, agent_id=request.agent_id)
        if not agent_calendar:
            raise HTTPException(status_code=404, detail="Agent calendar not found")

        duration = timedelta(minutes=request.duration_minutes)
        available_times = agent_calendar.find_available_slots(request.time_ranges, duration, request.count)
        if not available_times:
            raise HTTPException(status_code=404, detail="No available time slots found")
        return FindAvailableTimesResponse(available_times=available_times)
    except ValueError as e:
        logger.error(f"Error finding available times: {e}")
        raise HTTPException(status_code=404, detail="Agent calendar not found")
    except Exception as e:
        logger.error(f"Error finding available times: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/recommend", response_model=RecommendWorkResponse)
async def recommend_work(request: RecommendWorkRequest):
    try:
        agent_calendar = AgentCalendarFactory.create_calendar(client_id=request.client_id, agent_id=request.agent_id)
        if not agent_calendar:
            raise HTTPException(status_code=404, detail="Agent calendar not found")

        can_accept = agent_calendar.agent_can_accept_more_work(request.agent_id)
        message = "Agent has open time to take additional work." if can_accept else "Agent is fully booked today."
        return RecommendWorkResponse(can_accept_more_work=can_accept, message=message)
    except ValueError as e:
        logger.error(f"Error recommending work: {e}")
        raise HTTPException(status_code=404, detail="Agent calendar not found")
    except Exception as e:
        logger.error(f"Error recommending work: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
