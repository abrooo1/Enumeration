from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProcessingAlgorithm, QgsApplication
from .gui.plugin_dialog import PluginDialog

class ETH_preEA_Tool:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.menu = "&ETH preEA Tool"
        self.action = QAction("Run ETH preEA Tool", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dialog)
        self.iface.addPluginToMenu(self.menu, self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu("&ETH preEA Tool", self.action)
        self.iface.removeToolBarIcon(self.action)

    def show_dialog(self):
        dialog = PluginDialog(self.iface)
        dialog.exec_()