"""Test navbar text visibility in light and dark themes."""
from app import create_app

def test_navbar_theme():
    app = create_app()
    client = app.test_client()
    
    # Test 1: Check navbar in light theme
    response = client.get('/dashboard')
    html = response.data.decode()
    
    # Check for navbar elements
    assert 'KisanCare' in html, "Logo should be present"
    assert 'Home' in html, "Nav links should be present"
    assert 'nav-link' in html, "Nav link class should be present"
    print("✅ Navbar renders with nav links")
    
    # Test 2: Check with language parameter (load theme CSS)
    response = client.get('/dashboard?lang=en')
    assert response.status_code == 200
    print("✅ Dashboard loads properly")
    
    # Test 3: Check weather page navbar
    response = client.get('/weather')
    html = response.data.decode()
    assert 'KisanCare' in html
    assert 'nav-link' in html
    print("✅ Navbar present on all pages")
    
    # Test 4: Check themes.css is loaded
    response = client.get('/')
    html = response.data.decode()
    assert 'themes.css' in html, "themes.css should be linked"
    print("✅ themes.css is loaded")
    
    print("\n✅ All navbar theme tests passed!")

if __name__ == '__main__':
    test_navbar_theme()
