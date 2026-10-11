$ErrorActionPreference = "Stop"

uv run --with pip --with jupyter --with nbconvert --with line-solver --with pandas --with matplotlib python gerar_pdf.py
