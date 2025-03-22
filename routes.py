import os
from flask import request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, call_groq_api, process_voices, extract_and_save_text, process_large_text
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
        groq_response=process_large_text(text)
        response_text=extract_and_save_text(groq_response)

        wav_path = process_voices(response_text)

        return jsonify({"wav_file": wav_path})

    @app.route("/audio/<filename>")
    def get_audio(filename):
        audio_path = os.path.join(Config.AUDIO_FOLDER, filename)
        return send_file(audio_path, mimetype="audio/wav")
