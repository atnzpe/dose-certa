# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py)
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.styles.style import AppFonts, AppDimensions, main_button_style

logger = logging.getLogger(__name__)

class ItensCRUDView(ft.View):
    """
    Uma classe que herda de ft.View para criar a tela de gerenciamento de itens.
    Gerencia seu próprio estado e componentes internos.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/cadastros/item"
        self.appbar = ft.AppBar(title=ft.Text("Cadastro de Itens"), center_title=True)
        
        self.items_data = []
        self.categories_data = []
        self.units_data = []

        # Define o DataTable como um atributo da classe
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Unidade")),
                ft.DataColumn(ft.Text("Ações"), numeric=True),
            ],
            rows=[],
            expand=True,
        )

        self.controls = [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Adicionar Novo Item",
                        icon=ft.Icons.ADD,
                        on_click=self.open_add_dialog,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row([self.data_table], expand=True),
        ]
        
        # Carrega os dados iniciais quando a view é criada
        self.load_data()

    def load_data(self):
        """Carrega os dados do banco e atualiza a tabela."""
        self.items_data = queries.get_all_items_with_details()
        self.update_table()

    def update_table(self):
        """Limpa e recarrega as linhas da tabela com os dados mais recentes."""
        self.data_table.rows.clear()
        for item in self.items_data:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'])),
                        ft.DataCell(ft.Text(item['unidade'])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, item_id=item['id']: self.open_edit_dialog(item_id)),
                                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id)),
                                ]
                            )
                        ),
                    ]
                )
            )
        # Atualiza a página se ela existir
        if self.page:
            self.page.update()

    def open_add_dialog(self, e):
        # Implementação futura do diálogo de adição
        pass

    def open_edit_dialog(self, item_id):
        # Implementação futura do diálogo de edição
        pass
    
    def open_delete_dialog(self, item_id):
        # Implementação futura do diálogo de exclusão
        pass

# Função de fábrica para criar a view, mantendo o padrão
def create_itens_crud_view(page: ft.Page) -> ItensCRUDView:
    return ItensCRUDView(page)