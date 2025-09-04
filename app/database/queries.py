# =================================================================================
# MÓDULO DE CONSULTAS AO BANCO DE DADOS (queries.py) - CORRIGIDO
# =================================================================================

import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

# --- (O início do arquivo com as queries de usuário e onboarding permanece o mesmo) ---
# ... (cole as funções has_real_user, get_user_by_email, create_user, etc. aqui) ...
def has_real_user() -> bool:
    """Verifica se existe algum usuário "real" (não o admin padrão) no banco."""
    conn = get_db_connection()
    if conn is None: return True
    try:
        cursor = conn.execute("SELECT 1 FROM usuarios WHERE email != ?", ("admin@dosedata.com",))
        return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Erro ao verificar a existência de usuário real: {e}", exc_info=True)
        return True
    finally:
        if conn: conn.close()

def get_user_by_email(email: str):
    """Busca um usuário no banco de dados pelo seu e-mail."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        return cursor.fetchone()
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
        cursor.execute("INSERT INTO estabelecimentos (id_usuario, nome) VALUES (?, ?)", (user_id, establishment_name))
        establishment_id = cursor.lastrowid
        cursor.execute("INSERT INTO locais_estoque (id_estabelecimento, nome) VALUES (?, ?)", (establishment_id, location_name))
        conn.commit()
    finally:
        if conn: conn.close()

def get_establishment_by_user_id(user_id: int):
    """Busca o estabelecimento de um usuário pelo ID do usuário."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cursor = conn.execute("SELECT * FROM estabelecimentos WHERE id_usuario = ?", (user_id,))
        return cursor.fetchone()
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

# =================================================================================
# QUERIES PARA O CRUD DE ITENS - CORRIGIDAS
# =================================================================================

def get_all_items_with_details(conn=None):
    """Busca todos os itens do estoque com detalhes. Pode reutilizar uma conexão."""
    # Se nenhuma conexão for passada, abre uma nova.
    close_conn = False
    if conn is None:
        conn = get_db_connection()
        close_conn = True
    
    if conn is None: return []
    try:
        cursor = conn.execute("""
            SELECT 
                i.id, i.nome, i.id_categoria, i.id_unidade_medida,
                c.nome as categoria, 
                u.nome as unidade 
            FROM itens i
            LEFT JOIN categorias c ON i.id_categoria = c.id
            LEFT JOIN unidades_medida u ON i.id_unidade_medida = u.id
            ORDER BY i.nome
        """)
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao buscar todos os itens: {e}", exc_info=True)
        return []
    finally:
        # Fecha a conexão apenas se ela foi criada dentro desta função.
        if close_conn and conn: conn.close()

def get_all_categories(conn=None):
    """Busca todas as categorias. Pode reutilizar uma conexão."""
    close_conn = False
    if conn is None:
        conn = get_db_connection()
        close_conn = True

    if conn is None: return []
    try:
        cursor = conn.execute("SELECT id, nome FROM categorias ORDER BY nome")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        if close_conn and conn: conn.close()

def get_all_units(conn=None):
    """Busca todas as unidades de medida. Pode reutilizar uma conexão."""
    close_conn = False
    if conn is None:
        conn = get_db_connection()
        close_conn = True

    if conn is None: return []
    try:
        cursor = conn.execute("SELECT id, nome, sigla FROM unidades_medida ORDER BY nome")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        if close_conn and conn: conn.close()

# --- As funções de escrita (add, update, delete) não precisam de alteração ---
# Elas são operações atômicas e é aceitável que abram e fechem sua própria conexão.
def add_item(nome: str, id_categoria: int, id_unidade_medida: int):
    """Adiciona um novo item ao banco de dados."""
    conn = get_db_connection()
    if conn is None: return
    try:
        conn.execute(
            "INSERT INTO itens (nome, id_categoria, id_unidade_medida) VALUES (?, ?, ?)",
            (nome, id_categoria, id_unidade_medida)
        )
        conn.commit()
        logger.info(f"Item '{nome}' adicionado com sucesso.")
    except conn.IntegrityError:
        logger.warning(f"Item com nome '{nome}' já existe.")
    finally:
        if conn: conn.close()

def update_item(item_id: int, nome: str, id_categoria: int, id_unidade_medida: int):
    """Atualiza os dados de um item existente."""
    conn = get_db_connection()
    if conn is None: return
    try:
        conn.execute(
            "UPDATE itens SET nome = ?, id_categoria = ?, id_unidade_medida = ? WHERE id = ?",
            (nome, id_categoria, id_unidade_medida, item_id)
        )
        conn.commit()
        logger.info(f"Item ID {item_id} atualizado com sucesso.")
    finally:
        if conn: conn.close()

def delete_item(item_id: int):
    """Exclui um item do banco de dados."""
    conn = get_db_connection()
    if conn is None: return
    try:
        conn.execute("DELETE FROM itens WHERE id = ?", (item_id,))
        conn.commit()
        logger.info(f"Item ID {item_id} excluído com sucesso.")
    finally:
        if conn: conn.close()