import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from agent_calendar.agent_calendar_settings import get_agent_calendar_settings


def test_get_agent_calendar_settings():
    client_id = 1
    agent_id = 1
    settings = get_agent_calendar_settings(client_id, agent_id)
    assert settings.client_id == client_id
    assert settings.agent_id == agent_id
    assert settings.calendar_type == "json"
