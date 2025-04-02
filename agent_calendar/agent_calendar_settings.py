import json
import os

from models import AgentCalendarSettings


def load_agent_calendar_settings():
    # Construct the file path relative to the current file
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'agent_calendar_settings.json')
    # Open and load the JSON data into memory
    with open(file_path, 'r', encoding='utf-8') as file:
        settings = json.load(file)

    return settings


def get_agent_calendar_settings(client_id: int, agent_id: int) -> AgentCalendarSettings:
    # use list comprehension to filter settings and find the one that matches client_id and agent_id

    settings = [setting for setting in all_agent_calendar_settings if setting['client_id'] == client_id and setting['agent_id'] == agent_id]
    if len(settings) == 0:
        raise ValueError(f"No settings found for client_id {client_id} and agent_id {agent_id}")
    if len(settings) > 1:
        raise ValueError(f"Multiple settings found for client_id {client_id} and agent_id {agent_id}")
    # Assuming we want the first match
    settings = settings[0]
    return AgentCalendarSettings(**settings)


# loading on import for ease of use as an example datasource
all_agent_calendar_settings = load_agent_calendar_settings().get('agent_calendar_settings', [])
