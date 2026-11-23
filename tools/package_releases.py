from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
RELEASES = ROOT / "release" / "itchio"
WINDOWS = ROOT / "builds" / "windows" / "Da Rua ao Estrelado.exe"
WEB = ROOT / "builds" / "web"
SOURCE_ITEMS = ["assets", "docs", "scenes", "scripts", "tools", "project.godot", "export_presets.cfg", "README.md"]


def put_text(path: Path, text: str):
    path.write_text(text.strip() + "\n", encoding="utf-8")


def make_windows():
    if not WINDOWS.exists():
        raise FileNotFoundError(WINDOWS)
    readme = RELEASES / "README-Windows.txt"
    put_text(readme, """
    DA RUA AO ESTRELADO — WINDOWS

    Extraia o conteúdo deste ZIP e execute “Da Rua ao Estrelado.exe”.
    Controles: A/D ou setas para mover; Espaço/W/↑ para pular; J cabeçada;
    K carrinho; L chute; P ou Esc pausa; Enter inicia/continua; R reinicia na pausa.
    Jogo de plataforma 2D individual. Projeto acadêmico — Godot 4.7.2.
    """)
    out = RELEASES / "Da-Rua-ao-Estrelado-Windows.zip"
    with ZipFile(out, "w", ZIP_DEFLATED, compresslevel=6) as z:
        z.write(WINDOWS, WINDOWS.name)
        z.write(readme, readme.name)
    return out


def make_web():
    required = [WEB / "index.html", WEB / "index.js", WEB / "index.wasm", WEB / "index.pck"]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)
    readme = WEB / "README-itchio.txt"
    put_text(readme, """
    DA RUA AO ESTRELADO — WEB

    Projeto HTML5 exportado no modo Web do Godot 4.7.2, sem threads.
    Para publicar no itch.io, envie este conteúdo como projeto HTML jogável.
    O arquivo index.html precisa permanecer junto aos arquivos de dados.
    Controles: A/D ou setas; Espaço/W/↑; J; K; L; P/Esc; Enter; R na pausa.
    """)
    out = RELEASES / "Da-Rua-ao-Estrelado-Web.zip"
    with ZipFile(out, "w", ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(WEB.iterdir()):
            if path.is_file() and path.name != "README-itchio.txt":
                z.write(path, path.name)
        z.write(readme, readme.name)
    return out


def make_source():
    out = RELEASES / "Projeto-fonte-Da-Rua-ao-Estrelado.zip"
    with ZipFile(out, "w", ZIP_DEFLATED, compresslevel=6) as z:
        for item in SOURCE_ITEMS:
            path = ROOT / item
            if path.is_dir():
                for child in sorted(path.rglob("*")):
                    if child.is_file() and ".godot" not in child.parts and "__pycache__" not in child.parts:
                        z.write(child, child.relative_to(ROOT))
            elif path.is_file():
                z.write(path, path.relative_to(ROOT))
    return out


if __name__ == "__main__":
    RELEASES.mkdir(parents=True, exist_ok=True)
    for archive in (make_windows(), make_web(), make_source()):
        print(f"{archive} ({archive.stat().st_size:,} bytes)")
