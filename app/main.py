# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

import flet as ft
import logging

from app.services import auth_service
from app.views.login_view import create_login_view
from app.views.onboarding_view import create_onboarding_view
from app.views.register_view import create_register_view
from app.views.dashboard_view import create_dashboard_view
from app.database.seeder import seed_database
from app.database import queries
from app.database.database import initialize_database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================

class DoseCertaApp:
    def __init__(self, page: ft.Page):
        logger.info("Iniciando a classe DoseCertaApp.")
        self.page = page
        self.current_user = None
        
        self.setup_page()
        self.setup_routes()
        
        initialize_database()
        # Removido a criação de usuário padrão daqui para permitir o cadastro do primeiro usuário.
        # auth_service.create_default_user() 
        seed_database()
        
        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")

    def on_login_success(self, user: dict):
        self.current_user = user
        if queries.has_establishment(user['id']):
            self.page.go("/dashboard")
        else:
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        self.page.go("/dashboard")

    def on_register_success(self):
        logger.info("Cadastro bem-sucedido. Redirecionando para a tela de login.")
        self.page.go("/")

    # --- NOVA FUNÇÃO DE LOGOUT ---
    def logout(self):
        """Limpa a sessão do usuário e retorna para a tela de login."""
        logger.info(f"Usuário {self.current_user['email']} deslogado.")
        self.current_user = None
        self.page.go("/")

    def setup_page(self):
        self.page.title = "App Dose Certa"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 400
        self.page.window_height = 700
        self.page.window_resizable = False
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def setup_routes(self):
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        logger.info(f"Rota alterada para: {self.page.route}")
        self.page.views.clear()

        if self.page.route == "/":
            self.page.views.append(create_login_view(self.on_login_success))
        
        elif self.page.route == "/register":
            self.page.views.append(create_register_view(self.on_register_success))

        elif self.page.route == "/onboarding" and self.current_user:
            self.page.views.append(
                create_onboarding_view(
                    user=self.current_user,
                    on_complete=self.on_onboarding_complete
                )
            )
            
        elif self.page.route == "/dashboard" and self.current_user:
            self.page.views.append(
                # --- ATUALIZADO: Passa a função de logout para a view ---
                create_dashboard_view(
                    user=self.current_user,
                    page=self.page,
                    on_logout=self.logout
                )
            )
        else:
            logger.warning("Acesso não autorizado ou rota inválida. Redirecionando para o login.")
            self.page.views.append(create_login_view(self.on_login_success))
        
        self.page.update()

    def on_view_pop(self, view: ft.View):
        if view.route == "/dashboard":
            return
        
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