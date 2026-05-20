New-Item -ItemType Directory -Path .\results -Force | Out-Null
python .\eval_ollama_models.py --pull --num-ctx 8192 --output .\results\benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
python .\gen_dashboard.py --standard .\results\benchmark-standard.json
Write-Host "Dashboard data generated at results/dashboard-data.js"
