# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py) - VERSÃO FINAL CORRIGIDA
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.components.app_bar import create_app_bar

# Configuração do logger para este módulo.
logger = logging.getLogger(__name__)

class ItensCRUDView(ft.View):
    """
    Classe que representa a View de Gerenciamento de Itens (CRUD).
    """
    def __init__(self, page: ft.Page, on_logout):
        """
        Construtor da classe ItensCRUDView.

        - Inicializa a View, seus componentes e atributos de dados.
        - Define a estrutura visual da tela.
        """
        super().__init__()
        # ==================================================
        # 1. INICIALIZAÇÃO DE ATRIBUTOS
        # ==================================================
        logger.debug("ItensCRUDView: __init__ - Iniciando.")
        self.page = page  # Referência ao objeto da página principal.
        self.on_logout = on_logout # Função de callback para logout.
        self.route = "/cadastros/item" # Rota desta view.

        # Atributos para armazenar os dados carregados do banco.
        self.items_data = []
        self.categories_data = []
        self.units_data = []

        # Atributo para o diálogo de adição/edição.
        self.dialog = None

        # ==================================================
        # 2. DEFINIÇÃO DA INTERFACE GRÁFICA (UI)
        # ==================================================
        
        # Cria a AppBar reutilizável.
        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Cadastro de Itens")

        # Cria a DataTable que exibirá os itens.
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Unidade")),
                ft.DataColumn(ft.Text("Ações"), numeric=True),
            ],
            rows=[], # As linhas serão populadas dinamicamente.
        )
        
        # Define a estrutura de controles da View.
        self.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.ElevatedButton(
                            "Adicionar Novo Item",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.open_dialog(), # Chama o diálogo sem item (modo de criação).
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.symmetric(horizontal=10)
            ),
            # Coloca a DataTable dentro de um ListView para garantir a rolagem.
            ft.ListView([self.data_table], expand=True),
        ]
        logger.debug("ItensCRUDView: __init__ - Construção da UI concluída.")

    def load_and_update_table(self):
        """
        Função central que carrega os dados do banco e atualiza a tabela na UI.
        """
        logger.debug("ItensCRUDView: load_and_update_table - Iniciando.")
        try:
            # Carrega todos os dados necessários.
            self.items_data = queries.get_all_items_with_details()
            self.categories_data = queries.get_all_categories()
            self.units_data = queries.get_all_units()
            logger.info(f"ItensCRUDView: Dados carregados - {len(self.items_data)} itens.")
            
            # Limpa as linhas existentes da tabela.
            self.data_table.rows.clear()
            
            # Repopula a tabela com os novos dados.
            for item in self.items_data:
                self.data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item['nome'])),
                            ft.DataCell(ft.Text(item['categoria'] or "")),
                            ft.DataCell(ft.Text(item['unidade'] or "")),
                            ft.DataCell(
                                ft.Row([
                                    # CORREÇÃO: Passa o objeto 'item' diretamente para a lambda.
                                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=item: self.open_dialog(i), tooltip="Editar"),
                                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id), tooltip="Excluir"),
                                ])
                            ),
                        ]
                    )
                )
            
            logger.info(f"ItensCRUDView: Tabela atualizada com {len(self.data_table.rows)} linhas.")
            # Atualiza a página para refletir as mudanças.
            self.page.update()
        except Exception as e:
            logger.error(f"ItensCRUDView: Erro ao carregar e atualizar a tabela: {e}", exc_info=True)

    def open_dialog(self, item_to_edit=None):
        """
        Abre o diálogo para Adicionar (item_to_edit=None) ou Editar um item.
        """
        is_editing = item_to_edit is not None
        logger.info(f"ItensCRUDView: open_dialog - Modo Edição: {is_editing}")
        
        # --- Cria os campos do formulário ---
        nome_field = ft.TextField(label="Nome do Item", value=item_to_edit['nome'] if is_editing else "")
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(cat['id'], cat['nome']) for cat in self.categories_data],
            value=item_to_edit.get('id_categoria') if is_editing else None
        )
        unidade_dropdown = ft.Dropdown(
            label="Unidade de Medida",
            options=[ft.dropdown.Option(unit['id'], unit['nome']) for unit in self.units_data],
            value=item_to_edit.get('id_unidade_medida') if is_editing else None
        )
        
        def save_item(e):
            """Função de callback para o botão Salvar."""
            try:
                if is_editing:
                    logger.debug(f"ItensCRUDView: save_item - Atualizando item ID: {item_to_edit['id']}")
                    queries.update_item(
                        item_id=item_to_edit['id'],
                        nome=nome_field.value,
                        id_categoria=int(categoria_dropdown.value),
                        id_unidade_medida=int(unidade_dropdown.value)
                    )
                else:
                    logger.debug("ItensCRUDView: save_item - Adicionando novo item.")
                    queries.add_item(
                        nome=nome_field.value,
                        id_categoria=int(categoria_dropdown.value),
                        id_unidade_medida=int(unidade_dropdown.value)
                    )
                self.close_dialog()
                self.load_and_update_table() # Recarrega tudo
            except Exception as ex:
                logger.error(f"ItensCRUDView: Erro ao salvar item: {ex}", exc_info=True)
        
        # Cria e configura o diálogo
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Item" if is_editing else "Adicionar Novo Item"),
            content=ft.Column([nome_field, categoria_dropdown, unidade_dropdown]),
            actions=[
                ft.TextButton("Salvar", on_click=save_item),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Abre o diálogo na página
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def open_delete_dialog(self, item_id):
        """Abre o diálogo de confirmação para exclusão."""
        logger.info(f"ItensCRUDView: open_delete_dialog - Solicitando exclusão do item ID: {item_id}")
        
        def delete_item(e):
            """Função de callback para o botão Excluir."""
            try:
                logger.debug(f"ItensCRUDView: delete_item - Excluindo item ID: {item_id}")
                queries.delete_item(item_id)
                self.close_dialog()
                self.load_and_update_table() # Recarrega tudo
            except Exception as ex:
                logger.error(f"ItensCRUDView: Erro ao excluir item: {ex}", exc_info=True)
                
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir este item?"),
            actions=[
                ft.TextButton("Sim, Excluir", on_click=delete_item),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
            ],
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
        
    def close_dialog(self, e=None):
        """Fecha o diálogo que estiver aberto."""
        if self.dialog:
            logger.debug("ItensCRUDView: close_dialog - Fechando diálogo.")
            self.dialog.open = False
            self.page.update()