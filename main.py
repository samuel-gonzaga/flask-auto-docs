from flask import Flask
from config import Config
from blueprints.documents import bp as documents_bp
from logger_config import setup_logger
from flask_moment import Moment
from datetime import datetime
import os
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['WTF_CSRF_ENABLED'] = True
    csrf = CSRFProtect(app)

    
    # Inicializar extensões
    setup_logger()
    moment = Moment(app)
    
    # Configurações adicionais
    Config.init_app(app)
    
    # Registrar filtros customizados
    @app.template_filter('datetimeformat')
    def datetimeformat_filter(value, format='%d/%m/%Y %H:%M'):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d')
        return value.strftime(format)
    
    @app.template_global()
    def get_file_mod_time(filepath):
        return datetime.fromtimestamp(os.path.getmtime(filepath))
    
    # Registrar blueprints
    app.register_blueprint(documents_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)