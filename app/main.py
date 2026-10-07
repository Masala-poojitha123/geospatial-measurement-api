from fastapi import FastAPI, UploadFile, File, HTTPException
import os, tempfile
from.processor import process_kml, process_shapefile_zip, extract_features
from.crs_utils import calculate_measurement
from.storage import storage, save_file

app = FastAPI(title="Geospatial File Measurement API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Geospatial Measurement API running"}

@app.post("/api/files/")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename.endswith('.zip') or file.filename.endswith('.kml')):
        raise HTTPException(status_code=400, detail="Only.zip and.kml allowed")
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        if file.filename.endswith('.kml'):
            gdf = process_kml(tmp_path)
        else:
            gdf = process_shapefile_zip(tmp_path)
        raw_features = extract_features(gdf)
        measurements, clean_features = [], []
        for f in raw_features:
            meas, m_type = calculate_measurement(f["_shapely_geom"], f["crs"])
            measurements.append({"feature_id": f["id"], "type": m_type, "value": meas})
            del f["_shapely_geom"]
            clean_features.append(f)
        crs = raw_features[0]['crs'] if raw_features else "EPSG:4326"
        file_id = save_file(file.filename, clean_features, measurements, crs)
        return storage[file_id]
    finally:
        os.remove(tmp_path)

@app.get("/api/files/{file_id}")
def get_file_info(file_id: str):
    if file_id not in storage:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": storage[file_id]["id"], "filename": storage[file_id]["filename"], "feature_count": storage[file_id]["feature_count"], "crs": storage[file_id]["crs"], "status": storage[file_id]["status"]}

@app.get("/api/files/{file_id}/measurements/")
def get_measurements(file_id: str):
    if file_id not in storage:
        raise HTTPException(status_code=404, detail="Not found")
    return storage[file_id]["measurements"]
