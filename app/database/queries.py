# =================================================================================
# MÓDULO DE CONSULTAS AO BANCO DE DADOS (queries.py)
# Local: app/database/queries.py
# =================================================================================

import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

# --- NOVA QUERY PARA VERIFICAR O NÚMERO DE USUÁRIOS ---
def count_users() -> int:
    """
    Conta o número total de usuários registrados no banco de dados.
    :return: Um inteiro representando o total de usuários.
    """
    conn = get_db_connection()
    if conn is None: return 0
    try:
        cursor = conn.execute("SELECT COUNT(id) FROM usuarios")
        # fetchone() em uma query COUNT retorna uma tupla com um único valor, ex: (1,)
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logger.error(f"Erro ao contar usuários: {e}", exc_info=True)
        return 0 # Retorna 0 em caso de erro para evitar bloqueios indevidos.
    finally:
        if conn: conn.close()

def get_user_by_email(email: str):
    """Busca um usuário no banco de dados pelo seu e-mail."""
    logger.info(f"Buscando usuário com o e-mail: {email}")
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {e}", exc_info=True)
        return None
    finally:
        if conn: conn.close()

def create_user(nome: str, email: str, senha_hash: str, whatsapp: str = None):
    """Insere um novo usuário no banco de dados."""
    logger.info(f"Tentando criar um novo usuário com e-mail: {email}")
    conn = get_db_connection()
    if conn is None: return
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, whatsapp) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, whatsapp)
        )
        conn.commit()
        logger.info(f"Usuário '{email}' criado com sucesso.")
    except conn.IntegrityError:
        logger.warning(f"Usuário com e-mail '{email}' já existe no banco de dados.")
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}", exc_info=True)
        conn.rollback()
    finally:
        if conn: conn.close()

def find_or_create_category(nome: str) -> int:
    """Busca uma categoria pelo nome. Se não encontrar, cria uma nova."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row: return row['id']
        else:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
            conn.commit()
            return cursor.lastrowid
    finally:
        if conn: conn.close()

def find_or_create_unit(nome: str, sigla: str) -> int:
    """Busca uma unidade de medida pelo nome. Se não encontrar, cria uma nova."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM unidades_medida WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row: return row['id']
        else:
            cursor.execute("INSERT INTO unidades_medida (nome, sigla) VALUES (?, ?)", (nome, sigla))
            conn.commit()
            return cursor.lastrowid
    finally:
        if conn: conn.close()

def create_item_if_not_exists(nome: str, id_categoria: int, id_unidade_medida: int):
    """Cria um novo item no banco de dados, somente se ele não existir."""
    conn = get_db_connection()
    if conn is None: return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM itens WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if not row:
            cursor.execute(
                "INSERT INTO itens (nome, id_categoria, id_unidade_medida) VALUES (?, ?, ?)",
                (nome, id_categoria, id_unidade_medida)
            )
            conn.commit()
            logger.info(f"Item padrão '{nome}' inserido no banco de dados.")
    except Exception as e:
        logger.error(f"Erro ao inserir o item '{nome}': {e}", exc_info=True)
        conn.rollback()
    finally:
        if conn: conn.close()
        
def has_establishment(user_id: int) -> bool:
    """Verifica se um usuário já possui um estabelecimento cadastrado."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cursor = conn.execute("SELECT 1 FROM estabelecimentos WHERE id_usuario = ?", (user_id,))
        return cursor.fetchone() is not None
    finally:
        if conn: conn.close()

def complete_onboarding(user_id: int, user_name: str, establishment_name: str, location_name: str):
    """Salva os dados do onboarding, criando o estabelecimento e o local de estoque."""
    conn = get_db_connection()
    if conn is None: return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET nome = ? WHERE id = ?", (user_name, user_id))
        cursor.execute(
            "INSERT INTO estabelecimentos (id_usuario, nome) VALUES (?, ?)",
            (user_id, establishment_name)
        )
        establishment_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO locais_estoque (id_estabelecimento, nome) VALUES (?, ?)",
            (establishment_id, location_name)
        )
        conn.commit()
        logger.info(f"Onboarding concluído para o usuário ID {user_id}.")
    except Exception as e:
        logger.error(f"Erro ao completar o onboarding para o usuário ID {user_id}: {e}", exc_info=True)
        conn.rollback()
    finally:
        if conn: conn.close()

def get_establishment_by_user_id(user_id: int):
    """
    Busca o estabelecimento de um usuário pelo ID do usuário.
    :param user_id: O ID do usuário.
    :return: Um objeto de linha (sqlite3.Row) com os dados do estabelecimento ou None.
    """
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM estabelecimentos WHERE id_usuario = ?", (user_id,))
        establishment = cursor.fetchone()
        return establishment
    finally:
        if conn: conn.close()