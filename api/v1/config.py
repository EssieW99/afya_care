import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

class Config:
    SECRET_KEY = 'deathly_hallows'
    TEMPLATE_FOLDER = TEMPLATE_DIR
    STATIC_FOLDER = STATIC_DIR
    UPLOAD_FOLDER = UPLOAD_FOLDER
    CORS_RESOURCES = {r"/api/v1/*": {"origins": "*"}}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
