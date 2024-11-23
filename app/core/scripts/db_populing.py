import os
import django
from faker import Faker
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seu_projeto.settings")  # Substitua "seu_projeto" pelo nome do seu projeto
django.setup()

# Importar os modelos
from sua_app.models import Usuario  # Substitua "sua_app" e "Usuario" pelos nomes corretos

# Inicializar o Faker
fake = Faker()

# Função para popular o banco
def popular_usuarios(quantidade=100):
    usuarios = []
    for _ in range(quantidade):
        usuario = Usuario(
            nome=fake.name(),
            email=fake.email(),
            idade=random.randint(18, 99),
        )
        usuarios.append(usuario)
    
    # Criar registros em massa
    Usuario.objects.bulk_create(usuarios)
    print(f"{quantidade} usuários criados com sucesso!")

if __name__ == "__main__":
    # Quantidade de registros a criar
    quantidade = 1000  # Altere conforme necessário
    popular_usuarios(quantidade)
