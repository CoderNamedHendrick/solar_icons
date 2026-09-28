"""Merge Solar icon fonts and regenerate their Dart IconData providers.

Requires FontTools in the repository-local .venv:
  .\\.venv\\Scripts\\python.exe tool\\merge_fonts.py
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from fontTools.merge import Merger
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
TEMP_DIR = ROOT / ".tmp" / "merged-font-inputs"
OUTPUT_FONT = FONT_DIR / "SolarIcons.ttf"
OUTPUT_MAPPING = ROOT / ".tmp" / "solar_icons_codepoints.json"
PRIVATE_USE_START = 0xE000

# Reserve 0x500 code points per family. The current source fonts each fit in
# their range, and their new code points stay stable when another family gains
# glyphs.
SOURCES = (
    ("bold", "SolarIconsBold.ttf", "lib/src/solar_icons_bold.dart", 0xE000),
    ("broken", "SolarIconsBroken.ttf", "lib/src/solar_icons_broken.dart", 0xE500),
    ("outline", "SolarIconsOutline.ttf", "lib/src/solar_icons_outline.dart", 0xEA00),
)


def primary_cmap(font: TTFont) -> dict[int, str]:
    tables = [table for table in font["cmap"].tables if table.isUnicode()]
    if not tables:
        raise ValueError("Font has no Unicode cmap")
    return max(tables, key=lambda table: len(table.cmap)).cmap


def glyph_signature(font: TTFont, code_point: int) -> tuple[object, ...]:
    glyph_name = primary_cmap(font)[code_point]
    pen = RecordingPen()
    font.getGlyphSet()[glyph_name].draw(pen)
    return tuple(pen.value)


def remap_font(
    source: Path, destination: Path, start: int, namespace: str
) -> tuple[dict[int, int], dict[int, tuple[object, ...]]]:
    font = TTFont(source)
    # The fonts also map .notdef/control glyphs at 0x0, 0x1, and 0x20. They
    # are not part of the IconData API and must retain their original cmap
    # entries; only the private-use icon glyphs are merged and remapped.
    code_points = sorted(code_point for code_point in primary_cmap(font) if code_point >= PRIVATE_USE_START)
    if not code_points:
        raise ValueError(f"{source.name} has no mapped glyphs")

    source_start = code_points[0]
    source_end = code_points[-1]
    if source_end - source_start >= 0x500:
        raise ValueError(f"{source.name} exceeds its reserved private-use range")

    mapping = {code_point: start + code_point - source_start for code_point in code_points}
    if max(mapping.values()) > 0xF8FF:
        raise ValueError(f"{source.name} does not fit in the BMP private-use area")

    signatures = {code_point: glyph_signature(font, code_point) for code_point in code_points}
    glyph_names = {
        glyph_name: glyph_name if glyph_name == ".notdef" else f"{namespace}_{glyph_name}"
        for glyph_name in font.getGlyphOrder()
    }
    glyph_table = font["glyf"]
    glyph_table.glyphs = {
        glyph_names[glyph_name]: glyph for glyph_name, glyph in glyph_table.glyphs.items()
    }
    for glyph in glyph_table.glyphs.values():
        if glyph.isComposite():
            for component in glyph.components:
                component.glyphName = glyph_names.get(component.glyphName, component.glyphName)
    font["hmtx"].metrics = {
        glyph_names[glyph_name]: metric for glyph_name, metric in font["hmtx"].metrics.items()
    }
    font.setGlyphOrder([glyph_names[glyph_name] for glyph_name in font.getGlyphOrder()])
    # The source fonts use a format-3 post table, which has no glyph names.
    # Preserve our namespaced glyph identities by writing a format-2 table.
    font["post"].formatType = 2.0
    font["post"].extraNames = []
    font["post"].mapping = {}
    for table in font["cmap"].tables:
        table.cmap = {
            mapping.get(code_point, code_point): glyph_names.get(glyph_name, glyph_name)
            for code_point, glyph_name in table.cmap.items()
        }

    # Preserve the source glyph bounds and bearings. FontTools otherwise
    # recalculates some bounds while serializing and shifts those outlines.
    font.recalcBBoxes = False
    font.save(destination)
    remapped_font = TTFont(destination)
    remap_mismatches = [
        hex(new_code_point)
        for old_code_point, new_code_point in mapping.items()
        if glyph_signature(remapped_font, new_code_point) != signatures[old_code_point]
    ]
    if remap_mismatches:
        raise ValueError(
            f"Remapping {source.name} changed {len(remap_mismatches)} glyph outlines; "
            f"first: {', '.join(remap_mismatches[:5])}"
        )
    return mapping, signatures


def set_family_name(font: TTFont) -> None:
    for record in font["name"].names:
        if record.nameID == 1:  # Font Family
            record.string = "SolarIcons".encode("utf-16-be") if record.isUnicode() else b"SolarIcons"
        elif record.nameID == 2:  # Font Subfamily
            record.string = "Regular".encode("utf-16-be") if record.isUnicode() else b"Regular"
        elif record.nameID == 4:  # Full font name
            record.string = "SolarIcons Regular".encode("utf-16-be") if record.isUnicode() else b"SolarIcons Regular"
        elif record.nameID == 6:  # PostScript name
            record.string = b"SolarIcons-Regular"


def update_dart_provider(path: Path, mapping: dict[int, int], source_text: str | None = None) -> None:
    text = source_text if source_text is not None else path.read_text(encoding="utf-8")
    is_merged_provider = bool(
        re.search(r"static const\s+_fontFamily\s*=\s*'SolarIcons';", text)
    )
    if "@staticIconProvider" not in text:
        text = text.replace("class SolarIcons", "@staticIconProvider\nclass SolarIcons", 1)
    text = re.sub(
        r"static const\s+_fontFamily\s*=\s*'[^']+';",
        "static const _fontFamily = 'SolarIcons';",
        text,
    )
    # Keep the existing generated single-line style. Dart format would expand
    # every declaration and make a code-point-only update look like a rewrite.
    text = re.sub(r"(static const \w+)\s*=\s*\n\s*", r"\1 = ", text)
    text = re.sub(
        r"(static const \w+)\s*=\s*IconData\(\s*(0x[0-9a-fA-F]+)\s*,\s*fontFamily: _fontFamily,\s*fontPackage: 'solar_icons',\s*\)",
        r"\1 = IconData(\2, fontFamily: _fontFamily, fontPackage: 'solar_icons')",
        text,
    )

    def replace_icon_data(match: re.Match[str]) -> str:
        code_point = int(match.group(1), 16)
        if is_merged_provider and code_point in mapping.values():
            return f"IconData(0x{code_point:x},"
        if code_point in mapping:
            return f"IconData(0x{mapping[code_point]:x},"
        if code_point in mapping.values():
            return f"IconData(0x{code_point:x},"
        raise ValueError(f"{path}: code point {match.group(1)} is absent from its font")

    text, replacements = re.subn(r"IconData\((0x[0-9a-fA-F]+),", replace_icon_data, text)
    if replacements == 0:
        raise ValueError(f"{path}: no IconData constants found")
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--from-git-head",
        action="store_true",
        help="Regenerate providers from their pre-merge source in Git HEAD.",
    )
    args = parser.parse_args()
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True)

    input_paths: list[Path] = []
    all_mappings: dict[str, dict[str, str]] = {}
    expected_signatures: dict[int, tuple[object, ...]] = {}
    for style, filename, dart_file, start in SOURCES:
        remapped = TEMP_DIR / filename
        mapping, signatures = remap_font(FONT_DIR / filename, remapped, start, style)
        input_paths.append(remapped)
        source_text = None
        if args.from_git_head:
            source_text = subprocess.check_output(
                ["git", "show", f"HEAD:{dart_file}"], cwd=ROOT, text=True
            )
        update_dart_provider(ROOT / dart_file, mapping, source_text)
        all_mappings[style] = {f"0x{old:x}": f"0x{new:x}" for old, new in mapping.items()}
        expected_signatures.update({mapping[old]: signature for old, signature in signatures.items()})

    merged = Merger().merge(input_paths)
    mismatches = [
        code_point
        for code_point, signature in expected_signatures.items()
        if glyph_signature(merged, code_point) != signature
    ]
    if mismatches:
        samples = ", ".join(
            f"{hex(code_point)}->{primary_cmap(merged)[code_point]}" for code_point in mismatches[:5]
        )
        raise ValueError(f"Merged font changed {len(mismatches)} glyph outlines; first: {samples}")
    set_family_name(merged)
    merged.save(OUTPUT_FONT)
    OUTPUT_MAPPING.write_text(json.dumps(all_mappings, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_FONT.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_MAPPING.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
