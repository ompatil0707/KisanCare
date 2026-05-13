"""Test weather route and functionality"""
from app import app

with app.test_client() as client:
    # Test GET /weather
    print("Testing GET /weather...")
    response = client.get('/weather')
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.data.decode()}")
    else:
        print("✅ GET /weather works")
    
    print("\nTesting POST /weather...")
    response = client.post('/weather', json={'city': 'Delhi'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    print("\nTesting GET /api/weather...")
    response = client.get('/api/weather?city=Delhi&lang=en')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.get_json()
        print(f"Data keys: {data.keys() if isinstance(data, dict) else 'not a dict'}")
        print(f"Data: {data}")
    else:
        print(f"Error: {response.data.decode()}")
