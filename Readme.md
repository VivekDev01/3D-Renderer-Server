# Sample
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3141e9ea-5834-43cf-99f8-e2ff6952ba40" />


# 0. Create .env file
```bash
ALLOWED_ORIGIN1=<Your Local Host>
ALLOWED_ORIGIN2=<Your Production Host>
```

# 1. Create 3d-models folder
```bash
mkdir 3d-models
```

# 2. Make subfolders inside 3d-models folder and put all .obj and .mtl files inside them
```bash
mkdir 3d-models/liver
mkdir 3d-models/heart
mkdir 3d-models/kidney
mkdir 3d-models/lung
mkdir 3d-models/stomach
```

# 3. Create Virtual Environment
```bash
python -m venv venv
```

# 4. Activate Virtual Environment
```bash
venv\Scripts\activate
```

# 5. Install Dependencies
```bash
pip install -r requirements.txt
```

# 6. Run the Server
```bash
uvicorn main:app --reload --port 5000
```
