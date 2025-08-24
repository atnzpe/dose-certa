# =================================================================================
# MÓDULO DE CONSULTAS AO BANCO DE DADOS (queries.py)
# Local: app/database/queries.py
# =================================================================================

import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

def count_users() -> int:
    """Conta o número total de usuários registrados no banco de dados."""
    conn = get_db_connection()
    if conn is None: return 0
    try:
        cursor = conn.execute("SELECT COUNT(id) FROM usuarios")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logger.error(f"Erro ao contar usuários: {e}", exc_info=True)
        return 0
    finally:
        if conn: conn.close()

# --- NOVA QUERY PARA VERIFICAR USUÁRIO REAL ---
def has_real_user() -> bool:
    """
    Verifica se existe algum usuário "real" (não o admin padrão) no banco.
    :return: True se existir pelo menos um usuário não-admin, False caso contrário.
    """
    conn = get_db_connection()
    # Assume True para ser seguro e bloquear o registro em caso de erro de conexão.
    if conn is None: return True
    try:
        # Procura por qualquer usuário cujo e-mail seja diferente do admin padrão.
        cursor = conn.execute("SELECT 1 FROM usuarios WHERE email != ?", ("admin@dosedata.com",))
        return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Erro ao verificar a existência de usuário real: {e}", exc_info=True)
        return True # Bloqueia o registro por segurança em caso de erro.
    finally:
        if conn: conn.close()

def get_user_by_email(email: str):
    """Busca um usuário no banco de dados pelo seu e-mail."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        return user
    finally:
        if conn: conn.close()

def create_user(nome: str, email: str, senha_hash: str, whatsapp: str = None):
    """Insere um novo usuário no banco de dados."""
    conn = get_db_connection()
    if conn is None: return
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash, whatsapp) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, whatsapp)
        )
        conn.commit()
    except conn.IntegrityError:
        logger.warning(f"Usuário com e-mail '{email}' já existe no banco de dados.")
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
    finally:
        if conn: conn.close()

def get_establishment_by_user_id(user_id: int):
    """Busca o estabelecimento de um usuário pelo ID do usuário."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM estabelecimentos WHERE id_usuario = ?", (user_id,))
        establishment = cursor.fetchone()
        return establishment
    finally:
        if conn: conn.close()
