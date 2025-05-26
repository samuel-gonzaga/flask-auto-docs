import os
from pathlib import Path
from werkzeug.utils import secure_filename

# Configurações básicas
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    UPLOAD_FOLDER = 'templates'
    GENERATED_FOLDER = 'generated'
    ALLOWED_EXTENSIONS = {'docx', 'doc', 'txt'}
    
    @staticmethod
    def init_app(app):
        # Criar pastas necessárias
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
        app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
        app.config['GENERATED_FOLDER'] = Config.GENERATED_FOLDER

    @staticmethod
    def validate_file_path(base_dir, filename):
        """Valida completamente um caminho de arquivo"""
        safe_filename = secure_filename(filename)
        if not safe_filename or safe_filename != filename:
            return None
        
        try:
            base_path = os.path.abspath(base_dir)
            full_path = os.path.abspath(os.path.join(base_path, safe_filename))
            
            # Verificação adicional para symlinks
            if os.path.islink(full_path):
                return None
                
            # Verifica se está dentro do diretório base
            if not full_path.startswith(base_path):
                return None
                
            return full_path
        except Exception:
            return None