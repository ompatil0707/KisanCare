"""
Government Schemes Service - Provides information about agricultural schemes.
Includes eligibility, benefits, and application details.
"""
from typing import List, Dict, Any


class GovernmentSchemesService:
    """Service for managing information about government agricultural schemes."""
    
    # Government schemes database
    SCHEMES_DATABASE = [
        {
            'id': 'pm-kisan',
            'name': {
                'en': 'PM Kisan Samman Nidhi',
                'hi': 'पीएम किसान सम्मान निधि',
                'mr': 'पीएम किसान सन्मान निधि'
            },
            'description': {
                'en': 'Direct income support to all landholding farmers',
                'hi': 'सभी भूमि धारक किसानों को प्रत्यक्ष आय सहायता',
                'mr': 'सर्व जमीन धारक शेतकरींना थेट उत्पन्न सहायता'
            },
            'benefits': {
                'en': '₹6,000 per year in 3 installments',
                'hi': '₹6,000 प्रति वर्ष 3 किश्तों में',
                'mr': '₹6,000 प्रति वर्ष 3 हप्त्यांमध्ये'
            },
            'eligibility': {
                'en': 'All landholding farmers, small and marginal farmers',
                'hi': 'सभी भूमि धारक, छोटे और सीमांत किसान',
                'mr': 'सर्व जमीन धारक, लहान व सीमांत शेतकरी'
            },
            'documents': ['Land records', 'Aadhar card', 'Bank account details'],
            'website': 'https://pmkisan.gov.in'
        },
        {
            'id': 'crop-insurance',
            'name': {
                'en': 'Pradhan Mantri Fasal Bima Yojana',
                'hi': 'प्रधानमंत्री फसल बीमा योजना',
                'mr': 'प्रधानमंत्री पीक विमा योजना'
            },
            'description': {
                'en': 'Crop insurance scheme for financial support during crop failure',
                'hi': 'फसल की विफलता के दौरान आर्थिक सहायता के लिए फसल बीमा योजना',
                'mr': 'पीक अपयशाच्या दरम्यान आर्थिक सहायतेसाठी पीक विमा योजना'
            },
            'benefits': {
                'en': 'Covers crop loss due to natural calamities and bad weather',
                'hi': 'प्राकृतिक आपदाओं और खराब मौसम के कारण फसल नुकसान को कवर करता है',
                'mr': 'नैसर्गिक आपत्ती आणि वाईट हवामानामुळे पीकाचे नुकसान भरून देते'
            },
            'eligibility': {
                'en': 'All farmers with agricultural land',
                'hi': 'कृषि भूमि वाले सभी किसान',
                'mr': 'कृषी जमीन असलेले सर्व शेतकरी'
            },
            'documents': ['Land records', 'Proof of crop sowing', 'Bank details'],
            'website': 'https://pmfby.gov.in'
        },
        {
            'id': 'soil-health',
            'name': {
                'en': 'Soil Health Card Scheme',
                'hi': 'मृदा स्वास्थ्य पत्र योजना',
                'mr': 'माती आरोग्य कार्ड योजना'
            },
            'description': {
                'en': 'Free soil testing and personalized fertilizer recommendations',
                'hi': 'मुफ्त मिट्टी परीक्षण और व्यक्तिगत उर्वरक सुझाव',
                'mr': 'विनामूल्य माती चाचणी आणि व्यक्तिगत खत सुझाव'
            },
            'benefits': {
                'en': 'Free soil health assessment, improves crop productivity',
                'hi': 'मिट्टी स्वास्थ्य की मुफ्त जांच, फसल उत्पादकता में सुधार',
                'mr': 'मातीच्या आरोग्याची विनामूल्य चाचणी, पीक उत्पादकता सुधारते'
            },
            'eligibility': {
                'en': 'All farmers',
                'hi': 'सभी किसान',
                'mr': 'सर्व शेतकरी'
            },
            'documents': ['Land identification'],
            'website': 'https://soilhealth.dac.gov.in'
        },
        {
            'id': 'subsidy-irrigation',
            'name': {
                'en': 'Pradhan Mantri Krishi Sinchayee Yojana',
                'hi': 'प्रधानमंत्री कृषि सिंचाई योजना',
                'mr': 'प्रधानमंत्री कृषी सिंचन योजना'
            },
            'description': {
                'en': 'Subsidies for irrigation infrastructure development',
                'hi': 'सिंचाई बुनियादी ढांचे के विकास के लिए सब्सिडी',
                'mr': 'सिंचन बुनियादी सुविधा विकासासाठी अनुदान'
            },
            'benefits': {
                'en': '40-90% subsidy on irrigation equipment and pumps',
                'hi': 'सिंचाई उपकरण और पंपों पर 40-90% सब्सिडी',
                'mr': 'सिंचन उपकरण व पंपांवर 40-90% अनुदान'
            },
            'eligibility': {
                'en': 'Farmers with land ownership or agricultural leases',
                'hi': 'भूमि स्वामित्व वाले या कृषि पट्टे वाले किसान',
                'mr': 'जमीन मालकी किंवा कृषी लीज असलेले शेतकरी'
            },
            'documents': ['Land records', 'Income certificate', 'Bank details'],
            'website': 'https://pmksy.gov.in'
        },
        {
            'id': 'subsidy-seeds',
            'name': {
                'en': 'Seed Subsidy Scheme',
                'hi': 'बीज सब्सिडी योजना',
                'mr': 'बियाण अनुदान योजना'
            },
            'description': {
                'en': 'Subsidies on certified quality seeds for various crops',
                'hi': 'विभिन्न फसलों के लिए प्रमाणित गुणवत्ता वाले बीजों पर सब्सिडी',
                'mr': 'विविध पीकांसाठी प्रमाणित गुणवत्तेच्या बियाणांवर अनुदान'
            },
            'benefits': {
                'en': '50% subsidy on seed cost, up to ₹5,000 per hectare',
                'hi': 'बीज लागत पर 50% सब्सिडी, प्रति हेक्टेयर ₹5,000 तक',
                'mr': 'बियाण खर्चावर 50% अनुदान, हेक्टरी ₹5,000 पर्यंत'
            },
            'eligibility': {
                'en': 'Small and marginal farmers',
                'hi': 'छोटे और सीमांत किसान',
                'mr': 'लहान व सीमांत शेतकरी'
            },
            'documents': ['Farmer registration', 'Land records', 'Bank details'],
            'website': 'https://agriwelfare.gov.in/en/SeedsDiv'
        }
    ]
    
    def get_all_schemes(self, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get all government schemes.
        
        Args:
            language: Language (en, hi, mr)
        
        Returns:
            List of schemes formatted for display
        """
        schemes = []
        for scheme in self.SCHEMES_DATABASE:
            schemes.append(self._format_scheme(scheme, language))
        return schemes
    
    def get_scheme_by_id(self, scheme_id: str, language: str = 'en') -> Dict[str, Any]:
        """
        Get detailed information about a specific scheme.
        
        Args:
            scheme_id: Scheme ID
            language: Language (en, hi, mr)
        
        Returns:
            Scheme details
        """
        for scheme in self.SCHEMES_DATABASE:
            if scheme['id'] == scheme_id:
                return self._format_scheme(scheme, language)
        return {}
    
    def search_schemes(self, query: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Search schemes by name or description.
        
        Args:
            query: Search query
            language: Language (en, hi, mr)
        
        Returns:
            List of matching schemes
        """
        query_lower = query.lower()
        results = []
        
        for scheme in self.SCHEMES_DATABASE:
            name = scheme['name'].get(language, scheme['name']['en']).lower()
            desc = scheme['description'].get(language, scheme['description']['en']).lower()
            
            if query_lower in name or query_lower in desc:
                results.append(self._format_scheme(scheme, language))
        
        return results
    
    def get_schemes_for_crop(self, crop: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get relevant schemes for a specific crop.
        
        Args:
            crop: Crop name or code
            language: Language (en, hi, mr)
        
        Returns:
            Relevant schemes
        """
        # For demo purposes, return all schemes
        # In production, you would filter based on crop-specific eligibility
        return self.get_all_schemes(language)
    
    def _format_scheme(self, scheme: Dict, language: str) -> Dict[str, Any]:
        """Format scheme data with language support."""
        return {
            'id': scheme['id'],
            'name': scheme['name'].get(language, scheme['name']['en']),
            'description': scheme['description'].get(language, scheme['description']['en']),
            'benefits': scheme['benefits'].get(language, scheme['benefits']['en']),
            'eligibility': scheme['eligibility'].get(language, scheme['eligibility']['en']),
            'documents': scheme.get('documents', []),
            'website': scheme.get('website', '#')
        }
    
    def get_scheme_categories(self, language: str = 'en') -> List[Dict[str, str]]:
        """
        Get categories of government schemes.
        
        Args:
            language: Language (en, hi, mr)
        
        Returns:
            List of categories
        """
        categories = [
            {
                'id': 'income-support',
                'name': {'en': 'Income Support', 'hi': 'आय सहायता', 'mr': 'उत्पन्न सहायता'},
                'schemes': ['pm-kisan']
            },
            {
                'id': 'insurance',
                'name': {'en': 'Insurance', 'hi': 'बीमा', 'mr': 'विमा'},
                'schemes': ['crop-insurance']
            },
            {
                'id': 'soil-management',
                'name': {'en': 'Soil Management', 'hi': 'मिट्टी प्रबंधन', 'mr': 'माती व्यवस्थापन'},
                'schemes': ['soil-health']
            },
            {
                'id': 'infrastructure',
                'name': {'en': 'Infrastructure', 'hi': 'बुनियादी ढांचा', 'mr': 'बुनियादी सुविधा'},
                'schemes': ['subsidy-irrigation']
            },
            {
                'id': 'input-subsidy',
                'name': {'en': 'Input Subsidy', 'hi': 'इनपुट सब्सिडी', 'mr': 'इनपुट अनुदान'},
                'schemes': ['subsidy-seeds']
            }
        ]
        
        return [{
            'id': cat['id'],
            'name': cat['name'].get(language, cat['name']['en']),
            'scheme_count': len(cat['schemes'])
        } for cat in categories]
