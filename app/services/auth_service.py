# =================================================================================
# MÓDULO DE SERVIÇO DE AUTENTICAÇÃO (auth_service.py)
# Local: app/services/auth_service.py
# =================================================================================

# Módulo para hashing de senhas.
import hashlib
# Módulo de logging para registrar eventos.
import logging
# Importa as funções de consulta ao banco de dados.
from app.database import queries

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÕES DO SERVIÇO
# =================================================================================

def _hash_password(password: str) -> str:
    """
    Gera um hash SHA-256 para uma senha fornecida.
    NOTA: Em um ambiente de produção, bibliotecas como 'bcrypt' ou 'passlib'
    são recomendadas por serem mais seguras.

    :param password: A senha em texto plano.
    :return: A representação hexadecimal do hash da senha.
    """
    # Converte a senha para bytes, gera o hash e o retorna como uma string hexadecimal.
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_default_user():
    """
    Cria um usuário padrão para fins de teste, se nenhum usuário existir.
    """
    logger.info("Verificando a necessidade de criar um usuário padrão.")
    # E-mail e senha do usuário padrão.
    default_email = "admin@dosedata.com"
    default_password = "admin"
    
    # Verifica se o usuário já existe.
    user = queries.get_user_by_email(default_email)
    if user is None:
        logger.info("Nenhum usuário padrão encontrado. Criando um novo.")
        # Gera o hash da senha padrão.
        password_hash = _hash_password(default_password)
        # Chama a função para criar o usuário no banco de dados.
        queries.create_user(
            nome="Admin Padrão",
            email=default_email,
            senha_hash=password_hash,
            whatsapp="11999999999"
        )
    else:
        logger.info("Usuário padrão já existe.")

def authenticate_user(email: str, password: str) -> dict:
    """
    Autentica um usuário com base no e-mail и na senha.

    :param email: O e-mail fornecido pelo usuário.
    :param password: A senha fornecida pelo usuário.
    :return: Um dicionário com os dados do usuário se a autenticação for bem-sucedida,
             caso contrário, retorna None.
    """
    if not email or not password:
        logger.warning("Tentativa de login com e-mail ou senha vazios.")
        return None

    # Busca o usuário no banco de dados pelo e-mail.
    user_data = queries.get_user_by_email(email)

    # Se nenhum usuário for encontrado, a autenticação falha.
    if user_data is None:
        logger.warning(f"Tentativa de login falhou: e-mail '{email}' não encontrado.")
        return None

    # Gera o hash da senha fornecida pelo usuário.
    provided_password_hash = _hash_password(password)

    # Compara o hash da senha fornecida com o hash armazenado no banco de dados.
    if provided_password_hash == user_data['senha_hash']:
        logger.info(f"Usuário '{email}' autenticado com sucesso.")
        # Retorna os dados do usuário como um dicionário para facilitar o uso.
        return dict(user_data)
    else:
        logger.warning(f"Tentativa de login falhou: senha incorreta para o e-mail '{email}'.")
        return None