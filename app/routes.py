from flask import Blueprint, request, jsonify, render_template
import os
from config import Config
from .utils import save_file

main = Blueprint("main", __name__)

# Home page
@main.route("/")
def index():
    return render_template("index.html")

# Upload endpoint (API)
@main.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = save_file(file)

    if not filepath:
        return jsonify({"error": "Invalid file type"}), 400

    # TODO: Call your biodiversity analysis pipeline here
    results = {
        "filename": os.path.basename(filepath),
        "status": "File uploaded successfully",
        "analysis": {
            "taxonomy_detected": ["Species A", "Species B", "Species C"],
            "biodiversity_score": 0.87
        }
    }

    return jsonify(results)
