#!/usr/bin/env python3
import pathlib
import sys
import requests
from textwrap import dedent


def construir_prompt(contenido_md: str) -> str:
    return dedent(
        f"""
        Eres un experto en selección de personal y redacción de perfiles profesionales.

        Recibirás un currículum en formato Markdown.

        Tu tarea:
        - Escribir un resumen profesional en tercera persona.
        - Extensión: 7–10 líneas (máx. 200 palabras).
        - Estilo profesional y claro.
        - Sintetizar la información, no copiar listas.

        Además:
        - Evalúa si el perfil es válido para el puesto:
          profesor de ciclos formativos de formación profesional.
        - Da un veredicto: VÁLIDO / NO VÁLIDO / INCONCLUYENTE.
        - Justifica en 3–5 puntos.

        Formato obligatorio:
        1) Resumen
        2) Veredicto
        3) Motivos

        CV:
        ---
        {contenido_md}
        ---
        """
    ).strip()


def resumir_cv(ruta_md: str) -> str:
    ruta = pathlib.Path(ruta_md)

    if not ruta.exists():
        print(f"Error: no existe el archivo {ruta_md}", file=sys.stderr)
        sys.exit(1)

    contenido_md = ruta.read_text(encoding="utf-8", errors="replace")

    prompt = construir_prompt(contenido_md)

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=600)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Ollama: {e}", file=sys.stderr)
        sys.exit(1)

    data = response.json()

    if "response" not in data:
        print("Respuesta inesperada de Ollama:", file=sys.stderr)
        print(data, file=sys.stderr)
        sys.exit(1)

    return data["response"].strip()


if __name__ == "__main__":
    resultado = resumir_cv("micurriculum.md")

    pathlib.Path("resumen_micurriculum.txt").write_text(
        resultado,
        encoding="utf-8"
    )

    print("✅ Resumen generado: resumen_micurriculum.txt")

