from PySide6.QtWidgets import QGraphicsEllipseItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def itemChange(self, change, value):
    try:
        if change == QGraphicsEllipseItem.ItemPositionHasChanged:
            for linha in self.conexoes:
                linha.atualizar_posicao()

            scene = self.scene()
            if scene and hasattr(scene, "snap"):
                snapped = scene.snap(self.pos())
                QGraphicsEllipseItem.setPos(self, snapped)

            scene = self.scene()
            if scene is not None:
                try:
                    item_br_scene = self.mapToScene(self.boundingRect()).boundingRect()

                    padding = 1200
                    necessario = item_br_scene.adjusted(-padding, -padding, padding, padding)

                    atual = scene.sceneRect()
                    if atual.isNull() or atual.isEmpty():
                        scene.setSceneRect(necessario)

                    else:
                        if not atual.contains(necessario):
                            scene.setSceneRect(atual.united(necessario))

                except Exception:
                    pass

        return QGraphicsEllipseItem.itemChange(self, change, value)

    except Exception as e:
        logger.error(f"Erro ao processar mudança de item: {str(e)}", exc_info=True)
        return QGraphicsEllipseItem.itemChange(self, change, value)
