import zipfile, tempfile, os
import geopandas as gpd

def process_kml(file_path: str):
    gdf = gpd.read_file(file_path, driver='KML')
    return gdf

def process_shapefile_zip(zip_path: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmpdir)
            shp_file = None
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith('.shp'):
                        shp_file = os.path.join(root, f)
                        break
            if not shp_file:
                raise ValueError("No .shp found in zip")
            gdf = gpd.read_file(shp_file)
            return gdf

def extract_features(gdf):
    features = []
    crs_str = str(gdf.crs) if gdf.crs else "EPSG:4326"
    for idx, row in gdf.iterrows():
        geom = row.geometry
        features.append({
            "id": int(idx),
            "geometry_type": geom.geom_type,
            "geometry": geom.__geo_interface__,
            "crs": crs_str,
            "properties": {k: v for k, v in row.items() if k != 'geometry'},
            "_shapely_geom": geom
        })
    return features
