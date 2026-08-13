#!/usr/bin/env python3
"""Build generated/ white-label overlays from brand.json + logos/.

Usage:
  python apply-brand.py
  python apply-brand.py --brand brand.json

Re-run after editing brand.json or logos for a new customer.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required: pip install Pillow", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent


def load_brand(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("productName", "description", "themeColor", "logo"):
        if key not in data:
            raise SystemExit(f"brand.json missing '{key}'")
    if "white" not in data["logo"]:
        raise SystemExit("brand.json logo.white is required")
    return data


def trim_and_square(img: Image.Image, pad: int = 8) -> Image.Image:
    """Crop near-black margins; keep logo mark with transparent background."""
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if r < 28 and g < 28 and b < 28:
                pixels[x, y] = (0, 0, 0, 0)
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    cw, ch = cropped.size
    side = max(cw, ch) + pad * 2
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(cropped, ((side - cw) // 2, (side - ch) // 2), cropped)
    return canvas


def trim_mark(img: Image.Image, pad: int = 4) -> Image.Image:
    """Crop empty margins; keep transparent bg. Works for black or white marks."""
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    # Only clear fully-transparent-ish near-pure backgrounds that are already alpha;
    # for black marks, do NOT wipe black pixels — only crop by alpha bbox.
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    if pad:
        cw, ch = cropped.size
        canvas = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
        canvas.paste(cropped, (pad, pad), cropped)
        return canvas
    return cropped


def white_mark_from_dark_bg(img: Image.Image, pad: int = 8) -> Image.Image:
    """White logo on black/transparent → white mark, transparent bg, squared."""
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if r < 28 and g < 28 and b < 28:
                pixels[x, y] = (0, 0, 0, 0)
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    cw, ch = cropped.size
    side = max(cw, ch) + pad * 2
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(cropped, ((side - cw) // 2, (side - ch) // 2), cropped)
    return canvas


def black_mark_from_file(img: Image.Image, pad: int = 8) -> Image.Image:
    """Black mark on transparent → squared transparent PNG."""
    rgba = img.convert("RGBA")
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    cw, ch = cropped.size
    side = max(cw, ch) + pad * 2
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(cropped, ((side - cw) // 2, (side - ch) // 2), cropped)
    return canvas


def save_png_sizes(mark: Image.Image, out_dir: Path, theme: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, size in (("logo192.png", 192), ("logo512.png", 512)):
        if theme != "white":
            continue
        resized = mark.resize((size, size), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (size, size), (11, 61, 92, 255))
        tile.alpha_composite(resized)
        tile.convert("RGB").save(out_dir.parent / name, "PNG")

    if theme != "white":
        return

    fav_dir = out_dir.parent / "favicons"
    fav_dir.mkdir(parents=True, exist_ok=True)
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    ico_images = []
    for s in ico_sizes:
        r = mark.resize(s, Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", s, (11, 61, 92, 255))
        tile.alpha_composite(r)
        ico_images.append(tile.convert("RGBA"))
    ico_images[0].save(
        fav_dir / "favicon-32.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=ico_images[1:],
    )
    fav32 = mark.resize((32, 32), Image.Resampling.LANCZOS)
    tile32 = Image.new("RGBA", (32, 32), (11, 61, 92, 255))
    tile32.alpha_composite(fav32)
    tile32.save(fav_dir / "favicon-32.png", "PNG")


def write_stock_svg_placeholder(path: Path, product: str) -> None:
    path.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 214 37" width="214" height="37" role="img" aria-label="{product}">
  <image href="/brand/logo-white.png" xlink:href="/brand/logo-white.png" width="214" height="37" preserveAspectRatio="xMidYMid meet"/>
</svg>
''',
        encoding="utf-8",
    )


def write_inject_js(out: Path, brand: dict) -> None:
    name = brand["productName"]
    full = brand.get("productNameFull") or name

    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace("'", "\\'")

    template = (ROOT / "inject.template.js").read_text(encoding="utf-8")
    out.write_text(
        template.replace("__PRODUCT__", esc(name)).replace("__PRODUCT_FULL__", esc(full)),
        encoding="utf-8",
    )


AUTH_RESCUE_SCRIPT = r"""
    <style>
      /* Pre-paint: hide stock Bigcapital marks until Astrans inject replaces them. */
      [data-icon="bigcapital"],
      [data-icon="bigcapital-alt"],
      [data-icon="mini-bigcapital"],
      .bp4-icon-bigcapital,
      .bp4-icon-bigcapital-alt,
      .bp4-icon-mini-bigcapital,
      .bigcapital-logo {
        opacity: 0 !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
      }
      /* Auth route: hide stock wordmark SVGs before inject chrome mounts. */
      html.astrans-on-auth [data-icon="bigcapital"],
      html.astrans-on-auth [data-icon="bigcapital-alt"],
      html.astrans-on-auth [data-icon="mini-bigcapital"],
      html.astrans-on-auth .bp4-icon-bigcapital,
      html.astrans-on-auth .bp4-icon-bigcapital-alt,
      html.astrans-on-auth .bp4-icon-mini-bigcapital,
      html.astrans-on-auth .bigcapital-logo,
      html.astrans-on-auth svg[viewBox="0 0 214 37"],
      html.astrans-on-auth svg[viewBox="0 0 215 38"] {
        display: none !important;
      }
    </style>
    <script>
      /* Sync: mark /auth before first paint; unregister legacy SW. No DOM chrome here. */
      (function () {
        try {
          if (location.pathname.indexOf('/auth') === 0) {
            document.documentElement.classList.add('astrans-on-auth');
          }
        } catch (e) {}
        try {
          if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations()
              .then(function (rs) { rs.forEach(function (r) { r.unregister(); }); })
              .catch(function () {});
          }
        } catch (e) {}
      })();
    </script>
"""


def write_index_html(out: Path, brand: dict, stock: Path | None, inject_src: str) -> None:
    import re
    import time as _time

    name = brand["productName"]
    full = brand.get("productNameFull") or name
    desc = brand["description"]
    theme = brand["themeColor"]
    ver = str(int(_time.time()))
    inject_tag = f'<script src="{inject_src}?v={ver}" defer></script>'

    stock_html = None
    candidates = [
        stock,
        ROOT.parent / "patches" / "webapp-assets" / "index.html",
    ]
    for c in candidates:
        if c and c.exists():
            stock_html = c.read_text(encoding="utf-8")
            break

    if stock_html:
        html = stock_html
        html = html.replace("<title>Bigcapital</title>", f"<title>{full}</title>")
        html = html.replace(f"<title>{name}</title>", f"<title>{full}</title>")
        html = html.replace(
            'content="Bigcapital Financial Managment Software"',
            f'content="{desc}"',
        )
        if 'content="Bigcapital' in html:
            html = re.sub(
                r'content="Bigcapital[^"]*"',
                f'content="{desc}"',
                html,
            )
        if 'name="theme-color"' in html:
            html = re.sub(
                r'(<meta\s+name="theme-color"\s+content=")[^"]*(")',
                rf"\g<1>{theme}\2",
                html,
            )
        # Drop prior brand inject / rescue; re-insert clean ones.
        html = re.sub(
            r'\s*<script[^>]+/brand/[^"\']+\.js[^>]*></script>',
            "",
            html,
        )
        html = re.sub(
            r'\s*<script>\s*/\* (?:Quiet SW|Kill stale SW|Inline rescue|Unregister legacy SW).*?</script>',
            "",
            html,
            flags=re.S,
        )
        html = re.sub(
            r'\s*<style>\s*/\* Pre-paint: hide stock Bigcapital marks.*?</style>',
            "",
            html,
            flags=re.S,
        )
        # Strip accidental ?v= cache-busters on Vite entry assets (breaks login).
        html = re.sub(r'(/assets/[^"\']+\.(?:js|css))\?v=\d+', r"\1", html)
        html = html.replace(
            "</head>",
            AUTH_RESCUE_SCRIPT + f"\n    {inject_tag}\n  </head>",
        )
    else:
        html = f"""<!doctype html>
<html dir="ltr" lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="/favicons/favicon-32.ico" sizes="32x32" />
    <link rel="apple-touch-icon" href="/logo192.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="{theme}" />
    <meta name="description" content="{desc}" />
    <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate" />
    <link rel="manifest" href="/manifest.json" />
    <title>{full}</title>
    <script>
      (function () {{
        try {{
          var t =
            localStorage.getItem("theme") ||
            (window.matchMedia("(prefers-color-scheme: dark)").matches
              ? "dark"
              : "light");
          if (t === "dark") document.documentElement.classList.add("bp4-dark");
          else document.documentElement.classList.remove("bp4-dark");
        }} catch (e) {{}}
      }})();
    </script>
{AUTH_RESCUE_SCRIPT}
    {inject_tag}
    <script type="module" crossorigin src="/assets/index-C4jBpDeP.js"></script>
    <link rel="stylesheet" crossorigin href="/assets/index-WIyr6BOV.css">
  </head>
  <body>
    <script>
      (function () {{
        try {{
          var t =
            localStorage.getItem("theme") ||
            (window.matchMedia("(prefers-color-scheme: dark)").matches
              ? "dark"
              : "light");
          if (t === "dark") document.body.classList.add("bp4-dark");
          else document.body.classList.remove("bp4-dark");
        }} catch (e) {{}}
      }})();
    </script>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <div id="nprogress"></div>
  </body>
</html>
"""
    # Always avoid hard-locking dark mode in any stock template we used
    html = html.replace('<body class="bp4-dark">', "<body>")
    html = html.replace("<body class='bp4-dark'>", "<body>")
    # Strip any ?v= on Vite entry assets (breaks module graph / login in some browsers).
    html = re.sub(r'(/assets/[^"\']+\.(?:js|css))\?v=\d+', r"\1", html)
    # manifest.json is not an ES module — modulepreload freezes some browsers.
    html = html.replace(
        '<link rel="modulepreload" href="/manifest.json" />',
        '<link rel="manifest" href="/manifest.json" />',
    )
    html = html.replace(
        "<link rel='modulepreload' href='/manifest.json' />",
        "<link rel='manifest' href='/manifest.json' />",
    )
    # Normalize any leftover legacy inject paths to the versioned file.
    html = re.sub(
        r'src="/brand/inject\.js[^"]*"',
        f'src="{inject_src}?v={ver}"',
        html,
    )
    html = re.sub(
        r"src='/brand/inject\.js[^']*'",
        f"src='{inject_src}?v={ver}'",
        html,
    )
    out.write_text(html, encoding="utf-8")


def write_manifest(out: Path, brand: dict) -> None:
    name = brand["productName"]
    full = brand.get("productNameFull") or name
    theme = brand["themeColor"]
    manifest = {
        "short_name": name,
        "name": full,
        "icons": [
            {"src": "favicon.ico", "sizes": "64x64 32x32 24x24 16x16", "type": "image/x-icon"},
            {"src": "logo192.png", "type": "image/png", "sizes": "192x192"},
            {"src": "logo512.png", "type": "image/png", "sizes": "512x512"},
            {"src": "brand/logo-white.png", "type": "image/png", "sizes": "any"},
        ],
        "start_url": ".",
        "display": "standalone",
        "theme_color": theme,
        "background_color": "#000000",
    }
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply Bigcapital white-label brand pack")
    ap.add_argument("--brand", default=str(ROOT / "brand.json"))
    ap.add_argument("--stock-index", default="", help="Optional path to stock index.html")
    args = ap.parse_args()

    brand_path = Path(args.brand)
    brand = load_brand(brand_path)

    white_rel = brand["logo"]["white"]
    white_path = (ROOT / white_rel).resolve()
    if not white_path.exists():
        raise SystemExit(f"Logo not found: {white_path}")

    black_rel = brand["logo"].get("black")
    black_path = (ROOT / black_rel).resolve() if black_rel else None
    if black_rel and not black_path.exists():
        raise SystemExit(f"Black logo not found: {black_path}")

    generated = ROOT / "generated"
    if generated.exists():
        shutil.rmtree(generated)
    brand_dir = generated / "brand"
    brand_dir.mkdir(parents=True)

    white_mark = white_mark_from_dark_bg(Image.open(white_path))
    white_mark.save(brand_dir / "logo-white.png", "PNG")
    # Default logo.png = white (matches historical dark-first UI)
    white_mark.save(brand_dir / "logo.png", "PNG")
    save_png_sizes(white_mark, brand_dir, "white")

    if black_path:
        black_mark = black_mark_from_file(Image.open(black_path))
        black_mark.save(brand_dir / "logo-black.png", "PNG")
    else:
        # Invert white mark → black for light mode fallback
        inv = white_mark.copy()
        px = inv.load()
        for y in range(inv.size[1]):
            for x in range(inv.size[0]):
                r, g, b, a = px[x, y]
                if a > 0:
                    px[x, y] = (0, 0, 0, a)
        inv.save(brand_dir / "logo-black.png", "PNG")

    write_stock_svg_placeholder(generated / "bigcapital.svg", brand["productName"])
    import time as _time

    brand_ver = str(int(_time.time()))
    inject_name = f"astrans-inject-{brand_ver}.js"
    write_inject_js(brand_dir / inject_name, brand)
    # Keep legacy path updated too (cached HTML may still request it).
    write_inject_js(brand_dir / "inject.js", brand)
    stock = Path(args.stock_index) if args.stock_index else None
    write_index_html(
        generated / "index.html",
        brand,
        stock,
        inject_src=f"/brand/{inject_name}",
    )
    write_manifest(generated / "manifest.json", brand)

    fav = generated / "favicons" / "favicon-32.ico"
    if fav.exists():
        shutil.copy2(fav, generated / "favicon.ico")

    print(f"OK — wrote {generated}")
    print(f"  product: {brand['productName']}")
    print(f"  white:   {white_path.name}")
    print(f"  black:   {black_path.name if black_path else '(inverted from white)'}")


if __name__ == "__main__":
    main()
