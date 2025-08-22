# =================================================================================
# MÓDULO DE CONSULTAS AO BANCO DE DADOS (queries.py)
# Local: app/database/queries.py
# =================================================================================

# Módulo de logging para registrar eventos.
import logging
# Importa a função de conexão do nosso módulo de database.
from .database import get_db_connection

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÕES DE CONSULTA (QUERIES)
# =================================================================================

def get_user_by_email(email: str):
    """
    Busca um usuário no banco de dados pelo seu e-mail.

    :param email: O e-mail do usuário a ser pesquisado.
    :return: Um objeto de linha (sqlite3.Row) contendo os dados do usuário
             ou None se nenhum usuário for encontrado.
    """
    logger.info(f"Buscando usuário com o e-mail: {email}")
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        # Executa a consulta SQL para selecionar o usuário.
        # O uso de '?' previne contra ataques de SQL Injection.
        cursor = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone() # Retorna a primeira linha encontrada.
        return user
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {e}", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def create_user(nome: str, email: str, senha_hash: str, whatsapp: str = None):
    """
    Insere um novo usuário no banco de dados.

    :param nome: Nome do novo usuário.
    :param email: E-mail do novo usuário.
    :param senha_hash: O hash da senha do novo usuário.
    :param whatsapp: Número do WhatsApp (opcional).
    """
    logger.info(f"Tentando criar um novo usuário com e-mail: {email}")
    conn = get_db_connection()
    if conn is None:
        return

    try:
        # Executa o comando SQL para inserir um novo registro na tabela 'usuarios'.
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, whatsapp) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, whatsapp)
        )
        conn.commit() # Salva (confirma) a transação.
        logger.info(f"Usuário '{email}' criado com sucesso.")
    except conn.IntegrityError:
        # Este erro ocorre se tentarmos inserir um e-mail que já existe (devido à restrição UNIQUE).
        logger.warning(f"Usuário com e-mail '{email}' já existe no banco de dados.")
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}", exc_info=True)
        conn.rollback() # Desfaz a transação em caso de erro.
    finally:
        if conn:
            conn.close()