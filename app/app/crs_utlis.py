from shapely.ops import transform
import pyproj

def get_utm_crs(lon: float, lat: float) -> str:
    zone_number = int((lon + 180) / 6) + 1
    is_northern = lat >= 0
    epsg = 32600 + zone_number if is_northern else 32700 + zone_number
    return f"EPSG:{epsg}"

def get_projected_geometry(geom, src_crs: str):
    if src_crs is None:
        src_crs = "EPSG:4326"
    if src_crs != "EPSG:4326" and "4326" not in str(src_crs):
        return geom, src_crs
    centroid = geom.centroid
    dst_crs = get_utm_crs(centroid.x, centroid.y)
    transformer = pyproj.Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    projected_geom = transform(transformer.transform, geom)
    return projected_geom, dst_crs

def calculate_measurement(geom, src_crs: str):
    if geom.geom_type == "Point":
        return None, None
    proj_geom, _ = get_projected_geometry(geom, src_crs)
    if geom.geom_type in ["Polygon", "MultiPolygon"]:
        return {"area_sq_m": float(proj_geom.area)}, "AREA"
    elif geom.geom_type in ["LineString", "MultiLineString"]:
        return {"length_m": float(proj_geom.length)}, "LENGTH"
    else:
        return None, "UNSUPPORTED"
