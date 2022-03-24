from flask import Flask
from app.router import router as app_router

app = Flask(__name__)
app.register_blueprint(app_router)