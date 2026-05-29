#!/usr/bin/env python3
"""
Резервное копирование базы данных PostgreSQL и файлов Odoo
Запуск: python3 backup.py
"""

import subprocess
import os
import datetime
import glob
import time
import logging

# Настройки
BACKUP_DIR = "/backup"
DB_NAME = "boking_dance"
DB_USER = "odoo_user"
ODOO_DATA_DIR = "/var/lib/odoo"
KEEP_DAYS = 7

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_backup():
    """Создание резервной копии"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"odoo_backup_{timestamp}")
    
    try:
        os.makedirs(backup_path, exist_ok=True)
        logging.info(f"Создание бэкапа в {backup_path}")
        
        # Бэкап PostgreSQL
        db_backup = os.path.join(backup_path, f"{DB_NAME}.dump")
        subprocess.run([
            "pg_dump", "-h", "localhost", "-U", DB_USER, "-F", "c", "-f", db_backup, DB_NAME
        ], check=True)
        logging.info(f"БД сохранена: {db_backup}")
        
        # Бэкап файлов Odoo
        if os.path.exists(ODOO_DATA_DIR):
            subprocess.run([
              "sudo", "cp", "-r", ODOO_DATA_DIR, backup_path
            ], check=True)
            logging.info(f"Файлы сохранены: {ODOO_DATA_DIR}")
        
        # Очистка старых бэкапов
        for old_backup in glob.glob(os.path.join(BACKUP_DIR, "odoo_backup_*")):
            if os.path.getmtime(old_backup) < (time.time() - KEEP_DAYS * 86400):
                subprocess.run(["rm", "-rf", old_backup])
                logging.info(f"Удалён старый бэкап: {old_backup}")
        
        logging.info(f"Бэкап успешно создан: {backup_path}")
        
    except Exception as e:
        logging.error(f"Ошибка при создании бэкапа: {e}")

if __name__ == "__main__":
    create_backup()
