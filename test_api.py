import requests
import json

# Base URL for the Flask application
BASE_URL = "http://127.0.0.1:5000"

def test_api_endpoints():
    print("Testing API endpoints...")
    
    # Test the login API endpoint
    print("\n1. Testing /api/auth/login endpoint:")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except ValueError:
            print(f"Non-JSON Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test the features API endpoint
    print("\n2. Testing /api/features endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/api/features")
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except ValueError:
            print(f"Non-JSON Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
        
    # Test the non-API features endpoint (should return same format)
    print("\n3. Testing /features endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/features")
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except ValueError:
            print(f"Non-JSON Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

    # Test a page route to ensure it still returns HTML
    print("\n4. Testing /login page route:")
    try:
        response = requests.get(f"{BASE_URL}/login")
        print(f"Status Code: {response.status_code}")
        if response.headers.get('content-type', '').startswith('text/html'):
            print("Content-Type: text/html (expected for page routes)")
            print(f"Response preview: {response.text[:200]}...")
        else:
            print(f"Unexpected Content-Type: {response.headers.get('content-type')}")
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()