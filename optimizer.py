from PIL import Image
import os

def optimize_png(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.png'):
                filepath = os.path.join(root, file)
                img = Image.open(filepath)
                
                # Resize if too large (adjust as needed)
                max_size = (1200, 1200)  # Max dimensions
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save optimized
                img.save(filepath, optimize=True, quality=85)
                print(f"Optimized: {file}")

# Run on all folders
for folder in ['USA_easy', 'USA_med', 'USA_extreme', 'NA_easy', 'NA_med', 'NA_extreme']:
    if os.path.exists(folder):
        print(f"Processing {folder}...")
        optimize_png(folder)