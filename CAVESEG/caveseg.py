import os
from ultralytics import YOLO
from tkinter import Tk, filedialog
import cv2

def select_images():
    """Open a file dialog to select images."""
    Tk().withdraw()  # Hides the root Tkinter window
    file_paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return list(file_paths)

def run_yolo_on_images(model_path, image_paths, output_dir="results"):
    """
    Runs YOLO model on selected images and saves the results.

    Args:
        model_path (str): Path to the YOLO model file (e.g., 'best.pt').
        image_paths (list of str): List of image file paths.
        output_dir (str): Directory to save the output images.
    """
    # Load the YOLO model
    model = YOLO(model_path)

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    for image_path in image_paths:
        # Run YOLO model on the image
        results = model(image_path)

        # Save the results (annotated image)
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        results.save(save_dir=output_dir)
        print(f"Processed {image_path}, results saved to {output_path}")

def main():
    # Select the YOLO model path
    model_path = "best.pt"  # Change this to your model path

    # Select images to process
    image_paths = select_images()
    if not image_paths:
        print("No images selected. Exiting...")
        return

    # Run YOLO on the selected images
    run_yolo_on_images(model_path, image_paths)

if __name__ == "__main__":
    main()
