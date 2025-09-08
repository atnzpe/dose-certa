# =================================================================================
# MÓDULO DA VIEW DE CADASTROS (cadastros_view.py) - VERSÃO REFATORADA
# =================================================================================

# Importa a biblioteca Flet, essencial para a construção da UI.
import flet as ft

# Importa o módulo de logging para registrar informações sobre a execução.
import logging

# Importa as dimensões e estilos padronizados para manter a consistência visual.
from app.styles.style import AppDimensions, main_button_style

# Importa o componente reutilizável da AppBar para manter o cabeçalho padrão.
from app.components import create_app_bar

# Inicializa o logger para este módulo, permitindo um rastreamento detalhado.
logger = logging.getLogger(__name__)


def create_cadastros_view(page: ft.Page, on_logout) -> ft.View:
    """
    Cria e retorna a View que serve como menu central para os módulos de cadastro.

    Args:
        page (ft.Page): A instância da página principal da aplicação.
        on_logout (function): A função de callback a ser executada ao clicar em 'Sair'.

    Returns:
        ft.View: O objeto da view Flet, pronto para ser adicionado à página.
    """
    # Log detalhado: Registra o início da criação da view.
    logger.info("Iniciando a criação da view do menu de Cadastros.")

    # Cria a AppBar padronizada, passando a página e a função de logout.
    app_bar = create_app_bar(page, on_logout)
    # Define o título específico desta view na AppBar.
    app_bar.title = ft.Text("Módulo de Cadastros")

    # --- BOTÕES DO MENU DE CADASTROS ---

    # Botão para navegar para o CRUD de Itens.
    cadastro_item_button = ft.ElevatedButton(
        text="Cadastro de Itens",
        icon=ft.Icons.ADD_BOX_OUTLINED,  # Ícone visualmente relacionado a "adicionar caixas/itens".
        width=AppDimensions.FIELD_WIDTH,  # Largura padronizada.
        style=main_button_style,  # Estilo de botão principal padronizado.
        on_click=lambda e: e.page.go(
            "/cadastros/item"
        ),  # Ação de navegação para a rota de itens.
    )

    # Botão para navegar para o CRUD de Locais de Estoque.
    cadastro_local_button = ft.ElevatedButton(
        text="Cadastro de Local de Estoque",
        icon=ft.Icons.INVENTORY_2_OUTLINED,  # Ícone que remete a inventário/prateleiras.
        width=AppDimensions.FIELD_WIDTH,
        style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/local"),  # Ação de navegação.
    )

    # Botão para navegar para o CRUD de Unidades de Medida.
    cadastro_unidade_button = ft.ElevatedButton(
        text="Cadastro de Unidade de Medida",
        icon=ft.Icons.SQUARE_FOOT_OUTLINED,  # Ícone relacionado a medições.
        width=AppDimensions.FIELD_WIDTH,
        style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/unidade"),  # Ação de navegação.
    )

    # NOVO: Botão para navegar para o CRUD de Fichas Técnicas.
    cadastro_fichas_button = ft.ElevatedButton(
        text="Cadastro de Fichas Técnicas",
        icon=ft.Icons.DESCRIPTION_OUTLINED,  # Ícone que remete a documentos/receitas.
        width=AppDimensions.FIELD_WIDTH,
        style=main_button_style,
        on_click=lambda e: e.page.go(
            "/cadastros/fichas-tecnicas"
        ),  # Ação de navegação.
    )

    # NOVO: Botão para o gerenciamento de Usuários.
    # Nota: A funcionalidade pode ser expandida no futuro.
    gerenciar_usuarios_button = ft.ElevatedButton(
        text="Controle de Usuário",
        icon=ft.Icons.MANAGE_ACCOUNTS_OUTLINED,  # Ícone para gerenciamento de contas.
        width=AppDimensions.FIELD_WIDTH,
        style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/usuarios"),  # Ação de navegação.
        disabled=False,  # Habilitado por padrão, pode ser controlado por permissões no futuro.
    )

    # --- ESTRUTURA FINAL DA VIEW ---
    # Log detalhado: Registra que a view está sendo montada e retornada.
    logger.debug("Montando a estrutura final da ft.View para o menu de cadastros.")
    return ft.View(
        route="/cadastros",  # Rota que ativa esta view.
        appbar=app_bar,  # Adiciona a AppBar criada ao topo da view.
        controls=[
            # A view contém uma única coluna para organizar os botões.
            ft.Column(
                [
                    # Lista de botões a serem exibidos verticalmente.
                    cadastro_item_button,
                    cadastro_local_button,
                    cadastro_unidade_button,
                    cadastro_fichas_button,
                    gerenciar_usuarios_button,
                ],
                # Alinhamento principal: Centraliza a coluna de botões verticalmente na tela.
                alignment=ft.MainAxisAlignment.CENTER,
                # Alinhamento cruzado: Centraliza os botões horizontalmente dentro da coluna.
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # Expand: Faz com que a coluna ocupe todo o espaço vertical disponível.
                expand=True,
                # Espaçamento vertical de 20 pixels entre cada botão.
                spacing=20,
            )
        ],
    )
