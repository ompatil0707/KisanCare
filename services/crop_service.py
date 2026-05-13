"""
Crop Recommendation Service - Recommends crops based on soil and climate conditions.
Uses rule-based logic for educational purposes.
"""
from typing import List, Dict, Any


class CropRecommendationService:
    """Service for recommending crops based on environmental conditions."""
    
    # Crop requirements database
    CROP_DATABASE = {
        'banana': {
            'name_en': 'Banana',
            'name_hi': 'केला',
            'name_mr': 'केळं',
            'min_temp': 18,
            'max_temp': 35,
            'min_rainfall': 1500,
            'max_rainfall': 2250,
            'soil_types': ['loamy', 'clayey'],
            'water_requirement': 'high',
            'min_humidity': 60,
            'max_humidity': 85
        },
        'corn': {
            'name_en': 'Corn',
            'name_hi': 'मक्का',
            'name_mr': 'मका',
            'min_temp': 18,
            'max_temp': 32,
            'min_rainfall': 500,
            'max_rainfall': 1000,
            'soil_types': ['sandy', 'loamy', 'clayey'],
            'water_requirement': 'medium',
            'min_humidity': 40,
            'max_humidity': 70
        },
        'cotton': {
            'name_en': 'Cotton',
            'name_hi': 'कपास',
            'name_mr': 'कापूस',
            'min_temp': 20,
            'max_temp': 35,
            'min_rainfall': 500,
            'max_rainfall': 1000,
            'soil_types': ['sandy', 'loamy'],
            'water_requirement': 'medium',
            'min_humidity': 30,
            'max_humidity': 70
        },
        'rice': {
            'name_en': 'Rice',
            'name_hi': 'धान',
            'name_mr': 'तांदूळ',
            'min_temp': 21,
            'max_temp': 37,
            'min_rainfall': 1000,
            'max_rainfall': 2000,
            'soil_types': ['clayey', 'loamy'],
            'water_requirement': 'very_high',
            'min_humidity': 70,
            'max_humidity': 90
        },
        'wheat': {
            'name_en': 'Wheat',
            'name_hi': 'गेहूं',
            'name_mr': 'गहू',
            'min_temp': 15,
            'max_temp': 25,
            'min_rainfall': 400,
            'max_rainfall': 750,
            'soil_types': ['loamy', 'sandy'],
            'water_requirement': 'low',
            'min_humidity': 30,
            'max_humidity': 60
        }
    }
    
    # Season to months mapping
    SEASON_MONTHS = {
        'kharif': {  # Southwest monsoon (June-September)
            'en': 'Kharif (Monsoon)',
            'hi': 'खरीफ (मानसून)',
            'mr': 'खरीफ (मान्सून)',
            'months': [6, 7, 8, 9]
        },
        'rabi': {  # Winter (October-March)
            'en': 'Rabi (Winter)',
            'hi': 'रबी (सर्दी)',
            'mr': 'रबी (हिवाळ)',
            'months': [10, 11, 12, 1, 2, 3]
        },
        'summer': {
            'en': 'Summer',
            'hi': 'गर्मी',
            'mr': 'उन्हाळ',
            'months': [4, 5]
        }
    }
    
    # Soil characteristics
    SOIL_QUALITY = {
        'fertile': {'nitrogen': 'high', 'phosphorus': 'high', 'potassium': 'high'},
        'moderate': {'nitrogen': 'medium', 'phosphorus': 'medium', 'potassium': 'medium'},
        'poor': {'nitrogen': 'low', 'phosphorus': 'low', 'potassium': 'low'}
    }
    
    def recommend_crops(self, 
                       min_temp: float,
                       max_temp: float,
                       rainfall: float,
                       soil_type: str,
                       season: str,
                       humidity: float = 50) -> List[Dict[str, Any]]:
        """
        Recommend crops based on environmental conditions.
        
        Args:
            min_temp: Minimum temperature (°C)
            max_temp: Maximum temperature (°C)
            rainfall: Annual rainfall (mm)
            soil_type: Type of soil (sandy, loamy, clayey)
            season: Growing season (kharif, rabi, summer)
            humidity: Average humidity (%)
        
        Returns:
            List of recommended crops with compatibility scores
        """
        recommendations = []
        
        for crop_code, crop_data in self.CROP_DATABASE.items():
            score = self._calculate_suitability_score(
                min_temp, max_temp, rainfall, soil_type, humidity, crop_data
            )
            
            if score > 0:
                recommendations.append({
                    'crop_code': crop_code,
                    'crop_name_en': crop_data['name_en'],
                    'crop_name_hi': crop_data['name_hi'],
                    'crop_name_mr': crop_data['name_mr'],
                    'suitability_score': round(score, 2),
                    'water_requirement': crop_data['water_requirement'],
                    'suitable_soils': crop_data['soil_types'],
                    'temperature_range': f"{crop_data['min_temp']}-{crop_data['max_temp']}°C",
                    'rainfall_range': f"{crop_data['min_rainfall']}-{crop_data['max_rainfall']}mm"
                })
        
        # Sort by suitability score (descending)
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _calculate_suitability_score(self, min_temp, max_temp, rainfall, soil_type, 
                                     humidity, crop_data) -> float:
        """Calculate suitability score for a crop (0-100)."""
        score = 100.0
        
        # Temperature scoring
        temp_avg = (min_temp + max_temp) / 2
        if not (crop_data['min_temp'] <= temp_avg <= crop_data['max_temp']):
            distance = min(
                abs(temp_avg - crop_data['min_temp']),
                abs(temp_avg - crop_data['max_temp'])
            )
            score -= distance * 2  # Penalty for temperature mismatch
        
        # Rainfall scoring
        if not (crop_data['min_rainfall'] <= rainfall <= crop_data['max_rainfall']):
            if rainfall < crop_data['min_rainfall']:
                score -= (crop_data['min_rainfall'] - rainfall) / 50
            else:
                score -= (rainfall - crop_data['max_rainfall']) / 50
        
        # Soil type scoring
        if soil_type.lower() in crop_data['soil_types']:
            pass  # Full score for soil match
        else:
            score -= 20  # Penalty for soil mismatch
        
        # Humidity scoring
        if not (crop_data['min_humidity'] <= humidity <= crop_data['max_humidity']):
            distance = min(
                abs(humidity - crop_data['min_humidity']),
                abs(humidity - crop_data['max_humidity'])
            )
            score -= distance * 0.5
        
        return max(score, 0)  # Ensure score is not negative
    
    def get_crop_details(self, crop_code: str, language: str = 'en') -> Dict[str, Any]:
        """
        Get detailed information about a crop.
        
        Args:
            crop_code: Crop code (e.g., 'banana', 'wheat')
            language: Language (en, hi, mr)
        
        Returns:
            Crop details dictionary
        """
        if crop_code not in self.CROP_DATABASE:
            return {}
        
        crop = self.CROP_DATABASE[crop_code]
        return {
            'name': crop[f'name_{language}'] if f'name_{language}' in crop else crop['name_en'],
            'temperature_range': f"{crop['min_temp']}-{crop['max_temp']}°C",
            'rainfall_range': f"{crop['min_rainfall']}-{crop['max_rainfall']}mm",
            'humidity_range': f"{crop['min_humidity']}-{crop['max_humidity']}%",
            'water_requirement': crop['water_requirement'],
            'suitable_soils': ', '.join(crop['soil_types']),
            'code': crop_code
        }
    
    def validate_input(self, min_temp: float, max_temp: float, rainfall: float,
                      soil_type: str, humidity: float) -> Dict[str, Any]:
        """
        Validate input parameters.
        
        Args:
            min_temp: Minimum temperature
            max_temp: Maximum temperature
            rainfall: Rainfall amount
            soil_type: Soil type
            humidity: Humidity percentage
        
        Returns:
            Validation result with errors if any
        """
        errors = []
        
        if min_temp >= max_temp:
            errors.append("Minimum temperature must be less than maximum temperature")
        
        if min_temp < -50 or max_temp > 60:
            errors.append("Temperature out of reasonable range")
        
        if rainfall < 0 or rainfall > 10000:
            errors.append("Rainfall out of reasonable range")
        
        if humidity < 0 or humidity > 100:
            errors.append("Humidity must be between 0-100%")
        
        if soil_type.lower() not in ['sandy', 'loamy', 'clayey']:
            errors.append("Soil type must be sandy, loamy, or clayey")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
