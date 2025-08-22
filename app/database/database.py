# =================================================================================
# MÓDULO DE BANCO DE DADOS (database.py)
# Local: app/database/database.py
# =================================================================================

# Módulo sqlite3 para interação com o banco de dados SQLite.
import sqlite3
# Módulo de logging para registrar eventos e facilitar a depuração.
import logging
# Módulo os para manipulação de caminhos de arquivos.
import os

# Configuração básica do logger para exibir mensagens a partir do nível INFO.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÃO ---
# Define o nome do arquivo do banco de dados.
DB_FILE = "dose_certa.db"
# Constrói o caminho completo para o arquivo do banco de dados, garantindo que ele
# seja criado dentro da pasta 'app/database/'.
DB_PATH = os.path.join(os.path.dirname(__file__), DB_FILE)

# =================================================================================
# 1. FUNÇÃO DE CONEXÃO
# =================================================================================

def get_db_connection():
    """
    Cria e retorna um objeto de conexão com o banco de dados SQLite.
    Habilita o suporte a chaves estrangeiras (foreign keys).

    :return: Um objeto de conexão sqlite3.Connection ou None em caso de erro.
    """
    try:
        # Tenta estabelecer uma conexão com o arquivo de banco de dados no caminho especificado.
        # Se o arquivo não existir, o SQLite o criará automaticamente.
        conn = sqlite3.connect(DB_PATH)
        
        # Define o row_factory para sqlite3.Row. Isso faz com que os resultados das consultas
        # se comportem como dicionários, permitindo o acesso às colunas pelo nome.
        # Ex: row['nome'] em vez de row[1].
        conn.row_factory = sqlite3.Row
        
        # Habilita a imposição de restrições de chave estrangeira. Por padrão, o SQLite
        # aceita a sintaxe de FK, mas não as impõe. Este comando é crucial para a
        # integridade dos dados.
        conn.execute("PRAGMA foreign_keys = ON;")
        
        logger.info(f"Conexão com o banco de dados '{DB_PATH}' estabelecida com sucesso.")
        return conn
        
    except sqlite3.Error as e:
        # Em caso de erro na conexão, registra o erro e retorna None.
        logger.error(f"Erro ao conectar ao banco de dados SQLite: {e}", exc_info=True)
        return None

# =================================================================================
# 2. DEFINIÇÃO DAS ESTRUTURAS DAS TABELAS (SQL DDL)
# =================================================================================

# Uma lista contendo todas as instruções SQL 'CREATE TABLE' para criar o esquema do banco.
# Usar """ (triple quotes) permite que a string ocupe múltiplas linhas, melhorando a legibilidade.

CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        whatsapp TEXT,
        senha_hash TEXT,
        criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS estabelecimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        nome TEXT NOT NULL,
        criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS unidades_medida (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        sigla TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER,
        id_unidade_medida INTEGER,
        nome TEXT UNIQUE NOT NULL,
        quantidade_estoque REAL NOT NULL DEFAULT 0,
        custo_unitario REAL,
        codigo_barras TEXT,
        ativo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (id_categoria) REFERENCES categorias (id) ON DELETE SET NULL,
        FOREIGN KEY (id_unidade_medida) REFERENCES unidades_medida (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS locais_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estabelecimento INTEGER NOT NULL,
        nome TEXT NOT NULL,
        FOREIGN KEY (id_estabelecimento) REFERENCES estabelecimentos (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS contagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_local_estoque INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        data_contagem TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        observacoes TEXT,
        FOREIGN KEY (id_local_estoque) REFERENCES locais_estoque (id) ON DELETE CASCADE,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS contagem_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_contagem INTEGER NOT NULL,
        id_item INTEGER NOT NULL,
        quantidade_contada REAL NOT NULL,
        quantidade_sistema REAL NOT NULL,
        FOREIGN KEY (id_contagem) REFERENCES contagens (id) ON DELETE CASCADE,
        FOREIGN KEY (id_item) REFERENCES itens (id) ON DELETE CASCADE
    );
    """
]

# =================================================================================
# 3. FUNÇÃO DE INICIALIZAÇÃO DO BANCO DE DADOS
# =================================================================================

def initialize_database():
    """
    Executa o script de criação de todas as tabelas do banco de dados.
    Esta função é 'idempotente', ou seja, pode ser executada várias vezes
    sem causar erros, graças ao uso de 'CREATE TABLE IF NOT EXISTS'.
    """
    logger.info("Iniciando a inicialização do banco de dados...")
    
    # Obtém uma conexão com o banco de dados.
    conn = get_db_connection()
    
    # Se a conexão falhar, a função é interrompida.
    if conn is None:
        logger.error("Não foi possível inicializar o banco de dados: falha na conexão.")
        return

    try:
        # Cria um objeto 'cursor' a partir da conexão. O cursor é usado para
        # executar comandos SQL.
        cursor = conn.cursor()
        
        # Itera sobre a lista de comandos SQL.
        for table_sql in CREATE_TABLES_SQL:
            # Executa cada comando 'CREATE TABLE'.
            cursor.execute(table_sql)
            
        # Confirma (salva) todas as alterações feitas na transação atual.
        conn.commit()
        logger.info("Todas as tabelas foram criadas ou já existiam. Banco de dados pronto para uso.")
        
    except sqlite3.Error as e:
        # Em caso de erro durante a execução do SQL, registra a exceção.
        logger.error(f"Ocorreu um erro ao criar as tabelas: {e}", exc_info=True)
        # Desfaz quaisquer alterações feitas na transação atual.
        conn.rollback()
        
    finally:
        # O bloco 'finally' garante que a conexão com o banco de dados seja
        # sempre fechada, mesmo que ocorram erros.
        if conn:
            conn.close()
            logger.info("Conexão com o banco de dados fechada.")

# =================================================================================
# 4. PONTO DE EXECUÇÃO DO SCRIPT
# =================================================================================

# O bloco 'if __name__ == "__main__"' permite que este script seja executado
# diretamente pelo terminal para inicializar o banco de dados manualmente.
# Ex: python app/database/database.py
if __name__ == '__main__':
    initialize_database()
