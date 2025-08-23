# =================================================================================
# MÓDULO DA VIEW DE LOGIN (login_view.py)
# Local: app/views/login_view.py
# =================================================================================

import flet as ft
import logging
from app.services import auth_service
from app.database import queries

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================

def create_login_view(on_login_success) -> ft.View:
    """
    Cria e retorna a View de Login com todos os seus componentes visuais e lógica.
    """
    logger.info("Criando a interface gráfica e a lógica da tela de login.")

    has_registered_user = queries.has_real_user()
    is_registration_allowed = not has_registered_user

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
        # ... (lógica de login permanece a mesma)
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
            on_login_success(user)
        else:
            error_text.value = "E-mail ou senha inválidos."
            error_text.visible = True
        
        email_field.disabled = False
        password_field.disabled = False
        login_button.disabled = False
        progress_ring.visible = False
        e.page.update()
        
    # --- NOVA FUNÇÃO: Manipulador para "Esqueceu a senha" ---
    def handle_forgot_password(e):
        """
        Exibe uma mensagem informativa sobre a recuperação de senha.
        """
        page = e.page
        page.snack_bar = ft.SnackBar(
            content=ft.Text("A recuperação de senha estará disponível na versão online."),
            show_close_icon=True,
        )
        page.snack_bar.open = True
        page.update()

    login_button = ft.ElevatedButton(
        text="Entrar", width=300, height=45, icon=ft.Icons.LOGIN,
        on_click=handle_login_click
    )
    
    google_login_button = ft.OutlinedButton(
        text="Login com Google",
        width=300,
        height=45,
        icon=ft.Icons.LANGUAGE,
    )
    
    signup_button = ft.TextButton(
        "Cadastre-se",
        on_click=lambda e: e.page.go("/register"),
        disabled=not is_registration_allowed,
        tooltip="Apenas um usuário real é permitido na versão gratuita" if not is_registration_allowed else None
    )

    signup_text = ft.Row(
        [
            ft.Text("Não tem uma conta?"),
            signup_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )
    
    # --- NOVO: Botão "Esqueceu a senha" ---
    forgot_password_button = ft.TextButton(
        "Esqueceu a senha?",
        on_click=handle_forgot_password,
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
                        # Adiciona o botão "Esqueceu a senha" alinhado à direita
                        ft.Row([forgot_password_button], alignment=ft.MainAxisAlignment.END),
                        error_text,
                        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                        ft.Row([login_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                        google_login_button,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        signup_text,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20,
    )