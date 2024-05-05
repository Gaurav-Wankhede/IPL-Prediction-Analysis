import re
from datetime import datetime

# Define a function to extract the day, month, and year separately
def extract_date_parts(date_str):
    # Regular expression pattern to match the date, month, and year
    match = re.match(r'(\w+)\s+(\d+)(?:\s*-\s*(\d+))?,\s+(\d{4})', date_str)
    if match:
        month = match.group(1)
        day = int(match.group(2))
        end_day = int(match.group(3)) if match.group(3) else day
        year = int(match.group(4))
        return day, month, year, end_day
    else:
        raise ValueError("Invalid date format")

# Example usage
date_patterns = [
    "May 28 - 29, 2023",
    "May 26, 2023",
    "May 24, 2023"
]

for date_str in date_patterns:
    day, month, year, end_day = extract_date_parts(date_str)
    print("Day:", day)
    print("Month:", month)
    print("Year:", year)
    print("End Day:", end_day)
    print()
data = f"{day}-{month}-{year}"
print(data)