# =================================================================================
# 1. IMPORTAÇÕES (PWA Version - Final)
# =================================================================================
# Módulo principal do Flet para construção da interface.
import flet as ft

# Módulo para medir o tempo de execução.
import time
import logging

# Módulo para logging de eventos.


# Módulo para interação com o sistema operacional.
import os

# Módulo para serialização e desserialização de JSON.
import json

# NOVO IMPORTE: A biblioteca 'flet-webview' é utilizada para renderizar conteúdo da web,
# como vídeos do YouTube, dentro da aplicação Flet.
# Ela substitui o 'flet-video' que lidava apenas com arquivos locais.
import flet_webview as fv

# Módulo para controle de rotas e importações dinâmicas.
import sys
import datetime  # Importado para obter o timestamp das tentativas de login.
import urllib.parse




# Obtém uma instância do logger.
logger = logging.getLogger(__name__)

# NOVO: Constante para o nome do arquivo de log de tentativas de login.
LOGIN_ATTEMPTS_FILE = "login_attempts.json"


# =================================================================================
# 3. CLASSE PRINCIPAL DA APLICAÇÃO (PWA Version)
# =================================================================================
class AppFBKMKLN:
    """
    Classe que encapsula toda a lógica e a interface da aplicação PWA.
    """

    def __init__(self, page: ft.Page):
        self.start_time = time.time()
        logger.debug("Initializing AppFBKMKLN class for PWA.")
        self.page = page
        
       

        self.user_data = None
        

        

        self.setup_page_and_routes()
        self.page.go("/")

        # Registra o tempo final e calcula a diferença.
        end_time = time.time()
        load_time = end_time - self.start_time
        logger.info(f"Tempo de inicialização da aplicação: {load_time:.2f} segundos.")

    def setup_page_and_routes(self):
        """Configura as propriedades visuais da página e os manipuladores de rotas."""
        logger.debug("Configuring PWA page properties and routes.")
        self.page.title = "App Dose Certa"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = ft.Colors.BLACK
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.on_view_pop

    def on_route_change(self, route):
        """Manipulador de mudança de rota. Renderiza a View correta."""
        logger.info(f"Navigating to PWA route: {self.page.route}")
        self.page.views.clear()
        user_data_json = self.page.client_storage.get("user_data")
        self.user_data = json.loads(user_data_json) if user_data_json else None

        # Estrutura de roteamento principal.
        if self.page.route == "/":
            self.page.views.append(self.create_login_view())
        elif self.page.route == "/dashboard" and self.user_data:
            self.page.views.append(self.create_dashboard_view(user=self.user_data))
        elif self.page.route == "/Cadastros" and self.user_data:
            self.page.views.append(self.create_cadastros_view(user=self.user_data))
        elif self.page.route == "/Incluir Itens" and self.user_data:
            self.page.views.append(self.create_incluir_itens_view(user=self.user_data))
        
        elif self.page.route == "/Contagem de Estoque" and self.user_data:
            self.page.views.append(self.create_contagem_estoque_view())
        elif self.page.route == "/Relatóriso" and self.user_data:
            self.page.views.append(self.create_relatorios_view())
        e
        else:
            self.page.views.append(self.create_login_view())

        self.page.update()

    def on_view_pop(self, view):
        """Manipula o evento de "voltar" da AppBar."""
        logger.debug("on_view_pop event triggered.")
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    # NOVO: Função para registrar a tentativa de login.
    def _log_login_attempt(self, username, status):
        """Registra a tentativa de login em um arquivo JSON."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "username": username,
            "status": status,
        }

        # Verifica se o arquivo existe e carrega os dados
        if os.path.exists(LOGIN_ATTEMPTS_FILE):
            with open(LOGIN_ATTEMPTS_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    # Se o arquivo estiver corrompido, inicia uma nova lista
                    data = []
        else:
            data = []

        # Adiciona a nova entrada e salva o arquivo
        data.append(entry)
        with open(LOGIN_ATTEMPTS_FILE, "w") as f:
            json.dump(data, f, indent=4)
            logger.info(f"Tentativa de login '{status}' para '{username}' registrada.")

    

        )

    def create_dashboard_view(self, user: dict) -> ft.View:
        """Constrói e retorna a View do dashboard, simplificada para PWA."""
        user_login_name = user.get("LOGIN", "User")
        logger.info(f"Displaying PWA dashboard for user: {user_login_name}")
        logo_header = ft.Image(
            src="/icon.jpg", width=80, height=80, border_radius=ft.border_radius.all(40)
        )
        welcome_message = ft.Text(
            f"Kidá (קִדָּה), {user_login_name}!", size=24, weight=ft.FontWeight.BOLD
        )
        header_content = ft.Column(
            [logo_header, welcome_message],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        btn_logout = ft.IconButton(
            icon=ft.Icons.LOGOUT, on_click=self.logout, tooltip="Sair"
        )
        header_row = ft.Row([ft.Container(expand=True), btn_logout])
        button_style = ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.WHITE24)

        btn_programa = ft.ElevatedButton(
            "Programa Técnico",
            icon=ft.Icons.DESCRIPTION,
            on_click=lambda _: self.page.go("/program"),
            height=50,
            style=button_style,
        )
        btn_videos = ft.ElevatedButton(
            "Vídeos de Movimentos",
            icon=ft.Icons.VIDEO_LIBRARY,
            on_click=lambda _: self.page.go("/videos"),
            height=50,
            style=button_style,
        )
        btn_local_treino = ft.ElevatedButton(
            "Onde Treinar",
            icon=ft.Icons.LOCATION_ON,
            on_click=lambda _: self.page.go("/training_location"),
            height=50,
            style=button_style,
        )
        btn_social = ft.ElevatedButton(
            "Mídias Sociais",
            icon=ft.Icons.GROUP,
            on_click=lambda _: self.page.go("/social_media"),
            height=50,
            style=button_style,
        )
        btn_cursos = ft.ElevatedButton(
            "Cursos",
            icon=ft.Icons.SCHOOL,
            on_click=lambda _: self.page.go("/courses"),
            height=50,
            style=button_style,
        )
        
        # NOVO: Lógica para o botão do WhatsApp
        # NOTA: SUBSTITUA O NÚMERO ABAIXO PELO NÚMERO DA FEDERAÇÃO
        phone_number = "5581997629232" # Exemplo: Código do país + DDD + Número
        # Mensagem pré-definida e codificada para o URL
        # Mensagem pré-definida e codificada para o URL
        whatsapp_message = "Kidá Mestre! Quero comprar equipamentos para me desenvolver. O que o senhor indica?"
        whatsapp_url = f"https://wa.me/{phone_number}?text={urllib.parse.quote(whatsapp_message)}"
        
        btn_ecommerce = ft.ElevatedButton(
            "E-commerce",
            icon=ft.Icons.SHOPPING_CART,
            on_click=lambda _: self.page.launch_url(whatsapp_url),
            height=50,
            style=button_style,
        )

        dashboard_buttons = ft.ResponsiveRow(
            [
                ft.Column([btn_programa], col={"xs": 12, "sm": 6, "md": 4}),
                ft.Column([btn_videos], col={"xs": 12, "sm": 6, "md": 4}),
                ft.Column([btn_local_treino], col={"xs": 12, "sm": 6, "md": 4}),
                ft.Column([btn_social], col={"xs": 12, "sm": 6, "md": 4}),
                ft.Column([btn_cursos], col={"xs": 12, "sm": 6, "md": 4}),
                # NOVO: Adiciona o botão de e-commerce ao layout.
                ft.Column([btn_ecommerce], col={"xs": 12, "sm": 6, "md": 4}),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            run_spacing=10,
            spacing=10,
        )

        return ft.View(
            "/dashboard",
            [
                # CORREÇÃO: Adicionamos a propriedade `scroll` ao Column principal
                # para que ele seja responsivo em telas menores.
                ft.Column(
                    [
                        header_row,
                        header_content,
                        ft.Divider(height=20, color=ft.Colors.WHITE24),
                        dashboard_buttons,
                    ],
                    spacing=25,
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            ],
            padding=20,
        )

    def create_program_view(self, user: dict) -> ft.View:
        """Constrói a View do programa técnico, simplificada para usar 'launch_url'."""
        logger.info(
            f"Creating PWA technical program view for user: {user.get('LOGIN')}"
        )
        accessible_ranks = self.auth_service.get_accessible_ranks(user)
        program_buttons = []
        try:
            all_programs = os.listdir(self.program_path)
            for rank in RANK_HIERARCHY:
                if rank in accessible_ranks:
                    pdf_file = f"{rank}.pdf"
                    if pdf_file in all_programs:
                        pdf_url = f"/programa_tecnico/{pdf_file}"
                        on_click_handler = lambda _, url=pdf_url: self.page.launch_url(
                            url
                        )

                        button = ft.ElevatedButton(
                            text=f"Programa - Faixa {rank}",
                            icon=ft.Icons.PICTURE_AS_PDF,
                            on_click=on_click_handler,
                            height=50,
                            tooltip="Abrir PDF em nova aba",
                        )
                        program_buttons.append(button)
                    else:
                        logger.warning(
                            f"PDF file '{pdf_file}' for rank '{rank}' not found."
                        )
        except Exception as e:
            logger.error(f"Error listing technical program PDFs: {e}", exc_info=True)
            program_buttons.append(
                ft.Text("Não foi possível carregar os programas.", color=ft.Colors.RED)
            )

        return ft.View(
            "/program",
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.page.go("/dashboard"),
                            tooltip="Voltar",
                        ),
                        ft.Text("Programa Técnico", size=24, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                ft.Column(
                    program_buttons,
                    spacing=15,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            padding=20,
        )

    def create_videos_view(self, user: dict) -> ft.View:
        """Constrói a View de seleção de modo de treino (vídeos)."""
        logger.info(f"Creating training selection view for: {user.get('LOGIN')}")
        accessible_ranks = self.auth_service.get_accessible_ranks(user)
        user_next_rank = user.get("PROXIMA_GRADUACAO")
        layout_controls = []

        # Estilo dos botões para manter a consistência com o Dashboard.
        button_style = ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.WHITE24)

        try:
            # A checagem do arquivo `playlist.json` é mantida para garantir que a playlist existe.
            for rank in RANK_HIERARCHY:
                if rank in accessible_ranks:
                    if os.path.exists(
                        os.path.join(self.videos_path, rank, "playlist.json")
                    ):
                        layout_controls.append(
                            ft.Text(f"Faixa {rank}", size=20, weight=ft.FontWeight.BOLD)
                        )

                        def create_train_handler(r):
                            def handler(e):
                                logger.debug(f"Botão 'Treinar Faixa {r}' clicado.")
                                self.start_training(playlist_type="rank", rank=r)

                            return handler

                        train_button = ft.ElevatedButton(
                            text=f"Treinar Faixa {rank}",
                            icon=ft.Icons.PLAYLIST_PLAY,
                            on_click=create_train_handler(rank),
                            height=50,
                            style=button_style,  # APLICAÇÃO DO ESTILO DO DASHBOARD
                        )
                        current_rank_index = RANK_HIERARCHY.index(rank)
                        if current_rank_index + 1 < len(RANK_HIERARCHY):
                            next_rank_in_hierarchy = RANK_HIERARCHY[
                                current_rank_index + 1
                            ]
                            if next_rank_in_hierarchy == user_next_rank:

                                def create_exam_handler(r):
                                    def handler(e):
                                        logger.debug(
                                            f"Botão 'Simular Exame para {r}' clicado."
                                        )
                                        self.start_training(
                                            playlist_type="exam", rank=r
                                        )

                                    return handler

                                exam_button = ft.ElevatedButton(
                                    text=f"Simular Exame para {next_rank_in_hierarchy}",
                                    icon=ft.Icons.VIDEO_CAMERA_FRONT,
                                    on_click=create_exam_handler(
                                        next_rank_in_hierarchy
                                    ),
                                    height=50,
                                    style=button_style,  # APLICAÇÃO DO ESTILO DO DASHBOARD
                                )
                                # CORREÇÃO: Usamos um Column para alinhar os botões verticalmente.
                                layout_controls.append(
                                    ft.Column(
                                        [train_button, exam_button],
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                )
                            else:
                                layout_controls.append(train_button)
                        else:
                            layout_controls.append(train_button)
                        layout_controls.append(ft.Divider(height=20))
        except Exception as e:
            logger.error(f"Error creating videos view: {e}", exc_info=True)
            layout_controls.append(
                ft.Text("Could not load training options.", color=ft.Colors.RED)
            )
        return ft.View(
            "/videos",
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.page.go("/dashboard"),
                            tooltip="Voltar",
                        ),
                        ft.Text("Modos de Treino", size=24, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                ft.Column(
                    layout_controls,
                    spacing=15,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                ),
            ],
            padding=20,
        )

    

    def create_social_media_view(self) -> ft.View:
        """Constrói a View de Mídias Sociais."""
        logger.info("Creating Social Media view.")
        YOUTUBE_URL = "https://www.youtube.com/@KMLNDEFENSE"
        INSTAGRAM_URL = "https://www.instagram.com/fbkmklnoficial/"
        youtube_button = ft.ElevatedButton(
            "Acessar Canal no YouTube",
            icon=ft.Icons.SMART_DISPLAY_OUTLINED,
            on_click=lambda _: self.page.launch_url(YOUTUBE_URL),
            height=50,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.WHITE24),
        )
        instagram_button = ft.ElevatedButton(
            "Seguir no Instagram",
            icon=ft.Icons.CAMERA_ALT_OUTLINED,
            on_click=lambda _: self.page.launch_url(INSTAGRAM_URL),
            height=50,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.WHITE24),
        )
        return ft.View(
            "/social_media",
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.page.go("/dashboard"),
                            tooltip="Voltar",
                        ),
                        ft.Text("Mídias Sociais", size=24, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                ft.Column(
                    [
                        ft.Text(
                            "Siga a Federação Leão do Norte nas redes sociais para ficar por dentro das novidades, eventos e dicas de treino.",
                            text_align=ft.TextAlign.CENTER,
                            size=16,
                            color=ft.Colors.WHITE70,
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        youtube_button,
                        instagram_button,
                    ],
                    spacing=20,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            padding=20,
        )

    def create_courses_view(self) -> ft.View:
        """Constrói a View 'Cursos'."""
        logger.info("Creating 'Courses' view.")
        all_courses = self.course_service.get_courses()
        open_courses = [c for c in all_courses if c.get("Status") == "Abertas"]
        closed_courses = [c for c in all_courses if c.get("Status") == "Encerradas"]
        main_column = ft.Column(spacing=20, scroll=ft.ScrollMode.ADAPTIVE, expand=True)

        def create_course_card(course: dict):
            card_content = []
            image_url = course.get("Imagem")
            if image_url:
                card_content.append(
                    ft.Image(
                        src=image_url,
                        height=150,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(10),
                    )
                )
            card_content.extend(
                [
                    ft.Text(
                        course.get("Nome do Curso", "N/A"),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(course.get("Descrição", "")),
                ]
            )
            if course.get("Status") == "Abertas":
                course_date = course.get("Data")
                date_text = (
                    ft.Text(f"Data: {course_date}", weight=ft.FontWeight.BOLD)
                    if course_date
                    else ft.Text(
                        "Data: Em Breve",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.AMBER,
                    )
                )
                card_content.append(date_text)
                card_content.append(
                    ft.Text(f"Vagas: {course.get('Número de Vagas', 'N/A')}")
                )
                card_content.extend(
                    [
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Inscreva-se",
                            icon=ft.Icons.EDIT_DOCUMENT,
                            on_click=lambda _, url=course.get(
                                "Link da Inscrição"
                            ): self.page.launch_url(url),
                            disabled=not course.get("Link da Inscrição"),
                        ),
                    ]
                )
            else:
                if image_url and card_content:
                    card_content[0].opacity = 0.5
                card_content.extend(
                    [
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Text(
                            "VAGAS ENCERRADAS",
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                    ]
                )
            return ft.Card(
                content=ft.Container(
                    padding=15, content=ft.Column(card_content, spacing=10)
                )
            )

        if open_courses:
            main_column.controls.append(
                ft.Text("Inscrições Abertas", size=22, weight=ft.FontWeight.BOLD)
            )
            for course in open_courses:
                main_column.controls.append(create_course_card(course))
        if closed_courses:
            main_column.controls.append(ft.Divider(height=30, color=ft.Colors.WHITE24))
            main_column.controls.append(
                ft.Text("Cursos Anteriores", size=22, weight=ft.FontWeight.BOLD)
            )
            for course in closed_courses:
                main_column.controls.append(create_course_card(course))
        if not open_courses and not closed_courses:
            main_column.controls.append(
                ft.Text(
                    "Nenhum curso disponível no momento.",
                    text_align=ft.TextAlign.CENTER,
                    size=16,
                )
            )

        return ft.View(
            "/courses",
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.page.go("/dashboard"),
                            tooltip="Voltar",
                        ),
                        ft.Text("Cursos e Eventos", size=24, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                main_column,
            ],
            padding=20,
        )


# =================================================================================
# 4. PONTO DE ENTRADA DA APLICAÇÃO (PWA Version)
# =================================================================================
def main(page: ft.Page):
    """
    Função de entrada principal que o Flet chama para iniciar a aplicação PWA.
    """
    logger.info("Starting the AppFBKMKLN PWA version.")
    AppFBKMKLN(page)


if __name__ == "__main__":
    logger.info("Executing the Flet app via __main__ for PWA deployment.")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8000)
