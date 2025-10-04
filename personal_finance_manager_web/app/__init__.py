from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)

    return app
