# =================================================================================
# MÓDULO DA VIEW DO DASHBOARD (dashboard_view.py)
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.styles.style import AppFonts, AppDimensions, main_button_style
# --- NOVO: Importa a AppBar reutilizável ---
from app.components.app_bar import create_app_bar

logger = logging.getLogger(__name__)

def create_dashboard_view(user: dict, page: ft.Page, on_logout) -> ft.View:
    logger.info(f"Criando a view do Dashboard para o usuário: {user['email']}")

    establishment = queries.get_establishment_by_user_id(user['id'])
    establishment_name = establishment['nome'] if establishment else "Não encontrado"
    user_name = user.get('nome', 'Usuário')

    # Cria a AppBar usando o componente reutilizável e define seu título
    app_bar = create_app_bar(page, on_logout)
    app_bar.title = ft.Text("Dashboard")

    header = ft.Column(
        [
            ft.Text(f"Usuário: {user_name}", size=AppFonts.BODY_MEDIUM),
            ft.Text(f"Estabelecimento: {establishment_name}", size=AppFonts.BODY_LARGE, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )
    
    cadastros_button = ft.ElevatedButton(
        text="Cadastros", icon=ft.Icons.EDIT_DOCUMENT, 
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros")
    )
    contagem_button = ft.ElevatedButton(
        text="Contagem de Estoque", icon=ft.Icons.FORMAT_LIST_NUMBERED, 
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/contagem")
    )
    saidas_button = ft.ElevatedButton(
        text="Registrar Saídas", icon=ft.Icons.REMOVE_SHOPPING_CART, 
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/saidas")
    )
    relatorios_button = ft.ElevatedButton(
        text="Relatórios", icon=ft.Icons.ASSESSMENT, 
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/relatorios")
    )

    return ft.View(
        route="/dashboard",
        appbar=app_bar, # Usa a AppBar criada
        controls=[
            ft.Column(
                [
                    header,
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    cadastros_button,
                    contagem_button,
                    saidas_button,
                    relatorios_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=20,
            )
        ],
    )
