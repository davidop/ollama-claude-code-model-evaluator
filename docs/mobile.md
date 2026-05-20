# Ejecutar el benchmark desde el móvil

## Android / Termux

```bash
pkg update
pkg install python
python eval_ollama_models.py --base-url http://IP_DE_TU_PC:11434 --models qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
```

## PC exponiendo Ollama en red local

Linux/macOS:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Windows PowerShell:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

Asegúrate de que el firewall permite conexiones al puerto `11434` desde tu red local.
