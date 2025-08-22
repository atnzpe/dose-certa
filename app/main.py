# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

# Módulo principal do Flet para construção da interface.
import flet as ft
import logging

# Importa a função para inicializar o banco de dados do nosso módulo de database.
from app.database.database import initialize_database

# Importa a função que cria a nossa nova view de login.
from app.views.login_view import create_login_view

# Configuração inicial do logging para depuração.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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

        :param page: A página Flet principal fornecida pela execução do `ft.app`.
        """
        logger.info("Iniciando a classe DoseCertaApp.")
        self.page = page
        self.setup_page()
        self.setup_routes()
        
        # --- NOVO: INICIALIZAÇÃO DO BANCO DE DADOS ---
        # Chama a função para criar as tabelas do banco de dados na inicialização do app.
        initialize_database()
        
        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")

    def setup_page(self):
        """
        Configura as propriedades visuais globais da página (título, tema, etc.).
        """
        logger.info("Configurando propriedades da página.")
        self.page.title = "App Dose Certa"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 400
        self.page.window_height = 700 # Aumentado para melhor visualização
        self.page.window_resizable = False
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def setup_routes(self):
        """
        Define os manipuladores de rotas e de pop de view.
        """
        logger.info("Configurando as rotas da aplicação.")
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        """
        Manipulador que é chamado sempre que a rota da página muda.
        Ele limpa as views existentes e adiciona a view correspondente à nova rota.
        """
        logger.info(f"Rota alterada para: {self.page.route}")
        self.page.views.clear()

        # Lógica de roteamento principal.
        if self.page.route == "/":
            # --- ATUALIZADO: Usa a função importada para criar a view ---
            logger.info("Renderizando a view de Login.")
            self.page.views.append(create_login_view(self.page))
            
        elif self.page.route == "/dashboard":
            # TODO: Implementar a create_dashboard_view.
            logger.info("Renderizando a view do Dashboard.")
            self.page.views.append(
                ft.View(
                    route="/dashboard",
                    controls=[
                        ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Dashboard em construção...", size=20)
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        
        self.page.update()

    def on_view_pop(self, view: ft.View):
        """
        Manipula o evento de "voltar" (ex: botão 'voltar' da AppBar).
        """
        logger.info(f"Retornando da view: {view.route}")
        self.page.views.pop()
        top_view = self.page.views[-1]
        logger.info(f"Navegando de volta para: {top_view.route}")
        self.page.go(top_view.route)


# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    """
    Função de entrada principal que o Flet chama para iniciar a aplicação.
    """
    logger.info("Aplicação Dose Certa iniciada.")
    DoseCertaApp(page)

# Verifica se o script está sendo executado diretamente.
if __name__ == "__main__":
    logger.info("Executando o app Flet via __main__.")
    # O assets_dir agora aponta para o diretório correto na raiz do projeto.
    ft.app(target=main, assets_dir="assets")