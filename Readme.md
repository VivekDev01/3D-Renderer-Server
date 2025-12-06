# 1. Create Virtual Environment
```bash
python -m venv venv
```

# 2. Activate Virtual Environment
```bash
venv\Scripts\activate
```

# 3. Install Dependencies
```bash
pip install -r requirements.txt
```

# 4. Run the Server
```bash
uvicorn main:app --reload --port 5000
```
