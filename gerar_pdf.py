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

# O HTML do nbconvert mantém os blocos de código em uma única linha visual.
# Na impressão em PDF isso pode fazer o fim das linhas sair da página. Este
# estilo limita os elementos à largura imprimível e permite a quebra visual.
conteudo_html = html.read_text(encoding="utf-8")
estilo_impressao = """
<style>
@page {
    size: A4;
    margin: 12mm;
}
@media print {
    pre,
    code,
    .highlight pre,
    .jp-InputArea-editor pre {
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }

    .highlight,
    .input_area,
    .jp-InputArea,
    .jp-InputArea-editor,
    .jp-CodeCell,
    .jp-Cell {
        box-sizing: border-box !important;
        max-width: 100% !important;
        overflow: visible !important;
    }

    table {
        max-width: 100% !important;
    }
}
</style>
"""
conteudo_html = conteudo_html.replace("</head>", f"{estilo_impressao}</head>", 1)
html.write_text(conteudo_html, encoding="utf-8")

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
