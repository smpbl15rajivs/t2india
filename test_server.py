import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify
from flask_cors import CORS
from src.routes.handicraft import handicraft_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app)

app.register_blueprint(handicraft_bp, url_prefix='/api/handicrafts')

@app.route('/')
def home():
    return jsonify({"message": "T2India Handicraft API is running", "endpoints": [
        "/api/handicrafts/destinations",
        "/api/handicrafts/destination/<name>/handicrafts",
        "/api/handicrafts/handicraft/<id>",
        "/api/handicrafts/search",
        "/api/handicrafts/route-planning"
    ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

