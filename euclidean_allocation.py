def generate_euclidean_allocation(building_raster, admin_boundary):
    from qgis import processing
    polygons = processing.run("gdal:polygonize", {'INPUT': building_raster, 'BAND': 1})['OUTPUT']
    clipped = clip_to_boundary(polygons, admin_boundary)
    allocation = processing.run("gdal:proximity", {
        'INPUT': clipped,
        'VALUES': '1',
        'DISTANCE_UNITS': 1
    })['OUTPUT']
    return allocation