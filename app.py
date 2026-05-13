"""
KisanCare - Smart Agriculture Assistant Platform
Entry point for Flask application

This module initializes and runs the KisanCare smart agriculture platform.
The application factory pattern is used for better modularity and testing.
All routes are registered via Flask blueprints in api/routes.py
"""
import os
from app_new import create_app

# Create Flask app instance using the application factory
app = create_app(os.environ.get('FLASK_ENV', 'development'))


if __name__ == "__main__":
    """
    Main entry point for running the Flask development server.
    
    Environment variables:
    - FLASK_ENV: Set to 'development' for debug mode (default: 'development')
    - FLASK_PORT: Port to run server on (default: 5000)
    
    Usage:
        python app.py
    """
    # Create upload folder if it doesn't exist
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Get configuration from environment
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = app.config.get('DEBUG', False)
    
    # Run development server
    print(f"\n🌾 KisanCare - Smart Agriculture Assistant")
    print(f"🚀 Starting server on http://0.0.0.0:{port}")
    print(f"📝 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🐛 Debug mode: {debug}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=True
    )
