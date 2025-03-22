from flask import Flask
from config import Config
from routes import init_routes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
