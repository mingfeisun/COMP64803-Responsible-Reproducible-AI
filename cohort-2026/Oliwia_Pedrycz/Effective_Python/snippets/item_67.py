# Item 67: Use datetime Instead of time for Local Clocks

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Time in New York
arrival_time = "2019-03-16 23:33:24"

# Convert the string into a datetime object
nyc_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")

# Attach the New York time zone
nyc_time = nyc_time.replace(tzinfo=ZoneInfo("America/New_York"))

print("New York time:", nyc_time)

# 4. Convert New York time to UTC
utc_time = nyc_time.astimezone(timezone.utc)

print("UTC time:", utc_time)