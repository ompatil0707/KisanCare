"""
KisanCare Application Factory.
Creates and initializes the Flask application with all configurations.
"""
import os
from flask import Flask
from config import config


def create_app(config_name="development"):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment (development, production, testing)
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = config.get(config_name, config["default"])
    app.config.from_object(config_class)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Register blueprints
    from api.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def server_error(error):
        from flask import render_template
        return render_template("500.html"), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        from flask import jsonify
        return jsonify({"error": "Bad request"}), 400
