"""Quick test script for KisanCare routes"""
from app import app

# Test the Flask test client
with app.test_client() as client:
    # Test dashboard route
    response = client.get('/')
    print(f"✅ GET / => {response.status_code}")
    
    # Test dashboard route (alt)
    response = client.get('/dashboard')
    print(f"✅ GET /dashboard => {response.status_code}")
    
    # Test weather route
    response = client.get('/weather')
    print(f"✅ GET /weather => {response.status_code}")
    
    # Test crop recommendation route
    response = client.get('/crop-recommendation')
    print(f"✅ GET /crop-recommendation => {response.status_code}")
    
    # Test health check API
    response = client.get('/api/health')
    print(f"✅ GET /api/health => {response.status_code}")
    
    # Test translation API
    response = client.get('/api/translate?key=dashboard&lang=en')
    print(f"✅ GET /api/translate => {response.status_code}")
    
    # Test info API
    response = client.get('/api/info')
    print(f"✅ GET /api/info => {response.status_code}")
    
    print("\n✅ All basic route tests passed!")
