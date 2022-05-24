from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Create database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    # Get values from config.py which gets values from .env
    app.config.from_object("config.Config")
    db.init_app(app)

    with app.app_context():
        # Import views
        from views import views as view_routes
        from auth import auth as auth_routes
        from admin import admin as admin_routes
        # Register views
        app.register_blueprint(view_routes, url_prefix='/')
        app.register_blueprint(auth_routes, url_prefix='/')
        app.register_blueprint(admin_routes, url_prefix='/admin')

        # Create database tables for data models in models.py
        db.create_all()

        # Import user model and initialise login manager
        from models import User
        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        return app


app = create_app()

if __name__ == '__main__':
    app.run()
