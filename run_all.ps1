
# One-shot helper (PowerShell): backend + frontend
$ErrorActionPreference = "Stop"

# --- Backend ---
Push-Location "$PSScriptRoot\backend"
if (!(Test-Path ".venv")) { python -m venv .venv }
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\data\generate_dataset.py
Start-Process powershell -ArgumentList "-NoExit","-Command","cd `"$PWD`"; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 127.0.0.1 --port 8000"

Pop-Location

# --- Frontend ---
Push-Location "$PSScriptRoot\frontend"
npm install
npm run dev
Pop-Location
