from flask import Flask
from config import Config
from extensions import db  # ✅ from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Import and register blueprints
    from routes.post_routes import post_bp
    app.register_blueprint(post_bp)

    return app

app = create_app()


if __name__ == '__main__':
    # Recreate the tables
    with app.app_context():
        db.create_all()             
    app.run(debug=True)
