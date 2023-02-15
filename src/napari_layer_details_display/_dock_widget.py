from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QScrollArea
from qtpy.QtCore import Qt
from napari_tools_menu import register_dock_widget

@register_dock_widget(menu = "Utilities > Layer Details")
class LayerDetailsDisplay(QMainWindow):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.text = QLabel("")
        self.text.setWordWrap(True)

        # create a scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # disable horizontal scroll bar
        self.scrollArea.setMinimumWidth(400)
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)

        self.contents = QWidget()

        # self.contents.setAlignment(AlignTop)
        self.scrollArea.setWidget(self.contents)
        self.scrollArea.setWidget(self.contents)
        self.layout = QVBoxLayout(self.contents)

        self.layout.addWidget(self.text)

        btn = QPushButton("Refresh")
        btn.clicked.connect(self._on_selection)
        self.layout.addWidget(btn)

        napari_viewer.layers.selection.events.changed.connect(self._on_selection)

        self._on_selection()

    def _on_selection(self, event=None):
        text = ""
        for layer in self.viewer.layers.selection:
            text = text + \
                   "<b>" + layer.name + "</b>"
            if hasattr(layer, "data"):
                text = text + \
                       "<li>data:"

                text = text + ", ".join([attr_to_str(layer.data, attr) for attr in ["shape", "dtype"]])
                text = text + ", <br/>" + str(type(layer.data)).replace("<", "&lt;").replace(">", "&gt;") + \
                       "</li>"

                for attr in ["scale", "translate", "rotate", "shear", "opacity", "contrast_limits", "gamma", "multiscale", "cache", "metadata", "properties"]:
                    value = attr_to_str(layer, attr)
                    if value is not None:
                        text = text + \
                               "<li>" + attr + ":" + value + "</li>"
            text = text + \
                   "<br/><br>"

        self.text.setText(text)

def attr_to_str(object, attr):
    if hasattr(object, attr):
        value = getattr(object, attr)
        if isinstance(value, dict):
            return "<br/>&nbsp;-&nbsp;" + str(list(value.keys())).replace(",", "<br/>&nbsp;-&nbsp;")
        else:
            return str(value)
    return ""

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [LayerDetailsDisplay]
