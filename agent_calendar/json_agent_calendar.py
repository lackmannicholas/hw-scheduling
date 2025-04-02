import json
from datetime import datetime, timedelta
from typing import List

from models import AgentCalendarEvent, TimeRange
from agent_calendar.agent_calendar import AgentCalendar


class JSONAgentCalendar(AgentCalendar):
    def __init__(self, json_file: str, client_id: int, agent_id: int):
        self.json_file: str = json_file
        self.client_id: int = client_id
        self.agent_id: int = agent_id
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
            print(f"Error loading calendar events: {e}")
            return []

    def is_time_available(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if the time slot is available for the agent."""
        # Check if the time slot overlaps with any existing events
        for event in self.events:
            if start_time < event.dtend and end_time > event.dtstart:
                return False
        # TODO: Future enhancement - Check if the time slot is within the agent's working hours
        return True

    def find_available_slots(self, user_id: int, time_ranges: List[TimeRange], duration: timedelta, count: int) -> List[datetime]:
        available = []
        for interval in time_ranges:
            current_start = interval.start
            while current_start + duration <= interval.end and len(available) < count:
                if self.is_time_available(user_id, current_start):
                    available.append(current_start)
                current_start += timedelta(minutes=15)  # increment by a step; adjustable
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
