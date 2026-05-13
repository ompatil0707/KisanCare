"""
Translation Service - Handles multilingual support for KisanCare.
Supports: English, Hindi, Marathi
"""

# Translation dictionary with all UI strings, disease names, crops, etc.
TRANSLATIONS = {
    # Navigation & UI
    'dashboard': {'en': 'Dashboard', 'hi': 'डैशबोर्ड', 'mr': 'डॅशबोर्ड'},
    'predict_disease': {'en': 'Disease Prediction', 'hi': 'रोग पूर्वानुमान', 'mr': 'रोग भविष्यवाणी'},
    'weather': {'en': 'Weather', 'hi': 'मौसम', 'mr': 'हवामान'},
    'crop_recommendation': {'en': 'Crop Recommendation', 'hi': 'फसल सुझाव', 'mr': 'पीक सुझाव'},
    'fertilizer': {'en': 'Fertilizer', 'hi': 'उर्वरक', 'mr': 'खत'},
    'schemes': {'en': 'Government Schemes', 'hi': 'सरकारी योजनाएं', 'mr': 'सरकारी योजना'},
    'market_prices': {'en': 'Market Prices', 'hi': 'बाजार मूल्य', 'mr': 'बाजार दर'},
    
    # Common buttons & actions
    'submit': {'en': 'Submit', 'hi': 'जमा करें', 'mr': 'सबमिट करा'},
    'cancel': {'en': 'Cancel', 'hi': 'रद्द करें', 'mr': 'रद्द करा'},
    'back': {'en': 'Back', 'hi': 'वापस', 'mr': 'परत'},
    'home': {'en': 'Home', 'hi': 'होम', 'mr': 'घर'},
    'about': {'en': 'About', 'hi': 'परिचय', 'mr': 'विषयी'},
    
    # Disease Prediction
    'select_crop': {'en': 'Select Crop', 'hi': 'फसल चुनें', 'mr': 'पीक निवडा'},
    'upload_image': {'en': 'Upload Leaf Image', 'hi': 'पत्ते की छवि अपलोड करें', 'mr': 'पानाची प्रतिमा अपलोड करा'},
    'predict': {'en': 'Predict Disease', 'hi': 'रोग की भविष्यवाणी करें', 'mr': 'रोगाचा अंदाज लावा'},
    'prediction_result': {'en': 'Prediction Result', 'hi': 'पूर्वानुमान परिणाम', 'mr': 'भविष्यवाणी परिणाम'},
    'crop': {'en': 'Crop', 'hi': 'फसल', 'mr': 'पीक'},
    'disease': {'en': 'Disease', 'hi': 'रोग', 'mr': 'रोग'},
    'confidence': {'en': 'Confidence', 'hi': 'आत्मविश्वास', 'mr': 'आत्मविश्वास'},
    'treatment': {'en': 'Treatment', 'hi': 'उपचार', 'mr': 'उपचार'},
    
    # Weather
    'enter_city': {'en': 'Enter City Name', 'hi': 'शहर का नाम दर्ज करें', 'mr': 'शहराचे नाव प्रविष्ट करा'},
    'temperature': {'en': 'Temperature', 'hi': 'तापमान', 'mr': 'तापमान'},
    'humidity': {'en': 'Humidity', 'hi': 'आर्द्रता', 'mr': 'आर्द्रता'},
    'condition': {'en': 'Condition', 'hi': 'स्थिति', 'mr': 'स्थिति'},
    'wind_speed': {'en': 'Wind Speed', 'hi': 'हवा की गति', 'mr': 'वाऱ्याचा वेग'},
    'rainfall': {'en': 'Rainfall', 'hi': 'वर्षा', 'mr': 'पाऊस'},
    'advice': {'en': 'Farming Advice', 'hi': 'खेती की सलाह', 'mr': 'शेतीचा सल्ला'},
    
    # Crop Recommendation
    'soil_type': {'en': 'Soil Type', 'hi': 'मिट्टी का प्रकार', 'mr': 'माती प्रकार'},
    'season': {'en': 'Season', 'hi': 'ऋतु', 'mr': 'ऋतु'},
    'water_availability': {'en': 'Water Availability', 'hi': 'जल की उपलब्धता', 'mr': 'जलाची उपलब्धता'},
    'recommended_crops': {'en': 'Recommended Crops', 'hi': 'अनुशंसित फसलें', 'mr': 'शिफारसील पीक'},
    'crop_requirements': {'en': 'Crop Requirements', 'hi': 'फसल की आवश्यकता', 'mr': 'पीकची आवश्यकता'},
    
    # Fertilizer
    'organic': {'en': 'Organic', 'hi': 'जैविक', 'mr': 'जैविक'},
    'chemical': {'en': 'Chemical', 'hi': 'रासायनिक', 'mr': 'रासायनिक'},
    'dosage': {'en': 'Dosage', 'hi': 'मात्रा', 'mr': 'मात्रा'},
    'application': {'en': 'Application', 'hi': 'आवेदन', 'mr': 'वापर'},
    
    # Schemes
    'eligibility': {'en': 'Eligibility', 'hi': 'योग्यता', 'mr': 'पात्रता'},
    'benefits': {'en': 'Benefits', 'hi': 'लाभ', 'mr': 'फायदे'},
    'description': {'en': 'Description', 'hi': 'विवरण', 'mr': 'विवरण'},
    'apply': {'en': 'Apply', 'hi': 'आवेदन करें', 'mr': 'अर्ज करा'},
    
    # Market
    'market_price': {'en': 'Market Price', 'hi': 'बाजार मूल्य', 'mr': 'बाजार दर'},
    'mandi': {'en': 'Mandi', 'hi': 'मंडी', 'mr': 'मंडी'},
    'price': {'en': 'Price', 'hi': 'कीमत', 'mr': 'दर'},
    'unit': {'en': 'Unit', 'hi': 'इकाई', 'mr': 'एकक'},
    
    # Crops
    'banana': {'en': 'Banana', 'hi': 'केला', 'mr': 'केळं'},
    'corn': {'en': 'Corn', 'hi': 'मक्का', 'mr': 'मका'},
    'cotton': {'en': 'Cotton', 'hi': 'कपास', 'mr': 'कापूस'},
    'rice': {'en': 'Rice', 'hi': 'धान', 'mr': 'तांदूळ'},
    'wheat': {'en': 'Wheat', 'hi': 'गेहूं', 'mr': 'गहू'},
    
    # Messages
    'success': {'en': 'Success', 'hi': 'सफलता', 'mr': 'यश'},
    'error': {'en': 'Error', 'hi': 'त्रुटि', 'mr': 'त्रुटी'},
    'loading': {'en': 'Loading...', 'hi': 'लोड हो रहा है...', 'mr': 'लोड होत आहे...'},
    'no_data': {'en': 'No Data Available', 'hi': 'कोई डेटा उपलब्ध नहीं', 'mr': 'कोणताही डेटा उपलब्ध नाही'},
}


class TranslationService:
    """Service for managing multilingual translations."""
    
    @staticmethod
    def get_translation(key, language='en', default=None):
        """
        Get translation for a key in specified language.
        
        Args:
            key: Translation key
            language: Language code (en, hi, mr)
            default: Default value if key not found
        
        Returns:
            Translated string or default value
        """
        if key in TRANSLATIONS:
            return TRANSLATIONS[key].get(language, TRANSLATIONS[key].get('en', default or key))
        return default or key
    
    @staticmethod
    def get_all_translations(language='en'):
        """
        Get all translations for a specific language.
        
        Args:
            language: Language code (en, hi, mr)
        
        Returns:
            Dictionary of all translations for the language
        """
        result = {}
        for key, translations in TRANSLATIONS.items():
            result[key] = translations.get(language, translations.get('en', key))
        return result
    
    @staticmethod
    def translate_dict(data, language='en'):
        """
        Translate dictionary values if they are translation keys.
        
        Args:
            data: Dictionary to translate
            language: Target language
        
        Returns:
            Translated dictionary
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, dict) and all(k in ['en', 'hi', 'mr'] for k in value.keys()):
                result[key] = value.get(language, value.get('en', key))
            else:
                result[key] = value
        return result
