#!/usr/bin/env python3
from pypdf import PdfReader
from pathlib import Path
import re
import sys


def limpiar_texto(texto: str) -> str:
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()


def pdf_a_md(pdf_path: str, md_path: str) -> None:
    ruta_pdf = Path(pdf_path)

    if not ruta_pdf.exists():
        print(f"Error: no existe el archivo {pdf_path}", file=sys.stderr)
        sys.exit(1)

    reader = PdfReader(ruta_pdf)
    texto_completo = ""

    for pagina in reader.pages:
        texto = pagina.extract_text() or ""
        texto_completo += texto + "\n\n"

    texto_completo = limpiar_texto(texto_completo)

    Path(md_path).write_text(texto_completo, encoding="utf-8")

    print(f"✅ Markdown generado correctamente: {md_path}")


if __name__ == "__main__":
    pdf_a_md("micurriculum.pdf", "micurriculum.md")

