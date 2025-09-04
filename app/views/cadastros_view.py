# =================================================================================
# MÓDULO DA VIEW DE CADASTROS (cadastros_view.py)
# =================================================================================

import flet as ft
import logging
from app.styles.style import AppDimensions, main_button_style
# --- NOVO: Importa a AppBar reutilizável ---
from app.components import create_app_bar

logger = logging.getLogger(__name__)

# --- ATUALIZADO: A view agora aceita page e on_logout como argumentos ---
def create_cadastros_view(page: ft.Page, on_logout) -> ft.View:
    """Cria e retorna a View que serve como menu para os cadastros."""
    logger.info("Criando a view de Cadastros.")

    # --- ATUALIZADO: Cria a AppBar e define seu título ---
    app_bar = create_app_bar(page, on_logout)
    app_bar.title = ft.Text("Módulo de Cadastros")

    # --- (Definição dos botões permanece a mesma) ---
    cadastro_item_button = ft.ElevatedButton(
        text="Cadastro de Itens", icon=ft.Icons.ADD_BOX_OUTLINED, 
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/item")
    )
    
    cadastro_local_button = ft.ElevatedButton(
        text="Cadastro de Local de Estoque", icon=ft.Icons.INVENTORY_2_OUTLINED,
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/local")
    )

    cadastro_unidade_button = ft.ElevatedButton(
        text="Cadastro de Unidade de Medida", icon=ft.Icons.SQUARE_FOOT_OUTLINED,
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/cadastros/unidade")
    )

    saida_itens_button = ft.ElevatedButton(
        text="Saída de Itens", icon=ft.Icons.REMOVE_SHOPPING_CART_OUTLINED,
        width=AppDimensions.FIELD_WIDTH, style=main_button_style,
        on_click=lambda e: e.page.go("/saidas")
    )

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/cadastros",
        appbar=app_bar, # Usa a AppBar padronizada
        controls=[
            ft.Column(
                [
                    cadastro_item_button,
                    cadastro_local_button,
                    cadastro_unidade_button,
                    saida_itens_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=20,
            )
        ]
    )