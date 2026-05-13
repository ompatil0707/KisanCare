"""Test market prices page displays correctly."""
from app import create_app
import json

def test_market_page():
    app = create_app()
    client = app.test_client()
    
    # Test 1: Load market page with all prices
    response = client.get('/market')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✅ GET /market => 200")
    
    # Test 2: Load with specific crop
    response = client.get('/market?crop=banana')
    assert response.status_code == 200
    print("✅ GET /market?crop=banana => 200")
    
    # Test 3: Load with state filter
    response = client.get('/market?state=Delhi')
    assert response.status_code == 200
    print("✅ GET /market?state=Delhi => 200")
    
    # Test 4: Check template renders without errors
    response = client.get('/market')
    html = response.data.decode()
    assert 'Mandi' in html, "Mandi column should be in page"
    assert '₹' in html, "Currency symbol should be in page"
    assert 'Banana' in html or 'Corn' in html, "Crop names should be in page"
    print("✅ Market page renders with proper data")
    
    print("\n✅ All market page tests passed!")

if __name__ == '__main__':
    test_market_page()
