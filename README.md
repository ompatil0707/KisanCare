s
# 🌾 KisanCare - Smart Agriculture Assistant Platform

A comprehensive Flask-based intelligent agriculture platform designed to help Indian farmers with crop disease detection, weather analysis, crop recommendations, fertilizer suggestions, government schemes, and market prices.

## ✨ Features

- **🔬 Disease Prediction**: Advanced CNN-based plant disease detection using PyTorch
- **🌦️ Weather Analysis**: Real-time weather from Open-Meteo API (no key needed)
- **🌱 Crop Recommendation**: Intelligent crop suggestions based on soil and climate parameters
- **🧪 Fertilizer Guide**: Organic and chemical fertilizer recommendations with NPK ratios
- **📋 Government Schemes**: Information about agricultural subsidy schemes and benefits
- **💰 Market Prices**: Real mandi prices from AGMARKET API with fallback to sample data
- **🗣️ Multilingual Support**: Available in English, Hindi, and Marathi
- **🎨 Dark/Light Theme**: User preferences with theme persistence
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or download the project**:
```bash
cd plant_disease_detector
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your settings (optional):
# - Add your OpenWeatherMap API key (free tier available)
# - Set FLASK_ENV to 'development' or 'production'
```

5. **Run the application**:
```bash
python app.py
```

The application will start at `http://localhost:5000`

## 📁 Project Structure

```
plant_disease_detector/
├── app.py                          # Entry point
├── app_new.py                      # Application factory
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── api/
│   ├── __init__.py
│   └── routes.py                   # All Flask routes
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── translation_service.py      # Multilingual support
│   ├── weather_service.py          # Weather API integration
│   ├── crop_service.py             # Crop recommendations
│   ├── fertilizer_service.py       # Fertilizer suggestions
│   ├── schemes_service.py          # Government schemes
│   └── market_service.py           # Market price data
│
├── model/
│   ├── predict.py                  # Disease prediction module
│   ├── train.py                    # Model training script
│   ├── banana/, corn/, cotton/, rice/, wheat/  # Trained models
│   └── *.pt, *.pth files           # PyTorch model weights
│
├── templates/                      # HTML templates
│   ├── base.html                   # Master template
│   ├── dashboard.html              # Main dashboard
│   ├── predict.html                # Disease prediction page
│   ├── weather.html                # Weather page
│   ├── crop-recommendation.html    # Crop recommendation
│   ├── fertilizer.html             # Fertilizer advice
│   ├── schemes.html                # Government schemes
│   ├── market.html                 # Market prices
│   ├── 404.html                    # Error page
│   └── 500.html                    # Server error page
│
├── static/
│   ├── css/
│   │   ├── styles.css              # Original styles
│   │   └── themes.css              # New theme system
│   ├── js/
│   │   ├── scripts.js              # Original scripts
│   │   └── main.js                 # New application logic
│   └── uploads/                    # User uploaded images
│
├── database/
│   └── (Future: SQLAlchemy models)
│
└── dataset/                        # Training datasets
    ├── banana_split/
    ├── corn_split/
    ├── cotton_split/
    ├── rice_split/
    └── wheat_split/
```

## 🔌 API Endpoints

### Dashboard
- `GET /` - Home page
- `GET /dashboard` - Dashboard page

### Disease Prediction
- `GET /predict` - Prediction form
- `POST /predict` - Submit image for prediction
- `GET /uploads/<filename>` - Retrieve uploaded image

### Weather
- `GET /weather` - Weather form
- `POST /weather` - Submit weather query
- `GET /api/weather?city=<city>&lang=<lang>` - Weather API

### Crop Recommendation
- `GET /crop-recommendation` - Recommendation form
- `POST /crop-recommendation` - Submit parameters
- `GET /api/crop-recommendation` - Crop recommendation API

### Fertilizer
- `GET /fertilizer` - Fertilizer form
- `POST /fertilizer` - Submit crop
- `GET /api/fertilizer/<crop>?lang=<lang>` - Fertilizer API

### Government Schemes
- `GET /schemes` - Schemes page
- `POST /schemes` - Search schemes
- `GET /api/schemes` - Schemes API (with search/filter)

### Market Prices
- `GET /market` - Market prices page
- `GET /api/market/prices` - Price data API
- `GET /api/market/best-price/<crop>` - Best price for crop

### Translation
- `GET /api/translate?key=<key>&lang=<lang>` - Single translation
- `GET /api/translations/<lang>` - All translations

### Utility
- `GET /api/health` - Health check
- `GET /api/info` - Application info

## 🌐 Supported Languages

- **English** (en)
- **Hindi** (hi)
- **Marathi** (mr)

Select language from the top navigation or use `?lang=en|hi|mr` parameter in URLs.

## 🎨 Themes

Supports both light and dark themes. Toggle with the theme button in the navbar. Your preference is saved locally.

## 📊 Supported Crops & Diseases

### Banana
- Black Sigatoka
- Bract Mosaic Virus
- Insect Pest Disease
- Moko Disease
- Panama Disease
- Yellow Sigatoka
- Healthy

### Corn
- Blight
- Common Rust
- Gray Leaf Spot
- Healthy

### Cotton
- Bacterial Blight
- Curl Virus
- Fusarium Wilt
- Healthy

### Rice
- Bacterial Blight
- Bacterial Leaf Blight
- Brown Spot
- Leaf Blast
- Leaf Scald
- Leaf Smut
- Narrow Brown Spot
- Healthy

### Wheat
- Black Point
- Fusarium Foot Rot
- Leaf Blight
- Wheat Blast
- Healthy

## 🔐 Environment Variables

See `.env.example` for configuration template:

```env
# Flask
FLASK_ENV=development
FLASK_PORT=5000
DEBUG=True
SECRET_KEY=your-secret-key

# Weather API (optional, uses mock data if not provided)
WEATHER_API_KEY=your_openweathermap_key

# Upload settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 🛠️ Development

### Running Tests

```bash
python test_routes.py
```

### Adding New Features

1. Create service module in `services/` if data layer needed
2. Add routes in `api/routes.py`
3. Create template in `templates/` if UI needed
4. Update `services/translation_service.py` for multilingual support

### Adding New Crops

1. Add model files to `model/<crop>/`
2. Update `CATEGORY_LABELS` in `api/routes.py`
3. Add disease translations in `services/translation_service.py`
4. Update `services/crop_service.py` CROP_DATABASE
5. Add to `services/fertilizer_service.py`

## 📚 Model Information

- **Architecture**: EfficientNet B3 with ImageNet pretrained weights
- **Input Size**: 300x300 RGB images
- **Output**: Crop + Disease classification with confidence scores
- **Framework**: PyTorch
- **Training Data**: Structured dataset with train/val splits per crop

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Change port in .env or command line
FLASK_PORT=5001 python app.py
```

### Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Weather API Not Working
- Weather API is optional and falls back to mock data
- Get free API key: https://openweathermap.org/api
- Add to `.env`: `WEATHER_API_KEY=your_key`

### Static Files Not Loading
- Ensure `UPLOAD_FOLDER=uploads` exists
- Clear browser cache (Ctrl+F5)

## 📝 License

This project is for educational purposes.

## 👥 Support

For issues, questions, or suggestions, please refer to the GitHub repository or contact the development team.

## 🎯 Future Enhancements

- [ ] User authentication and histories
- [ ] Database integration for predictions tracking
- [ ] Real-time market price integration
- [ ] Mobile app (native iOS/Android)
- [ ] Advanced weather forecasting
- [ ] Soil testing integration
- [ ] Community forum
- [ ] Expert consultation booking

---

**Made with ❤️ for Indian Agriculture**
# KisanCare
