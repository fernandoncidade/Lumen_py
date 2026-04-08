import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from source.utils.LogManager import LogManager
from source.utils.IconUtils import get_icon_path
logger = LogManager.get_logger()
WINDOWS_APP_ID = "fernandoncidade.lumen.estudoacessivel"
_NATIVE_ICON_HANDLES = []

def configurar_windows_app_id(app_id: str = WINDOWS_APP_ID) -> bool:
    if os.name != "nt":
        return False

    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(str(app_id))
        logger.debug(f"AppUserModelID configurado para Windows: {app_id}")
        return True

    except Exception as e:
        logger.warning(f"Não foi possível configurar AppUserModelID: {e}", exc_info=True)
        return False

def configurar_aplicacao():
    app = QApplication(sys.argv)
    app.setApplicationName("Lúmen")
    app.setOrganizationName("fernandoncidade")
    app.setOrganizationDomain("fernandoncidade.github.io")
    return app

def configurar_icone_aplicacao(app):
    icon_path = get_icon_path("autismo.ico")
    logger.debug(f"Tentando carregar ícone de: {icon_path}")

    if icon_path and os.path.exists(icon_path):
        try:
            with open(icon_path, "rb") as fh:
                header = fh.read(6)

                if header[:4] == b"\x00\x00\x01\x00":
                    count = int.from_bytes(header[4:6], "little")

                    if count < 2:
                        logger.warning(
                            "O arquivo autismo.ico possui apenas 1 tamanho interno. "
                            "Recomenda-se ícone multi-resolução (16/24/32/48/64/128/256) "
                            "para estabilidade na barra de tarefas."
                        )

        except Exception:
            pass

        app_icon = QIcon(icon_path)
        available_sizes = app_icon.availableSizes()
        logger.debug(f"Tamanhos disponíveis do ícone: {available_sizes}")

        if not app_icon.isNull():
            app.setWindowIcon(app_icon)
            logger.info(f"✓ Ícone da aplicação configurado com sucesso: {icon_path}")
            return app_icon

        else:
            logger.error(f"✗ Ícone carregado está nulo ou sem tamanhos: {icon_path}")

    else:
        logger.error(f"✗ Caminho do ícone não encontrado ou não existe: {icon_path}")

    return None

def criar_janela_principal():
    from source import EstudoAcessivel
    return EstudoAcessivel()

def configurar_icone_janela(window, app_icon):
    if app_icon:
        window.setWindowIcon(app_icon)

    try:
        icon_path = get_icon_path("autismo.ico")
        _aplicar_icone_nativo_windows(window, icon_path)

    except Exception as e:
        logger.debug(f"Não foi possível aplicar ícone nativo na janela: {e}")

def _aplicar_icone_nativo_windows(window, icon_path: str):
    if os.name != "nt" or not icon_path or not os.path.exists(icon_path):
        return

    try:
        import ctypes

        hwnd = int(window.winId())
        user32 = ctypes.windll.user32
        LR_LOADFROMFILE = 0x00000010
        LR_DEFAULTSIZE = 0x00000040
        IMAGE_ICON = 1
        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1

        hicon_small = user32.LoadImageW(None, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE | LR_DEFAULTSIZE)
        hicon_big = user32.LoadImageW(None, icon_path, IMAGE_ICON, 256, 256, LR_LOADFROMFILE | LR_DEFAULTSIZE)

        if hicon_small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
            _NATIVE_ICON_HANDLES.append(hicon_small)

        if hicon_big:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
            _NATIVE_ICON_HANDLES.append(hicon_big)

        logger.debug("Ícone nativo do Windows aplicado via WM_SETICON")

    except Exception as e:
        logger.debug(f"Falha ao aplicar ícone nativo via WM_SETICON: {e}", exc_info=True)

def iniciar_aplicacao():
    try:
        configurar_windows_app_id()
        app = configurar_aplicacao()
        app_icon = configurar_icone_aplicacao(app)
        window = criar_janela_principal()
        # from source.utils.TrialManager import TrialManager
        # TrialManager.enforce_trial()  # Descomente esta linha para forçar o uso da versão de avaliação
        # TrialManager.delete_first_run_timestamp()  # Use esta linha para testes, removendo o timestamp de primeiro uso

        configurar_icone_janela(window, app_icon)
        window.show()

        exit_code = app.exec()
        logger.debug(f"Aplicação encerrada com código de saída: {exit_code}")

        return exit_code

    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar aplicação: {e}", exc_info=True)
        return 1

def montar_e_mostrar_janela(app):
    try:
        app_icon = configurar_icone_aplicacao(app)
        window = criar_janela_principal()
        configurar_icone_janela(window, app_icon)
        window.show()

        try:
            from PySide6.QtCore import QTimer
            icon_path = get_icon_path("autismo.ico")
            QTimer.singleShot(0, lambda: _aplicar_icone_nativo_windows(window, icon_path))

        except Exception:
            pass

        return window

    except Exception as e:
        logger.critical(f"Erro ao montar e mostrar janela: {e}", exc_info=True)
        raise
