"""Build the GitHub Pages catalog from CATALOG.md and its tracked files."""
import argparse
import hashlib
import json
import re
import shutil
from collections import defaultdict
from html import escape
from string import Template
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = {
    "stickers": "Stickers",
    "t-shirts": "Playeras",
    "totebags": "Totebags",
    "caps": "Gorras",
    "merch": "Otro merch",
    "posters": "Pósters",
    "flyers": "Flyers",
    "social-media": "Redes sociales",
    "signage": "Señalética",
    "packaging": "Empaque",
    "facade": "Fachada",
    "illustrations": "Ilustraciones",
    "logo": "Logos",
    "references": "Fotos y referencias",
    "other": "Otros recursos",
}
LINK = re.compile(r"\[(.+)\]\(([^)]+)\)")
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
# These older identifiers name a series that contains distinct compositions.
SERIES_IDS = {"facade", "facade-sheet", "giraffe-at-workbench", "support-local-guitar-shop"}
GROUP_TITLES = {
    "puro-bujia-cartoon": "Puro Bujía",
    "dtf-shirt-chest": "Playera · solapa DTF",
    "dtf-shirt-back": "Playera · espalda DTF",
    "dtf-tote-facade": "Totebag · fachada DTF",
}
# Early cream DTF links were shared with dots in the version number.
SHARED_LINK_STEMS = {
    "dtf-shirt-chest-v1.2.0-cream-wordmark",
    "dtf-shirt-back-v1.2.0-cream-wordmark",
}


def repository_path(value):
    path = (ROOT / value).resolve(strict=True)
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f"Ruta de catálogo inválida: {value}")
    return path


def category_for(category):
    if category in CATEGORIES:
        return category
    if category in {"photography", "punk"}:
        return "references"
    if category in {"scenes", "characters", "objects", "graphic-elements", "textures"}:
        return "illustrations"
    return "other"


def image_metadata(image, output):
    if image.suffix.lower() not in IMAGE_TYPES:
        return None, None
    name = hashlib.sha256(str(image.relative_to(ROOT)).encode()).hexdigest()[:20] + ".webp"
    with Image.open(image) as source:
        oriented = ImageOps.exif_transpose(source)
        width, height = oriented.size
        metadata = f"{width} × {height} px"
        dpi = source.info.get("dpi")
        if dpi and round(dpi[0]) == round(dpi[1]):
            metadata += f" · {round(dpi[0])} ppp"
        preview = oriented.convert("RGBA")
        preview.thumbnail((560, 560), Image.Resampling.LANCZOS)
        preview.save(output / "thumbs" / name, quality=82, method=4)
    return f"thumbs/{name}", metadata


def file_size(path):
    size = path.stat().st_size
    if size >= 1024**2:
        return f"{size / 1024**2:.1f} MiB"
    return f"{size / 1024:.1f} KiB"


def prepare_resource(asset, item, output):
    asset_key = str(asset.relative_to(ROOT))
    suffix = hashlib.sha256(asset_key.encode()).hexdigest()[:10]
    slug = re.sub(r"[^a-z0-9-]+", "-", asset.stem.lower()).strip("-")
    folder = f"resources/{slug}-{suffix}"
    directory = output / folder
    directory.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(asset, directory / asset.name)
    item["file"] = folder + "/" + quote(asset.name)
    item["page"] = folder + "/"
    item["thumbnail"], item["dimensions"] = image_metadata(asset, output)
    item["size"] = file_size(asset)
    if asset.stem in SHARED_LINK_STEMS:
        alias = output / "resources" / f"{asset.stem}-{suffix}"
        alias.mkdir()
        target = "../" + Path(folder).name + "/"
        (alias / "index.html").write_text(
            '<!doctype html><html lang="es"><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={target}">'
            f'<link rel="canonical" href="{target}"><title>Ficha de Bujía</title>'
            f'<a href="{target}">Abrir ficha</a></html>',
            encoding="utf-8",
        )


def preview_for(item):
    if not item["thumbnail"]:
        return f'<span>{escape(item["format"])}</span>'
    return f'<img src="../../{escape(item["thumbnail"])}" alt="{escape(item["title"])}">'


def versions_for(versions, current):
    if len(versions) == 1:
        return ""
    cards = []
    for version in versions:
        uri = "../../" + escape(version["page"])
        file = "../../" + escape(version["file"])
        title = escape(version["title"])
        selected = ' aria-current="page"' if version is current else ""
        cards.append(
            f'<article class="card"><a class="preview" href="{uri}"{selected} aria-label="Ver {title}">'
            f'{preview_for(version)}</a><div class="details">'
            f'<div class="meta"><span class="version">v{escape(version["version"])}</span></div>'
            f'<h3><a href="{uri}"{selected}>{title}</a></h3>'
            f'<div class="links"><a class="action" href="{file}" download>Descargar</a>'
            f'<button class="action" type="button" data-share="{uri}" data-share-title="{title}">Compartir</button>'
            f'</div></div></article>'
        )
    return (
        '<section class="resource-versions" aria-labelledby="versions-heading">'
        f'<h2 id="versions-heading">Versiones de {escape(current["groupTitle"])} ({len(versions)})</h2>'
        f'<div class="grid">{"".join(cards)}</div></section>'
    )


def resource_page(item, versions, output, template):
    dimensions = item["dimensions"]
    html = template.substitute(
        title=escape(item["title"]),
        description=escape(item["description"]),
        category=escape(item["categoryLabel"]),
        version=escape(item["version"]),
        format=escape(item["format"]),
        size=item["size"],
        dimensions=f"<dt>Resolución</dt><dd>{escape(dimensions)}</dd>" if dimensions else "",
        file=item["file"].rsplit("/", 1)[-1],
        preview=preview_for(item),
        versions=versions_for(versions, item),
    )
    (output / item["page"] / "index.html").write_text(html, encoding="utf-8")


def group_for(item, asset, card):
    identifier = item["id"]
    if identifier not in SERIES_IDS:
        return item["category"], identifier
    origin = re.search(r"^- Origen: \[[^\]]+\]\(([^)]+)\)", card.read_text(encoding="utf-8"), re.M)
    stem = Path(origin[1]).stem if origin else asset.stem
    return item["category"], identifier, re.sub(r"-v[0-9]+\.[0-9]+\.[0-9]+", "", stem)


def representative_key(item):
    return bool(item["thumbnail"]), tuple(int(part) for part in item["version"].split(".")), item["page"]


def groups_for(output):
    groups = defaultdict(list)
    for number, line in enumerate((ROOT / "CATALOG.md").read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) != 10:
            raise ValueError(f"CATALOG.md:{number}: se esperaban 10 columnas")
        identifier, name, category, _, version, _, file, status, _, description = cells
        if status.strip("`") != "approved":
            continue
        title_link = LINK.fullmatch(name)
        file_link = LINK.fullmatch(file)
        if not title_link or not file_link:
            raise ValueError(f"CATALOG.md:{number}: faltan enlaces de ficha o archivo")
        title, card_path = title_link.groups()
        format_name, asset_path = file_link.groups()
        asset = repository_path(asset_path)
        card = repository_path(card_path)
        key = category_for(category.strip("`"))
        item = {
            "id": identifier.strip("`"), "title": title,
            "category": key, "categoryLabel": CATEGORIES[key],
            "version": version.strip("`"),
            "description": description.replace(r"\|", "|"),
            "format": format_name,
        }
        prepare_resource(asset, item, output)
        groups[group_for(item, asset, card)].append(item)
    return groups


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError(f"Usa un directorio nuevo para generar el sitio: {output}")
    (output / "thumbs").mkdir()
    for name in ("index.html", "catalog.css", "catalog.js", "share.js"):
        shutil.copyfile(ROOT / "site" / name, output / name)
    logo = repository_path("masters/logo/bujia-oval-logo-v1.0.0-red-cream.png")
    with Image.open(logo) as source:
        stamp = source.convert("RGBA")
        stamp = stamp.crop(stamp.getbbox())
        stamp.thumbnail((216, 98), Image.Resampling.LANCZOS)
        stamp.save(output / "logo.png")
    groups = groups_for(output)
    template = Template((ROOT / "site" / "resource.html").read_text(encoding="utf-8"))
    items = []
    for versions in groups.values():
        versions.sort(key=representative_key, reverse=True)
        group_title = GROUP_TITLES.get(versions[0]["id"], versions[0]["title"])
        for item in versions:
            item["groupTitle"] = group_title
            resource_page(item, versions, output, template)
        search_terms = " ".join(f'{item["title"]} {item["description"]} {item["version"]}' for item in versions)
        items.append(dict(versions[0], versionCount=len(versions), searchTerms=search_terms))
    items.sort(key=lambda item: item["groupTitle"].casefold())
    used = {item["category"] for item in items}
    data = {"categories": [(key, label) for key, label in CATEGORIES.items() if key in used], "items": items}
    (output / "catalog-data.js").write_text(
        "window.catalog = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8"
    )
    print(f"{len(items)} recursos y {sum(item['versionCount'] for item in items)} versiones en el catálogo")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build(parser.parse_args().output)
