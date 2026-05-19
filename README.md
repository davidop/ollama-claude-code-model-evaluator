# Ollama Claude Code Model Evaluator

Repositorio mínimo para evaluar qué modelo local de Ollama funciona mejor para tareas de desarrollo y uso con Claude Code.

El benchmark mide:

- Velocidad media en tokens/segundo.
- Latencia media.
- Calidad aproximada mediante tests de código.
- Modelo ganador recomendado para usar con Claude Code.

> El script no usa dependencias externas de Python. Funciona con la librería estándar.

## Requisitos

- Python 3.10 o superior.
- Ollama instalado.
- Uno o varios modelos locales en Ollama, o usar `--pull` para descargarlos.

## DevContainer (recomendado si tienes problemas con Python en Windows)

Este repo incluye `/.devcontainer/devcontainer.json` para abrirlo con Python ya listo dentro de un contenedor.

1. Instala Docker Desktop y la extension `Dev Containers` en VS Code.
2. Con Ollama activo en tu host (`ollama serve`), abre el comando:
   - `Dev Containers: Reopen in Container`
3. Dentro del contenedor, ejecuta el benchmark normalmente:

```bash
python eval_ollama_models.py --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
```

Nota: el DevContainer usa `OLLAMA_BASE_URL=http://host.docker.internal:11434` para conectarse al Ollama que corre en tu maquina host.

## Instalación rápida

```bash
ollama serve
```

En otra terminal:

```bash
python eval_ollama_models.py --pull --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
```

## Benchmark estándar para publicar resultados

Si quieres una corrida útil para compartir en GitHub sin tardar horas, usa 3 modelos.

Windows PowerShell:

```powershell
python .\eval_ollama_models.py --pull --num-ctx 8192 --output .\results\benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
```

Linux/macOS:

```bash
python eval_ollama_models.py --pull --num-ctx 8192 --output ./results/benchmark-standard.json --models qwen2.5-coder:3b qwen2.5-coder:7b deepseek-coder:6.7b
```

Atajo con scripts incluidos:

- Windows: `scripts/run-basic.ps1`
- Linux/macOS: `scripts/run-basic.sh`

El archivo de salida recomendado para publicar es `results/benchmark-standard.json`.

## Uso básico

Evaluar modelos ya instalados:

```bash
python eval_ollama_models.py --models qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
```

Descargar modelos faltantes y evaluarlos:

```bash
python eval_ollama_models.py --pull --models qwen2.5-coder:3b qwen2.5-coder:7b
```

Usar más contexto:

```bash
python eval_ollama_models.py --pull --num-ctx 16384 --models qwen2.5-coder:7b qwen2.5-coder:14b
```

Guardar resultados en otro fichero:

```bash
python eval_ollama_models.py --output results.json --models qwen2.5-coder:7b
```

## Recomendaciones por hardware

| Hardware aproximado | Modelos a probar                          |
| ------------------- | ----------------------------------------- |
| CPU / 16 GB RAM     | `qwen2.5-coder:3b`, `qwen2.5-coder:7b`    |
| NVIDIA 8 GB VRAM    | `qwen2.5-coder:7b`, `deepseek-coder:6.7b` |
| NVIDIA 12 GB VRAM   | `qwen2.5-coder:7b`, `qwen2.5-coder:14b`   |
| NVIDIA 16 GB VRAM   | `qwen2.5-coder:14b`                       |
| NVIDIA 24 GB VRAM   | `qwen2.5-coder:32b`                       |

## Ejecutar desde el móvil contra el PC

El modelo corre en el PC. El móvil solo ejecuta el script y llama a la API de Ollama por red local.

### En el PC

Linux/macOS:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Windows PowerShell:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

Obtén la IP local del PC.

Windows:

```powershell
ipconfig
```

Linux/macOS:

```bash
ip addr
```

### En Android con Termux

```bash
pkg update
pkg install python
python eval_ollama_models.py --base-url http://192.168.1.50:11434 --models qwen2.5-coder:7b deepseek-coder:6.7b codellama:7b
```

Cambia `192.168.1.50` por la IP real de tu PC.

## Usar el modelo ganador con Claude Code

El script imprime un comando similar a este:

```bash
ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" ANTHROPIC_BASE_URL=http://localhost:11434 claude --model qwen2.5-coder:7b
```

En Linux/macOS puedes exportarlo así:

```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_BASE_URL=http://localhost:11434
claude --model qwen2.5-coder:7b
```

En Windows PowerShell:

```powershell
$env:ANTHROPIC_AUTH_TOKEN="ollama"
$env:ANTHROPIC_API_KEY=""
$env:ANTHROPIC_BASE_URL="http://localhost:11434"
claude --model qwen2.5-coder:7b
```

## Checklist de publicación en GitHub

Antes de anunciar el repo:

1. Ejecuta el benchmark estándar y confirma que existe `results/benchmark-standard.json`.
2. Copia al README un resumen corto con modelo ganador, score y tokens/s.
3. Verifica que CI pase en GitHub Actions (`Validate`).
4. Abre al menos un issue de roadmap para mostrar dirección del proyecto.
5. Publica release inicial (`v0.1.0`) con enlace al resultado JSON.

## Nota sobre la puntuación

La puntuación no pretende sustituir a un benchmark académico. Está pensada para una decisión práctica: qué modelo local es más útil para tareas de código en tu propia máquina.

La fórmula actual pondera:

- 65% calidad aproximada.
- 35% velocidad, normalizada contra 40 tokens/s.

Puedes modificar los tests en la constante `TESTS` del script.
