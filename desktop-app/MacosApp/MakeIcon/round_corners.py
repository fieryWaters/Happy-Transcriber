from PIL import Image, ImageDraw, ImageOps
import sys

def round_image_corners(image_path, output_path, radius_ratio=0.25):
    # Load the image
    img = Image.open(image_path)

    # Determine the radius for the rounded corners
    radius = int(radius_ratio * min(img.size))

    # Create a mask with rounded corners
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)

    # Apply the mask to the image
    rounded_img = Image.composite(img, Image.new("RGBA", img.size, (0, 0, 
0, 0)), mask)
    rounded_img.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python round_corners.py <input_image_path> <output_image_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]
    round_image_corners(input_image_path, output_image_path)

