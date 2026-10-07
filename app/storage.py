storage = {}

def save_file(filename, features, measurements, crs):
    import uuid
    file_id = str(uuid.uuid4())[:8]
    storage[file_id] = {
        "id": file_id,
        "filename": filename,
        "feature_count": len(features),
        "crs": crs,
        "status": "COMPLETED",
        "features": features,
        "measurements": measurements
    }
    return file_id
