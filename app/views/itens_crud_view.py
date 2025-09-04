# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py)
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.styles.style import AppDimensions
# --- NOVO: Importa a AppBar reutilizável ---
from app.components.app_bar import create_app_bar

logger = logging.getLogger(__name__)

class ItensCRUDView(ft.View):
    """
    Uma classe que herda de ft.View para criar e gerenciar a tela de CRUD de itens.
    """
    def __init__(self, page: ft.Page, on_logout):
        super().__init__()
        self.page = page
        self.route = "/cadastros/item"
        
        # --- ATUALIZADO: Usa o componente de AppBar ---
        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Cadastro de Itens")
        
        # Atributos para armazenar os dados e o diálogo
        self.items_data = []
        self.categories_data = []
        self.units_data = []
        self.dialog = None

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
            # --- CORRIGIDO: O padding é aplicado a um Container que envolve a Row ---
            ft.Container(
                content=ft.Row(
                    [
                        ft.ElevatedButton(
                            "Adicionar Novo Item",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.open_dialog(),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.symmetric(horizontal=10)
            ),
            ft.ListView([self.data_table], expand=True),
        ]
        
        # REMOVA ESTA LINHA DO __init__
        # self.load_all_data()

    def load_all_data(self):
        """Carrega todos os dados necessários do banco e atualiza a tabela."""
        self.items_data = queries.get_all_items_with_details()
        self.categories_data = queries.get_all_categories()
        self.units_data = queries.get_all_units()
        self.update_table()

    def update_table(self):
        """Limpa e recarrega as linhas da tabela."""
        self.data_table.rows.clear()
        for item in self.items_data:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'])),
                        ft.DataCell(ft.Text(item['unidade'])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=item: self.open_dialog(i)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id)),
                            ])
                        ),
                    ]
                )
            )
        self.update()

    def open_dialog(self, item_to_edit=None):
        """Abre um diálogo para adicionar ou editar um item."""
        is_editing = item_to_edit is not None

        # --- CAMPOS DO FORMULÁRIO ---
        nome_field = ft.TextField(label="Nome do Item", value=item_to_edit['nome'] if is_editing else "")
        
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(cat['id'], cat['nome']) for cat in self.categories_data],
            value=item_to_edit['id_categoria'] if is_editing else None
        )
        
        unidade_dropdown = ft.Dropdown(
            label="Unidade de Medida",
            options=[ft.dropdown.Option(unit['id'], unit['nome']) for unit in self.units_data],
            value=item_to_edit['id_unidade_medida'] if is_editing else None
        )

        def save(e):
            if is_editing:
                queries.update_item(
                    item_id=item_to_edit['id'],
                    nome=nome_field.value,
                    id_categoria=categoria_dropdown.value,
                    id_unidade_medida=unidade_dropdown.value
                )
            else:
                queries.add_item(
                    nome=nome_field.value,
                    id_categoria=categoria_dropdown.value,
                    id_unidade_medida=unidade_dropdown.value
                )
            self.dialog.open = False
            self.load_all_data() # Recarrega os dados e atualiza a tabela
            self.page.update()

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Item" if is_editing else "Adicionar Novo Item"),
            content=ft.Column([nome_field, categoria_dropdown, unidade_dropdown]),
            actions=[
                ft.TextButton("Salvar", on_click=save),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def open_delete_dialog(self, item_id):
        """Abre um diálogo de confirmação para exclusão."""
        def delete(e):
            queries.delete_item(item_id)
            self.dialog.open = False
            self.load_all_data()
            self.page.update()

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir este item?"),
            actions=[
                ft.TextButton("Sim, Excluir", on_click=delete),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
        
    def close_dialog(self):
        """Fecha o diálogo atualmente aberto."""
        if self.dialog:
            self.dialog.open = False
            self.page.update()

# Função de fábrica para criar a view
def create_itens_crud_view(page: ft.Page, on_logout) -> ItensCRUDView:
    return ItensCRUDView(page, on_logout)