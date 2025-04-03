"""
Test cases for JSONAgentCalendar class.
In a real application the tests would be more comprehensive and would include
more edge cases, error handling, and possibly mocking of external dependencies.
"""

import sys
from pathlib import Path

from models import TimeRange

sys.path.append(str(Path(__file__).parent.parent))

from agent_calendar.agent_calendar_settings import get_agent_calendar_settings
from agent_calendar.json_agent_calendar import JSONAgentCalendar
import datetime as dt
from datetime import datetime


def test_agent_json_calendar_init():
    # get calendar settings
    settings = get_agent_calendar_settings(client_id=1, agent_id=1)

    # create a JSONAgentCalendar instance
    calendar = JSONAgentCalendar(
        calendar_json_file="data/ics_data.json",
        todo_json_file="data/todo.json",
        client_id=1,
        agent_id=1,
        calendar_settings=settings,
    )

    assert calendar.client_id == 1
    assert calendar.agent_id == 1
    assert calendar.calendar_settings == settings
    assert calendar.events is not None and len(calendar.events) > 0
    assert calendar.todo_tasks is not None and len(calendar.todo_tasks) > 0


def test_is_time_available_true():
    # get calendar settings
    settings = get_agent_calendar_settings(client_id=1, agent_id=1)

    # create a JSONAgentCalendar instance
    calendar = JSONAgentCalendar(
        calendar_json_file="data/ics_data.json",
        todo_json_file="data/todo.json",
        client_id=1,
        agent_id=1,
        calendar_settings=settings,
    )

    # test time availability as datetime objects
    start_time = datetime.fromisoformat("2025-04-03T09:00:00").replace(tzinfo=dt.timezone.utc)
    end_time = datetime.fromisoformat("2025-04-03T10:00:00").replace(tzinfo=dt.timezone.utc)
    available = calendar.is_time_available(start_time=start_time, end_time=end_time)
    assert available is True


def test_is_time_available_false():
    # get calendar settings
    settings = get_agent_calendar_settings(client_id=1, agent_id=1)

    # create a JSONAgentCalendar instance
    calendar = JSONAgentCalendar(
        calendar_json_file="data/ics_data.json",
        todo_json_file="data/todo.json",
        client_id=1,
        agent_id=1,
        calendar_settings=settings,
    )

    # test time availability as datetime objects
    start_time = datetime.fromisoformat("2025-04-05T12:00:00").replace(tzinfo=dt.timezone.utc)
    end_time = datetime.fromisoformat("2025-04-05T12:30:00").replace(tzinfo=dt.timezone.utc)
    available = calendar.is_time_available(start_time=start_time, end_time=end_time)
    assert available is False


def test_find_available_slots():
    # get calendar settings
    settings = get_agent_calendar_settings(client_id=1, agent_id=1)

    # create a JSONAgentCalendar instance
    calendar = JSONAgentCalendar(
        calendar_json_file="data/ics_data.json",
        todo_json_file="data/todo.json",
        client_id=1,
        agent_id=1,
        calendar_settings=settings,
    )

    # test time availability as datetime objects
    start_time = datetime.fromisoformat("2025-04-03T09:00:00").replace(tzinfo=dt.timezone.utc)
    end_time = datetime.fromisoformat("2025-04-03T13:00:00").replace(tzinfo=dt.timezone.utc)
    available_slots = calendar.find_available_slots(time_ranges=[TimeRange(start=start_time, end=end_time)], duration=dt.timedelta(minutes=30), count=3)
    assert len(available_slots) == 3


def test_recommend_work_from_todo():
    # get calendar settings
    settings = get_agent_calendar_settings(client_id=1, agent_id=1)

    # create a JSONAgentCalendar instance
    calendar = JSONAgentCalendar(
        calendar_json_file="data/ics_data.json",
        todo_json_file="data/todo.json",
        client_id=1,
        agent_id=1,
        calendar_settings=settings,
    )

    # test time availability as datetime objects
    suggestions = calendar.recommend_work_from_todo()
    assert len(suggestions) > 0
    assert isinstance(suggestions[0], str)
