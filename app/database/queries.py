# =================================================================================
# MÓDULO DE CONSULTAS AO BANCO DE DADOS (queries.py)
# Local: app/database/queries.py
# =================================================================================

import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

# =================================================================================
# QUERIES DE USUÁRIO
# =================================================================================

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

# =================================================================================
# --- NOVAS QUERIES PARA O SEEDER ---
# =================================================================================

def find_or_create_category(nome: str) -> int:
    """
    Busca uma categoria pelo nome. Se não encontrar, cria uma nova.
    :param nome: O nome da categoria.
    :return: O ID da categoria (existente ou recém-criada).
    """
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row:
            return row['id']
        else:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
            conn.commit()
            return cursor.lastrowid
    finally:
        if conn: conn.close()

def find_or_create_unit(nome: str, sigla: str) -> int:
    """
    Busca uma unidade de medida pelo nome. Se não encontrar, cria uma nova.
    :param nome: O nome da unidade de medida.
    :param sigla: A sigla da unidade de medida.
    :return: O ID da unidade de medida (existente ou recém-criada).
    """
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM unidades_medida WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        if row:
            return row['id']
        else:
            cursor.execute("INSERT INTO unidades_medida (nome, sigla) VALUES (?, ?)", (nome, sigla))
            conn.commit()
            return cursor.lastrowid
    finally:
        if conn: conn.close()

def create_item_if_not_exists(nome: str, id_categoria: int, id_unidade_medida: int):
    """
    Cria um novo item no banco de dados, somente se ele não existir.
    :param nome: O nome do item.
    :param id_categoria: O ID da categoria do item.
    :param id_unidade_medida: O ID da unidade de medida do item.
    """
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