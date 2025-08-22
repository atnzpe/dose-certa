# =================================================================================
# MÓDULO DE SERVIÇO DE AUTENTICAÇÃO (auth_service.py)
# Local: app/services/auth_service.py
# =================================================================================

import bcrypt
import logging
from app.database import queries

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÕES DO SERVIÇO
# =================================================================================

def _hash_password(password: str) -> str:
    """Gera um hash seguro para uma senha usando bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto plano corresponde a um hash bcrypt armazenado."""
    try:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except (ValueError, TypeError) as e:
        logger.error(f"Erro ao verificar a senha. O hash pode estar malformado: {e}")
        return False

def create_default_user():
    """Cria um usuário padrão para fins de teste, se nenhum usuário existir."""
    logger.info("Verificando a necessidade de criar um usuário padrão.")
    default_email = "admin@dosedata.com"
    default_password = "admin"
    
    user = queries.get_user_by_email(default_email)
    if user is None:
        logger.info("Nenhum usuário padrão encontrado. Criando um novo com hash bcrypt.")
        password_hash = _hash_password(default_password)
        queries.create_user(
            nome="Admin Padrão",
            email=default_email,
            senha_hash=password_hash,
            whatsapp="11999999999"
        )
    else:
        logger.info("Usuário padrão já existe.")

def authenticate_user(email: str, password: str) -> dict:
    """Autentica um usuário com base no e-mail e na senha, agora usando bcrypt."""
    if not email or not password:
        logger.warning("Tentativa de login com e-mail ou senha vazios.")
        return None

    user_data = queries.get_user_by_email(email)

    if user_data is None:
        logger.warning(f"Tentativa de login falhou: e-mail '{email}' não encontrado.")
        return None

    stored_hash = user_data['senha_hash']
    
    if _verify_password(password, stored_hash):
        logger.info(f"Usuário '{email}' autenticado com sucesso.")
        return dict(user_data)
    else:
        logger.warning(f"Tentativa de login falhou: senha incorreta para o e-mail '{email}'.")
        return None

# --- NOVA FUNÇÃO PARA REGISTRO DE USUÁRIO ---
def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    """
    Registra um novo usuário no sistema.

    :param name: Nome do usuário.
    :param email: E-mail do usuário.
    :param password: Senha em texto plano.
    :return: Uma tupla (bool, str) indicando sucesso/falha e uma mensagem.
    """
    logger.info(f"Tentativa de registro para o e-mail: {email}")
    
    # Verifica se o usuário já existe
    if queries.get_user_by_email(email):
        message = "Este e-mail já está cadastrado."
        logger.warning(message)
        return False, message
    
    # Gera o hash da senha
    try:
        password_hash = _hash_password(password)
        queries.create_user(nome=name, email=email, senha_hash=password_hash)
        message = "Usuário cadastrado com sucesso!"
        logger.info(message)
        return True, message
    except Exception as e:
        message = "Ocorreu um erro inesperado durante o cadastro."
        logger.error(f"{message} Erro: {e}", exc_info=True)
        return False, message