# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py) - CRUD FUNCIONAL
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.database.database import get_db_connection
from app.styles.style import AppDimensions
from app.components.app_bar import create_app_bar

logger = logging.getLogger(__name__)


class ItensCRUDView(ft.View):
    def __init__(self, page: ft.Page, on_logout):
        super().__init__()
        self.page = page
        self.route = "/cadastros/item"
        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Cadastro de Itens")

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
        )

        self.controls = [
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

    def load_all_data(self):
        """Carrega todos os dados necessários do banco e atualiza a tabela."""
        logger.info("ItensCRUDView: Carregando todos os dados do banco.")
        conn = get_db_connection()
        if not conn:
            return
        try:
            self.items_data = queries.get_all_items_with_details(conn=conn)
            self.categories_data = queries.get_all_categories(conn=conn)
            self.units_data = queries.get_all_units(conn=conn)
        finally:
            conn.close()

        self.update_table()

    def update_table(self):
        """Limpa e recarrega as linhas da DataTable com os dados mais recentes."""
        self.data_table.rows.clear()
        for item in self.items_data:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'] or "")),
                        ft.DataCell(ft.Text(item['unidade'] or "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=item: self.open_dialog(
                                    i), tooltip="Editar"),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(
                                    item_id), tooltip="Excluir"),
                            ])
                        ),
                    ]
                )
            )

        # A atualização da página já é chamada dentro das funções save() e delete()
        # após o load_all_data, então chamar aqui é redundante, mas não prejudicial.
        if self.page:
            self.page.update()

    def open_dialog(self, item_to_edit=None):
        """Abre um diálogo para adicionar ou editar um item."""
        is_editing = item_to_edit is not None

        nome_field = ft.TextField(
            label="Nome do Item", value=item_to_edit['nome'] if is_editing else "")
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(cat['id'], cat['nome'])
                     for cat in self.categories_data],
            value=item_to_edit.get('id_categoria') if is_editing else None
        )
        unidade_dropdown = ft.Dropdown(
            label="Unidade de Medida",
            options=[ft.dropdown.Option(unit['id'], unit['nome'])
                     for unit in self.units_data],
            value=item_to_edit.get('id_unidade_medida') if is_editing else None
        )

        def save(e):
            """Função aninhada para salvar as alterações do item."""
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
            self.close_dialog()  # Fecha o diálogo
            self.load_all_data()  # Recarrega os dados do banco
            # CORREÇÃO: page.update() foi movido para dentro de load_all_data -> update_table

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Editar Item" if is_editing else "Adicionar Novo Item"),
            content=ft.Column(
                [nome_field, categoria_dropdown, unidade_dropdown]),
            actions=[
                ft.TextButton("Salvar", on_click=save),
                ft.TextButton(
                    "Cancelar", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def open_delete_dialog(self, item_id):
        """Abre um diálogo de confirmação para exclusão."""
        def delete(e):
            """Função aninhada para deletar o item."""
            queries.delete_item(item_id)
            self.close_dialog()
            self.load_all_data()
            # CORREÇÃO: page.update() foi movido para dentro de load_all_data -> update_table

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir este item?"),
            actions=[
                ft.TextButton("Sim, Excluir", on_click=delete),
                ft.TextButton(
                    "Cancelar", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Fecha o diálogo atualmente aberto de forma segura."""
        if self.dialog:
            self.dialog.open = False
            self.page.update()
