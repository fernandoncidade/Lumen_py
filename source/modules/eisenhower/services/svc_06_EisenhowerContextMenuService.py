from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QCoreApplication, QLocale
from source.modules.eisenhower.services.EisenhowerContextMenuService import (
    _compute_widget_height,
    _apply_widget_min_height,
    _effective_locale,
    _apply_locale_to_dateedit,
    _is_completed_list,
    _quadrant_options,
    _target_list_for_quadrant,
    _find_source_item_for_calendar,
    editar_tarefa_item,
    editar_tarefa_por_dados,
    remover_tarefa_item,
    remover_tarefa_por_dados,
    remover_todas_por_data,
    _base_text_from_item,
    _build_display_and_tooltip,
    _edit_date_time_dialog,
    _move_to_quadrant,
    mostrar_menu_contexto
)
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class EisenhowerContextMenuService:
    def __init__(self, app):
        self.app = app

    def get_text(self, text):
        return QCoreApplication.translate("App", text)

    def _compute_widget_height(self, widget, name: str | None = None) -> int:
        return _compute_widget_height(self, widget, name)

    def _apply_widget_min_height(self, widget, name: str | None = None):
        return _apply_widget_min_height(self, widget, name)

    def _effective_locale(self) -> QLocale:
        return _effective_locale(self)

    def _apply_locale_to_dateedit(self, de: QDateEdit):
        return _apply_locale_to_dateedit(self, de)

    def _is_completed_list(self, lst) -> bool:
        return _is_completed_list(self, lst)

    def _quadrant_options(self):
        return _quadrant_options(self)

    def _target_list_for_quadrant(self, quadrant_index: int, keep_completed: bool):
        return _target_list_for_quadrant(self, quadrant_index, keep_completed)

    def _find_source_item_for_calendar(self, task_dict):
        return _find_source_item_for_calendar(self, task_dict)

    def editar_tarefa_item(self, item, list_widget=None):
        return editar_tarefa_item(self, item, list_widget)

    def editar_tarefa_por_dados(self, task_data: dict):
        return editar_tarefa_por_dados(self, task_data)

    def remover_tarefa_item(self, item, list_widget=None, confirm: bool = True) -> bool:
        return remover_tarefa_item(self, item, list_widget, confirm)

    def remover_tarefa_por_dados(self, task_data: dict, confirm: bool = True) -> bool:
        return remover_tarefa_por_dados(self, task_data, confirm)

    def remover_todas_por_data(self, date_iso: str) -> int:
        return remover_todas_por_data(self, date_iso)

    def _base_text_from_item(self, item) -> str:
        return _base_text_from_item(self, item)

    def _build_display_and_tooltip(self, base_text: str, date_iso: str | None, time_str: str | None):
        return _build_display_and_tooltip(self, base_text, date_iso, time_str)

    def _edit_date_time_dialog(self, item):
        return _edit_date_time_dialog(self, item)

    def _move_to_quadrant(self, item, source_list):
        return _move_to_quadrant(self, item, source_list)

    def mostrar_menu_contexto(self, point, list_widget):
        return mostrar_menu_contexto(self, point, list_widget)


def show_context_menu(app_or_service, point, list_widget):
    try:
        if isinstance(app_or_service, EisenhowerContextMenuService):
            return app_or_service.mostrar_menu_contexto(point, list_widget)

        svc = EisenhowerContextMenuService(app_or_service)
        return svc.mostrar_menu_contexto(point, list_widget)

    except Exception as e:
        logger.error(f"Erro em show_context_menu wrapper: {e}", exc_info=True)
        return None

def editar_tarefa_por_dados(app_or_service, task_data: dict):
    try:
        if isinstance(app_or_service, EisenhowerContextMenuService):
            return app_or_service.editar_tarefa_por_dados(task_data)

        svc = EisenhowerContextMenuService(app_or_service)
        return svc.editar_tarefa_por_dados(task_data)

    except Exception as e:
        logger.error(f"Erro em editar_tarefa_por_dados wrapper: {e}", exc_info=True)
        return None

def remover_tarefa_por_dados(app_or_service, task_data: dict, confirm: bool = True) -> bool:
    try:
        if isinstance(app_or_service, EisenhowerContextMenuService):
            return bool(app_or_service.remover_tarefa_por_dados(task_data, confirm=confirm))

        svc = EisenhowerContextMenuService(app_or_service)
        return bool(svc.remover_tarefa_por_dados(task_data, confirm=confirm))

    except Exception as e:
        logger.error(f"Erro em remover_tarefa_por_dados wrapper: {e}", exc_info=True)
        return False

def remover_todas_por_data(app_or_service, date_iso: str) -> int:
    try:
        if isinstance(app_or_service, EisenhowerContextMenuService):
            return int(app_or_service.remover_todas_por_data(date_iso))

        svc = EisenhowerContextMenuService(app_or_service)
        return int(svc.remover_todas_por_data(date_iso))

    except Exception as e:
        logger.error(f"Erro em remover_todas_por_data wrapper: {e}", exc_info=True)
        return 0
