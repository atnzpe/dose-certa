# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py) - OTIMIZADO
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.database.database import get_db_connection # Importa a função de conexão
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
            expand=True,
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
        """Carrega todos os dados necessários do banco usando uma única conexão."""
        logger.info("Carregando dados para a ItensCRUDView com conexão otimizada.")
        # Abre uma única conexão para todas as queries desta operação
        conn = get_db_connection()
        if not conn:
            logger.error("Não foi possível carregar os dados: falha na conexão com o banco.")
            return

        try:
            self.items_data = queries.get_all_items_with_details(conn=conn)
            self.categories_data = queries.get_all_categories(conn=conn)
            self.units_data = queries.get_all_units(conn=conn)
        finally:
            # Fecha a conexão após todas as queries serem concluídas
            conn.close()
        
        self.update_table()

    def update_table(self):
        """Limpa e recarrega as linhas da tabela."""
        self.data_table.rows.clear()
        for item in self.items_data:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'] or "")), # Adicionado 'or ""' para evitar erros se for None
                        ft.DataCell(ft.Text(item['unidade'] or "")),   # Adicionado 'or ""' para evitar erros se for None
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=item: self.open_dialog(i)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id)),
                            ])
                        ),
                    ]
                )
            )
        # Verifica se a página ainda existe antes de atualizar
        if self.page:
            self.page.update() # Alterado de self.update() para self.page.update() para garantir a atualização completa da tela

    def open_dialog(self, item_to_edit=None):
        """Abre um diálogo para adicionar ou editar um item."""
        is_editing = item_to_edit is not None

        # --- CAMPOS DO FORMULÁRIO ---
        nome_field = ft.TextField(label="Nome do Item", value=item_to_edit['nome'] if is_editing else "")
        
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(cat['id'], cat['nome']) for cat in self.categories_data],
            value=item_to_edit.get('id_categoria') if is_editing else None # Usar .get() para segurança
        )
        
        unidade_dropdown = ft.Dropdown(
            label="Unidade de Medida",
            options=[ft.dropdown.Option(unit['id'], unit['nome']) for unit in self.units_data],
            value=item_to_edit.get('id_unidade_medida') if is_editing else None # Usar .get() para segurança
        )

        def save(e):
            # As chamadas a queries aqui usarão sua própria conexão, o que é aceitável
            # para operações de escrita individuais.
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
