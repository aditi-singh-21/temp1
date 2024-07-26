from dotenv import load_dotenv
from os import getenv
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from interfaces.flask_app import recommended_vendors
import certifi

load_dotenv()

app = Flask(__name__, static_url_path='')
CORS(app)
client=MongoClient(getenv("MONGO_URI"), tlsCAFile=certifi.where())
app.config["mongo_db"]=client['denver']
app.register_blueprint(
    recommended_vendors , url_prefix = "/api/recommended/"
)
if __name__ == '__main__':
    app.run(debug=True)





