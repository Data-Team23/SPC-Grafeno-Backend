import psycopg2
from faker import Faker
import random

fake = Faker()

# Configurações do banco
DATABASE_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "localhost",
    "port": 5432,
}

def execute_query(query, params=None):
    try:
        with psycopg2.connect(**DATABASE_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cur.fetchall()
    except Exception as e:
        print(f"Erro: {e}")

def test_load_inserts():
    for _ in range(1000):
        name = fake.name()
        email = fake.email()
        age = random.randint(18, 99)
        query = "INSERT INTO DBTesting (nome, email, idade) VALUES (%s, %s, %s)"
        execute_query(query, (name, email, age))

if __name__ == "__main__":
    test_load_inserts()
