# =================================================================================
# MÓDULO DA VIEW DO DASHBOARD (dashboard_view.py)
# Local: app/views/dashboard_view.py
# =================================================================================

import flet as ft
import logging
from app.database import queries

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================

# --- ATUALIZADO: A função agora recebe um callback 'on_logout' ---
def create_dashboard_view(user: dict, page: ft.Page, on_logout) -> ft.View:
    """
    Cria e retorna a View principal do Dashboard.
    """
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
    
    # --- NOVO: Botão de Logout ---
    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        tooltip="Sair",
        on_click=lambda e: on_logout() # Chama o callback de logout.
    )
    
    header = ft.Column(
        [
            ft.Text(f"Usuário: {user_name}", size=16),
            ft.Text(f"Estabelecimento: {establishment_name}", size=20, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )
    
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
        padding=ft.padding.all(15),
    )

    cadastros_button = ft.ElevatedButton(
        text="Cadastros", icon=ft.Icons.EDIT_DOCUMENT, width=300, style=button_style,
        on_click=lambda e: e.page.go("/cadastros")
    )
    contagem_button = ft.ElevatedButton(
        text="Contagem de Estoque", icon=ft.Icons.FORMAT_LIST_NUMBERED, width=300, style=button_style,
        on_click=lambda e: e.page.go("/contagem")
    )
    incluir_button = ft.ElevatedButton(
        text="Incluir Itens", icon=ft.Icons.ADD_SHOPPING_CART, width=300, style=button_style,
        on_click=lambda e: e.page.go("/incluir")
    )
    relatorios_button = ft.ElevatedButton(
        text="Relatórios", icon=ft.Icons.ASSESSMENT, width=300, style=button_style,
        on_click=lambda e: e.page.go("/relatorios")
    )

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text("Dashboard"),
                center_title=True,
                bgcolor=ft.Colors.SURFACE_VARIANT,
                # --- ATUALIZADO: Adiciona os botões à AppBar ---
                actions=[theme_button, logout_button]
            ),
            ft.Column(
                [
                    header,
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    cadastros_button,
                    contagem_button,
                    incluir_button,
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
        padding=0,
    )