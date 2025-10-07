# Digital Conveyor Line with random effects
# Roni Bandini
# August 2025
# MIT License

from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import os
import time
import random
from itertools import cycle

# === SETTINGS ===
displayTime = 3  # seconds per image
modification_rate = 0.1  # e.g. 0.1 = 1 out of 10 images modified
image_folder = r"C:\Users\XXXX\Desktop\samples"

def pixelate(image, factor):
    """Applies a pixelation effect to an image."""
    small = image.resize((max(1, image.width // factor), max(1, image.height // factor)), Image.NEAREST)
    return small.resize(image.size, Image.NEAREST)

def process_image(img_path):
    """Loads and potentially modifies an image, with error handling."""
    try:
        img = Image.open(img_path)
        # Pillow's lazy loading can hide errors. We force a full load here.
        img.load() 
        filename = os.path.basename(img_path)

        if random.random() < modification_rate:
            factor = random.randint(2, 8)
            degraded = pixelate(img, factor=factor)
            contrast_factor = round(random.choice([
                random.uniform(0.0, 0.2),    # mushy gray
                random.uniform(0.5, 1.8),    # mild
                random.uniform(3.0, 5.0)     # extreme
            ]), 2)
            degraded = ImageEnhance.Contrast(degraded).enhance(contrast_factor)
            title = f"{filename} - modified (px {factor}, contrast {contrast_factor})"
        else:
            degraded = img
            title = f"{filename} - original"
        
        return degraded, title
    except (OSError, IOError) as e:
        print(f"⚠️  Error processing image {img_path}: {e}")
        # Return a placeholder or None to indicate failure
        return None, f"Error: {os.path.basename(img_path)}"

# === Main Loop with Single Figure ===
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
if not image_files:
    print("No images found in the specified folder.")
    exit()

image_iterator = cycle(image_files)

# Create the figure and axes once
fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

mng = plt.get_current_fig_manager()
try:
    mng.full_screen_toggle()
except Exception:
    try:
        mng.window.state("zoomed")
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass

ax.axis("off") # Turn off axes to remove all borders and labels

title_text = fig.text(0.01, 0.99, "", color="white", fontsize=14,
                      ha="left", va="top", backgroundcolor="black")

try:
    while True:
        degraded, title = None, None
        
        # Keep trying to get a valid image
        while degraded is None:
            img_path = next(image_iterator)
            degraded, title = process_image(img_path)

        # Clear the previous image from the axes
        ax.cla()
        ax.axis("off")
        
        # Display the new image on the same axes
        ax.imshow(degraded, aspect='auto')
        
        # Update the title text
        title_text.set_text(title)
        
        # Redraw the figure
        fig.canvas.draw_idle()
        plt.pause(displayTime)

except KeyboardInterrupt:
    print("Conveyor stopped by user.")
    plt.close('all')