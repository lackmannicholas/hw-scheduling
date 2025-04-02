from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AgentCalendar(ABC):
    @abstractmethod
    def is_time_available(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Checks if the agent is available between the given start_time and end_time.

        Args:
            start_time (datetime): The starting time of the slot.
            end_time (datetime): The ending time of the slot.

        Returns:
            bool: True if available, False otherwise.
        """
        pass

    @abstractmethod
    def find_available_slots(self, duration: timedelta) -> list:
        """
        Finds available time slots that can accommodate a task of a given duration.

        Args:
            duration (timedelta): The duration needed for the appointment.

        Returns:
            list: A list of available time slot tuples (start_time, end_time).
        """
        pass

    @abstractmethod
    def agent_can_accept_more_work(self) -> bool:
        """
        Determines if the agent can accept more work based on their current schedule.

        Returns:
            bool: True if the agent can accept more work, False otherwise.
        """
        pass
