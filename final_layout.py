from PIL import Image
import os
import re


def get_images_by_row():
    images = {}
    pattern = re.compile(r"(\d+)_(\d+)\.png")

    for file in os.listdir():
        match = pattern.match(file)
        if match:
            row = int(match.group(1))
            if row not in images:
                images[row] = []
            images[row].append(file)

    # Sort rows and images within each row
    sorted_images = {
        row: sorted(
            images[row], key=lambda x: int(re.search(r"_(\d+)\.png", x).group(1))
        )
        for row in sorted(images.keys())
    }
    return sorted_images


def create_final_layout(output_filename="finalLayout.png", dpi=72):
    images_by_row = get_images_by_row()

    def mm_to_px(mm):
        return int((mm / 25.4) * dpi)

    margin = mm_to_px(40)
    spacing = mm_to_px(25)

    row_heights = []
    row_images = []

    for row in images_by_row.values():
        imgs = [Image.open(img) for img in row]
        row_height = max(img.height for img in imgs)
        row_width = sum(img.width for img in imgs) + spacing * (len(imgs) - 1)
        row_images.append((imgs, row_width, row_height))
        row_heights.append(row_height)

    total_width = max(row_width for _, row_width, _ in row_images) + 2 * margin
    total_height = sum(row_heights) + spacing * (len(row_heights) - 1) + 2 * margin

    final_image = Image.new("RGB", (total_width, total_height), "white")
    y_offset = margin

    for imgs, row_width, row_height in row_images:
        x_offset = margin
        for img in imgs:
            final_image.paste(img, (x_offset, y_offset))
            x_offset += img.width + spacing
        y_offset += row_height + spacing

    final_image.save(output_filename)
    print(f"Final layout saved as {output_filename}")


if __name__ == "__main__":
    create_final_layout()
