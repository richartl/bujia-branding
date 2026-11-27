"""Build the GitHub Pages catalog from CATALOG.md and its tracked files."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/richartl/bujia-branding/blob/main/"
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


def thumbnail(image, output):
    if image.suffix.lower() not in IMAGE_TYPES:
        return None
    name = hashlib.sha256(str(image.relative_to(ROOT)).encode()).hexdigest()[:20] + ".webp"
    path = output / "thumbs" / name
    if not path.exists():
        with Image.open(image) as source:
            preview = ImageOps.exif_transpose(source).convert("RGBA")
            preview.thumbnail((560, 560), Image.Resampling.LANCZOS)
            preview.save(path, quality=82, method=4)
    return f"thumbs/{name}"


def items_for(output):
    items = []
    for number, line in enumerate((ROOT / "CATALOG.md").read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) != 10:
            raise ValueError(f"CATALOG.md:{number}: se esperaban 10 columnas")
        identifier, name, category, _, version, _, file, status, _, description = cells
        title_link = LINK.fullmatch(name)
        file_link = LINK.fullmatch(file)
        if not title_link or not file_link:
            raise ValueError(f"CATALOG.md:{number}: faltan enlaces de ficha o archivo")
        title, card_path = title_link.groups()
        format_name, asset_path = file_link.groups()
        asset = repository_path(asset_path)
        repository_path(card_path)
        key = category_for(category.strip("`"))
        items.append({
            "id": identifier.strip("`"), "title": title,
            "category": key, "categoryLabel": CATEGORIES[key],
            "version": version.strip("`"), "status": status.strip("`"),
            "description": description.replace(r"\|", "|"),
            "format": format_name, "thumbnail": thumbnail(asset, output),
            "file": REPO + quote(asset_path), "card": REPO + quote(card_path),
        })
    return items


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    (output / "thumbs").mkdir(exist_ok=True)
    for name in ("index.html", "catalog.css", "catalog.js"):
        shutil.copyfile(ROOT / "site" / name, output / name)
    logo = repository_path("masters/logo/bujia-oval-logo-v1.0.0-red-cream.png")
    with Image.open(logo) as source:
        stamp = source.convert("RGBA")
        stamp = stamp.crop(stamp.getbbox())
        stamp.thumbnail((216, 98), Image.Resampling.LANCZOS)
        stamp.save(output / "logo.png")
    items = items_for(output)
    items.sort(key=lambda item: (item["status"] != "approved", item["title"].casefold(), item["version"]))
    data = {"categories": list(CATEGORIES.items()), "items": items}
    (output / "catalog-data.js").write_text(
        "window.catalog = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8"
    )
    print(f"{len(items)} recursos en el catálogo")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build(parser.parse_args().output)
