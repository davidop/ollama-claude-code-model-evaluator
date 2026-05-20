$ErrorActionPreference = "Stop"

$ollamaBaseUrl = if ($env:OLLAMA_BASE_URL) { $env:OLLAMA_BASE_URL } else { "http://localhost:11434" }

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
	Write-Host "ERROR: python not found. Install Python 3.10+ and try again." -ForegroundColor Red
	exit 1
}

python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) {
	Write-Host "ERROR: Python 3.10+ is required." -ForegroundColor Red
	python --version
	exit 1
}

try {
	Invoke-WebRequest -Uri "$ollamaBaseUrl/api/tags" -UseBasicParsing | Out-Null
} catch {
	Write-Host "ERROR: Cannot reach Ollama at $ollamaBaseUrl" -ForegroundColor Red
	Write-Host "Start Ollama in another terminal, for example: ollama serve" -ForegroundColor Yellow
	exit 1
}

New-Item -ItemType Directory -Path .\results -Force | Out-Null
python .\eval_ollama_models.py --pull --num-ctx 8192 --output .\results\benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b

if (-not (Test-Path .\results\benchmark-standard.json)) {
	Write-Host "ERROR: Benchmark completed without creating results/benchmark-standard.json" -ForegroundColor Red
	exit 1
}

python .\gen_dashboard.py --standard .\results\benchmark-standard.json --base-url $ollamaBaseUrl
Write-Host "Dashboard data generated at results/dashboard-data.js" -ForegroundColor Green
