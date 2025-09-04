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

# --- MODO DE DEPURAÇÃO: Nível de log alterado para DEBUG e formato melhorado ---
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Logger específico para a classe principal da aplicação.
logger = logging.getLogger("DoseCertaApp")

# =================================================================================
# 2. CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================
class DoseCertaApp:
    def __init__(self, page: ft.Page):
        logger.debug("DoseCertaApp: __init__ - Iniciando a classe principal.")
        self.page = page
        self.current_user = None
        self.setup_page()
        self.setup_routes()
        
        logger.debug("DoseCertaApp: __init__ - Executando sequência de inicialização do banco de dados.")
        initialize_database()
        auth_service.create_default_user() 
        seed_database()
        
        logger.info("DoseCertaApp: __init__ - Navegando para a rota inicial ('/').")
        self.page.go("/")

    def on_login_success(self, user: dict):
        logger.info(f"DoseCertaApp: on_login_success - Login bem-sucedido para {user.get('email')}")
        self.current_user = user
        if queries.has_establishment(user['id']):
            logger.debug(f"DoseCertaApp: on_login_success - Usuário já possui estabelecimento. Navegando para /dashboard.")
            self.page.go("/dashboard")
        else:
            logger.debug(f"DoseCertaApp: on_login_success - Usuário precisa de onboarding. Navegando para /onboarding.")
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        logger.info("DoseCertaApp: on_onboarding_complete - Onboarding concluído. Navegando para /dashboard.")
        self.page.go("/dashboard")

    def on_register_success(self):
        logger.info("DoseCertaApp: on_register_success - Registro bem-sucedido. Navegando para /.")
        self.page.go("/")

    def logout(self):
        if self.current_user:
            logger.info(f"DoseCertaApp: logout - Usuário {self.current_user.get('email', '')} deslogado.")
        self.current_user = None
        self.page.go("/")

    def setup_page(self):
        logger.debug("DoseCertaApp: setup_page - Configurando propriedades da página.")
        self.page.title = "App Dose Certa"
        self.page.theme = AppThemes.light_theme
        self.page.dark_theme = AppThemes.dark_theme
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 400
        self.page.window_height = 700
        self.page.window_resizable = False
        self.page.padding = 0

    def setup_routes(self):
        logger.debug("DoseCertaApp: setup_routes - Configurando manipuladores de rota.")
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        logger.info(f"ROUTER: Rota alterada para: {self.page.route}")
        logger.debug("ROUTER: Limpando views existentes.")
        self.page.views.clear()

        public_routes = ["/", "/register"]
        
        logger.debug(f"ROUTER: Verificando se a rota '{self.page.route}' é pública.")
        if self.page.route in public_routes:
            logger.info("ROUTER: Rota é pública.")
            if self.page.route == "/":
                logger.debug("ROUTER: Renderizando a view de LOGIN.")
                self.page.views.append(create_login_view(self.on_login_success))
            elif self.page.route == "/register":
                logger.debug("ROUTER: Renderizando a view de REGISTRO.")
                self.page.views.append(
                    create_register_view(
                        page=self.page, 
                        on_logout=self.logout, 
                        on_register_success=self.on_register_success
                    )
                )
        
        elif self.current_user:
            logger.info("ROUTER: Rota é protegida e o usuário está logado.")
            if self.page.route == "/onboarding":
                logger.debug("ROUTER: Renderizando a view de ONBOARDING.")
                self.page.views.append(create_onboarding_view(self.current_user, self.on_onboarding_complete))
            elif self.page.route == "/dashboard":
                logger.debug("ROUTER: Renderizando a view de DASHBOARD.")
                self.page.views.append(create_dashboard_view(self.current_user, self.page, self.logout))
            elif self.page.route == "/cadastros":
                logger.debug("ROUTER: Renderizando a view de CADASTROS.")
                self.page.views.append(create_cadastros_view(self.page, self.logout))
            
            # --- PONTO DE DEPURAÇÃO CRÍTICO ---
            elif self.page.route == "/cadastros/item":
                logger.debug("ROUTER: Entrou no bloco da rota /cadastros/item.")
                
                logger.debug("ROUTER: Passo 1 - Criando a instância da ItensCRUDView.")
                itens_view = ItensCRUDView(self.page, self.logout)
                
                logger.debug("ROUTER: Passo 2 - Adicionando a view à página.")
                self.page.views.append(itens_view)

                logger.info("ROUTER: Passo 3 - CHAMANDO itens_view.load_all_data(). ESTE É O PONTO CRÍTICO.")
                itens_view.load_all_data()
                logger.info("ROUTER: Chamada para itens_view.load_all_data() CONCLUÍDA.")

            else:
                logger.warning(f"ROUTER: Rota protegida desconhecida '{self.page.route}'. Redirecionando para /dashboard.")
                self.page.go("/dashboard")
        else:
            logger.warning("ROUTER: Usuário não logado tentando acessar rota protegida. Redirecionando para /.")
            self.page.go("/")
        
        logger.debug("ROUTER: Chamando page.update() no final do manipulador de rotas.")
        self.page.update()

    def on_view_pop(self, e: ft.ViewPopEvent):
        logger.debug(f"DoseCertaApp: on_view_pop - Evento 'voltar' na rota {e.view.route}.")
        if e.view.route == "/dashboard":
            logger.debug("DoseCertaApp: on_view_pop - Nenhuma ação tomada no dashboard.")
            return
        
        self.page.views.pop()
        top_view = self.page.views[-1]
        logger.debug(f"DoseCertaApp: on_view_pop - Navegando de volta para {top_view.route}.")
        self.page.go(top_view.route)

# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    DoseCertaApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
