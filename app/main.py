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
from app.views.cadastros_view import create_cadastros_view
from app.views.itens_crud_view import ItensCRUDView
from app.database.seeder import seed_database
from app.database import queries
from app.database.database import initialize_database
from app.styles.style import AppThemes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================
class DoseCertaApp:
    def __init__(self, page: ft.Page):
        # A inicialização permanece a mesma...
        self.page = page
        self.current_user = None
        self.setup_page()
        self.setup_routes()
        initialize_database()
        auth_service.create_default_user() 
        seed_database()
        self.page.go("/")

    # ... (outros métodos como on_login_success, logout, etc. permanecem os mesmos) ...

    def on_login_success(self, user: dict):
        self.current_user = user
        if queries.has_establishment(user['id']):
            self.page.go("/dashboard")
        else:
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        self.page.go("/dashboard")

    def on_register_success(self):
        self.page.go("/")

    def logout(self):
        if self.current_user:
            logger.info(f"Usuário {self.current_user.get('email', '')} deslogado.")
        self.current_user = None
        self.page.go("/")

    def setup_page(self):
        self.page.title = "App Dose Certa"
        self.page.theme = AppThemes.light_theme
        self.page.dark_theme = AppThemes.dark_theme
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 400
        self.page.window_height = 700
        self.page.window_resizable = False
        self.page.padding = 0

    def setup_routes(self):
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        self.page.views.clear()
        public_routes = ["/", "/register"]
        
        if self.page.route in public_routes:
            if self.page.route == "/":
                self.page.views.append(create_login_view(self.on_login_success))
            elif self.page.route == "/register":
                self.page.views.append(
                    create_register_view(
                        page=self.page, 
                        on_logout=self.logout, 
                        on_register_success=self.on_register_success
                    )
                )
        elif self.current_user:
            if self.page.route == "/onboarding":
                self.page.views.append(create_onboarding_view(self.current_user, self.on_onboarding_complete))
            elif self.page.route == "/dashboard":
                self.page.views.append(create_dashboard_view(self.current_user, self.page, self.logout))
            elif self.page.route == "/cadastros":
                self.page.views.append(create_cadastros_view(self.page, self.logout))
            
            # --- CORREÇÃO APLICADA AQUI ---
            elif self.page.route == "/cadastros/item":
                # 1. Cria a instância da view.
                itens_view = ItensCRUDView(self.page, self.logout)
                # 2. Adiciona a view à página.
                self.page.views.append(itens_view)
                # 3. CHAMA O MÉTODO PARA CARREGAR OS DADOS.
                #    Isso garante que a tabela seja preenchida após a view ser criada.
                itens_view.load_all_data()
            else:
                self.page.go("/dashboard")
        else:
            self.page.go("/")
        
        self.page.update()

    def on_view_pop(self, e: ft.ViewPopEvent):
        if e.view.route == "/dashboard":
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

