def create_building_blocks(input_layers, admin_boundary):
    from qgis import processing
    merged_lines = []
    for layer in input_layers:
        clipped = clip_to_boundary(layer, admin_boundary)
        reprojected = reproject_layer(clipped)
        merged_lines.append(reprojected)

    combined = processing.run("native:collect", {'INPUT': merged_lines})['OUTPUT']
    voronoi = processing.run("qgis:voronoipolygons", {'INPUT': combined, 'BUFFER': 0.01})['OUTPUT']
    intersected = processing.run("qgis:intersection", {'INPUT': voronoi, 'OVERLAY': admin_boundary})['OUTPUT']
    return intersected