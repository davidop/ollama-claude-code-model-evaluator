# Contributing

Gracias por contribuir a Ollama Claude Code Model Evaluator.

## Requisitos locales

- Python 3.10 o superior
- Ollama instalado y ejecutandose en local

## Flujo recomendado

1. Crea una rama desde main.
2. Ejecuta una validacion minima local:
   - python -m py_compile eval_ollama_models.py
   - python eval_ollama_models.py --help
3. Si tu cambio toca benchmark, ejecuta al menos una corrida corta:
   - python eval_ollama_models.py --models qwen2.5-coder:3b
4. Abre PR con descripcion clara del problema y resultado esperado.

## Como agregar un nuevo test de benchmark

1. Edita la constante TESTS en eval_ollama_models.py.
2. Agrega:
   - name unico
   - prompt enfocado
   - keywords verificables
3. Mantener prompts cortos y deterministicos para facilitar comparacion.

## Convenciones

- Mantener compatibilidad con Python stdlib (sin dependencias externas).
- Evitar cambios grandes no relacionados al objetivo del PR.
- Documentar en README cualquier flag nuevo del CLI.

## Reporte de bugs

Abre un issue con:

- Comando exacto ejecutado
- Sistema operativo
- Version de Python
- Error completo
- Si Ollama estaba corriendo en localhost:11434
