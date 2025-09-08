# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py) - VERSÃO REFATORADA
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.components.app_bar import create_app_bar

logger = logging.getLogger("ItensCRUDView")

class ItensCRUDView(ft.View):
    """
    View responsável por LISTAR os itens e gerenciar a exclusão.
    """
    def __init__(self, page: ft.Page, on_logout):
        super().__init__()
        self.page = page
        self.on_logout = on_logout
        self.route = "/cadastros/item"
        self.items_data = []

        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Cadastro de Itens")

        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Unidade")),
                ft.DataColumn(ft.Text("Ações"), numeric=True),
            ],
            rows=[]
        )
        
        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.ElevatedButton(
                            "Adicionar Novo Item",
                            icon=ft.Icons.ADD,
                            # Ação: Navega para a nova rota do formulário de criação.
                            on_click=lambda e: self.page.go("/cadastros/item/novo")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                padding=ft.padding.symmetric(horizontal=10)
            ),
            ft.ListView([self.data_table], expand=True)
        ]

    def show_snackbar(self, message: str, color: str):
        """Exibe uma notificação (SnackBar) na parte inferior da página."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color, duration=3000)
        self.page.snack_bar.open = True
        self.page.update()

    def load_and_update_table(self, success_message: str = None):
        """Carrega os dados do banco e atualiza a tabela na UI. Opcionalmente, exibe uma mensagem de sucesso."""
        try:
            self.items_data = queries.get_all_items_with_details()
            self.data_table.rows.clear()
            
            for item in self.items_data:
                self.data_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'] or "")),
                        ft.DataCell(ft.Text(item['unidade'] or "")),
                        ft.DataCell(ft.Row([
                            ft.IconButton(
                                ft.Icons.EDIT,
                                # Ação: Navega para a rota de edição com o ID do item.
                                on_click=lambda e, item_id=item['id']: self.page.go(f"/cadastros/item/editar/{item_id}"),
                                tooltip="Editar"
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                # Ação: Abre o diálogo de confirmação para exclusão.
                                on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id),
                                tooltip="Excluir"
                            ),
                        ]))
                    ])
                )
            
            # Se uma mensagem de sucesso for passada (pelo callback do formulário), exibe-a.
            if success_message:
                self.show_snackbar(success_message, ft.Colors.GREEN)
            else:
                self.page.update()
        except Exception as e:
            logger.error(f"Erro ao carregar e atualizar a tabela: {e}", exc_info=True)
            self.show_snackbar("Erro ao carregar dados.", ft.Colors.RED)

    def open_delete_dialog(self, item_id):
        """Abre o diálogo de confirmação para exclusão."""
        logger.info(f"AÇÃO DO USUÁRIO: Solicitando exclusão do item ID: {item_id}")
        
        def delete_item_confirm(e):
            logger.info(f"AÇÃO DO USUÁRIO: Confirmou a exclusão do item ID: {item_id}.")
            try:
                queries.delete_item(item_id)
                # Passa a instância do diálogo para garantir que o correto seja fechado.
                self.close_dialog(dialog)
                self.load_and_update_table("Item excluído com sucesso!")
            except Exception as ex:
                logger.error(f"Erro ao excluir item: {ex}", exc_info=True)
                self.show_snackbar("Erro ao excluir o item.", ft.Colors.RED)
        
        # Cria a instância do diálogo localmente.
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir este item?"),
            actions=[
                ft.TextButton("Sim, Excluir", on_click=delete_item_confirm),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Atribui ao page.dialog e abre.
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
    def close_dialog(self, dialog_instance):
        """Fecha a instância específica do diálogo que foi passada."""
        if dialog_instance:
            dialog_instance.open = False
            self.page.update()
