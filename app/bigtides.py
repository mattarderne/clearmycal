import requests
from datetime import datetime
import pytz
from ics import Calendar, Event
from mailer import Mailer
from mailer import Message

# Your JSON data goes here
# https://docs.stormglass.io/#/tide
tide_data = {...}
# https://docs.stormglass.io/#/astronomy
daylight_data = {...}

# Mailgun settings
mailgun_domain = 'your_mailgun_domain'
mailgun_api_key = 'your_mailgun_api_key'
sender = 'you@yourdomain.com'
recipient = 'recipient@example.com'

# Criteria for high tide
high_tide_threshold = 1.0  # replace with the threshold you want

def is_weekend(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
    return date_obj.weekday() >= 5  # 5 for Saturday, 6 for Sunday

def get_daylight_hours(daylight_data, date_str):
    for entry in daylight_data['data']:
        if entry['time'].startswith(date_str[:10]):
            return entry['civilDawn'], entry['civilDusk']
    return None, None

def filter_tides(tide_data, daylight_data):
    qualified_days = []
    for tide in tide_data['data']:
        if tide['type'] == 'high' and float(tide['height']) >= high_tide_threshold:
            tide_time = datetime.strptime(tide['time'], '%Y-%m-%d %H:%M:%S%z')
            civil_dawn, civil_dusk = get_daylight_hours(daylight_data, tide['time'])
            if civil_dawn and civil_dusk:
                dawn_time = datetime.strptime(civil_dawn, '%Y-%m-%dT%H:%M:%S%z')
                dusk_time = datetime.strptime(civil_dusk, '%Y-%m-%dT%H:%M:%S%z')
                if dawn_time <= tide_time <= dusk_time and is_weekend(tide['time']):
                    qualified_days.append(tide_time)
    return qualified_days

def send_email_with_calendar_event(qualified_day):
    # Create the calendar event
    c = Calendar()
    e = Event()
    e.name = "High Tide Event"
    e.begin = qualified_day
    e.end = qualified_day + timedelta(hours=1)  # Assuming the event lasts 1 hour
    e.description = "High tide is above the threshold."
    c.events.add(e)
    ics_content = str(c)

    # Create the email message with an attachment
    message = Message(From=sender,
                      To=recipient,
                      Subject="High Tide Alert")
    message.Body = "The high tide meets the criteria on: {}".format(qualified_day.strftime("%Y-%m-%d"))
    message.attach("event.ics", "text/calendar", ics_content)

    # Send the message via Mailgun
    mailer = Mailer(domain=mailgun_domain, api_key=mailgun_api_key)
    response = mailer.send(message)

    return response

# Main script execution
qualified_days = filter_tides(tide_data, daylight_data)
for day in qualified_days:
    send_email_with_calendar_event(day)
