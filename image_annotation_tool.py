import os
import cv2
import base64
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuration
IMAGE_FOLDER = "/Users/a906075/dataset-1"
SAVE_FOLDER = "/Users/a906075/dataset-1/objects"

# Create save folder if it doesn't exist
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Get all JPG images and sort them
images = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
index = 0

def encode_image(path):
    """Encode image to base64 string"""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image {path}: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main HTML interface"""
    try:
        with open("index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("""
        <html>
        <body>
        <h1>Error: index.html not found</h1>
        <p>Please make sure index.html is in the same directory as this Python file.</p>
        </body>
        </html>
        """, status_code=404)

@app.get("/get_image")
async def get_image():
    """Get current image data"""
    global index
    
    if not images:
        return JSONResponse({"error": "No images found"}, status_code=404)
    
    if index >= len(images):
        index = len(images) - 1
    
    img_path = os.path.join(IMAGE_FOLDER, images[index])
    img_b64 = encode_image(img_path)
    
    if img_b64 is None:
        return JSONResponse({"error": "Failed to encode image"}, status_code=500)
    
    return JSONResponse({
        "original": images[index],
        "save_as": os.path.splitext(images[index])[0] + "_obj.jpg",
        "image": img_b64,
        "index": index,
        "total": len(images)
    })

@app.post("/save_bbox")
async def save_bbox(request: Request):
    """Save cropped bounding box as new image with specified annotation type"""
    global index
    
    try:
        data = await request.json()
        x, y = int(data["x"]), int(data["y"])
        annotation_type = data.get("type", "a")  # Default to 'a' if not specified
        
        # Fixed boundary box size: 100x100 (updated from 50x50)
        w, h = 100, 100
        
        img_path = os.path.join(IMAGE_FOLDER, images[index])
        img = cv2.imread(img_path)
        
        if img is None:
            return JSONResponse({"error": "Failed to load image"}, status_code=500)
        
        # Ensure bounding box is within image bounds
        img_height, img_width = img.shape[:2]
        
        # Adjust coordinates to ensure 100x100 box stays within image bounds
        if x + w > img_width:
            x = img_width - w
        if y + h > img_height:
            y = img_height - h
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        # If image is smaller than 100x100, handle gracefully
        if img_width < 100 or img_height < 100:
            w = min(100, img_width)
            h = min(100, img_height)
        
        # Crop the image
        crop = img[y:y+h, x:x+w]
        
        # Generate save path with annotation type
        base, ext = os.path.splitext(images[index])
        save_path = os.path.join(SAVE_FOLDER, f"{base}_{annotation_type}{ext}")
        
        # Handle duplicate filenames
        counter = 1
        while os.path.exists(save_path):
            save_path = os.path.join(SAVE_FOLDER, f"{base}_{annotation_type}_{counter}{ext}")
            counter += 1
        
        # Save the cropped image
        success = cv2.imwrite(save_path, crop)
        
        if not success:
            return JSONResponse({"error": "Failed to save image"}, status_code=500)
        
        return JSONResponse({
            "status": "saved",
            "path": save_path,
            "filename": os.path.basename(save_path),
            "type": annotation_type,
            "size": f"{w}x{h}"
        })
        
    except Exception as e:
        print(f"Error saving bbox: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/next")
async def next_image():
    """Go to next image"""
    global index
    if index < len(images) - 1:
        index += 1
    return JSONResponse({"index": index, "total": len(images)})

@app.post("/prev")
async def prev_image():
    """Go to previous image"""
    global index
    if index > 0:
        index -= 1
    return JSONResponse({"index": index, "total": len(images)})

@app.get("/status")
async def get_status():
    """Get current status"""
    return JSONResponse({
        "current_index": index,
        "total_images": len(images),
        "current_image": images[index] if images else None,
        "images_folder": IMAGE_FOLDER,
        "save_folder": SAVE_FOLDER
    })

if __name__ == "__main__":
    print(f"Starting image annotation server...")
    print(f"Images folder: {IMAGE_FOLDER}")
    print(f"Save folder: {SAVE_FOLDER}")
    print(f"Found {len(images)} images")
    
    if not images:
        print("Warning: No images found in the specified folder!")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)




