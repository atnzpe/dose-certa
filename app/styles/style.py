# =================================================================================
# MÓDULO DE ESTILOS GLOBAIS (style.py)
# =================================================================================

import flet as ft

# =================================================================================
# PALETAS DE CORES ACESSÍVEIS
# =================================================================================

light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE_GREY_800,
    on_primary=ft.Colors.WHITE,
    primary_container=ft.Colors.BLUE_GREY_100,
    secondary=ft.Colors.TEAL_600,
    on_secondary=ft.Colors.WHITE,
    background=ft.Colors.WHITE,
    on_background=ft.Colors.BLACK87,
    surface=ft.Colors.GREY_50,
    on_surface=ft.Colors.BLACK87,
    error=ft.Colors.RED_700,
    on_error=ft.Colors.WHITE,
)

dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.CYAN_ACCENT_400,
    on_primary=ft.Colors.BLACK,
    primary_container=ft.Colors.CYAN_800,
    secondary=ft.Colors.TEAL_ACCENT_400,
    on_secondary=ft.Colors.BLACK,
    background="#121212",
    on_background=ft.Colors.WHITE,
    surface="#1e1e1e",
    on_surface=ft.Colors.WHITE,
    error=ft.Colors.RED_ACCENT_200,
    on_error=ft.Colors.BLACK,
)

# =================================================================================
# TEMAS COMPLETOS
# =================================================================================

class AppThemes:
    """Agrupa os objetos de Tema para fácil importação."""
    # --- CORRIGIDO: 'ThemeVisualDensity' para 'VisualDensity' ---
    light_theme = ft.Theme(color_scheme=light_color_scheme, visual_density=ft.VisualDensity.COMPACT)
    dark_theme = ft.Theme(color_scheme=dark_color_scheme, visual_density=ft.VisualDensity.COMPACT)

# =================================================================================
# FONTES E DIMENSÕES
# =================================================================================

class AppFonts:
    """Define os tamanhos de fonte padrão."""
    TITLE_LARGE = 32
    TITLE_MEDIUM = 28
    BODY_LARGE = 20
    BODY_MEDIUM = 16
    BODY_SMALL = 14

class AppDimensions:
    """Define dimensões e raios de borda reutilizáveis."""
    FIELD_WIDTH = 300
    BORDER_RADIUS = 10

# =================================================================================
# ESTILOS DE COMPONENTES REUTILIZÁVEIS
# =================================================================================

main_button_style = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=AppDimensions.BORDER_RADIUS),
    padding=ft.padding.all(15),
)
secondary_button_style = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=AppDimensions.BORDER_RADIUS),)