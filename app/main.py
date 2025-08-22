# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

import flet as ft
import logging

from app.services import auth_service
from app.views.login_view import create_login_view

# --- NOVO: Importa a função de seeder ---
from app.database.seeder import seed_database

# Configuração inicial do logging para depuração.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================


class DoseCertaApp:
    """
    Classe principal que encapsula toda a lógica e a interface
    do aplicativo Dose Certa.
    """

    def __init__(self, page: ft.Page):
        """
        Inicializador da classe da aplicação.
        """
        logger.info("Iniciando a classe DoseCertaApp.")
        self.page = page
        self.current_user = None

        self.setup_page()
        self.setup_routes()

        # --- ATUALIZADO: Chama o seeder após criar o usuário padrão ---
        auth_service.create_default_user()
        seed_database()  # Popula o banco com os itens iniciais.

        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")

    def on_login_success(self, user: dict):
        """
        Callback chamado pela view de login quando a autenticação é bem-sucedida.
        """
        logger.info(
            f"Login bem-sucedido para o usuário ID: {user['id']}. Navegando para o dashboard."
        )
        self.current_user = user
        self.page.go("/dashboard")

    def setup_page(self):
        """
        Configura as propriedades visuais globais da página.
        """
        self.page.title = "App Dose Certa"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 400
        self.page.window_height = 700
        self.page.window_resizable = False
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def setup_routes(self):
        """
        Define os manipuladores de rotas.
        """
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        """
        Manipulador de mudança de rota.
        """
        logger.info(f"Rota alterada para: {self.page.route}")
        self.page.views.clear()

        if self.page.route == "/":
            logger.info("Renderizando a view de Login.")
            self.page.views.append(
                create_login_view(on_login_success=self.on_login_success)
            )

        elif self.page.route == "/dashboard" and self.current_user:
            logger.info("Renderizando a view do Dashboard.")
            user_name = self.current_user.get("nome", "Usuário")
            self.page.views.append(
                ft.View(
                    route="/dashboard",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Dashboard"),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        ft.Text(f"Bem-vindo, {user_name}!", size=20),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        else:
            logger.warning(
                "Acesso não autorizado a uma rota protegida. Redirecionando para o login."
            )
            self.page.views.append(
                create_login_view(on_login_success=self.on_login_success)
            )

        self.page.update()

    def on_view_pop(self, view: ft.View):
        """
        Manipula o evento de "voltar".
        """
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    DoseCertaApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
