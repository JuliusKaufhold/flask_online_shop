from flask import Flask
import os

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URI")
    app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")
    from app.routes import main,login_manager
    app.register_blueprint(main)
    login_manager.init_app(app)

    from app.models import User, Cart, Item, db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
