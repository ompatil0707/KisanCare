"""
KisanCare API Routes - Flask Blueprint with all application routes.
Includes: Dashboard, Disease Prediction, Weather, Crop Recommendation, 
Fertilizer, Schemes, and Market Prices endpoints.
"""
import os
import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask import current_app

# Import services
from services.translation_service import TranslationService
from services.weather_service import WeatherService
from services.crop_service import CropRecommendationService
from services.fertilizer_service import FertilizerRecommendationService
from services.schemes_service import GovernmentSchemesService
from services.market_service import MarketPriceService
from model.predict import predict

# Create blueprint
bp = Blueprint('main', __name__)

# Initialize services
translation_svc = TranslationService()
weather_svc = WeatherService()
crop_svc = CropRecommendationService()
fertilizer_svc = FertilizerRecommendationService()
schemes_svc = GovernmentSchemesService()
market_svc = MarketPriceService()

# Configuration from existing app
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}

CATEGORY_LABELS = {
    "banana": ["Black Sigatoka", "Bract Mosiac Virus", "Healthy", "Insect Pest Disease", "Moko Disease", "Panama Disease", "Yellow Sigatoka"],
    "corn": ["Blight", "Common Rust", "Gray Leaf Spot", "Healthy"],
    "cotton": ["Bacterial Blight", "Curl Virus", "Fussarium Wilt", "Healthy"],
    "rice": ["Bacterial Blight", "Bacterial Leaf Blight", "Brown Spot", "Healthy", "Leaf Blast", "Leaf Scald", "Leaf Smut", "Narrow Brown Spot"],
    "wheat": ["Black Point", "Fusarium Foot Rot", "Healthy", "Leaf Blight", "Wheat Blast"]
}

TREATMENT_GUIDE = {
    "banana": {
        "Black Sigatoka": "Spray Mancozeb 0.2% or Carbendazim every 7–10 days.",
        "Bract Mosiac Virus": "Use virus-free planting material; control vectors.",
        "Healthy": "No treatment needed.",
        "Insect Pest Disease": "Apply neem-based insecticides or Imidacloprid.",
        "Moko Disease": "Remove infected plants and disinfect tools.",
        "Panama Disease": "Use resistant cultivars and improve soil drainage.",
        "Yellow Sigatoka": "Use Propiconazole-based fungicides."
    },
    "corn": {
        "Blight": "Apply fungicide containing Chlorothalonil or Mancozeb.",
        "Common Rust": "Use resistant varieties; spray Mancozeb if severe.",
        "Gray Leaf Spot": "Apply fungicides like Azoxystrobin at early symptoms.",
        "Healthy": "No treatment needed."
    },
    "cotton": {
        "Bacterial Blight": "Use copper fungicides and resistant seeds.",
        "Curl Virus": "Control whiteflies; use Imidacloprid sprays.",
        "Fussarium Wilt": "Improve drainage and avoid monoculture.",
        "Healthy": "No treatment needed."
    },
    "rice": {
        "Bacterial Blight": "Use copper-based bactericides and maintain field hygiene.",
        "Bacterial Leaf Blight": "Apply Streptocycline and maintain field sanitation.",
        "Brown Spot": "Use fungicides like Tricyclazole and apply balanced fertilization.",
        "Healthy": "No treatment needed.",
        "Leaf Blast": "Spray Tricyclazole and maintain proper plant spacing.",
        "Leaf Scald": "Use Mancozeb or Thiophanate-methyl; ensure good drainage.",
        "Leaf Smut": "No chemical control available; remove infected leaves manually.",
        "Narrow Brown Spot": "Apply Propiconazole and supplement with potassium-rich fertilizers."
    },
    "wheat": {
        "Black Point": "Avoid excessive irrigation near harvesting.",
        "Fusarium Foot Rot": "Improve drainage and crop rotation.",
        "Healthy": "No treatment needed.",
        "Leaf Blight": "Use Mancozeb or Chlorothalonil sprays.",
        "Wheat Blast": "Use tolerant varieties and seed treatment with fungicides."
    }
}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================================
# DASHBOARD ROUTE
# ============================================================================

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """Main dashboard page."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    # Count available features
    features = {
        'diseases': len(CATEGORY_LABELS),
        'crops': 5,
        'schemes': len(schemes_svc.get_all_schemes(lang)),
        'market_prices': len(market_svc.get_crop_supported())
    }
    
    return render_template('dashboard.html', 
                         lang=lang, 
                         trans=trans,
                         features=features)


# ============================================================================
# EXISTING DISEASE PREDICTION (No changes - preserved functionality)
# ============================================================================

@bp.route('/predict', methods=['GET', 'POST'])
def predict_disease():
    """Predict crop disease from leaf image."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        category = request.form.get('category', '')
        
        if not file or not category:
            return jsonify({'error': 'Missing file or category'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format'}), 400
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get prediction
            model_path = os.path.join('model', category, 'model.pt')
            class_names = CATEGORY_LABELS.get(category)
            
            if not class_names or not os.path.exists(model_path):
                return jsonify({'error': 'Model not found for category'}), 404
            
            label, confidence = predict(filepath, model_path, class_names)
            treatment = TREATMENT_GUIDE.get(category, {}).get(label, 'Consult agronomist')
            
            # Get fertilizer recommendation based on disease
            fertilizer_rec = fertilizer_svc.recommend_for_disease(label, lang)
            
            return render_template('predict.html',
                                 category=category,
                                 label=label,
                                 confidence=f"{confidence:.2f}",
                                 image_filename=filename,
                                 treatment=treatment,
                                 fertilizer_recommendation=fertilizer_rec,
                                 lang=lang,
                                 trans=trans)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('predict.html', 
                         lang=lang, 
                         trans=trans,
                         crops=CATEGORY_LABELS.keys())


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


# ============================================================================
# WEATHER ROUTES
# ============================================================================

@bp.route('/weather', methods=['GET', 'POST'])
def weather():
    """Weather information and farming advice."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    if request.method == 'POST' and request.is_json:
        data = request.json
        city = data.get('city', 'Delhi')
        
        try:
            weather_data = weather_svc.get_weather(city)
            advice = weather_svc.get_farming_advice(weather_data, lang)
            
            return jsonify({
                'success': True,
                'weather': weather_data,
                'advice': advice
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('weather.html', lang=lang, trans=trans)


@bp.route('/api/weather')
def api_weather():
    """API endpoint for weather data."""
    city = request.args.get('city', 'Delhi')
    lang = request.args.get('lang', 'en')
    
    try:
        weather_data = weather_svc.get_weather(city)
        advice = weather_svc.get_farming_advice(weather_data, lang)
        
        return jsonify({
            'success': True,
            'location': city,
            'weather': weather_data,
            'advice': advice,
            'language': lang
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# CROP RECOMMENDATION ROUTES
# ============================================================================

@bp.route('/crop-recommendation', methods=['GET', 'POST'])
def crop_recommendation():
    """Crop recommendation interface."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    if request.method == 'POST' and request.is_json:
        data = request.json
        
        # Validate input
        validation = crop_svc.validate_input(
            float(data.get('min_temp', 20)),
            float(data.get('max_temp', 30)),
            float(data.get('rainfall', 800)),
            data.get('soil_type', 'loamy'),
            float(data.get('humidity', 60))
        )
        
        if not validation['valid']:
            return jsonify({'error': validation['errors']}), 400
        
        try:
            recommendations = crop_svc.recommend_crops(
                min_temp=float(data['min_temp']),
                max_temp=float(data['max_temp']),
                rainfall=float(data['rainfall']),
                soil_type=data['soil_type'],
                season=data.get('season', 'kharif'),
                humidity=float(data.get('humidity', 60))
            )
            
            return jsonify({
                'success': True,
                'recommendations': recommendations,
                'count': len(recommendations)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('crop-recommendation.html', lang=lang, trans=trans)


@bp.route('/api/crop-recommendation')
def api_crop_recommendation():
    """API endpoint for crop recommendations."""
    try:
        min_temp = float(request.args.get('min_temp', 20))
        max_temp = float(request.args.get('max_temp', 30))
        rainfall = float(request.args.get('rainfall', 800))
        soil_type = request.args.get('soil_type', 'loamy')
        humidity = float(request.args.get('humidity', 60))
        
        recommendations = crop_svc.recommend_crops(
            min_temp, max_temp, rainfall, soil_type, humidity=humidity
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# FERTILIZER ROUTES
# ============================================================================

@bp.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    """Fertilizer recommendation interface."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    if request.method == 'POST' and request.is_json:
        crop = request.json.get('crop', 'wheat')
        
        try:
            recommendations = fertilizer_svc.recommend_fertilizer(crop, lang)
            npk_ratio = fertilizer_svc.get_npk_ratio(crop)
            
            return jsonify({
                'success': True,
                'crop': crop,
                'recommendations': recommendations,
                'npk_ratio': npk_ratio
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('fertilizer.html', lang=lang, trans=trans)


@bp.route('/api/fertilizer/<crop>')
def api_fertilizer(crop):
    """API endpoint for fertilizer recommendations."""
    lang = request.args.get('lang', 'en')
    
    try:
        recommendations = fertilizer_svc.recommend_fertilizer(crop, lang)
        npk_ratio = fertilizer_svc.get_npk_ratio(crop)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'recommendations': recommendations,
            'npk_ratio': npk_ratio
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# GOVERNMENT SCHEMES ROUTES
# ============================================================================

@bp.route('/schemes', methods=['GET', 'POST'])
def schemes():
    """Government schemes information."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    if request.method == 'POST' and request.is_json:
        search_query = request.json.get('query', '')
        
        try:
            if search_query:
                results = schemes_svc.search_schemes(search_query, lang)
            else:
                results = schemes_svc.get_all_schemes(lang)
            
            return jsonify({
                'success': True,
                'schemes': results,
                'count': len(results)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    schemes_list = schemes_svc.get_all_schemes(lang)
    return render_template('schemes.html', 
                         lang=lang, 
                         trans=trans,
                         schemes=schemes_list)


@bp.route('/api/schemes')
def api_schemes():
    """API endpoint for government schemes."""
    lang = request.args.get('lang', 'en')
    scheme_id = request.args.get('id')
    search = request.args.get('search', '')
    
    try:
        if scheme_id:
            scheme = schemes_svc.get_scheme_by_id(scheme_id, lang)
            return jsonify({'success': True, 'scheme': scheme})
        elif search:
            results = schemes_svc.search_schemes(search, lang)
            return jsonify({'success': True, 'schemes': results})
        else:
            schemes_list = schemes_svc.get_all_schemes(lang)
            return jsonify({'success': True, 'schemes': schemes_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# MARKET PRICES ROUTES
# ============================================================================

@bp.route('/market', methods=['GET'])
def market_prices():
    """Market prices (Mandi rates) page."""
    lang = request.args.get('lang', 'en')
    trans = translation_svc.get_all_translations(lang)
    
    crop = request.args.get('crop')
    state = request.args.get('state')
    
    if crop:
        price_data = market_svc.get_crop_prices(crop)
    else:
        # Get all mandi prices, optionally filtered by state
        mandi_prices = market_svc.get_mandi_prices(state if state else None)
        price_data = {'prices': mandi_prices}
    
    crops = market_svc.get_crop_supported()
    states = market_svc.get_states_list()
    
    return render_template('market.html',
                         lang=lang,
                         trans=trans,
                         price_data=price_data,
                         crops=crops,
                         states=states)


@bp.route('/api/market/prices')
def api_market_prices():
    """API endpoint for market prices."""
    crop = request.args.get('crop')
    state = request.args.get('state')
    
    try:
        if crop:
            prices = market_svc.get_crop_prices(crop)
        elif state:
            prices = market_svc.get_mandi_prices(state)
        else:
            return jsonify(market_svc.get_all_prices())
        
        return jsonify(prices)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/market/best-price/<crop>')
def api_best_price(crop):
    """API endpoint to get best mandi price for a crop."""
    try:
        best = market_svc.get_best_price(crop)
        return jsonify(best) if best else jsonify({'error': 'Crop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# TRANSLATION API
# ============================================================================

@bp.route('/api/translate')
def api_translate():
    """API endpoint for translations."""
    key = request.args.get('key', '')
    lang = request.args.get('lang', 'en')
    
    translation = translation_svc.get_translation(key, lang)
    
    return jsonify({
        'key': key,
        'language': lang,
        'translation': translation
    })


@bp.route('/api/translations/<lang>')
def api_translations(lang):
    """Get all translations for a language."""
    translations = translation_svc.get_all_translations(lang)
    return jsonify(translations)


# ============================================================================
# UTILITY ROUTES
# ============================================================================

@bp.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'services': {
            'translation': 'active',
            'weather': 'active',
            'crop_recommendation': 'active',
            'fertilizer': 'active',
            'schemes': 'active',
            'market_prices': 'active'
        }
    })


@bp.route('/api/info')
def app_info():
    """Application information endpoint."""
    return jsonify({
        'name': 'KisanCare',
        'version': '1.0.0',
        'description': 'Smart Agriculture Assistant Platform',
        'crops_supported': list(CATEGORY_LABELS.keys()),
        'languages_supported': ['en', 'hi', 'mr'],
        'features': [
            'Disease Prediction',
            'Weather Advisory',
            'Crop Recommendation',
            'Fertilizer Suggestion',
            'Government Schemes',
            'Market Prices'
        ]
    })


# ============================================================================
# HOME/INDEX ROUTE (Existing compatibility)
# ============================================================================

@bp.route('/index')
def index_compat():
    """Compatibility route for existing index."""
    return redirect(url_for('main.dashboard'))
