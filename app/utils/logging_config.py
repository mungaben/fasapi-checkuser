# app/utils/logging_config.py
import logging
import os

log_file_path = os.path.join(os.getcwd(), 'logs/app.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Append mode
)
