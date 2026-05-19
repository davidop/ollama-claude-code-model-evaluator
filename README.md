# Ollama Claude Code Model Evaluator

[![Validate](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml/badge.svg)](https://github.com/davidop/ollama-claude-code-model-evaluator/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/runtime-Ollama-black.svg)](https://ollama.com/)

Idioma:

- Espanol: [README.md](README.md)
- English: [README.en.md](README.en.md)

Repositorio mínimo para evaluar qué modelo local de Ollama funciona mejor para tareas de desarrollo y uso con Claude Code.

Compara calidad y velocidad en tu propio hardware, publica resultados reproducibles y usa el modelo ganador con Claude Code en un solo comando.

Enlaces rapidos:

- Dashboard interactivo: [dashboard.html](dashboard.html)
- Benchmark estandar (JSON): [results/benchmark-standard.json](results/benchmark-standard.json)
- Benchmark con contexto 16384 + 14b (JSON): [results/benchmark-ctx16384-plus14b.json](results/benchmark-ctx16384-plus14b.json)

Vista previa del dashboard:

![Dashboard preview](docs/assets/dashboard-preview.svg)

## Por que importa

- Menor costo: puedes elegir modelo local antes de gastar en APIs cloud.
- Mayor privacidad: codigo y prompts se quedan en tu equipo.
- Mejor ajuste real: decides segun tu hardware, no solo por rankings genericos.

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

## Resultados recientes (este PC)

Los siguientes resultados se generaron en este repositorio con los comandos estandar documentados.

### Benchmark estandar (num_ctx=8192)

| Rank | Modelo | Score | Quality | Tokens/s | Latencia (s) | Passed |
| ---- | ------ | ----- | ------- | -------- | ------------ | ------ |
| 1 | qwen2.5-coder:3b | 0.428 | 0.530 | 9.49 | 28.49 | 1/4 |
| 2 | qwen2.5-coder:7b | 0.406 | 0.573 | 3.86 | 53.15 | 1/4 |
| 3 | deepseek-coder:6.7b | 0.308 | 0.430 | 3.31 | 117.90 | 1/4 |

Ganador estandar para este equipo: **qwen2.5-coder:3b**.

### Benchmark calidad (num_ctx=16384, incluye 14b)

| Rank | Modelo | Score | Quality | Tokens/s | Latencia (s) | Passed |
| ---- | ------ | ----- | ------- | -------- | ------------ | ------ |
| 1 | qwen2.5-coder:14b | 0.441 | 0.660 | 1.41 | 135.42 | 2/4 |
| 2 | qwen2.5-coder:3b | 0.379 | 0.480 | 7.65 | 41.13 | 1/4 |
| 3 | qwen2.5-coder:7b | 0.371 | 0.522 | 3.55 | 94.89 | 1/4 |
| 4 | deepseek-coder:6.7b | 0.307 | 0.430 | 3.16 | 141.75 | 1/4 |

Ganador por calidad en este equipo: **qwen2.5-coder:14b**.

Lectura rapida:

- Si priorizas velocidad y latencia: usa qwen2.5-coder:3b.
- Si priorizas calidad final para Claude Code: usa qwen2.5-coder:14b.

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

Activos listos para publicar:

- Notas de release v0.1.0: [docs/release/v0.1.0-release-notes.md](docs/release/v0.1.0-release-notes.md)
- Roadmap 01 (alcance global): [docs/release/roadmap-01-english-readme-and-global-distribution.md](docs/release/roadmap-01-english-readme-and-global-distribution.md)
- Roadmap 02 (expansion benchmark): [docs/release/roadmap-02-benchmark-suite-expansion.md](docs/release/roadmap-02-benchmark-suite-expansion.md)
- Roadmap 03 (dashboard y assets): [docs/release/roadmap-03-dashboard-and-sharing-assets.md](docs/release/roadmap-03-dashboard-and-sharing-assets.md)
- Roadmap 04 (guardrails CI): [docs/release/roadmap-04-ci-and-quality-guardrails.md](docs/release/roadmap-04-ci-and-quality-guardrails.md)
- Launch pack para redes: [docs/release/launch-pack.md](docs/release/launch-pack.md)
- Checklist automatizado de release: [scripts/release-check.sh](scripts/release-check.sh)
- Guia operativa de publicacion v0.1.0: [docs/release/publish-v0.1.0.md](docs/release/publish-v0.1.0.md)

## Nota sobre la puntuación

La puntuación no pretende sustituir a un benchmark académico. Está pensada para una decisión práctica: qué modelo local es más útil para tareas de código en tu propia máquina.

La fórmula actual pondera:

- 65% calidad aproximada.
- 35% velocidad, normalizada contra 40 tokens/s.

Puedes modificar los tests en la constante `TESTS` del script.
