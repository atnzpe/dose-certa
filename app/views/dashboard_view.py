# =================================================================================
# MÓDULO DA VIEW DO DASHBOARD (dashboard_view.py)
# =================================================================================

import flet as ft
import logging
from app.database import queries
# --- NOVO: Importa as constantes de estilo ---
from app.styles.style import AppFonts, AppDimensions, main_button_style

logger = logging.getLogger(__name__)

def create_dashboard_view(user: dict, page: ft.Page, on_logout) -> ft.View:
    """Cria e retorna a View principal do Dashboard."""
    logger.info(f"Criando a view do Dashboard para o usuário: {user['email']}")

    establishment = queries.get_establishment_by_user_id(user['id'])
    establishment_name = establishment['nome'] if establishment else "Estabelecimento não encontrado"
    user_name = user.get('nome', 'Usuário')

    def toggle_theme(e):
        """Alterna entre o tema claro e escuro."""
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_button.icon = ft.Icons.WB_SUNNY_OUTLINED if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_OUTLINED
        page.update()

    # --- COMPONENTES DA UI ---
    
    theme_button = ft.IconButton(
        icon=ft.Icons.WB_SUNNY_OUTLINED,
        tooltip="Mudar tema",
        on_click=toggle_theme,
    )
    
    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        tooltip="Sair",
        on_click=lambda e: on_logout()
    )
    
    header = ft.Column(
        [
            ft.Text(f"Usuário: {user_name}", size=AppFonts.BODY_MEDIUM),
            ft.Text(f"Estabelecimento: {establishment_name}", size=AppFonts.BODY_LARGE, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # --- Botões de Navegação ---
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

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(
            title=ft.Text("Dashboard"),
            center_title=True,
            # A cor agora é controlada pelo tema global em main.py
            actions=[theme_button, logout_button]
        ),
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
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
