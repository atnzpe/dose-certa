# =================================================================================
# MÓDULO DE POVOAMENTO DO BANCO DE DADOS (seeder.py)
# Local: app/database/seeder.py
# =================================================================================

import logging
# Importa as novas funções de consulta que acabamos de criar.
from . import queries

logger = logging.getLogger(__name__)

# =================================================================================
# DADOS INICIAIS (Extraídos da planilha e expandidos)
# =================================================================================

INITIAL_CATEGORIES = [
    "Cervejas", "Destilados", "Vinhos", "Refrigerantes",
    "Sucos", "Energéticos", "Água", "Licores", "Xaropes"
]

INITIAL_UNITS = [
    {"nome": "Garrafa 1L", "sigla": "GF 1L"},
    {"nome": "Garrafa 995ml", "sigla": "GF 995ml"},
    {"nome": "Garrafa 900ml", "sigla": "GF 900ml"},
    {"nome": "Garrafa 750ml", "sigla": "GF 750ml"},
    {"nome": "Garrafa 700ml", "sigla": "GF 700ml"},
    {"nome": "Garrafa 600ml", "sigla": "GF 600ml"},
    {"nome": "Garrafa 500ml", "sigla": "GF 500ml"},
    {"nome": "Long Neck", "sigla": "LN"},
    {"nome": "Lata 350ml", "sigla": "LT"},
    {"nome": "Dose 50ml", "sigla": "DS"},
    {"nome": "Dose 30ml", "sigla": "DS 30ml"},
]

INITIAL_ITEMS = [
    # Cervejas
    {"nome": "Heineken", "categoria": "Cervejas", "unidade": "Long Neck"},
    {"nome": "Budweiser", "categoria": "Cervejas", "unidade": "Long Neck"},
    {"nome": "Stella Artois", "categoria": "Cervejas", "unidade": "Long Neck"},
    {"nome": "Original", "categoria": "Cervejas", "unidade": "Garrafa 600ml"},
    
    # Destilados (Gins, Vodkas, Whiskys, etc.)
    {"nome": "Aperol", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Run Bacardi", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "Campari", "categoria": "Destilados", "unidade": "Garrafa 900ml"},
    {"nome": "Gin Beefeater", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Beefeater 24", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Bombay", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Bulldog", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Gordons", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Hendricks", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin London n 1", "categoria": "Destilados", "unidade": "Garrafa 700ml"},
    {"nome": "Gin Monkey 47", "categoria": "Destilados", "unidade": "Garrafa 500ml"},
    {"nome": "Gin Plymouth", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Seagers", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Seagrams", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Tanqueray", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Gin Tanqueray Tem", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Grey Goose", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "José Cuervo Silver", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Smirnoff Red", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "Vodka Absolute Extrakt", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Vodka Absolut Original", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "Vodka Ciroc", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "Vodka Orloff", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "Vodka Skyy", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "Vodka Stolichnaya", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "W Black Label", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Chivas 12", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Chivas 18", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "W Chivas Extra", "categoria": "Destilados", "unidade": "Garrafa 750ml"},
    {"nome": "W Jack Daniels", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Jack Daniels Tenesse Honey", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Jameson", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Logan", "categoria": "Destilados", "unidade": "Garrafa 700ml"},
    {"nome": "W Old Parr", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Old Parr Silver", "categoria": "Destilados", "unidade": "Garrafa 1L"},
    {"nome": "W Red Label", "categoria": "Destilados", "unidade": "Garrafa 1L"},

    # Licores
    {"nome": "Licor 43", "categoria": "Licores", "unidade": "Garrafa 700ml"},
    {"nome": "Licor Amarula", "categoria": "Licores", "unidade": "Garrafa 750ml"},
    {"nome": "Licor Baileys", "categoria": "Licores", "unidade": "Garrafa 750ml"},
    {"nome": "Licor Cointreau", "categoria": "Licores", "unidade": "Garrafa 700ml"},
    {"nome": "Licor Fireball", "categoria": "Licores", "unidade": "Garrafa 750ml"},
    {"nome": "Licor Frangelico", "categoria": "Licores", "unidade": "Garrafa 700ml"},

    # Xaropes
    {"nome": "Monin Frutas Vermelhas", "categoria": "Xaropes", "unidade": "Garrafa 700ml"},
    {"nome": "Monin Gengibre", "categoria": "Xaropes", "unidade": "Garrafa 700ml"},

    # Vinhos e Outros
    {"nome": "Martini Rosso", "categoria": "Vinhos", "unidade": "Garrafa 995ml"},
    {"nome": "Vinho Tinto", "categoria": "Vinhos", "unidade": "Garrafa 750ml"},
    {"nome": "Vinho Branco", "categoria": "Vinhos", "unidade": "Garrafa 750ml"},
    
    # Não alcoólicos
    {"nome": "Coca-Cola", "categoria": "Refrigerantes", "unidade": "Lata 350ml"},
    {"nome": "Guaraná", "categoria": "Refrigerantes", "unidade": "Lata 350ml"},
    {"nome": "Suco de Laranja", "categoria": "Sucos", "unidade": "Garrafa 1L"},
    {"nome": "Red Bull", "categoria": "Energéticos", "unidade": "Lata 350ml"},
    {"nome": "Água com Gás", "categoria": "Água", "unidade": "Garrafa 600ml"},
    {"nome": "Água sem Gás", "categoria": "Água", "unidade": "Garrafa 600ml"}
]

# =================================================================================
# FUNÇÃO PRINCIPAL DE POVOAMENTO
# =================================================================================

def seed_database():
    """
    Executa o processo de povoamento do banco de dados com os dados iniciais.
    A função é idempotente: pode ser executada várias vezes sem duplicar dados.
    """
    logger.info("Iniciando o processo de povoamento (seeding) do banco de dados...")
    
    try:
        # 1. Insere as categorias e armazena seus IDs em um dicionário.
        category_ids = {name: queries.find_or_create_category(name) for name in INITIAL_CATEGORIES}
        logger.info("Categorias iniciais verificadas/inseridas.")

        # 2. Insere as unidades de medida e armazena seus IDs.
        unit_ids = {unit["nome"]: queries.find_or_create_unit(unit["nome"], unit["sigla"]) for unit in INITIAL_UNITS}
        logger.info("Unidades de medida iniciais verificadas/inseridas.")

        # 3. Itera sobre os itens iniciais e os insere no banco de dados.
        for item in INITIAL_ITEMS:
            # Busca os IDs correspondentes nos dicionários que criamos.
            cat_id = category_ids.get(item["categoria"])
            unit_id = unit_ids.get(item["unidade"])
            
            # Insere o item apenas se a categoria e a unidade foram encontradas.
            if cat_id and unit_id:
                queries.create_item_if_not_exists(
                    nome=item["nome"],
                    id_categoria=cat_id,
                    id_unidade_medida=unit_id
                )
            else:
                logger.warning(f"Não foi possível inserir o item '{item['nome']}' pois sua categoria ou unidade não foi encontrada.")
        
        logger.info("Povoamento do banco de dados concluído com sucesso.")

    except Exception as e:
        logger.error(f"Ocorreu um erro durante o povoamento do banco de dados: {e}", exc_info=True)
