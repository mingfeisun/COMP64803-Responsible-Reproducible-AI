from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import re

def parse_ics(file_path):
    """
    Parse the ICS file and return a list of events with their start and end times.

    Args:
        file_path (str): Path to the ICS file.

    Returns:
        list: List of events with their start and end times.
    """
    try:
        with open(file_path, 'r') as f:
            calendar = Calendar.from_ical(f.read())
    except ValueError as e:
        print(f"Error parsing ICS file: {e}")
        return []

    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {
                'summary': str(component.get('SUMMARY')),
                'start': component.get('DTSTART').dt,
                'end': component.get('DTEND').dt,
                'description': str(component.get('DESCRIPTION')),
                'location': str(component.get('LOCATION'))
            }
            events.append(event)
    return events

def get_previous_and_next_events(events, current_time):
    """
    Get the previous and next events based on the current time.

    Args:
        events (list): List of events with their start and end times.
        current_time (datetime): The current time.

    Returns:
        tuple: Previous event and next event.
    """
    previous_event = None
    next_event = None

    for event in sorted(events, key=lambda x: x['start']):
        if event['start'] <= current_time:
            previous_event = event
        elif event['start'] > current_time and next_event is None:
            next_event = event
            break

    return previous_event, next_event

def extract_lat_lng_from_description(description):
    """
    Extract latitude and longitude from the Google Map link in the event description.

    Args:
        description (str): The event description containing the Google Map link.

    Returns:
        tuple: Latitude and longitude as floats.
    """
    match = re.search(r'https://www\.google\.com/maps/search/\?api=1&query=([\d\.\-]+),([\d\.\-]+)', description)
    if match:
        lat = float(match.group(1))
        lng = float(match.group(2))
        return lat, lng
    return None, None

def get_lat_lng_from_events(events, current_time):
    """
    Get the latitude and longitude of the previous and next events based on the current time.

    Args:
        events (list): List of events with their start and end times.
        current_time (datetime): The current time.

    Returns:
        tuple: Latitude and longitude of the previous and next events.
    """
    previous_event, next_event = get_previous_and_next_events(events, current_time)

    prev_lat, prev_lng = extract_lat_lng_from_description(previous_event['description']) if previous_event else (None, None)
    next_lat, next_lng = extract_lat_lng_from_description(next_event['description']) if next_event else (None, None)

    return (prev_lat, prev_lng), (next_lat, next_lng)

def create_new_ics_with_modified_events(input_file_path, output_file_path, current_time):
    """
    Create a new ICS file with the previous and next events from the existing ICS file,
    but modify the start time to one hour before the current time and one hour after the current time,
    each with one hour duration, with other information unchanged.

    Args:
        input_file_path (str): Path to the input ICS file.
        output_file_path (str): Path to the output ICS file.
        current_time (datetime): The current time.
    """
    events = parse_ics(input_file_path)
    if not events:
        print("No valid events found in the ICS file.")
        return

    previous_event, next_event = get_previous_and_next_events(events, current_time)

    new_calendar = Calendar()

    if previous_event:
        new_event = Event()
        new_event.add('summary', previous_event['summary'])
        new_event.add('dtstart', current_time - timedelta(hours=1))
        new_event.add('dtend', current_time)
        new_event.add('description', previous_event['description'])
        new_event.add('location', previous_event['location'])
        new_calendar.add_component(new_event)

    if next_event:
        new_event = Event()
        new_event.add('summary', next_event['summary'])
        new_event.add('dtstart', current_time + timedelta(hours=1))
        new_event.add('dtend', current_time + timedelta(hours=2))
        new_event.add('description', next_event['description'])
        new_event.add('location', next_event['location'])
        new_calendar.add_component(new_event)

    with open(output_file_path, 'wb') as f:
        f.write(new_calendar.to_ical())

if __name__ == "__main__":
    input_file_path = "example.ics"
    output_file_path = "usercase_one.ics"
    current_time = datetime.now(pytz.utc)

    create_new_ics_with_modified_events(input_file_path, output_file_path, current_time)
    print(f"New ICS file created: {output_file_path}")

    events = parse_ics(input_file_path)
    (prev_lat, prev_lng), (next_lat, next_lng) = get_lat_lng_from_events(events, current_time)

    print(f"Previous Event Latitude, Longitude: {prev_lat}, {prev_lng}")
    print(f"Next Event Latitude, Longitude: {next_lat}, {next_lng}")