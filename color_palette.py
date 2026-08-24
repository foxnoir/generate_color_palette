from PIL import Image, ImageDraw
import argparse
import colorsys
import os

# Color types in rainbow order; pink sits next to red on the hue wheel.
_FAMILY_ORDER = (
    "red",
    "pink",
    "orange",
    "yellow",
    "green",
    "cyan",
    "blue",
    "purple",
    "neutral",
)


def _hex_to_rgb(hex_color):
    return (
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16),
    )


def luminance(hex_color):
    r, g, b = _hex_to_rgb(hex_color)
    return 0.299 * r + 0.587 * g + 0.114 * b


def color_family(hex_color):
    r, g, b = _hex_to_rgb(hex_color)
    h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    hue = h * 360

    if s < 0.12:
        return "neutral"
    if hue < 15 or (hue >= 345 and s >= 0.5):
        return "red"
    if 15 <= hue < 45:
        return "orange"
    if hue < 70:
        return "yellow"
    if hue < 165:
        return "green"
    if hue < 200:
        return "cyan"
    if hue < 255:
        return "blue"
    if hue < 290:
        return "purple"
    return "pink"


def sort_key(hex_color):
    # Type first, then light → dark within each type.
    return (_FAMILY_ORDER.index(color_family(hex_color)), -luminance(hex_color))


def create_color_palette(colors, output_filename="colorPalette.png"):
    # Convert colors from 0xAARRGGBB to #RRGGBB
    hex_colors = [f"#{color[-6:]}" for color in colors]

    hex_colors.sort(key=sort_key)
    
    # Define image size
    num_colors = len(hex_colors)
    box_size = 200
    spacing = 20
    margin = 15  # 5mm in pixels (approximately 15 pixels at 72 DPI)
    img_width = num_colors * (box_size + spacing) - spacing + 2 * margin
    img_height = box_size + 2 * margin
    
    # Create image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    # Draw color boxes
    for i, color in enumerate(hex_colors):
        x = margin + i * (box_size + spacing)
        y = margin
        draw.rectangle([x, y, x + box_size, y + box_size], fill=color, outline="black", width=5)
    
    # Save image
    img.save(output_filename)
    print(f"Image saved as: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a color palette as an image.")
    parser.add_argument("colors", nargs="+", help="List of colors in the format 0xAARRGGBB")
    parser.add_argument("--output", default="colorPalette.png", help="Name of the output file")
    args = parser.parse_args()
    
    create_color_palette(args.colors, args.output)
