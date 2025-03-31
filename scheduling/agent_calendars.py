class MockCalendarStore:
    def __init__(self):
        # In-memory store for agent calendars.
        # The key is an agent identifier, the value is a string containing ICS calendar data.
        self.calendars = {}

    def get_calendar(self, agent_id):
        """
        Get the ICS calendar data for the specified agent.

        :param agent_id: Unique identifier for the agent.
        :return: String containing the ICS calendar data or None if not found.
        """
        return self.calendars.get(agent_id)

    def set_calendar(self, agent_id, ics_data):
        """
        Set or update the ICS calendar data for the specified agent.

        :param agent_id: Unique identifier for the agent.
        :param ics_data: String containing the ICS calendar data.
        :return: None
        """
        # Optionally, validate basic ICS structure
        if not ics_data.startswith("BEGIN:VCALENDAR") or "END:VCALENDAR" not in ics_data:
            raise ValueError("Provided data does not appear to be valid ICS format.")

        self.calendars[agent_id] = ics_data


# Example usage (this block can be removed or adapted as needed)
if __name__ == '__main__':
    store = MockCalendarStore()

    # Sample mock ICS calendar data
    sample_ics = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Mock Calendar//EN\n"
        "BEGIN:VEVENT\n"
        "UID:unique-event-id@example.com\n"
        "DTSTAMP:20231010T080000Z\n"
        "DTSTART:20231010T090000Z\n"
        "DTEND:20231010T100000Z\n"
        "SUMMARY:Mock Event\n"
        "END:VEVENT\n"
        "END:VCALENDAR"
    )

    # Setting a calendar for an agent
    agent_id = "agent_001"
    store.set_calendar(agent_id, sample_ics)

    # Getting the calendar for the same agent
    retrieved_ics = store.get_calendar(agent_id)
    print("Retrieved ICS data:")
    print(retrieved_ics)
