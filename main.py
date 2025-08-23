# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

import flet as ft
import logging

# --- CORREÇÃO: Importações ajustadas para a nova estrutura de arquivos ---
from app.services import auth_service
from app.views.login_view import create_login_view
from app.views.onboarding_view import create_onboarding_view
from app.database.seeder import seed_database
from app.database import queries
# --- CORREÇÃO: Importa a função para criar as tabelas ---
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
        
        # --- CORREÇÃO CRÍTICA: Ordem de inicialização corrigida ---
        # 1. Cria as tabelas do banco de dados.
        initialize_database()
        # 2. Cria o usuário padrão (agora as tabelas já existem).
        auth_service.create_default_user()
        # 3. Popula o banco com os itens iniciais.
        seed_database()
        
        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")

    def on_login_success(self, user: dict):
        self.current_user = user
        if queries.has_establishment(user['id']):
            logger.info(f"Usuário ID {user['id']} já completou o onboarding. Navegando para o dashboard.")
            self.page.go("/dashboard")
        else:
            logger.info(f"Usuário ID {user['id']} precisa completar o onboarding. Navegando para /onboarding.")
            self.page.go("/onboarding")

    def on_onboarding_complete(self):
        logger.info("Onboarding concluído. Navegando para o dashboard.")
        self.page.go("/dashboard")

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
            # --- CORREÇÃO: Passa o callback como argumento posicional ---
            self.page.views.append(create_login_view(self.on_login_success))
        
        elif self.page.route == "/onboarding" and self.current_user:
            self.page.views.append(
                create_onboarding_view(
                    user=self.current_user,
                    on_complete=self.on_onboarding_complete
                )
            )
            
        elif self.page.route == "/dashboard" and self.current_user:
            user_name = self.current_user.get('nome', 'Usuário')
            self.page.views.append(
                ft.View(
                    route="/dashboard",
                    controls=[
                        ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.Colors.BLUE_GREY_800),
                        ft.Text(f"Bem-vindo, {user_name}!", size=20)
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        else:
            logger.warning("Acesso não autorizado ou rota inválida. Redirecionando para o login.")
            self.page.views.append(create_login_view(self.on_login_success))
        
        self.page.update()

    def on_view_pop(self, view: ft.View):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    DoseCertaApp(page)

if __name__ == "__main__":
    # O assets_dir agora aponta para a pasta 'assets' na raiz do projeto.
    ft.app(target=main, assets_dir="assets")