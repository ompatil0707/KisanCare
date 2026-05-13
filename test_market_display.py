from services.market_service import MarketPriceService

svc = MarketPriceService()
prices = svc.get_mandi_prices()
print(f'✅ Total mandi prices: {len(prices)}')
print('\n📊 Sample market data for display:')
for p in prices[:5]:
    print(f"  {p['crop']} - {p['mandi']}, {p['state']}: ₹{p['price']} (₹{p['min']}-₹{p['max']})")
