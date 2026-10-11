from pathlib import Path
import os
import subprocess
import sys


notebook = Path("Atividade_Capitulo_6.ipynb").resolve()
executado = notebook.with_name(f"{notebook.stem}_executado.ipynb")
pdf = notebook.with_suffix(".pdf")
html = notebook.with_suffix(".html")

if not notebook.exists():
    raise FileNotFoundError(f"Notebook não encontrado: {notebook}")

subprocess.run(
    [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        str(notebook),
        "--to",
        "notebook",
        "--execute",
        "--ExecutePreprocessor.timeout=1200",
        "--output",
        executado.name,
    ],
    check=True,
    cwd=notebook.parent,
)

subprocess.run(
    [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        str(executado),
        "--to",
        "html",
        "--output",
        html.name,
    ],
    check=True,
    cwd=notebook.parent,
)

pastas = [
    Path(os.environ.get("PROGRAMFILES", "")) / "Microsoft/Edge/Application/msedge.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft/Edge/Application/msedge.exe",
    Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
]

navegadores_playwright = sorted(
    (Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright").glob(
        "chromium_headless_shell-*/chrome-headless-shell-win64/headless_shell.exe"
    ),
    reverse=True,
)
navegador = next((caminho for caminho in pastas + navegadores_playwright if caminho.exists()), None)

if navegador is None:
    raise FileNotFoundError("Edge ou Chrome não foi encontrado")

subprocess.run(
    [
        str(navegador),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=15000",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    ],
    check=True,
)

html.unlink()

print(f"Notebook executado: {executado}")
print(f"PDF gerado: {pdf}")
