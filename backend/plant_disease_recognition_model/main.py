import os
import io
import numpy as np

os.environ["TF_USE_LEGACY_KERAS"] = "1"

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image

# Use EfficientNet's preprocessing function
from tf_keras.applications.efficientnet import preprocess_input

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "plant_disease_model_working.h5")
CLASSES_PATH = os.path.join(BASE_DIR, "classes.txt")

# Load model
print("Loading model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("Model loaded successfully!")
    print(f"Model input shape: {model.input_shape}")
except Exception as e:
    print(f"Error loading model: {e}")
    raise e

# Load Class Names
try:
    with open(CLASSES_PATH, "r") as f:
        class_names = [line.strip() for line in f.readlines()]
    print(f"Loaded {len(class_names)} classes: {class_names[:5]}...")
except FileNotFoundError:
    print(f"Error: classes.txt not found at {CLASSES_PATH}")
    class_names = []

# FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "active"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((224, 224))
        
        # Convert to numpy array (keep as 0-255 range)
        img_array = np.array(image, dtype=np.float32)
        
        # Apply EfficientNet preprocessing (handles normalization internally)
        img_array = preprocess_input(img_array)
        
        # Expand dimensions to create a batch
        img_batch = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = model.predict(img_batch, verbose=0)
        
        # Get top 3 predictions for debugging
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        print(f"Top 3 predictions: {[(class_names[i], f'{predictions[0][i]:.4f}') for i in top_indices]}")
        
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = class_names[predicted_class_index]
        confidence = float(np.max(predictions[0]))
        
        return {
            "class": predicted_class_name,
            "confidence": f"{confidence:.2%}"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
