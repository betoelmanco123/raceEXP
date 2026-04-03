# Race (uv + pygame)

## Ejecutar sin errores de imports

Este proyecto usa `uv` y el entorno virtual local `.venv`.

Comando recomendado:

```bash
uv run python runner.py
```

Si quieres usar `python` directo en la terminal:

```bash
source .venv/bin/activate
python runner.py
```

Si ejecutas `python3 runner.py` sin activar `.venv`, usaras el Python global y pueden fallar imports como `pygame`.
