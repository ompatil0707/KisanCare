"""
Weather Service - Provides weather data and farming advice.
Uses Open-Meteo API (free, no API key required) or mock data as fallback.
"""
import requests
import json
import random
from datetime import datetime
from typing import Dict, Any, Tuple


# City coordinates mapping for Open-Meteo API
CITY_COORDINATES = {
    'delhi': (28.7041, 77.1025),
    'mumbai': (19.0760, 72.8777),
    'bangalore': (12.9716, 77.5946),
    'kolkata': (22.5726, 88.3639),
    'hyderabad': (17.3850, 78.4867),
    'pune': (18.5204, 73.8567),
    'ahmedabad': (23.0225, 72.5714),
    'jaipur': (26.9124, 75.7873),
    'lucknow': (26.8467, 80.9462),
    'indore': (22.7196, 75.8577),
    'chandigarh': (30.7333, 76.7794),
    'nagpur': (21.1458, 79.0882),
    'bhopal': (23.1815, 79.9864),
    'agra': (27.1767, 78.0081),
    'guwahati': (26.1445, 91.7362),
    'kochi': (9.9312, 76.2673),
    'visakhapatnam': (17.6869, 83.2185),
    'vadodara': (22.3072, 73.1812),
}


class WeatherService:
    """Service for fetching weather data and providing farming advice."""
    
    # Weather advice based on conditions
    WEATHER_ADVICE = {
        'Sunny': {
            'en': 'Good weather for irrigation. Keep soil moisture adequate.',
            'hi': 'सिंचाई के लिए अच्छा मौसम। मिट्टी की नमी पर्याप्त रखें।',
            'mr': 'सिंचनासाठी चांगले हवामान. माती ओलावण पुरेसे ठेवा.'
        },
        'Rainy': {
            'en': 'Avoid spraying pesticides. Risk of fungal diseases.',
            'hi': 'कीटनाशकों का छिड़काव न करें। फंगल रोग का खतरा।',
            'mr': 'कीटकनाशकांची फवारणी टाळा. बुरशीजन्य रोगाचा धोका.'
        },
        'Cloudy': {
            'en': 'Moderate conditions. Good time for weeding and fertilization.',
            'hi': 'मध्यम स्थिति। निराई और उर्वरण का अच्छा समय।',
            'mr': 'मध्यम परिस्थिती. तणनिवारण व खत देण्याचा चांगला वेळ.'
        },
        'Clear': {
            'en': 'Clear skies. Monitor irrigation needs closely.',
            'hi': 'साफ आसमान। सिंचाई की आवश्यकता पर नजर रखें।',
            'mr': 'साफ आकाश. सिंचनाची गरज लक्षात ठेवा.'
        }
    }
    
    # Farming advice based on temperature
    TEMPERATURE_ADVICE = {
        'hot': {
            'en': 'High temperature: Increase irrigation frequency. Provide shade for sensitive crops.',
            'hi': 'उच्च तापमान: सिंचाई की आवृत्ति बढ़ाएं। संवेदनशील पौधों को छाया दें।',
            'mr': 'उच्च तापमान: सिंचन वारंवारता वाढवा. संवेदनशील पिकांना सावली द्या.'
        },
        'cold': {
            'en': 'Low temperature: Reduce irrigation. Protect from frost damage.',
            'hi': 'कम तापमान: सिंचाई कम करें। ठंढ की क्षति से बचाव करें।',
            'mr': 'कमी तापमान: सिंचन कमी करा. थंडीचे नुकसान टाळा.'
        },
        'moderate': {
            'en': 'Ideal temperature range. Continue normal farming practices.',
            'hi': 'आदर्श तापमान रेंज। सामान्य खेती की प्रथाओं को जारी रखें।',
            'mr': 'आदर्श तापमान श्रेणी. सामान्य शेतीचे काम सुरू ठेवा.'
        }
    }
    
    # Humidity advice
    HUMIDITY_ADVICE = {
        'high': {
            'en': 'High humidity: Risk of fungal and bacterial diseases. Ensure proper drainage.',
            'hi': 'उच्च आर्द्रता: फंगल और जीवाणु रोग का खतरा। उचित जलनिकासी सुनिश्चित करें।',
            'mr': 'उच्च आर्द्रता: बुरशी व जीवाणु रोगाचा धोका. योग्य पाणी बाहेर जाण्याची व्यवस्था करा.'
        },
        'low': {
            'en': 'Low humidity: High evaporation. Increase irrigation and mulching.',
            'hi': 'कम आर्द्रता: उच्च वाष्पीकरण। सिंचाई और मल्चिंग बढ़ाएं।',
            'mr': 'कमी आर्द्रता: उच्च बाष्पीकरण. सिंचन व मल्चिंग वाढवा.'
        },
        'moderate': {
            'en': 'Optimal humidity levels. Maintain regular farming schedule.',
            'hi': 'इष्टतम आर्द्रता स्तर। नियमित खेती का कार्यक्रम बनाए रखें।',
            'mr': 'इष्टतम आर्द्रता पातळी. नियमित शेतीचे वेळापत्रक राखून ठेवा.'
        }
    }
    
    # Mock data for fallback
    MOCK_DATA = {
        'temperature': 28.5,
        'humidity': 65,
        'condition': 'Sunny',
        'wind_speed': 12.5,
        'sunrise': '06:00',
        'sunset': '18:00'
    }
    
    def __init__(self):
        """
        Initialize weather service with Open-Meteo API (no API key needed).
        """
        self.openmeteo_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get weather data for a city using Open-Meteo API.
        Falls back to mock data if API fails.
        
        Args:
            city: City name
        
        Returns:
            Dictionary with weather data
        """
        try:
            # Try to get coordinates from known cities first
            lat, lon = self._get_city_coordinates(city)
            
            if lat and lon:
                return self._get_openmeteo_weather(city, lat, lon)
            else:
                # Fallback to mock data
                return self._get_mock_weather(city)
        except Exception:
            # Fallback to mock data on any error
            return self._get_mock_weather(city)
    
    def _get_city_coordinates(self, city: str) -> Tuple[float, float]:
        """
        Get latitude and longitude for a city.
        Uses known coordinates or geocoding API.
        
        Args:
            city: City name
        
        Returns:
            Tuple of (latitude, longitude) or (None, None)
        """
        city_lower = city.lower().strip()
        
        # Check if city is in our known coordinates
        if city_lower in CITY_COORDINATES:
            return CITY_COORDINATES[city_lower]
        
        # Try geocoding API
        try:
            params = {
                'name': city,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            response = requests.get(self.geocoding_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                return (result.get('latitude'), result.get('longitude'))
        except Exception:
            pass
        
        return (None, None)
    
    def _get_openmeteo_weather(self, city: str, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch weather from Open-Meteo API.
        
        Args:
            city: City name
            lat: Latitude
            lon: Longitude
        
        Returns:
            Weather data dictionary
        """
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
                'timezone': 'auto'
            }
            response = requests.get(self.openmeteo_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current', {})
            
            # Map weather code to condition
            weather_code = current.get('weather_code', 0)
            condition = self._get_weather_condition(weather_code)
            
            return {
                'city': city,
                'temperature': round(current.get('temperature_2m', 25), 1),
                'humidity': current.get('relative_humidity_2m', 50),
                'condition': condition,
                'description': condition.lower(),
                'wind_speed': round(current.get('wind_speed_10m', 0), 1),
                'pressure': None,  # Open-Meteo doesn't provide pressure in free tier
                'timestamp': datetime.now().isoformat(),
                'source': 'open-meteo'
            }
        except Exception:
            return self._get_mock_weather(city)
    
    def _get_weather_condition(self, code: int) -> str:
        """
        Convert WMO weather code to readable condition.
        Based on WMO Weather interpretation codes.
        """
        if code == 0:
            return 'Clear'
        elif code == 1 or code == 2:
            return 'Sunny'
        elif code == 3:
            return 'Cloudy'
        elif code == 45 or code == 48:
            return 'Foggy'
        elif code in [51, 53, 55, 61, 63, 65, 71, 73, 75, 80, 81, 82, 85, 86]:
            return 'Rainy'
        elif code in [77, 80, 81, 82]:
            return 'Rainy'
        else:
            return 'Cloudy'
    
    def get_farming_advice(self, weather_data: Dict, language: str = 'en') -> str:
        """
        Get customized farming advice based on weather.
        
        Args:
            weather_data: Weather data dictionary
            language: Language for advice (en, hi, mr)
        
        Returns:
            Farming advice string
        """
        advice = []
        
        # Get condition-based advice
        condition = weather_data.get('condition', 'Sunny')
        advice.append(self.WEATHER_ADVICE.get(condition, {}).get(language, ''))
        
        # Get temperature-based advice
        temp = weather_data.get('temperature', 25)
        if temp > 30:
            advice.append(self.TEMPERATURE_ADVICE['hot'].get(language, ''))
        elif temp < 15:
            advice.append(self.TEMPERATURE_ADVICE['cold'].get(language, ''))
        else:
            advice.append(self.TEMPERATURE_ADVICE['moderate'].get(language, ''))
        
        # Get humidity-based advice
        humidity = weather_data.get('humidity', 50)
        if humidity > 75:
            advice.append(self.HUMIDITY_ADVICE['high'].get(language, ''))
        elif humidity < 30:
            advice.append(self.HUMIDITY_ADVICE['low'].get(language, ''))
        else:
            advice.append(self.HUMIDITY_ADVICE['moderate'].get(language, ''))
        
        return ' | '.join(filter(None, advice))
    
    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """
        Return realistic mock weather data that varies by city.
        Uses city name as seed for consistency.
        """
        # Use city name as seed for reproducible but varied results
        seed_value = sum(ord(c) for c in city.lower()) if city else 0
        rng = random.Random(seed_value)
        
        # City-specific temperature baselines (realistic ranges)
        city_temps = {
            'delhi': (28, 38),
            'mumbai': (25, 32),
            'bangalore': (20, 28),
            'kolkata': (26, 35),
            'hyderabad': (26, 36),
            'pune': (22, 32),
            'ahmedabad': (28, 40),
            'jaipur': (26, 38),
            'lucknow': (24, 36),
            'indore': (26, 37),
            'chandigarh': (20, 34),
            'nagpur': (24, 34),
        }
        
        # Get temperature range for city (default to moderate range)
        city_lower = city.lower()
        temp_min, temp_max = city_temps.get(city_lower, (20, 30))
        
        # Generate weather data
        temperature = rng.uniform(temp_min, temp_max)
        humidity = rng.randint(45, 85)
        wind_speed = rng.uniform(5, 25)
        
        # Vary condition based on humidity
        if humidity > 75:
            condition = rng.choice(['Rainy', 'Cloudy', 'Rainy'])
        elif humidity > 60:
            condition = rng.choice(['Cloudy', 'Clear', 'Sunny'])
        else:
            condition = rng.choice(['Sunny', 'Clear', 'Sunny'])
        
        return {
            'city': city or 'Not Available',
            'temperature': round(temperature, 1),
            'humidity': humidity,
            'condition': condition,
            'description': 'Partly cloudy' if condition == 'Cloudy' else condition.lower(),
            'wind_speed': round(wind_speed, 1),
            'pressure': rng.randint(1008, 1020),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock'
        }
    
    def get_weather_by_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get weather by latitude and longitude.
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Weather data dictionary
        """
        if self.use_mock:
            return self._get_mock_weather('Current Location')
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            return self._parse_weather_data(data)
        except requests.exceptions.RequestException:
            return self._get_mock_weather('Current Location')
