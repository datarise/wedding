#!/usr/bin/env python3

from PIL import Image
import os
import glob

# Get all jpg files from static/images
image_dir = "static/images"
images = sorted([f for f in glob.glob(f"{image_dir}/*.jpg") + glob.glob(f"{image_dir}/*.JPG") 
                 if not f.endswith('collage.jpg') and not f.endswith('hero.jpg')])

print(f"Found {len(images)} images: {images}")

# Create collage: 3x2 grid (3 columns, 2 rows)
# Each image: 300x300
# Total: 900x600

collage_width = 900
collage_height = 600
tile_size = 300

# Create white background
collage = Image.new('RGB', (collage_width, collage_height), 'white')

# Paste images in 3x2 grid
positions = [
    (0, 0),      # Top left
    (300, 0),    # Top middle
    (600, 0),    # Top right
    (0, 300),    # Bottom left
    (300, 300),  # Bottom middle
    (600, 300)   # Bottom right
]

for i in range(min(6, len(images))):
    img = Image.open(images[i])
    
    # Crop to square (centered) first
    width, height = img.size
    square_size = min(width, height)
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = left + square_size
    bottom = top + square_size
    img_square = img.crop((left, top, right, bottom))
    
    # Now resize the square to tile_size
    img_resized = img_square.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
    
    collage.paste(img_resized, positions[i])
    print(f"Pasted image {i+1} at {positions[i]}: {images[i]}")

# Save collage as hero.jpg
output_path = f"{image_dir}/hero.jpg"
collage.save(output_path, quality=85)
print(f"\nCollage created: {output_path}")
print(f"Collage size: {collage.size}")

