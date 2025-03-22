import os

class Config:
    UPLOAD_FOLDER = 'static/uploads'
    AUDIO_FOLDER = 'static/audio'
    ALLOWED_EXTENSIONS = {'pdf'}
    SECRET_KEY = 'supersecretkey'  # Change this in production

    @staticmethod
    def ensure_folders():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.AUDIO_FOLDER, exist_ok=True)

Config.ensure_folders()
