# =================================================================================
# MÓDULO DE BANCO DE DADOS (database.py)
# =================================================================================

import sqlite3
import logging
import os

# Configuração básica do logger para registrar eventos importantes.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define o nome do arquivo do banco de dados.
DB_FILE = "dose_certa.db"
# Garante que o caminho do banco de dados seja na raiz do projeto para fácil acesso.
DB_PATH = os.path.join(os.getcwd(), DB_FILE)

def get_db_connection():
    """Cria e retorna um objeto de conexão com o banco de dados SQLite."""
    try:
        # Tenta conectar ao arquivo do banco de dados.
        conn = sqlite3.connect(DB_PATH)
        # Configura a conexão para retornar linhas que se comportam como dicionários.
        conn.row_factory = sqlite3.Row
        # Habilita a imposição de chaves estrangeiras para garantir a integridade dos dados.
        conn.execute("PRAGMA foreign_keys = ON;")
        logger.info(f"Conexão com o banco de dados '{DB_PATH}' estabelecida com sucesso.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar ao banco de dados SQLite: {e}", exc_info=True)
        return None

# Lista contendo os comandos SQL para criar cada uma das tabelas do aplicativo.
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        whatsapp TEXT, senha_hash TEXT, criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS estabelecimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_usuario INTEGER NOT NULL, nome TEXT NOT NULL,
        criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """,
    "CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE NOT NULL);",
    "CREATE TABLE IF NOT EXISTS unidades_medida (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE NOT NULL, sigla TEXT);",
    """
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_categoria INTEGER, id_unidade_medida INTEGER,
        nome TEXT UNIQUE NOT NULL, quantidade_estoque REAL NOT NULL DEFAULT 0, custo_unitario REAL,
        codigo_barras TEXT, ativo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_categoria) REFERENCES categorias (id) ON DELETE SET NULL,
        FOREIGN KEY (id_unidade_medida) REFERENCES unidades_medida (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS locais_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_estabelecimento INTEGER NOT NULL, nome TEXT NOT NULL,
        FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS contagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_local_estoque INTEGER NOT NULL, id_usuario INTEGER NOT NULL,
        data_contagem TEXT NOT NULL DEFAULT (datetime('now', 'localtime')), observacoes TEXT,
        FOREIGN KEY (id_local_estoque) REFERENCES locais_estoque (id) ON DELETE CASCADE,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS contagem_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_contagem INTEGER NOT NULL, id_item INTEGER NOT NULL,
        quantidade_contada REAL NOT NULL, quantidade_sistema REAL NOT NULL,
        FOREIGN KEY (id_contagem) REFERENCES contagens (id) ON DELETE CASCADE,
        FOREIGN KEY (id_item) REFERENCES itens (id) ON DELETE CASCADE
    );
    """,
    # --- NOVAS TABELAS (Atualizadas conforme o planejamento) ---
    """
    CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_item INTEGER NOT NULL, id_usuario INTEGER NOT NULL,
        tipo_movimentacao TEXT NOT NULL, quantidade REAL NOT NULL, 
        data_movimentacao TEXT NOT NULL DEFAULT (datetime('now', 'localtime')), observacao TEXT,
        FOREIGN KEY (id_item) REFERENCES itens (id),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS fichas_tecnicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE NOT NULL,
        descricao TEXT, rendimento REAL DEFAULT 1
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ficha_tecnica_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_ficha_tecnica INTEGER NOT NULL, id_item INTEGER NOT NULL,
        quantidade REAL NOT NULL,
        FOREIGN KEY (id_ficha_tecnica) REFERENCES fichas_tecnicas (id) ON DELETE CASCADE,
        FOREIGN KEY (id_item) REFERENCES itens (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS cardapio_categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE NOT NULL, ordem INTEGER DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS cardapio_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT, id_cardapio_categoria INTEGER NOT NULL,
        id_item_estoque INTEGER, id_ficha_tecnica INTEGER, nome_venda TEXT NOT NULL,
        descricao TEXT, preco_venda REAL NOT NULL, disponivel INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_cardapio_categoria) REFERENCES cardapio_categorias (id),
        FOREIGN KEY (id_item_estoque) REFERENCES itens (id),
        FOREIGN KEY (id_ficha_tecnica) REFERENCES fichas_tecnicas (id)
    );
    """
]

def initialize_database():
    """Executa o script de criação de todas as tabelas do banco de dados."""
    logger.info("Iniciando a inicialização do banco de dados...")
    conn = get_db_connection()
    if conn is None:
        logger.error("Não foi possível inicializar o banco de dados: falha na conexão.")
        return
    try:
        cursor = conn.cursor()
        for table_sql in CREATE_TABLES_SQL:
            cursor.execute(table_sql)
        conn.commit()
        logger.info("Todas as tabelas foram criadas ou já existiam. Banco de dados pronto para uso.")
    except sqlite3.Error as e:
        logger.error(f"Ocorreu um erro ao criar as tabelas: {e}", exc_info=True)
        conn.rollback()
    finally:
        if conn:
            conn.close()
            logger.info("Conexão com o banco de dados fechada.")

# Permite que este script seja executado diretamente para inicializar o banco.
if __name__ == '__main__':
    initialize_database()
