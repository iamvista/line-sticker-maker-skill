#!/usr/bin/env python3
"""
LINE Sticker Post-Processor

Converts raw AI-generated sticker images to LINE Creators Market format:
- Sticker body: 370x320px PNG with transparent background
- Main image: 240x240px PNG with transparent background
- Chat tab icon: 96x74px PNG with transparent background

Usage:
    python3 process_stickers.py --input-dir ./originals --output-dir ./line_format
    python3 process_stickers.py --input-dir ./originals --output-dir ./line_format --padding-override "04:55,08:45"
"""
import argparse
import os
import sys
from PIL import Image


def remove_white_bg(img, threshold=240):
    """Remove white/near-white background and make it transparent."""
    img = img.convert("RGBA")
    pixels = list(img.getdata())
    new_pixels = []
    for r, g, b, a in pixels:
        if r > threshold and g > threshold and b > threshold:
            new_pixels.append((255, 255, 255, 0))
        else:
            new_pixels.append((r, g, b, a))
    img.putdata(new_pixels)
    return img


def fit_to_size(img, target_w, target_h, padding=10):
    """Resize image to fit within target size with padding, centered."""
    avail_w = target_w - 2 * padding
    avail_h = target_h - 2 * padding

    ratio = min(avail_w / img.width, avail_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.paste(resized, (x, y), resized)

    return canvas


def parse_padding_overrides(override_str):
    """Parse padding override string like '04:55,08:45' into a dict."""
    overrides = {}
    if not override_str:
        return overrides
    for pair in override_str.split(","):
        parts = pair.strip().split(":")
        if len(parts) == 2:
            idx = int(parts[0])
            pad = int(parts[1])
            overrides[idx] = pad
    return overrides


def main():
    parser = argparse.ArgumentParser(description="LINE Sticker Post-Processor")
    parser.add_argument("--input-dir", required=True, help="Directory with original sticker PNGs")
    parser.add_argument("--output-dir", required=True, help="Output directory for LINE-format files")
    parser.add_argument("--default-padding", type=int, default=10, help="Default padding in px (default: 10)")
    parser.add_argument("--bg-threshold", type=int, default=240, help="White background threshold 0-255 (default: 240)")
    parser.add_argument("--padding-override", type=str, default="", help="Per-sticker padding overrides, e.g. '04:55,08:45'")
    parser.add_argument("--main-source", type=int, default=1, help="Which sticker to use for main image (default: 1)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    overrides = parse_padding_overrides(args.padding_override)

    # Find all sticker files (sorted)
    sticker_files = sorted([
        f for f in os.listdir(args.input_dir)
        if f.startswith("sticker_") and f.endswith(".png")
    ])

    if not sticker_files:
        print(f"No sticker_*.png files found in {args.input_dir}")
        sys.exit(1)

    print(f"=== LINE Sticker Post-Processor ===")
    print(f"Found {len(sticker_files)} stickers\n")

    # Process sticker bodies (370x320px)
    for i, filename in enumerate(sticker_files, 1):
        src_path = os.path.join(args.input_dir, filename)
        img = Image.open(src_path)
        img = remove_white_bg(img, args.bg_threshold)

        pad = overrides.get(i, args.default_padding)
        sticker = fit_to_size(img, 370, 320, padding=pad)

        out_name = f"{i:02d}.png"
        out_path = os.path.join(args.output_dir, out_name)
        sticker.save(out_path, "PNG")

        pad_info = f" (padding={pad})" if pad != args.default_padding else ""
        print(f"  [{i:02d}] {filename} -> {out_name} (370x320){pad_info}")

    # Main image (240x240px)
    main_idx = args.main_source - 1
    if main_idx < len(sticker_files):
        print(f"\n--- Main Image (240x240) ---")
        src = os.path.join(args.input_dir, sticker_files[main_idx])
        img = Image.open(src)
        img = remove_white_bg(img, args.bg_threshold)
        main_img = fit_to_size(img, 240, 240, padding=10)
        main_img.save(os.path.join(args.output_dir, "main.png"), "PNG")
        print(f"  main.png from {sticker_files[main_idx]}")

    # Chat tab icon (96x74px)
    if main_idx < len(sticker_files):
        print(f"\n--- Chat Tab Icon (96x74) ---")
        tab_img = fit_to_size(img, 96, 74, padding=4)
        tab_img.save(os.path.join(args.output_dir, "tab.png"), "PNG")
        print(f"  tab.png from {sticker_files[main_idx]}")

    # Summary
    total = len(os.listdir(args.output_dir))
    print(f"\n=== Done! {total} files in {args.output_dir} ===")

    # Verify
    print(f"\n--- Verification ---")
    for f in sorted(os.listdir(args.output_dir)):
        if f.endswith(".png"):
            fpath = os.path.join(args.output_dir, f)
            im = Image.open(fpath)
            size_kb = os.path.getsize(fpath) / 1024
            status = "OK" if size_kb < 1024 else "TOO LARGE"
            print(f"  {f:20s} {im.size[0]}x{im.size[1]}  {size_kb:.0f}KB  {status}")


if __name__ == "__main__":
    main()
