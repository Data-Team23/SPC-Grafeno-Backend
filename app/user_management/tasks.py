import os
import subprocess
from celery import shared_task
from minio import Minio
from datetime import datetime
import psycopg2
from pymongo import MongoClient
import json
import logging


MINIO_CLIENT = Minio(
    'minio:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)


@shared_task
def backup_postgres():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    try:
        postgres_backup_file = f'/tmp/postgres_backup_{timestamp}.sql'
        logging.info("Iniciando backup do PostgreSQL...")

        connection = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="db",
            port="5432"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()

        with open(postgres_backup_file, 'w') as backup_file:
            for table in tables:
                table_name = table[0]
                logging.info(f"Realizando backup da tabela {table_name}...")
                cursor.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", backup_file)

        logging.info(f"Backup do PostgreSQL concluído.")
        upload_to_minio(postgres_backup_file, f'backups/postgres/{timestamp}.sql')

        cursor.close()
        connection.close()

    except Exception as e:
        logging.error(f"Erro ao fazer backup do PostgreSQL: {e}")

    if os.path.exists(postgres_backup_file):
        os.remove(postgres_backup_file)
        logging.info(f"Arquivo temporário {postgres_backup_file} removido.")


@shared_task
def backup_mongo_logs():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    try:
        mongo_backup_file = f'/tmp/mongo_logs_backup_{timestamp}.json'
        logging.info("Iniciando backup do MongoDB - Logs...")

        mongo_client = MongoClient('mongodb://mongo_user:mongo_password@mongodb:27017/')
        logs_db = mongo_client['logs']
        
        backup_data = {}
        collections = logs_db.list_collection_names()
        for collection_name in collections:
            collection = logs_db[collection_name]
            backup_data[collection_name] = list(collection.find({}))

        with open(mongo_backup_file, 'w') as f:
            json.dump(backup_data, f, default=str)
        
        logging.info("Backup do MongoDB - Logs concluído.")
        upload_to_minio(mongo_backup_file, f'backups/mongo/logs/{timestamp}.json')

    except Exception as e:
        logging.error(f"Erro ao fazer backup do MongoDB - Logs: {e}")

    if os.path.exists(mongo_backup_file):
        os.remove(mongo_backup_file)
        logging.info(f"Arquivo temporário {mongo_backup_file} removido.")


@shared_task
def backup_mongo_encrypt():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    try:
        mongo_backup_file = f'/tmp/mongo_encrypt_backup_{timestamp}.json'
        logging.info("Iniciando backup do MongoDB - Encrypt...")

        mongo_client = MongoClient('mongodb://mongo_user:mongo_password@mongodb:27017/')
        encrypt_db = mongo_client['encrypt']
        
        backup_data = {}
        collections = encrypt_db.list_collection_names()
        for collection_name in collections:
            collection = encrypt_db[collection_name]
            backup_data[collection_name] = list(collection.find({}))

        with open(mongo_backup_file, 'w') as f:
            json.dump(backup_data, f, default=str)
        
        logging.info("Backup do MongoDB - Encrypt concluído.")
        upload_to_minio(mongo_backup_file, f'backups/mongo/encrypt/{timestamp}.json')

    except Exception as e:
        logging.error(f"Erro ao fazer backup do MongoDB - Encrypt: {e}")

    if os.path.exists(mongo_backup_file):
        os.remove(mongo_backup_file)
        logging.info(f"Arquivo temporário {mongo_backup_file} removido.")


def upload_to_minio(file_path, minio_path):
    try:
        with open(file_path, 'rb') as file_data:
            MINIO_CLIENT.put_object(
                'backups',
                minio_path,
                file_data,
                length=os.path.getsize(file_path),
            )
        logging.info(f"Backup enviado para o MinIO: {minio_path}")
    except Exception as e:
        logging.error(f"Falha ao enviar backup para o MinIO: {e}")
