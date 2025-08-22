# =================================================================================
# MÓDULO DA VIEW DE LOGIN (login_view.py)
# Local: app/views/login_view.py
# =================================================================================

# Módulo principal do Flet para construção da interface.
import flet as ft

# Módulo de logging para registrar eventos.
import logging

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================


def create_login_view(page: ft.Page) -> ft.View:
    """
    Cria e retorna a View de Login com todos os seus componentes visuais.

    :param page: A página Flet principal, usada para navegação.
    :return: Um objeto ft.View configurado para a tela de login.
    """
    logger.info("Criando a interface gráfica da tela de login.")

    # --- COMPONENTES DA TELA ---

    # Campo de texto para o e-mail do usuário.
    email_field = ft.TextField(
        label="E-mail",
        hint_text="Digite seu e-mail",
        width=300,
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.icons.EMAIL_OUTLINED,
        border_radius=ft.border_radius.all(10),
    )

    # Campo de texto para a senha do usuário.
    password_field = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        width=300,
        password=True,  # Oculta o texto digitado.
        can_reveal_password=True,  # Adiciona um ícone para mostrar/ocultar a senha.
        prefix_icon=ft.icons.LOCK_OUTLINE,
        border_radius=ft.border_radius.all(10),
    )

    # Botão principal para realizar o login.
    # A lógica de clique (on_click) será implementada no próximo sprint.
    login_button = ft.ElevatedButton(
        text="Entrar",
        width=300,
        height=45,
        icon=ft.icons.LOGIN,
        # on_click=lambda e: page.go("/dashboard") # Lógica temporária para teste
    )

    # Botão para login com a conta do Google.
    google_login_button = ft.OutlinedButton(
        text="Login com Google",
        width=300,
        height=45,
        icon=ft.icons.G_MOBILE_DATA_ROUNDED,
        # on_click=... # Lógica a ser implementada futuramente
    )

    # Texto com link para a tela de cadastro.
    signup_text = ft.Row(
        [
            ft.Text("Não tem uma conta?"),
            ft.TextButton(
                "Cadastre-se",
                # on_click=... # Lógica para navegar para a tela de cadastro
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
    )

    # --- ESTRUTURA DA VIEW ---

    # Cria a View, que é o contêiner principal de uma tela no Flet.
    login_view = ft.View(
        route="/",  # Define a rota que ativa esta view.
        controls=[
            # Usamos um contêiner para centralizar todo o conteúdo.
            ft.Container(
                content=ft.Column(
                    [
                        # Logo ou título do aplicativo.
                        ft.Text("Dose Certa", size=32, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        # Campos de entrada.
                        email_field,
                        password_field,
                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                        # Botões de ação.
                        login_button,
                        google_login_button,
                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                        # Link de cadastro.
                        signup_text,
                    ],
                    # Alinhamento dos controles dentro da coluna.
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,  # Espaçamento vertical entre os elementos.
                ),
                # Alinhamento do contêiner na página.
                alignment=ft.alignment.center,
                expand=True,  # Faz o contêiner ocupar todo o espaço disponível.
            )
        ],
        # Configurações de alinhamento para a View inteira.
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20,
    )

    return login_view
