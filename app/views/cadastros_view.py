# =================================================================================
# MÓDULO DA VIEW DE CADASTROS (cadastros_view.py)
# =================================================================================

import flet as ft
import logging
# --- NOVO: Importa as constantes de estilo ---
from app.styles.style import AppDimensions, main_button_style

logger = logging.getLogger(__name__)

def create_cadastros_view() -> ft.View:
    logger.info("Criando a view de Cadastros.")

    # --- BOTÕES DE NAVEGAÇÃO ---
    
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
        appbar=ft.AppBar(title=ft.Text("Módulo de Cadastros"), center_title=True),
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
                # --- CORREÇÃO: 'expand' precisa de um valor e adicionado espaçamento ---
                expand=True,
                spacing=20,
            )
        ]
    )