from datetime import datetime, timedelta
from typing import List

from models import TimeRange
from agent_calendar.agent_calendar import agent_calendars


def is_time_available(user_id: int, time: datetime) -> bool:
    bookings = agent_calendars.get(user_id, [])
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
