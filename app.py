from pathlib import Path

from flask import Flask, abort, render_template, send_from_directory
from markupsafe import Markup
from jx import Catalog


app = Flask(__name__)

DISPLAY_DIR = Path(__file__).parent / "display"


def build_catalog() -> Catalog:
    return Catalog(str(DISPLAY_DIR), auto_reload=True)


def resolve_asset_url(url: str, folder: str) -> str:
    """Rewrite relative asset URLs to /<folder>/<url>."""
    if url.startswith(("/", "http://", "https://")):
        return url
    if folder:
        return f"/{folder}/{url}"
    return f"/{url}"


def collect_assets(catalog: Catalog, relpath: str) -> tuple[Markup, Markup]:
    """Walk the component import tree, resolving asset URLs per component folder."""
    css_urls: list[str] = []
    js_urls: list[str] = []
    visited: set[str] = set()

    def _walk(rp: str) -> None:
        if rp in visited:
            return
        visited.add(rp)
        co = catalog.get_component(rp)
        folder = rp.rsplit("/", 1)[0] if "/" in rp else ""
        for url in co.css:
            resolved = resolve_asset_url(url, folder)
            if resolved not in css_urls:
                css_urls.append(resolved)
        for url in co.js:
            resolved = resolve_asset_url(url, folder)
            if resolved not in js_urls:
                js_urls.append(resolved)
        for imp_relpath in co.imports.values():
            _walk(imp_relpath)

    _walk(relpath)

    css = Markup("\n".join(f'<link rel="stylesheet" href="{u}">' for u in css_urls))
    js = Markup("\n".join(f'<script type="module" src="{u}"></script>' for u in js_urls))
    return css, js


def discover_components() -> list[tuple[str, str]]:
    """Return (display_name, url_path) pairs for all .jinja files."""
    components = []
    for jinja_file in sorted(DISPLAY_DIR.rglob("*.jinja")):
        rel = jinja_file.relative_to(DISPLAY_DIR)
        url_path = "/" + str(rel.with_suffix(""))
        components.append((str(rel), url_path))
    return components


@app.route("/")
def index():
    components = discover_components()
    links = "\n".join(
        f'<li><a href="{url}" class="text-blue-600 hover:underline">{name}</a></li>'
        for name, url in components
    )
    content = f"""\
<div class="max-w-2xl mx-auto py-12 px-4">
  <h1 class="text-3xl font-bold mb-8">Jx Component Viewer</h1>
  <ul class="space-y-2 list-disc list-inside">
{links}
  </ul>
</div>"""
    return render_template(
        "wrapper.html", title="Jx Component Viewer", css="", js="", content=content
    )


@app.route("/<path:path>")
def view_component(path):
    # Serve static files from display subfolders directly.
    file_path = DISPLAY_DIR / path
    if file_path.is_file() and not path.endswith(".jinja"):
        return send_from_directory(file_path.parent, file_path.name)

    relpath = f"{path}.jinja"
    catalog = build_catalog()

    try:
        catalog.get_component(relpath)
    except Exception:
        abort(404)

    css, js = collect_assets(catalog, relpath)
    html = catalog.render(relpath)

    return render_template("wrapper.html", title=path, css=css, js=js, content=html)
