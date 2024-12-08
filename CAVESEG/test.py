from PIL import Image

image_path = "path/to/your/image.jpg"
try:
    with Image.open(image_path) as img:
        print(f"{image_path} is a valid {img.format} image.")
except IOError:
    print(f"Cannot open {image_path} as an image.")