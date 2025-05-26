import logging
import os
from datetime import datetime

def setup_logger():
    # Cria diretório de logs se não existir
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
