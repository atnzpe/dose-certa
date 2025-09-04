# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

import flet as ft
import logging

# Módulos de serviços e views da aplicação
from app.services import auth_service
from app.views.login_view import create_login_view
from app.views.onboarding_view import create_onboarding_view
from app.views.register_view import create_register_view
from app.views.dashboard_view import create_dashboard_view
from app.views.cadastros_view import create_cadastros_view

# Módulos de banco de dados
from app.database.seeder import seed_database
from app.database import queries
from app.database.database import initialize_database

# --- NOVO: Importa os temas do módulo de estilos ---
from app.styles.style import AppThemes

# Configuração do logger
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
        
        # Sequência de inicialização correta
        initialize_database()
        auth_service.create_default_user() 
        seed_database()
        
        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")

    def on_login_success(self, user: dict):
        """Callback chamado após um login bem-sucedido."""
        self.current_user = user
        if queries.has_establishment(user['id']):
            logger.info(f"Usuário ID {user['id']} já completou o onboarding. Navegando para /dashboard.")
            self.page.go("/dashboard")
        else:
            logger.info(f"Usuário ID {user['id']} precisa completar o onboarding. Navegando para /onboarding.")
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        """Callback chamado após a conclusão do onboarding."""
        logger.info("Onboarding concluído. Navegando para o dashboard.")
        self.page.go("/dashboard")

    def on_register_success(self):
        """Callback chamado após um cadastro bem-sucedido."""
        logger.info("Cadastro bem-sucedido. Redirecionando para a tela de login.")
        self.page.go("/")

    def logout(self):
        """Limpa a sessão do usuário e retorna para a tela de login."""
        logger.info(f"Usuário {self.current_user['email']} deslogado.")
        self.current_user = None
        self.page.go("/")

    def setup_page(self):
        """Configura as propriedades iniciais da janela e os temas da aplicação."""
        self.page.title = "App Dose Certa"
        
        # --- ATUALIZADO: Aplica os temas a partir do módulo de estilos ---
        self.page.theme = AppThemes.light_theme
        self.page.dark_theme = AppThemes.dark_theme
        
        # A aplicação começa no modo escuro por padrão
        self.page.theme_mode = ft.ThemeMode.DARK
        
        # Configurações da janela
        self.page.window_width = 400
        self.page.window_height = 700
        self.page.window_resizable = False
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Padding é gerenciado pelas views individuais para maior controle
        self.page.padding = 0


    def setup_routes(self):
        """Configura os manipuladores de rotas."""
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        """Manipulador central de rotas da aplicação."""
        logger.info(f"Rota alterada para: {self.page.route}")
        self.page.views.clear()

        public_routes = ["/", "/register"]
        
        # Lógica para rotas públicas
        if self.page.route in public_routes:
            if self.page.route == "/":
                self.page.views.append(create_login_view(self.on_login_success))
            elif self.page.route == "/register":
                self.page.views.append(create_register_view(self.on_register_success))
        
        # Lógica para rotas protegidas (exigem login)
        elif self.current_user:
            if self.page.route == "/onboarding":
                self.page.views.append(create_onboarding_view(self.current_user, self.on_onboarding_complete))
            elif self.page.route == "/dashboard":
                self.page.views.append(create_dashboard_view(self.current_user, self.page, self.logout))
            elif self.page.route == "/cadastros":
                self.page.views.append(create_cadastros_view())
            else:
                logger.warning(f"Rota desconhecida '{self.page.route}' para usuário logado. Redirecionando para o dashboard.")
                self.page.go("/dashboard")
        
        # Se o usuário não está logado e tenta acessar uma rota protegida
        else:
            logger.warning("Acesso não autorizado a uma rota protegida. Redirecionando para o login.")
            self.page.go("/")
        
        self.page.update()

    def on_view_pop(self, e: ft.ViewPopEvent):
        """Manipula o evento de 'voltar' (clique na seta da AppBar)."""
        if e.view.route == "/dashboard":
            logger.info("Botão 'voltar' pressionado no Dashboard. Nenhuma ação tomada.")
            return
        
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    """Função principal que o Flet chama para iniciar a aplicação."""
    DoseCertaApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
