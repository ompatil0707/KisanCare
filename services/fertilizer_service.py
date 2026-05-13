"""
Fertilizer Recommendation Service - Suggests organic and chemical fertilizers.
Based on crop type and soil conditions.
"""
from typing import Dict, List, Any


class FertilizerRecommendationService:
    """Service for recommending fertilizers based on crop and soil."""
    
    # Fertilizer database with detailed information
    FERTILIZER_DATABASE = {
        # Banana fertilizers
        'banana': {
            'organic': [
                {
                    'name': 'Cow Dung',
                    'name_hi': 'गोबर',
                    'name_mr': 'गोठीची खत',
                    'quantity': '10-15 kg/plant',
                    'period': 'Once every 3 months',
                    'benefits': 'Improves soil structure and nutrient content',
                    'application': 'Mix with soil around plant base'
                },
                {
                    'name': 'Compost',
                    'name_hi': 'खाद',
                    'name_mr': 'खत',
                    'quantity': '5-8 kg/plant',
                    'period': 'Every 2 months',
                    'benefits': 'Balanced nutrients and organic matter',
                    'application': 'Incorporate into soil during tilling'
                },
                {
                    'name': 'Neem Cake',
                    'name_hi': 'नीम की खली',
                    'name_mr': 'नीम केक',
                    'quantity': '500g/plant',
                    'period': 'Every 2 months',
                    'benefits': 'Nitrogen source and pest control',
                    'application': 'Mix with soil or apply as top dressing'
                }
            ],
            'chemical': [
                {
                    'name': 'Urea (46% N)',
                    'name_hi': 'यूरिया',
                    'name_mr': 'युरिया',
                    'quantity': '200-250g/plant',
                    'period': 'Every month',
                    'benefits': 'High nitrogen for leaf growth',
                    'application': 'Dissolve in water and apply'
                },
                {
                    'name': 'DAP (18:46:0)',
                    'name_hi': 'डीएपी',
                    'name_mr': 'डीएपी',
                    'quantity': '150g/plant',
                    'period': 'Every 3 months',
                    'benefits': 'Phosphorus and nitrogen',
                    'application': 'Mix with soil'
                }
            ]
        },
        # Corn fertilizers
        'corn': {
            'organic': [
                {
                    'name': 'Farm Yard Manure',
                    'name_hi': 'खेत की खाद',
                    'name_mr': 'शेताची खत',
                    'quantity': '10-15 tons/hectare',
                    'period': 'Before planting',
                    'benefits': 'Balanced nutrients and soil improvement',
                    'application': 'Incorporate 2-3 weeks before planting'
                },
                {
                    'name': 'Vermicompost',
                    'name_hi': 'वर्मीकम्पोस्ट',
                    'name_mr': 'व्हर्मीकंपोस्ट',
                    'quantity': '5 tons/hectare',
                    'period': 'Every season',
                    'benefits': 'Rich in beneficial microbes',
                    'application': 'Mix into soil before sowing'
                }
            ],
            'chemical': [
                {
                    'name': 'Urea',
                    'name_hi': 'यूरिया',
                    'name_mr': 'युरिया',
                    'quantity': '120kg/hectare',
                    'period': 'Split in 3 doses',
                    'benefits': 'Nitrogen source for growth',
                    'application': 'Top dress at 25, 45, 60 days'
                }
            ]
        },
        # Cotton fertilizers
        'cotton': {
            'organic': [
                {
                    'name': 'Groundnut Cake',
                    'name_hi': 'मूंगफली की खली',
                    'name_mr': 'मूंगफळीची केक',
                    'quantity': '1-1.5 tons/hectare',
                    'period': 'Before sowing',
                    'benefits': 'Nitrogen and organic matter',
                    'application': 'Mix into soil during preparation'
                }
            ],
            'chemical': [
                {
                    'name': 'Potassium Chloride (60% K)',
                    'name_hi': 'पोटेशियम क्लोराइड',
                    'name_mr': 'पोटॅशियम क्लोराईड',
                    'quantity': '50kg/hectare',
                    'period': 'At flowering',
                    'benefits': 'Improves fiber quality',
                    'application': 'Side dress near plants'
                }
            ]
        },
        # Rice fertilizers
        'rice': {
            'organic': [
                {
                    'name': 'Rice Straw Compost',
                    'name_hi': 'धान की पुआल खाद',
                    'name_mr': 'तांदूळाच्या पिवळ्याची खत',
                    'quantity': '8-10 tons/hectare',
                    'period': 'Before transplanting',
                    'benefits': 'Improves water retention',
                    'application': 'Incorporate into soil'
                }
            ],
            'chemical': [
                {
                    'name': 'Ammonium Sulfate',
                    'name_hi': 'अमोनियम सल्फेट',
                    'name_mr': 'अमोनियम सल्फेट',
                    'quantity': '50kg/hectare',
                    'period': 'Every 30 days',
                    'benefits': 'Nitrogen and sulfur source',
                    'application': 'Apply during vegetative stage'
                }
            ]
        },
        # Wheat fertilizers
        'wheat': {
            'organic': [
                {
                    'name': 'Mustard Cake',
                    'name_hi': 'सरसों की खली',
                    'name_mr': 'सोयाबीनची केक',
                    'quantity': '1-2 tons/hectare',
                    'period': 'Before sowing',
                    'benefits': 'Nitrogen source with pest control',
                    'application': 'Mix with soil during tilling'
                }
            ],
            'chemical': [
                {
                    'name': 'Urea',
                    'name_hi': 'यूरिया',
                    'name_mr': 'युरिया',
                    'quantity': '100-120 kg/hectare',
                    'period': 'Split in 2 doses',
                    'benefits': 'Nitrogen for grain filling',
                    'application': 'At tillering and heading stages'
                }
            ]
        }
    }
    
    # Disease-specific fertilizer recommendations
    DISEASE_FERTILIZER_MAP = {
        'powdery_mildew': {
            'nutrients': 'High Potassium',
            'recommendation': 'Apply potassium-rich fertilizers to improve disease resistance'
        },
        'leaf_spot': {
            'nutrients': 'Balanced NPK',
            'recommendation': 'Maintain balanced nutrition to strengthen plant immunity'
        },
        'rust': {
            'nutrients': 'High Phosphorus',
            'recommendation': 'Increase phosphorus to strengthen plant tissues'
        }
    }
    
    def recommend_fertilizer(self, crop: str, language: str = 'en') -> Dict[str, Any]:
        """
        Get fertilizer recommendations for a crop.
        
        Args:
            crop: Crop code (banana, corn, cotton, rice, wheat)
            language: Language (en, hi, mr)
        
        Returns:
            Fertilizer recommendations with organic and chemical options
        """
        if crop not in self.FERTILIZER_DATABASE:
            return {
                'status': 'error',
                'message': f'No recommendations for crop: {crop}'
            }
        
        crop_data = self.FERTILIZER_DATABASE[crop]
        
        result = {
            'crop': crop,
            'organic': [],
            'chemical': []
        }
        
        # Process organic fertilizers
        for fertilizer in crop_data.get('organic', []):
            result['organic'].append(self._format_fertilizer(fertilizer, language))
        
        # Process chemical fertilizers
        for fertilizer in crop_data.get('chemical', []):
            result['chemical'].append(self._format_fertilizer(fertilizer, language))
        
        return result
    
    def _format_fertilizer(self, fertilizer: Dict, language: str) -> Dict:
        """Format fertilizer data with language support."""
        name_key = f'name_{language}' if f'name_{language}' in fertilizer else 'name'
        return {
            'name': fertilizer.get(name_key, fertilizer.get('name', '')),
            'quantity': fertilizer.get('quantity', ''),
            'period': fertilizer.get('period', ''),
            'benefits': fertilizer.get('benefits', ''),
            'application': fertilizer.get('application', '')
        }
    
    def recommend_for_disease(self, disease: str, language: str = 'en') -> Dict[str, Any]:
        """
        Get fertilizer recommendations for disease management.
        
        Args:
            disease: Disease code or name
            language: Language (en, hi, mr)
        
        Returns:
            Disease-specific fertilizer recommendations
        """
        disease_lower = disease.lower().replace(' ', '_')
        
        if disease_lower not in self.DISEASE_FERTILIZER_MAP:
            return {
                'status': 'info',
                'message': 'Use balanced NPK fertilizer for general disease resistance'
            }
        
        recommendation = self.DISEASE_FERTILIZER_MAP[disease_lower]
        
        return {
            'disease': disease,
            'nutrients_needed': recommendation['nutrients'],
            'recommendation': recommendation['recommendation'],
            'general_advice': 'Maintain proper nutrition to strengthen plant immunity against diseases'
        }
    
    def get_npk_ratio(self, crop: str) -> Dict[str, Any]:
        """
        Get recommended NPK ratio for a crop.
        
        Args:
            crop: Crop code
        
        Returns:
            NPK ratio recommendation
        """
        npk_ratios = {
            'banana': {'N': 300, 'P': 150, 'K': 500, 'unit': 'kg/hectare'},
            'corn': {'N': 120, 'P': 60, 'K': 40, 'unit': 'kg/hectare'},
            'cotton': {'N': 100, 'P': 50, 'K': 50, 'unit': 'kg/hectare'},
            'rice': {'N': 120, 'P': 60, 'K': 50, 'unit': 'kg/hectare'},
            'wheat': {'N': 100, 'P': 50, 'K': 40, 'unit': 'kg/hectare'}
        }
        
        if crop in npk_ratios:
            ratio = npk_ratios[crop]
            total = ratio['N'] + ratio['P'] + ratio['K']
            return {
                'crop': crop,
                'nitrogen': f"{ratio['N']} {ratio['unit']}",
                'phosphorus': f"{ratio['P']} {ratio['unit']}",
                'potassium': f"{ratio['K']} {ratio['unit']}",
                'ratio': f"{ratio['N']}:{ratio['P']}:{ratio['K']}",
                'total': f"{total} {ratio['unit']}"
            }
        
        return {}
    
    def validate_crop(self, crop: str) -> bool:
        """Check if crop is supported."""
        return crop in self.FERTILIZER_DATABASE
