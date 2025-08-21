# =================================================================================
# 1. IMPORTAÇÕES
# =================================================================================

# Módulo principal do Flet para construção da interface.
import flet as ft
import logging

# Configuração inicial do logging para depuração.
logging.basicConfig(level=logging.INFO)
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
        self.setup_page()  # Configura as propriedades iniciais da página.
        self.setup_routes()  # Configura o sistema de roteamento das views.

        logger.info("Navegando para a rota inicial ('/').")
        self.page.go("/")  # Navega para a rota inicial ao iniciar o app.

    def setup_page(self):
        """
        Configura as propriedades visuais globais da página (título, tema, etc.).
        """
        logger.info("Configurando propriedades da página.")
        self.page.title = "App Dose Certa"
        self.page.theme_mode = ft.ThemeMode.DARK  # Tema escuro como padrão[cite: 79].
        self.page.window_width = 400
        self.page.window_height = 600
        self.page.window_resizable = False

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
        self.page.views.clear()  # Limpa a pilha de views.

        # Lógica de roteamento principal.
        if self.page.route == "/":
            # Quando a rota for a raiz, exibe a tela de login.
            # TODO: Implementar a create_login_view.
            logger.info("Renderizando a view de Login.")
            self.page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT
                        ),
                        ft.Text("Página de Login em construção...", size=20),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif self.page.route == "/dashboard":
            # TODO: Implementar a create_dashboard_view.
            logger.info("Renderizando a view do Dashboard.")
            self.page.views.append(
                ft.View(
                    route="/dashboard",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Dashboard"),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        ft.Text("Dashboard em construção...", size=20),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        self.page.update()  # Atualiza a página para exibir a nova view.

    def on_view_pop(self, view: ft.View):
        """
        Manipula o evento de "voltar" (ex: botão 'voltar' da AppBar).
        """
        logger.info(f"Retornando da view: {view.route}")
        self.page.views.pop()  # Remove a view atual da pilha.
        top_view = self.page.views[-1]  # Pega a view anterior.
        logger.info(f"Navegando de volta para: {top_view.route}")
        self.page.go(top_view.route)  # Navega para a view anterior.


# =================================================================================
# 3. PONTO DE ENTRADA DA APLICAÇÃO
# =================================================================================
def main(page: ft.Page):
    """
    Função de entrada principal que o Flet chama para iniciar a aplicação.
    """
    logger.info("Aplicação Dose Certa iniciada.")
    DoseCertaApp(page)  # Instancia a classe principal da aplicação.


# Verifica se o script está sendo executado diretamente.
if __name__ == "__main__":
    logger.info("Executando o app Flet via __main__.")
    # Inicia a aplicação Flet, definindo a função 'main' como alvo.
    ft.app(target=main, assets_dir="../assets")
