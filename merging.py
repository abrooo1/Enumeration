def add_building_count(blocks_layer):
    # Dummy function; replace with real raster count join
    return blocks_layer

def apply_area_threshold(layer, max_area):
    from qgis import processing
    return processing.run("qgis:extractbyattribute", {
        'INPUT': layer,
        'FIELD': 'area',
        'OPERATOR': 2,  # Less than
        'VALUE': str(max_area)
    })['OUTPUT']

def merge_building_blocks(blocks_layer, max_buildings, max_area, compact_weight):
    from qgis import processing
    blocks_with_count = add_building_count(blocks_layer)
    merged = processing.run("qgis:dissolve", {
        'INPUT': blocks_with_count,
        'FIELD': ['building_count'],
        'SEPARATE_COLLECTIONS': True
    })['OUTPUT']
    filtered = apply_area_threshold(merged, max_area)
    return filtered