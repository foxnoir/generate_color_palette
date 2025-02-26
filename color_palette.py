from PIL import Image, ImageDraw
import argparse
import os

def luminance(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b  # Standard luminance calculation

def create_color_palette(colors, output_filename="colorPalette.png"):
    # Convert colors from 0xAARRGGBB to #RRGGBB
    hex_colors = [f"#{color[-6:]}" for color in colors]
    
    # Sort colors by brightness (dark -> light)
    hex_colors.sort(key=luminance)
    
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
