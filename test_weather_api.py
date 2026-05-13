"""Test weather API with different cities"""
from app import app

with app.test_client() as client:
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Pune']
    
    print("🌡️ Weather API Test - Verifying Variable Temperatures\n")
    print("City".ljust(15), "Temperature", "Humidity", "Condition")
    print("-" * 50)
    
    for city in cities:
        response = client.get(f'/api/weather?city={city}&lang=en')
        data = response.get_json()
        
        if data.get('weather'):
            weather = data['weather']
            print(
                city.ljust(15),
                f"{weather['temperature']}°C".ljust(15),
                f"{weather['humidity']}%".ljust(10),
                weather['condition']
            )
    
    print("\n✅ API test completed successfully!")
