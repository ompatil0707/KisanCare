"""Test market prices integration with AGMARKET API"""
from services.market_service import MarketPriceService

# Create service
service = MarketPriceService()

# Test different crops
crops = ['wheat', 'rice', 'corn', 'cotton', 'banana']

print("💰 Market Prices Test - AGMARKET API Integration\n")
print("Crop".ljust(15), "Avg Price (₹)", "Min-Max", "Source")
print("-" * 65)

for crop in crops:
    prices = service.get_crop_prices(crop)
    
    if 'prices' in prices:
        avg = prices.get('average_price', 0)
        min_p = prices.get('lowest_price', 0)
        max_p = prices.get('highest_price', 0)
        source = prices.get('source', 'unknown')
        
        print(
            crop.ljust(15),
            f"{avg:.0f}".ljust(14),
            f"{min_p:.0f}-{max_p:.0f}",
            source
        )

# Test state-wise prices
print("\n\n📍 State-wise Prices (Sample)\n")
print("Crop".ljust(12), "Mandi".ljust(18), "Price (₹)".ljust(12), "State")
print("-" * 65)

mandi_prices = service.get_mandi_prices()
for item in mandi_prices[:10]:
    print(
        item['crop_code'].ljust(12),
        item['mandi'].ljust(18),
        f"{item['price']:.0f}".ljust(12),
        item['state']
    )

print(f"\nTotal prices: {len(mandi_prices)} mandis across all crops")
print("\n✅ Market prices integration test completed!")
