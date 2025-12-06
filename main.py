from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

app = FastAPI()

origins = [
    os.getenv("ALLOWED_ORIGIN1"),
    os.getenv("ALLOWED_ORIGIN2"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client("s3")

BASE_MODELS_DIR = Path("3d-models")
BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get("/load-local-model/{path_name}")
async def load_model(path_name: str):
    folder = BASE_MODELS_DIR / path_name

    if not folder.exists() or not folder.is_dir():
        raise HTTPException(404, f"Model folder '{path_name}' not found in backend.")

    obj_files = list(folder.glob("*.obj"))
    mtl_files = {f.stem: f for f in folder.glob("*.mtl")}

    if not obj_files:
        raise HTTPException(404, "No OBJ files found in the folder.")

    rendering_elements = []

    for obj_path in obj_files:
        filename = obj_path.name
        base = obj_path.stem    

        obj_content = obj_path.read_text()
        mtl_content = ""
        if base in mtl_files:
            mtl_content = mtl_files[base].read_text()

        rendering_elements.append({
            "filename": filename,
            "objContent": obj_content,
            "mtlContent": mtl_content
        })

    return {"renderingElements": rendering_elements}


@app.get("/load-model/{path_name}")
async def load_model(path_name: str):
    prefix = f"{path_name}/"  

    try:
        listed = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if "Contents" not in listed:
        raise HTTPException(404, f"No files found in S3 folder: {prefix}")

    # Extract all file names in folder
    files = [item["Key"] for item in listed["Contents"]]

    obj_files = [f for f in files if f.endswith(".obj")]
    mtl_files = [f for f in files if f.endswith(".mtl")]

    if not obj_files:
        raise HTTPException(404, "No OBJ files found in S3 folder")

    rendering_elements = []

    for obj_key in obj_files:
        obj_filename = obj_key.split("/")[-1]   
        base_name = obj_filename.replace(".obj", "")

        # Read OBJ content
        obj_data = s3.get_object(Bucket=BUCKET_NAME, Key=obj_key)
        obj_text = obj_data["Body"].read().decode("utf-8")

        # Find matching MTL
        mtl_key = f"{path_name}/{base_name}.mtl"

        mtl_text = ""
        if mtl_key in mtl_files:
            mtl_data = s3.get_object(Bucket=BUCKET_NAME, Key=mtl_key)
            mtl_text = mtl_data["Body"].read().decode("utf-8")

        rendering_elements.append({
            "filename": obj_filename,
            "objContent": obj_text,
            "mtlContent": mtl_text
        })

    return {"renderingElements": rendering_elements}