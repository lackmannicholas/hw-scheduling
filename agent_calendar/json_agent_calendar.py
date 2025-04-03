import json
import logging

import datetime as dt
from datetime import datetime, timedelta
from typing import List

from models import AgentCalendarEvent, AgentCalendarSettings, TimeRange, ToDo
from agent_calendar.agent_calendar import AgentCalendar

logger = logging.getLogger(__name__)


class JSONAgentCalendar(AgentCalendar):
    def __init__(self, calendar_json_file: str, todo_json_file: str, client_id: int, agent_id: int, calendar_settings: AgentCalendarSettings):
        self.calendar_json_file: str = calendar_json_file
        self.todo_json_file: str = todo_json_file
        self.client_id: int = client_id
        self.agent_id: int = agent_id
        self.calendar_settings: AgentCalendarSettings = calendar_settings
        self.events: List[AgentCalendarEvent] = self._load_calendar_events()
        self.todo_tasks: List[ToDo] = self._load_tasks()

    def _load_calendar_events(self):
        try:
            with open(self.calendar_json_file, 'r') as f:
                all_events = json.load(f)
                # Filter events for the specific client and agent: Mock query to a database
                # In a real-world scenario, this would be a database query
                agent_calendar = [event for event in all_events if event['client_id'] == self.client_id and event['agent_id'] == self.agent_id]
                events = []
                for calendar in agent_calendar:
                    # Flatten the events list
                    events.extend(calendar.get("calendar_events", []))

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

    def _load_tasks(self):
        try:
            with open(self.todo_json_file, 'r') as f:
                all_todo_tasks = json.load(f)
                # Filter tasks for the specific client and agent: Mock query to a database
                # In a real-world scenario, this would be a database query
                agent_todos = [task for task in all_todo_tasks if task['client_id'] == self.client_id and task['agent_id'] == self.agent_id]

                # Add ids and convert datetime strings to datetime objects
                for todo in agent_todos:
                    todo['due_date'] = datetime.fromisoformat(todo['due_date'])

                # Sort tasks by due date and priority
                agent_todos.sort(key=lambda x: (x['due_date'], x['priority']))

                # use list comprehension to cast all events to AgentCalendarEvent
                agent_todos = [ToDo(**task) for task in agent_todos]

                return agent_todos
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

    def recommend_work_from_todo(self) -> List[str]:
        """
        Find available time slots for the tasks that are due soon on a day when the agent does not have any events.
        Search for available time slots in the agent's calendar over the next week during the agent's working hours.
        Suggest work based on the todo list when the agent is free.
        Add the task description and due date to the suggestion in a conversational manner.
        """
        suggestions = []
        today = datetime.now().date()
        week_start = today + timedelta(days=1)
        week_end = week_start + timedelta(days=7)

        # Filter tasks that are due in the next week
        upcoming_tasks = [task for task in self.todo_tasks if task.due_date <= week_end]

        for task in upcoming_tasks:
            # Check if the agent is free on the day of the task
            task_date = task.due_date
            start_of_day = datetime.combine(task_date, self.calendar_settings.working_hours.start).replace(tzinfo=dt.timezone.utc)
            end_of_day = datetime.combine(task_date, self.calendar_settings.working_hours.end).replace(tzinfo=dt.timezone.utc)

            # find available slots for the task during the day it's due
            available_slots = self.find_available_slots([TimeRange(start=start_of_day, end=end_of_day)], timedelta(minutes=30), 1)
            if available_slots:
                # Suggest the task with available slots
                for slot in available_slots:
                    suggestions.append(f"On {task.due_date.strftime('%Y-%m-%d')}, you can work on '{task.task}' at {slot.strftime('%Y-%m-%d %I:%M %p')}.")

            else:
                # If no slots are available, suggest the task with a general suggestion
                suggestions.append(f"On {task.due_date.strftime('%Y-%m-%d')}, you have a task: '{task.task}' due. You can work on it during your available time.")

        return suggestions
