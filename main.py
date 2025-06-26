
import json
import unittest
from datetime import datetime

# Load test data files (create them if they don't exist)
try:
    with open("./data-1.json", "r") as f:
        jsonData1 = json.load(f)
except FileNotFoundError:
    jsonData1 = []

try:
    with open("./data-2.json", "r") as f:
        jsonData2 = json.load(f)
except FileNotFoundError:
    jsonData2 = []

try:
    with open("./data-result.json", "r") as f:
        jsonExpectedResult = json.load(f)
except FileNotFoundError:
    jsonExpectedResult = []

def convertFromFormat1(jsonObject):
    """Convert from format 1 with location string and direct fields"""
    locationParts = jsonObject['location'].split('/')
    
    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }
    
    return result

def convertFromFormat2(jsonObject):
    """Convert from format 2 with nested device object and ISO timestamp"""
    date = datetime.strptime(
        jsonObject['timestamp'],
        '%Y-%m-%dT%H:%M:%S.%fZ'
    )
    timestamp = round(
        (date - datetime(1970, 1, 1)).total_seconds() * 1000
    )
    
    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': {
            'status': jsonObject['status'],
            'temperature': jsonObject['temperature']
        }
    }
    
    return result

def normalize_data(jsonObject):
    """Automatically detect format and normalize data"""
    # Format detection: Format 2 has a 'device' field, Format 1 doesn't
    if 'device' in jsonObject:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)

def iso_to_millis(iso_str):
    """Parse ISO 8601 string and return epoch time in milliseconds"""
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return int(dt.timestamp() * 1000)

def normalize_data1(data1):
    """Legacy function for simple timestamp conversion"""
    data1["timestamp"] = iso_to_millis(data1["timestamp_iso"])
    del data1["timestamp_iso"]
    return data1

def normalize_data2(data2):
    """Legacy function - no conversion needed"""
    return data2

class TestDataNormalization(unittest.TestCase):
    """Unit tests for data normalization functions"""
    
    def test_format1_conversion(self):
        """Test conversion from format 1"""
        test_data = {
            'deviceID': 'DEV001',
            'deviceType': 'sensor',
            'timestamp': 1672574400000,
            'location': 'USA/NYC/Manhattan/Factory1/SectionA',
            'operationStatus': 'active',
            'temp': 23.5
        }
        
        result = convertFromFormat1(test_data)
        
        self.assertEqual(result['deviceID'], 'DEV001')
        self.assertEqual(result['location']['country'], 'USA')
        self.assertEqual(result['location']['city'], 'NYC')
        self.assertEqual(result['data']['status'], 'active')
        self.assertEqual(result['data']['temperature'], 23.5)
    
    def test_format2_conversion(self):
        """Test conversion from format 2"""
        test_data = {
            'device': {
                'id': 'DEV002',
                'type': 'actuator'
            },
            'timestamp': '2023-01-01T12:00:00.000Z',
            'country': 'Canada',
            'city': 'Toronto',
            'area': 'Downtown',
            'factory': 'Factory2',
            'section': 'SectionB',
            'status': 'inactive',
            'temperature': 18.2
        }
        
        result = convertFromFormat2(test_data)
        
        self.assertEqual(result['deviceID'], 'DEV002')
        self.assertEqual(result['deviceType'], 'actuator')
        self.assertEqual(result['timestamp'], 1672574400000)
        self.assertEqual(result['location']['country'], 'Canada')
        self.assertEqual(result['data']['status'], 'inactive')
    
    def test_auto_detection(self):
        """Test automatic format detection"""
        format1_data = {
            'deviceID': 'DEV001',
            'deviceType': 'sensor',
            'timestamp': 1672574400000,
            'location': 'USA/NYC/Manhattan/Factory1/SectionA',
            'operationStatus': 'active',
            'temp': 23.5
        }
        
        format2_data = {
            'device': {'id': 'DEV002', 'type': 'actuator'},
            'timestamp': '2023-01-01T12:00:00.000Z',
            'country': 'Canada',
            'city': 'Toronto',
            'area': 'Downtown',
            'factory': 'Factory2',
            'section': 'SectionB',
            'status': 'inactive',
            'temperature': 18.2
        }
        
        result1 = normalize_data(format1_data)
        result2 = normalize_data(format2_data)
        
        self.assertEqual(result1['deviceID'], 'DEV001')
        self.assertEqual(result2['deviceID'], 'DEV002')

if __name__ == "__main__":
    # Create sample data files if they don't exist
    sample_data1 = [
        {
            'deviceID': 'DEV001',
            'deviceType': 'sensor',
            'timestamp': 1672574400000,
            'location': 'USA/NYC/Manhattan/Factory1/SectionA',
            'operationStatus': 'active',
            'temp': 23.5
        }
    ]
    
    sample_data2 = [
        {
            'device': {'id': 'DEV002', 'type': 'actuator'},
            'timestamp': '2023-01-01T12:00:00.000Z',
            'country': 'Canada',
            'city': 'Toronto',
            'area': 'Downtown',
            'factory': 'Factory2',
            'section': 'SectionB',
            'status': 'inactive',
            'temperature': 18.2
        }
    ]
    
    # Create data files
    with open("data-1.json", "w") as f:
        json.dump(sample_data1, f, indent=2)
    
    with open("data-2.json", "w") as f:
        json.dump(sample_data2, f, indent=2)
    
    # Demo the normalization
    print("=== Data Normalization Demo ===")
    print("\nFormat 1 Data:")
    print(json.dumps(sample_data1[0], indent=2))
    normalized1 = normalize_data(sample_data1[0])
    print("\nNormalized Format 1:")
    print(json.dumps(normalized1, indent=2))
    
    print("\nFormat 2 Data:")
    print(json.dumps(sample_data2[0], indent=2))
    normalized2 = normalize_data(sample_data2[0])
    print("\nNormalized Format 2:")
    print(json.dumps(normalized2, indent=2))
    
    # Run unit tests
    print("\n=== Running Unit Tests ===")
    unittest.main(argv=[''], exit=False, verbosity=2)
