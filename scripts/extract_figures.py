#!/usr/bin/env python3
"""PaperKraken figure extractor (PyMuPDF).

Run via: uv run --with pymupdf python extract_figures.py <mode> <paper.pdf> [options]

Modes:
  list                       Print detected figure captions + proposed crop rects (JSON).
  auto  -o DIR               Extract all detected figures as PNGs into DIR.
  crop  --page N --rect x0,y0,x1,y1 -o DIR [--name NAME]
                             Manual crop (PDF points, origin top-left).
  page  --page N -o DIR [--grid]
                             Render a full page; --grid overlays a 50pt coordinate grid.

Crops are heuristic (caption-anchored): ALWAYS verify each PNG visually and
re-crop with `crop` if clipped or polluted with body text.
"""
import argparse
import json
import re
import sys

import fitz  # PyMuPDF

DPI = 200
CAPTION_RE = re.compile(r"^(?:Figure|Fig\.?|그림)\s*(\d+)", re.IGNORECASE)
PAD = 10   # points of padding above/below detected content
HPAD = 14  # extra horizontal padding — tight side-crops clip edge characters


def find_captions(page):
    """Return [(fig_no, caption_rect, caption_text)] for caption blocks on this page."""
    out = []
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        m = CAPTION_RE.match(text.strip())
        if m:
            out.append((m.group(1), fitz.Rect(x0, y0, x1, y1), text.strip()[:120]))
    return out


def content_rect_above(page, cap_rect, captions):
    """Union of image/drawing rects sitting above a caption in the same column."""
    page_rect = page.rect
    # Column bounds: caption x-range widened moderately.
    col_x0 = max(page_rect.x0, cap_rect.x0 - 40)
    col_x1 = min(page_rect.x1, cap_rect.x1 + 40)
    # Vertical ceiling: bottom of the nearest caption above, else top margin.
    ceil = page_rect.y0 + 20
    for _, r, _ in captions:
        if r.y1 < cap_rect.y0 - 5 and r.y1 > ceil:
            ceil = r.y1

    cands = []
    for info in page.get_image_info():
        r = fitz.Rect(info["bbox"])
        if r.y1 <= cap_rect.y0 + 5 and r.y0 >= ceil - 5 and r.x1 > col_x0 and r.x0 < col_x1:
            if r.width > 20 and r.height > 20:
                cands.append(r)
    for d in page.get_drawings():
        r = d["rect"]
        if r.y1 <= cap_rect.y0 + 5 and r.y0 >= ceil - 5 and r.x1 > col_x0 and r.x0 < col_x1:
            if r.width > 15 and r.height > 8:
                cands.append(r)

    if not cands:
        return None
    u = cands[0]
    for r in cands[1:]:
        u |= r
    u = fitz.Rect(
        min(u.x0, cap_rect.x0) - HPAD,
        u.y0 - PAD,
        max(u.x1, cap_rect.x1) + HPAD,
        cap_rect.y0 - 2,
    )
    return u & page.rect


def detect(doc):
    found = []
    for pno in range(len(doc)):
        page = doc[pno]
        caps = find_captions(page)
        for fig_no, cap_rect, cap_text in caps:
            rect = content_rect_above(page, cap_rect, caps)
            found.append({
                "figure": fig_no,
                "page": pno + 1,
                "caption": cap_text,
                "rect": [round(v, 1) for v in rect] if rect else None,
            })
    return found


def save_crop(doc, page_no, rect, out_path):
    page = doc[page_no - 1]
    pix = page.get_pixmap(dpi=DPI, clip=fitz.Rect(rect))
    pix.save(out_path)
    print(f"saved {out_path} ({pix.width}x{pix.height}px)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["list", "auto", "crop", "page"])
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out", default=".")
    ap.add_argument("--page", type=int)
    ap.add_argument("--rect")
    ap.add_argument("--name")
    ap.add_argument("--grid", action="store_true")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)

    if args.mode == "list":
        print(json.dumps(detect(doc), indent=2, ensure_ascii=False))

    elif args.mode == "auto":
        results = detect(doc)
        n = 0
        for item in results:
            if item["rect"] is None:
                print(f"skip figure {item['figure']} p.{item['page']}: no content detected "
                      f"(use `page --page {item['page']} --grid` then `crop`)", file=sys.stderr)
                continue
            name = f"figure{item['figure']}"
            save_crop(doc, item["page"], item["rect"], f"{args.out}/{name}.png")
            n += 1
        print(f"extracted {n}/{len(results)} detected figures. VERIFY EACH PNG VISUALLY.")

    elif args.mode == "crop":
        if not (args.page and args.rect):
            sys.exit("crop requires --page and --rect x0,y0,x1,y1")
        rect = [float(v) for v in args.rect.split(",")]
        name = args.name or f"page{args.page}-crop"
        save_crop(doc, args.page, rect, f"{args.out}/{name}.png")

    elif args.mode == "page":
        if not args.page:
            sys.exit("page requires --page")
        page = doc[args.page - 1]
        pix = page.get_pixmap(dpi=DPI)
        out = f"{args.out}/page{args.page}{'-grid' if args.grid else ''}.png"
        if args.grid:
            # Overlay a 50pt grid with labels so crop rects can be read off visually.
            shape = page.new_shape()
            step = 50
            x = page.rect.x0
            while x < page.rect.x1:
                shape.draw_line((x, page.rect.y0), (x, page.rect.y1))
                x += step
            y = page.rect.y0
            while y < page.rect.y1:
                shape.draw_line((page.rect.x0, y), (page.rect.x1, y))
                y += step
            shape.finish(color=(1, 0, 0), width=0.4)
            shape.commit()
            for gx in range(0, int(page.rect.x1), step):
                page.insert_text((gx + 2, 10), str(gx), fontsize=6, color=(1, 0, 0))
            for gy in range(0, int(page.rect.y1), step):
                page.insert_text((2, gy + 8), str(gy), fontsize=6, color=(1, 0, 0))
            pix = page.get_pixmap(dpi=DPI)
        pix.save(out)
        print(f"saved {out} (page size: {page.rect.width:.0f}x{page.rect.height:.0f}pt, "
              f"grid step 50pt)" if args.grid else f"saved {out}")


if __name__ == "__main__":
    main()
