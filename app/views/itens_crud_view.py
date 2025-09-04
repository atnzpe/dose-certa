# =================================================================================
# MÓDULO DA VIEW CRUD DE ITENS (itens_crud_view.py) - DEBUGGING COM LOGS
# =================================================================================

import flet as ft
import logging
from app.database import queries
from app.database.database import get_db_connection # Importa a função de conexão
from app.styles.style import AppDimensions
from app.components.app_bar import create_app_bar

# Configura um logger específico para este módulo para facilitar a filtragem.
logger = logging.getLogger(__name__)

class ItensCRUDView(ft.View):
    def __init__(self, page: ft.Page, on_logout):
        # Log: Início da inicialização da View.
        logger.info("ItensCRUDView: __init__ - Iniciando a construção da view.")
        super().__init__()
        self.page = page
        self.route = "/cadastros/item"
        self.appbar = create_app_bar(page, on_logout)
        self.appbar.title = ft.Text("Cadastro de Itens")
        
        # Log: Inicialização dos atributos de dados.
        self.items_data = []
        self.categories_data = []
        self.units_data = []
        self.dialog = None
        logger.info("ItensCRUDView: __init__ - Atributos de dados inicializados como listas vazias.")

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
        logger.info("ItensCRUDView: __init__ - DataTable criado com sucesso.")

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
        # Log: Finalização da inicialização.
        logger.info("ItensCRUDView: __init__ - Construção da view concluída.")

    def load_all_data(self):
        """Carrega todos os dados necessários do banco usando uma única conexão."""
        logger.info("ItensCRUDView: load_all_data - Iniciando carregamento de dados.")
        
        conn = get_db_connection()
        if not conn:
            logger.error("ItensCRUDView: load_all_data - Falha ao obter conexão com o banco.")
            return

        try:
            logger.debug("ItensCRUDView: load_all_data - Chamando queries.get_all_items_with_details.")
            self.items_data = queries.get_all_items_with_details(conn=conn)
            logger.info(f"ItensCRUDView: load_all_data - {len(self.items_data)} itens encontrados.")

            logger.debug("ItensCRUDView: load_all_data - Chamando queries.get_all_categories.")
            self.categories_data = queries.get_all_categories(conn=conn)
            logger.info(f"ItensCRUDView: load_all_data - {len(self.categories_data)} categorias encontradas.")

            logger.debug("ItensCRUDView: load_all_data - Chamando queries.get_all_units.")
            self.units_data = queries.get_all_units(conn=conn)
            logger.info(f"ItensCRUDView: load_all_data - {len(self.units_data)} unidades encontradas.")

        except Exception as e:
            logger.error(f"ItensCRUDView: load_all_data - Ocorreu uma exceção: {e}", exc_info=True)
        finally:
            logger.debug("ItensCRUDView: load_all_data - Fechando a conexão com o banco.")
            conn.close()
        
        # Chama a atualização da tabela após carregar os dados.
        logger.info("ItensCRUDView: load_all_data - Carregamento concluído. Chamando update_table.")
        self.update_table()

    def update_table(self):
        """Limpa e recarrega as linhas da tabela."""
        logger.info("ItensCRUDView: update_table - Iniciando atualização da DataTable.")
        
        self.data_table.rows.clear()
        logger.debug("ItensCRUDView: update_table - Linhas da tabela limpas.")

        if not self.items_data:
            logger.warning("ItensCRUDView: update_table - Nenhum dado de item para exibir.")

        for item in self.items_data:
            logger.debug(f"ItensCRUDView: update_table - Adicionando item à tabela: {item['nome']}")
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['nome'])),
                        ft.DataCell(ft.Text(item['categoria'] or "")),
                        ft.DataCell(ft.Text(item['unidade'] or "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, i=item: self.open_dialog(i)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, item_id=item['id']: self.open_delete_dialog(item_id)),
                            ])
                        ),
                    ]
                )
            )
        
        logger.info(f"ItensCRUDView: update_table - Tabela populada com {len(self.data_table.rows)} linhas.")
        
        if self.page:
            logger.debug("ItensCRUDView: update_table - Chamando self.page.update() para renderizar as mudanças.")
            self.page.update()
        else:
            logger.warning("ItensCRUDView: update_table - self.page não está disponível. A UI não será atualizada.")

    def open_dialog(self, item_to_edit=None):
        """Abre um diálogo para adicionar ou editar um item."""
        logger.info(f"ItensCRUDView: open_dialog - Abrindo diálogo. Modo Edição: {item_to_edit is not None}")
        
        # Log para verificar se os dados necessários para os dropdowns foram carregados
        if not self.categories_data or not self.units_data:
            logger.error("ItensCRUDView: open_dialog - Dados de categorias ou unidades não foram carregados. O diálogo pode falhar.")
            # Você pode adicionar um snackbar de erro aqui se desejar
            return

        is_editing = item_to_edit is not None

        # --- CAMPOS DO FORMULÁRIO ---
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
        logger.debug("ItensCRUDView: open_dialog - Campos do formulário criados.")

        def save(e):
            logger.info("ItensCRUDView: save (dentro de open_dialog) - Botão 'Salvar' clicado.")
            # Validações básicas podem ser adicionadas aqui
            if not nome_field.value or not categoria_dropdown.value or not unidade_dropdown.value:
                logger.warning("ItensCRUDView: save - Tentativa de salvar com campos vazios.")
                # Implementar feedback visual (ex: snackbar, bordas de erro)
                return

            if is_editing:
                logger.debug(f"ItensCRUDView: save - Chamando queries.update_item para o ID: {item_to_edit['id']}")
                queries.update_item(
                    item_id=item_to_edit['id'],
                    nome=nome_field.value,
                    id_categoria=categoria_dropdown.value,
                    id_unidade_medida=unidade_dropdown.value
                )
            else:
                logger.debug("ItensCRUDView: save - Chamando queries.add_item.")
                queries.add_item(
                    nome=nome_field.value,
                    id_categoria=categoria_dropdown.value,
                    id_unidade_medida=unidade_dropdown.value
                )
            self.dialog.open = False
            logger.info("ItensCRUDView: save - Diálogo fechado. Recarregando todos os dados.")
            self.load_all_data()

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
        logger.debug("ItensCRUDView: open_dialog - Diálogo aberto e página atualizada.")
        self.page.update()

    def open_delete_dialog(self, item_id):
        """Abre um diálogo de confirmação para exclusão."""
        logger.info(f"ItensCRUDView: open_delete_dialog - Abrindo diálogo de exclusão para o item ID: {item_id}")
        
        def delete(e):
            logger.info(f"ItensCRUDView: delete (dentro de open_delete_dialog) - Confirmada a exclusão do item ID: {item_id}")
            queries.delete_item(item_id)
            self.dialog.open = False
            logger.info("ItensCRUDView: delete - Diálogo fechado. Recarregando todos os dados.")
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
        logger.debug(f"ItensCRUDView: open_delete_dialog - Diálogo de exclusão aberto para o item ID: {item_id}.")
        self.page.update()
        
    def close_dialog(self):
        """Fecha o diálogo atualmente aberto."""
        logger.info("ItensCRUDView: close_dialog - Fechando diálogo.")
        if self.dialog:
            self.dialog.open = False
            self.page.update()
