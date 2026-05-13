"""
Market Price Service - Provides agricultural commodity prices (Mandi rates).
Uses AGMARKET API for real market data with fallback to sample data.
"""
import requests
from typing import List, Dict, Any
from datetime import datetime


class MarketPriceService:
    """Service for managing agricultural market prices via AGMARKET API."""
    
    # AGMARKET API endpoint
    AGMARKET_API_URL = "https://agmarket.nic.in/api"
    
    # Crop mapping to AGMARKET commodity codes
    CROP_MAPPING = {
        'banana': 'Banana',
        'corn': 'Maize',
        'cotton': 'Cotton',
        'rice': 'Rice',
        'wheat': 'Wheat'
    }
    
    # Major mandi codes in AGMARKET
    MAJOR_MANDIS = {
        'delhi': 5,
        'mumbai': 8,
        'bangalore': 2,
        'pune': 24,
        'kolkata': 20,
        'indore': 14,
        'ludhiana': 17,
        'jaipur': 15,
        'nagpur': 23,
    }
    
    # Fallback sample market prices (in INR per quintal or unit)
    MARKET_DATA = {
        'banana': {
            'name_en': 'Banana',
            'name_hi': 'केला',
            'name_mr': 'केळं',
            'unit': 'Dozen',
            'prices': [
                {'mandi': 'Delhi', 'price': 450, 'min': 420, 'max': 500, 'state': 'Delhi'},
                {'mandi': 'Mumbai', 'price': 480, 'min': 450, 'max': 510, 'state': 'Maharashtra'},
                {'mandi': 'Bangalore', 'price': 420, 'min': 400, 'max': 460, 'state': 'Karnataka'},
                {'mandi': 'Nashik', 'price': 470, 'min': 440, 'max': 500, 'state': 'Maharashtra'},
            ]
        },
        'corn': {
            'name_en': 'Corn (Maize)',
            'name_hi': 'मक्का',
            'name_mr': 'मका',
            'unit': 'Quintal (100 kg)',
            'prices': [
                {'mandi': 'Delhi', 'price': 1850, 'min': 1800, 'max': 1900, 'state': 'Delhi'},
                {'mandi': 'Indore', 'price': 1950, 'min': 1900, 'max': 2000, 'state': 'Madhya Pradesh'},
                {'mandi': 'Ludhiana', 'price': 1900, 'min': 1850, 'max': 1950, 'state': 'Punjab'},
                {'mandi': 'Jaipur', 'price': 1880, 'min': 1830, 'max': 1930, 'state': 'Rajasthan'},
            ]
        },
        'cotton': {
            'name_en': 'Cotton',
            'name_hi': 'कपास',
            'name_mr': 'कापूस',
            'unit': 'Quintal (100 kg)',
            'prices': [
                {'mandi': 'Mumbai', 'price': 5800, 'min': 5700, 'max': 5900, 'state': 'Maharashtra'},
                {'mandi': 'Gujarat', 'price': 5700, 'min': 5600, 'max': 5800, 'state': 'Gujarat'},
                {'mandi': 'Yavatmal', 'price': 5900, 'min': 5800, 'max': 6000, 'state': 'Maharashtra'},
                {'mandi': 'Nagpur', 'price': 5850, 'min': 5750, 'max': 5950, 'state': 'Maharashtra'},
            ]
        },
        'rice': {
            'name_en': 'Rice',
            'name_hi': 'धान',
            'name_mr': 'तांदूळ',
            'unit': 'Quintal (100 kg)',
            'prices': [
                {'mandi': 'Delhi', 'price': 1950, 'min': 1900, 'max': 2000, 'state': 'Delhi'},
                {'mandi': 'Chhattisgarh', 'price': 1850, 'min': 1800, 'max': 1900, 'state': 'Chhattisgarh'},
                {'mandi': 'Punjab', 'price': 2000, 'min': 1950, 'max': 2050, 'state': 'Punjab'},
                {'mandi': 'Haryana', 'price': 1980, 'min': 1930, 'max': 2030, 'state': 'Haryana'},
            ]
        },
        'wheat': {
            'name_en': 'Wheat',
            'name_hi': 'गेहूं',
            'name_mr': 'गहू',
            'unit': 'Quintal (100 kg)',
            'prices': [
                {'mandi': 'Delhi', 'price': 2100, 'min': 2050, 'max': 2150, 'state': 'Delhi'},
                {'mandi': 'Punjab', 'price': 2050, 'min': 2000, 'max': 2100, 'state': 'Punjab'},
                {'mandi': 'Haryana', 'price': 2080, 'min': 2030, 'max': 2130, 'state': 'Haryana'},
                {'mandi': 'Madhya Pradesh', 'price': 2120, 'min': 2070, 'max': 2170, 'state': 'Madhya Pradesh'},
            ]
        }
    }
    
    # State information
    MAJOR_STATES = [
        'Delhi', 'Maharashtra', 'Punjab', 'Haryana', 'Madhya Pradesh',
        'Karnataka', 'Gujarat', 'Chhattisgarh', 'Rajasthan'
    ]
    
    def __init__(self):
        """Initialize market service with AGMARKET API support."""
        pass
    
    def _get_agmarket_prices(self, crop: str) -> Dict[str, Any]:
        """
        Fetch prices from AGMARKET API.
        
        Args:
            crop: Crop code
        
        Returns:
            Price data from AGMARKET or None on failure
        """
        try:
            commodity = self.CROP_MAPPING.get(crop)
            if not commodity:
                return None
            
            # Try to fetch from AGMARKET API
            payload = {
                'commodity': commodity
            }
            
            response = requests.get(
                f"{self.AGMARKET_API_URL}/marketPrice",
                params=payload,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if data and 'data' in data:
                return self._format_agmarket_data(data['data'], crop)
        except Exception:
            # Fall through to mock data
            pass
        
        return None
    
    def _format_agmarket_data(self, agmarket_data: List, crop: str) -> Dict[str, Any]:
        """
        Format AGMARKET API response to our standard format.
        
        Args:
            agmarket_data: Raw data from AGMARKET API
            crop: Crop code
        
        Returns:
            Formatted price data
        """
        try:
            prices = []
            
            for item in agmarket_data[:4]:  # Top 4 mandis
                prices.append({
                    'mandi': item.get('market_name', 'Unknown'),
                    'price': float(item.get('price', 0)) if item.get('price') else 0,
                    'min': float(item.get('min_price', 0)) if item.get('min_price') else 0,
                    'max': float(item.get('max_price', 0)) if item.get('max_price') else 0,
                    'state': item.get('state', 'Unknown'),
                })
            
            crop_data = self.MARKET_DATA[crop]
            
            return {
                'crop_code': crop,
                'crop_name': crop_data['name_en'],
                'unit': crop_data['unit'],
                'last_updated': datetime.now().isoformat(),
                'prices': prices,
                'average_price': sum(p['price'] for p in prices) / len(prices) if prices else 0,
                'highest_price': max(p['price'] for p in prices) if prices else 0,
                'lowest_price': min(p['price'] for p in prices) if prices else 0,
                'source': 'agmarket'
            }
        except Exception:
            return None
    
    def get_crop_prices(self, crop: str) -> Dict[str, Any]:
        """
        Get market prices for a specific crop across mandis.
        Tries AGMARKET API first, falls back to mock data.
        
        Args:
            crop: Crop code (banana, corn, cotton, rice, wheat)
        
        Returns:
            Dictionary with crop prices from different mandis
        """
        # Try AGMARKET API first
        agmarket_prices = self._get_agmarket_prices(crop)
        if agmarket_prices:
            return agmarket_prices
        
        # Fallback to mock data
        if crop not in self.MARKET_DATA:
            return {
                'status': 'error',
                'message': f'Price data not available for {crop}'
            }
        
        data = self.MARKET_DATA[crop]
        return {
            'crop_code': crop,
            'crop_name': data['name_en'],
            'unit': data['unit'],
            'last_updated': datetime.now().isoformat(),
            'prices': data['prices'],
            'average_price': self._calculate_average_price(data['prices']),
            'highest_price': max([p['price'] for p in data['prices']]),
            'lowest_price': min([p['price'] for p in data['prices']]),
            'source': 'mock'
        }
    
    def get_all_prices(self) -> Dict[str, Any]:
        """
        Get market prices for all crops.
        
        Returns:
            Dictionary with all crop prices
        """
        result = []
        for crop_code, crop_data in self.MARKET_DATA.items():
            result.append({
                'crop_code': crop_code,
                'crop_name': crop_data['name_en'],
                'unit': crop_data['unit'],
                'current_price': self._get_average_price(crop_code),
                'price_range': self._get_price_range(crop_code)
            })
        return {
            'timestamp': datetime.now().isoformat(),
            'crops': result
        }
    
    def get_mandi_prices(self, state: str = None) -> List[Dict[str, Any]]:
        """
        Get prices for a specific state or all mandis.
        
        Args:
            state: State name (optional)
        
        Returns:
            List of mandi prices
        """
        result = []
        
        for crop_code, crop_data in self.MARKET_DATA.items():
            for price_info in crop_data['prices']:
                if state is None or price_info['state'] == state:
                    result.append({
                        'crop': crop_data['name_en'],
                        'crop_code': crop_code,
                        'mandi': price_info['mandi'],
                        'state': price_info['state'],
                        'price': price_info['price'],
                        'min': price_info['min'],
                        'max': price_info['max'],
                        'unit': crop_data['unit']
                    })
        
        return result
    
    def get_price_trend(self, crop: str) -> Dict[str, Any]:
        """
        Get price trend for a crop.
        
        Args:
            crop: Crop code
        
        Returns:
            Price trend information
        """
        if crop not in self.MARKET_DATA:
            return {}
        
        prices = [p['price'] for p in self.MARKET_DATA[crop]['prices']]
        
        return {
            'crop': crop,
            'current_avg': self._calculate_average_price(self.MARKET_DATA[crop]['prices']),
            'min_price': min(prices),
            'max_price': max(prices),
            'volatility': max(prices) - min(prices),
            'trend': 'stable'  # In production, calculate from historical data
        }
    
    def get_best_price(self, crop: str) -> Dict[str, Any]:
        """
        Get the mandi with best (highest) price for a crop.
        
        Args:
            crop: Crop code
        
        Returns:
            Mandi with best price
        """
        if crop not in self.MARKET_DATA:
            return {}
        
        prices = self.MARKET_DATA[crop]['prices']
        best = max(prices, key=lambda x: x['price'])
        
        return {
            'crop': crop,
            'crop_name': self.MARKET_DATA[crop]['name_en'],
            'best_mandi': best['mandi'],
            'best_price': best['price'],
            'state': best['state'],
            'unit': self.MARKET_DATA[crop]['unit']
        }
    
    def compare_crop_prices(self, crops: List[str]) -> List[Dict[str, Any]]:
        """
        Compare prices of multiple crops.
        
        Args:
            crops: List of crop codes
        
        Returns:
            Comparison of crop prices
        """
        result = []
        
        for crop in crops:
            if crop in self.MARKET_DATA:
                avg_price = self._get_average_price(crop)
                result.append({
                    'crop': crop,
                    'crop_name': self.MARKET_DATA[crop]['name_en'],
                    'average_price': avg_price,
                    'unit': self.MARKET_DATA[crop]['unit']
                })
        
        return result
    
    def get_mandi_list(self, state: str = None) -> List[str]:
        """
        Get list of mandis for a state.
        
        Args:
            state: State name
        
        Returns:
            List of mandis
        """
        mandis = set()
        
        for crop_data in self.MARKET_DATA.values():
            for price_info in crop_data['prices']:
                if state is None or price_info['state'] == state:
                    mandis.add(price_info['mandi'])
        
        return list(mandis)
    
    def get_states_list(self) -> List[str]:
        """
        Get list of all states with market data.
        
        Returns:
            List of states
        """
        states = set()
        
        for crop_data in self.MARKET_DATA.values():
            for price_info in crop_data['prices']:
                states.add(price_info['state'])
        
        return sorted(list(states))
    
    def _calculate_average_price(self, prices: List[Dict]) -> float:
        """Calculate average price from list of prices."""
        if not prices:
            return 0
        total = sum([p['price'] for p in prices])
        return total / len(prices)
    
    def _get_average_price(self, crop: str) -> float:
        """Get average price for a crop."""
        if crop not in self.MARKET_DATA:
            return 0
        return self._calculate_average_price(self.MARKET_DATA[crop]['prices'])
    
    def _get_price_range(self, crop: str) -> Dict[str, float]:
        """Get price range for a crop."""
        if crop not in self.MARKET_DATA:
            return {'min': 0, 'max': 0}
        
        prices = [p['price'] for p in self.MARKET_DATA[crop]['prices']]
        return {
            'min': min(prices),
            'max': max(prices),
            'range': max(prices) - min(prices)
        }
    
    def get_crop_supported(self) -> List[str]:
        """
        Get list of supported crops.
        
        Returns:
            List of supported crop codes
        """
        return list(self.MARKET_DATA.keys())
