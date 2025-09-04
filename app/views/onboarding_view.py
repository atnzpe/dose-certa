# =================================================================================
# MÓDULO DA VIEW DE ONBOARDING (onboarding_view.py)
# =================================================================================

import flet as ft
import logging
from app.database import queries
# --- NOVO: Importa as constantes de estilo ---
from app.styles.style import AppFonts, AppDimensions

logger = logging.getLogger(__name__)


def create_onboarding_view(user: dict, on_complete) -> ft.View:
    """
    Cria e retorna a View de Onboarding para o primeiro acesso do usuário.
    """
    logger.info(
        f"Criando a view de onboarding para o usuário: {user['email']}")

    # --- COMPONENTES DA TELA ---

    user_name_field = ft.TextField(
        label="Seu Nome Completo",
        value=user.get('nome', ''),
        width=AppDimensions.FIELD_WIDTH,
        prefix_icon=ft.Icons.PERSON,
        border_radius=ft.border_radius.all(AppDimensions.BORDER_RADIUS),
    )

    establishment_name_field = ft.TextField(
        label="Nome do Estabelecimento",
        hint_text="Ex: Bar do Gleyson",
        width=AppDimensions.FIELD_WIDTH,
        prefix_icon=ft.Icons.STORE,
        border_radius=ft.border_radius.all(AppDimensions.BORDER_RADIUS),
    )

    location_name_field = ft.TextField(
        label="Primeiro Local de Contagem",
        value="Estoque Padrão",
        width=AppDimensions.FIELD_WIDTH,
        prefix_icon=ft.Icons.INVENTORY,
        border_radius=ft.border_radius.all(AppDimensions.BORDER_RADIUS),
    )

    error_text = ft.Text(value="", visible=False)
    progress_ring = ft.ProgressRing(
        width=20, height=20, stroke_width=2, visible=False)

    def handle_save_click(e):
        """
        Valida os campos e salva os dados do onboarding no banco de dados.
        """
        user_name = user_name_field.value.strip()
        establishment_name = establishment_name_field.value.strip()
        location_name = location_name_field.value.strip()

        if not user_name or not establishment_name or not location_name:
            error_text.value = "Todos os campos são obrigatórios."
            error_text.color = e.page.theme.color_scheme.error
            error_text.visible = True
            e.page.update()
            return

        for field in [user_name_field, establishment_name_field, location_name_field, save_button]:
            field.disabled = True
        progress_ring.visible = True
        e.page.update()

        queries.complete_onboarding(
            user_id=user['id'],
            user_name=user_name,
            establishment_name=establishment_name,
            location_name=location_name
        )

        on_complete()

    save_button = ft.ElevatedButton(
        text="Salvar e Começar",
        width=AppDimensions.FIELD_WIDTH,
        height=45,
        icon=ft.Icons.SAVE,
        on_click=handle_save_click
    )

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/onboarding",
        controls=[
            ft.Column(
                [
                    ft.Icon(ft.Icons.WAVING_HAND, size=AppFonts.TITLE_LARGE),
                    ft.Text("Bem-vindo(a)!", size=AppFonts.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD),
                    ft.Text("Vamos configurar sua conta rapidamente.",
                            size=AppFonts.BODY_MEDIUM),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    user_name_field,
                    establishment_name_field,
                    location_name_field,
                    error_text,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row([save_button, progress_ring],
                           alignment=ft.MainAxisAlignment.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
