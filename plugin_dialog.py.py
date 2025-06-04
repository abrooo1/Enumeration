from PyQt5.QtWidgets import QDialog
from qgis.core import QgsVectorFileWriter
import os
from ..processing.data_preprocessing import clip_to_boundary, reproject_layer, merge_divided_roads
from ..processing.building_blocks import create_building_blocks
from ..processing.merging import merge_building_blocks
from ..utils.euclidean_allocation import generate_euclidean_allocation

class PluginDialog(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.init_ui()

    def init_ui(self):
        from PyQt5.uic import loadUi
        PLUGIN_DIR = os.path.dirname(__file__)
        loadUi(os.path.join(PLUGIN_DIR, "plugin_dialog.ui"), self)

        self.run_button.clicked.connect(self.run_analysis)

    def run_analysis(self):
        boundary = self.admin_boundary_layer.currentLayer()
        roads = self.road_network_layer.currentLayer()
        railways = self.railway_layer.currentLayer()
        waterways = self.waterways_layer.currentLayer()
        uncrossables = self.uncrossable_features_layer.currentLayer()
        buildings = self.building_footprints_layer.currentLayer()
        max_buildings = self.max_buildings.value()
        max_area = self.max_area.value()
        compact_weight = self.compact_slider.value() / 100.0
        output_folder = self.output_folder.filePath()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        try:
            processed_roads = merge_divided_roads(roads)
            reprojected_roads = reproject_layer(processed_roads)

            euc_alloc = generate_euclidean_allocation(buildings, boundary)
            building_blocks = create_building_blocks([reprojected_roads, railways, waterways], boundary)
            final_preEAs = merge_building_blocks(building_blocks, max_buildings, max_area, compact_weight)

            output_path = os.path.join(output_folder, "ETH_PreEAs.shp")
            QgsVectorFileWriter.writeAsVectorFormat(final_preEAs, output_path, "utf-8", driverName="ESRI Shapefile")

            self.iface.messageBar().pushSuccess("Success", f"preEAs saved to {output_path}")
        except Exception as e:
            self.iface.messageBar().pushCritical("Error", str(e))