# Geospatial File Measurement API

## Run
pip install -r app/requirements.txt
uvicorn app.main:app --reload

## APIs
- POST /api/files/ - upload KML or ZIP
- GET /api/files/{id}
- GET /api/files/{id}/measurements/

## CRS Handling
Files EPSG:4326 lo untayi, degrees lo area wrong vastundi. So centroid tho UTM zone kanukoni reproject chesi meters lo calculate chesa.

## Learnings
UTM auto-detection, GeoPandas KML parsing

## Future
PostGIS, Celery, GeoJSON support
