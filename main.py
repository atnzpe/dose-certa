# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================
import flet as ft
import logging
import re  # Importa o módulo de expressões regulares
from app.services import auth_service
from app.views.login_view import create_login_view
from app.views.onboarding_view import create_onboarding_view
from app.views.register_view import create_register_view
from app.views.dashboard_view import create_dashboard_view
from app.views.cadastros_view import create_cadastros_view

# --- NOVAS IMPORTAÇÕES ---
from app.views.itens_crud_view import ItensCRUDView
from app.views.item_form_view import ItemFormView  # Nova view de formulário

# --- FIM DAS NOVAS IMPORTAÇÕES ---
from app.database.seeder import seed_database
from app.database import queries
from app.database.database import initialize_database
from app.styles.style import AppThemes

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("DoseCertaApp")


# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================
class DoseCertaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = None
        self.setup_page()
        self.setup_routes()
        initialize_database()
        auth_service.create_default_user()
        seed_database()
        self.page.go("/")

    # ... (outros métodos como on_login_success, etc. permanecem os mesmos) ...

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

    def on_route_change(self, route):
        """
        Manipulador de rotas refatorado para suportar as views de lista e formulário.
        """
        logger.info(f"ROUTER: Rota alterada para: {self.page.route}")

        # --- LÓGICA DE ROTEAMENTO REESTRUTURADA ---
        current_view = self.page.views[-1] if self.page.views else None

        # Padrão para a rota de edição (ex: /cadastros/item/editar/5)
        edit_match = re.match(r"/cadastros/item/editar/(\d+)", self.page.route)

        # Limpa as views APENAS se estivermos a navegar para uma rota "base"
        if self.page.route in ["/", "/register", "/dashboard", "/cadastros"]:
            self.page.views.clear()

        # Rotas públicas que não exigem login
        if self.page.route == "/":
            self.page.views.append(create_login_view(self.on_login_success))
        elif self.page.route == "/register":
            self.page.views.append(
                create_register_view(self.page, self.logout,
                                     self.on_register_success)
            )
        # Se não for rota pública, verifica se o usuário está logado
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

            # Rota para a LISTA de itens
            elif self.page.route == "/cadastros/item":
                # Só limpa se a view anterior não for um formulário de item
                if not isinstance(current_view, ItemFormView):
                    self.page.views.clear()
                list_view = ItensCRUDView(self.page, self.logout)
                self.page.views.append(list_view)
                list_view.load_and_update_table()

            # Rota para o formulário de NOVO item
            elif self.page.route == "/cadastros/item/novo":
                def on_save_callback(message):
                    if self.page.views:
                        list_view = self.page.views[0]
                        if isinstance(list_view, ItensCRUDView):
                            list_view.load_and_update_table(message)
                self.page.views.append(
                    ItemFormView(self.page, self.logout, on_save_callback)
                )

            # Rota para o formulário de EDIÇÃO de item
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

    def on_view_pop(self, e: ft.ViewPopEvent):
        """
        Manipula o clique no botão 'voltar' da AppBar.
        """
        self.page.views.pop()
        if self.page.views:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)


# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    DoseCertaApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")