"""Verify that the checked-in merged SolarIcons font matches its sources.

Run with:
  python tool/verify_merged_font.py

Requires FontTools. The verifier never writes into the repository.
"""

from __future__ import annotations

import importlib.util
import re
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MERGE_SCRIPT = ROOT / "tool" / "merge_fonts.py"


def load_merge_module():
    spec = importlib.util.spec_from_file_location("merge_fonts", MERGE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {MERGE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exported_code_points(path: Path) -> set[int]:
    return {
        int(code_point, 16)
        for code_point in re.findall(
            r"IconData\((0x[0-9a-fA-F]+),", path.read_text(encoding="utf-8")
        )
    }


def main() -> None:
    merge = load_merge_module()
    merged = merge.TTFont(merge.OUTPUT_FONT)
    merged_cmap = merge.primary_cmap(merged)
    expected_signatures: dict[int, tuple[object, ...]] = {}
    with tempfile.TemporaryDirectory(prefix="solar-icons-verify-") as temp_dir:
        temp_dir = Path(temp_dir)
        input_paths: list[Path] = []
        for style, filename, dart_file, start in merge.SOURCES:
            mapping, signatures = merge.remap_font(
                merge.FONT_DIR / filename, temp_dir / filename, start, style
            )
            input_paths.append(temp_dir / filename)
            expected_signatures.update(
                {mapping[source]: signature for source, signature in signatures.items()}
            )
            exports = exported_code_points(ROOT / dart_file)
            mapped = set(mapping.values())
            unknown_exports = exports - mapped
            missing_glyphs = exports - set(merged_cmap)
            if unknown_exports or missing_glyphs:
                raise ValueError(
                    f"{dart_file}: invalid exports; "
                    f"unmapped={sorted(hex(code) for code in unknown_exports)}, "
                    f"missing={sorted(hex(code) for code in missing_glyphs)}"
                )

        expected = merge.Merger().merge(input_paths)
        mismatches = [
            code_point
            for code_point, signature in expected_signatures.items()
            if merge.glyph_signature(expected, code_point) != signature
        ]
        if mismatches:
            raise ValueError(
                "Merging changed source glyph outlines; first: "
                + ", ".join(hex(code_point) for code_point in mismatches[:5])
            )

    names = {(record.nameID, record.toUnicode()) for record in merged["name"].names}
    if (1, "SolarIcons") not in names or (6, "SolarIcons-Regular") not in names:
        raise ValueError("Merged font has incorrect SolarIcons name metadata")

    print("Verified the merged font, source glyphs, and Dart exports.")


if __name__ == "__main__":
    main()
