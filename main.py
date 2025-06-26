import json
from datetime import datetime

def iso_to_millis(iso_str):
    # Parse ISO 8601 string (with 'Z' suffix) and return epoch time in milliseconds
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return int(dt.timestamp() * 1000)

# IMPLEMENT: normalize_data1
def normalize_data1(...):
    ...
    # Example: data1["timestamp"] = iso_to_millis(data1["timestamp_iso"])

# IMPLEMENT: normalize_data2
def normalize_data2(...):
    ...
    # No conversion needed here because it's already in milliseconds


from datetime import datetime

def iso_to_millis(iso_str):
    # Ensure Z is converted to a UTC offset that fromisoformat accepts
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return int(dt.timestamp() * 1000)



from datetime import datetime

def iso_to_millis(iso_str):
    dt = datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    epoch = datetime(1970, 1, 1, tzinfo=dt.tzinfo)
    return int((dt - epoch).total_seconds() * 1000)

def normalize_data1(data1):
    # Convert ISO 8601 timestamp to milliseconds
    data1["timestamp"] = iso_to_millis(data1["timestamp_iso"])
    # Remove the original ISO timestamp field
    del data1["timestamp_iso"]
    return data1
