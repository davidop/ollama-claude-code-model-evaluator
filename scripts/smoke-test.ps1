$ErrorActionPreference = "Stop"

$ollamaBaseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://localhost:11434" }

Write-Host "[1/6] Checking Python"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: python not found. Install Python 3.10+ and retry." -ForegroundColor Red
    exit 1
}

python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.10+ required." -ForegroundColor Red
    python --version
    exit 1
}

Write-Host "[2/6] Checking Ollama endpoint ($ollamaBaseUrl)"
try {
    Invoke-WebRequest -Uri "$ollamaBaseUrl/api/tags" -UseBasicParsing | Out-Null
} catch {
    Write-Host "ERROR: Ollama is not reachable at $ollamaBaseUrl" -ForegroundColor Red
    Write-Host "Start Ollama in another terminal: ollama serve" -ForegroundColor Yellow
    exit 1
}

Write-Host "[3/6] Checking required files"
$requiredFiles = @(
    "eval_ollama_models.py",
    "gen_dashboard.py",
    "hwdetect.py",
    "dashboard.html"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "ERROR: Missing required file: $file" -ForegroundColor Red
        exit 1
    }
    Write-Host "  OK: $file"
}

Write-Host "[4/6] Compiling Python scripts"
python -m py_compile eval_ollama_models.py gen_dashboard.py hwdetect.py scripts/validate-benchmark-json.py
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "[5/6] Validating benchmark JSON"
python scripts/validate-benchmark-json.py
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "[6/6] Ensuring dashboard data file exists"
if (-not (Test-Path .\results\dashboard-data.js)) {
    python .\gen_dashboard.py --standard .\results\benchmark-standard.json --base-url $ollamaBaseUrl
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if (-not (Test-Path .\results\dashboard-data.js)) {
    Write-Host "ERROR: results/dashboard-data.js was not generated" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Smoke test passed." -ForegroundColor Green
Write-Host "Open dashboard: $PWD\dashboard.html"
