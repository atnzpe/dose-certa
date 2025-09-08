# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================
# As importações permanecem as mesmas, incluindo 're'.
import flet as ft
import logging
import re
from app.services import auth_service
from app.views.login_view import create_login_view
from app.views.onboarding_view import create_onboarding_view
from app.views.register_view import create_register_view
from app.views.dashboard_view import create_dashboard_view
from app.views.cadastros_view import create_cadastros_view
from app.views.itens_crud_view import ItensCRUDView
from app.views.item_form_view import ItemFormView
from app.database.seeder import seed_database
from app.database import queries
from app.database.database import initialize_database
from app.styles.style import AppThemes

# Configuração de Logging.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("DoseCertaApp")


# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================
class DoseCertaApp:
    # ... (O método __init__ e outros métodos permanecem inalterados) ...
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        self.setup_page()
        self.setup_routes()
        initialize_database()
        auth_service.create_default_user()
        seed_database()
        self.page.go("/")

    def on_login_success(self, user: dict):
        self.current_user = user
        if queries.has_establishment(user["id"]):
            self.page.go("/dashboard")
        else:
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        self.page.go("/dashboard")

    def on_register_success(self):
        self.page.go("/")

    def logout(self):
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

    # ... (O método on_route_change permanece inalterado) ...
    def on_route_change(self, route):
        logger.info(f"ROUTER: Rota alterada para: {self.page.route}")
        current_view = self.page.views[-1] if self.page.views else None
        edit_match = re.match(r"/cadastros/item/editar/(\d+)", self.page.route)
        if self.page.route in ["/", "/register", "/dashboard", "/cadastros"]:
            self.page.views.clear()
        if self.page.route == "/":
            self.page.views.append(create_login_view(self.on_login_success))
        elif self.page.route == "/register":
            self.page.views.append(
                create_register_view(self.page, self.logout,
                                     self.on_register_success)
            )
        elif self.current_user:
            if self.page.route == "/onboarding":
                self.page.views.append(
                    create_onboarding_view(
                        self.current_user, self.on_onboarding_complete
                    )
                )
            elif self.page.route == "/dashboard":
                self.page.views.append(
                    create_dashboard_view(
                        self.current_user, self.page, self.logout)
                )
            elif self.page.route == "/cadastros":
                self.page.views.append(
                    create_cadastros_view(self.page, self.logout))
            elif self.page.route == "/cadastros/item":
                if not isinstance(current_view, ItemFormView):
                    self.page.views.clear()
                list_view = ItensCRUDView(self.page, self.logout)
                self.page.views.append(list_view)
                list_view.load_and_update_table()
            elif self.page.route == "/cadastros/item/novo":
                def on_save_callback(message):
                    if self.page.views:
                        list_view = self.page.views[0]
                        if isinstance(list_view, ItensCRUDView):
                            list_view.load_and_update_table(message)
                self.page.views.append(
                    ItemFormView(self.page, self.logout, on_save_callback)
                )
            elif edit_match:
                item_id = int(edit_match.group(1))
                def on_save_callback(message):
                    if self.page.views:
                        list_view = self.page.views[0]
                        if isinstance(list_view, ItensCRUDView):
                            list_view.load_and_update_table(message)
                self.page.views.append(
                    ItemFormView(
                        self.page, self.logout, on_save_callback, item_id=item_id
                    )
                )
            else:
                self.page.go("/dashboard")
        else:
            self.page.go("/")
        self.page.update()

    # --- MÉTODO on_view_pop REFATORADO ---
    def on_view_pop(self, e: ft.ViewPopEvent):
        """
        Manipula o clique no botão 'voltar' da AppBar com lógica de negócio customizada.
        """
        # Pega a rota da view que está sendo fechada (a view do topo da pilha).
        popped_view_route = e.view.route

        # Log de depuração: informa qual view está sendo fechada. Essencial para rastrear a navegação.
        logger.debug(f"on_view_pop: Usuário clicou em 'Voltar'. View a ser removida: '{popped_view_route}'")

        # REGRA 1: Impede que o usuário "volte" da tela principal, o Dashboard.
        if popped_view_route == "/dashboard":
            logger.debug("on_view_pop: Tentativa de voltar do Dashboard. Nenhuma ação será tomada.")
            return

        # REGRA 2 (NOVA): Se a rota da view que está fechando começar com "/cadastros",
        # a navegação será forçada para o Dashboard, ignorando a pilha de views.
        if popped_view_route and popped_view_route.startswith("/cadastros"):
            logger.info("on_view_pop: Rota de cadastro detectada. Navegando para o /dashboard.")
            self.page.go("/dashboard")
        else:
            # COMPORTAMENTO PADRÃO: Para qualquer outra rota, usa a navegação de pilha.
            logger.debug("on_view_pop: Rota não customizada. Usando navegação de pilha padrão.")
            # Remove a view atual da lista de views da página.
            self.page.views.pop()
            # Pega a view que agora está no topo da pilha.
            top_view = self.page.views[-1]
            # Navega para a rota da view que ficou no topo.
            self.page.go(top_view.route)



# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    DoseCertaApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")