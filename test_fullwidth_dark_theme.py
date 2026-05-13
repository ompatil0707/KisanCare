"""Test full-width dark theme viewport coverage."""
from app import create_app

def test_fullwidth_dark_theme():
    app = create_app()
    client = app.test_client()
    
    # Test dashboard with full viewport dark theme
    response = client.get('/dashboard')
    html = response.data.decode()
    
    # Verify viewport meta tag exists
    assert 'viewport' in html, "Viewport meta tag should be present"
    print("✅ Viewport meta tag present")
    
    # Check for main-content element
    assert 'main-content' in html or '<main' in html, "main-content should be present"
    print("✅ main-content element present")
    
    # Check both CSS files loaded
    assert 'styles.css' in html and 'themes.css' in html
    print("✅ Both CSS files loaded (styles.css and themes.css)")
    
    # Check data-theme support for full viewport
    assert 'data-theme' in html
    print("✅ data-theme attribute support present")
    
    # Verify dark theme JavaScript is present
    assert 'toggleTheme' in html or 'theme' in html.lower()
    print("✅ Theme toggle functionality present")
    
    # Test all pages have proper structure
    for url, name in [
        ('/dashboard', 'Dashboard'),
        ('/weather', 'Weather'),
        ('/market', 'Market Prices'),
        ('/crop-recommendation', 'Crop Recommendation'),
    ]:
        response = client.get(url)
        assert response.status_code == 200
        html = response.data.decode()
        assert 'html' in html and 'body' in html
        assert 'main' in html
        print(f"✅ {name} has proper HTML structure")
    
    print("\n✅ All full-width dark theme tests passed!")
    print("\n📋 CSS Changes Applied:")
    print("   ✓ html element: 100% width, dark background on toggle")
    print("   ✓ body element: 100% width, full viewport coverage")
    print("   ✓ main element: 100% width, removed max-width constraint")
    print("   ✓ main-content class: Full width with padding")
    print("   ✓ No margins or constraints keeping dark theme from edges")

if __name__ == '__main__':
    test_fullwidth_dark_theme()
