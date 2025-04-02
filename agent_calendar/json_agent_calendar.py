import json
import logging

import datetime as dt
from datetime import datetime, timedelta
from typing import List

from models import AgentCalendarEvent, AgentCalendarSettings, TimeRange
from agent_calendar.agent_calendar import AgentCalendar

logger = logging.getLogger(__name__)


class JSONAgentCalendar(AgentCalendar):
    def __init__(self, json_file: str, client_id: int, agent_id: int, calendar_settings: AgentCalendarSettings):
        self.json_file: str = json_file
        self.client_id: int = client_id
        self.agent_id: int = agent_id
        self.calendar_settings: AgentCalendarSettings = calendar_settings
        self.events: AgentCalendarEvent = self._load_calendar_events()

    def _load_calendar_events(self):
        try:
            with open(self.json_file, 'r') as f:
                all_events = json.load(f)
                # Filter events for the specific client and agent: Mock query to a database
                # In a real-world scenario, this would be a database query
                agent_calendar = [event for event in all_events if event['client_id'] == self.client_id and event['agent_id'] == self.agent_id]
                events = []
                for agent_calendar in agent_calendar:
                    # Flatten the events list
                    events.extend(agent_calendar.get("calendar_events", []))

                # Add ids and convert datetime strings to datetime objects
                for event in events:
                    event['dtstamp'] = datetime.fromisoformat(event['dtstamp'])
                    event['dtstart'] = datetime.fromisoformat(event['dtstart'])
                    event['dtend'] = datetime.fromisoformat(event['dtend'])

                # Sort events by start time
                events.sort(key=lambda x: x['dtstart'])

                # use list comprehension to cast all events to AgentCalendarEvent
                events = [AgentCalendarEvent(**event) for event in events]

                return events
        except Exception as e:
            logger.error(f"Error loading calendar events: {e}", exc_info=True)
            return []

    def is_time_available(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if the time slot is available for the agent."""
        # convert start_time and end_time to time of day check if the start and end times are within the agent's working hours
        if start_time.time() < self.calendar_settings.working_hours.start or end_time.time() > self.calendar_settings.working_hours.end:
            return False

        # check if the start time is before the end time
        if start_time >= end_time:
            return False

        # Check if the time slot overlaps with any existing events
        for event in self.events:
            # check if the event overlaps with the requested time slot
            if start_time < event.dtend and end_time > event.dtstart:
                return False

        return True

    def find_available_slots(self, time_ranges: List[TimeRange], duration: timedelta, count: int) -> List[datetime]:
        available = []
        for interval in time_ranges:
            current_start = interval.start

            while current_start + duration <= interval.end and len(available) < count:
                if self.is_time_available(current_start, current_start + duration):
                    available.append(current_start)

                current_start += timedelta(minutes=self.calendar_settings.availability_increment)

                # if current_start plus duration falls after the calender_settings.working_hours.end, go to beginning of the next date
                if (current_start + duration).time() > self.calendar_settings.working_hours.end:
                    current_start = datetime.combine(current_start.date() + timedelta(days=1), self.calendar_settings.working_hours.start).replace(tzinfo=dt.timezone.utc)

            if len(available) >= count:
                break
        return available

    def agent_can_accept_more_work(self, agent_id: int) -> bool:
        # check if the agent's calendar has > 3 bookings today
        bookings = self.events.get(agent_id, [])
        today = datetime.now().date()
        todays_bookings = [b for b in bookings if b[0].date() == today]
        return len(todays_bookings) < 3

    def _save_events(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.events, f, indent=4)

    def add_event(self, event: dict):
        """Add a new event to the calendar and persist the change."""
        self.events.append(event)
        self._save_events()

    def remove_event(self, event_id: str):
        """Remove an event by its id and persist the change."""
        self.events = [event for event in self.events if event.get('id') != event_id]
        self._save_events()

    def get_events(self):
        """Retrieve the list of current events."""
        return self.events
