# This module defines a factory class for creating instances of different calendar types.
# It uses the Factory design pattern to encapsulate the instantiation logic for different calendar classes.

# Examples:
# from agent_calendar.google_calendar import GoogleAgentCalendar
# from agent_calendar.outlook_calendar import OutlookAgentCalendar

from agent_calendar.agent_calendar import AgentCalendar
from agent_calendar.agent_calendar_settings import get_agent_calendar_settings
from agent_calendar.json_agent_calendar import JSONAgentCalendar


class AgentCalendarFactory:
    @staticmethod
    def create_calendar(client_id: int, agent_id: int) -> AgentCalendar:
        """
        Factory method to create an instance of an AgentCalendar concrete class based on the agent_calendar_settings.

        Args:
          client_id (int): The client ID.
          agent_id (int): The agent ID.

        Returns:
          An instance of a concrete AgentCalendar class.

        Raises:
          ValueError: If calendar_type is not recognized.
        """
        # get agent_calendar_settings
        agent_calendar_settings = get_agent_calendar_settings(client_id, agent_id)
        calendar_type = agent_calendar_settings.calendar_type.lower()

        if calendar_type == "json":
            # Create a JSON-based calendar
            return JSONAgentCalendar(json_file="data/ics_data.json", client_id=client_id, agent_id=agent_id)
        else:
            raise ValueError(f"Unknown calendar type: {calendar_type}")
