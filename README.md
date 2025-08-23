
# 5CNP — Run Guide (Windows)

## Prereqs
- Python 3.11+
- Node 18/20+
- PowerShell
- (Optional) Docker Desktop

## 1) Backend: create venv, install, seed DB, run
```powershell
cd .\backend
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python .\data\generate_dataset.py
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Now your API is at http://127.0.0.1:8000 (test http://127.0.0.1:8000/health).

## 2) Frontend: install and run
Open a new terminal:
```powershell
cd .\frontend
npm install
npm run dev
```
Visit http://localhost:5173

### Configure API base (optional)
Create `frontend/.env` with:
```
VITE_API_BASE=http://127.0.0.1:8000
```

## Troubleshooting
- Port busy (8000/5173): pick another port or stop existing server.
- CORS: allowed for all origins in `app.main`.
- LLM: `/interrupt` returns a stubbed reply until you wire your Agno/OpenAI keys.

## Optional: Docker
```powershell
cd backend
docker build -t dhushy63ai-backend .
docker run -p 8000:8000 dhushy63ai-backend
```
Then run the frontend as usual.
