import sys
from pathlib import Path

# Add the project root to sys.path so that modules can be discovered.
sys.path.append(str(Path(__file__).parent))

import json
from datetime import datetime, timedelta
import pytest
from agent_calendar.json_agent_calendar import AgentJSONCalendar


# Dummy TimeRange for testing find_available_slots.
class DummyTimeRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def test_agent_json_calendar_init():
    file = "data/ics_data.json"
    calendar = AgentJSONCalendar(file, client_id=1, agent_id=1)
    assert calendar.json_file == file
    assert calendar.client_id == 1
    assert calendar.agent_id == 1
    assert len(calendar.events) == 3
