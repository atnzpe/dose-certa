# =================================================================================
# MÓDULO DA VIEW DE FORMULÁRIO DE ITENS (item_form_view.py) - NOVO ARQUIVO
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.components.app_bar import create_app_bar

logger = logging.getLogger("ItemFormView")

class ItemFormView(ft.View):
    """
    View dedicada para o formulário de criação e edição de itens.
    """
    def __init__(self, page: ft.Page, on_logout, on_save_callback, item_id: int = None):
        super().__init__()
        # ==================================================
        # 1. INICIALIZAÇÃO DE ATRIBUTOS
        # ==================================================
        self.page = page
        self.on_logout = on_logout
        self.on_save_callback = on_save_callback
        self.item_id = item_id
        self.is_editing = item_id is not None
        
        self.item_data = None
        self.categories_data = []
        self.units_data = []

        # ==================================================
        # 2. CONFIGURAÇÃO DA VIEW E AppBar
        # ==================================================
        self.route = f"/cadastros/item/editar/{self.item_id}" if self.is_editing else "/cadastros/item/novo"
        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Editar Item" if self.is_editing else "Adicionar Item")
        
        # ==================================================
        # 3. CRIAÇÃO DOS CONTROLES DE FORMULÁRIO
        # ==================================================
        self.nome_field = ft.TextField(label="Nome do Item")
        self.categoria_dropdown = ft.Dropdown(label="Categoria")
        self.unidade_dropdown = ft.Dropdown(label="Unidade de Medida")
        
        self.controls = [
            ft.Column(
                [
                    self.nome_field,
                    self.categoria_dropdown,
                    self.unidade_dropdown,
                    ft.ElevatedButton(
                        "Salvar",
                        icon=ft.Icons.SAVE,
                        on_click=self.save_item
                    )
                ],
                spacing=20,
                # Centraliza o formulário na tela
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
        
        # Carrega os dados necessários para o formulário
        self.load_form_data()

    def show_snackbar(self, message: str, color: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color, duration=3000)
        self.page.snack_bar.open = True
        self.page.update()

    def load_form_data(self):
        """Carrega categorias, unidades e os dados do item (se estiver a editar)."""
        try:
            self.categories_data = queries.get_all_categories()
            self.units_data = queries.get_all_units()

            self.categoria_dropdown.options = [ft.dropdown.Option(cat['id'], cat['nome']) for cat in self.categories_data]
            self.unidade_dropdown.options = [ft.dropdown.Option(unit['id'], unit['nome']) for unit in self.units_data]

            if self.is_editing:
                self.item_data = queries.get_item_by_id(self.item_id)
                if self.item_data:
                    self.nome_field.value = self.item_data['nome']
                    self.categoria_dropdown.value = self.item_data['id_categoria']
                    self.unidade_dropdown.value = self.item_data['id_unidade_medida']
            
            self.page.update()
        except Exception as e:
            logger.error(f"Erro ao carregar dados do formulário: {e}", exc_info=True)
            self.show_snackbar("Erro ao carregar dados para o formulário.", ft.Colors.RED)

    def save_item(self, e):
        """Valida e salva os dados do formulário no banco de dados."""
        logger.info("AÇÃO DO USUÁRIO: Clicou em 'Salvar' no formulário.")
        try:
            if not self.nome_field.value or not self.categoria_dropdown.value or not self.unidade_dropdown.value:
                self.show_snackbar("Todos os campos são obrigatórios.", ft.Colors.AMBER)
                return

            if self.is_editing:
                queries.update_item(
                    item_id=self.item_id,
                    nome=self.nome_field.value,
                    id_categoria=int(self.categoria_dropdown.value),
                    id_unidade_medida=int(self.unidade_dropdown.value)
                )
                message = "Item atualizado com sucesso!"
            else:
                queries.add_item(
                    nome=self.nome_field.value,
                    id_categoria=int(self.categoria_dropdown.value),
                    id_unidade_medida=int(self.unidade_dropdown.value)
                )
                message = "Item adicionado com sucesso!"

            # Chama o callback para notificar a view de lista que ela precisa de ser atualizada
            if self.on_save_callback:
                self.on_save_callback(message)
            
            # Navega de volta para a tela de lista
            self.page.go("/cadastros/item")

        except Exception as ex:
            logger.error(f"Erro ao salvar item: {ex}", exc_info=True)
            self.show_snackbar("Erro ao salvar o item.", ft.Colors.RED)