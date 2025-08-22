# =================================================================================
# MÓDULO DA VIEW DE LOGIN (login_view.py)
# Local: app/views/login_view.py
# =================================================================================

import flet as ft
import logging
from app.services import auth_service

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================

# --- CORREÇÃO: A função agora aceita 'on_login_success' como um argumento posicional. ---
def create_login_view(on_login_success) -> ft.View:
    """
    Cria e retorna a View de Login com todos os seus componentes visuais e lógica.

    :param on_login_success: Uma função (callback) a ser chamada quando o login for bem-sucedido.
    :return: Um objeto ft.View configurado para a tela de login.
    """
    logger.info("Criando a interface gráfica e a lógica da tela de login.")

    email_field = ft.TextField(
        label="E-mail", hint_text="Digite seu e-mail", width=300,
        keyboard_type=ft.KeyboardType.EMAIL, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=ft.border_radius.all(10),
    )
    password_field = ft.TextField(
        label="Senha", hint_text="Digite sua senha", width=300,
        password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE,
        border_radius=ft.border_radius.all(10),
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED, visible=False)
    progress_ring = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)

    def handle_login_click(e):
        email_field.disabled = True
        password_field.disabled = True
        login_button.disabled = True
        error_text.visible = False
        progress_ring.visible = True
        e.page.update()

        email = email_field.value.strip()
        password = password_field.value

        user = auth_service.authenticate_user(email, password)

        if user:
            logger.info(f"Login bem-sucedido para {email}. Chamando o callback.")
            on_login_success(user)
        else:
            error_text.value = "E-mail ou senha inválidos."
            error_text.visible = True
        
        email_field.disabled = False
        password_field.disabled = False
        login_button.disabled = False
        progress_ring.visible = False
        e.page.update()

    login_button = ft.ElevatedButton(
        text="Entrar", width=300, height=45, icon=ft.Icons.LOGIN,
        on_click=handle_login_click
    )
    google_login_button = ft.OutlinedButton(
        text="Login com Google", width=300, height=45, icon=ft.Icons.G_MOBILE_DATA_ROUNDED,
    )
    signup_text = ft.Row(
        [ft.Text("Não tem uma conta?"), ft.TextButton("Cadastre-se")],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Dose Certa", size=32, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        email_field,
                        password_field,
                        error_text,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row([login_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                        google_login_button,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        signup_text,
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