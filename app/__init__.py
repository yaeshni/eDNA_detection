from flask import Flask
import os

def create_app():
    # Create Flask app and tell it where to find templates & static
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static")
    )

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
