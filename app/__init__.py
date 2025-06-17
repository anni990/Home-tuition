from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_wtf.csrf import CSRFProtect
from .utils.image_utils import get_fallback_image, get_image_url

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    # XAMPP default configuration from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Set login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register template filters
    @app.template_filter('get_image')
    def get_image_filter(image_path, category='default'):
        return get_fallback_image(category) if not image_path else image_path
    
    @app.template_filter('get_icon')
    def get_icon_filter(image_path, category='default', social_platform=None):
        return get_image_url(image_path, category, social_platform)
    
    with app.app_context():
        # Import models
        from app.models import models
        
        # Import routes
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.tutor import tutor_bp
        from app.routes.booking import booking_bp
        
        # Register blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(tutor_bp)
        app.register_blueprint(booking_bp)
        
        # Create database tables
        db.create_all()
        
        # User loader for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            # Try loading as regular user first
            user = models.User.query.get(int(user_id))
            if user:
                return user
            # If not found, try loading as tutor
            return models.Tutor.query.get(int(user_id))
    
    return app 