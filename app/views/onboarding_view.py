# =================================================================================
# MÓDULO DA VIEW DE ONBOARDING (onboarding_view.py)
# Local: app/views/onboarding_view.py
# =================================================================================

import flet as ft
import logging
from app.database import queries

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================

def create_onboarding_view(user: dict, on_complete) -> ft.View:
    """
    Cria e retorna a View de Onboarding para o primeiro acesso do usuário.

    :param user: Dicionário contendo os dados do usuário logado.
    :param on_complete: Função callback a ser chamada quando o formulário for salvo.
    :return: Um objeto ft.View configurado para a tela de onboarding.
    """
    logger.info(f"Criando a view de onboarding para o usuário: {user['email']}")

    # --- COMPONENTES DA TELA ---
    
    user_name_field = ft.TextField(
        label="Seu Nome Completo",
        value=user.get('nome', ''), # Preenche com o nome atual do usuário.
        width=300,
        prefix_icon=ft.Icons.PERSON,
        border_radius=ft.border_radius.all(10),
    )
    
    establishment_name_field = ft.TextField(
        label="Nome do Estabelecimento",
        hint_text="Ex: Bar do Gleyson",
        width=300,
        prefix_icon=ft.Icons.STORE,
        border_radius=ft.border_radius.all(10),
    )
    
    location_name_field = ft.TextField(
        label="Primeiro Local de Contagem",
        value="Estoque Padrão", # Sugestão padrão.
        width=300,
        prefix_icon=ft.Icons.INVENTORY,
        border_radius=ft.border_radius.all(10),
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED, visible=False)
    progress_ring = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)

    def handle_save_click(e):
        """
        Valida os campos e salva os dados do onboarding no banco de dados.
        """
        user_name = user_name_field.value.strip()
        establishment_name = establishment_name_field.value.strip()
        location_name = location_name_field.value.strip()

        # Validação simples para garantir que os campos não estão vazios.
        if not user_name or not establishment_name or not location_name:
            error_text.value = "Todos os campos são obrigatórios."
            error_text.visible = True
            e.page.update()
            return

        # Desabilita os campos e mostra o progresso.
        user_name_field.disabled = True
        establishment_name_field.disabled = True
        location_name_field.disabled = True
        save_button.disabled = True
        error_text.visible = False
        progress_ring.visible = True
        e.page.update()

        # Chama a query para salvar os dados.
        queries.complete_onboarding(
            user_id=user['id'],
            user_name=user_name,
            establishment_name=establishment_name,
            location_name=location_name
        )
        
        # Chama o callback para notificar a conclusão.
        on_complete()

    save_button = ft.ElevatedButton(
        text="Salvar e Começar",
        width=300,
        height=45,
        icon=ft.Icons.SAVE,
        on_click=handle_save_click
    )

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/onboarding",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.WAVING_HAND, size=32),
                        ft.Text("Bem-vindo(a)!", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Vamos configurar sua conta rapidamente.",
                            size=16,
                            color=ft.Colors.WHITE70
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        user_name_field,
                        establishment_name_field,
                        location_name_field,
                        error_text,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row([save_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20,
    )