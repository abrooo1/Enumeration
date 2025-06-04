def clip_to_boundary(layer, boundary_layer):
    from qgis import processing
    return processing.run("qgis:clip", {'INPUT': layer, 'OVERLAY': boundary_layer})['OUTPUT']

def reproject_layer(layer, crs="EPSG:32637"):
    from qgis import processing
    return processing.run("qgis:reprojectlayer", {'INPUT': layer, 'TARGET_CRS': crs})['OUTPUT']

def merge_divided_roads(road_layer):
    from qgis import processing
    return processing.run("native:mergelines", {'INPUT': road_layer})['OUTPUT']