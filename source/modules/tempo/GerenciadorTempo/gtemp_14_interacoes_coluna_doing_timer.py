from PySide6.QtCore import Qt
from source.utils.LogManager import LogManager
from source.utils.MessageBox import MessageBox
logger = LogManager.get_logger()

def _item_key(item):
    try:
        if item is None:
            return None

        tarefa_id = item.data(Qt.UserRole)

        if tarefa_id:
            return ("id", tarefa_id)

        titulo = ((item.text() or "").split("\n")[0] or "")
        titulo = titulo.split("—")[0]
        titulo = (
            titulo
            .replace("🔴 ", "")
            .replace("🟠 ", "")
            .replace("🟡 ", "")
            .replace("🟢 ", "")
            .strip()
        )
        return ("titulo", titulo)

    except Exception:
        return None

def _resolver_tarefa_por_item_doing_timer(self, item):
    try:
        if item is None:
            return None

        tarefa_id = item.data(Qt.UserRole)
        tarefas = getattr(getattr(self, "tarefas", None), "tarefas", []) or []

        if tarefa_id:
            for t in tarefas:
                if getattr(t, "id", None) == tarefa_id:
                    return t

        key = _item_key(item)

        if not key or key[0] != "titulo":
            return None

        titulo = key[1]

        for t in tarefas:
            if (getattr(t, "titulo", "") or "").strip() == titulo:
                return t

        return None

    except Exception as e:
        logger.error(f"Erro ao resolver tarefa da coluna lateral: {str(e)}", exc_info=True)
        return None

def _abrir_arquivo_vinculado_coluna_doing_timer(self, item):
    try:
        alvo = _resolver_tarefa_por_item_doing_timer(self, item)

        if not alvo:
            return

        path = getattr(alvo, "file_path", None)

        if not path:
            return

        import os
        import subprocess

        if os.path.exists(path):
            try:
                if os.name == "nt":
                    os.startfile(path)

                else:
                    subprocess.Popen(["xdg-open", path])

            except Exception as e:
                logger.error(f"Erro ao abrir arquivo vinculado na coluna lateral: {str(e)}", exc_info=True)

                try:
                    subprocess.Popen([path], shell=True)

                except Exception as e2:
                    logger.error(f"Erro ao abrir arquivo vinculado na coluna lateral: {str(e2)}", exc_info=True)

        else:
            MessageBox.warning_file_not_found(self)

    except Exception as e:
        logger.error(f"Erro no duplo clique da coluna lateral: {str(e)}", exc_info=True)

def _sincronizar_estado_coluna_doing_timer(self):
    try:
        lista_direita = getattr(self, "col_doing_timer_list", None)
        lista_central_doing = getattr(getattr(getattr(self, "tarefas", None), "col_doing", None), "lista", None)

        if lista_direita is None or lista_central_doing is None:
            return

        estados = {}

        for i in range(lista_direita.count()):
            item = lista_direita.item(i)
            key = _item_key(item)

            if key is None:
                continue

            estados[key] = {"selected": bool(item.isSelected()),}

        lista_central_doing.blockSignals(True)

        try:
            for i in range(lista_central_doing.count()):
                item = lista_central_doing.item(i)
                key = _item_key(item)
                estado = estados.get(key, None)

                if estado is None:
                    item.setSelected(False)
                    continue

                item.setSelected(bool(estado.get("selected", False)))

        finally:
            lista_central_doing.blockSignals(False)

    except Exception as e:
        logger.error(f"Erro ao sincronizar seleção da coluna lateral: {str(e)}", exc_info=True)

def _mostrar_menu_contexto_coluna_doing_timer(self, pos):
    try:
        lista = getattr(self, "col_doing_timer_list", None)

        if lista is None:
            return

        item = lista.itemAt(pos)

        if item is None:
            return

        self._sincronizar_estado_coluna_doing_timer()

        if hasattr(self, "tarefas") and self.tarefas is not None:
            self.tarefas.mostrar_menu_contexto(pos, lista)

    except Exception as e:
        logger.error(f"Erro ao abrir menu de contexto da coluna lateral: {str(e)}", exc_info=True)
