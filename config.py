import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Supabase configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or "https://orupwiygpnzibophlwpe.supabase.co"
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ydXB3aXlncG56aWJvcGhsd3BlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTE2ODk0MiwiZXhwIjoyMDY0NzQ0OTQyfQ.if3LMxtMx5apkX5PVcUKUihCk8XmiBD9hoUQVvmMnW8"

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Admin authentication
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'gns2025!'

    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
