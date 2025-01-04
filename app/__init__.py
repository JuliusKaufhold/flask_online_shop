from flask import Flask
import os

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URI")


    from app.routes import main
    app.register_blueprint(main)

    from app.models import User,db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
