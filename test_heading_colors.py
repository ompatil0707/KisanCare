import unittest
import re
from app import create_app

class TestHeadingDarkTheme(unittest.TestCase):
    """Test that all heading elements have proper dark theme color rules"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_css_has_dark_h1_h6_rules(self):
        """Verify CSS files contain dark theme rules for h1-h6 elements"""
        
        with open('static/css/styles.css', 'r', encoding='utf-8') as f:
            styles_content = f.read()
        
        with open('static/css/themes.css', 'r', encoding='utf-8') as f:
            themes_content = f.read()
        
        # Check for dark theme h1-h6 rules in styles.css
        self.assertIn('[data-theme="dark"] h1', styles_content, 
                      "Missing [data-theme=\"dark\"] h1 rule in styles.css")
        self.assertIn('[data-theme="dark"] h2', styles_content,
                      "Missing [data-theme=\"dark\"] h2 rule in styles.css")
        self.assertIn('[data-theme="dark"] h3', styles_content,
                      "Missing [data-theme=\"dark\"] h3 rule in styles.css")
        self.assertIn('[data-theme="dark"] h4', styles_content,
                      "Missing [data-theme=\"dark\"] h4 rule in styles.css")
        self.assertIn('[data-theme="dark"] h5', styles_content,
                      "Missing [data-theme=\"dark\"] h5 rule in styles.css")
        self.assertIn('[data-theme="dark"] h6', styles_content,
                      "Missing [data-theme=\"dark\"] h6 rule in styles.css")
        
        # Check body.dark-theme variants
        self.assertIn('body.dark-theme h1', styles_content)
        self.assertIn('body.dark-theme h2', styles_content)
        
        # Check for .section-title dark theme rule
        self.assertIn('[data-theme="dark"] .section-title', themes_content,
                      "Missing [data-theme=\"dark\"] .section-title rule in themes.css")
        self.assertIn('body.dark-theme .section-title', themes_content,
                      "Missing body.dark-theme .section-title rule in themes.css")
        
        # Check for .footer-section h4 dark theme rule
        self.assertIn('[data-theme="dark"] .footer-section h4', themes_content,
                      "Missing [data-theme=\"dark\"] .footer-section h4 rule in themes.css")
    
    def test_all_pages_render_with_headings(self):
        """Verify all pages render with proper heading elements"""
        
        pages = [
            ('/', 'Dashboard'),
            ('/weather', 'Weather'),
            ('/market', 'Market Prices'),
            ('/crop-recommendation', 'Crop Recommendation'),
            ('/fertilizer', 'Fertilizer'),
            ('/schemes', 'Government Schemes'),
        ]
        
        for route, name in pages:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Page {name} returned {response.status_code}")
            
            # Check that page contains heading elements
            html = response.data.decode()
            has_heading = (
                '<h1' in html or 
                '<h2' in html or 
                '<h3' in html or 
                '<h4' in html or
                'hero-title' in html or
                'section-title' in html
            )
            self.assertTrue(has_heading, f"Page {name} has no heading elements")
    
    def test_heading_color_values_visible(self):
        """Verify heading colors are set to visible values for dark theme"""
        
        with open('static/css/styles.css', 'r', encoding='utf-8') as f:
            styles_content = f.read()
        
        with open('static/css/themes.css', 'r', encoding='utf-8') as f:
            themes_content = f.read()
        
        # Extract the color value from dark theme h1 rule
        h1_match = re.search(r'\[data-theme="dark"\]\s+h[1-6].*?{\s*color:\s*([^;]+);', styles_content, re.DOTALL)
        self.assertIsNotNone(h1_match, "Could not find color value in dark theme heading rule")
        
        color_value = h1_match.group(1).strip()
        
        # Verify it's a light color (not black, gray or hard to read)
        self.assertIn('#e0e0e0', color_value.lower(),
                      f"Dark theme heading color '{color_value}' may not be visible. Should be #e0e0e0 or similar light color")

if __name__ == '__main__':
    unittest.main()

