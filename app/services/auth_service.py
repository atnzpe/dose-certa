# =================================================================================
# MÓDULO DE SERVIÇO DE AUTENTICAÇÃO (auth_service.py)
# Local: app/services/auth_service.py
# =================================================================================

# --- ATUALIZADO: Importa a biblioteca bcrypt para hashing seguro de senhas. ---
import bcrypt
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
    Gera um hash seguro para uma senha usando bcrypt.
    O bcrypt incorpora um "sal" (salt) aleatório para proteger contra ataques
    de rainbow table.

    :param password: A senha em texto plano.
    :return: O hash da senha (em formato de string) para ser armazenado no banco de dados.
    """
    # Converte a senha de string para bytes, que é o formato esperado pelo bcrypt.
    password_bytes = password.encode('utf-8')
    # Gera um "sal" aleatório.
    salt = bcrypt.gensalt()
    # Gera o hash da senha com o sal.
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Retorna o hash decodificado como string para armazenamento no banco de dados.
    return hashed_bytes.decode('utf-8')

def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a um hash bcrypt armazenado.

    :param plain_password: A senha fornecida pelo usuário durante o login.
    :param hashed_password: O hash da senha armazenado no banco de dados.
    :return: True se a senha corresponder, False caso contrário.
    """
    try:
        # Converte a senha em texto plano e o hash para bytes.
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        
        # A função checkpw do bcrypt compara a senha com o hash de forma segura.
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except (ValueError, TypeError) as e:
        # Captura possíveis erros se o hash armazenado for inválido.
        logger.error(f"Erro ao verificar a senha. O hash pode estar malformado: {e}")
        return False

def create_default_user():
    """
    Cria um usuário padrão para fins de teste, se nenhum usuário existir.
    Agora utiliza o hashing com bcrypt.
    """
    logger.info("Verificando a necessidade de criar um usuário padrão.")
    default_email = "admin@dosedata.com"
    default_password = "admin"
    
    user = queries.get_user_by_email(default_email)
    if user is None:
        logger.info("Nenhum usuário padrão encontrado. Criando um novo com hash bcrypt.")
        # --- ATUALIZADO: Gera o hash da senha padrão usando a nova função. ---
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
    """
    Autentica um usuário com base no e-mail e na senha, agora usando bcrypt.

    :param email: O e-mail fornecido pelo usuário.
    :param password: A senha fornecida pelo usuário.
    :return: Um dicionário com os dados do usuário se a autenticação for bem-sucedida,
             caso contrário, retorna None.
    """
    if not email or not password:
        logger.warning("Tentativa de login com e-mail ou senha vazios.")
        return None

    user_data = queries.get_user_by_email(email)

    if user_data is None:
        logger.warning(f"Tentativa de login falhou: e-mail '{email}' não encontrado.")
        return None

    # --- ATUALIZADO: Usa a função de verificação do bcrypt. ---
    # Pega o hash armazenado no banco de dados.
    stored_hash = user_data['senha_hash']
    
    # Compara a senha fornecida com o hash armazenado.
    if _verify_password(password, stored_hash):
        logger.info(f"Usuário '{email}' autenticado com sucesso.")
        return dict(user_data)
    else:
        logger.warning(f"Tentativa de login falhou: senha incorreta para o e-mail '{email}'.")
        return None
