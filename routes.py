import os
from flask import request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from utils import (
    extract_text_from_pdf,
    call_groq_api,
    process_voices,
    extract_and_save_text,
    get_characters,
    get_frequent_characters,
    available_voices
)
from config import Config

def init_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload_pdf():
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "" or not file.filename.endswith(".pdf"):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        characters = get_characters(filepath)
        
        groq_response = call_groq_api(text)
        response_text=extract_and_save_text(groq_response)
        
        file_path = os.path.join(os.getcwd(), "sample_story.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        # drama format saved in sample_story.txt
        frequent_characters = get_frequent_characters(groq_response, characters)
        
        return jsonify({"characters": frequent_characters, "voices": available_voices()})

    @app.route("/process_story", methods=["POST"])
    
    def process_story():
        data = request.json
        filepath = data.get("filepath")

        wav_path = process_voices(response_text)

        return jsonify({"wav_file": wav_path})

    @app.route("/audio/<filename>")
    def get_audio(filename):
        audio_path = os.path.join(Config.AUDIO_FOLDER, filename)
        return send_file(audio_path, mimetype="audio/wav")
