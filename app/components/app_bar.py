# =================================================================================
# MÓDULO DE COMPONENTES REUTILIZÁVEIS - APPBAR (app_bar.py)
# =================================================================================

import flet as ft

def create_app_bar(page: ft.Page, on_logout) -> ft.AppBar:
    """
    Cria e retorna uma AppBar padronizada com ações globais.
    """
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_button.icon = ft.Icons.WB_SUNNY_OUTLINED if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_OUTLINED
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.WB_SUNNY_OUTLINED if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_OUTLINED,
        tooltip="Mudar tema",
        on_click=toggle_theme,
    )
    
    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        tooltip="Sair",
        on_click=lambda e: on_logout()
    )

    return ft.AppBar(
        title=ft.Text(""), # O título será definido em cada view
        center_title=True,
        actions=[theme_button, logout_button]
    )
