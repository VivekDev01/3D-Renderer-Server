from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

# Allow React requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_MODELS_DIR = Path("3d-models")  # folder inside backend


@app.get("/load-model/{path_name}")
async def load_model(path_name: str):
    folder = BASE_MODELS_DIR / path_name

    if not folder.exists() or not folder.is_dir():
        raise HTTPException(404, f"Model folder '{path_name}' not found in backend.")

    # List all OBJ + MTL files inside folder
    obj_files = list(folder.glob("*.obj"))
    mtl_files = {f.stem: f for f in folder.glob("*.mtl")}  # map: filename → file

    if not obj_files:
        raise HTTPException(404, "No OBJ files found in the folder.")

    rendering_elements = []

    for obj_path in obj_files:
        filename = obj_path.name
        base = obj_path.stem  # e.g. 'liver2_1'

        # Read .obj content
        obj_content = obj_path.read_text()

        # Find matching .mtl
        mtl_content = ""
        if base in mtl_files:
            mtl_content = mtl_files[base].read_text()

        rendering_elements.append({
            "filename": filename,
            "objContent": obj_content,
            "mtlContent": mtl_content
        })

    return {"renderingElements": rendering_elements}
