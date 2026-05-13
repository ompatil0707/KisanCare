"""Test weather service - verify temperature varies by city"""
from services.weather_service import WeatherService

# Create service (without API key to use mock data)
service = WeatherService()

# Test different cities
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Pune']

print("🌡️ Weather Temperature Test - Verifying Variable Temperatures\n")
print("City".ljust(15), "Temperature", "Humidity", "Condition")
print("-" * 50)

for city in cities:
    weather = service.get_weather(city)
    print(
        city.ljust(15),
        f"{weather['temperature']}°C".ljust(15),
        f"{weather['humidity']}%".ljust(10),
        weather['condition']
    )

# Test that same city returns same temperature
print("\n🔄 Consistency Test - Same city should give same temperature:")
weather1 = service.get_weather('Delhi')
weather2 = service.get_weather('Delhi')
print(f"Delhi Request 1: {weather1['temperature']}°C")
print(f"Delhi Request 2: {weather2['temperature']}°C")
if weather1['temperature'] == weather2['temperature']:
    print("✅ PASS - Same city returns consistent temperature")
else:
    print("❌ FAIL - Temperature changed for same city")

print("\n✅ Temperature variation test completed!")
