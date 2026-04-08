from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QListWidget, QSplitter, QFrame, QAbstractItemView, QSizePolicy
from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import Qt, QObject, QEvent, QCoreApplication, QTimer
from PySide6.QtGui import QPalette, QColor
from source.modules.feynman.fey_17_limpar_abas import adicionar_botao_limpar
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def setup_ui(self):
    try:
        layout = QVBoxLayout()

        self.label_instrucoes = QLabel()
        self.label_instrucoes.setWordWrap(True)
        self.label_instrucoes.setMaximumHeight(60)
        self.label_instrucoes.setAlignment(Qt.AlignTop)
        layout.addWidget(self.label_instrucoes)

        frame_principal = QFrame(self)
        frame_principal.setFrameShape(QFrame.Box)
        frame_principal.setFrameShadow(QFrame.Plain)
        frame_principal.setLineWidth(1)
        frame_principal.setMidLineWidth(0)

        layout_frame = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        painel_esquerdo = QWidget(self)
        layout_esquerdo = QVBoxLayout()

        self.label_meus_conceitos = QLabel()
        layout_esquerdo.addWidget(self.label_meus_conceitos)

        self.lista_conceitos = QListWidget()
        self.lista_conceitos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lista_conceitos.setSelectionRectVisible(True)
        self.lista_conceitos.itemClicked.connect(self.selecionar_conceito)
        self.lista_conceitos.itemDoubleClicked.connect(self.on_lista_conceitos_double_click)
        self.lista_conceitos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_conceitos.customContextMenuRequested.connect(self.mostrar_menu_contexto)
        layout_esquerdo.addWidget(self.lista_conceitos)

        botoes_conceitos = QHBoxLayout()
        botoes_conceitos.setAlignment(Qt.AlignLeft)

        try:
            self.btn_novo = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_novo = QPushButton()

        self.btn_novo.clicked.connect(self.novo_conceito)
        botoes_conceitos.addWidget(self.btn_novo, 0, Qt.AlignLeft)

        try:
            self.btn_deletar = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_deletar = QPushButton()

        self.btn_deletar.clicked.connect(self.deletar_conceito)
        botoes_conceitos.addWidget(self.btn_deletar, 0, Qt.AlignLeft)
        botoes_conceitos.addStretch()

        layout_esquerdo.addLayout(botoes_conceitos)
        painel_esquerdo.setLayout(layout_esquerdo)

        painel_direito = QWidget(self)
        layout_direito = QVBoxLayout()

        self.label_conceito = QLabel()
        self.label_conceito.setWordWrap(True)

        self.input_titulo = QTextEdit()
        self.input_titulo.setObjectName("feynman_user_input")

        self.label_passo1 = QLabel()
        self.label_passo1.setWordWrap(True)

        self.texto_explicacao = QTextEdit()
        self.texto_explicacao.setObjectName("feynman_user_input")

        self.label_passo2 = QLabel()
        self.label_passo2.setWordWrap(True)

        self.texto_lacunas = QTextEdit()
        self.texto_lacunas.setObjectName("feynman_user_input")

        self.label_passo3 = QLabel()
        self.label_passo3.setWordWrap(True)

        self.texto_revisao = QTextEdit()
        self.texto_revisao.setObjectName("feynman_user_input")

        self.label_nivel = QLabel()
        self.combo_dominio = QComboBox()

        self.btn_salvar = QPushButton()

        self.tab_widget = QTabWidget(self)

        # Aba 1: Conceito
        tab1 = QWidget()
        t1_layout = QVBoxLayout()
        t1_layout.addWidget(self.label_conceito)
        t1_layout.addWidget(self.input_titulo)
        tab1.setLayout(t1_layout)

        # Aba 2: Explique com Simplicidade
        tab2 = QWidget()
        t2_layout = QVBoxLayout()
        t2_layout.addWidget(self.label_passo1)
        t2_layout.addWidget(self.texto_explicacao)
        tab2.setLayout(t2_layout)

        # Aba 3: Lacunas Identificadas
        tab3 = QWidget()
        t3_layout = QVBoxLayout()
        t3_layout.addWidget(self.label_passo2)
        t3_layout.addWidget(self.texto_lacunas)
        tab3.setLayout(t3_layout)

        # Aba 4: Revisão e Simplificação Final
        tab4 = QWidget()
        t4_layout = QVBoxLayout()
        t4_layout.addWidget(self.label_passo3)
        t4_layout.addWidget(self.texto_revisao)

        tab4.setLayout(t4_layout)

        self.tab_widget.addTab(tab1, QCoreApplication.translate("App", "1️⃣ Conceito"))
        self.tab_widget.addTab(tab2, QCoreApplication.translate("App", "2️⃣ Explique"))
        self.tab_widget.addTab(tab3, QCoreApplication.translate("App", "3️⃣ Lacunas"))
        self.tab_widget.addTab(tab4, QCoreApplication.translate("App", "4️⃣ Revisão"))

        layout_direito.addWidget(self.tab_widget)

        try:
            self.btn_salvar = self.gerenciador_botoes.create_button()

        except Exception:
            self.btn_salvar = QPushButton()

        try:
            self.btn_salvar.clicked.connect(self.salvar_conceito_atual)

        except Exception:
            pass

        footer_layout = QHBoxLayout()
        self.combo_dominio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        footer_layout.addWidget(self.label_nivel)
        footer_layout.addWidget(self.combo_dominio, 1)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_salvar)

        try:
            try:
                adicionar_botao_limpar(self)

            except Exception:
                pass

            if hasattr(self, 'btn_limpar') and self.btn_limpar is not None:
                footer_layout.addWidget(self.btn_limpar)

        except Exception:
            pass

        layout_direito.addLayout(footer_layout)
        painel_direito.setLayout(layout_direito)

        def _update_right_panel_min_width():
            try:
                btns_width = 0

                if self.btn_salvar is not None:
                    btns_width += self.btn_salvar.minimumSizeHint().width()

                if hasattr(self, "btn_limpar") and self.btn_limpar is not None:
                    btns_width += self.btn_limpar.minimumSizeHint().width()

                min_combo = max(180, self.combo_dominio.minimumSizeHint().width())
                min_label = self.label_nivel.minimumSizeHint().width()
                spacing = max(24, footer_layout.spacing() * 4)
                computed = btns_width + min_combo + min_label + spacing

                painel_direito.setMinimumWidth(max(520, computed))

            except Exception:
                painel_direito.setMinimumWidth(520)

        splitter.addWidget(painel_esquerdo)
        splitter.addWidget(painel_direito)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        painel_esquerdo.setMinimumWidth(260)
        _update_right_panel_min_width()
        splitter.setSizes([320, 960])

        layout_frame.addWidget(splitter)
        frame_principal.setLayout(layout_frame)

        layout.addWidget(frame_principal)
        self.setLayout(layout)

        from PySide6.QtWidgets import QApplication

        def _apply_window_as_base(widget):
            if widget is None:
                return

            app = QApplication.instance()
            if app is None:
                return

            app_pal = app.palette()
            window_color = app_pal.color(QPalette.Window)

            def _is_light_color(col: QColor) -> bool:
                try:
                    r, g, b = col.red(), col.green(), col.blue()
                    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                    return lum >= 0.85

                except Exception:
                    return True

            is_light_theme = _is_light_color(window_color)
            pal = widget.palette()

            try:
                is_combo = isinstance(widget, QComboBox)

            except Exception:
                is_combo = False

            if is_combo:
                try:
                    pal.setColor(QPalette.Button, window_color)

                except Exception:
                    pass

                widget.setPalette(pal)
                view = getattr(widget, "view", None)

                if callable(view):
                    try:
                        v = view()

                        if v is not None:
                            popup_pal = v.palette()

                            if is_light_theme:
                                popup_base = window_color

                            else:
                                popup_base = window_color.darker(115)

                            popup_pal.setColor(QPalette.Base, popup_base)
                            popup_pal.setColor(QPalette.AlternateBase, popup_base)
                            v.setPalette(popup_pal)

                            try:
                                v.viewport().setAutoFillBackground(True)
                                v.viewport().setPalette(popup_pal)

                            except Exception:
                                pass

                    except Exception:
                        pass

            else:
                pal.setColor(QPalette.Base, window_color)
                pal.setColor(QPalette.AlternateBase, window_color)
                widget.setPalette(pal)
                vp = getattr(widget, "viewport", None)

                if callable(vp):
                    try:
                        widget.viewport().setAutoFillBackground(True)
                        widget.viewport().setPalette(pal)

                    except Exception:
                        pass

                else:
                    widget.setAutoFillBackground(True)

                view = getattr(widget, "view", None)

                if callable(view):
                    try:
                        v = view()

                        if v is not None:
                            v.setPalette(pal)

                            try:
                                v.viewport().setAutoFillBackground(True)
                                v.viewport().setPalette(pal)

                            except Exception:
                                pass

                    except Exception:
                        pass

        def _sync_feynman_backgrounds():
            try:
                _apply_window_as_base(self.input_titulo)
                _apply_window_as_base(self.texto_explicacao)
                _apply_window_as_base(self.texto_lacunas)
                _apply_window_as_base(self.texto_revisao)
                _apply_window_as_base(self.combo_dominio)
                _apply_window_as_base(self.lista_conceitos)

            except Exception as e:
                logger.debug(f"Falha ao sincronizar fundos do Método Feynman via QPalette: {e}", exc_info=True)

        class _PaletteThemeSyncFilter(QObject):
            def eventFilter(self, obj, event):
                et = event.type()
                tipos = (QEvent.ApplicationPaletteChange, QEvent.PaletteChange, QEvent.StyleChange, QEvent.ThemeChange,)

                try:
                    tipos = tipos + (QEvent.ColorSchemeChange,)

                except AttributeError:
                    pass

                if et in tipos:
                    _sync_feynman_backgrounds()

                return super().eventFilter(obj, event)

        _sync_feynman_backgrounds()

        self._feynman_palette_sync_filter = _PaletteThemeSyncFilter(self)
        app = QApplication.instance()

        if app is not None:
            app.installEventFilter(self._feynman_palette_sync_filter)

        self.atualizar_traducoes()
        self.atualizar_lista()
        self.conceito_atual = None
        QTimer.singleShot(0, _update_right_panel_min_width)

    except Exception as e:
        logger.error(f"Erro ao configurar interface do MetodoFeynman: {str(e)}", exc_info=True)
