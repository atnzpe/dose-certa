# =================================================================================
# MÓDULO DA VIEW DE CADASTRO (register_view.py)
# Local: app/views/register_view.py
# =================================================================================

import flet as ft
import logging
from app.services import auth_service

logger = logging.getLogger(__name__)

# =================================================================================
# FUNÇÃO PRINCIPAL DA VIEW
# =================================================================================

def create_register_view(on_register_success) -> ft.View:
    """
    Cria e retorna a View de Cadastro de novos usuários.

    :param on_register_success: Callback a ser chamado após o cadastro bem-sucedido.
    :return: Um objeto ft.View configurado para a tela de cadastro.
    """
    logger.info("Criando a interface gráfica e a lógica da tela de cadastro.")

    # --- COMPONENTES DA TELA ---
    
    name_field = ft.TextField(
        label="Nome Completo", hint_text="Digite seu nome", width=300,
        prefix_icon=ft.Icons.PERSON, border_radius=ft.border_radius.all(10),
    )
    email_field = ft.TextField(
        label="E-mail", hint_text="Digite seu e-mail", width=300,
        keyboard_type=ft.KeyboardType.EMAIL, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=ft.border_radius.all(10),
    )
    password_field = ft.TextField(
        label="Senha", hint_text="Crie uma senha", width=300,
        password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE,
        border_radius=ft.border_radius.all(10),
    )
    confirm_password_field = ft.TextField(
        label="Confirmar Senha", hint_text="Digite a senha novamente", width=300,
        password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE,
        border_radius=ft.border_radius.all(10),
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED, visible=False)
    progress_ring = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)

    def handle_register_click(e):
        """
        Valida os dados do formulário e tenta registrar o novo usuário.
        """
        # Limpa erros anteriores
        error_text.visible = False
        
        # Validações
        if not all([name_field.value, email_field.value, password_field.value, confirm_password_field.value]):
            error_text.value = "Todos os campos são obrigatórios."
            error_text.visible = True
            e.page.update()
            return
        
        if password_field.value != confirm_password_field.value:
            error_text.value = "As senhas não coincidem."
            error_text.visible = True
            e.page.update()
            return

        # Desabilita campos e mostra progresso
        for field in [name_field, email_field, password_field, confirm_password_field, register_button]:
            field.disabled = True
        progress_ring.visible = True
        e.page.update()

        # Chama o serviço de autenticação para registrar o usuário
        result, message = auth_service.register_user(
            name=name_field.value.strip(),
            email=email_field.value.strip(),
            password=password_field.value
        )

        if result:
            # Se o cadastro for bem-sucedido, chama o callback
            on_register_success()
        else:
            # Se falhar, exibe a mensagem de erro
            error_text.value = message
            error_text.visible = True

        # Reabilita campos e esconde progresso
        for field in [name_field, email_field, password_field, confirm_password_field, register_button]:
            field.disabled = False
        progress_ring.visible = False
        e.page.update()

    register_button = ft.ElevatedButton(
        text="Cadastrar", width=300, height=45, icon=ft.Icons.APP_REGISTRATION,
        on_click=handle_register_click
    )
    
    login_text = ft.Row(
        [
            ft.Text("Já tem uma conta?"),
            ft.TextButton("Faça o login", on_click=lambda e: e.page.go("/")),
        ],
        alignment=ft.MainAxisAlignment.CENTER, spacing=5,
    )

    # --- ESTRUTURA DA VIEW ---
    return ft.View(
        route="/register",
        controls=[
            ft.AppBar(title=ft.Text("Criar Nova Conta"), bgcolor=ft.Colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Column(
                    [
                        name_field,
                        email_field,
                        password_field,
                        confirm_password_field,
                        error_text,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row([register_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        login_text,
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
