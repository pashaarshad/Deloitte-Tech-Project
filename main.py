import json
from datetime import datetime


def iso_to_millis(iso_str):
    # Parse ISO 8601 string (with 'Z' suffix) and return epoch time in milliseconds
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return int(dt.timestamp() * 1000)


def normalize_data1(data1):
    # Convert ISO 8601 timestamp to milliseconds
    data1["timestamp"] = iso_to_millis(data1["timestamp_iso"])
    # Remove the original ISO timestamp field
    del data1["timestamp_iso"]
    return data1


def normalize_data2(data2):
    # No conversion needed here because it's already in milliseconds
    return data2


if __name__ == "__main__":
    # Test the functions
    test_data1 = {"timestamp_iso": "2023-01-01T12:00:00.000Z", "value": 100}
    test_data2 = {"timestamp": 1672574400000, "value": 200}

    print("Original data1:", test_data1)
    normalized1 = normalize_data1(test_data1)
    print("Normalized data1:", normalized1)

    print("Original data2:", test_data2)
    normalized2 = normalize_data2(test_data2)
    print("Normalized data2:", normalized2)
